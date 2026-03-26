"""GM-32: Persona value map table."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, shape_rect

def set_subtitle(ctx, slide, text, gray_color=None):
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
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def _fallback_personas(content):
    personas = []
    for sec in content.get("sections", [])[:6]:
        items = sec.get("items", [])
        personas.append(
            {
                "persona": sec.get("title", "Persona"),
                "pain": items[0] if len(items) > 0 else "关键痛点",
                "value": items[1] if len(items) > 1 else "价值主张",
                "kpi": "效率提升",
                "proof": items[2] if len(items) > 2 else "案例证明",
                "influence": "medium",
                "primary": False,
            }
        )
    return personas


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-32 Persona Value Map"))
    set_subtitle(ctx, slide, data.get("subtitle", "多角色价值框架"), C["gray"])

    content = data.get("content", {})
    personas = content.get("personas") or _fallback_personas(content)
    personas = personas[:6]

    left = Inches(0.5)
    top = Inches(1.15)
    total_w = Inches(8.5)
    headers = ["Persona", "Pain", "Value", "KPI", "Proof"]
    widths = [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.6), Inches(1.8)]
    head_h = Inches(0.38)
    row_h = Inches(0.62)

    x = left
    for i, h in enumerate(headers):
        shape_rect(slide, x, top, widths[i], head_h, fill_color=C["dark"])
        textbox(slide, x, top + Inches(0.03), widths[i], Inches(0.26), h, size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        x += widths[i]

    for r_i, p in enumerate(personas):
        y = top + head_h + r_i * row_h
        bg = C["white"] if r_i % 2 == 0 else C["light"]
        if p.get("primary"):
            shape_rect(slide, left - Inches(0.04), y, Inches(0.03), row_h, fill_color=C["primary"])

        vals = [p.get("persona", ""), p.get("pain", ""), p.get("value", ""), p.get("kpi", ""), p.get("proof", "")]
        x = left
        for c_i, val in enumerate(vals):
            shape_rect(slide, x, y, widths[c_i], row_h, fill_color=bg, line_color=C["line"])
            textbox(slide, x + Inches(0.03), y + Inches(0.03), widths[c_i] - Inches(0.06), row_h - Inches(0.06), val, size="label", color=C["text"])
            x += widths[c_i]

    return slide
