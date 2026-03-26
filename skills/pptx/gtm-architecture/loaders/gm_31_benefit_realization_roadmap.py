"""GM-31: Benefit realization roadmap timeline."""
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


def _fallback_phases(content):
    sections = content.get("sections", [])
    phases = []
    for sec in sections[:4]:
        items = sec.get("items", [])
        phases.append(
            {
                "name": sec.get("title", "Phase"),
                "owner": "CS/PMO",
                "kpi": items[1] if len(items) > 1 else "关键指标",
                "benefit": items[0] if items else "价值里程碑",
                "confidence": "Medium",
            }
        )
    return phases


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-31 Benefit Realization Roadmap"))
    set_subtitle(ctx, slide, data.get("subtitle", "分阶段价值交付"), C["gray"])

    content = data.get("content", {})
    phases = content.get("phases") or _fallback_phases(content)
    phases = phases[:4]

    timeline_left = Inches(0.55)
    timeline_top = Inches(1.25)
    timeline_w = Inches(8.35)
    shape_rect(slide, timeline_left, timeline_top, timeline_w, Inches(0.03), fill_color=C["gray"])

    phase_w = Inches(2.0)
    gap = Inches(0.12)
    for i, ph in enumerate(phases):
        x = timeline_left + i * (phase_w + gap)
        # node
        shape_rect(slide, x + phase_w / 2 - Inches(0.06), timeline_top - Inches(0.06), Inches(0.12), Inches(0.12), fill_color=C["primary"])

        # header
        shape_rect(slide, x, Inches(1.45), phase_w, Inches(0.35), fill_color=C["dark"])
        textbox(slide, x, Inches(1.48), phase_w, Inches(0.25), ph.get("name", "Phase"), size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)

        # body
        shape_rect(slide, x, Inches(1.82), phase_w, Inches(2.95), fill_color=C["light"], line_color=C["line"])
        textbox(slide, x + Inches(0.07), Inches(1.92), phase_w - Inches(0.14), Inches(0.25), f"Owner: {ph.get('owner', 'N/A')}", size="label", color=C["text"])
        textbox(slide, x + Inches(0.07), Inches(2.2), phase_w - Inches(0.14), Inches(1.0), ph.get("benefit", ""), size="label", bold=True, color=C["text"])
        textbox(slide, x + Inches(0.07), Inches(3.25), phase_w - Inches(0.14), Inches(0.6), ph.get("kpi", ""), size="label", color=C["dark"])

        conf = ph.get("confidence", "Medium")
        c_color = C["primary"] if conf.lower() == "high" else (C["dark"] if conf.lower() == "medium" else C["gray"])
        shape_rect(slide, x + Inches(0.07), Inches(4.25), Inches(0.85), Inches(0.22), fill_color=c_color)
        textbox(slide, x + Inches(0.07), Inches(4.26), Inches(0.85), Inches(0.2), f"Conf: {conf}", size="caption", color=C["white"], align=PP_ALIGN.CENTER)

    return slide
