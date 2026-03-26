"""RA-09 Governance gate flow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))
from pptx_lib import header, layout_by_names
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from renderer_utils import resolve_font_size, shape_rect, textbox

def set_subtitle(ctx, slide, text, gray_color=None):
    subtitle_ph = next((s for s in slide.shapes if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1), None)
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def short_text(text, limit):
    text = str(text or "")
    return text if len(text) <= limit else text[: max(1, limit - 1)] + "…"


def split_criteria(text):
    raw = str(text or "Criteria: ROI/Feasibility").strip()
    if ":" in raw:
        k, v = raw.split(":", 1)
        key = short_text(k.strip() + ":", 11)
        val = short_text(v.strip(), 14)
        return key, val
    if "/" in raw:
        parts = [p.strip() for p in raw.split("/") if p.strip()]
        if len(parts) >= 2:
            return short_text(parts[0], 11), short_text(parts[1], 14)
    return "Criteria:", short_text(raw, 14)


def textbox_nowrap(slide, left, top, width, height, text, size="label", bold=False, color=None, align=PP_ALIGN.LEFT):
    shape = slide.shapes.add_textbox(left, top, width, height)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(resolve_font_size(size))
    p.font.bold = bold
    if color:
        p.font.color.rgb = RGBColor(*color) if isinstance(color, tuple) else color
    p.alignment = align
    return shape


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-09 Governance Gate"))
    set_subtitle(ctx, slide, data.get("subtitle", "治理关口图"), C["gray"])

    content = data.get("content", {})
    stages = content.get("stages", [])[:5]

    y = int(Inches(2.3))
    stage_w = int(Inches(1.28))
    stage_h = int(Inches(0.76))
    gate_w = int(Inches(0.34))
    gate_h = int(Inches(0.44))
    gap = int(Inches(0.05))
    x = int(Inches(0.4))

    for i, st in enumerate(stages):
        shape_rect(slide, x, y, stage_w, stage_h, fill_color=C["dark"])
        textbox_nowrap(slide, x + int(Inches(0.05)), y + int(Inches(0.08)), stage_w - int(Inches(0.1)), int(Inches(0.2)), short_text(st.get("name", ""), 18), size="label", bold=True, color=C["white"])
        textbox_nowrap(slide, x + int(Inches(0.05)), y + int(Inches(0.31)), stage_w - int(Inches(0.1)), int(Inches(0.18)), short_text(st.get("owner", "Owner:TBD"), 18), size="caption", color=C["white"])
        c1, c2 = split_criteria(st.get("criteria", "Criteria: ROI/Feasibility"))
        textbox_nowrap(slide, x + int(Inches(0.05)), y + int(Inches(0.5)), stage_w - int(Inches(0.1)), int(Inches(0.1)), c1, size="micro", color=C["white"])
        textbox_nowrap(slide, x + int(Inches(0.05)), y + int(Inches(0.6)), stage_w - int(Inches(0.1)), int(Inches(0.1)), short_text(c2, 16), size="micro", color=C["white"])
        x += stage_w
        if i < len(stages) - 1:
            gx = x + int(Inches(0.03))
            gy = y + int(Inches(0.14))
            shape_rect(slide, gx, gy, gate_w, gate_h, fill_color=C["secondary"])
            textbox_nowrap(slide, gx + int(Inches(0.03)), gy + int(Inches(0.12)), gate_w - int(Inches(0.06)), int(Inches(0.2)), short_text(st.get("gate", "Go"), 8), size="micro", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
            textbox(slide, x + int(Inches(0.19)), y + int(Inches(0.63)), int(Inches(0.2)), int(Inches(0.2)), "→", size="body", color=C["gray"])
            x += gate_w + gap

    textbox(slide, int(Inches(0.55)), int(Inches(3.2)), int(Inches(8.4)), int(Inches(0.2)), content.get("raci", "RACI: Recommender=PM, Decider=CPO"), size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Gate policy: Go / Hold / Kill") + " | Decision gates highlighted in cyan", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)

    return slide
