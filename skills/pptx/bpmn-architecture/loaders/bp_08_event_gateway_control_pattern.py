"""BP-08 Event and Gateway Control Pattern — BPMN loader.

Renders a pattern card grid showing BPMN gateway and event combinations.
Official anchor: OMG BPMN 2.0.2 §10.5–10.6, Examples §6/§9 incident/travel.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event, add_task,
    add_gateway, add_sequence_flow, add_circle, add_intermediate_event,
    set_title_subtitle, connect_seq, slide_scale,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render an Event and Gateway Control Pattern (BP-08) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    variant = content.get("variant", "pattern_card")
    patterns = content.get("patterns", [])

    if variant == "pattern_card":
        _render_pattern_cards(prs, slide, patterns, C)
    else:
        # Combined flow variant: treat patterns[0] as a single flow
        if patterns:
            _render_single_pattern(prs, slide, patterns[0], C, full_slide=True)

    return slide


def _render_pattern_cards(prs, slide, patterns, C):
    """Render multiple small pattern cards in a grid."""
    n = len(patterns)
    cols = 2
    rows = (n + cols - 1) // cols

    sx, sy, su = slide_scale(prs)
    card_w = emu(4.2 * sx)
    card_h = emu(1.5 * sy)
    margin_l = emu(0.5 * sx)
    margin_t = emu(1.2 * sy)
    gap_x = emu(0.4 * sx)
    gap_y = emu(0.2 * sy)

    for i, pattern in enumerate(patterns):
        col = i % cols
        row = i // cols
        cx = margin_l + col * (card_w + gap_x)
        cy = margin_t + row * (card_h + gap_y)

        # Card border
        add_rounded_rect(slide, cx, cy, card_w, card_h,
                         fill_rgb=C["white"],
                         line_rgb=C["light"],
                         line_width=Pt(0.5), corner_radius=Pt(3))

        # Card title
        add_rounded_rect(slide, cx + emu(0.1 * sx), cy + emu(0.05 * sy),
                 card_w - emu(0.2 * sx), emu(0.2 * sy),
                         fill_rgb=None, line_rgb=None,
                         text=pattern.get("title", f"Pattern {i+1}"),
                         font_size=FontSize.PATTERN_CARD_TITLE,
                         font_color=C["primary"], bold=True)

        # Render mini-flow inside card
        _render_single_pattern(prs, slide, pattern, C, region=(cx, cy + emu(0.3 * sy), card_w, card_h - emu(0.35 * sy)))


def _render_single_pattern(prs, slide, pattern, C, region=None, full_slide=False):
    """Render a single pattern's nodes and flows within a region."""
    nodes = pattern.get("nodes", [])
    flows = pattern.get("flows", [])

    sx, sy, su = slide_scale(prs)

    if full_slide:
        ox, oy, rw, rh = emu(0.6 * sx), emu(1.5 * sy), 8.5 * sx, 3.0 * sy
        scale = 1.0
    elif region:
        ox, oy, rw_emu, rh_emu = region
        ox += emu(0.15 * sx)
        oy += emu(0.1 * sy)
        rw = rw_emu / 914400 - 0.3 * sx   # EMU to inches minus padding
        rh = rh_emu / 914400 - 0.25 * sy
        scale = 0.7
    else:
        ox, oy, rw, rh = emu(0.6 * sx), emu(1.5 * sy), 8.5 * sx, 3.0 * sy
        scale = 1.0

    task_w = int(emu(0.8 * su) * scale)
    task_h = int(emu(0.35 * su) * scale)
    ev_d = int(emu(0.18 * su) * scale)
    gw_s = int(emu(0.25 * su) * scale)

    # --- Use Sugiyama layout engine for node positioning ---
    positions = auto_layout(
        nodes=nodes,
        edges=flows,
        region={"left": ox / 914400, "top": oy / 914400,
                "width": rw * scale, "height": rh * scale},
        node_sizes={
            "task": (0.8 * su * scale, 0.35 * su * scale),
            "event": (0.18 * su * scale, 0.18 * su * scale),
            "gateway": (0.25 * su * scale, 0.25 * su * scale),
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
        elif ntype == "intermediate_event":
            s = add_intermediate_event(slide, cx, cy, C, ev_d, marker=node.get("marker", ""))
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


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
