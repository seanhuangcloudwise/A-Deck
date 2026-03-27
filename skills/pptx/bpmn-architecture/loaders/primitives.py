"""
BPMN 2.0 Drawing Primitives — local to bpmn-architecture skill.

All BPMN shape/connector rendering functions live here.
NO imports from skills/pptx/shared, togaf, gtm, or roadmap.
Only python-pptx and stdlib are used.
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import math

_DML_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
_EMU_PER_INCH = 914400
_BASE_W_IN = 10.0
_BASE_H_IN = 5.625
_FLOW_CONNECTOR_TYPE = MSO_CONNECTOR_TYPE.CURVE


# ---------------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------------

def emu(inches: float) -> int:
    """Convert fractional inches to integer EMU (avoid float XML pollution)."""
    return int(Inches(inches))


def slide_size_in(prs):
    """Return slide size in inches as (width, height)."""
    return prs.slide_width / _EMU_PER_INCH, prs.slide_height / _EMU_PER_INCH


def slide_scale(prs, base_w=_BASE_W_IN, base_h=_BASE_H_IN):
    """Return input-space scale for current slide size.

    Cloudwise masters apply an observed horizontal render stretch, so BPMN loader
    input coordinates should keep base-canvas X sizing and only adapt in Y.
    Returns:
        sx: input X scale (kept at 1.0 to compensate master stretch)
        sy: input Y scale based on slide height
        su: uniform input size scale for shape widths/heights (kept at 1.0)
    """
    w_in, h_in = slide_size_in(prs)
    sx = 1.0
    sy = h_in / base_h if base_h else 1.0
    return sx, sy, 1.0


def scaled_region(prs, left, top, width, height, base_w=_BASE_W_IN, base_h=_BASE_H_IN):
    """Scale a base-canvas region to current slide inches."""
    sx, sy, _ = slide_scale(prs, base_w=base_w, base_h=base_h)
    return {
        "left": left * sx,
        "top": top * sy,
        "width": width * sx,
        "height": height * sy,
    }


def mid_x(left: int, width: int) -> int:
    return left + width // 2


def mid_y(top: int, height: int) -> int:
    return top + height // 2


def auto_text_color(fill_rgb, dark, white):
    """Return dark or white text color depending on fill relative luminance.

    Ensures readable contrast: white text on dark fills, dark text on light fills.
    Threshold luminance 0.4 keeps WCAG AA at typical font sizes.
    """
    if fill_rgb is None:
        return dark
    r, g, b = fill_rgb
    lum = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 255
    return white if lum < 0.4 else dark


def fit_x_scale(x_in_values, left_in, node_w_in=0.0,
                slide_w_in=10.0, right_margin_in=0.3):
    """Return a scale factor (≤1.0) so nodes fit within the slide width.

    Ensures: left_in + max(x_in)*scale + node_w_in ≤ slide_w_in − right_margin_in
    """
    if not x_in_values:
        return 1.0
    max_x = max(x_in_values)
    if max_x <= 0:
        return 1.0
    avail = slide_w_in - right_margin_in - left_in - node_w_in
    return min(1.0, avail / max_x)


def _best_cxn_pair(src_box, dst_box):
    """Choose the connection-point index pair that minimises distance.

    Each box is (cx, cy, w, h).  Indices: 0=top  1=left  2=bottom  3=right.
    Returns (src_idx, dst_idx).
    """
    def _anchors(box):
        cx, cy, w, h = box
        return [
            (cx, cy - h // 2),   # 0 = top
            (cx - w // 2, cy),   # 1 = left
            (cx, cy + h // 2),   # 2 = bottom
            (cx + w // 2, cy),   # 3 = right
        ]

    sa = _anchors(src_box)
    da = _anchors(dst_box)
    best_dist = float('inf')
    best = (1, 3)
    for si in range(4):
        for di in range(4):
            dx = sa[si][0] - da[di][0]
            dy = sa[si][1] - da[di][1]
            d = dx * dx + dy * dy
            if d < best_dist:
                best_dist = d
                best = (si, di)
    return best


def edge_endpoints(src_box, dst_box):
    """Compute connector start/end coordinates at nearest bounding-box edges.

    Each box is (cx, cy, w, h).  Returns (x1, y1, x2, y2).
    """
    anchors_map = {
        0: lambda b: (b[0], b[1] - b[3] // 2),   # top
        1: lambda b: (b[0] - b[2] // 2, b[1]),    # left
        2: lambda b: (b[0], b[1] + b[3] // 2),    # bottom
        3: lambda b: (b[0] + b[2] // 2, b[1]),    # right
    }
    si, di = _best_cxn_pair(src_box, dst_box)
    sx, sy = anchors_map[si](src_box)
    dx, dy = anchors_map[di](dst_box)
    return sx, sy, dx, dy


def connect_seq(slide, node_boxes, src_id, dst_id, colors, label=""):
    """Draw a sequence flow between two nodes stored in node_boxes.

    node_boxes[id] = (cx, cy, w, h, shape).
    Automatically picks nearest anchor points and elbow-routes.
    """
    src = node_boxes.get(src_id)
    dst = node_boxes.get(dst_id)
    if not src or not dst:
        return None
    sb = src[:4]
    db = dst[:4]
    x1, y1, x2, y2 = edge_endpoints(sb, db)
    return add_sequence_flow(slide, x1, y1, x2, y2, colors,
                             label=label,
                             begin_shape=src[4], end_shape=dst[4],
                             src_box=sb, dst_box=db)


def connect_msg(slide, node_boxes, src_id, dst_id, colors, label=""):
    """Draw a message flow between two nodes stored in node_boxes."""
    src = node_boxes.get(src_id)
    dst = node_boxes.get(dst_id)
    if not src or not dst:
        return None
    sb = src[:4]
    db = dst[:4]
    x1, y1, x2, y2 = edge_endpoints(sb, db)
    return add_message_flow(slide, x1, y1, x2, y2, colors,
                            label=label,
                            begin_shape=src[4], end_shape=dst[4],
                            src_box=sb, dst_box=db)


# ---------------------------------------------------------------------------
# Low-level shape factories
# ---------------------------------------------------------------------------

def add_rounded_rect(slide, left, top, width, height, fill_rgb=None, line_rgb=None,
                     line_width=Pt(1), corner_radius=Pt(4), text="", font_size=Pt(8),
                     font_color=None, bold=False, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    """Add a rounded rectangle with optional text."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.rotation = 0.0
    # Corner radius
    if hasattr(shape, 'adjustments') and len(shape.adjustments) > 0:
        # Adjustment value 0..1 range; keep small
        max_dim = min(width, height)
        if max_dim > 0:
            ratio = int(corner_radius) / max_dim
            shape.adjustments[0] = min(ratio, 0.15)
    # Fill
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _to_rgb(fill_rgb)
    else:
        shape.fill.background()
    # Line
    if line_rgb:
        shape.line.color.rgb = _to_rgb(line_rgb)
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    # Text
    if text:
        _set_text(shape, text, font_size, font_color, bold, alignment, anchor)
    return shape


def add_circle(slide, cx, cy, diameter, fill_rgb=None, line_rgb=None,
               line_width=Pt(1.5), text="", font_size=Pt(7)):
    """Add a circle centered at (cx, cy)."""
    r = diameter // 2
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, diameter, diameter)
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _to_rgb(fill_rgb)
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = _to_rgb(line_rgb)
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    if text:
        _set_text(shape, text, font_size, None, False, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    return shape


def add_diamond(slide, cx, cy, size, fill_rgb=None, line_rgb=None,
                line_width=Pt(1.25), marker_text="", font_size=Pt(10), font_color=None):
    """Add a diamond (gateway) centered at (cx, cy)."""
    half = size // 2
    shape = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, cx - half, cy - half, size, size)
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _to_rgb(fill_rgb)
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = _to_rgb(line_rgb)
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    if marker_text:
        _set_text(shape, marker_text, font_size, font_color or line_rgb, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    return shape


def add_hexagon(slide, left, top, width, height, fill_rgb=None, line_rgb=None,
                line_width=Pt(1), text="", font_size=Pt(7)):
    """Add a hexagon (Conversation node)."""
    shape = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, left, top, width, height)
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _to_rgb(fill_rgb)
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = _to_rgb(line_rgb)
        shape.line.width = line_width
    if text:
        _set_text(shape, text, font_size, None, False, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    return shape


# ---------------------------------------------------------------------------
# BPMN semantic shape factories
# ---------------------------------------------------------------------------

def add_start_event(slide, cx, cy, colors, diameter=None):
    """BPMN Start Event — thin circle, primary color."""
    d = diameter or emu(0.24)
    return add_circle(slide, cx, cy, d,
                      fill_rgb=None,
                      line_rgb=colors["primary"],
                      line_width=Pt(1.5))


def add_end_event(slide, cx, cy, colors, diameter=None):
    """BPMN End Event — thick circle, dark color."""
    d = diameter or emu(0.24)
    return add_circle(slide, cx, cy, d,
                      fill_rgb=None,
                      line_rgb=colors.get("stroke", colors["dark"]),
                      line_width=Pt(3))


def add_intermediate_event(slide, cx, cy, colors, diameter=None, marker=""):
    """BPMN Intermediate Event — double circle."""
    d = diameter or emu(0.24)
    outer = add_circle(slide, cx, cy, d,
                       fill_rgb=None,
                   line_rgb=colors.get("stroke", colors["dark"]),
                       line_width=Pt(1.5))
    inner_d = int(d * 0.75)
    add_circle(slide, cx, cy, inner_d,
               fill_rgb=None,
               line_rgb=colors.get("stroke", colors["dark"]),
               line_width=Pt(1),
               text=marker,
               font_size=Pt(7))
    return outer


def add_task(slide, left, top, width, height, colors, label="", task_type="task"):
    """BPMN Task — rounded rectangle with optional task type icon text."""
    fill = colors["white"]
    border = colors.get("stroke", colors["dark"])
    text_color = colors.get("ink", colors["text"])
    shape = add_rounded_rect(slide, left, top, width, height,
                             fill_rgb=fill, line_rgb=border,
                             line_width=Pt(1), corner_radius=Pt(4),
                             text=label, font_size=Pt(8),
                             font_color=text_color)
    return shape


def add_gateway(slide, cx, cy, colors, gateway_type="exclusive", size=None):
    """BPMN Gateway — diamond with type marker.

    gateway_type: exclusive | parallel | inclusive | event_based | complex
    """
    s = size or emu(0.32)
    markers = {
        "exclusive": "X",
        "parallel": "+",
        "inclusive": "O",
        "event_based": "⬠",
        "complex": "*",
    }
    marker = markers.get(gateway_type, "")
    fill = colors["white"]
    border = colors.get("stroke", colors["dark"])
    return add_diamond(slide, cx, cy, s, fill_rgb=fill, line_rgb=border,
                       line_width=Pt(1.25), marker_text=marker, font_size=Pt(9),
                       font_color=colors.get("ink", colors.get("text", border)))


def add_pool_header(slide, left, top, width, height, colors, name="", orientation="horizontal"):
    """Pool header strip."""
    fill = colors["primary"]
    shape = add_rounded_rect(slide, left, top, width, height,
                             fill_rgb=fill, line_rgb=colors.get("stroke", colors["dark"]),
                             line_width=Pt(1), corner_radius=Pt(0),
                             text=name, font_size=Pt(11),
                             font_color=colors["white"], bold=True)
    if orientation == "vertical":
        shape.rotation = 270.0
    return shape


def add_lane_header(slide, left, top, width, height, colors, name="", level=0):
    """Lane header strip (nested lanes use level > 0 for indentation)."""
    if colors.get("mode") == "dark":
        if level == 0:
            fill = _mix(colors["secondary"], colors["light"], 0.55)
        else:
            fill = _mix(colors["primary"], colors["light"], 0.82)
    else:
        if level == 0:
            fill = colors["secondary"]
        else:
            fill = colors["light"]
    text_color = auto_text_color(fill, colors.get("ink", colors["dark"]), colors["white"])
    shape = add_rounded_rect(slide, left, top, width, height,
                             fill_rgb=fill, line_rgb=colors.get("stroke", colors["dark"]),
                             line_width=Pt(0.75), corner_radius=Pt(0),
                             text=name, font_size=Pt(9),
                             font_color=text_color, bold=(level == 0))
    return shape


# ---------------------------------------------------------------------------
# Connector factories
# ---------------------------------------------------------------------------

def _set_arrow_end(connector):
    """Attach an open arrowhead at the tail (destination) of a connector via XML."""
    from lxml import etree
    ln = connector.line._ln
    # Remove any pre-existing arrow elements to avoid duplicates
    for tag in (f'{{{_DML_NS}}}tailEnd', f'{{{_DML_NS}}}headEnd'):
        for el in ln.findall(tag):
            ln.remove(el)
    tail = etree.SubElement(ln, f'{{{_DML_NS}}}tailEnd')
    tail.set('type', 'arrow')
    tail.set('w', 'sm')
    tail.set('len', 'med')


def add_sequence_flow(slide, x1, y1, x2, y2, colors, label="",
                      begin_shape=None, end_shape=None,
                      src_box=None, dst_box=None):
    """Solid arrow — BPMN Sequence Flow (curved connector with arrowhead)."""
    connector = slide.shapes.add_connector(
        _FLOW_CONNECTOR_TYPE, x1, y1, x2, y2)
    connector.line.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    connector.line.width = Pt(1)
    if begin_shape is not None and end_shape is not None and src_box and dst_box:
        bi, ei = _best_cxn_pair(src_box, dst_box)
        try:
            connector.begin_connect(begin_shape, bi)
            connector.end_connect(end_shape, ei)
        except Exception:
            pass
    _set_arrow_end(connector)
    if label:
        _add_label_near_line(slide, x1, y1, x2, y2, label, colors, Pt(7))
    return connector


def add_message_flow(slide, x1, y1, x2, y2, colors, label="",
                     begin_shape=None, end_shape=None,
                     src_box=None, dst_box=None):
    """Dashed arrow with open arrowhead — BPMN Message Flow."""
    connector = slide.shapes.add_connector(
    _FLOW_CONNECTOR_TYPE, x1, y1, x2, y2)
    line_color = colors["secondary"]
    connector.line.color.rgb = _to_rgb(line_color)
    connector.line.width = Pt(1.5)
    connector.line.dash_style = 4  # dash
    if begin_shape is not None and end_shape is not None and src_box and dst_box:
        bi, ei = _best_cxn_pair(src_box, dst_box)
        try:
            connector.begin_connect(begin_shape, bi)
            connector.end_connect(end_shape, ei)
        except Exception:
            pass
    _set_arrow_end(connector)
    if label:
        _add_label_near_line(slide, x1, y1, x2, y2, label, colors, Pt(7), italic=True)
    return connector


def add_association(slide, x1, y1, x2, y2, colors,
                    begin_shape=None, end_shape=None,
                    src_box=None, dst_box=None):
    """Dotted line — BPMN Association (no arrowhead)."""
    connector = slide.shapes.add_connector(
    _FLOW_CONNECTOR_TYPE, x1, y1, x2, y2)
    connector.line.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    connector.line.width = Pt(1)
    connector.line.dash_style = 2  # dot
    if begin_shape is not None and end_shape is not None and src_box and dst_box:
        bi, ei = _best_cxn_pair(src_box, dst_box)
        try:
            connector.begin_connect(begin_shape, bi)
            connector.end_connect(end_shape, ei)
        except Exception:
            pass
    return connector


def add_conversation_link(slide, x1, y1, x2, y2, colors,
                          begin_shape=None, end_shape=None,
                          src_box=None, dst_box=None):
    """Solid line without arrowhead — BPMN Conversation Link."""
    connector = slide.shapes.add_connector(
    _FLOW_CONNECTOR_TYPE, x1, y1, x2, y2)
    connector.line.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    connector.line.width = Pt(1)
    if begin_shape is not None and end_shape is not None and src_box and dst_box:
        bi, ei = _best_cxn_pair(src_box, dst_box)
        try:
            connector.begin_connect(begin_shape, bi)
            connector.end_connect(end_shape, ei)
        except Exception:
            pass
    return connector


# ---------------------------------------------------------------------------
# Text annotation
# ---------------------------------------------------------------------------

def add_annotation(slide, left, top, width, height, text, colors, font_size=Pt(7)):
    """BPMN Text Annotation — bracket + text box."""
    from pptx.util import Pt as _Pt
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    # Left bracket line
    bracket_w = emu(0.05)
    bracket = slide.shapes.add_connector(
        MSO_CONNECTOR_TYPE.STRAIGHT, left - bracket_w, top, left - bracket_w, top + height)
    bracket.line.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    bracket.line.width = _Pt(1)
    return tb


# ---------------------------------------------------------------------------
# Subtitle / title helpers
# ---------------------------------------------------------------------------

def set_title_subtitle(slide, title, subtitle=""):
    """Set title (idx=0) and subtitle (idx=1) via placeholders. Placeholder-first rule."""
    for shape in slide.shapes:
        if not getattr(shape, "is_placeholder", False):
            continue
        idx = shape.placeholder_format.idx
        if idx == 0 and shape.has_text_frame and title:
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = title
        elif idx == 1 and shape.has_text_frame and subtitle:
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = subtitle


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _to_rgb(color):
    """Convert (R,G,B) tuple or RGBColor to RGBColor."""
    if isinstance(color, RGBColor):
        return color
    if isinstance(color, (list, tuple)) and len(color) == 3:
        return RGBColor(*color)
    return color


def _mix(rgb_a, rgb_b, factor):
    return tuple(int(a + (b - a) * factor) for a, b in zip(rgb_a, rgb_b))


def _set_text(shape, text, font_size, font_color, bold, alignment, anchor):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf.paragraphs[0].alignment = alignment
    except Exception:
        pass
    try:
        shape.text_frame.auto_size = None
        shape.text_frame.word_wrap = True
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = font_size
    if font_color:
        p.font.color.rgb = _to_rgb(font_color)
    p.font.bold = bold
    p.alignment = alignment
    try:
        tf.paragraphs[0].space_before = Pt(0)
        tf.paragraphs[0].space_after = Pt(0)
    except Exception:
        pass


def _add_label_near_line(slide, x1, y1, x2, y2, text, colors, font_size, italic=False):
    """Add a small text label near the midpoint of a line."""
    mx = (x1 + x2) // 2
    my = (y1 + y2) // 2
    w = emu(0.8)
    h = emu(0.2)
    tb = slide.shapes.add_textbox(mx - w // 2, my - h, w, h)
    p = tb.text_frame.paragraphs[0]
    p.text = text
    p.font.size = font_size
    p.font.color.rgb = _to_rgb(colors.get("stroke", colors["dark"]))
    p.font.italic = italic
    p.alignment = PP_ALIGN.CENTER
    return tb
