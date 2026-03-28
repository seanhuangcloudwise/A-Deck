"""Common rendering helpers for TOGAF loaders — specialized layout patterns."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))

from pptx_lib import add_text, header, layout_by_names, lighter, set_dash
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches as _Inches, Pt
from lxml import etree as _etree
from renderer_utils import shape_rect, textbox
from semantic_layout_constraints import apply_semantic_constraints_emu  # pyright: ignore[reportMissingImports]

_LEGACY_WIDTH_IN = 13.333
_LEGACY_HEIGHT_IN = 7.5
_SCALE = 1.0


def _set_scale(ctx):
    """Scale legacy TOGAF coordinates to current master size."""
    global _SCALE
    sx = ctx.prs.slide_width / _Inches(_LEGACY_WIDTH_IN)
    sy = ctx.prs.slide_height / _Inches(_LEGACY_HEIGHT_IN)
    # Keep uniform scaling so relative geometry remains consistent.
    _SCALE = float(min(sx, sy))


def Inches(value):
    """Scaled inches helper: legacy coords -> active master coords."""
    return _Inches(float(value) * _SCALE)

def _semantic_from_theme(c):
    """Build semantic colors from master theme whenever possible."""
    return {
        "warn": c.get("warn", c.get("accent5", c.get("primary"))),
        "red": c.get("red", c.get("accent1", c.get("primary"))),
        "green": c.get("green", c.get("accent4", c.get("secondary"))),
    }


def _C(ctx):
    """Build colors dict from theme + semantic overrides."""
    c = dict(ctx.colors)
    c.update(_semantic_from_theme(c))
    c.setdefault("white", (255, 255, 255))
    c.setdefault("text", c.get("dark", (34, 34, 34)))
    c.setdefault("line", c.get("gray", (190, 190, 190)))
    c.setdefault("dark", c.get("text", (34, 34, 34)))
    return c


# Layout constants (inches)
_CX, _CY = 0.55, 1.55
_CW, _CH = 12.25, 5.45
_FY = 6.82


# ─── Base helpers ─────────────────────────────────────────────────────────────

def _new_slide(ctx):
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    return ctx.prs.slides.add_slide(layout)


def set_subtitle(ctx, slide, text, C):
    ph = next(
        (s for s in slide.shapes
         if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1),
        None,
    )
    if ph and ph.has_text_frame:
        tf = ph.text_frame; tf.clear()
        p = tf.paragraphs[0]; p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*C["gray"])


def short(text, limit=36):
    t = str(text or "")
    return t if len(t) <= limit else t[:max(1, limit - 1)] + "…"


def should_render(value):
    """Check if a field value should be rendered.
    
    Returns False if value is None, empty string, or empty list/dict.
    This allows loaders to conditionally skip rendering optional elements.
    """
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    return True


def _badge(slide, tag, C):
    shape_rect(slide, int(Inches(_CX)), int(Inches(_CY - 0.30)),
               int(Inches(1.30)), int(Inches(0.24)), fill_color=C["dark"])
    textbox(slide, int(Inches(_CX)), int(Inches(_CY - 0.29)),
            int(Inches(1.30)), int(Inches(0.18)),
            tag, size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)


def _footer(slide, note="", C=None):
    if should_render(note) and C:
        textbox(slide, int(Inches(_CX)), int(Inches(_FY)),
                int(Inches(8.4)), int(Inches(0.22)),
                short(note, 120), size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)


def _init(ctx, data, dt, ds, tag, C=None, P=None):
    if C is None: C = _C(ctx)
    _set_scale(ctx)
    slide = _new_slide(ctx)
    header(slide, data.get("title", dt))
    set_subtitle(ctx, slide, data.get("subtitle", ds), C)
    _badge(slide, tag, C)
    return slide


def _canvas(ctx, data, dt, ds, tag, C, P, slide=None, region=None, th_margin=0.3):
    """
    Create or reuse a slide and return the usable canvas bounds.
    Returns (slide, x0, y0, tw, th, is_fullpage).

    Full-page mode (slide=None):
      Creates a new slide with header / subtitle / badge.
      Prefer the active master's safe content region when available.

    Region mode (slide, region=(x, y, w, h)):
      Paints into the specified region on an existing slide.
      No header / subtitle / badge is rendered; _footer is suppressed.
      All (x, y, w, h) values must be in EMU integers.
    """
    _set_scale(ctx)
    if slide is None:
        sl = _new_slide(ctx)
        header(sl, data.get("title", dt))
        set_subtitle(ctx, sl, data.get("subtitle", ds), C)
        _badge(sl, tag, C)
        if all(hasattr(ctx, attr) for attr in ("safe_left", "safe_width", "content_top", "safe_bottom")):
            sx = int(ctx.safe_left)
            sy = int(ctx.content_top + Inches(0.08))
            sw = int(ctx.safe_width)
            sh = int(ctx.safe_bottom - sy - Inches(0.06))
            return sl, sx, sy, sw, sh, True
        return sl, int(Inches(_CX)), int(Inches(_CY)), int(Inches(_CW)), int(Inches(_CH - th_margin)), True
    x, y, w, h = region
    return slide, int(x), int(y), int(w), int(h), False


def _lighter(c, a=110):
    return tuple(min(255, x + a) for x in c)


def _hline(slide, x, y, w, color, thick=0.04):
    shape_rect(slide, x, y - int(Inches(thick / 2)), w, int(Inches(thick)), fill_color=color)


def _vline(slide, x, y, h, color, thick=0.04):
    shape_rect(slide, x - int(Inches(thick / 2)), y, int(Inches(thick)), h, fill_color=color)


# ─── Pattern 1: Capability Grid ───────────────────────────────────────────────
# BA-01, AA-11, TA-09  ·  rows × cells, left label strip + colored cells

_CAPA_DEF = [
    {"label": "Core Capabilities",     "items": ["Client Acquire",  "Service Deliver", "Retain",    "Analytics"]},
    {"label": "Support",               "items": ["Finance",         "HR & Talent",     "Legal",     "Compliance"]},
    {"label": "Enablement",            "items": ["Data Platform",   "Technology",      "Innovation","Governance"]},
]


def render_capability_grid(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Capability Map', 'Capability domain overview', tag, C, P, slide, region, th_margin=0.3)
    c    = data.get("content", {})
    rows = c.get("rows", defaults or _CAPA_DEF)
    note = c.get("note", "")
    n    = len(rows)

    lw = int(Inches(1.1));  g  = int(Inches(0.07))
    rh = int((th - g * (n - 1)) / n)
    for i, row in enumerate(rows):
        y   = y0 + i * (rh + g)
        col = P[i % len(P)]
        lit = _lighter(col)
        shape_rect(slide, x0, y, lw, rh, fill_color=col)
        textbox(slide, x0, y + rh // 2 - int(Inches(0.15)), lw, int(Inches(0.28)),
                short(row.get("label", ""), 16), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        items = list(row.get("items", []))
        ni  = max(len(items), 1)
        ix0 = x0 + lw + g
        itw = tw - lw - g
        cw  = int((itw - g * (ni - 1)) / ni)
        for j, item in enumerate(items):
            cx = ix0 + j * (cw + g)
            shape_rect(slide, cx, y, cw, rh, fill_color=lit, line_color=C["line"])
            textbox(slide, cx + int(Inches(0.05)), y + rh // 2 - int(Inches(0.12)),
                    cw - int(Inches(0.1)), int(Inches(0.24)),
                    short(item, 20), size="label", color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 2: Horizontal Stage Flow ─────────────────────────────────────────
# BA-02 Value Stream, AA-05 Service Interaction, DA-06 Master Data Lifecycle

_FLOW_DEF = [
    {"title": "Initiate",  "items": ["Define scope",      "Assign owners"]},
    {"title": "Analyze",   "items": ["Current state",     "Gap analysis"]},
    {"title": "Design",    "items": ["Target state",      "Architecture"]},
    {"title": "Build",     "items": ["Implement",         "Integrate"]},
    {"title": "Operate",   "items": ["Monitor",           "Improve"]},
]


def render_flow_stages(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Stage Flow', 'Left-to-right value stages', tag, C, P, slide, region, th_margin=0.55)
    c      = data.get("content", {})
    stages = c.get("stages", defaults or _FLOW_DEF)
    note   = c.get("note", "")
    n      = len(stages)
    aw = int(Inches(0.22))
    if fp:
        x0 = int(Inches(_CX))
        y0 = int(Inches(_CY + 0.05))
    else:
        y0 += int(Inches(0.05))
    g  = int(Inches(0.05))
    bh = th - int(Inches(0.25))
    bw = int((tw - aw * (n - 1) - g * 2 * (n - 1)) / n)
    for i, stage in enumerate(stages):
        cx  = x0 + i * (bw + aw + g * 2)
        col = P[i % len(P)]
        lit = _lighter(col)
        shape_rect(slide, cx, y0, bw, bh, fill_color=lit, line_color=C["line"])
        shape_rect(slide, cx, y0, bw, int(Inches(0.32)), fill_color=col)
        textbox(slide, cx + int(Inches(0.05)), y0 + int(Inches(0.04)),
                bw - int(Inches(0.1)), int(Inches(0.24)),
                short(stage.get("title", f"S{i+1}"), 18), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        for bi, item in enumerate(list(stage.get("items", []))[:5]):
            textbox(slide, cx + int(Inches(0.07)), y0 + int(Inches(0.38 + bi * 0.46)),
                    bw - int(Inches(0.14)), int(Inches(0.4)),
                    f"· {short(item, 28)}", size="caption", color=C["text"])
        if i < n - 1:
            ax = cx + bw + g;  ay = y0 + bh // 2
            _hline(slide, ax, ay, aw + g, C["primary"], 0.14)
            shape_rect(slide, ax + aw + g - int(Inches(0.06)),
                       ay - int(Inches(0.12)), int(Inches(0.06)), int(Inches(0.24)),
                       fill_color=C["primary"])
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 3: Swimlane ───────────────────────────────────────────────────────
# BA-03 Business Process, AA-10 Application Sequence Flow

_LANE_DEF = [
    {"actor": "Customer",     "steps": ["Submit Request",    "Review Proposal",  "Accept & Sign"]},
    {"actor": "Front-Office", "steps": ["Receive Request",   "Prepare Proposal", ""]},
    {"actor": "Back-Office",  "steps": ["",                  "Evaluate & Approve","Dispatch"]},
]


def _rgb(color, C=None):
    """Convert color to RGBColor: supports tuple (r,g,b), color name string, or RGBColor.
    
    Handles:
    - RGBColor instances (pass through)
    - Tuples/lists of (r,g,b) -> convert to RGBColor
    - String color names (if C dict provided, resolve; otherwise fallback to gray)
    - None -> fallback to dark gray
    """
    # Already an RGBColor
    if isinstance(color, RGBColor):
        return color
    # Tuple/list -> convert to RGBColor
    if isinstance(color, (tuple, list)) and len(color) == 3:
        return RGBColor(*color)
    # String color name - try to resolve from theme
    if isinstance(color, str):
        if C and color in C:
            resolved = C.get(color)
            # Recursively convert the resolved value
            if isinstance(resolved, (tuple, list)):
                return RGBColor(*resolved)
            if isinstance(resolved, RGBColor):
                return resolved
        # If not found or resolution failed, return gray fallback
        return RGBColor(128, 128, 128)
    # None or unknown -> fallback to gray
    return RGBColor(128, 128, 128)


def _bp_round_rect(slide, x, y, w, h, fill, line=None, line_width=1.0, C=None):
    # Use rectangle instead of rounded rectangle
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(fill, C)
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = _rgb(line, C)
        shape.line.width = Pt(line_width)
    return shape


def _bp_lane(slide, x, y, w, h, title, C, header_w):
    shape_rect(slide, x, y, header_w, h, fill_color=C["dark"])
    textbox(slide, x + int(Inches(0.08)), y + int(Inches(0.08)),
            header_w - int(Inches(0.16)), h - int(Inches(0.16)),
            title, size=11, bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    body_x = x + header_w + int(Inches(0.02))
    body_w = max(int(Inches(0.60)), w - header_w - int(Inches(0.02)))
    shape_rect(slide, body_x, y, body_w, h,
               fill_color=C.get("white", (255, 255, 255)), line_color=C["line"])


def _bp_step(slide, x, y, w, h, step, C):
    name = step.get("name") or step.get("text") or ""
    system = step.get("system", "")
    duration = step.get("duration", "")
    critical = bool(step.get("critical"))
    manual = bool(step.get("manual"))

    fill = step.get("fill_color", C.get("light", (230, 245, 247)) if not manual else _lighter(C["gray"], 145))
    edge = step.get("line_color", C["primary"] if critical else C["line"])
    text_color = step.get("text_color", C["dark"])
    system_fill = step.get("system_fill_color", C["dark"])
    system_text = step.get("system_text_color", C["white"])
    duration_line = step.get("duration_line_color", C["gray"])
    duration_text = step.get("duration_text_color", C["gray"])
    shape = _bp_round_rect(slide, x, y, w, h, fill, line=edge, line_width=2.0 if critical else 1.0, C=C)
    if manual:
        set_dash(shape)

    # Add text directly to the shape
    if name:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_top = int(Inches(0.05))
        tf.margin_bottom = int(Inches(0.05))
        tf.margin_left = int(Inches(0.05))
        tf.margin_right = int(Inches(0.05))
        for i, line in enumerate(short(name, 22).split('\n')):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9)
            p.font.color.rgb = _rgb(text_color, C)
            p.alignment = PP_ALIGN.CENTER

    if should_render(system):
        pill = _bp_round_rect(slide, x + int(Inches(0.12)), y + int(Inches(0.34)),
                              w - int(Inches(0.24)), int(Inches(0.14)),
                              system_fill, line=system_fill, C=C)
        add_text(pill, short(system, 18), size=7, color=_rgb(system_text, C))

    if should_render(duration):
        dur = _bp_round_rect(slide, x + w - int(Inches(0.34)), y + int(Inches(0.02)),
                             int(Inches(0.30)), int(Inches(0.12)),
                             C.get("white", (255, 255, 255)), line=duration_line, C=C)
        add_text(dur, short(duration, 8), size=6, color=_rgb(duration_text, C))

    if critical:
        textbox(slide, x + w - int(Inches(0.10)), y - int(Inches(0.03)),
                int(Inches(0.08)), int(Inches(0.08)),
                "!", size=8, bold=True, color=C["red"], align=PP_ALIGN.CENTER)
    return shape


def _bp_decision(slide, x, y, w, h, text, C, *, fill=None, line=None, text_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(fill or C.get("white", (255, 255, 255)), C)
    shape.line.color.rgb = _rgb(line or C["dark"], C)
    shape.line.width = Pt(1.2)
    
    # Add text directly to the shape
    if text:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_top = int(Inches(0.05))
        tf.margin_bottom = int(Inches(0.05))
        tf.margin_left = int(Inches(0.05))
        tf.margin_right = int(Inches(0.05))
        for i, line in enumerate(short(text, 14).split('\n')):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(8)
            p.font.color.rgb = _rgb(text_color or C["dark"], C)
            p.alignment = PP_ALIGN.CENTER
    return shape


def _bp_event(slide, x, y, C, *, start=False, end=False):
    size = int(Inches(0.18))
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, size, size)
    shape.fill.solid()
    fill = C["dark"] if start or end else C["primary"]
    shape.fill.fore_color.rgb = _rgb(fill)
    shape.line.color.rgb = _rgb(fill)
    return shape


def _bp_anchor(box, side):
    x, y, w, h = box
    if side == "left":
        return x, y + h // 2
    if side == "right":
        return x + w, y + h // 2
    if side == "top":
        return x + w // 2, y
    if side == "bottom":
        return x + w // 2, y + h
    return x + w // 2, y + h // 2


def _bp_anchor_index(side):
    return {
        "top": 0,
        "left": 1,
        "bottom": 2,
        "right": 3,
    }.get(side)


def _bp_link(slide, start_node, end_node, C, label="", dashed=False, color=None,
             start_side="right", end_side="left"):
    start_box = start_node.get("box") if isinstance(start_node, dict) else start_node
    end_box = end_node.get("box") if isinstance(end_node, dict) else end_node
    start_shape = start_node.get("shape") if isinstance(start_node, dict) else None
    end_shape = end_node.get("shape") if isinstance(end_node, dict) else None
    sx, sy = _bp_anchor(start_box, start_side)
    ex, ey = _bp_anchor(end_box, end_side)
    connector_type = MSO_CONNECTOR.ELBOW if (sx != ex and sy != ey) else MSO_CONNECTOR.STRAIGHT
    conn = slide.shapes.add_connector(connector_type, sx, sy, ex, ey)
    conn.line.color.rgb = _rgb(color or C["dark"], C)
    conn.line.width = Pt(1.3)
    if dashed:
        conn.line.dash_style = 4
    # Add triangle arrowhead at connector end
    ln = conn.line._ln
    tail_end = _etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd')
    tail_end.set('type', 'triangle')
    tail_end.set('w', 'med')
    tail_end.set('len', 'med')
    if start_shape is not None:
        try:
            conn.begin_connect(start_shape, _bp_anchor_index(start_side))
        except Exception:
            pass
    if end_shape is not None:
        try:
            conn.end_connect(end_shape, _bp_anchor_index(end_side))
        except Exception:
            pass
    if label:
        mx = (sx + ex) // 2
        my = (sy + ey) // 2
        textbox(slide, mx - int(Inches(0.4)), my - int(Inches(0.15)),
                int(Inches(0.8)), int(Inches(0.15)),
                label, size=7, color=C["gray"], align=PP_ALIGN.CENTER)


def _swimlane_simple(slide, x0, y0, tw, th, lanes, C, P):
    nl = len(lanes)
    ns = max((len(l.get("steps", [])) for l in lanes), default=3)
    ns = max(ns, 3)
    lane_gap = int(Inches(0.06))
    step_gap = int(Inches(0.08))
    header_w = int(Inches(1.20))
    lh = int((th - lane_gap * (nl - 1)) / nl)
    flow_w = tw - header_w - int(Inches(0.16))
    sw = int((flow_w - step_gap * (ns - 1)) / ns)
    step_h = min(int(Inches(0.58)), max(int(Inches(0.44)), lh - int(Inches(0.22))))

    for i, lane in enumerate(lanes):
        ly = y0 + i * (lh + lane_gap)
        _bp_lane(slide, x0, ly, tw, lh, lane.get("actor", ""), C, header_w)
        lx = x0 + header_w + int(Inches(0.12))
        prev_box = None
        for j, step in enumerate(list(lane.get("steps", []))[:ns]):
            if isinstance(step, str):
                step = {"name": step}
            if not str(step.get("name") or step.get("text") or "").strip():
                prev_box = None
                continue
            sx = lx + j * (sw + step_gap)
            sy = ly + (lh - step_h) // 2
            box = (sx, sy, sw, step_h)
            if step.get("type") == "decision":
                _bp_decision(slide, sx, sy, sw, step_h, step.get("text") or step.get("name", ""), C)
            elif step.get("type") == "event":
                event_size = int(Inches(0.18))
                ex = sx + (sw - event_size) // 2
                ey = sy + (step_h - event_size) // 2
                _bp_event(slide, ex, ey, C, start=step.get("start", False), end=step.get("end", False))
                box = (ex, ey, event_size, event_size)
            else:
                _bp_step(slide, sx, sy, sw, step_h, step, C)
            if prev_box is not None:
                _bp_link(slide, prev_box, box, C, label=step.get("link_label", ""),
                         dashed=step.get("dashed", False), color=C["primary"])
            prev_box = box


def _swimlane_detailed(slide, x0, y0, tw, th, content, C):
    # Layout rule for production swimlanes:
    # 1) keep activity boxes size-consistent unless content forces exception,
    # 2) align semantically paired cross-lane nodes on shared centerlines when possible,
    # 3) distribute nodes evenly across the usable flow canvas to avoid large right-side whitespace.
    lanes = content.get("lanes", [])
    lane_names = [lane.get("actor", "") if isinstance(lane, dict) else str(lane) for lane in lanes]
    if not lane_names:
        return

    lane_gap = int(Inches(content.get("lane_gap", 0.08)))
    header_w = int(Inches(content.get("lane_header_w", 1.22)))
    flow_gap = int(Inches(content.get("flow_gap", 0.11)))
    lh = int((th - lane_gap * (len(lane_names) - 1)) / len(lane_names))
    flow_x = x0 + header_w + flow_gap
    flow_w = tw - header_w - flow_gap

    lane_boxes = {}
    for idx, lane_name in enumerate(lane_names):
        ly = y0 + idx * (lh + lane_gap)
        lane_boxes[lane_name] = (flow_x, ly, flow_w, lh)
        _bp_lane(slide, x0, ly, tw, lh, lane_name, C, header_w)

    nodes = content.get("nodes", [])
    has_event_node = any(node.get("type") == "event" for node in nodes)
    ncols = max(content.get("columns", 0), max((int(node.get("col", 0)) for node in nodes), default=0) + 1, 1)
    col_gap = int(Inches(content.get("col_gap", 0.18)))
    slot_w = int((flow_w - col_gap * max(0, ncols - 1)) / ncols)
    base_step_w = min(int(Inches(content.get("step_w", 0.92))), slot_w)
    base_step_h = int(Inches(content.get("step_h", 0.56)))
    left_pad = int(Inches(content.get("left_pad_in", 0.12 if has_event_node else 0.06)))
    right_pad = int(Inches(content.get("right_pad_in", 0.28 if has_event_node else 0.06)))
    start_event_outer_pad = int(Inches(content.get("start_event_outer_pad_in", 0.04)))
    end_event_outer_pad = int(Inches(content.get("end_event_outer_pad_in", 0.06)))

    node_map = {}
    pending_nodes = []
    for node in nodes:
        lane_name = node.get("lane") or lane_names[min(int(node.get("lane_index", 0)), len(lane_names) - 1)]
        lane_box = lane_boxes.get(lane_name)
        if lane_box is None:
            continue
        lx, ly, _, lh2 = lane_box
        node_w = int(Inches(node.get("w_in", 0))) if node.get("w_in") is not None else base_step_w
        node_h = int(Inches(node.get("h_in", 0))) if node.get("h_in") is not None else base_step_h
        if node.get("type") == "decision":
            node_w = node_w or int(Inches(0.56))
            node_h = node_h or int(Inches(0.52))
        elif node.get("type") == "event":
            node_w = node_h = int(Inches(0.18))

        if node.get("x_in") is not None:
            nx = flow_x + int(Inches(node.get("x_in", 0)))
        else:
            col = int(node.get("col", 0))
            nx = lx + col * (slot_w + col_gap)

        # 约束节点在可用泳道画布内。
        # 普通节点遵守通用左右留白；开始/结束事件节点单独计算外侧边距，
        # 避免把终点圆点反向挤回最后一个活动框上方/内部。
        min_x = flow_x + left_pad
        max_x = flow_x + flow_w - node_w - right_pad
        if node.get("type") == "event":
            if node.get("start", False):
                min_x = flow_x + start_event_outer_pad
            if node.get("end", False):
                max_x = flow_x + flow_w - node_w - end_event_outer_pad
        nx = max(min_x, min(nx, max_x))
        
        if node.get("y_in") is not None:
            ny = y0 + int(Inches(node.get("y_in", 0)))
        else:
            ny = ly + (lh2 - node_h) // 2
        
        # 约束节点不超出底边界
        max_y = y0 + th - node_h - int(Inches(0.02))
        ny = min(ny, max_y)

        kind = node.get("type", "step")
        node_id = node.get("id", f"node_{len(pending_nodes)}")
        pending_nodes.append({
            "id": node_id,
            "node": node,
            "kind": kind,
            "node_w": node_w,
            "node_h": node_h,
            "nx": nx,
            "ny": ny,
        })

    raw_positions = {
        item["id"]: (item["nx"], item["ny"], item["node_w"], item["node_h"])
        for item in pending_nodes
    }
    semantic_constraints = content.get("semantic_constraints")
    if semantic_constraints:
        region_in = {
            "left": flow_x / 914400,
            "top": y0 / 914400,
            "width": flow_w / 914400,
            "height": th / 914400,
        }
        raw_positions = apply_semantic_constraints_emu(
            raw_positions,
            nodes,
            region_in,
            semantic_constraints,
        )

    for item in pending_nodes:
        node = item["node"]
        kind = item["kind"]
        node_id = item["id"]
        nx, ny, node_w, node_h = raw_positions.get(
            node_id,
            (item["nx"], item["ny"], item["node_w"], item["node_h"]),
        )

        if kind == "decision":
            shape = _bp_decision(
                slide, nx, ny, node_w, node_h, node.get("text") or node.get("name", ""), C,
                fill=node.get("fill_color"), line=node.get("line_color"), text_color=node.get("text_color"),
            )
        elif kind == "event":
            shape = _bp_event(slide, nx, ny, C, start=node.get("start", False), end=node.get("end", False))
        else:
            shape = _bp_step(slide, nx, ny, node_w, node_h, node, C)

        node_map[node_id] = {
            "shape": shape,
            "box": (nx, ny, node_w, node_h),
            "kind": kind,
        }

    for link in content.get("links", []):
        start_box = node_map.get(link.get("from"))
        end_box = node_map.get(link.get("to"))
        if not start_box or not end_box:
            continue
        link_color = C["gray"] if link.get("dashed") else C["dark"]
        _bp_link(
            slide,
            start_box,
            end_box,
            C,
            label=link.get("label", ""),
            dashed=bool(link.get("dashed")),
            color=link.get("color", link_color),
            start_side=link.get("start_side", "right"),
            end_side=link.get("end_side", "left"),
        )


def render_swimlane(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Swimlane Flow', 'Multi-actor process flow', tag, C, P, slide, region, th_margin=0.3)
    c = data.get("content", {})
    default_content = defaults if isinstance(defaults, dict) else {}
    merged = dict(default_content)
    merged.update(c)
    note = merged.get("note", "") or c.get("note", "")
    lanes = merged.get("lanes", defaults or _LANE_DEF)

    if merged.get("nodes"):
        _swimlane_detailed(slide, x0, y0, tw, th, merged, C)
    else:
        _swimlane_simple(slide, x0, y0, tw, th, lanes, C, P)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 4: Actor Grid (hub + left / right spokes) ────────────────────────
# BA-04 Actor Interaction

_ACTOR_DEF = {
    "hub": "Central Service Hub",
    "spokes": [
        {"label": "Sales",         "interaction": "Lead & Opportunity"},
        {"label": "Product",       "interaction": "Product Information"},
        {"label": "Operations",    "interaction": "Execution & Delivery"},
        {"label": "Finance",       "interaction": "Billing & Cost"},
        {"label": "Technology",    "interaction": "Platform Support"},
        {"label": "Customer",      "interaction": "Service Request"},
    ],
}


def render_actor_grid(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Actor Interaction', 'Hub-and-spoke collaboration', tag, C, P, slide, region, th_margin=0.3)
    c       = data.get("content", {})
    note    = c.get("note", "")
    d       = defaults or _ACTOR_DEF
    hub_lbl = c.get("hub", d["hub"])
    spokes  = c.get("spokes", d["spokes"])
    n       = len(spokes)
    left_s  = spokes[:(n + 1) // 2]
    right_s = spokes[(n + 1) // 2:]
    nl, nr  = len(left_s), len(right_s)

    sw = int(Inches(1.95)); sh = int(Inches(0.62))
    hw = int(Inches(2.2));  hh = int(Inches(0.72))
    g  = int(Inches(0.15))
    hcx = x0 + tw // 2 - hw // 2
    hcy = y0 + th // 2 - hh // 2
    shape_rect(slide, hcx, hcy, hw, hh, fill_color=C["dark"], line_color=C["primary"])
    textbox(slide, hcx, hcy + hh // 2 - int(Inches(0.13)), hw, int(Inches(0.26)),
            short(hub_lbl, 20), size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for i, sp in enumerate(left_s):
        col = P[(i + 1) % len(P)];  lit = _lighter(col)
        sy  = y0 + (i * (sh + g)) + max(0, (th - nl * (sh + g)) // 2)
        shape_rect(slide, x0, sy, sw, sh, fill_color=lit, line_color=C["line"])
        textbox(slide, x0 + int(Inches(0.06)), sy + int(Inches(0.05)),
                sw - int(Inches(0.12)), int(Inches(0.22)),
                short(sp.get("label", ""), 22), size="label", bold=True, color=C["text"])
        textbox(slide, x0 + int(Inches(0.06)), sy + int(Inches(0.28)),
                sw - int(Inches(0.12)), int(Inches(0.28)),
                short(sp.get("interaction", ""), 26), size="caption", color=C["gray"])
        _hline(slide, x0 + sw, sy + sh // 2, hcx - (x0 + sw), C["secondary"], 0.05)
    rx = hcx + hw + int(Inches(0.3))
    for i, sp in enumerate(right_s):
        col = P[(i + 4) % len(P)];  lit = _lighter(col)
        sy  = y0 + (i * (sh + g)) + max(0, (th - nr * (sh + g)) // 2)
        shape_rect(slide, rx, sy, sw, sh, fill_color=lit, line_color=C["line"])
        textbox(slide, rx + int(Inches(0.06)), sy + int(Inches(0.05)),
                sw - int(Inches(0.12)), int(Inches(0.22)),
                short(sp.get("label", ""), 22), size="label", bold=True, color=C["text"])
        textbox(slide, rx + int(Inches(0.06)), sy + int(Inches(0.28)),
                sw - int(Inches(0.12)), int(Inches(0.28)),
                short(sp.get("interaction", ""), 26), size="caption", color=C["gray"])
        _hline(slide, hcx + hw, sy + sh // 2, rx - (hcx + hw), C["secondary"], 0.05)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 5: Hierarchy Tree ─────────────────────────────────────────────────
# BA-05 Service Decomposition, AA-02 Component Diagram, DA-08 Data Catalog

_TREE_DEF = {
    "root": "Root Service",
    "branches": [
        {"label": "Domain A", "children": ["Service A1", "Service A2", "A3"]},
        {"label": "Domain B", "children": ["Service B1", "Service B2"]},
        {"label": "Domain C", "children": ["Service C1", "Service C2", "C3"]},
    ],
}


def render_tree(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Hierarchy Tree', 'Service / component decomposition', tag, C, P, slide, region, th_margin=0.3)
    c        = data.get("content", {})
    note     = c.get("note", "")
    d        = defaults or _TREE_DEF
    root     = c.get("root", d["root"])
    branches = c.get("branches", d["branches"])[:5]
    nb       = len(branches)

    rw = int(Inches(2.4));  rh = int(Inches(0.44))
    rx = x0 + tw // 2 - rw // 2
    ry = y0
    shape_rect(slide, rx, ry, rw, rh, fill_color=C["dark"])
    textbox(slide, rx + int(Inches(0.05)), ry + int(Inches(0.07)),
            rw - int(Inches(0.1)), int(Inches(0.28)),
            short(root, 22), size="caption", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    bw   = int((tw - int(Inches(0.08)) * (nb - 1)) / nb)
    bh   = int(Inches(0.42))
    link_y = ry + rh + int(Inches(0.2))
    by   = link_y + int(Inches(0.22))
    b_xs = [x0 + i * (bw + int(Inches(0.08))) + bw // 2 for i in range(nb)]
    _vline(slide, rx + rw // 2, ry + rh, link_y - (ry + rh), C["primary"])
    if nb > 1:
        _hline(slide, b_xs[0], link_y, b_xs[-1] - b_xs[0], C["primary"])
    for i, br in enumerate(branches):
        bx  = x0 + i * (bw + int(Inches(0.08)))
        col = P[i % len(P)];  lit = _lighter(col)
        _vline(slide, b_xs[i], link_y, by - link_y, C["primary"])
        shape_rect(slide, bx, by, bw, bh, fill_color=col)
        textbox(slide, bx + int(Inches(0.05)), by + int(Inches(0.07)),
                bw - int(Inches(0.1)), int(Inches(0.28)),
                short(br.get("label", ""), 20), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        children = list(br.get("children", []))[:4]
        nc = len(children)
        if not nc:
            continue
        child_link_y = by + bh + int(Inches(0.18))
        cy = child_link_y + int(Inches(0.2))
        cw = int((bw - int(Inches(0.06)) * (nc - 1)) / nc)
        ch = int(Inches(0.38))
        c_xs = [bx + j * (cw + int(Inches(0.06))) + cw // 2 for j in range(nc)]
        _vline(slide, b_xs[i], by + bh, child_link_y - (by + bh), C["primary"])
        if nc > 1:
            _hline(slide, c_xs[0], child_link_y, c_xs[-1] - c_xs[0], C["primary"])
        for j, child in enumerate(children):
            cx2 = bx + j * (cw + int(Inches(0.06)))
            _vline(slide, c_xs[j], child_link_y, cy - child_link_y, C["primary"])
            shape_rect(slide, cx2, cy, cw, ch, fill_color=lit, line_color=C["line"])
            textbox(slide, cx2 + int(Inches(0.03)), cy + int(Inches(0.05)),
                    cw - int(Inches(0.06)), ch - int(Inches(0.1)),
                    short(child, 18), size="caption", color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 6: Matrix Table ───────────────────────────────────────────────────
# BA-06 Function-Capability Mapping, BA-10 RACI Matrix, AA-09 App-Capability


_MATRIX_DEF = {
    "row_headers": ["Process A", "Process B", "Process C", "Process D"],
    "col_headers": ["Owner",    "Architect",  "Dev Team",  "Ops"],
    "cells":       [["R","A","C","I"], ["C","R","A","I"], ["I","C","R","A"], ["I","I","C","R"]],
}


def render_matrix_table(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    _RACI_CELL_COLORS = {"R": C["red"], "A": C["primary"], "C": C["warn"], "I": C["gray"]}
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Matrix / Table', 'Responsibility and mapping grid', tag, C, P, slide, region, th_margin=0.25)
    c         = data.get("content", {})
    note      = c.get("note", "")
    d         = defaults or _MATRIX_DEF
    row_hdrs  = c.get("row_headers", d["row_headers"])
    col_hdrs  = c.get("col_headers", d["col_headers"])
    cells     = c.get("cells",       d["cells"])
    nr, nc    = len(row_hdrs), len(col_hdrs)

    lw = int(Inches(1.9));   hh = int(Inches(0.38))
    cw = int((tw - lw) / nc);  rh = int((th - hh) / nr)
    shape_rect(slide, x0, y0, lw, hh, fill_color=C["dark"])
    for j, ch_lbl in enumerate(col_hdrs):
        cx = x0 + lw + j * cw
        shape_rect(slide, cx, y0, cw, hh, fill_color=C["dark"], line_color=C["line"])
        textbox(slide, cx + int(Inches(0.03)), y0 + int(Inches(0.07)),
                cw - int(Inches(0.06)), int(Inches(0.24)),
                short(ch_lbl, 14), size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for i, rh_lbl in enumerate(row_hdrs):
        ry  = y0 + hh + i * rh
        col = P[i % len(P)];  lit = _lighter(col, 130)
        shape_rect(slide, x0, ry, lw, rh, fill_color=lit, line_color=C["line"])
        textbox(slide, x0 + int(Inches(0.06)), ry + rh // 2 - int(Inches(0.12)),
                lw - int(Inches(0.12)), int(Inches(0.24)),
                short(rh_lbl, 22), size="label", bold=True, color=C["text"])
        row_cells = cells[i] if i < len(cells) else []
        for j in range(nc):
            val = str(row_cells[j]) if j < len(row_cells) else ""
            cx  = x0 + lw + j * cw
            cell_col = _RACI_CELL_COLORS.get(val.upper()) if val.upper() in _RACI_CELL_COLORS else None
            shape_rect(slide, cx, ry, cw, rh,
                       fill_color=cell_col or C["light"], line_color=C["line"])
            textbox(slide, cx + int(Inches(0.03)), ry + rh // 2 - int(Inches(0.12)),
                    cw - int(Inches(0.06)), int(Inches(0.24)),
                    short(val, 16) if val else "·",
                    size="label" if val.upper() in _RACI_CELL_COLORS else 7.5,
                    bold=val.upper() in _RACI_CELL_COLORS,
                    color=C["white"] if cell_col else C["text"],
                    align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 7: Two-Column Compare ─────────────────────────────────────────────
# BA-07 As-Is/To-Be, TA-08 Disaster Recovery

_TWO_COL_DEF = {
    "left_title":  "As-Is / Current",
    "right_title": "To-Be / Target",
    "left_items":  ["Manual processes",   "Siloed systems",     "Data fragmentation", "High operational cost"],
    "right_items": ["Automated workflows","Integrated platform","Unified data layer",  "Optimized OpEx"],
    "delta":       "Δ Transform",
}


def render_two_column(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'As-Is / To-Be', 'Before-and-after transformation', tag, C, P, slide, region, th_margin=0.25)
    c     = data.get("content", {})
    note  = c.get("note", "")
    d     = defaults or _TWO_COL_DEF
    lt    = c.get("left_title",  d["left_title"])
    rt    = c.get("right_title", d["right_title"])
    li    = c.get("left_items",  d["left_items"])
    ri    = c.get("right_items", d["right_items"])
    delta = c.get("delta",       d["delta"])

    aw = int(Inches(0.9));  ph = int(Inches(0.44))
    cw = int((tw - aw) // 2)
    # left panel (gray = as-is)
    shape_rect(slide, x0, y0, cw, th, fill_color=lighter(C["gray"], 0.6), line_color=C["line"])
    shape_rect(slide, x0, y0, cw, ph, fill_color=C["dark"])
    textbox(slide, x0 + int(Inches(0.1)), y0 + int(Inches(0.07)),
            cw - int(Inches(0.2)), int(Inches(0.28)),
            short(lt, 26), size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for k, txt in enumerate(li[:6]):
        iy = y0 + ph + int(Inches(0.12 + k * 0.62))
        shape_rect(slide, x0 + int(Inches(0.12)), iy, cw - int(Inches(0.24)), int(Inches(0.5)),
                   fill_color=C["light"], line_color=lighter(C["gray"], 0.35))
        textbox(slide, x0 + int(Inches(0.18)), iy + int(Inches(0.1)),
                cw - int(Inches(0.36)), int(Inches(0.3)),
                short(txt, 36), size="label", color=C["text"])
    # center arrow
    mx = x0 + cw
    textbox(slide, mx, y0 + th // 2 - int(Inches(0.28)), aw, int(Inches(0.28)),
            "→", size="h2", bold=True, color=C["primary"], align=PP_ALIGN.CENTER)
    if should_render(delta):
        textbox(slide, mx, y0 + th // 2 - int(Inches(0.0)), aw, int(Inches(0.22)),
                short(delta, 12), size="caption", color=C["gray"], align=PP_ALIGN.CENTER)
    # right panel (cyan = to-be)
    rx = x0 + cw + aw
    rcw = tw - cw - aw
    shape_rect(slide, rx, y0, rcw, th, fill_color=lighter(C["primary"], 0.9), line_color=C["primary"])
    shape_rect(slide, rx, y0, rcw, ph, fill_color=C["primary"])
    textbox(slide, rx + int(Inches(0.1)), y0 + int(Inches(0.07)),
            rcw - int(Inches(0.2)), int(Inches(0.28)),
            short(rt, 26), size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for k, txt in enumerate(ri[:6]):
        iy = y0 + ph + int(Inches(0.12 + k * 0.62))
        shape_rect(slide, rx + int(Inches(0.12)), iy, rcw - int(Inches(0.24)), int(Inches(0.5)),
                   fill_color=lighter(C["primary"], 0.85), line_color=C["primary"])
        textbox(slide, rx + int(Inches(0.18)), iy + int(Inches(0.1)),
                rcw - int(Inches(0.36)), int(Inches(0.3)),
                short(txt, 36), size="label", color=C["text"])
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 8: Journey Stages ─────────────────────────────────────────────────
# BA-08 Scenario Journey Map

_JOURNEY_DEF = [
    {"title": "Awareness",     "touchpoints": ["Ad Campaign", "Search"],        "emotion": "+", "pain": "Hard to find info"},
    {"title": "Consideration", "touchpoints": ["Demo",        "Comparison"],     "emotion": "~", "pain": "Unclear pricing"},
    {"title": "Decision",      "touchpoints": ["Proposal",    "Legal review"],   "emotion": "+", "pain": "Long approval"},
    {"title": "Onboarding",    "touchpoints": ["Training",    "Config"],          "emotion": "-", "pain": "Complex setup"},
    {"title": "Advocacy",      "touchpoints": ["Reviews",     "Referrals"],       "emotion": "+", "pain": ""},
]


def render_journey_stages(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Scenario Journey', 'Customer scenario journey map', tag, C, P, slide, region, th_margin=0.3)
    c      = data.get("content", {})
    phases = c.get("phases", defaults or _JOURNEY_DEF)
    note   = c.get("note", "")
    n      = len(phases)
    g = int(Inches(0.06))
    pw = int((tw - g * (n - 1)) / n)
    ph = th
    e_map = {"+": (C["green"], "😊"), "~": (C["warn"], "😐"), "-": (C["red"], "😟")}
    for i, phase in enumerate(phases):
        cx  = x0 + i * (pw + g)
        col = P[i % len(P)];  lit = _lighter(col, 120)
        shape_rect(slide, cx, y0, pw, ph, fill_color=lit, line_color=C["line"])
        shape_rect(slide, cx, y0, pw, int(Inches(0.32)), fill_color=col)
        textbox(slide, cx + int(Inches(0.04)), y0 + int(Inches(0.04)),
                pw - int(Inches(0.08)), int(Inches(0.24)),
                short(phase.get("title", ""), 16), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        for ti, tp in enumerate(list(phase.get("touchpoints", []))[:3]):
            textbox(slide, cx + int(Inches(0.06)), y0 + int(Inches(0.38 + ti * 0.38)),
                    pw - int(Inches(0.12)), int(Inches(0.34)),
                    f"· {short(tp, 24)}", size="caption", color=C["text"])
        emo = str(phase.get("emotion", "~"))
        e_col, e_icon = e_map.get(emo, (C["gray"], "·"))
        ey = y0 + int(Inches(1.6))
        shape_rect(slide, cx + pw // 2 - int(Inches(0.2)), ey, int(Inches(0.4)), int(Inches(0.4)),
                   fill_color=e_col)
        textbox(slide, cx + pw // 2 - int(Inches(0.2)), ey + int(Inches(0.05)),
                int(Inches(0.4)), int(Inches(0.3)), e_icon, size="label",
                color=C["white"], align=PP_ALIGN.CENTER)
        pain = str(phase.get("pain", ""))
        if should_render(pain):
            textbox(slide, cx + int(Inches(0.05)), y0 + int(Inches(2.2)),
                    pw - int(Inches(0.1)), int(Inches(0.8)),
                    f"⚠ {short(pain, 32)}", size="caption", color=C["red"])
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 9: KPI Cascade ───────────────────────────────────────────────────
# BA-09 KPI Alignment

_KPI_DEF = [
    {"label": "Customer Satisfaction", "owner": "CEO",  "kpis": ["NPS > 50",    "CSAT > 90%", "FCR > 85%"]},
    {"label": "Operational Efficiency","owner": "COO",  "kpis": ["Automation 60%","MTTR < 2h",  "Cost ↓15%"]},
    {"label": "Revenue Growth",        "owner": "CRO",  "kpis": ["YoY +25%",    "New logos 30%","ARR $10M"]},
]


def render_kpi_cascade(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'KPI Alignment', 'Objective → KPI cascade', tag, C, P, slide, region, th_margin=0.3)
    c     = data.get("content", {})
    objs  = c.get("objectives", defaults or _KPI_DEF)
    note  = c.get("note", "")
    no    = len(objs)
    g  = int(Inches(0.12))
    ow = int((tw - g * (no - 1)) / no)
    oh = int(Inches(0.72))
    for i, obj in enumerate(objs):
        ox  = x0 + i * (ow + g)
        col = P[i % len(P)];  lit = _lighter(col)
        shape_rect(slide, ox, y0, ow, oh, fill_color=col)
        textbox(slide, ox + int(Inches(0.06)), y0 + int(Inches(0.05)),
                ow - int(Inches(0.12)), int(Inches(0.28)),
                short(obj.get("label", ""), 22), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        owner = str(obj.get("owner", ""))
        if should_render(owner):
            textbox(slide, ox + int(Inches(0.06)), y0 + int(Inches(0.38)),
                    ow - int(Inches(0.12)), int(Inches(0.22)),
                    f"Owner: {short(owner, 16)}", size="caption", color=C["secondary"],
                    align=PP_ALIGN.CENTER)
        _vline(slide, ox + ow // 2, y0 + oh, int(Inches(0.24)), C["primary"])
        kpis = list(obj.get("kpis", []))[:4]
        kpy  = y0 + oh + int(Inches(0.24))
        for ki, kpi in enumerate(kpis):
            ky = kpy + ki * int(Inches(0.9))
            shape_rect(slide, ox, ky, ow, int(Inches(0.78)), fill_color=lit, line_color=C["line"])
            shape_rect(slide, ox, ky, ow, int(Inches(0.22)), fill_color=_lighter(col, 60))
            textbox(slide, ox + int(Inches(0.05)), ky + int(Inches(0.25)),
                    ow - int(Inches(0.1)), int(Inches(0.44)),
                    short(kpi, 28), size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 10: Layered Stack ────────────────────────────────────────────────
# AA-01 App Landscape, AA-08 Microservice, DA-05 Governance, TA-02/03/04/06/07

_STACK_DEF = [
    {"label": "Presentation",  "items": ["Web UI",         "Mobile App",     "Portal"]},
    {"label": "API Gateway",   "items": ["REST API",       "Auth / AuthZ",   "Rate Limiting"]},
    {"label": "Business Svc",  "items": ["Order Service",  "User Service",   "Product Service"]},
    {"label": "Data",          "items": ["PostgreSQL",     "Redis Cache",    "ElasticSearch"]},
    {"label": "Infrastructure","items": ["Kubernetes",     "CI/CD Pipeline", "Monitoring"]},
]


def render_layered_stack(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Layered Stack', 'Horizontal tier architecture', tag, C, P, slide, region, th_margin=0.28)
    c      = data.get("content", {})
    layers = c.get("layers", defaults or _STACK_DEF)
    note   = c.get("note", "")
    nl     = len(layers)

    lw = int(Inches(1.5));   g = int(Inches(0.06))
    lh = int((th - g * (nl - 1)) / nl)
    for i, layer in enumerate(layers):
        ly  = y0 + i * (lh + g)
        col = P[i % len(P)];  lit = _lighter(col)
        shape_rect(slide, x0, ly, lw, lh, fill_color=col)
        textbox(slide, x0, ly + lh // 2 - int(Inches(0.14)), lw, int(Inches(0.28)),
                short(layer.get("label", ""), 18), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        items = list(layer.get("items", []))
        ni  = max(len(items), 1)
        ix0 = x0 + lw + g
        itw = tw - lw - g
        iw  = int((itw - g * (ni - 1)) / ni)
        for j, item in enumerate(items):
            ix = ix0 + j * (iw + g)
            shape_rect(slide, ix, ly, iw, lh, fill_color=lit, line_color=C["line"])
            textbox(slide, ix + int(Inches(0.06)), ly + lh // 2 - int(Inches(0.12)),
                    iw - int(Inches(0.12)), int(Inches(0.26)),
                    short(item, 22), size="label", color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 11: Node Graph ────────────────────────────────────────────────────
# AA-03 Integration, AA-06 API Graph, DA-03 DFD, DA-04 Data Domain, TA-01 Infra

_GRAPH_DEF = {
    "nodes": [
        {"id": "A", "label": "System A",   "x": 0.1,  "y": 0.2},
        {"id": "B", "label": "System B",   "x": 0.45, "y": 0.2},
        {"id": "C", "label": "System C",   "x": 0.80, "y": 0.2},
        {"id": "D", "label": "Database",   "x": 0.1,  "y": 0.7},
        {"id": "E", "label": "API Gateway","x": 0.45, "y": 0.7},
    ],
    "edges": [
        {"from": "A", "to": "B", "label": "REST"},
        {"from": "B", "to": "C", "label": "gRPC"},
        {"from": "A", "to": "D", "label": "SQL"},
        {"from": "B", "to": "E", "label": "API"},
    ],
}


def render_node_graph(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Node Graph', 'System integration topology', tag, C, P, slide, region, th_margin=0.3)
    c     = data.get("content", {})
    note  = c.get("note", "")
    d     = defaults or _GRAPH_DEF
    nodes = c.get("nodes", d["nodes"])
    edges = c.get("edges", d["edges"])

    nw = int(Inches(1.6));  nh = int(Inches(0.5))
    pos = {}
    for k, n in enumerate(nodes[:16]):
        nx = x0 + int(float(n.get("x", 0.1)) * tw) - nw // 2
        ny = y0 + int(float(n.get("y", 0.5)) * th) - nh // 2
        col = P[k % len(P)]
        shape_rect(slide, nx, ny, nw, nh, fill_color=col, line_color=C["secondary"])
        textbox(slide, nx + int(Inches(0.04)), ny + nh // 2 - int(Inches(0.12)),
                nw - int(Inches(0.08)), int(Inches(0.26)),
                short(n.get("label", ""), 18), size="label", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        pos[n.get("id", str(k))] = (nx + nw // 2, ny + nh // 2, nx, ny, nw, nh)
    for e in edges[:24]:
        src = pos.get(e.get("from"))
        dst = pos.get(e.get("to"))
        if not src or not dst:
            continue
        sx, sy = src[0], src[1];  dx, dy = dst[0], dst[1]
        lth = int(Inches(0.035))
        if abs(sx - dx) >= abs(sy - dy):
            lx = min(sx, dx);  lw2 = abs(dx - sx)
            _hline(slide, lx, sy, lw2, C["secondary"], 0.035)
            if sy != dy:
                _vline(slide, dx, min(sy, dy), abs(dy - sy), C["secondary"], 0.035)
        else:
            ly = min(sy, dy);  lh2 = abs(dy - sy)
            _vline(slide, sx, ly, lh2, C["secondary"], 0.035)
            if sx != dx:
                _hline(slide, min(sx, dx), dy, abs(dx - sx), C["secondary"], 0.035)
        lbl = str(e.get("label", ""))
        if should_render(lbl):
            mx = (sx + dx) // 2;  my = (sy + dy) // 2
            textbox(slide, mx - int(Inches(0.4)), my - int(Inches(0.12)),
                    int(Inches(0.8)), int(Inches(0.2)), short(lbl, 12),
                    size="micro", color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 12: Event Bus ─────────────────────────────────────────────────────
# AA-07 Event-Driven Architecture

_EBUS_DEF = {
    "producers": ["Order Service", "Inventory Service", "User Service", "Payment Service"],
    "bus_title": "Event Bus / Kafka",
    "topics":    ["order.created", "inventory.updated", "user.registered", "payment.processed"],
    "consumers": ["Notification Svc", "Analytics Svc", "Audit Log", "Reporting"],
}


def render_event_bus(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Event-Driven Architecture', 'Producer → Bus → Consumer topology', tag, C, P, slide, region, th_margin=0.28)
    c      = data.get("content", {})
    note   = c.get("note", "")
    d      = defaults or _EBUS_DEF
    prods  = c.get("producers", d["producers"])
    bus_t  = c.get("bus_title",  d["bus_title"])
    topics = c.get("topics",     d["topics"])
    conss  = c.get("consumers",  d["consumers"])

    pw = int(Inches(2.2))
    bw = int(Inches(3.0))
    cw = tw - pw * 2 - bw - int(Inches(0.6))
    bx = x0 + pw + int(Inches(0.3))
    cx = bx + bw + int(Inches(0.3))
    box_h = int(Inches(0.55));  g = int(Inches(0.14))
    # producers
    for i, p in enumerate(prods[:5]):
        col = P[i % len(P)];  lit = _lighter(col)
        py  = y0 + int(Inches(0.2)) + i * (box_h + g)
        shape_rect(slide, x0, py, pw, box_h, fill_color=lit, line_color=C["line"])
        textbox(slide, x0 + int(Inches(0.06)), py + box_h // 2 - int(Inches(0.12)),
                pw - int(Inches(0.12)), int(Inches(0.24)),
                short(p, 22), size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
        _hline(slide, x0 + pw, py + box_h // 2, bx - (x0 + pw), C["primary"], 0.06)
    # bus
    shape_rect(slide, bx, y0, bw, th, fill_color=C["dark"])
    textbox(slide, bx + int(Inches(0.08)), y0 + int(Inches(0.08)),
            bw - int(Inches(0.16)), int(Inches(0.28)),
            short(bus_t, 22), size="caption", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for ti, topic in enumerate(topics[:6]):
        ty = y0 + int(Inches(0.48)) + ti * int(Inches(0.76))
        shape_rect(slide, bx + int(Inches(0.12)), ty, bw - int(Inches(0.24)), int(Inches(0.62)),
                   fill_color=_lighter(C["dark"], 60), line_color=C["secondary"])
        textbox(slide, bx + int(Inches(0.16)), ty + int(Inches(0.12)),
                bw - int(Inches(0.32)), int(Inches(0.36)),
                short(topic, 24), size="caption", color=C["secondary"], align=PP_ALIGN.CENTER)
    # consumers
    for i, con in enumerate(conss[:5]):
        col = P[(i + 4) % len(P)];  lit = _lighter(col)
        cy2 = y0 + int(Inches(0.2)) + i * (box_h + g)
        shape_rect(slide, cx, cy2, cw, box_h, fill_color=lit, line_color=C["line"])
        textbox(slide, cx + int(Inches(0.06)), cy2 + box_h // 2 - int(Inches(0.12)),
                cw - int(Inches(0.12)), int(Inches(0.24)),
                short(con, 22), size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
        _hline(slide, bx + bw, cy2 + box_h // 2, cx - (bx + bw), C["primary"], 0.06)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 13: Bounded Context ──────────────────────────────────────────────
# AA-04 Bounded Context, DA-04 Data Domain, TA-05 Container Orchestration

_BCTX_DEF = {
    "contexts": [
        {"name": "Order Context",     "items": ["Order", "OrderLine", "Cart"],   "color": 0},
        {"name": "Inventory Context", "items": ["Product", "SKU", "Stock"],       "color": 1},
        {"name": "User Context",      "items": ["Customer", "Account", "Auth"],   "color": 2},
        {"name": "Payment Context",   "items": ["Invoice","Transaction","Refund"], "color": 3},
    ],
    "relations": [
        {"from": "Order Context",     "to": "Inventory Context", "type": "Customer-Supplier"},
        {"from": "Order Context",     "to": "User Context",      "type": "Partnership"},
        {"from": "Order Context",     "to": "Payment Context",   "type": "Conformist"},
    ],
}


def render_bounded_context(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Bounded Context', 'Domain boundaries and relationships', tag, C, P, slide, region, th_margin=0.3)
    c     = data.get("content", {})
    note  = c.get("note", "")
    d     = defaults or _BCTX_DEF
    ctxs  = c.get("contexts",  d["contexts"])
    rels  = c.get("relations",  d.get("relations", []))
    n     = len(ctxs)
    ncols = min(n, 3);  nrows = (n + ncols - 1) // ncols

    g  = int(Inches(0.2))
    cw = int((tw - g * (ncols - 1)) / ncols)
    ch = int((th - g * (nrows - 1)) / nrows)
    name_to_pos = {}
    for k, ctx_item in enumerate(ctxs[:6]):
        r = k // ncols;  col_idx = k % ncols
        cx = x0 + col_idx * (cw + g)
        cy = y0 + r * (ch + g)
        col = P[int(ctx_item.get("color", k)) % len(P)]
        lit = _lighter(col, 115)
        shape_rect(slide, cx, cy, cw, ch, fill_color=lit, line_color=col)
        shape_rect(slide, cx, cy, cw, int(Inches(0.36)), fill_color=col)
        textbox(slide, cx + int(Inches(0.08)), cy + int(Inches(0.06)),
                cw - int(Inches(0.16)), int(Inches(0.24)),
                short(ctx_item.get("name", ""), 26), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        for ii, item in enumerate(list(ctx_item.get("items", []))[:5]):
            textbox(slide, cx + int(Inches(0.1)), cy + int(Inches(0.42 + ii * 0.38)),
                    cw - int(Inches(0.2)), int(Inches(0.34)),
                    f"· {short(item, 24)}", size="caption", color=C["text"])
        name_to_pos[ctx_item.get("name", "")] = (cx + cw // 2, cy + ch // 2)
    for rel in rels[:6]:
        sp = name_to_pos.get(rel.get("from"))
        ep = name_to_pos.get(rel.get("to"))
        if sp and ep:
            sx, sy = sp;  dx, dy = ep
            if abs(sx - dx) >= abs(sy - dy):
                _hline(slide, min(sx, dx), sy, abs(dx - sx), C["dark"], 0.04)
            else:
                _vline(slide, sx, min(sy, dy), abs(dy - sy), C["dark"], 0.04)
            lbl = str(rel.get("type", ""))
            if should_render(lbl):
                textbox(slide, (sx + dx) // 2 - int(Inches(0.6)), (sy + dy) // 2 - int(Inches(0.14)),
                        int(Inches(1.2)), int(Inches(0.2)), short(lbl, 18),
                        size="micro", color=C["dark"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 14: ER Diagram ────────────────────────────────────────────────────
# DA-01 Conceptual Data Model, DA-02 Logical Data Model

_ER_DEF = {
    "entities": [
        {"name": "Customer",  "attrs": ["id PK","name","email"],     "x": 0.08, "y": 0.15},
        {"name": "Order",     "attrs": ["id PK","date","total"],      "x": 0.08, "y": 0.65},
        {"name": "Product",   "attrs": ["id PK","name","price"],      "x": 0.55, "y": 0.15},
        {"name": "OrderLine", "attrs": ["order_id FK","product_id FK","qty"], "x": 0.55, "y": 0.65},
    ],
    "relations": [
        {"from": "Customer",  "to": "Order",     "label": "1..* places"},
        {"from": "Order",     "to": "OrderLine", "label": "1..* contains"},
        {"from": "Product",   "to": "OrderLine", "label": "1..* in"},
    ],
}


def render_er_diagram(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'ER Diagram', 'Entity-relationship conceptual model', tag, C, P, slide, region, th_margin=0.3)
    c       = data.get("content", {})
    note    = c.get("note", "")
    d       = defaults or _ER_DEF
    entities = c.get("entities", d["entities"])
    relations = c.get("relations", d.get("relations", []))

    ew = int(Inches(2.2));  eh_base = int(Inches(0.34))
    pos = {}
    for k, ent in enumerate(entities[:8]):
        nx = x0 + int(float(ent.get("x", 0.1)) * tw)
        ny = y0 + int(float(ent.get("y", 0.1)) * th)
        attrs = list(ent.get("attrs", []))[:5]
        eh    = eh_base + len(attrs) * int(Inches(0.28))
        col   = P[k % len(P)];  lit = _lighter(col)
        shape_rect(slide, nx, ny, ew, eh, fill_color=lit, line_color=col)
        shape_rect(slide, nx, ny, ew, eh_base, fill_color=col)
        textbox(slide, nx + int(Inches(0.06)), ny + int(Inches(0.05)),
                ew - int(Inches(0.12)), int(Inches(0.24)),
                short(ent.get("name", ""), 20), size="caption", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)
        for ai, attr in enumerate(attrs):
            textbox(slide, nx + int(Inches(0.08)), ny + eh_base + ai * int(Inches(0.28)) + int(Inches(0.04)),
                    ew - int(Inches(0.16)), int(Inches(0.22)),
                    short(attr, 22), size="caption", color=C["text"])
        pos[ent.get("name", str(k))] = (nx + ew // 2, ny + eh // 2, nx, ny, ew, eh)
    for rel in relations[:8]:
        sp = pos.get(rel.get("from"))
        ep = pos.get(rel.get("to"))
        if not sp or not ep:
            continue
        sx, sy = sp[0], sp[1];  dx, dy = ep[0], ep[1]
        if abs(sx - dx) >= abs(sy - dy):
            _hline(slide, min(sx, dx), sy, abs(dx - sx), C["primary"], 0.04)
            if sy != dy:
                _vline(slide, dx, min(sy, dy), abs(dy - sy), C["primary"], 0.04)
        else:
            _vline(slide, sx, min(sy, dy), abs(dy - sy), C["primary"], 0.04)
            if sx != dx:
                _hline(slide, min(sx, dx), dy, abs(dx - sx), C["primary"], 0.04)
        lbl = str(rel.get("label", ""))
        if should_render(lbl):
            textbox(slide, (sx + dx) // 2 - int(Inches(0.5)), (sy + dy) // 2 - int(Inches(0.12)),
                    int(Inches(1.0)), int(Inches(0.2)), short(lbl, 16),
                    size="micro", color=C["text"], align=PP_ALIGN.CENTER)
    if fp: _footer(slide, note, C)
    return slide


# ─── Pattern 15: Data Lineage ─────────────────────────────────────────────────
# DA-07 Data Lineage

_LINEAGE_DEF = {
    "sources":    ["CRM System",    "ERP System",  "Web Logs",     "IoT Sensors"],
    "transforms": ["ETL Pipeline",  "Data Cleanse","Aggregation",  "ML Features"],
    "targets":    ["Data Warehouse","Analytics Db","ML Platform",  "Reports"],
}


def render_data_lineage(ctx, data, tag, defaults=None, slide=None, region=None):
    C = _C(ctx)
    P = ctx.palette
    slide, x0, y0, tw, th, fp = _canvas(
        ctx, data, 'Data Lineage', 'Source → Transform → Target flow', tag, C, P, slide, region, th_margin=0.28)
    c      = data.get("content", {})
    note   = c.get("note", "")
    d      = defaults or _LINEAGE_DEF
    sources    = c.get("sources",    d["sources"])
    transforms = c.get("transforms", d["transforms"])
    targets    = c.get("targets",    d["targets"])

    aw = int(Inches(0.4))
    cw = int((tw - aw * 2) / 3)
    bh = int(Inches(0.56));  g = int(Inches(0.14))

    def _col(slide, items, cx, label, col):
        shape_rect(slide, cx, y0, cw, int(Inches(0.36)), fill_color=col)
        textbox(slide, cx + int(Inches(0.06)), y0 + int(Inches(0.05)),
                cw - int(Inches(0.12)), int(Inches(0.26)),
                label, size="caption", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        lit = _lighter(col)
        for k, item in enumerate(items[:6]):
            by2 = y0 + int(Inches(0.44)) + k * (bh + g)
            shape_rect(slide, cx, by2, cw, bh, fill_color=lit, line_color=C["line"])
            textbox(slide, cx + int(Inches(0.08)), by2 + bh // 2 - int(Inches(0.12)),
                    cw - int(Inches(0.16)), int(Inches(0.26)),
                    short(item, 24), size="label", color=C["text"], align=PP_ALIGN.CENTER)
        return y0 + int(Inches(0.44)), k

    _col(slide, sources,    x0,                    "Sources",    P[0])
    _col(slide, transforms, x0 + cw + aw,          "Transforms", P[2])
    _col(slide, targets,    x0 + 2 * cw + 2 * aw,  "Targets",    P[1])
    # arrows between columns
    n_max = max(len(sources), len(transforms), len(targets), 1)
    for k in range(min(n_max, 6)):
        my = y0 + int(Inches(0.44)) + k * (bh + g) + bh // 2
        _hline(slide, x0 + cw, my, aw, C["primary"], 0.12)
        _hline(slide, x0 + 2 * cw + aw, my, aw, C["primary"], 0.12)
    if fp: _footer(slide, note, C)
    return slide


# ─── Legacy: Generic Card Grid (backward compat) ──────────────────────────────

def render_generic_slide(ctx, data, default_title, default_subtitle, domain_tag):
    C = _C(ctx)
    P = ctx.palette
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)

    header(slide, data.get("title", default_title))
    set_subtitle(ctx, slide, data.get("subtitle", default_subtitle), C)

    content = data.get("content", {})

    shape_rect(
        slide,
        int(Inches(0.55)),
        int(Inches(1.15)),
        int(Inches(1.3)),
        int(Inches(0.28)),
        fill_color=C["dark"],
    )
    textbox(
        slide,
        int(Inches(0.55)),
        int(Inches(1.18)),
        int(Inches(1.3)),
        int(Inches(0.2)),
        domain_tag,
        size="label",
        bold=True,
        color=C["white"],
        align=PP_ALIGN.CENTER,
    )

    cards = content.get("cards", [])[:6]
    if not cards:
        cards = [
            {
                "title": "Scope",
                "bullets": [
                    content.get(
                        "summary", "Architecture scope and key relationships"
                    )
                ],
            },
            {
                "title": "Key Elements",
                "bullets": [
                    "Actors / Systems / Domains",
                    "Flows / Dependencies / Ownership",
                ],
            },
            {
                "title": "Decision Focus",
                "bullets": [
                    content.get(
                        "focus",
                        "Prioritize design trade-offs and governance decisions",
                    )
                ],
            },
        ]

    left = int(Inches(0.55))
    top = int(Inches(1.55))
    gap_x = int(Inches(0.16))
    gap_y = int(Inches(0.18))
    col_w = int(Inches(2.7))
    row_h = int(Inches(1.25))

    for i, card in enumerate(cards):
        r = i // 3
        c = i % 3
        x = left + c * (col_w + gap_x)
        y = top + r * (row_h + gap_y)

        shape_rect(
            slide,
            x,
            y,
            col_w,
            row_h,
            fill_color=C["light"],
            line_color=C["line"],
        )
        shape_rect(
            slide,
            x,
            y,
            col_w,
            int(Inches(0.26)),
            fill_color=C["secondary"],
        )
        textbox(
            slide,
            x + int(Inches(0.05)),
            y + int(Inches(0.05)),
            col_w - int(Inches(0.1)),
            int(Inches(0.14)),
            short(card.get("title", "Module"), 28),
            size="label",
            bold=True,
            color=C["text"],
        )

        bullets = card.get("bullets", [])[:4]
        for bi, b in enumerate(bullets):
            textbox(
                slide,
                x + int(Inches(0.07)),
                y + int(Inches(0.34 + bi * 0.2)),
                col_w - int(Inches(0.14)),
                int(Inches(0.16)),
                f"- {short(b, 42)}",
                size="caption",
                color=C["text"],
            )

    note = content.get(
        "note", "Connectors represent semantic relationships only; no decorative lines."
    )
    textbox(
        slide,
        int(Inches(0.55)),
        int(Inches(5.65)),
        int(Inches(8.4)),
        int(Inches(0.2)),
        short(note, 120),
        size="caption",
        color=C["gray"],
        align=PP_ALIGN.RIGHT,
    )

    return slide
