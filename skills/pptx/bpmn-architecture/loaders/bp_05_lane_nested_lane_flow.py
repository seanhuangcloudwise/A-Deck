"""BP-05 Lane and Nested Lane Flow — BPMN loader.

Renders a swimlane process diagram with optional nested lanes.
Official anchor: OMG BPMN 2.0 by Example §10.3, formal spec §10.8.

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
    set_title_subtitle, fit_x_scale, connect_seq, slide_scale,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Pt
from pptx.enum.shapes import MSO_CONNECTOR_TYPE


def load_slide(ctx, data):
    """Render a Lane and Nested Lane Flow (BP-05) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    pool = content.get("pool", {"id": "default", "name": "Process"})
    lanes = content.get("lanes", [])
    nodes = content.get("nodes", [])
    flows = content.get("flows", [])

    # --- Geometry ---
    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.4 * sx)
    margin_t = emu(1.0 * sy)
    total_w = emu(9.2 * sx)
    total_h = emu(4.2 * sy)
    pool_header_w = emu(0.35 * sx)
    lane_header_w = emu(Size.LANE_HEADER_W * sx)

    # Flatten lanes (handle nested)
    flat_lanes = []
    for lane in lanes:
        nested = lane.get("nested_lanes", [])
        if nested:
            for nl in nested:
                flat_lanes.append({"id": nl["id"], "name": nl["name"], "parent": lane["name"], "level": 1})
        else:
            flat_lanes.append({"id": lane["id"], "name": lane["name"], "parent": None, "level": 0})

    n_lanes = max(len(flat_lanes), 1)
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
    content_left_in = 0.4 + 0.35 + Size.LANE_HEADER_W

    for i, fl in enumerate(flat_lanes):
        ly = margin_t + i * lane_h
        if C.get("mode") == "dark":
            lane_fill = C["light"] if fl["level"] == 0 else _mix(C["light"], C.get("ink", C["light"]), 0.22)
            add_rounded_rect(slide, content_left, ly, content_w, lane_h,
                             fill_rgb=lane_fill, line_rgb=None, corner_radius=Pt(0))
        # Lane header
        hw = emu(Size.NESTED_LANE_HEADER_W * sx) if fl["level"] > 0 else lane_header_w
        add_lane_header(slide, margin_l + pool_header_w, ly, hw, lane_h, C,
                        name=fl["name"], level=fl["level"])
        lane_regions[fl["id"]] = {
            "top": ly,
            "height": lane_h,
            "left": content_left,
            "width": content_w,
        }
        # Lane separator line
        if i > 0:
            sep = slide.shapes.add_connector(
                MSO_CONNECTOR_TYPE.STRAIGHT,
                margin_l + pool_header_w, ly,
                margin_l + total_w, ly)
            sep.line.color.rgb = _to_rgb_safe(C["dark"])
            sep.line.width = LineWidth.LANE_SEPARATOR_LINE

    # --- Nodes (auto-layout with lane constraints) ---
    task_w = emu(Size.TASK_W * su)
    task_h = emu(Size.TASK_H * su)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)

    # Compute auto_layout region in inches (content area inside pool)
    region_left_in = content_left / 914400
    region_top_in = (margin_t / 914400)
    region_w_in = content_w / 914400
    region_h_in = total_h / 914400
    lane_ids = [fl["id"] for fl in flat_lanes]

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
            s = add_task(slide, left, top, w, h, C,
                     label=node.get("label", ""), task_type=ntype)
            node_boxes[nid] = (left + w // 2, top + h // 2, w, h, s)

    # --- Flows ---
    for flow in flows:
        connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                    label=flow.get("label", ""))

    return slide


def _to_rgb_safe(c):
    from pptx.dml.color import RGBColor
    if isinstance(c, RGBColor):
        return c
    return RGBColor(*c)


def _mix(rgb_a, rgb_b, factor):
    return tuple(int(a + (b - a) * factor) for a, b in zip(rgb_a, rgb_b))


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
