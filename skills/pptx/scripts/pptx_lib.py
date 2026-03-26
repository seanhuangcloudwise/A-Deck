#!/usr/bin/env python3
"""pptx_lib — Shared drawing library for Cloudwise-branded PPTX generation.

Provides: color palette, canvas constants, drawing primitives, slide management,
diagram renderers (capability_map, flow, three_cols, wide_list, relationship),
and build/verify entry points.

Usage:
    from pptx_lib import *

    def my_slides(ctx):
        slide = ctx.add_content_slide()
        header(slide, "Title", subtitle="Sub", num=1)
        render_flow(slide, [{"title":"A","desc":"x"}, {"title":"B","desc":"y"}])

    build_pptx(TEMPLATE, OUTPUT, my_slides)
"""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path
from typing import Callable, Sequence

import yaml
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_VERTICAL_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 0. TEMPLATE SPECIFICATION LOADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_template_spec(spec_path: Path | str) -> dict:
    """Load template specification from YAML file.
    
    Args:
        spec_path: Path to cloudwise-spec.yaml (e.g., 'skills/pptx/master-library/light-cloudwise-cyan/cloudwise-spec.yaml')
    
    Returns:
        dict with keys: 'template', 'layout', 'safe_zone', 'infrastructure_colors', 'theme_colors', 'maturity_status'
    """
    spec_path = Path(spec_path)
    if not spec_path.exists():
        raise FileNotFoundError(f"Template spec not found: {spec_path}")
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)
    
    if not spec:
        raise ValueError(f"Template spec is empty: {spec_path}")
    
    return spec


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. THEME COLOR EXTRACTION  (dynamic — read from master template)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def _parse_scheme_color(elem) -> tuple[int, int, int]:
    """Extract RGB tuple from a scheme color element (<a:dk1>, etc.)."""
    srgb = elem.find("a:srgbClr", _NS)
    if srgb is not None:
        v = srgb.get("val", "000000")
        return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))
    sys_clr = elem.find("a:sysClr", _NS)
    if sys_clr is not None:
        v = sys_clr.get("lastClr", sys_clr.get("val", "000000"))
        return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))
    return (0, 0, 0)


def extract_theme_colors(prs) -> dict[str, tuple[int, int, int]]:
    """Extract color scheme from the first slide master's theme XML.

    Returns a dict with friendly role names mapped to RGB tuples:
        primary, secondary, accent3..accent6, dark, light,
        text, white, gray, header (alias for dark).
    """
    theme_el = None
    # Walk rels to find the theme part
    for rel in prs.slide_masters[0].part.rels.values():
        if "theme" in rel.reltype:
            theme_el = etree.fromstring(rel.target_part.blob)
            break
    if theme_el is None:
        raise RuntimeError("Cannot locate theme XML in template")

    scheme = theme_el.find(".//a:clrScheme", _NS)
    if scheme is None:
        raise RuntimeError("No <a:clrScheme> in theme XML")

    raw: dict[str, tuple[int, int, int]] = {}
    for tag in ("dk1", "dk2", "lt1", "lt2",
                "accent1", "accent2", "accent3", "accent4",
                "accent5", "accent6", "hlink", "folHlink"):
        el = scheme.find(f"a:{tag}", _NS)
        if el is not None:
            raw[tag] = _parse_scheme_color(el)

    dk2 = raw.get("dk2", (68, 84, 106))
    lt2 = raw.get("lt2", (231, 230, 230))

    colors = {
        "primary":   raw.get("accent1", (0, 204, 215)),
        "secondary": raw.get("accent2", (103, 224, 230)),
        "accent3":   raw.get("accent3", (35, 193, 224)),
        "accent4":   raw.get("accent4", (85, 206, 212)),
        "accent5":   raw.get("accent5", (91, 155, 213)),
        "accent6":   raw.get("accent6", (112, 173, 71)),
        "dark":      dk2,
        "header":    dk2,               # alias for readability
        "light":     lt2,
        "text":      raw.get("dk1", (0, 0, 0)),
        "white":     raw.get("lt1", (255, 255, 255)),
        # derived: midpoint of dk2 and lt2
        "gray":      tuple(int((a + b) / 2) for a, b in zip(dk2, lt2)),
    }
    return colors


def lighter(rgb: tuple[int, int, int], factor: float = 0.5) -> tuple[int, int, int]:
    """Lighten an RGB color toward white.  factor 0.0 = original, 1.0 = pure white."""
    return tuple(int(c + (255 - c) * factor) for c in rgb)


def darker(rgb: tuple[int, int, int], factor: float = 0.3) -> tuple[int, int, int]:
    """Darken an RGB color toward black.  factor 0.0 = original, 1.0 = pure black."""
    return tuple(int(c * (1 - factor)) for c in rgb)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. CLOUDWISE PALETTE  (legacy hard-coded — used only by pptx_lib internals)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

C = {
    "cyan":       RGBColor(0x00, 0xCC, 0xD7),
    "cyan_2":     RGBColor(0x67, 0xE0, 0xE6),
    "cyan_3":     RGBColor(0xD8, 0xF6, 0xF8),
    "dark":       RGBColor(0x22, 0x22, 0x22),
    "gray":       RGBColor(0x66, 0x66, 0x66),
    "mid_gray":   RGBColor(0x8A, 0x95, 0x99),
    "light":      RGBColor(0xF7, 0xF9, 0xFA),
    "line":       RGBColor(0xD9, 0xE4, 0xE8),
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "soft_green": RGBColor(0xE9, 0xF6, 0xEA),
    "soft_blue":  RGBColor(0xE9, 0xF7, 0xFB),
    "soft_yellow":RGBColor(0xFB, 0xF7, 0xE8),
    "domain_bg":  RGBColor(0x44, 0x54, 0x6A),
    "brand_gray": RGBColor(0xA5, 0xA7, 0xAA),
}

# Diagram-specific palettes
MATURITY = {
    "GA":      {"fill": C["cyan"],      "border": C["cyan"],      "text": C["white"],     "dash": False},
    "Managed": {"fill": RGBColor(0x53,0xE3,0xEB), "border": C["cyan"], "text": RGBColor(0x2F,0x2F,0x2F), "dash": False},
    "Beta":    {"fill": C["cyan_3"],    "border": C["cyan"],      "text": RGBColor(0x2F,0x2F,0x2F), "dash": False},
    "Alpha":   {"fill": C["brand_gray"],"border": C["brand_gray"],"text": C["white"],     "dash": False},
    "Planned": {"fill": C["white"],     "border": C["brand_gray"],"text": C["brand_gray"],"dash": True},
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. CANVAS CONSTANTS  (design baseline = 10" × 7.5")
#    Cloudwise master convention: content safe zone = top 10% to bottom 10%
#    i.e. 0.75" – 6.75" vertically (6.00" usable height)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE_HEIGHT_IN  = 7.5
SAFE_LEFT       = Inches(0.3)
SAFE_RIGHT      = Inches(9.68)
SAFE_WIDTH      = SAFE_RIGHT - SAFE_LEFT
SAFE_TOP        = Inches(BASE_HEIGHT_IN * 0.1)    # 0.75"
SAFE_BOTTOM     = Inches(BASE_HEIGHT_IN * 0.9)    # 6.75"
SAFE_HEIGHT     = SAFE_BOTTOM - SAFE_TOP           # 6.00"
HEADER_TOP      = Inches(0.12)
HEADER_HEIGHT   = Inches(0.58)
CONTENT_TOP     = SAFE_TOP + Inches(0.33)          # 1.08" (below title placeholder)
CONTENT_HEIGHT  = SAFE_BOTTOM - CONTENT_TOP        # ~5.67"
FLOW_Y          = Inches(2.1)
LIST_Y          = Inches(4.1)
BASE_WIDTH_IN   = 10.0

FONT_SIZE_TOKENS = {
    "display": 30,
    "title": 24,
    "h2": 20,
    "h3": 16,
    "subtitle": 10,
    "body": 12,
    "label": 10,
    "caption": 9,
    "micro": 8,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. LOW-LEVEL DRAWING PRIMITIVES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def set_rrect_adj(shape, adj=8000):
    """Set rounded-rect corner radius (default 8000 ≈ small modern corner)."""
    prstGeom = shape.element.spPr.find(qn("a:prstGeom"))
    if prstGeom is None:
        return
    avLst = prstGeom.find(qn("a:avLst"))
    if avLst is None:
        avLst = etree.SubElement(prstGeom, qn("a:avLst"))
    gd = avLst.find(qn("a:gd"))
    if gd is None:
        gd = etree.SubElement(avLst, qn("a:gd"))
    gd.set("name", "adj")
    gd.set("fmla", f"val {adj}")


def set_dash(shape):
    """Set shape border to dashed style."""
    ln = shape.element.spPr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(shape.element.spPr, qn("a:ln"))
    prstDash = ln.find(qn("a:prstDash"))
    if prstDash is None:
        prstDash = etree.SubElement(ln, qn("a:prstDash"))
    prstDash.set("val", "dash")


def rect(slide, x, y, w, h, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    return shape


def rrect(slide, x, y, w, h, fill, line=None, adj=8000):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    set_rrect_adj(shape, adj)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    return shape


def textbox(slide, x, y, w, h, text, size=16, bold=False,
            color=None, align=PP_ALIGN.LEFT, valign=MSO_VERTICAL_ANCHOR.TOP):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    resolved_size = FONT_SIZE_TOKENS.get(size, size) if isinstance(size, str) else size
    p.font.size = Pt(resolved_size)
    p.font.bold = bold
    # 正确处理颜色 - 转换tuple为RGBColor
    color_val = color or C["dark"]
    if isinstance(color_val, tuple):
        p.font.color.rgb = RGBColor(*color_val)
    else:
        p.font.color.rgb = color_val
    return box


def bullet_box(slide, x, y, w, h, lines, size=13):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for idx, line in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.LEFT
        p.font.size = Pt(size)
        p.font.color.rgb = C["dark"]
    return box


def add_text(shape, text, size, bold=False, color=None,
             align=PP_ALIGN.CENTER, valign=MSO_VERTICAL_ANCHOR.MIDDLE):
    """Write text into an existing shape with tight margins and single spacing."""
    color = color or RGBColor(0x2F, 0x2F, 0x2F)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    pPr = p._pPr
    if pPr is None:
        pPr = etree.SubElement(p._p, qn("a:pPr"))
    lnSpc = pPr.find(qn("a:lnSpc"))
    if lnSpc is None:
        lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
        etree.SubElement(lnSpc, qn("a:spcPct")).set("val", "100000")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. SLIDE MANAGEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def layout_by_names(prs, names, fallback_index=1):
    wanted = [n.lower() for n in names]
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(w in name for w in wanted):
            return layout
    return prs.slide_layouts[fallback_index]


def add_slide(prs, layout, keep_title=False):
    slide = prs.slides.add_slide(layout)
    for shape in list(slide.shapes):
        if getattr(shape, "is_placeholder", False):
            if keep_title and shape.placeholder_format.idx == 0:
                continue
            shape.element.getparent().remove(shape.element)
    return slide


def clear_slides(prs):
    for slide_id in list(prs.slides._sldIdLst):
        prs.part.drop_rel(slide_id.rId)
        prs.slides._sldIdLst.remove(slide_id)


def fit_slide_to_canvas(slide, scale_x):
    if abs(scale_x - 1.0) < 1e-6:
        return
    for shape in slide.shapes:
        # Preserve placeholder geometry from master/layout definitions.
        if getattr(shape, "is_placeholder", False):
            continue
        shape.left = int(shape.left * scale_x)
        shape.width = int(shape.width * scale_x)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. HEADER / FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def header(slide, title, subtitle=None, num=None):
    """Write header into slide. Uses the layout's title placeholder when present,
    inheriting its lstStyle (font, size, color from master). Falls back to manual
    shapes when no placeholder exists."""
    title_ph = next(
        (s for s in slide.shapes
         if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 0),
        None,
    )
    if title_ph is not None:
        tf = title_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = title
        # Do NOT override font properties — let the layout lstStyle apply
        # (内容1: 24pt bold accent1 微软雅黑, inherited from slideLayout2.xml)
    else:
        rrect(slide, SAFE_LEFT, HEADER_TOP, Inches(8.78), HEADER_HEIGHT, C["white"], line=C["line"])
        textbox(slide, Inches(0.52), Inches(0.2), Inches(8.42), Inches(0.32), title,
                size=26, bold=True, color=C["dark"])
    if subtitle:
        textbox(slide, Inches(0.52), Inches(0.54), Inches(8.42), Inches(0.18), subtitle,
                size=11, color=C["gray"])
    if num is not None:
        rrect(slide, Inches(9.02), Inches(0.16), Inches(0.56), Inches(0.44), C["soft_blue"], line=C["line"])
        textbox(slide, Inches(9.07), Inches(0.24), Inches(0.46), Inches(0.24), f"{num}",
                size=15, bold=True, color=C["cyan"], align=PP_ALIGN.CENTER)


def footer(slide):
    """Footer separator line at the bottom of the content safe zone."""
    rect(slide, SAFE_LEFT, SAFE_BOTTOM + Inches(0.01), SAFE_WIDTH, Inches(0.03), C["cyan_2"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. DIAGRAM RENDERERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def render_flow(slide, steps, y=2.45):
    """Horizontal flow: [{title, desc}, ...]. Arrows between steps."""
    left = SAFE_LEFT + Inches(0.02)
    total_w = SAFE_WIDTH - Inches(0.16)
    gap = Inches(0.14)
    box_w = (total_w - gap * (len(steps) - 1)) / len(steps)
    for idx, step in enumerate(steps):
        x = left + idx * (box_w + gap)
        fill = C["soft_blue"] if idx % 2 == 0 else C["light"]
        rrect(slide, x, Inches(y), box_w, Inches(1.15), fill, line=C["cyan"])
        textbox(slide, x + Inches(0.05), Inches(y) + Inches(0.12), box_w - Inches(0.1), Inches(0.28),
                step["title"], size=13, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)
        textbox(slide, x + Inches(0.08), Inches(y) + Inches(0.46), box_w - Inches(0.16), Inches(0.46),
                step["desc"], size=10, color=C["gray"], align=PP_ALIGN.CENTER)
        if idx < len(steps) - 1:
            textbox(slide, x + box_w + Inches(0.01), Inches(y) + Inches(0.37), Inches(0.13), Inches(0.2),
                    "▶", size=12, color=C["cyan"], align=PP_ALIGN.CENTER)


def render_wide_list(slide, items, colors, y_start=1.22, h=0.76, gap=0.12, size=17):
    """Stacked full-width rounded bars."""
    for idx, item in enumerate(items):
        y = Inches(y_start) + idx * (Inches(h) + Inches(gap))
        rrect(slide, SAFE_LEFT + Inches(0.02), y, SAFE_WIDTH - Inches(0.1), Inches(h),
              colors[idx % len(colors)], line=C["line"])
        textbox(slide, SAFE_LEFT + Inches(0.16), y + Inches(0.11), SAFE_WIDTH - Inches(0.26), Inches(h - 0.18),
                item, size=size, color=C["dark"])


def render_three_cols(slide, columns):
    """Three equal columns with header bar + bullet list."""
    left = SAFE_LEFT + Inches(0.02)
    top = Inches(1.26)
    gap_x = Inches(0.16)
    width = SAFE_WIDTH - Inches(0.14)
    col_w = (width - gap_x * 2) / 3
    body_h = Inches(5.74)
    bar_colors = [C["cyan"], C["cyan_2"], C["gray"]]
    fills = [C["soft_blue"], C["light"], C["soft_yellow"]]
    for idx, column in enumerate(columns):
        x = left + idx * (col_w + gap_x)
        rrect(slide, x, top, col_w, body_h, fills[idx % len(fills)], line=C["line"])
        rect(slide, x, top, col_w, Inches(0.5), bar_colors[idx % len(bar_colors)])
        textbox(slide, x + Inches(0.08), top + Inches(0.07), col_w - Inches(0.16), Inches(0.28),
                column["title"], size=14, bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        bullet_box(slide, x + Inches(0.12), top + Inches(0.68), col_w - Inches(0.24), Inches(4.78),
                   column["items"], size=12)


def render_relationship(slide, root_text, children):
    """Root box → vertical → horizontal → 3 child columns with headers + bullets."""
    rrect(slide, Inches(2.56), Inches(1.42), Inches(4.86), Inches(0.82), C["soft_blue"], line=C["cyan"])
    textbox(slide, Inches(2.8), Inches(1.65), Inches(4.36), Inches(0.28), root_text,
            size=18, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)
    rect(slide, Inches(4.98), Inches(2.17), Inches(0.04), Inches(0.45), C["cyan"])
    rect(slide, Inches(0.72), Inches(2.58), Inches(8.58), Inches(0.04), C["cyan_2"])
    xs = [0.2, 3.34, 6.48]
    fills = [C["soft_blue"], C["soft_yellow"], C["light"]]
    for idx, child in enumerate(children):
        x = Inches(xs[idx])
        rect(slide, x + Inches(1.46), Inches(2.58), Inches(0.04), Inches(0.22), C["cyan_2"])
        rrect(slide, x, Inches(2.8), Inches(2.86), Inches(3.08), fills[idx], line=C["line"])
        rect(slide, x, Inches(2.8), Inches(3.08), Inches(0.44), C["cyan"])
        textbox(slide, x + Inches(0.58), Inches(2.94), Inches(2.16), Inches(0.4), child["title"],
                size=14, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)
        bullet_box(slide, x + Inches(0.3), Inches(3.42), Inches(2.3), Inches(2.2), child["items"], size=12)


def render_capability_map(slide, domains, *,
                          grid_top=Inches(1.15), grid_bottom=Inches(6.72),
                          domain_w=Inches(1.42), cell_gap=Inches(0.06),
                          row_gap=Inches(0.07), legend_y=Inches(6.88)):
    """BA-01 Variant B: domain rows × capability cells with maturity colors + legend."""
    grid_height = grid_bottom - grid_top
    grid_left = SAFE_LEFT + domain_w + cell_gap
    grid_width = SAFE_RIGHT - grid_left
    n_rows = len(domains)
    total_row_gaps = row_gap * (n_rows - 1)
    row_h = int((grid_height - total_row_gaps) / n_rows)

    for row_idx, domain in enumerate(domains):
        y = grid_top + row_idx * (row_h + row_gap)
        dom_shape = rrect(slide, SAFE_LEFT, y, domain_w, row_h, C["domain_bg"], adj=4000)
        dom_shape.line.fill.background()
        add_text(dom_shape, domain["name"], size=11, bold=True, color=C["white"])

        caps = domain["caps"]
        n_caps = len(caps)
        total_cell_gaps = cell_gap * (n_caps - 1)
        cell_w = int((grid_width - total_cell_gaps) / n_caps)

        for col_idx, (cap_name, maturity) in enumerate(caps):
            x = grid_left + col_idx * (cell_w + cell_gap)
            m = MATURITY[maturity]
            cell = rrect(slide, x, y, cell_w, row_h, m["fill"], line=m["border"], adj=4000)
            cell.line.width = Pt(1.2)
            if m["dash"]:
                set_dash(cell)
            add_text(cell, cap_name, size=9, color=m["text"])
            # Maturity badge
            badge_w, badge_h = Inches(0.42), Inches(0.18)
            badge = slide.shapes.add_textbox(
                x + cell_w - badge_w - Inches(0.04),
                y + row_h - badge_h - Inches(0.03),
                badge_w, badge_h)
            btf = badge.text_frame
            btf.clear()
            btf.margin_left = btf.margin_right = btf.margin_top = btf.margin_bottom = 0
            bp = btf.paragraphs[0]
            bp.text = maturity
            bp.alignment = PP_ALIGN.RIGHT
            bp.font.size = Pt(7)
            bp.font.color.rgb = m["text"]

    # Legend
    legend_items = [
        ("GA (受管理)", C["cyan"], C["white"]),
        ("Managed (可管理)", MATURITY["Managed"]["fill"], C["dark"]),
        ("Beta (发展中)", C["cyan_3"], C["dark"]),
        ("Alpha (初级)", C["brand_gray"], C["white"]),
        ("Planned (计划中)", C["white"], C["brand_gray"]),
    ]
    legend_box_w, legend_label_w = Inches(0.22), Inches(1.2)
    legend_item_w = legend_box_w + Inches(0.06) + legend_label_w
    legend_start_x = SAFE_LEFT + (SAFE_WIDTH - legend_item_w * len(legend_items)) / 2
    for li, (label, fill, _txt_c) in enumerate(legend_items):
        lx = int(legend_start_x + li * legend_item_w)
        sw = rrect(slide, lx, legend_y, legend_box_w, Inches(0.18), fill, line=C["brand_gray"], adj=3000)
        sw.line.width = Pt(0.5)
        if fill == C["white"]:
            set_dash(sw)
        lbl = slide.shapes.add_textbox(lx + legend_box_w + Inches(0.04), legend_y - Inches(0.01),
                                       legend_label_w, Inches(0.2))
        ltf = lbl.text_frame
        ltf.clear()
        ltf.margin_left = ltf.margin_top = ltf.margin_bottom = 0
        lp = ltf.paragraphs[0]
        lp.text = label
        lp.font.size = Pt(8)
        lp.font.color.rgb = RGBColor(0x2F, 0x2F, 0x2F)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. BUILD CONTEXT & ENTRY POINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BuildContext:
    """Convenience wrapper passed to build functions.
    
    Args:
        prs: Presentation object from opening template PPTX
        scale_x: Horizontal scale factor (typically 1.0 or computed from slide width)
        template_spec: dict loaded from template-spec.yaml via load_template_spec()
                      Contains: layout names, safe zones, infrastructure colors, etc.
                      If None, falls back to Cloudwise defaults (legacy compat)
    """

    def __init__(self, prs: Presentation, scale_x: float, template_spec: dict | None = None):
        self.prs = prs
        self.scale_x = scale_x
        self.template_spec = template_spec or self._default_cloudwise_spec()
        
        # Extract layout names from template_spec
        spec_layout = self.template_spec.get('layout', {})
        cover_names = spec_layout.get('names', {}).get('cover', ['封面'])
        thanks_names = spec_layout.get('names', {}).get('thanks', ['感谢页'])
        content_names = spec_layout.get('names', {}).get('content', ['內容页', '内容页'])
        
        cover_idx = spec_layout.get('indices', {}).get('cover', 0)
        thanks_idx = spec_layout.get('indices', {}).get('thanks', 7)
        content_idx = spec_layout.get('indices', {}).get('content', 1)
        
        self._cover_layout = layout_by_names(prs, cover_names, cover_idx)
        self._thanks_layout = layout_by_names(prs, thanks_names, thanks_idx)
        self._content_layout = layout_by_names(prs, content_names, content_idx)
        self._colors = None
        self._palette = None

    @staticmethod
    def _default_cloudwise_spec() -> dict:
        """Fallback Cloudwise spec for backward compatibility (when template_spec not passed)."""
        return {
            'layout': {
                'names': {
                    'cover': ['封面'],
                    'content': ['內容页', '内容页'],
                    'thanks': ['感谢页'],
                },
                'indices': {
                    'cover': 0,
                    'content': 1,
                    'thanks': 7,
                }
            },
            'safe_zone': {
                'left_in': 0.3,
                'right_in': 9.68,
                'top_in': 0.75,
                'bottom_in': 6.75,
                'header_top_in': 0.12,
                'header_height_in': 0.58,
                'content_top_in': 1.08,
            },
            'typography': {
                'font_scale': 1.0,
                'min_font_size': 8.0,
                'tokens': {
                    'display': 28,
                    'title': 24,
                    'h2': 20,
                    'h3': 16,
                    'subtitle': 14,
                    'body': 12,
                    'label': 10,
                    'caption': 9,
                    'micro': 8,
                },
            },
        }

    @property
    def colors(self) -> dict[str, tuple[int, int, int]]:
        """Theme colors extracted from the master template merged with template infrastructure palette."""
        if self._colors is None:
            merged = extract_theme_colors(self.prs)
            infra = self.template_spec.get("infrastructure_colors", {}).get("palette", {})
            for key, value in infra.items():
                if isinstance(value, (list, tuple)) and len(value) == 3:
                    merged[key] = (int(value[0]), int(value[1]), int(value[2]))
            self._colors = merged
        return self._colors

    @property
    def palette(self) -> list[tuple[int, int, int]]:
        """7-color palette derived from theme: [dark, primary, secondary, accent3-6]."""
        if self._palette is None:
            c = self.colors
            self._palette = [
                c["dark"], c["primary"], c["secondary"],
                c["accent3"], c["accent4"], c["accent5"], c["accent6"],
            ]
        return self._palette

    @property
    def typography(self) -> dict[str, float]:
        """Typography tokens from template spec with safe defaults."""
        defaults = {
            "display": 28,
            "title": 24,
            "h2": 20,
            "h3": 16,
            "subtitle": 14,
            "body": 12,
            "label": 10,
            "caption": 9,
            "micro": 8,
        }
        tokens = self.template_spec.get("typography", {}).get("tokens", {})
        merged = defaults.copy()
        for key, value in tokens.items():
            try:
                merged[key] = float(value)
            except (TypeError, ValueError):
                pass
        return merged

    def add_cover_slide(self):
        return add_slide(self.prs, self._cover_layout)

    def add_content_slide(self):
        return add_slide(self.prs, self._content_layout, keep_title=True)

    def add_thanks_slide(self):
        return add_slide(self.prs, self._thanks_layout)

    # Safe zone properties (from template_spec)
    @property
    def safe_left(self) -> int:
        """Safe zone left edge (EMU)."""
        return Inches(self.template_spec['safe_zone']['left_in'])
    
    @property
    def safe_right(self) -> int:
        """Safe zone right edge (EMU)."""
        return Inches(self.template_spec['safe_zone']['right_in'])
    
    @property
    def safe_top(self) -> int:
        """Safe zone top edge (EMU)."""
        return Inches(self.template_spec['safe_zone']['top_in'])
    
    @property
    def safe_bottom(self) -> int:
        """Safe zone bottom edge (EMU)."""
        return Inches(self.template_spec['safe_zone']['bottom_in'])
    
    @property
    def safe_width(self) -> int:
        """Safe zone width (EMU)."""
        return self.safe_right - self.safe_left
    
    @property
    def safe_height(self) -> int:
        """Safe zone height (EMU)."""
        return self.safe_bottom - self.safe_top
    
    @property
    def header_top(self) -> int:
        """Header top edge (EMU)."""
        return Inches(self.template_spec['safe_zone']['header_top_in'])
    
    @property
    def header_height(self) -> int:
        """Header height (EMU)."""
        return Inches(self.template_spec['safe_zone']['header_height_in'])
    
    @property
    def content_top(self) -> int:
        """Content top edge (EMU, below title)."""
        return Inches(self.template_spec['safe_zone']['content_top_in'])
    
    @property
    def content_height(self) -> int:
        """Content area height (EMU)."""
        return self.safe_bottom - self.content_top

    def add_custom_slide(self, layout_names, fallback=1, keep_title=False):
        layout = layout_by_names(self.prs, layout_names, fallback)
        return add_slide(self.prs, layout, keep_title=keep_title)

    def finalize(self):
        """Apply scale_x to all slides."""
        for slide in self.prs.slides:
            fit_slide_to_canvas(slide, self.scale_x)


def build_pptx(template: Path | str, output: Path | str,
               build_fn: Callable[[BuildContext], None],
               template_spec_path: Path | str | None = None) -> Path:
    """Standard entry point for PPTX generation.

    Args:
        template: Path to the master template PPTX.
        output:   Path for the output PPTX.
        build_fn: Callable(ctx: BuildContext) that adds slides.
        template_spec_path: Path to template-spec.yaml (optional; if None, uses default Cloudwise spec).

    Returns:
        Path to the generated file.
    """
    template = Path(template)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    prs = Presentation(str(template))
    
    # Load template spec
    if template_spec_path:
        template_spec = load_template_spec(template_spec_path)
    else:
        template_spec = None  # Will use default Cloudwise spec in BuildContext  
    
    scale_x = prs.slide_width / Inches(BASE_WIDTH_IN)
    clear_slides(prs)

    ctx = BuildContext(prs, scale_x, template_spec)
    build_fn(ctx)
    ctx.finalize()

    prs.save(str(output))
    return output


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. INLINE VERIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def verify_pptx(output: Path | str, src_template: Path | str | None = None) -> dict:
    """Run inline QA on a generated PPTX. Prints summary and returns metrics dict."""
    output = Path(output)
    prs = Presentation(str(output))
    z = zipfile.ZipFile(str(output))

    slides_count = len(prs.slides)
    total_shapes = sum(len(s.shapes) for s in prs.slides)
    title_text = ""
    for s in prs.slides:
        for sh in s.shapes:
            if getattr(sh, "is_placeholder", False) and sh.placeholder_format.idx == 0:
                title_text = sh.text_frame.paragraphs[0].text if sh.has_text_frame else ""
                break
        if title_text:
            break

    theme_match = None
    if src_template:
        src_z = zipfile.ZipFile(str(src_template))
        src_hash = hashlib.sha256(src_z.read("ppt/theme/theme1.xml")).hexdigest()
        gen_hash = hashlib.sha256(z.read("ppt/theme/theme1.xml")).hexdigest()
        theme_match = src_hash == gen_hash

    result = {
        "slides": slides_count,
        "total_shapes": total_shapes,
        "first_title": title_text,
        "theme_match": theme_match,
    }

    print(f"=== PPTX QA: {output.name} ===")
    print(f"  Slides:       {slides_count}")
    print(f"  Total shapes: {total_shapes}")
    print(f"  First title:  {title_text}")
    if theme_match is not None:
        print(f"  Theme match:  {theme_match}")
    return result
