"""RA-01 Strategic roadmap timeline."""

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
    header(slide, data.get("title", "RA-01 Strategic Timeline"))
    set_subtitle(ctx, slide, data.get("subtitle", "战略路线图时间轴"), C["gray"])

    content = data.get("content", {})
    periods = content.get("periods", ["Q1", "Q2", "Q3", "Q4"])
    lanes = content.get("lanes", [])

    left = int(Inches(0.5))
    top = int(Inches(1.2))
    label_w = int(Inches(1.6))
    chart_w = int(Inches(7.9))
    head_h = int(Inches(0.35))
    lane_h = int(Inches(0.75))
    p_w = int(chart_w / max(1, len(periods)))

    shape_rect(slide, left, top, label_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top + int(Inches(0.03)), label_w, int(Inches(0.25)), "Theme", size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)

    for i, period in enumerate(periods):
        x = left + label_w + i * p_w
        bg = C["light"] if i == 0 else C["white"]
        shape_rect(slide, x, top, p_w, head_h, fill_color=bg, line_color=C["line"])
        textbox(slide, x, top + int(Inches(0.03)), p_w, int(Inches(0.25)), period, size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)

    for li, lane in enumerate(lanes[:6]):
        y = top + head_h + li * lane_h
        shape_rect(slide, left, y, label_w, lane_h, fill_color=C["dark"])
        textbox(slide, left + int(Inches(0.05)), y + int(Inches(0.07)), label_w - int(Inches(0.1)), lane_h - int(Inches(0.1)), lane.get("name", ""), size="label", bold=True, color=C["white"])

        for i in range(len(periods)):
            x = left + label_w + i * p_w
            bg = C["light"] if i % 2 == 0 else C["white"]
            shape_rect(slide, x, y, p_w, lane_h, fill_color=bg, line_color=C["line"])

        for item in lane.get("items", [])[:4]:
            start = max(0, min(len(periods) - 1, int(item.get("start", 0))))
            end = max(start, min(len(periods) - 1, int(item.get("end", start))))
            bx = left + label_w + start * p_w + int(Inches(0.05))
            bw = (end - start + 1) * p_w - int(Inches(0.1))
            by = y + int(Inches(0.08)) + int(item.get("row", 0)) * int(Inches(0.2))
            status = item.get("status", "plan")
            color = C["primary"] if status == "done" else (C["secondary"] if status == "wip" else C["gray"])
            shape_rect(slide, bx, by, bw, int(Inches(0.17)), fill_color=color)
            textbox(slide, bx + int(Inches(0.03)), by + int(Inches(0.01)), bw - int(Inches(0.06)), int(Inches(0.15)), item.get("label", ""), size="micro", color=C["text"])

    # Legend + footer
    lg_y = int(Inches(5.35))
    shape_rect(slide, int(Inches(0.55)), lg_y, int(Inches(0.18)), int(Inches(0.08)), fill_color=C["primary"])
    textbox(slide, int(Inches(0.76)), lg_y - int(Inches(0.02)), int(Inches(0.7)), int(Inches(0.14)), "Done", size="caption", color=C["text"])
    shape_rect(slide, int(Inches(1.45)), lg_y, int(Inches(0.18)), int(Inches(0.08)), fill_color=C["secondary"])
    textbox(slide, int(Inches(1.66)), lg_y - int(Inches(0.02)), int(Inches(0.7)), int(Inches(0.14)), "In Progress", size="caption", color=C["text"])
    shape_rect(slide, int(Inches(2.58)), lg_y, int(Inches(0.18)), int(Inches(0.08)), fill_color=C["gray"])
    textbox(slide, int(Inches(2.79)), lg_y - int(Inches(0.02)), int(Inches(0.8)), int(Inches(0.14)), "Planned", size="caption", color=C["text"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("time_range", "Time Range: FY2026") + " | Data as of: 2026-03", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
