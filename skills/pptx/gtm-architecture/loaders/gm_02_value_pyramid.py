"""GM-02 Value Pyramid — 3-tier stacked trapezoid pyramid with callouts."""

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


def _draw_trapezoid(slide, prs, left, top, width, height, fill_color):
    """Draw a trapezoid using a freeform shape."""
    from pptx.util import Emu

    specs = prs.slide_width  # just to access prs
    inset = int(width * 0.12)

    freeform = slide.shapes.build_freeform(
        int(left + inset), int(top)
    )
    freeform.add_line_to(int(left + width - inset), int(top))
    freeform.add_line_to(int(left + width), int(top + height))
    freeform.add_line_to(int(left), int(top + height))
    freeform.add_line_to(int(left + inset), int(top))

    shape = freeform.convert_to_shape()
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*fill_color)
    shape.line.fill.background()
    return shape


def load_slide(ctx, data):
    C = ctx.colors
    TIER_COLORS = [C["dark"], C["primary"], C["secondary"]]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    tiers = data["content"]["tiers"]
    num_tiers = len(tiers)

    pyramid_left = Inches(0.8)
    pyramid_top = Inches(1.3)
    pyramid_width = Inches(3.8)
    tier_height = Inches(1.1)
    tier_gap = Inches(0.08)

    for i, tier in enumerate(tiers):
        idx = i
        y = int(pyramid_top + idx * (tier_height + tier_gap))
        inset_factor = idx * 0.15
        inset = int(pyramid_width * inset_factor)
        t_left = int(pyramid_left + inset)
        t_width = int(pyramid_width - 2 * inset)

        color = TIER_COLORS[i % len(TIER_COLORS)]

        shape_rect(
            slide,
            t_left,
            y,
            t_width,
            int(tier_height),
            fill_color=color,
        )

        textbox(
            slide,
            int(t_left + Inches(0.15)),
            int(y + Inches(0.15)),
            int(t_width - Inches(0.3)),
            int(tier_height - Inches(0.3)),
            tier["label"],
            size="body",
            bold=True,
            color=C["white"],
            align=PP_ALIGN.CENTER,
        )

        callouts = tier.get("callouts", [])
        callout_x = int(pyramid_left + pyramid_width + Inches(0.5))
        callout_y = int(y + Inches(0.05))
        callout_text = "\n".join(f"• {c}" for c in callouts)
        if callout_text:
            textbox(
                slide,
                callout_x,
                callout_y,
                int(Inches(3.8)),
                int(tier_height),
                callout_text,
                size="caption",
                color=C["text"],
            )

    return slide
