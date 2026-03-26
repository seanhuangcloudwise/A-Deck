"""RA-08 Risk mitigation kanban."""

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
    header(slide, data.get("title", "RA-08 Risk Mitigation Kanban"))
    set_subtitle(ctx, slide, data.get("subtitle", "风险与缓解看板"), C["gray"])

    content = data.get("content", {})
    columns = content.get("columns", [])

    left = int(Inches(0.55))
    top = int(Inches(1.2))
    col_w = int(Inches(2.1))
    col_h = int(Inches(4.8))
    gap = int(Inches(0.1))

    total_cards = 0
    for c_i, col in enumerate(columns[:4]):
        x = left + c_i * (col_w + gap)
        shape_rect(slide, x, top, col_w, int(Inches(0.34)), fill_color=C["dark"])
        risks = col.get("risks", [])
        textbox(slide, x, top + int(Inches(0.03)), col_w, int(Inches(0.22)), col.get("name", ""), size="label", bold=True, color=C["white"])
        textbox(slide, x + col_w - int(Inches(0.45)), top + int(Inches(0.03)), int(Inches(0.4)), int(Inches(0.2)), str(len(risks[:6])), size="label", bold=True, color=C["secondary"], align=PP_ALIGN.RIGHT)
        shape_rect(slide, x, top + int(Inches(0.36)), col_w, col_h - int(Inches(0.36)), fill_color=C["light"], line_color=C["line"])

        for r_i, risk in enumerate(risks[:6]):
            total_cards += 1
            y = top + int(Inches(0.43)) + r_i * int(Inches(0.7))
            score = risk.get("score", "P3xI3")
            shape_rect(slide, x + int(Inches(0.07)), y, col_w - int(Inches(0.14)), int(Inches(0.62)), fill_color=C["white"], line_color=C["line"])
            textbox(slide, x + int(Inches(0.1)), y + int(Inches(0.06)), col_w - int(Inches(0.2)), int(Inches(0.22)), risk.get("title", ""), size="caption", bold=True, color=C["text"])
            textbox(slide, x + int(Inches(0.1)), y + int(Inches(0.3)), col_w - int(Inches(0.2)), int(Inches(0.18)), score, size="caption", color=C["gray"])
            if risk.get("new", False):
                textbox(slide, x + col_w - int(Inches(0.34)), y + int(Inches(0.03)), int(Inches(0.26)), int(Inches(0.14)), "NEW", size="micro", bold=True, color=C["accent6"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Risk scoring: P(1-5) x I(1-5)") + f" | Total risks: {total_cards}", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)

    return slide
