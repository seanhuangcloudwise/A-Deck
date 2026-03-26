"""GM-35: Assumption sensitivity table."""
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
        (s for s in slide.shapes if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1),
        None,
    )
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def _fallback_assumptions(content):
    assumptions = []
    for sec in content.get("sections", [])[:8]:
        assumptions.append(
            {
                "name": sec.get("title", "Assumption"),
                "base": "100%",
                "conservative": "85%",
                "aggressive": "115%",
                "impact": "ROI ±8%",
                "critical": "风险-高" in sec.get("title", ""),
            }
        )
    return assumptions


def load_slide(ctx, data):
    C = ctx.colors
    _SCENARIO = {"base": C["primary"], "conservative": C["gray"], "aggressive": C["secondary"], "critical": C["dark"]}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-35 Assumption Sensitivity"))
    set_subtitle(ctx, slide, data.get("subtitle", "ROI稳健性分析"), C["gray"])

    content = data.get("content", {})
    assumptions = content.get("assumptions") or _fallback_assumptions(content)
    assumptions = assumptions[:10]

    left = Inches(0.5)
    top = Inches(1.2)
    headers = ["Assumption", "Base", "Conservative", "Aggressive", "Impact on ROI"]
    widths = [Inches(2.6), Inches(1.2), Inches(1.35), Inches(1.25), Inches(2.1)]
    head_h = Inches(0.38)
    row_h = Inches(0.38)

    # header
    x = left
    for i, h in enumerate(headers):
        shape_rect(slide, x, top, widths[i], head_h, fill_color=C["dark"])
        textbox(slide, x, top + Inches(0.03), widths[i], Inches(0.24), h, size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        x += widths[i]

    # rows
    for r_i, a in enumerate(assumptions):
        y = top + head_h + r_i * row_h
        bg = C["white"] if r_i % 2 == 0 else C["light"]
        if a.get("critical"):
            shape_rect(slide, left - Inches(0.03), y, Inches(0.03), row_h, fill_color=_SCENARIO["critical"])

        vals = [a.get("name", ""), a.get("base", ""), a.get("conservative", ""), a.get("aggressive", ""), a.get("impact", "")]
        x = left
        for c_i, val in enumerate(vals):
            shape_rect(slide, x, y, widths[c_i], row_h, fill_color=bg, line_color=C["line"])
            color = C["text"]
            if c_i == 1:
                color = _SCENARIO["base"]
            elif c_i == 2:
                color = _SCENARIO["conservative"]
            elif c_i == 3:
                color = _SCENARIO["aggressive"]
            textbox(slide, x + Inches(0.03), y + Inches(0.03), widths[c_i] - Inches(0.06), Inches(0.24), val, size="label", color=color, align=PP_ALIGN.CENTER if c_i > 0 else PP_ALIGN.LEFT)
            x += widths[c_i]

    textbox(slide, Inches(0.52), Inches(5.63), Inches(4.5), Inches(0.2), "高敏感假设以深色左边条标记", size="caption", color=C["text"])
    textbox(slide, Inches(0.52), Inches(5.84), Inches(8.3), Inches(0.2), "注：需在页脚补充假设来源与置信度口径", size="caption", color=C["gray"])
    return slide
