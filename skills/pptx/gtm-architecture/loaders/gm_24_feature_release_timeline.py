"""GM-24 Feature Release Timeline — Horizontal timeline with cards above/below."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from renderer_utils import textbox, shape_rect

def set_subtitle(ctx, slide, text, gray_color=None):
    subtitle_ph = next(
        (
            s
            for s in slide.shapes
            if getattr(s, "is_placeholder", False)
            and s.placeholder_format.idx == 1
        ),
        None,
    )
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    content = data["content"]
    quarters = content.get("quarters", [])
    items = content.get("items", [])
    nq = len(quarters)
    if nq == 0:
        return slide

    axis_left = Inches(0.5)
    axis_y = Inches(3.0)
    axis_w = Inches(8.5)
    axis_h = int(Inches(0.04))

    # Timeline axis
    shape_rect(slide, int(axis_left), int(axis_y), int(axis_w), axis_h,
                fill_color=C["gray"])

    # Quarter marks and labels
    q_gap = axis_w / nq
    quarter_map = {}
    for qi, q in enumerate(quarters):
        qx = int(axis_left + qi * q_gap + q_gap / 2)
        quarter_map[q] = qx

        # Milestone dot
        dot_size = int(Inches(0.12))
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            int(qx - dot_size / 2),
            int(axis_y - dot_size / 2 + axis_h / 2),
            dot_size, dot_size,
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*C["text"])
        dot.line.fill.background()

        textbox(slide, int(qx - Inches(0.5)), int(axis_y + Inches(0.1)),
                int(Inches(1.0)), int(Inches(0.25)),
                q, size="label", bold=True, color=C["text"],
                align=PP_ALIGN.CENTER)

    # Items: delivered above, planned below
    above_offset = 0
    below_offset = 0
    card_w = int(Inches(1.5))
    card_h = int(Inches(0.6))

    delivered_items = [it for it in items if it.get("status") == "delivered"]
    planned_items = [it for it in items if it.get("status") != "delivered"]

    for i, item in enumerate(delivered_items):
        q = item.get("quarter", "")
        cx = quarter_map.get(q, int(axis_left + i * Inches(1.8)))
        cy = int(axis_y - Inches(0.9) - (i % 2) * Inches(0.7))

        shape_rect(slide, int(cx - card_w / 2), cy, card_w, card_h,
                    fill_color=C["primary"])
        textbox(slide, int(cx - card_w / 2 + Inches(0.05)), cy,
                int(card_w - Inches(0.1)), card_h,
                item.get("label", ""), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

    for i, item in enumerate(planned_items):
        q = item.get("quarter", "")
        cx = quarter_map.get(q, int(axis_left + i * Inches(1.8)))
        cy = int(axis_y + Inches(0.45) + (i % 2) * Inches(0.7))

        shape_rect(slide, int(cx - card_w / 2), cy, card_w, card_h,
                    fill_color=C["light"], line_color=C["line"],
                    line_width=1)
        textbox(slide, int(cx - card_w / 2 + Inches(0.05)), cy,
                int(card_w - Inches(0.1)), card_h,
                item.get("label", ""), size="label",
                color=C["text"], align=PP_ALIGN.CENTER)

    return slide
