"""GM-17 Analyst Briefing Framework — 5 horizontal section bands."""

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
    BAND_ACCENTS = [C["dark"], C["primary"], C["primary"], C["secondary"], C["dark"]]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    sections = data["content"]["sections"]
    n = len(sections)
    if n == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.2)
    total_w = Inches(8.5)
    band_gap = Inches(0.08)
    total_h = Inches(3.7)
    band_h = int((total_h - (n - 1) * band_gap) / n)

    label_w = int(Inches(2.0))
    bullet_x = int(content_left + label_w + Inches(0.1))
    bullet_w = int(total_w - label_w - Inches(0.1))

    for i, section in enumerate(sections):
        by = int(content_top + i * (band_h + band_gap))
        accent = BAND_ACCENTS[i % len(BAND_ACCENTS)]

        # Accent bar
        shape_rect(slide, int(content_left), by,
                    int(Inches(0.06)), band_h, fill_color=accent)

        # Section name
        shape_rect(slide, int(content_left + Inches(0.06)), by,
                    int(label_w - Inches(0.06)), band_h,
                    fill_color=C["light"])
        textbox(slide, int(content_left + Inches(0.15)), by,
                int(label_w - Inches(0.2)), band_h,
                section.get("name", ""), size="label", bold=True,
                color=C["text"])

        # Content bullets
        bullets = section.get("bullets", [])
        bullet_text = "\n".join(f"• {b}" for b in bullets)
        textbox(slide, bullet_x, by,
                bullet_w, band_h,
                bullet_text, size="caption", color=C["text"])

    return slide
