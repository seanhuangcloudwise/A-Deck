"""
GM-06: Capability-Outcome Trace Matrix Loader
能力-结果映射矩阵
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from pptx_lib import layout_by_names, header  # noqa: F403
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, render_table_grid

def load_slide(ctx, data):
    """装载GM-06: Capability-Outcome Trace Matrix"""
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    header(slide, data["title"])
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    content = data["content"]
    mappings = content["mappings"]
    
    # 表格数据
    headers = ["A-Deck 功能", "目标用户", "关键成果", "商业价值"]
    rows = [
        [m["capability"], m["users"], m["outcome"], m["business_result"]]
        for m in mappings
    ]
    
    col_widths = [Inches(2.0), Inches(1.5), Inches(2.0), Inches(2.0)]
    
    render_table_grid(slide, Inches(0.4), Inches(1.2), headers, rows, {
        "header_bg": C["dark"],
        "header_text": C["white"],
        "row_bg": C["light"],
        "row_text": C["text"],
        "border": C["gray"],
    }, col_widths=col_widths)
    
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
