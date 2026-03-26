"""RA-02 Portfolio heat matrix."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))
from pptx_lib import header, layout_by_names
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from renderer_utils import shape_rect, textbox

def set_subtitle(ctx, slide, text, gray_color=None):
    subtitle_ph = next((s for s in slide.shapes if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1), None)
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def q_color(x, y, C):
    if x < 0.5 and y >= 0.5:
        return C["soft_green"]
    if x >= 0.5 and y >= 0.5:
        return C["soft_blue"]
    if x < 0.5 and y < 0.5:
        return C["light"]
    return C["soft_yellow"]


def short_text(text, limit=28):
    text = str(text or "")
    return text if len(text) <= limit else text[: max(1, limit - 1)] + "…"


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-02 Portfolio Heat Matrix"))
    set_subtitle(ctx, slide, data.get("subtitle", "举措组合热力矩阵"), C["gray"])

    content = data.get("content", {})
    x_label = content.get("x_label", "Effort")
    y_label = content.get("y_label", "Value")
    initiatives = content.get("initiatives", [])

    left = int(Inches(1.5))
    top = int(Inches(1.25))
    size = int(Inches(4.6))
    half = int(size / 2)

    # 2x2 heat quadrants
    shape_rect(slide, left, top, half, half, fill_color=q_color(0.25, 0.75, C), line_color=C["line"])
    shape_rect(slide, left + half, top, half, half, fill_color=q_color(0.75, 0.75, C), line_color=C["line"])
    shape_rect(slide, left, top + half, half, half, fill_color=q_color(0.25, 0.25, C), line_color=C["line"])
    shape_rect(slide, left + half, top + half, half, half, fill_color=q_color(0.75, 0.25, C), line_color=C["line"])

    textbox(slide, left + int(Inches(0.15)), top + int(Inches(0.1)), int(Inches(1.6)), int(Inches(0.2)), "Quick Wins", size="label", bold=True, color=C["dark"])
    textbox(slide, left + half + int(Inches(0.12)), top + int(Inches(0.1)), int(Inches(1.7)), int(Inches(0.2)), "Strategic Bets", size="label", bold=True, color=C["dark"])
    textbox(slide, left + int(Inches(0.15)), top + half + int(Inches(0.1)), int(Inches(1.5)), int(Inches(0.2)), "Fill-ins", size="label", color=C["gray"])
    textbox(slide, left + half + int(Inches(0.12)), top + half + int(Inches(0.1)), int(Inches(1.8)), int(Inches(0.2)), "Money Pits", size="label", color=C["gray"])

    # Axes labels
    textbox(slide, left + int(Inches(1.8)), top + size + int(Inches(0.05)), int(Inches(1.1)), int(Inches(0.2)), x_label, size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
    textbox(slide, left - int(Inches(1.1)), top + int(Inches(2.0)), int(Inches(1.0)), int(Inches(0.2)), y_label, size="label", bold=True, color=C["text"], align=PP_ALIGN.RIGHT)

    for i, it in enumerate(initiatives[:10], 1):
        x = float(it.get("x", 0.5))
        y = float(it.get("y", 0.5))
        px = left + int(x * size)
        py = top + int((1 - y) * size)
        rad = int(Inches(0.1 + 0.04 * float(it.get("size", 1))))
        shape_rect(slide, px - rad, py - rad, rad * 2, rad * 2, fill_color=C["primary"] if it.get("priority") == "high" else C["secondary"])
        textbox(slide, px - int(Inches(0.2)), py - int(Inches(0.04)), int(Inches(0.4)), int(Inches(0.1)), str(i), size="micro", color=C["text"], align=PP_ALIGN.CENTER)
        textbox(slide, int(Inches(6.35)), int(Inches(1.2 + i * 0.38)), int(Inches(2.4)), int(Inches(0.2)), f"{i}. {short_text(it.get('name', ''))}", size="caption", color=C["text"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("method", "Method: RICE / WSJF") + " | Data as of: 2026-03", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
