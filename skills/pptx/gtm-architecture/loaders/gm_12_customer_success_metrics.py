"""GM-12 Customer Success Metrics — 3 proof cards in a row."""

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

    cards = data["content"]["cards"]
    n = len(cards)
    if n == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.3)
    total_w = Inches(8.5)
    card_gap = Inches(0.2)
    card_w = int((total_w - (n - 1) * card_gap) / n)
    card_h = int(Inches(3.2))

    for i, card in enumerate(cards):
        cx = int(content_left + i * (card_w + card_gap))

        shape_rect(slide, cx, int(content_top), card_w, card_h,
                    fill_color=C["white"], line_color=C["line"])

        # Metric value (large cyan)
        textbox(slide, int(cx + Inches(0.15)), int(content_top + Inches(0.2)),
                int(card_w - Inches(0.3)), int(Inches(0.7)),
                card.get("metric", ""), size=36, bold=True,
                color=C["primary"], align=PP_ALIGN.CENTER)

        # Metric label
        textbox(slide, int(cx + Inches(0.15)), int(content_top + Inches(0.9)),
                int(card_w - Inches(0.3)), int(Inches(0.35)),
                card.get("label", ""), size="label", bold=True,
                color=C["text"], align=PP_ALIGN.CENTER)

        # Profile badge
        badge_y = int(content_top + Inches(1.4))
        badge_w = int(card_w - Inches(0.4))
        shape_rect(slide, int(cx + Inches(0.2)), badge_y,
                    badge_w, int(Inches(0.3)),
                    fill_color=C["dark"])
        textbox(slide, int(cx + Inches(0.2)), badge_y,
                badge_w, int(Inches(0.3)),
                card.get("profile", ""), size="label",
                color=C["white"], align=PP_ALIGN.CENTER)

        # Outcome statement
        textbox(slide, int(cx + Inches(0.15)), int(content_top + Inches(1.9)),
                int(card_w - Inches(0.3)), int(Inches(1.1)),
                card.get("outcome", ""), size="caption",
                color=C["text"])

    return slide
