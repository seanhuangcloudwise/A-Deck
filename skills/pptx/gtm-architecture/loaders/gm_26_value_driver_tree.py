"""
GM-05: Value Driver Tree Loader
价值驱动树
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
    装载GM-05: Value Driver Tree
    """
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    header(slide, data["title"])
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    content = data["content"]
    drivers = content["drivers"]
    
    # 总价值顶部
    total_top = Inches(1.2)
    textbox(slide, Inches(0.5), total_top, Inches(8.5), Inches(0.35),
            content["total_value"], size="body", bold=True, color=C["dark"],
            align=PP_ALIGN.CENTER)
    
    # 树形结构：3列驱动因素
    tree_top = Inches(1.8)
    col_width = Inches(2.8)
    spacing = Inches(0.3)
    
    for i, (driver_key, driver_data) in enumerate(drivers.items()):
        left = Inches(0.5) + i * (col_width + spacing)
        
        # 驱动因素框
        shape_rect(slide, left, tree_top, col_width, Inches(0.5),
                   fill_color=C["primary"])
        
        # 标题
        textbox(slide, left, tree_top, col_width, Inches(0.5),
                driver_data["title"], size="body", bold=True, color=C["white"],
                align=PP_ALIGN.CENTER)
        
        # 数值
        textbox(slide, left, tree_top + Inches(0.6), col_width, Inches(0.35),
                driver_data["impact"], size="h3", bold=True, color=C["primary"],
                align=PP_ALIGN.CENTER)
        
        # 杠杆
        y = tree_top + Inches(1.1)
        for lever in driver_data.get("levers", [])[:2]:
            textbox(slide, left + Inches(0.1), y, col_width - Inches(0.2), 
                    Inches(0.4), f"→ {lever}", size="label", color=C["text"],
                    align=PP_ALIGN.LEFT)
            y += Inches(0.45)
    
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
