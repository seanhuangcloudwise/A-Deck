"""GM-16 Category Creation — Legacy vs Emerging gap with product badge."""

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
    zone_h = int(Inches(3.4))

    # --- Left: Legacy blocks ---
    legacy = content.get("legacy", [])
    leg_x = Inches(0.5)
    leg_w = int(Inches(2.5))
    block_h = int(Inches(0.45))
    block_gap = int(Inches(0.1))

    textbox(slide, int(leg_x), int(top - Inches(0.3)),
            leg_w, int(Inches(0.25)),
            "Legacy Solutions", size="label", bold=True,
            color=C["gray"])

    for i, item in enumerate(legacy):
        by = int(top + i * (block_h + block_gap))
        shape_rect(slide, int(leg_x), by, leg_w, block_h,
                    fill_color=C["light"], line_color=C["line"])
        textbox(slide, int(leg_x + Inches(0.1)), by,
                int(leg_w - Inches(0.2)), block_h,
                item.get("name", ""), size="caption", color=C["text"])

    # --- Center: Gap zone ---
    gap_data = content.get("gap", {})
    gap_x = int(Inches(3.3))
    gap_w = int(Inches(3.0))

    shape_rect(slide, gap_x, int(top), gap_w, zone_h,
                fill_color=C["secondary"], line_color=C["primary"],
                line_width=2)

    textbox(slide, int(gap_x + Inches(0.15)), int(top + Inches(0.3)),
            int(gap_w - Inches(0.3)), int(Inches(0.6)),
            gap_data.get("problem", ""),
            size="label", color=C["text"], align=PP_ALIGN.CENTER)

    # Product badge
    product = content.get("product", "")
    badge_y = int(top + zone_h / 2 - Inches(0.3))
    badge_w = int(gap_w - Inches(0.5))
    shape_rect(slide, int(gap_x + Inches(0.25)), badge_y,
                badge_w, int(Inches(0.5)),
                fill_color=C["primary"])
    textbox(slide, int(gap_x + Inches(0.25)), badge_y,
            badge_w, int(Inches(0.5)),
            product, size="h3", bold=True,
            color=C["white"], align=PP_ALIGN.CENTER)

    # Category name
    cat_name = gap_data.get("category_name", "")
    textbox(slide, int(gap_x + Inches(0.15)), int(top + zone_h - Inches(0.7)),
            int(gap_w - Inches(0.3)), int(Inches(0.4)),
            cat_name, size="body", bold=True,
            color=C["dark"], align=PP_ALIGN.CENTER)

    # --- Right: Emerging needs ---
    emerging = content.get("emerging", [])
    em_x = int(Inches(6.6))
    em_w = int(Inches(2.5))

    textbox(slide, em_x, int(top - Inches(0.3)),
            em_w, int(Inches(0.25)),
            "Emerging Needs", size="label", bold=True,
            color=C["primary"])

    for i, item in enumerate(emerging):
        by = int(top + i * (block_h + block_gap))
        shape_rect(slide, em_x, by, em_w, block_h,
                    fill_color=C["secondary"])
        textbox(slide, int(em_x + Inches(0.1)), by,
                int(em_w - Inches(0.2)), block_h,
                item.get("name", ""), size="caption", color=C["text"])

    return slide
