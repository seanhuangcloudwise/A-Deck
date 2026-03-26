"""RA-07 Resource-priority matrix."""

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


def short_text(text, limit=28):
    text = str(text or "")
    return text if len(text) <= limit else text[: max(1, limit - 1)] + "…"


def load_slide(ctx, data):
    C = ctx.colors
    from pptx_lib import lighter
    _Q = [lighter(C["primary"], 0.90), lighter(C["primary"], 0.82), lighter(C["gray"], 0.75), lighter(C["gray"], 0.65)]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-07 Resource Priority Matrix"))
    set_subtitle(ctx, slide, data.get("subtitle", "资源-优先级矩阵"), C["gray"])

    content = data.get("content", {})
    points = content.get("initiatives", [])

    left = int(Inches(1.6))
    top = int(Inches(1.2))
    w = int(Inches(4.6))
    h = int(Inches(4.6))
    half_w = int(w / 2)
    half_h = int(h / 2)

    shape_rect(slide, left, top, half_w, half_h, fill_color=_Q[0], line_color=C["line"])
    shape_rect(slide, left + half_w, top, half_w, half_h, fill_color=_Q[1], line_color=C["line"])
    shape_rect(slide, left, top + half_h, half_w, half_h, fill_color=_Q[2], line_color=C["line"])
    shape_rect(slide, left + half_w, top + half_h, half_w, half_h, fill_color=_Q[3], line_color=C["line"])

    textbox(slide, left + int(Inches(0.14)), top + int(Inches(0.1)), int(Inches(1.5)), int(Inches(0.2)), "Under-invested ↑", size="label", bold=True, color=C["dark"])
    textbox(slide, left + half_w + int(Inches(0.12)), top + int(Inches(0.1)), int(Inches(1.8)), int(Inches(0.2)), "Justified ✓", size="label", bold=True, color=C["dark"])
    textbox(slide, left + int(Inches(0.14)), top + half_h + int(Inches(0.1)), int(Inches(1.4)), int(Inches(0.2)), "Low Overhead", size="caption", color=C["gray"])
    textbox(slide, left + half_w + int(Inches(0.12)), top + half_h + int(Inches(0.1)), int(Inches(1.8)), int(Inches(0.2)), "Over-invested ↓", size="caption", color=C["gray"])

    textbox(slide, left + int(Inches(1.5)), top + h + int(Inches(0.05)), int(Inches(1.4)), int(Inches(0.2)), content.get("x_label", "Resource"), size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
    textbox(slide, left - int(Inches(1.2)), top + int(Inches(2.1)), int(Inches(1.1)), int(Inches(0.2)), content.get("y_label", "Priority"), size="label", bold=True, color=C["text"], align=PP_ALIGN.RIGHT)

    for i, p in enumerate(points[:10], 1):
        x = left + int(float(p.get("x", 0.5)) * w)
        y = top + int((1 - float(p.get("y", 0.5))) * h)
        r = int(Inches(0.07 + 0.03 * float(p.get("size", 1))))
        shape_rect(slide, x - r, y - r, r * 2, r * 2, fill_color=C["primary"] if p.get("priority") == "high" else C["secondary"])
        textbox(slide, x - int(Inches(0.05)), y - int(Inches(0.04)), int(Inches(0.1)), int(Inches(0.1)), str(i), size="micro", color=C["text"], align=PP_ALIGN.CENTER)
        textbox(slide, int(Inches(6.45)), int(Inches(1.2 + i * 0.36)), int(Inches(2.3)), int(Inches(0.2)), f"{i}. {short_text(p.get('name', ''))}", size="caption", color=C["text"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("method", "Method: WSJF") + " | Rebalance action: shift budget from Q4 to Q1", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)

    return slide
