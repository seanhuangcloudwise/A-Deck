"""
GM-01: Positioning Statement Loader
装载器示例 - 展示装载器的标准结构
"""

import sys
from pathlib import Path

# 构建绝对导入路径
LOADER_DIR = Path(__file__).resolve().parent
GTM_DIR = LOADER_DIR.parent
PPTX_DIR = GTM_DIR.parent
SHARED_DIR = PPTX_DIR / "shared"
SCRIPTS_DIR = PPTX_DIR / "scripts"

# 添加路径
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SHARED_DIR))
sys.path.insert(0, str(PPTX_DIR))

# 现在导入
from pptx_lib import layout_by_names, textbox, header  # noqa: F403
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 导入共用渲染工具 - 直接从文件导入
import importlib.util
_spec = importlib.util.spec_from_file_location("renderer_utils", SHARED_DIR / "renderer_utils.py")
_renderer_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_renderer_utils)
shape_rect = _renderer_utils.shape_rect
shared_textbox = _renderer_utils.textbox


def load_slide(ctx, data):
    """
    装载GM-01: Positioning Statement
    
    Args:
        ctx: BuildContext (pptx_lib提供)
        data: dict 包含以下字段
            {
                "title": "GM-01 Positioning Statement | A-Deck 市场定位",
                "subtitle": "For 产品/营销团队 | 结构化定位链路",
                "content": {
                    "target": "...",
                    "problem": "...",
                    "product": "...",
                    "differentiator": "...",
                    "category": "..."
                }
            }
    
    Returns:
        slide: 生成的Slide对象
    """
    
    C = ctx.colors
    # 1. 获取幻灯片布局
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    
    # 2. 设置标题
    header(slide, data["title"])
    
    # 3. 设置副标题
    set_subtitle(ctx, slide, data["subtitle"], C["gray"])
    
    # 4. 渲染核心内容：5个定位框
    left = Inches(0.5)
    top = Inches(1.2)
    box_width = Inches(1.6)
    box_height = Inches(1.2)
    spacing = Inches(0.15)
    
    items = [
        ("Target", data["content"]["target"], C["primary"]),
        ("Problem", data["content"]["problem"], C["secondary"]),
        ("Product", data["content"]["product"], C["primary"]),
        ("Differentiator", data["content"]["differentiator"], C["dark"]),
        ("Category", data["content"]["category"], C["text"]),
    ]
    
    x = left
    for label, description, bg_color in items:
        # 背景框
        shape_rect(slide, x, top, box_width, box_height,
                   fill_color=bg_color)
        
        # 标签
        textbox(slide, x, top + Inches(0.05), box_width, Inches(0.25),
                label, size="body", bold=True, color=C["white"],
                align=PP_ALIGN.CENTER)
        
        # 描述文本
        textbox(slide, x + Inches(0.05), top + Inches(0.35), 
                box_width - Inches(0.1), Inches(0.8),
                description, size="label", color=C["white"],
                align=PP_ALIGN.CENTER)
        
        x += box_width + spacing
    
    return slide


def set_subtitle(ctx, slide, text, gray_color=None):
    """设置副标题（如果存在的话）"""
    subtitle_ph = next(
        (s for s in slide.shapes
         if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1),
        None,
    )
    if subtitle_ph is not None and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))
    else:
        # 如果没有占位符，用文本框添加
        textbox(slide, Inches(0.5), Inches(0.70), Inches(8.6), Inches(0.25),
                text, size="label", color=C["gray"])
