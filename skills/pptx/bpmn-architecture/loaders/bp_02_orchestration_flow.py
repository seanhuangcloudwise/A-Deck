"""BP-02 Orchestration Flow (Single Pool) — BPMN loader.

Renders an end-to-end single-pool process with gateways and events.
Official anchor: OMG BPMN 2.0 by Example — Shipment Process, Travel Booking.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, mid_x, mid_y, add_start_event, add_end_event, add_task,
    add_gateway, add_sequence_flow, set_title_subtitle, fit_x_scale,
    connect_seq, slide_scale, scaled_region,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render an Orchestration Flow (BP-02) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    nodes = content.get("nodes", [])
    flows = content.get("flows", [])

    _, _, su = slide_scale(prs)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)
    task_w = emu(Size.TASK_W * su)
    task_h = emu(Size.TASK_H * su)

    # --- Use Sugiyama layout engine ---
    positions = auto_layout(
        nodes=nodes,
        edges=flows,
        region=scaled_region(prs, 0.6, 1.5, 8.5, 3.0),
        node_sizes={
            "task": (Size.TASK_W * su, Size.TASK_H * su),
            "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
            "gateway": (Size.GATEWAY_SIZE * su, Size.GATEWAY_SIZE * su),
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
        else:
            s = add_task(slide, left, top, w, h, C,
                         label=node.get("label", ""), task_type=ntype)
            node_boxes[nid] = (left + w // 2, top + h // 2, w, h, s)

    for flow in flows:
        connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                    label=flow.get("label", ""))

    return slide


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
