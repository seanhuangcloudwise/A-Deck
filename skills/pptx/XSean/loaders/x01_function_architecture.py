"""X01 Function Architecture loader.

Based on diagrams/x01-founction-architecture.md
Focus: layered architecture overview with group-first layout.
"""

import sys
from pathlib import Path

from lxml import etree
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))

from pptx_lib import header, layout_by_names
from renderer_utils import shape_rect, textbox


def set_subtitle(ctx, slide, text):
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
        p.font.color.rgb = RGBColor(*ctx.colors["gray"])


def content_region(ctx, top_pad_in=0.22, bottom_pad_in=0.12):
    x = int(ctx.safe_left)
    y = int(ctx.content_top + Inches(top_pad_in))
    w = int(ctx.safe_width)
    h = int(ctx.safe_bottom - y - Inches(bottom_pad_in))
    return x, y, w, h


def _rgb(value):
    return RGBColor(*value) if isinstance(value, tuple) else value


def _lighten(value, factor=0.7):
    rgb = value if isinstance(value, tuple) else (value[0], value[1], value[2])
    return tuple(int(channel + (255 - channel) * factor) for channel in rgb)


def _stack_text(text):
    chars = []
    for ch in str(text):
        if ch == " ":
            continue
        if ch == "/":
            chars.append("/")
            continue
        chars.append(ch)
    return "\n".join(chars)


def _set_dash(shape):
    ln = shape.element.spPr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(shape.element.spPr, qn("a:ln"))
    prst_dash = ln.find(qn("a:prstDash"))
    if prst_dash is None:
        prst_dash = etree.SubElement(ln, qn("a:prstDash"))
    prst_dash.set("val", "dash")


def _set_line(shape, color, width=0.5):
    shape.line.color.rgb = _rgb(color)
    shape.line.width = Pt(width)


def _set_no_line(shape):
    shape.line.fill.background()


def _rect_shape(slide, x, y, w, h, fill_color=None, line_color=None, line_width=0.5, dashed=False):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(x), int(y), int(w), int(h))
    if fill_color is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _rgb(fill_color)
    if line_color is None:
        _set_no_line(shape)
    else:
        _set_line(shape, line_color, line_width)
        if dashed:
            _set_dash(shape)
    return shape


def _center_text_in_shape(shape, text, color, size="micro", bold=False):
    tf = shape.text_frame
    tf.clear()
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = str(text)
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(8 if size == "micro" else 9 if size == "caption" else 10)
    p.font.bold = bold
    p.font.color.rgb = _rgb(color)


def _style_by_depth(depth, colors, storage=False):
    """Depth means information granularity level, not vertical order.

    All depths have fill.
    Only the largest-granularity level (depth=1) has border.
    Fill becomes darker as granularity goes from large to small.
    """
    base = colors["secondary"] if storage else colors["primary"]
    light_map = {
        1: 0.88,
        2: 0.78,
        3: 0.62,
        4: 0.52,
    }
    tone = _lighten(base, light_map.get(depth, 0.62))
    line = tone if depth == 1 else None
    return {"fill": tone, "line": line}


def _add_module(slide, x, y, w, h, label, colors, style, is_storage=False):
    fill = style["storage_fill"] if is_storage else style["module_fill"]
    line = style["storage_line"] if is_storage else style["module_line"]
    shp = _rect_shape(slide, x, y, w, h, fill_color=fill, line_color=line, line_width=0.5)
    if fill is not None:
        _center_text_in_shape(shp, label, colors["text"], size="micro")
    else:
        textbox(
            slide,
            int(x + Inches(0.04)),
            int(y + Inches(0.03)),
            int(w - Inches(0.08)),
            int(h - Inches(0.06)),
            str(label),
            size="micro",
            color=colors["text"],
            align=PP_ALIGN.CENTER,
        )
    return shp


def _choose_grid(mods, area_w, area_h):
    max_label = max((len((mod.get("name", "") if isinstance(mod, dict) else str(mod)).strip()) for mod in mods), default=0)
    count = len(mods)
    if count <= 3:
        cols = count
    elif count <= 6 and max_label <= 10:
        cols = 3
    elif max_label <= 6 and count >= 6:
        cols = 3
    elif max_label <= 8 and count >= 4:
        cols = 2
    else:
        cols = 1

    cols = max(1, min(cols, 3))
    rows = (count + cols - 1) // cols
    if rows > 4 and cols < 3:
        cols += 1
        rows = (count + cols - 1) // cols
    return cols, rows


def _use_left_title_mode(item, granularity_depth, group_count=0, module_count=0):
    mode = item.get("title_mode", "auto")
    if mode == "left":
        return True
    if mode == "top":
        return False
    if granularity_depth > 2:
        return False
    return group_count >= 2 or module_count >= 4


def _draw_layer_relation_arrow(slide, src_box, dst_box, colors, direction=None, label=""):
    """Draw directional arrow shape between two layer boxes.

    Placement rules:
    - Up/Down arrows: horizontally centered between the two layers,
      vertically centered in the gap.
    - Left/Right arrows: vertically centered between the two layers,
      horizontally centered in the gap.
    """
    sx = int(src_box[0] + src_box[2] * 0.5)
    sy = int(src_box[1] + src_box[3] * 0.5)
    dx = int(dst_box[0] + dst_box[2] * 0.5)
    dy = int(dst_box[1] + dst_box[3] * 0.5)

    if direction is None:
        direction = "down" if abs(dy - sy) >= abs(dx - sx) and dy >= sy else \
                    "up" if abs(dy - sy) >= abs(dx - sx) else \
                    "right" if dx >= sx else "left"
    direction = str(direction).lower()

    fill = _rgb(colors["secondary"])

    if direction in ("up", "down"):
        gap_top = int(min(src_box[1] + src_box[3], dst_box[1] + dst_box[3]))
        gap_bottom = int(max(src_box[1], dst_box[1]))
        gap_h = max(int(Inches(0.18)), gap_bottom - gap_top)
        ah = max(int(Inches(0.16)), min(int(Inches(0.34)), int(gap_h * 0.72)))
        aw = int(max(Inches(0.16), min(Inches(0.24), ah * 0.75)))
        ax = int((sx + dx) / 2 - aw / 2)
        ay = int((gap_top + gap_bottom) / 2 - ah / 2)
        shp_type = MSO_SHAPE.UP_ARROW if direction == "up" else MSO_SHAPE.DOWN_ARROW
        arrow = slide.shapes.add_shape(shp_type, ax, ay, aw, ah)
    else:
        gap_left = int(min(src_box[0] + src_box[2], dst_box[0] + dst_box[2]))
        gap_right = int(max(src_box[0], dst_box[0]))
        gap_w = max(int(Inches(0.22)), gap_right - gap_left)
        aw = max(int(Inches(0.2)), min(int(Inches(0.38)), int(gap_w * 0.72)))
        ah = int(max(Inches(0.12), min(Inches(0.2), aw * 0.62)))
        ax = int((gap_left + gap_right) / 2 - aw / 2)
        ay = int((sy + dy) / 2 - ah / 2)
        shp_type = MSO_SHAPE.LEFT_ARROW if direction == "left" else MSO_SHAPE.RIGHT_ARROW
        arrow = slide.shapes.add_shape(shp_type, ax, ay, aw, ah)

    arrow.fill.solid()
    arrow.fill.fore_color.rgb = fill
    arrow.line.fill.background()

    if label:
        if direction in ("up", "down"):
            lx = int(ax - Inches(0.2))
            ly = int(ay + ah + Inches(0.01))
            lw = int(aw + Inches(0.4))
            lh = int(Inches(0.14))
        else:
            lx = int(ax)
            ly = int(ay + ah + Inches(0.005))
            lw = int(aw)
            lh = int(Inches(0.14))
        textbox(slide, lx, ly, lw, lh, label, size="micro", color=colors["gray"], align=PP_ALIGN.CENTER)


def load_slide(ctx, data):
    """Render X01 layered architecture page.

    Content schema:
    content:
      side_labels:
        left: "可选左侧标签"
        right: "可选右侧标签"
      layers:
        - name: "能力/服务层"
          groups:
            - name: "分组A"
              modules:
                - id: "m1"
                  name: "模块1"
                  type: "module"   # module | storage
      external_zones:
        - title: "外部系统区"
          style: "dashed"
          items: ["ERP", "CRM"]
      links:
        - from: "m1"
          to: "m2"
          label: "可选"
    """
    colors = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)

    header(slide, data.get("title", "X01 架构图"))
    set_subtitle(ctx, slide, data.get("subtitle", "分层 > 分组 > 模块"))

    content = data.get("content", {})
    x, y, w, h = content_region(ctx, top_pad_in=0.22, bottom_pad_in=0.1)

    left_tag = (content.get("side_labels") or {}).get("left", "")
    right_tag = (content.get("side_labels") or {}).get("right", "")
    side_w = int(Inches(0.44))
    side_gap = int(Inches(0.08))

    main_x = x
    main_w = w
    if left_tag:
        shape_rect(slide, x, y, side_w, h, fill_color=colors["dark"], line_color=colors["line"])
        textbox(slide, x + int(Inches(0.02)), y + int(Inches(0.06)), side_w - int(Inches(0.04)), h - int(Inches(0.12)), left_tag, size="caption", bold=True, color=colors["white"], align=PP_ALIGN.CENTER)
        main_x += side_w + side_gap
        main_w -= side_w + side_gap

    if right_tag:
        rx = x + w - side_w
        shape_rect(slide, rx, y, side_w, h, fill_color=colors["dark"], line_color=colors["line"])
        textbox(slide, rx + int(Inches(0.02)), y + int(Inches(0.06)), side_w - int(Inches(0.04)), h - int(Inches(0.12)), right_tag, size="caption", bold=True, color=colors["white"], align=PP_ALIGN.CENTER)
        main_w -= side_w + side_gap

    layers = content.get("layers", [])
    if not layers:
        shape_rect(slide, main_x, y, main_w, h, fill_color=colors["light"], line_color=colors["line"])
        textbox(slide, main_x + int(Inches(0.12)), y + int(h * 0.45), main_w - int(Inches(0.24)), int(Inches(0.28)), "X01: 请提供 layers/groups/modules 数据", size="caption", color=colors["text"], align=PP_ALIGN.CENTER)
        return slide

    layer_gap = int(Inches(0.08))
    layer_h = int((h - layer_gap * max(0, len(layers) - 1)) / max(1, len(layers)))

    layer_map = {}

    for li, layer in enumerate(layers[:6]):
        ly = int(y + li * (layer_h + layer_gap))
        layer_id = str(layer.get("id", f"layer_{li + 1}"))
        layer_group_count = len(layer.get("groups", []))
        layer_module_count = sum(len(group.get("modules", [])) for group in layer.get("groups", []))
        left_title_mode = _use_left_title_mode(layer, 1, layer_group_count, layer_module_count)
        title_strip_w = int(Inches(0.34)) if left_title_mode else 0
        title_top_h = 0 if left_title_mode else int(Inches(0.22))
        layer_box_style = _style_by_depth(1, colors)
        group_box_style = _style_by_depth(2, colors)
        module_box_style = _style_by_depth(3, colors)
        storage_box_style = _style_by_depth(3, colors, storage=True)
        style = {
            "module_fill": module_box_style["fill"],
            "module_line": module_box_style["line"],
            "storage_fill": storage_box_style["fill"],
            "storage_line": storage_box_style["line"],
        }

        _rect_shape(slide, main_x, ly, main_w, layer_h, fill_color=layer_box_style["fill"], line_color=layer_box_style["line"], line_width=0.5)
        if left_title_mode:
            title_shape = _rect_shape(
                slide,
                main_x + int(Inches(0.03)),
                ly + int(Inches(0.04)),
                title_strip_w,
                layer_h - int(Inches(0.08)),
                fill_color=layer_box_style["fill"],
                line_color=layer_box_style["line"],
                line_width=0.5,
            )
            if layer_box_style["fill"] is not None:
                _center_text_in_shape(title_shape, _stack_text(layer.get("name", f"Layer {li + 1}")), colors["text"], size="micro", bold=True)
            else:
                textbox(
                    slide,
                    main_x + int(Inches(0.05)),
                    ly + int(Inches(0.08)),
                    title_strip_w - int(Inches(0.04)),
                    layer_h - int(Inches(0.16)),
                    _stack_text(layer.get("name", f"Layer {li + 1}")),
                    size="micro",
                    bold=True,
                    color=colors["text"],
                    align=PP_ALIGN.CENTER,
                )
        else:
            textbox(slide, main_x + int(Inches(0.08)), ly + int(Inches(0.05)), main_w - int(Inches(0.16)), int(Inches(0.2)), layer.get("name", f"Layer {li + 1}"), size="label", bold=True, color=colors["text"])
        layer_map[layer_id] = (main_x, ly, main_w, layer_h)

        groups = layer.get("groups", [])
        if not groups:
            continue

        gx = int(main_x + Inches(0.08) + title_strip_w)
        gy = int(ly + Inches(0.05) + title_top_h)
        gw = int(main_w - Inches(0.16) - title_strip_w)
        gh = int(layer_h - Inches(0.12) - title_top_h)
        group_gap = int(Inches(0.08))
        group_w = int((gw - group_gap * max(0, len(groups) - 1)) / max(1, len(groups)))

        for gi, group in enumerate(groups[:8]):
            xg = int(gx + gi * (group_w + group_gap))
            group_module_count = len(group.get("modules", [])[:8])
            group_left_title_mode = _use_left_title_mode(group, 2, 0, group_module_count)
            group_title_left_w = int(Inches(0.22)) if group_left_title_mode else 0
            group_title_top_h = 0 if group_left_title_mode else int(Inches(0.18))
            panel = _rect_shape(
                slide,
                xg,
                gy,
                group_w,
                gh,
                fill_color=group_box_style["fill"],
                line_color=group_box_style["line"],
                line_width=0.5,
                dashed=group.get("style") == "dashed",
            )

            if group_left_title_mode:
                textbox(
                    slide,
                    xg + int(Inches(0.02)),
                    gy + int(Inches(0.04)),
                    group_title_left_w - int(Inches(0.02)),
                    gh - int(Inches(0.08)),
                    _stack_text(group.get("name", f"Group {gi + 1}")),
                    size="micro",
                    bold=True,
                    color=colors["text"],
                    align=PP_ALIGN.CENTER,
                )
            else:
                textbox(slide, xg + int(Inches(0.04)), gy + int(Inches(0.03)), group_w - int(Inches(0.08)), int(Inches(0.16)), group.get("name", f"Group {gi + 1}"), size="micro", bold=True, color=colors["text"])

            mods = group.get("modules", [])[:8]
            if not mods:
                continue

            area_x = int(xg + Inches(0.04) + group_title_left_w)
            area_y = int(gy + Inches(0.04) + group_title_top_h)
            area_w = int(group_w - Inches(0.08) - group_title_left_w)
            area_h = int(gh - Inches(0.08) - group_title_top_h)
            if li == 2 and len(mods) >= 3:
                cols = min(3, len(mods))
                rows = (len(mods) + cols - 1) // cols
            else:
                cols, rows = _choose_grid(mods, area_w, area_h)
            cell_gap_x = int(Inches(0.05))
            cell_gap_y = int(Inches(0.05))
            cell_w = int((area_w - cell_gap_x * max(0, cols - 1)) / max(1, cols))
            cell_h = int((area_h - cell_gap_y * max(0, rows - 1)) / max(1, rows))

            for mi, mod in enumerate(mods):
                r = mi // cols
                c = mi % cols
                mx = int(area_x + c * (cell_w + cell_gap_x))
                my = int(area_y + r * (cell_h + cell_gap_y))
                name = mod.get("name", f"M{mi + 1}") if isinstance(mod, dict) else str(mod)
                mod_type = mod.get("type", "module") if isinstance(mod, dict) else "module"
                _add_module(slide, mx, my, cell_w, cell_h, name, colors, style, is_storage=(mod_type == "storage"))

    ext_zones = content.get("external_zones", [])
    if ext_zones:
        ez_h = int(Inches(0.54))
        ez_y = int(y + h - ez_h)
        zones = ext_zones[:2]
        z_gap = int(Inches(0.08))
        z_w = int((main_w - z_gap * max(0, len(zones) - 1)) / max(1, len(zones)))
        for zi, zone in enumerate(zones):
            zx = int(main_x + zi * (z_w + z_gap))
            zshape = _rect_shape(slide, zx, ez_y, z_w, ez_h, fill_color=None, line_color=colors["primary"], line_width=0.5, dashed=zone.get("style", "dashed") == "dashed")
            textbox(slide, zx + int(Inches(0.05)), ez_y + int(Inches(0.03)), z_w - int(Inches(0.1)), int(Inches(0.15)), zone.get("title", "外部区域"), size="micro", bold=True, color=colors["text"])
            items = zone.get("items", [])[:4]
            for ii, item in enumerate(items):
                textbox(slide, zx + int(Inches(0.06)), ez_y + int(Inches(0.2 + 0.08 * ii)), z_w - int(Inches(0.12)), int(Inches(0.08)), f"• {item}", size="micro", color=colors["gray"])

    for link in content.get("links", []):
        src = layer_map.get(str(link.get("from")))
        dst = layer_map.get(str(link.get("to")))
        if src is None or dst is None or str(link.get("from")) == str(link.get("to")):
            continue
        _draw_layer_relation_arrow(
            slide,
            src,
            dst,
            colors,
            direction=link.get("direction"),
            label=link.get("label", ""),
        )

    return slide
