"""GM-23 Feature Adoption Funnel — 5-stage funnel with conversion rates."""

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
    FUNNEL_COLORS = [C["dark"], C["primary"], C["primary"], C["secondary"], C["light"]]
    FUNNEL_TEXT = [C["white"], C["white"], C["white"], C["text"], C["text"]]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    stages = data["content"]["stages"]
    n = len(stages)
    if n == 0:
        return slide

    funnel_left = Inches(0.8)
    funnel_top = Inches(1.3)
    max_w = Inches(5.5)
    min_w = Inches(1.8)
    stage_h = int(Inches(0.65))
    stage_gap = int(Inches(0.06))

    rate_x = int(funnel_left + max_w + Inches(0.5))
    rate_w = int(Inches(2.5))

    for i, stage in enumerate(stages):
        sy = int(funnel_top + i * (stage_h + stage_gap))

        # Taper width linearly
        progress = i / max(n - 1, 1)
        bar_w = int(max_w - progress * (max_w - min_w))
        bar_x = int(funnel_left + (max_w - bar_w) / 2)

        bg = FUNNEL_COLORS[i % len(FUNNEL_COLORS)]
        txt = FUNNEL_TEXT[i % len(FUNNEL_TEXT)]

        shape_rect(slide, bar_x, sy, bar_w, stage_h, fill_color=bg)

        label = stage.get("label", "")
        count = stage.get("count", "")
        display = f"{label}   {count}" if count else label
        textbox(slide, int(bar_x + Inches(0.1)), sy,
                int(bar_w - Inches(0.2)), stage_h,
                display, size="label", bold=True, color=txt,
                align=PP_ALIGN.CENTER)

        # Conversion rate on right
        rate = stage.get("rate", "")
        if rate and i < n - 1:
            ry = int(sy + stage_h / 2)
            textbox(slide, rate_x, ry, rate_w, int(Inches(0.25)),
                    f"▼ {rate}", size="caption", color=C["gray"])

    return slide
