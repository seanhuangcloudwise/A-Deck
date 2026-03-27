"""BP-10 Human-Driven vs System-Driven Split — BPMN loader.

Renders a process split by human/system/decision lanes with task-type icons.
Official anchor: OMG BPMN 2.0 by Example §6.3, formal spec §10.2.2.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event, add_task,
    add_gateway, add_sequence_flow, add_pool_header, add_lane_header,
    add_circle, add_annotation, set_title_subtitle,
    fit_x_scale, auto_text_color, connect_seq, slide_scale,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Pt
from pptx.enum.shapes import MSO_CONNECTOR_TYPE


# Task type icon text prefixes
_TASK_ICONS = {
    "user_task": "👤 ",
    "manual_task": "🤚 ",
    "service_task": "⚙ ",
    "script_task": "📜 ",
    "business_rule_task": "📋 ",
    "send_task": "✉→ ",
    "receive_task": "✉ ",
    "task": "",
}


def load_slide(ctx, data):
    """Render a Human vs System Split (BP-10) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    pool = content.get("pool", {"name": "Process"})
    lanes = content.get("lanes", [])
    nodes = content.get("nodes", [])
    flows = content.get("flows", [])
    boundary_events = content.get("boundary_events", [])
    automation_summary = content.get("automation_summary", {})

    # --- Geometry ---
    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.4 * sx)
    margin_t = emu(1.0 * sy)
    total_w = emu(9.2 * sx)
    total_h = emu(4.2 * sy)
    pool_header_w = emu(0.35 * sx)
    lane_header_w = emu(Size.LANE_HEADER_W * sx)

    n_lanes = max(len(lanes), 2)
    lane_h = total_h // n_lanes

    # Pool border
    add_rounded_rect(slide, margin_l, margin_t, total_w, total_h,
                     fill_rgb=None, line_rgb=C["dark"], line_width=LineWidth.POOL_BORDER,
                     corner_radius=Pt(0))

    # Pool header
    add_pool_header(slide, margin_l, margin_t, pool_header_w, total_h, C,
                    name=pool.get("name", ""))

    # Lane regions
    lane_regions = {}
    content_left = margin_l + pool_header_w + lane_header_w
    content_w = total_w - pool_header_w - lane_header_w

    if C.get("mode") == "dark":
        lane_type_colors = {
            "human": _mix(C["primary"], C["light"], 0.42),
            "system": _mix(C["secondary"], C["light"], 0.48),
            "decision": _mix(C["primary"], C["light"], 0.78),
        }
        lane_body_fills = {
            "human": _mix(C["light"], C.get("ink", C["light"]), 0.10),
            "system": _mix(C.get("secondary", C["primary"]), C["light"], 0.78),
            "decision": _mix(C.get("primary", C["secondary"]), C["light"], 0.90),
        }
    else:
        lane_type_colors = {
            "human": C["primary"],
            "system": C["secondary"],
            "decision": C["light"],
        }
        lane_body_fills = {
            "human": C["light"],
            "system": _mix(C.get("secondary", C["primary"]), C["light"], 0.82),
            "decision": _mix(C.get("primary", C["secondary"]), C["light"], 0.88),
        }

    for i, lane in enumerate(lanes):
        ly = margin_t + i * lane_h
        lid = lane.get("id", f"lane_{i}")
        ltype = lane.get("lane_type", "human")
        header_fill = lane_type_colors.get(ltype, C["primary"])

        # Lane header with custom color per type
        shape = add_rounded_rect(slide, margin_l + pool_header_w, ly,
                                 lane_header_w, lane_h,
                                 fill_rgb=header_fill, line_rgb=C["dark"],
                                 line_width=Pt(0.75), corner_radius=Pt(0),
                                 text=lane.get("name", lid),
                                 font_size=FontSize.LANE_NAME,
                                 font_color=auto_text_color(header_fill, C["dark"], C["white"]),
                                 bold=True)

        lane_regions[lid] = {
            "top": ly,
            "height": lane_h,
            "left": content_left,
            "width": content_w,
        }

        if C.get("mode") == "dark":
            add_rounded_rect(slide, content_left, ly, content_w, lane_h,
                             fill_rgb=lane_body_fills.get(ltype, C["light"]),
                             line_rgb=None, corner_radius=Pt(0))

        # Lane separator
        if i > 0:
            sep = slide.shapes.add_connector(
                MSO_CONNECTOR_TYPE.STRAIGHT,
                margin_l + pool_header_w, ly,
                margin_l + total_w, ly)
            sep.line.color.rgb = _to_rgb_safe(C["dark"])
            sep.line.width = LineWidth.LANE_SEPARATOR_LINE

        # Subtle lane body tint for system lane on light masters only.
        if ltype == "system" and C.get("mode") != "dark":
            add_rounded_rect(slide, content_left, ly, content_w, lane_h,
                             fill_rgb=_lighten(C.get("secondary", C["primary"]), 0.92),
                             line_rgb=None, corner_radius=Pt(0))

    # --- Nodes with task type icons (auto-layout with lane constraints) ---
    task_w = emu(Size.TASK_W * su)
    task_h = emu(Size.TASK_H * su)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)

    region_left_in = content_left / 914400
    region_top_in = margin_t / 914400
    region_w_in = content_w / 914400
    region_h_in = total_h / 914400
    lane_ids = [lane.get("id", f"lane_{i}") for i, lane in enumerate(lanes)]

    positions = auto_layout(
        nodes=nodes,
        edges=flows,
        region={"left": region_left_in, "top": region_top_in,
                "width": region_w_in, "height": region_h_in},
        node_sizes={
            "task": (Size.TASK_W * su, Size.TASK_H * su),
            "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
            "gateway": (Size.GATEWAY_SIZE * su, Size.GATEWAY_SIZE * su),
        },
        lanes=lane_ids,
    )

    node_boxes = {}

    for node in nodes:
        nid = node["id"]
        if nid not in positions:
            continue
        left, top, w, h = positions[nid]
        cx = left + w // 2
        cy = top + h // 2

        ntype = node.get("type", "task")
        if ntype == "start_event":
            s = add_start_event(slide, cx, cy, C, ev_d)
            node_boxes[nid] = (cx, cy, ev_d, ev_d, s)
        elif ntype == "end_event":
            s = add_end_event(slide, cx, cy, C, ev_d)
            node_boxes[nid] = (cx, cy, ev_d, ev_d, s)
        elif "gateway" in ntype:
            gtype = ntype.replace("_gateway", "")
            s = add_gateway(slide, cx, cy, C, gateway_type=gtype, size=gw_s)
            node_boxes[nid] = (cx, cy, gw_s, gw_s, s)
        else:
            lane_id = node.get("lane", lanes[0]["id"] if lanes else "default")
            # Add task type icon prefix to label
            icon = _TASK_ICONS.get(ntype, "")
            label = icon + node.get("label", "")
            # Use type-specific border color
            lane_obj = next((l for l in lanes if l["id"] == lane_id), None)
            ltype = lane_obj.get("lane_type", "human") if lane_obj else "human"
            border_color = lane_type_colors.get(ltype, C["dark"])

            shape = add_rounded_rect(slide, left, top, w, h,
                                     fill_rgb=C["white"],
                                     line_rgb=border_color,
                                     line_width=Pt(1), corner_radius=Pt(4),
                                     text=label, font_size=FontSize.TASK_LABEL,
                                     font_color=C["text"])
            node_boxes[nid] = (left + w // 2, top + h // 2, w, h, shape)

    # --- Boundary events ---
    for bev in boundary_events:
        parent = node_boxes.get(bev.get("attached_to"))
        if not parent:
            continue
        bev_d = emu(Size.EVENT_DIAMETER_SMALL * su)
        bx = parent[0] + parent[2] // 2
        by = parent[1] + parent[3] // 2 - bev_d // 2
        btype = bev.get("type", "timer_boundary")
        if "timer" in btype:
            color = C["timer"]
            marker = "⏰"
        else:
            color = C["dark"]
            marker = "!"
        s = add_circle(slide, bx, by, bev_d,
                   fill_rgb=C["white"],
                   line_rgb=color, line_width=Pt(1), text=marker, font_size=Pt(6))
        node_boxes[bev["id"]] = (bx, by, bev_d, bev_d, s)

    # --- Flows ---
    for flow in flows:
        connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                    label=flow.get("label", ""))

    # --- Automation summary annotation ---
    if automation_summary:
        pct = automation_summary.get("automation_pct", 0)
        human_n = automation_summary.get("human_tasks", 0)
        system_n = automation_summary.get("system_tasks", 0)
        summary_text = f"Automation: {pct}% ({system_n} system / {human_n} human tasks)"
        add_annotation(slide, emu(6.0 * sx), emu(5.0 * sy), emu(3.0 * sx), emu(0.25 * sy),
                       summary_text, C, FontSize.AUTOMATION_PCT)

    return slide


def _lighten(rgb_tuple, factor=0.85):
    return tuple(int(c + (255 - c) * factor) for c in rgb_tuple)


def _mix(rgb_a, rgb_b, factor):
    return tuple(int(a + (b - a) * factor) for a, b in zip(rgb_a, rgb_b))


def _to_rgb_safe(c):
    from pptx.dml.color import RGBColor
    if isinstance(c, RGBColor):
        return c
    return RGBColor(*c)


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
