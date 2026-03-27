"""BP-06 Choreography Interaction — BPMN loader.

Renders a Choreography diagram with participant bands.
Official anchor: OMG BPMN 2.0.2 §11 Choreography, Examples §10.6.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event,
    add_gateway, add_sequence_flow, set_title_subtitle,
    connect_seq, slide_scale,
)
from style_tokens import resolve_colors, Size, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render a Choreography Interaction (BP-06) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    tasks = content.get("choreography_tasks", [])
    flows = content.get("flows", [])

    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.6 * sx)
    base_y = emu(2.0 * sy)
    task_w = emu(1.4 * su)
    band_h = emu(0.2 * su)
    center_h = emu(0.4 * su)
    total_h = band_h * 2 + center_h
    gap = emu(0.5 * sx)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)

    # Auto-scale task width and gap so all tasks + start/end events fit within 9.5"
    n_tasks = max(len(tasks), 1)
    # total width: margin_l + ev_d + gap_after_start + n_tasks*(task_w+gap) + ev_d
    right_limit = emu(9.5 * sx)
    avail = right_limit - margin_l - ev_d * 2 - gap * 2
    natural = n_tasks * (task_w + gap)
    if natural > avail:
        sf = avail / natural
        task_w = int(task_w * sf)
        gap = int(gap * sf)

    node_boxes = {}

    # Start event
    start_x = margin_l
    start_y = base_y + total_h // 2
    s = add_start_event(slide, start_x, start_y, C, ev_d)
    node_boxes["start"] = (start_x, start_y, ev_d, ev_d, s)

    # Choreography tasks
    for i, ct in enumerate(tasks):
        cid = ct["id"]
        x = margin_l + emu(0.5 * sx) + i * (task_w + gap)
        y = base_y

        # Initiator band (top) — shaded
        add_rounded_rect(slide, x, y, task_w, band_h,
                         fill_rgb=C["primary"], line_rgb=C["dark"],
                         line_width=Pt(1), corner_radius=Pt(0),
                         text=ct.get("initiator", ""),
                         font_size=FontSize.CHOREOGRAPHY_PARTICIPANT,
                         font_color=C["white"], bold=True)

        # Center — interaction name
        add_rounded_rect(slide, x, y + band_h, task_w, center_h,
                         fill_rgb=C["white"],
                         line_rgb=C["dark"], line_width=Pt(1), corner_radius=Pt(0),
                         text=ct.get("name", ""),
                         font_size=FontSize.CHOREOGRAPHY_INTERACTION)

        # Responder band (bottom) — light
        add_rounded_rect(slide, x, y + band_h + center_h, task_w, band_h,
                         fill_rgb=C["light"],
                         line_rgb=C["dark"], line_width=Pt(1), corner_radius=Pt(0),
                         text=ct.get("responder", ""),
                         font_size=FontSize.CHOREOGRAPHY_PARTICIPANT,
                         font_color=C["dark"])

        # Outer border
        outer = add_rounded_rect(slide, x, y, task_w, total_h,
                         fill_rgb=None, line_rgb=C["dark"],
                         line_width=Pt(1), corner_radius=Pt(3))

        cx = x + task_w // 2
        cy = y + total_h // 2
        node_boxes[cid] = (cx, cy, task_w, total_h, outer)

    # End event
    ex = margin_l + emu(0.5 * sx) + len(tasks) * (task_w + gap)
    ey = base_y + total_h // 2
    s = add_end_event(slide, ex, ey, C, ev_d)
    node_boxes["end"] = (ex, ey, ev_d, ev_d, s)

    # Flows
    for flow in flows:
        connect_seq(slide, node_boxes, flow["from"], flow["to"], C)

    return slide


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
