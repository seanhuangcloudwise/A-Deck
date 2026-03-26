"""
GM-03: Competitor Positioning Matrix Loader
竞争格局矩阵
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
    """
    装载GM-03: Competitor Matrix
    
    Args:
        ctx: BuildContext
        data: {
            "title": "...",
            "subtitle": "...",
            "content": {
                "x_label": "...",
                "y_label": "...",
                "competitors": [
                    {"name": "Company", "x": 8.5, "y": 8.0, "color": (r,g,b), "size": 300},
                    ...
                ]
            }
        }
    """
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    header(slide, data["title"])
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    content = data["content"]
    competitors = content["competitors"]
    
    # 绘制2D坐标系
    left = Inches(1.0)
    top = Inches(1.2)
    width = Inches(7.5)
    height = Inches(3.5)
    
    # 坐标系框
    shape_rect(slide, left, top, width, height,
               fill_color=C["white"],
               line_color=C["light"], line_width=1)
    
    # 网格线
    for i in range(0, 11, 2):
        x = left + width * (i / 10)
        y_start = top
        y_end = top + height
        # 垂直线
        shape_rect(slide, x, y_start, Inches(0.01), height,
                   fill_color=C["light"])
        
        # 水平线
        x_start = left
        x_end = left + width
        shape_rect(slide, x_start, y_end - height * (i / 10), width, Inches(0.01),
                   fill_color=C["light"])
    
    # 绘制竞争方
    for comp in competitors:
        # 计算位置 (x, y 范围 0-10)
        cx = left + width * (comp["x"] / 10)
        cy = top + height * (1 - comp["y"] / 10)  # Y轴反向
        size = Inches(comp.get("size", 200) / 1000)
        
        # 圆点
        shape_rect(slide, cx - size/2, cy - size/2, size, size,
                   fill_color=tuple(comp.get("color", C["primary"])))
        
        # 公司名标签
        textbox(slide, cx - size, cy + size, size * 2, Inches(0.25),
                comp["name"], size="label", bold=True, color=C["text"],
                align=PP_ALIGN.CENTER)
    
    # 坐标轴标签
    textbox(slide, left + width/2, top + height + Inches(0.15), Inches(3), Inches(0.25),
            content["x_label"], size="caption", bold=True, color=C["text"],
            align=PP_ALIGN.CENTER)
    
    textbox(slide, left - Inches(0.8), top + height/2, Inches(0.7), Inches(0.5),
            content["y_label"], size="caption", bold=True, color=C["text"],
            align=PP_ALIGN.CENTER)
    
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
        p.font.color.rgb = RGBColor(165, 167, 170)
