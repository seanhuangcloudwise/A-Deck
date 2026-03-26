"""RA-10 Scenario investment view."""

import re
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


def parse_amount(value):
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([KMB])?", value.replace(",", "").upper())
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2) or ""
    if unit == "K":
        return num / 1000.0
    if unit == "B":
        return num * 1000.0
    return num


def format_m(value):
    return f"${value:.1f}M"


def load_slide(ctx, data):
    C = ctx.colors
    _SCENARIO = {"base": C["primary"], "conservative": C["gray"], "aggressive": C["secondary"]}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "RA-10 Scenario Investment"))
    set_subtitle(ctx, slide, data.get("subtitle", "场景化投资视图"), C["gray"])

    content = data.get("content", {})
    scenarios = content.get("scenarios", ["Conservative", "Base", "Aggressive"])
    initiatives = content.get("initiatives", [])

    left = int(Inches(0.6))
    top = int(Inches(1.2))
    name_w = int(Inches(2.4))
    col_w = int(Inches(2.0))
    head_h = int(Inches(0.38))
    row_h = int(Inches(0.45))

    shape_rect(slide, left, top, name_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top + int(Inches(0.03)), name_w, int(Inches(0.22)), "Initiative", size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)

    current_idx = int(content.get("current_scenario_index", 1))
    col_totals = [0.0, 0.0, 0.0]
    for i, sc in enumerate(scenarios[:3]):
        x = left + name_w + i * col_w
        color = _SCENARIO["conservative"] if i == 0 else (_SCENARIO["base"] if i == 1 else _SCENARIO["aggressive"])
        shape_rect(slide, x, top, col_w, head_h, fill_color=color)
        label = f"{sc} (Current)" if i == current_idx else sc
        textbox(slide, x, top + int(Inches(0.03)), col_w, int(Inches(0.22)), label, size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
        if i == current_idx:
            shape_rect(slide, x, top, col_w, int(Inches(4.8)), fill_color=None, line_color=C["text"], line_width=2)

    for r_i, init in enumerate(initiatives[:9]):
        y = top + head_h + r_i * row_h
        bg = C["white"] if r_i % 2 == 0 else C["light"]
        shape_rect(slide, left, y, name_w, row_h, fill_color=bg, line_color=C["line"])
        textbox(slide, left + int(Inches(0.05)), y + int(Inches(0.06)), name_w - int(Inches(0.1)), int(Inches(0.2)), init.get("name", ""), size="label", color=C["text"])
        vals = init.get("values", [])
        for i in range(3):
            x = left + name_w + i * col_w
            v = vals[i] if i < len(vals) else "-"
            parsed = parse_amount(v)
            if parsed is not None:
                col_totals[i] += parsed
            shape_rect(slide, x, y, col_w, row_h, fill_color=bg, line_color=C["line"])
            textbox(slide, x, y + int(Inches(0.06)), col_w, int(Inches(0.2)), str(v), size="label", color=C["text"], align=PP_ALIGN.CENTER)

    # Totals row
    ty = top + head_h + len(initiatives[:9]) * row_h
    shape_rect(slide, left, ty, name_w, row_h, fill_color=C["dark"])
    textbox(slide, left, ty + int(Inches(0.06)), name_w, int(Inches(0.2)), "Total", size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    for i in range(3):
        x = left + name_w + i * col_w
        shape_rect(slide, x, ty, col_w, row_h, fill_color=C["light"], line_color=C["line"])
        tv = format_m(col_totals[i]) if col_totals[i] != 0 else "-"
        textbox(slide, x, ty + int(Inches(0.06)), col_w, int(Inches(0.2)), tv, size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)

    current_name = scenarios[current_idx] if 0 <= current_idx < len(scenarios[:3]) else "Base"
    textbox(slide, int(Inches(0.55)), int(Inches(5.65)), int(Inches(8.4)), int(Inches(0.2)), content.get("note", "Scenarios: Conservative / Base / Aggressive") + f" | Current: {current_name} | Trigger: MAU growth > 30% => Aggressive", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
