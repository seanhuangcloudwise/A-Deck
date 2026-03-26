"""GM-15 Sales Playbook Flow — Horizontal stage cards with actions and output chips."""

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

    stages = data["content"]["stages"]
    n = len(stages)
    if n == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.2)
    total_w = Inches(8.5)
    arrow_w = Inches(0.25)
    card_gap = Inches(0.08)
    usable_w = total_w - (n - 1) * (arrow_w + card_gap)
    card_w = int(usable_w / n)
    card_h = int(Inches(3.3))

    header_h = int(Inches(0.4))
    output_h = int(Inches(0.3))

    for i, stage in enumerate(stages):
        cx = int(content_left + i * (card_w + arrow_w + card_gap))

        # Card background
        shape_rect(slide, cx, int(content_top), card_w, card_h,
                    fill_color=C["light"], line_color=C["line"])

        # Stage name header
        shape_rect(slide, cx, int(content_top), card_w, header_h,
                    fill_color=C["dark"])
        textbox(slide, cx, int(content_top + Inches(0.05)),
                card_w, int(header_h - Inches(0.1)),
                stage.get("name", ""), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

        # Actions
        actions = stage.get("actions", [])
        action_text = "\n".join(f"• {a}" for a in actions)
        textbox(slide,
                int(cx + Inches(0.08)),
                int(content_top + header_h + Inches(0.1)),
                int(card_w - Inches(0.16)),
                int(card_h - header_h - output_h - Inches(0.3)),
                action_text, size="label", color=C["text"])

        # Output chip
        output_y = int(content_top + card_h - output_h - Inches(0.08))
        shape_rect(slide,
                    int(cx + Inches(0.08)), output_y,
                    int(card_w - Inches(0.16)), output_h,
                    fill_color=C["primary"])
        textbox(slide,
                int(cx + Inches(0.08)), output_y,
                int(card_w - Inches(0.16)), output_h,
                stage.get("output", ""), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

        # Arrow
        if i < n - 1:
            ax = int(cx + card_w + Inches(0.02))
            ay = int(content_top + card_h / 2 - Inches(0.15))
            textbox(slide, ax, ay, int(arrow_w - Inches(0.04)), int(Inches(0.3)),
                    "→", size="h3", bold=True, color=C["primary"],
                    align=PP_ALIGN.CENTER)

    return slide
