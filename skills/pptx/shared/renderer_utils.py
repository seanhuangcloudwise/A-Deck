"""
共用渲染器工具集
- 所有装载器共享的、数据驱动的render函数
- 接收(ctx, data)，完成样式和布局的统一处理
"""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


_THEME = {
    "text": (47, 47, 47),
    "line": (180, 190, 200),
    "font_scale": 1.0,
    "min_font_size": 8.0,
    "font_tokens": {
        "display": 28.0,
        "title": 24.0,
        "h2": 20.0,
        "h3": 16.0,
        "subtitle": 14.0,
        "body": 12.0,
        "label": 10.0,
        "caption": 9.0,
        "micro": 8.0,
    },
}


def configure_theme(colors=None, template_spec=None):
    """Configure shared renderer defaults from template/theme context."""
    global _THEME
    if colors:
        if "text" in colors:
            _THEME["text"] = colors["text"]
        if "line" in colors:
            _THEME["line"] = colors["line"]

    if template_spec:
        typography = template_spec.get("typography", {})
        if "font_scale" in typography:
            _THEME["font_scale"] = float(typography["font_scale"])
        if "min_font_size" in typography:
            _THEME["min_font_size"] = float(typography["min_font_size"])
        for key, value in typography.get("tokens", {}).items():
            try:
                _THEME["font_tokens"][key] = float(value)
            except (TypeError, ValueError):
                pass
        # Inject default_styles.line_color as the shared line/border default
        ds = template_spec.get("default_styles", {})
        line_color = ds.get("line_color")
        if line_color and isinstance(line_color, (list, tuple)) and len(line_color) == 3:
            _THEME["line"] = tuple(line_color)
            # Also propagate to the colors dict so C["line"] picks it up
            if colors is not None:
                colors["line"] = RGBColor(*line_color) if not isinstance(colors.get("line"), tuple) else tuple(line_color)


def _scaled_size(size):
    scaled = float(size) * float(_THEME["font_scale"])
    return max(scaled, float(_THEME["min_font_size"]))


def resolve_font_size(size):
    """Resolve a numeric size or a typography token name to final point size."""
    if isinstance(size, str):
        base = _THEME["font_tokens"].get(size, _THEME["font_tokens"]["body"])
        return _scaled_size(base)
    return _scaled_size(size)

# ============================================================================
# 工具函数（来自pptx_lib，这里本地化重要函数避免依赖）
# ============================================================================

def textbox(slide, left, top, width, height, text, size=11, bold=False, color=None, align=PP_ALIGN.LEFT):
    """添加文本框"""
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(resolve_font_size(size))
    p.font.bold = bold
    color = color if color is not None else _THEME["text"]
    p.font.color.rgb = RGBColor(*color) if isinstance(color, tuple) else color
    p.alignment = align
    return shape


def shape_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=1):
    """添加矩形"""
    shape = slide.shapes.add_shape(1, left, top, width, height)
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_color) if isinstance(fill_color, tuple) else fill_color
    if line_color is None and fill_color is not None:
        line_color = _THEME["line"]
    if line_color:
        shape.line.color.rgb = RGBColor(*line_color) if isinstance(line_color, tuple) else line_color
        shape.line.width = Pt(line_width)
    return shape


def render_two_col_list(slide, x_offset, y_offset, col1_data, col2_data, colors):
    """
    渲染两列列表（通常用于对比、功能列表等）
    
    :param slide: Slide object
    :param x_offset: 起始左边距 (EMU)
    :param y_offset: 起始上边距 (EMU)
    :param col1_data: [{"title": "...", "items": [...]}, ...]
    :param col2_data: [{"title": "...", "items": [...]}, ...]
    :param colors: {"header": (r,g,b), "item": (r,g,b), ...}
    """
    col_width = Inches(4.0)
    row_height = Inches(0.35)
    
    # 左列
    y = y_offset
    for section in col1_data:
        textbox(slide, x_offset, y, col_width, Inches(0.25), section["title"], 
                size=11, bold=True, color=colors.get("header"))
        y += Inches(0.3)
        for item in section.get("items", []):
            textbox(slide, x_offset + Inches(0.15), y, col_width - Inches(0.3), row_height, 
                    f"• {item}", size=10, color=colors.get("item"))
            y += row_height
        y += Inches(0.15)
    
    # 右列
    y = y_offset
    for section in col2_data:
        textbox(slide, x_offset + col_width + Inches(0.3), y, col_width, Inches(0.25), 
                section["title"], size=11, bold=True, color=colors.get("header"))
        y += Inches(0.3)
        for item in section.get("items", []):
            textbox(slide, x_offset + col_width + Inches(0.45), y, col_width - Inches(0.3), 
                    row_height, f"• {item}", size=10, color=colors.get("item"))
            y += row_height
        y += Inches(0.15)


def render_three_col_list(slide, x_offset, y_offset, col1_data, col2_data, col3_data, colors):
    """
    渲染三列列表
    """
    col_width = Inches(2.7)
    row_height = Inches(0.35)
    
    cols = [col1_data, col2_data, col3_data]
    for col_idx, col_data in enumerate(cols):
        x = x_offset + col_idx * (col_width + Inches(0.2))
        y = y_offset
        
        for section in col_data:
            textbox(slide, x, y, col_width, Inches(0.25), section["title"],
                    size=10, bold=True, color=colors.get("header"))
            y += Inches(0.28)
            for item in section.get("items", []):
                textbox(slide, x + Inches(0.1), y, col_width - Inches(0.2), row_height,
                        f"• {item}", size=9, color=colors.get("item"))
                y += row_height
            y += Inches(0.1)


def render_horizontal_flow(slide, x_offset, y_offset, items, colors):
    """
    渲染水平流程（流程框、箭头等）
    
    :param items: [{"label": "...", "desc": "..."}, ...]
    :param colors: {"box": (r,g,b), "text": (r,g,b), ...}
    """
    box_width = Inches(1.3)
    box_height = Inches(0.6)
    spacing = Inches(0.15)
    
    x = x_offset
    for i, item in enumerate(items):
        # 流程框
        shape_rect(slide, x, y_offset, box_width, box_height, 
                   fill_color=colors.get("box"), line_color=colors.get("box"))
        
        # 标签
        textbox(slide, x, y_offset + Inches(0.08), box_width, Inches(0.5),
                item["label"], size=9, bold=True, color=colors.get("text"), 
                align=PP_ALIGN.CENTER)
        
        # 描述（可选）
        if "desc" in item:
            textbox(slide, x, y_offset + Inches(0.7), box_width, Inches(0.4),
                    item["desc"], size=8, color=colors.get("desc"))
        
        x += box_width + spacing
        
        # 箭头（最后一个不添加）
        if i < len(items) - 1:
            textbox(slide, x - Inches(0.1), y_offset + Inches(0.2), Inches(0.2), Inches(0.2),
                    "→", size=14, color=colors.get("arrow"))
            x += Inches(0.1)


def render_table_grid(slide, x_offset, y_offset, headers, rows, colors, col_widths=None):
    """
    渲染简单表格（使用矩形和文本框）
    
    :param headers: ["列1", "列2", "列3"]
    :param rows: [[cell, cell, ...], ...]
    :param col_widths: [Inches(2.0), ...] or None (均匀分配)
    :param colors: {"header_bg": (r,g,b), "header_text": (r,g,b), ...}
    """
    if col_widths is None:
        col_widths = [Inches(2.5)] * len(headers)
    
    row_height = Inches(0.4)
    
    # 表头
    x = x_offset
    for col_idx, header in enumerate(headers):
        shape_rect(slide, x, y_offset, col_widths[col_idx], row_height,
                   fill_color=colors.get("header_bg"),
                   line_color=colors.get("border", (150, 150, 150)))
        textbox(slide, x, y_offset, col_widths[col_idx], row_height,
                header, size=9, bold=True, color=colors.get("header_text"),
                align=PP_ALIGN.CENTER)
        x += col_widths[col_idx]
    
    # 数据行
    y = y_offset + row_height
    for row in rows:
        x = x_offset
        for col_idx, cell in enumerate(row):
            shape_rect(slide, x, y, col_widths[col_idx], row_height,
                       fill_color=colors.get("row_bg", (255, 255, 255)),
                       line_color=colors.get("border", (200, 200, 200)))
            textbox(slide, x, y, col_widths[col_idx], row_height,
                    str(cell), size=8, color=colors.get("row_text"),
                    align=PP_ALIGN.CENTER)
            x += col_widths[col_idx]
        y += row_height


def render_matrix_2d(slide, x_offset, y_offset, matrix_data, colors):
    """
    渲染2D矩阵（如竞品对标、象限图等）
    
    :param matrix_data: {
        "x_label": "轴标签", "y_label": "...",
        "quadrants": [
            {"pos": "tl", "title": "...", "items": [...]},
            {"pos": "tr", "title": "...", "items": [...]},
            ...
        ]
    }
    """
    cell_width = Inches(3.5)
    cell_height = Inches(2.2)
    
    label_height = Inches(0.3)
    
    # 绘制四象限
    positions = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    
    for quadrant in matrix_data.get("quadrants", []):
        pos_key = quadrant["pos"]
        col, row = positions[pos_key]
        x = x_offset + col * (cell_width + Inches(0.1))
        y = y_offset + row * (cell_height + Inches(0.1))
        
        # 背景
        shape_rect(slide, x, y, cell_width, cell_height,
                   fill_color=quadrant.get("bg_color", colors.get("quadrant_bg")),
                   line_color=colors.get("border"))
        
        # 标题
        textbox(slide, x, y, cell_width, label_height,
                quadrant["title"], size=10, bold=True, 
                color=quadrant.get("title_color", colors.get("quadrant_title")),
                align=PP_ALIGN.CENTER)
        
        # 项目列表
        inner_y = y + label_height + Inches(0.1)
        for item in quadrant.get("items", []):
            textbox(slide, x + Inches(0.15), inner_y, cell_width - Inches(0.3), Inches(0.3),
                    f"• {item}", size=8, color=colors.get("item_text"))
            inner_y += Inches(0.35)


# ============================================================================
# 装载器协议规范
# ============================================================================

def loader_protocol_example():
    """
    每个装载器应该遵循这个协议：
    
    def load_slide(ctx, data):
        '''
        装载一张图表
        
        Args:
            ctx: BuildContext (pptx_lib提供)
            data: dict - 该图表所需的全部业务数据
                {
                    "title": "图表标题",
                    "subtitle": "副标题",
                    "content": {...},  # 图表特定的内容
                    ...
                }
        
        Returns:
            slide: 生成的Slide对象
        '''
        slide = add_content_slide(ctx)
        # ... 基于 data["content"] 进行渲染 ...
        return slide
    """
    pass
