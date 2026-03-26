"""GM-09 Use Case Scenario — Numbered step cards in horizontal flow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
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

    steps = data["content"]["steps"]
    n = len(steps)
    if n == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.3)
    total_w = Inches(8.5)
    card_gap = Inches(0.15)
    arrow_w = Inches(0.25)
    usable_w = total_w - (n - 1) * (card_gap + arrow_w)
    card_w = int(usable_w / n)
    card_h = int(Inches(2.0))

    actor_h = int(Inches(0.3))
    num_circle_size = int(Inches(0.35))
    module_h = int(Inches(0.28))

    for i, step in enumerate(steps):
        cx = int(content_left + i * (card_w + card_gap + arrow_w))

        textbox(
            slide, cx, int(content_top - Inches(0.35)),
            card_w, actor_h,
            step.get("actor", ""),
            size="caption", color=C["gray"], align=PP_ALIGN.CENTER,
        )

        shape_rect(slide, cx, int(content_top), card_w, card_h,
                    fill_color=C["light"], line_color=C["line"])

        num_x = int(cx + card_w / 2 - num_circle_size / 2)
        from pptx.enum.shapes import MSO_SHAPE
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, num_x, int(content_top + Inches(0.12)),
            num_circle_size, num_circle_size,
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(*C["primary"])
        circle.line.fill.background()

        textbox(
            slide, num_x, int(content_top + Inches(0.12)),
            num_circle_size, num_circle_size,
            str(step.get("num", i + 1)),
            size="body", bold=True, color=C["white"], align=PP_ALIGN.CENTER,
        )

        textbox(
            slide,
            int(cx + Inches(0.08)),
            int(content_top + Inches(0.55)),
            int(card_w - Inches(0.16)),
            int(Inches(1.2)),
            step.get("title", ""),
            size="caption", bold=True, color=C["text"], align=PP_ALIGN.CENTER,
        )

        module_y = int(content_top + card_h + Inches(0.08))
        shape_rect(slide, cx, module_y, card_w, module_h,
                    fill_color=C["dark"])
        textbox(
            slide, cx, module_y, card_w, module_h,
            step.get("module", ""), size="caption", color=C["white"],
            align=PP_ALIGN.CENTER,
        )

        if i < n - 1:
            arrow_x = int(cx + card_w + Inches(0.02))
            arrow_y = int(content_top + card_h / 2 - Inches(0.15))
            textbox(
                slide, arrow_x, arrow_y, int(arrow_w), int(Inches(0.3)),
                "→", size="h3", bold=True, color=C["primary"],
                align=PP_ALIGN.CENTER,
            )

    return slide
