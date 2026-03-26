"""GM-25 Feature Proof Card — 3 vertical cards with claim/metric/evidence."""

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
    content_top = Inches(1.2)
    total_w = Inches(8.5)
    card_gap = Inches(0.2)
    card_w = int((total_w - (n - 1) * card_gap) / n)
    card_h = int(Inches(3.5))

    claim_h = int(Inches(0.45))
    metric_h = int(Inches(0.8))
    scope_h = int(Inches(0.28))

    for i, card in enumerate(cards):
        cx = int(content_left + i * (card_w + card_gap))

        # Card background
        shape_rect(slide, cx, int(content_top), card_w, card_h,
                    fill_color=C["white"], line_color=C["line"])

        # Claim strip header
        shape_rect(slide, cx, int(content_top), card_w, claim_h,
                    fill_color=C["dark"])
        textbox(slide, int(cx + Inches(0.1)), int(content_top + Inches(0.05)),
                int(card_w - Inches(0.2)), int(claim_h - Inches(0.1)),
                card.get("claim", ""), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

        # Metric badge (large cyan number)
        metric_y = int(content_top + claim_h + Inches(0.1))
        textbox(slide, int(cx + Inches(0.1)), metric_y,
                int(card_w - Inches(0.2)), metric_h,
                card.get("metric", ""), size=36, bold=True,
                color=C["primary"], align=PP_ALIGN.CENTER)

        # Metric label
        textbox(slide, int(cx + Inches(0.1)), int(metric_y + metric_h),
                int(card_w - Inches(0.2)), int(Inches(0.3)),
                card.get("metric_label", ""), size="caption",
                color=C["gray"], align=PP_ALIGN.CENTER)

        # Evidence note
        evidence_y = int(metric_y + metric_h + Inches(0.35))
        textbox(slide, int(cx + Inches(0.1)), evidence_y,
                int(card_w - Inches(0.2)), int(Inches(0.8)),
                card.get("evidence", ""), size="label",
                color=C["text"])

        # Scope tag at bottom
        scope_y = int(content_top + card_h - scope_h - Inches(0.08))
        shape_rect(slide, int(cx + Inches(0.1)), scope_y,
                    int(card_w - Inches(0.2)), scope_h,
                    fill_color=C["light"])
        textbox(slide, int(cx + Inches(0.1)), scope_y,
                int(card_w - Inches(0.2)), scope_h,
                card.get("scope", ""), size="caption",
                color=C["gray"], align=PP_ALIGN.CENTER)

    return slide
