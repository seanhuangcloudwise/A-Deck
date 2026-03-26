"""GM-08 Customer Journey Touchpoints — Horizontal timeline with stage columns."""

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
    col_gap = Inches(0.1)
    col_w = int((total_w - (n - 1) * col_gap) / n)

    row_labels = ["Stage", "Customer Action", "Touchpoint"]
    row_colors = [C["dark"], C["light"], C["secondary"]]
    row_text_colors = [C["white"], C["text"], C["text"]]
    row_h = int(Inches(0.85))
    row_gap = int(Inches(0.06))

    for ri, label in enumerate(row_labels):
        ry = int(content_top + ri * (row_h + row_gap))
        textbox(
            slide, int(content_left - Inches(0.05)), ry,
            int(Inches(0.01)), int(row_h),
            "", size=1,
        )

    for si, stage in enumerate(stages):
        sx = int(content_left + si * (col_w + col_gap))
        fields = [
            stage.get("name", ""),
            stage.get("customer_action", ""),
            stage.get("touchpoint", ""),
        ]

        for ri, field_text in enumerate(fields):
            ry = int(content_top + ri * (row_h + row_gap))
            shape_rect(slide, sx, ry, col_w, row_h, fill_color=row_colors[ri])
            textbox(
                slide,
                int(sx + Inches(0.08)),
                int(ry + Inches(0.08)),
                int(col_w - Inches(0.16)),
                int(row_h - Inches(0.16)),
                field_text,
                size="label" if ri > 0 else 10,
                bold=(ri == 0),
                color=row_text_colors[ri],
                align=PP_ALIGN.CENTER,
            )

        if si < n - 1:
            arrow_x = int(sx + col_w + Inches(0.01))
            arrow_y = int(content_top + Inches(0.25))
            textbox(slide, arrow_x, arrow_y, int(col_gap - Inches(0.02)),
                    int(Inches(0.3)), "→", size="label", color=C["gray"],
                    align=PP_ALIGN.CENTER)

    return slide
