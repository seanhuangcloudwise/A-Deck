"""GM-10 ROI Business Case — 3-zone flow: Investment → Benefits → Outcome."""

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
        (
            s
            for s in slide.shapes
            if getattr(s, "is_placeholder", False)
            and s.placeholder_format.idx == 1
        ),
        None,
    )
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    content = data["content"]
    top = Inches(1.3)

    # --- Zone 1: Investment ---
    inv = content.get("investment", {})
    inv_x = Inches(0.5)
    inv_w = int(Inches(2.2))
    zone_h = int(Inches(3.2))

    shape_rect(slide, int(inv_x), int(top), inv_w, zone_h,
                fill_color=C["light"], line_color=C["line"])
    textbox(slide, int(inv_x + Inches(0.1)), int(top + Inches(0.1)),
            int(inv_w - Inches(0.2)), int(Inches(0.35)),
            inv.get("label", "Investment"), size="body", bold=True,
            color=C["dark"], align=PP_ALIGN.CENTER)

    items = inv.get("items", [])
    for ii, item in enumerate(items):
        iy = int(top + Inches(0.55) + ii * Inches(0.35))
        textbox(slide, int(inv_x + Inches(0.15)), iy,
                int(inv_w - Inches(0.3)), int(Inches(0.3)),
                f"• {item}", size="caption", color=C["text"])

    # Arrow 1
    textbox(slide, int(inv_x + inv_w + Inches(0.02)), int(top + zone_h / 2 - Inches(0.15)),
            int(Inches(0.35)), int(Inches(0.3)), "→",
            size="h2", bold=True, color=C["primary"], align=PP_ALIGN.CENTER)

    # --- Zone 2: Benefits ---
    benefits = content.get("benefits", [])
    ben_x = int(Inches(3.1))
    ben_total_w = Inches(3.3)
    num_ben = max(len(benefits), 1)
    ben_gap = Inches(0.1)
    ben_card_w = int((ben_total_w - (num_ben - 1) * ben_gap) / num_ben)

    for bi, b in enumerate(benefits):
        bx = int(ben_x + bi * (ben_card_w + ben_gap))
        shape_rect(slide, bx, int(top), ben_card_w, zone_h,
                    fill_color=C["secondary"])
        textbox(slide, int(bx + Inches(0.05)), int(top + Inches(0.1)),
                int(ben_card_w - Inches(0.1)), int(Inches(0.3)),
                b.get("label", ""), size="caption", bold=True,
                color=C["text"], align=PP_ALIGN.CENTER)
        textbox(slide, int(bx + Inches(0.05)), int(top + Inches(0.5)),
                int(ben_card_w - Inches(0.1)), int(Inches(0.6)),
                b.get("value", ""), size="h2", bold=True,
                color=C["primary"], align=PP_ALIGN.CENTER)
        textbox(slide, int(bx + Inches(0.05)), int(top + Inches(1.2)),
                int(ben_card_w - Inches(0.1)), int(Inches(1.5)),
                b.get("desc", ""), size="label", color=C["text"])

    # Arrow 2
    textbox(slide, int(ben_x + ben_total_w + Inches(0.02)),
            int(top + zone_h / 2 - Inches(0.15)),
            int(Inches(0.35)), int(Inches(0.3)), "→",
            size="h2", bold=True, color=C["primary"], align=PP_ALIGN.CENTER)

    # --- Zone 3: Outcome ---
    outcome = content.get("outcome", {})
    out_x = int(Inches(6.8))
    out_w = int(Inches(2.2))

    shape_rect(slide, out_x, int(top), out_w, zone_h,
                fill_color=C["dark"])
    textbox(slide, int(out_x + Inches(0.1)), int(top + Inches(0.3)),
            int(out_w - Inches(0.2)), int(Inches(0.5)),
            "ROI", size="body", bold=True, color=C["gray"],
            align=PP_ALIGN.CENTER)
    textbox(slide, int(out_x + Inches(0.1)), int(top + Inches(0.8)),
            int(out_w - Inches(0.2)), int(Inches(0.8)),
            outcome.get("roi", ""),
            size=36, bold=True, color=C["primary"], align=PP_ALIGN.CENTER)
    textbox(slide, int(out_x + Inches(0.1)), int(top + Inches(1.8)),
            int(out_w - Inches(0.2)), int(Inches(0.4)),
            f"Payback: {outcome.get('payback', '')}",
            size="label", color=C["white"], align=PP_ALIGN.CENTER)

    return slide
