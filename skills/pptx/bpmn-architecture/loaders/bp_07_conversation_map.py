"""BP-07 Conversation Map — BPMN loader.

Renders a Conversation diagram with hexagonal nodes and participant rectangles.
Official anchor: OMG BPMN 2.0.2 §9.5, Examples §10.5.

Isolation: imports only from local primitives/style_tokens.
"""

import sys, math
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_hexagon, add_conversation_link,
    set_title_subtitle, edge_endpoints, slide_scale,
)
from style_tokens import resolve_colors, Size, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render a Conversation Map (BP-07) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    participants = content.get("participants", [])
    conversations = content.get("conversations", [])

    # --- Layout participants in a ring ---
    sx, sy, su = slide_scale(prs)
    cx_center = emu(5.0 * sx)
    cy_center = emu(2.8 * sy)
    radius = emu(2.0 * su)
    p_w = emu(1.0 * su)
    p_h = emu(0.5 * su)

    participant_positions = {}
    n_parts = max(len(participants), 1)
    for i, part in enumerate(participants):
        angle = 2 * math.pi * i / n_parts - math.pi / 2
        px = int(cx_center + radius * math.cos(angle)) - p_w // 2
        py = int(cy_center + radius * math.sin(angle)) - p_h // 2

        # Determine fill: use lighter primary variant
        s = add_rounded_rect(slide, px, py, p_w, p_h,
                         fill_rgb=C["primary"], line_rgb=C["dark"],
                         line_width=Pt(1), corner_radius=Pt(3),
                         text=part.get("name", part.get("id", "")),
                         font_size=Pt(8), font_color=C["white"], bold=True)
        participant_positions[part["id"]] = (px + p_w // 2, py + p_h // 2, s)

    # --- Place conversation hexagons ---
    conv_positions = {}
    hex_w = emu(Size.HEXAGON_W * su)
    hex_h = emu(Size.HEXAGON_H * su)

    for j, conv in enumerate(conversations):
        cid = conv["id"]
        connected = conv.get("connected_participants", [])
        # Position hexagon at centroid of connected participants
        if connected:
            avg_x = sum(participant_positions.get(p, (cx_center, cy_center))[0] for p in connected) // len(connected)
            avg_y = sum(participant_positions.get(p, (cx_center, cy_center))[1] for p in connected) // len(connected)
        else:
            avg_x, avg_y = cx_center, cy_center

        hx = avg_x - hex_w // 2
        hy = avg_y - hex_h // 2

        ctype = conv.get("type", "conversation")
        if ctype == "sub_conversation":
            fill = C["secondary"]
            hex_shape = add_hexagon(slide, hx, hy, hex_w, hex_h, fill_rgb=fill,
                        line_rgb=C["dark"], line_width=Pt(1),
                        text=conv.get("name", "") + " [+]", font_size=Pt(7))
        elif ctype == "call_conversation":
            hex_shape = add_hexagon(slide, hx, hy, hex_w, hex_h, fill_rgb=C["secondary"],
                        line_rgb=C["primary"], line_width=Pt(2.5),
                        text=conv.get("name", ""), font_size=Pt(7))
        else:
            hex_shape = add_hexagon(slide, hx, hy, hex_w, hex_h, fill_rgb=C["secondary"],
                        line_rgb=C["dark"], line_width=Pt(1),
                        text=conv.get("name", ""), font_size=Pt(7))

        conv_center = (avg_x, avg_y)
        conv_positions[cid] = (conv_center, hex_shape)

        # Conversation links to participants (no arrowheads)
        for pid in connected:
            ppos = participant_positions.get(pid)
            if ppos:
                sb = (conv_center[0], conv_center[1], hex_w, hex_h)
                db = (ppos[0], ppos[1], p_w, p_h)
                x1, y1, x2, y2 = edge_endpoints(sb, db)
                add_conversation_link(slide, x1, y1, x2, y2, C,
                                      begin_shape=hex_shape, end_shape=ppos[2],
                                      src_box=sb, dst_box=db)

    return slide


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
