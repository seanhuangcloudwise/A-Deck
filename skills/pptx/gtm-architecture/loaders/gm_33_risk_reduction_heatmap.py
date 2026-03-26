"""GM-33: Risk reduction heatmap with before/after markers."""
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


def _fallback_risks(content):
    risks = []
    level = {"LOW": 2, "MEDIUM": 3, "HIGH": 4}
    for sec in content.get("sections", []):
        domain = sec.get("title", "Domain")
        for idx, item in enumerate(sec.get("items", [])):
            before = 4
            after = 3
            if "[" in item and "->" in item and "]" in item:
                bracket = item[item.find("[") + 1 : item.find("]")]
                b, a = bracket.split("->")
                before = level.get(b.strip().upper(), 4)
                after = level.get(a.strip().upper(), 3)
            risks.append(
                {
                    "name": item.split("：")[0],
                    "domain": domain,
                    "before": [before, before],
                    "after": [after, after],
                }
            )
    return risks


def _cell_color(score, risk_colors):
    if score >= 8:
        return risk_colors["high"]
    if score >= 6:
        return risk_colors["med_high"]
    if score >= 4:
        return risk_colors["medium"]
    if score >= 2:
        return risk_colors["low"]
    return risk_colors["very_low"]


def load_slide(ctx, data):
    C = ctx.colors
    # Semantic risk-level colors
    _RISK = {"high": C["dark"], "med_high": (95, 138, 160), "medium": C["secondary"], "low": (186, 229, 232), "very_low": (236, 246, 247)}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-33 Risk Reduction Heatmap"))
    set_subtitle(ctx, slide, data.get("subtitle", "风险下降前后对比"), C["gray"])

    content = data.get("content", {})
    risks = content.get("risks") or _fallback_risks(content)
    risks = risks[:12]

    grid_left = Inches(2.0)
    grid_top = Inches(1.2)
    cell = Inches(0.9)

    # 5x5 grid
    for r in range(5):
        for c in range(5):
            score = (5 - r) + (c + 1)
            shape_rect(slide, grid_left + c * cell, grid_top + r * cell, cell, cell, fill_color=_cell_color(score, _RISK), line_color=C["line"])

    # axes labels
    y_labels = ["Critical", "High", "Medium", "Low", "Very Low"]
    x_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
    for i, lbl in enumerate(y_labels):
        textbox(slide, Inches(0.6), grid_top + i * cell + Inches(0.3), Inches(1.3), Inches(0.2), lbl, size="label", color=C["text"], align=PP_ALIGN.RIGHT)
    for i, lbl in enumerate(x_labels):
        textbox(slide, grid_left + i * cell, grid_top + 5 * cell + Inches(0.05), cell, Inches(0.3), lbl, size="caption", color=C["text"], align=PP_ALIGN.CENTER)
    textbox(slide, Inches(0.65), Inches(1.0), Inches(1.2), Inches(0.2), "Impact", size="label", bold=True, color=C["dark"], align=PP_ALIGN.RIGHT)
    textbox(slide, grid_left, Inches(5.8), Inches(4.5), Inches(0.2), "Likelihood", size="label", bold=True, color=C["dark"], align=PP_ALIGN.CENTER)

    # before/after markers + list
    list_top = Inches(1.25)
    for i, rk in enumerate(risks[:8]):
        bx, by = rk.get("before", [4, 4])
        ax, ay = rk.get("after", [3, 3])
        bx = max(1, min(5, int(bx)))
        by = max(1, min(5, int(by)))
        ax = max(1, min(5, int(ax)))
        ay = max(1, min(5, int(ay)))

        before_x = grid_left + (bx - 1) * cell + Inches(0.36)
        before_y = grid_top + (5 - by) * cell + Inches(0.28)
        after_x = grid_left + (ax - 1) * cell + Inches(0.36)
        after_y = grid_top + (5 - ay) * cell + Inches(0.28)

        textbox(slide, before_x, before_y, Inches(0.2), Inches(0.2), "●", size="label", color=C["dark"], align=PP_ALIGN.CENTER)
        textbox(slide, after_x, after_y, Inches(0.2), Inches(0.2), "○", size="label", color=C["primary"], align=PP_ALIGN.CENTER)

        ly = list_top + i * Inches(0.45)
        textbox(slide, Inches(6.8), ly, Inches(2.0), Inches(0.2), f"R{i+1} {rk.get('name', '')}", size="caption", bold=True, color=C["text"])
        textbox(slide, Inches(6.8), ly + Inches(0.18), Inches(2.0), Inches(0.2), f"{rk.get('domain', '')}  {bx},{by}→{ax},{ay}", size="caption", color=C["gray"])

    textbox(slide, Inches(6.8), Inches(5.0), Inches(2.0), Inches(0.2), "● Before   ○ After", size="label", color=C["text"])
    textbox(slide, Inches(0.55), Inches(5.95), Inches(8.3), Inches(0.18), "评分尺度 1-5；标记展示基线与残余风险位置", size="caption", color=C["gray"])
    return slide
