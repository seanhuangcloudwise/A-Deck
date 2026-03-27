"""BP-04 Collapsed Sub-Process + Call Activity — BPMN loader.

Renders an L1 process overview with collapsed sub-processes and call activities.
Official anchor: OMG BPMN 2.0.2 §10.2.4–10.2.5, Figures 10.25, 10.39–10.42.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event, add_task,
    add_gateway, add_sequence_flow, set_title_subtitle, add_annotation,
    connect_seq, slide_scale, scaled_region,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render a Collapsed Sub-Process + Call Activity (BP-04) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    nodes = content.get("nodes", [])
    flows = content.get("flows", [])
    legend = content.get("legend", [])

    _, _, su = slide_scale(prs)
    task_w = emu(1.4 * su)
    task_h = emu(0.6 * su)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)

    # --- Use Sugiyama layout engine ---
    positions = auto_layout(
        nodes=nodes,
        edges=flows,
        region=scaled_region(prs, 0.6, 1.5, 8.5, 3.2),
        node_sizes={
            "task": (1.4 * su, 0.6 * su),
            "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
            "gateway": (Size.GATEWAY_SIZE * su, Size.GATEWAY_SIZE * su),
            "subprocess": (1.4 * su, 0.6 * su),
        },
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

        elif ntype == "collapsed_subprocess":
            x, y = left, top
            # Collapsed sub-process: normal border + [+] marker
            shape = add_rounded_rect(slide, x, y, w, h,
                                     fill_rgb=C["light"],
                                     line_rgb=C["dark"],
                                     line_width=LineWidth.TASK,
                                     corner_radius=Pt(Size.TASK_CORNER_RADIUS),
                                     text=node.get("label", ""),
                                     font_size=FontSize.TASK_LABEL)
            # [+] marker at bottom center
            marker_size = emu(0.12 * su)
            add_rounded_rect(slide, x + w // 2 - marker_size // 2,
                             y + h - marker_size - emu(0.04 * su),
                             marker_size, marker_size,
                             fill_rgb=None, line_rgb=C["dark"],
                             line_width=Pt(0.75), corner_radius=Pt(0),
                             text="+", font_size=Pt(7), font_color=C["dark"])
            node_boxes[nid] = (x + w // 2, y + h // 2, w, h, shape)

        elif ntype == "call_activity":
            x, y = left, top
            # Call Activity: thick border
            shape = add_rounded_rect(slide, x, y, w, h,
                             fill_rgb=C["white"],
                             line_rgb=C["primary"],
                             line_width=LineWidth.CALL_ACTIVITY,
                             corner_radius=Pt(Size.TASK_CORNER_RADIUS),
                             text=node.get("label", ""),
                             font_size=FontSize.TASK_LABEL,
                             bold=True)
            # Reference note below
            ref = node.get("reference", "")
            if ref:
                add_annotation(slide, x, y + h + emu(0.05),
                               w, emu(0.18 * su), ref, C, FontSize.ANNOTATION)
            node_boxes[nid] = (x + w // 2, y + h // 2, w, h, shape)

        else:
            s = add_task(slide, left, top, w, h, C,
                     label=node.get("label", ""), task_type=ntype)
            node_boxes[nid] = (left + w // 2, top + h // 2, w, h, s)

    # Flows
    for flow in flows:
        connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                    label=flow.get("label", ""))

    # Legend
    if legend:
        ly = emu(4.6 * su)
        lx = emu(6.5 * su)
        for i, item in enumerate(legend):
            add_annotation(slide, lx, ly + i * emu(0.22 * su), emu(2.5 * su), emu(0.2 * su),
                           f"{item.get('symbol', '')} = {item.get('meaning', '')}",
                           C, FontSize.ANNOTATION)

    return slide


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
