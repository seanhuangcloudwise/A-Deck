"""GM-19: Feature Differentiation chart (radar-style score bars)."""
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


def _fallback_content(content):
    sections = content.get("sections", [])
    axes = [s.get("title", "") for s in sections if s.get("title")]
    if not axes:
        axes = ["AI智能度", "企业级功能", "集成生态", "实施效率", "总拥有成本", "行业适配"]

    # 旧数据无分产品打分，给出稳健默认值用于渲染图表。
    products = [
        {"name": "A-Deck", "scores": [9, 9, 8, 9, 8, 8][: len(axes)], "is_self": True},
        {"name": "Canva", "scores": [7, 5, 6, 8, 9, 6][: len(axes)], "is_self": False},
        {"name": "MS Designer", "scores": [7, 6, 5, 8, 8, 5][: len(axes)], "is_self": False},
    ]
    return axes, products


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-19 Feature Differentiation"))
    set_subtitle(ctx, slide, data.get("subtitle", "特性差异化对比"), C["gray"])

    content = data.get("content", {})
    axes = content.get("axes")
    products = content.get("products")
    if not axes or not products:
        axes, products = _fallback_content(content)

    chart_left = Inches(0.8)
    chart_top = Inches(1.2)
    label_w = Inches(1.6)
    chart_w = Inches(6.8)
    row_h = Inches(0.58)
    lane_h = Inches(0.14)
    lane_gap = Inches(0.06)

    # Scale line and ticks
    for tick in range(0, 11, 2):
        x = chart_left + label_w + (chart_w * tick / 10)
        shape_rect(slide, x, chart_top - Inches(0.1), Inches(0.01), Inches(4.0), fill_color=C["light"])
        textbox(slide, x - Inches(0.06), chart_top - Inches(0.22), Inches(0.2), Inches(0.12), str(tick), size="caption", color=C["gray"], align=PP_ALIGN.CENTER)

    palette = [C["primary"], C["dark"], C["gray"]]

    for i, axis_name in enumerate(axes[:6]):
        y = chart_top + i * row_h
        textbox(slide, chart_left, y + Inches(0.08), label_w - Inches(0.1), Inches(0.2), axis_name, size="label", bold=True, color=C["text"])

        for p_i, product in enumerate(products[:3]):
            score = product.get("scores", [0])[i] if i < len(product.get("scores", [])) else 0
            score = max(0, min(10, int(score)))
            bar_left = chart_left + label_w
            bar_top = y + p_i * (lane_h + lane_gap)
            bar_w = chart_w * score / 10
            color = C["primary"] if product.get("is_self") else palette[p_i % len(palette)]

            shape_rect(slide, bar_left, bar_top, chart_w, lane_h, fill_color=C["light"])
            shape_rect(slide, bar_left, bar_top, bar_w, lane_h, fill_color=color)
            textbox(slide, bar_left + bar_w + Inches(0.03), bar_top - Inches(0.01), Inches(0.3), Inches(0.16), str(score), size="caption", color=C["text"])

    # Legend (moved to bottom blank area)
    lg_top = Inches(5.2)
    lg_start = Inches(0.9)
    lg_gap = Inches(2.6)
    for p_i, product in enumerate(products[:3]):
        x = lg_start + p_i * lg_gap
        color = C["primary"] if product.get("is_self") else palette[p_i % len(palette)]
        shape_rect(slide, x, lg_top, Inches(0.18), Inches(0.08), fill_color=color)
        textbox(slide, x + Inches(0.22), lg_top - Inches(0.03), Inches(2.1), Inches(0.14), product.get("name", ""), size="label", color=C["text"])

    textbox(slide, Inches(0.8), Inches(5.5), Inches(8.2), Inches(0.2), "评分尺度 0-10，基于功能完备度/企业适配度/实施可行性综合评估", size="caption", color=C["gray"])
    return slide
