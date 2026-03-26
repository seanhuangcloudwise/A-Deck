"""RA-05 Dependency and critical path."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))
from pptx_lib import header, layout_by_names
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from renderer_utils import shape_rect, textbox

def set_subtitle(ctx, slide, text, gray_color=None):
    subtitle_ph = next((s for s in slide.shapes if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1), None)
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def load_slide(ctx, data):
    C = ctx.colors
    _CRITICAL = C["accent6"]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-05 Dependency Critical Path"))
    set_subtitle(ctx, slide, data.get("subtitle", "依赖与关键路径图"), C["gray"])

    content = data.get("content", {})
    nodes = content.get("nodes", [])
    edges = content.get("edges", [])

    # Draw nodes
    pos = {}
    for n in nodes[:12]:
        x = int(Inches(float(n.get("x", 1.0))))
        y = int(Inches(float(n.get("y", 2.0))))
        w = int(Inches(1.3))
        h = int(Inches(0.4))
        is_critical = bool(n.get("critical", False))
        shape_rect(slide, x, y, w, h, fill_color=_CRITICAL if is_critical else C["dark"])
        textbox(slide, x + int(Inches(0.03)), y + int(Inches(0.09)), w - int(Inches(0.06)), int(Inches(0.2)), n.get("label", ""), size="label", color=C["white"])
        pos[n.get("id", "")] = (x, y, w, h)

    critical_count = 0
    # Draw semantic arrows with text markers
    for e in edges[:20]:
        src = pos.get(e.get("from"))
        dst = pos.get(e.get("to"))
        if not src or not dst:
            continue
        sx = src[0] + src[2]
        sy = src[1] + int(src[3] / 2)
        dx = dst[0]
        dy = dst[1] + int(dst[3] / 2)
        mx = int((sx + dx) / 2)
        my = int((sy + dy) / 2)
        is_critical = bool(e.get("critical"))
        if is_critical:
            critical_count += 1
        line_color = _CRITICAL if is_critical else C["line"]
        line_th = int(Inches(0.015))
        if sx != dx:
            lx = min(sx, dx)
            lw = max(line_th, abs(dx - sx))
            shape_rect(slide, lx, sy - int(line_th / 2), lw, line_th, fill_color=line_color)
        if sy != dy:
            ly = min(sy, dy)
            lh = max(line_th, abs(dy - sy))
            shape_rect(slide, dx - int(line_th / 2), ly, line_th, lh, fill_color=line_color)
        textbox(slide, mx - int(Inches(0.08)), my - int(Inches(0.08)), int(Inches(0.16)), int(Inches(0.16)), "→", size="body", color=_CRITICAL if is_critical else C["line"])

    # Legend + critical path summary
    ly = int(Inches(5.35))
    shape_rect(slide, int(Inches(0.55)), ly + int(Inches(0.01)), int(Inches(0.18)), int(Inches(0.08)), fill_color=_CRITICAL)
    textbox(slide, int(Inches(0.78)), ly - int(Inches(0.01)), int(Inches(1.0)), int(Inches(0.14)), "Critical", size="caption", color=C["text"])
    shape_rect(slide, int(Inches(1.72)), ly + int(Inches(0.01)), int(Inches(0.18)), int(Inches(0.08)), fill_color=C["dark"])
    textbox(slide, int(Inches(1.95)), ly - int(Inches(0.01)), int(Inches(1.2)), int(Inches(0.14)), "Node", size="caption", color=C["text"])

    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Critical path highlighted in red") + f" | Critical edges: {critical_count}", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
