"""RA-06 Release train quarterly plan."""

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
    header(slide, data.get("title", "RA-06 Release Train Quarterly"))
    set_subtitle(ctx, slide, data.get("subtitle", "发布列车/季度计划"), C["gray"])

    content = data.get("content", {})
    periods = content.get("periods", ["Q1", "Q2", "Q3", "Q4"])
    trains = content.get("trains", [])

    left = int(Inches(0.7))
    top = int(Inches(1.2))
    label_w = int(Inches(1.8))
    col_w = int(Inches(1.6))
    head_h = int(Inches(0.36))
    row_h = int(Inches(0.65))

    shape_rect(slide, left, top, label_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top + int(Inches(0.03)), label_w, int(Inches(0.22)), "Train", size="label", bold=True, color=C["white"])

    for i, p in enumerate(periods[:4]):
        x = left + label_w + i * col_w
        shape_rect(slide, x, top, col_w, head_h, fill_color=C["dark"])
        textbox(slide, x, top + int(Inches(0.03)), col_w, int(Inches(0.22)), p, size="label", bold=True, color=C["white"])

    for r_i, t in enumerate(trains[:5]):
        y = top + head_h + r_i * row_h
        shape_rect(slide, left, y, label_w, row_h, fill_color=C["light"])
        textbox(slide, left + int(Inches(0.05)), y + int(Inches(0.07)), label_w - int(Inches(0.1)), int(Inches(0.2)), t.get("name", ""), size="label", bold=True, color=C["text"])
        for i in range(len(periods[:4])):
            x = left + label_w + i * col_w
            shape_rect(slide, x, y, col_w, row_h, fill_color=C["white"], line_color=C["line"])
        for m in t.get("milestones", [])[:3]:
            pi = max(0, min(3, int(m.get("period_index", 0))))
            x = left + label_w + pi * col_w + int(Inches(0.1))
            y0 = y + int(Inches(0.17))
            shape_rect(slide, x, y0, col_w - int(Inches(0.2)), int(Inches(0.22)), fill_color=C["secondary"])
            textbox(slide, x + int(Inches(0.03)), y0 + int(Inches(0.03)), col_w - int(Inches(0.26)), int(Inches(0.15)), m.get("label", ""), size="caption", color=C["text"])

    # Release markers
    for rm in content.get("release_markers", [{"period_index": 1, "label": "Release 1"}, {"period_index": 3, "label": "Release 2"}]):
        pi = max(0, min(3, int(rm.get("period_index", 0))))
        x = left + label_w + pi * col_w + int(col_w / 2)
        shape_rect(slide, x - int(Inches(0.01)), top, int(Inches(0.02)), int(Inches(4.0)), fill_color=C["text"])
        textbox(slide, x - int(Inches(0.5)), top - int(Inches(0.18)), int(Inches(1.0)), int(Inches(0.14)), rm.get("label", "Release"), size="caption", color=C["text"])

    shape_rect(slide, int(Inches(0.55)), int(Inches(5.38)), int(Inches(0.18)), int(Inches(0.08)), fill_color=C["secondary"])
    textbox(slide, int(Inches(0.78)), int(Inches(5.36)), int(Inches(1.8)), int(Inches(0.14)), "Milestone Card", size="caption", color=C["text"])
    shape_rect(slide, int(Inches(2.15)), int(Inches(5.38)), int(Inches(0.02)), int(Inches(0.08)), fill_color=C["text"])
    textbox(slide, int(Inches(2.24)), int(Inches(5.36)), int(Inches(1.8)), int(Inches(0.14)), "Release Marker", size="caption", color=C["text"])
    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Release cadence reviewed in quarterly PI planning"), size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)

    return slide
