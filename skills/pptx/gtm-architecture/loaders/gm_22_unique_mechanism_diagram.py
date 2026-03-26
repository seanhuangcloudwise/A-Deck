"""GM-22 Unique Mechanism Diagram — Input→Engine→Decision→Action→Feedback flow."""

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

    blocks = data["content"]["blocks"]
    feedback = data["content"].get("feedback", "")
    n = len(blocks)
    if n == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.5)
    total_w = Inches(8.5)
    arrow_w = Inches(0.3)
    block_gap = Inches(0.08)
    usable_w = total_w - (n - 1) * (arrow_w + block_gap)
    block_w = int(usable_w / n)
    block_h = int(Inches(2.0))

    for i, block in enumerate(blocks):
        bx = int(content_left + i * (block_w + arrow_w + block_gap))
        is_critical = block.get("is_critical", False)

        bg = C["secondary"] if is_critical else C["light"]
        border = C["primary"] if is_critical else C["gray"]
        lw = 3 if is_critical else 1

        shape_rect(slide, bx, int(content_top), block_w, block_h,
                    fill_color=bg, line_color=border, line_width=lw)

        textbox(slide, int(bx + Inches(0.08)), int(content_top + Inches(0.1)),
                int(block_w - Inches(0.16)), int(Inches(0.35)),
                block.get("label", ""), size="label", bold=True,
                color=C["text"], align=PP_ALIGN.CENTER)

        textbox(slide, int(bx + Inches(0.08)), int(content_top + Inches(0.5)),
                int(block_w - Inches(0.16)), int(block_h - Inches(0.6)),
                block.get("detail", ""), size="label", color=C["text"])

        if is_critical:
            textbox(slide, bx, int(content_top - Inches(0.22)),
                    block_w, int(Inches(0.2)),
                    "CRITICAL", size="caption", bold=True,
                    color=C["primary"], align=PP_ALIGN.CENTER)

        if i < n - 1:
            ax = int(bx + block_w + Inches(0.02))
            ay = int(content_top + block_h / 2 - Inches(0.15))
            textbox(slide, ax, ay, int(arrow_w - Inches(0.04)),
                    int(Inches(0.3)), "→", size="h3", bold=True,
                    color=C["primary"], align=PP_ALIGN.CENTER)

    # Feedback loop bar at bottom
    if feedback:
        fb_y = int(content_top + block_h + Inches(0.3))
        fb_w = int(total_w)
        shape_rect(slide, int(content_left), fb_y, fb_w, int(Inches(0.35)),
                    fill_color=C["dark"])
        textbox(slide, int(content_left + Inches(0.1)), fb_y,
                int(fb_w - Inches(0.2)), int(Inches(0.35)),
                f"↺ Feedback: {feedback}", size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

    return slide
