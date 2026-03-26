"""
GM-08: Baseline → Target KPI Loader
基线与目标KPI指标
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from pptx_lib import layout_by_names, header  # noqa: F403
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, render_table_grid, shape_rect

def load_slide(ctx, data):
    """装载GM-08: Baseline → Target KPI"""
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    header(slide, data["title"])
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    content = data["content"]
    kpis = content["kpis"]
    
    # 创建表格
    headers = ["指标", "基线 (Baseline)", "目标 (Target)", "改进"]
    rows = [
        [kpi["metric"], kpi["baseline"], kpi["target"], kpi["improvement"]]
        for kpi in kpis
    ]
    
    col_widths = [Inches(2.2), Inches(1.8), Inches(1.8), Inches(1.7)]
    
    render_table_grid(slide, Inches(0.4), Inches(1.2), headers, rows, {
        "header_bg": C["dark"],
        "header_text": C["white"],
        "row_bg": C["light"],
        "row_text": C["text"],
        "border": C["gray"],
    }, col_widths=col_widths)
    
    # 跟踪方式
    tracking_top = Inches(3.8)
    textbox(slide, Inches(0.4), tracking_top, Inches(1.0), Inches(0.25),
            "跟踪方式", size="label", bold=True, color=C["dark"],
            align=PP_ALIGN.LEFT)
    
    y = tracking_top + Inches(0.35)
    for track_method in content.get("tracking", []):
        textbox(slide, Inches(0.5), y, Inches(8.0), Inches(0.25),
                f"→ {track_method}", size="caption", color=C["text"],
                align=PP_ALIGN.LEFT)
        y += Inches(0.3)
    
    return slide


def set_subtitle(ctx, slide, text, gray_color=None):
    """设置副标题"""
    subtitle_ph = next(
        (s for s in slide.shapes
         if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1),
        None,
    )
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))
