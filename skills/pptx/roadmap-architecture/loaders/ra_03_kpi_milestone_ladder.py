"""RA-03 KPI milestone ladder."""

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


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-03 KPI Milestone Ladder"))
    set_subtitle(ctx, slide, data.get("subtitle", "KPI里程碑阶梯"), C["gray"])

    content = data.get("content", {})
    steps = content.get("steps", [])

    base_x = int(Inches(0.8))
    base_y = int(Inches(4.8))
    step_w = int(Inches(1.55))
    step_h = int(Inches(0.58))

    for i, step in enumerate(steps[:5]):
        x = base_x + i * step_w
        y = base_y - i * int(Inches(0.52))
        color = C["primary"] if i == len(steps[:5]) - 1 else (C["secondary"] if i > 1 else C["light"])
        shape_rect(slide, x, y, step_w, step_h, fill_color=color, line_color=C["line"])
        textbox(slide, x + int(Inches(0.04)), y + int(Inches(0.03)), step_w - int(Inches(0.08)), int(Inches(0.18)), step.get("label", ""), size="label", bold=True, color=C["text"])
        textbox(slide, x + int(Inches(0.04)), y + int(Inches(0.22)), step_w - int(Inches(0.08)), int(Inches(0.14)), step.get("value", ""), size="label", bold=True, color=C["dark"])
        textbox(slide, x + int(Inches(0.04)), y + int(Inches(0.37)), step_w - int(Inches(0.08)), int(Inches(0.14)), step.get("date", ""), size="caption", color=C["gray"])
        if i < len(steps[:5]) - 1:
            textbox(slide, x + step_w - int(Inches(0.03)), y - int(Inches(0.1)), int(Inches(0.2)), int(Inches(0.2)), "↗", size="body", color=C["dark"], align=PP_ALIGN.CENTER)

    actual = content.get("actual", {})
    if actual:
        ai = max(0, min(len(steps[:5]) - 1, int(actual.get("step_index", len(steps[:5]) - 1))))
        ax = base_x + ai * step_w + int(step_w / 2)
        ay = base_y - ai * int(Inches(0.52)) - int(Inches(0.18))
        textbox(slide, ax - int(Inches(0.07)), ay, int(Inches(0.14)), int(Inches(0.14)), "▲", size="body", color=C["secondary"], align=PP_ALIGN.CENTER)
        textbox(slide, ax + int(Inches(0.08)), ay - int(Inches(0.01)), int(Inches(1.2)), int(Inches(0.14)), actual.get("label", "Actual"), size="caption", color=C["secondary"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Owner + Target Date required for each milestone"), size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
