"""RA-04 Capability evolution roadmap."""

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


def color_by_level(level, level_colors):
    key = f"c{max(0, min(3, int(level)))}"
    return level_colors.get(key, level_colors["c0"])


def load_slide(ctx, data):
    C = ctx.colors
    from pptx_lib import lighter
    _c = {"c0": lighter(C["primary"], 0.95), "c1": lighter(C["primary"], 0.75), "c2": C["secondary"], "c3": C["primary"]}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-04 Capability Evolution"))
    set_subtitle(ctx, slide, data.get("subtitle", "能力演进路线图"), C["gray"])

    content = data.get("content", {})
    periods = content.get("periods", [])
    capabilities = content.get("capabilities", [])

    left = int(Inches(0.7))
    top = int(Inches(1.25))
    label_w = int(Inches(2.0))
    head_h = int(Inches(0.38))
    row_h = int(Inches(0.48))
    col_w = int(Inches(1.6))

    shape_rect(slide, left, top, label_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top + int(Inches(0.03)), label_w, int(Inches(0.22)), "Capability", size="label", bold=True, color=C["white"])

    for i, p in enumerate(periods[:4]):
        x = left + label_w + i * col_w
        shape_rect(slide, x, top, col_w, head_h, fill_color=C["dark"])
        textbox(slide, x, top + int(Inches(0.03)), col_w, int(Inches(0.22)), p, size="label", bold=True, color=C["white"])

    for r_i, cap in enumerate(capabilities[:7]):
        y = top + head_h + r_i * row_h
        shape_rect(slide, left, y, label_w, row_h, fill_color=C["light"], line_color=C["line"])
        textbox(slide, left + int(Inches(0.05)), y + int(Inches(0.06)), label_w - int(Inches(0.1)), int(Inches(0.2)), cap.get("name", ""), size="label", color=C["text"])
        for c_i, lv in enumerate(cap.get("levels", [])[:4]):
            x = left + label_w + c_i * col_w
            lvi = int(lv)
            shape_rect(slide, x, y, col_w, row_h, fill_color=color_by_level(lvi, _c), line_color=C["line"])
            textbox(slide, x, y + int(Inches(0.06)), col_w, int(Inches(0.2)), f"L{lvi}", size="label", bold=True, color=C["text"])

    # Maturity legend
    ly = int(Inches(5.3))
    for i in range(4):
        lx = int(Inches(0.7 + i * 1.0))
        shape_rect(slide, lx, ly, int(Inches(0.2)), int(Inches(0.1)), fill_color=color_by_level(i, _c), line_color=C["line"])
        textbox(slide, lx + int(Inches(0.24)), ly - int(Inches(0.02)), int(Inches(0.6)), int(Inches(0.14)), f"L{i}", size="caption", color=C["text"])

    textbox(slide, int(Inches(4.9)), ly - int(Inches(0.02)), int(Inches(1.4)), int(Inches(0.14)), "Maturity Level", size="caption", color=C["gray"])
    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Capability levels L0-L3 across roadmap periods"), size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)

    return slide
