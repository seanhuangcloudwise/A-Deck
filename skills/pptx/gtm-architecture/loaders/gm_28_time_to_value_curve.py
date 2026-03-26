"""
GM-07: Time-To-Value Curve Loader
价值实现时间曲线
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from pptx_lib import layout_by_names, header  # noqa: F403
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, shape_rect

def load_slide(ctx, data):
    """装载GM-07: Time-To-Value Curve"""
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    header(slide, data["title"])
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    content = data["content"]
    stages = content["stages"]
    
    # 绘制时间轴和曲线
    chart_left = Inches(1.0)
    chart_top = Inches(1.3)
    chart_width = Inches(7.0)
    chart_height = Inches(2.8)
    
    # 坐标轴
    # X轴
    shape_rect(slide, chart_left, chart_top + chart_height, chart_width, Inches(0.05),
               fill_color=C["text"])
    # Y轴
    shape_rect(slide, chart_left, chart_top, Inches(0.05), chart_height,
               fill_color=C["text"])
    
    # 绘制数据点和连接
    max_value = max(int(s["cumulative_value"].replace("$", "").replace(",", "")) 
                    for s in stages)
    
    points = []
    for i, stage in enumerate(stages):
        x = chart_left + chart_width * (i / (len(stages) - 1)) if len(stages) > 1 else chart_left
        value = int(stage["cumulative_value"].replace("$", "").replace(",", ""))
        y = chart_top + chart_height - (chart_height * value / max_value)
        
        points.append((x, y))
        
        # 数据点
        shape_rect(slide, x - Inches(0.08), y - Inches(0.08), Inches(0.16), Inches(0.16),
                   fill_color=C["primary"])
        
        # 周数标签
        textbox(slide, x - Inches(0.3), chart_top + chart_height + Inches(0.1), 
                Inches(0.6), Inches(0.2), f"W{stage['week']}", size="label", 
                color=C["text"], align=PP_ALIGN.CENTER)
    
    # 绘制连接线
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # 简化：用矩形表示连接线
        line_width = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        line_angle = Pt(1)
        
        # 这里为简化，直接用价值标签表示
        textbox(slide, (x1 + x2) / 2 - Inches(0.4), (y1 + y2) / 2, Inches(0.8), 
                Inches(0.2), "↗", size="h3", color=C["primary"], align=PP_ALIGN.CENTER)
    
    # 阶段和价值信息
    info_top = Inches(4.3)
    col_width = Inches(1.8)
    
    for i, stage in enumerate(stages):
        left = Inches(0.5) + i * (col_width + Inches(0.1))
        
        # 相位
        textbox(slide, left, info_top, col_width, Inches(0.3),
                stage["phase"], size="label", bold=True, color=C["dark"],
                align=PP_ALIGN.CENTER)
        
        # 价值
        textbox(slide, left, info_top + Inches(0.35), col_width, Inches(0.3),
                stage["cumulative_value"], size="label", bold=True, color=C["primary"],
                align=PP_ALIGN.CENTER)
    
    # ROI breakeven标注
    textbox(slide, Inches(0.5), Inches(5.0), Inches(8.5), Inches(0.25),
            f"ROI达成周期: {content.get('roi_breakeven', 'N/A')}", 
            size="label", bold=True, color=C["dark"], align=PP_ALIGN.LEFT)
    
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
