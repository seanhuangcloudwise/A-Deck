"""GM-03 Before/After Comparison — Two side-by-side panels with cards."""

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


def _render_panel(slide, x, y, w, h, panel_data, is_after, colors):
    """Render a Before or After panel with cards."""
    bg_color = colors["primary"] if is_after else colors["gray"]
    header_color = colors["white"] if is_after else colors["text"]
    card_bg = colors["secondary"] if is_after else colors["light"]

    shape_rect(slide, int(x), int(y), int(w), int(Inches(0.4)), fill_color=bg_color)
    textbox(
        slide,
        int(x + Inches(0.1)),
        int(y + Inches(0.05)),
        int(w - Inches(0.2)),
        int(Inches(0.3)),
        panel_data.get("label", ""),
        size="h3",
        bold=True,
        color=header_color,
        align=PP_ALIGN.CENTER,
    )

    cards = panel_data.get("cards", [])
    card_top = int(y + Inches(0.5))
    card_h = Inches(0.7)
    card_gap = Inches(0.1)

    for i, card in enumerate(cards):
        cy = int(card_top + i * (card_h + card_gap))
        shape_rect(
            slide, int(x + Inches(0.1)), cy, int(w - Inches(0.2)), int(card_h),
            fill_color=card_bg,
        )

        title_text = card.get("title", "")
        delta = card.get("delta", "")
        display = f"{title_text}  {delta}" if delta else title_text
        textbox(
            slide,
            int(x + Inches(0.2)),
            cy,
            int(w - Inches(0.4)),
            int(Inches(0.3)),
            display,
            size="label",
            bold=True,
            color=colors["text"],
        )
        textbox(
            slide,
            int(x + Inches(0.2)),
            int(cy + Inches(0.28)),
            int(w - Inches(0.4)),
            int(Inches(0.35)),
            card.get("desc", ""),
            size="label",
            color=colors["text"],
        )


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    content = data["content"]
    panel_w = Inches(3.9)
    panel_h = Inches(3.8)
    panel_y = Inches(1.2)

    _render_panel(slide, Inches(0.5), panel_y, panel_w, panel_h, content["before"], False, C)

    arrow_x = int(Inches(0.5) + panel_w + Inches(0.05))
    textbox(
        slide,
        arrow_x,
        int(panel_y + panel_h / 2 - Inches(0.2)),
        int(Inches(0.5)),
        int(Inches(0.4)),
        "→",
        size="title",
        bold=True,
        color=C["primary"],
        align=PP_ALIGN.CENTER,
    )

    after_x = int(Inches(0.5) + panel_w + Inches(0.6))
    _render_panel(slide, after_x, panel_y, panel_w, panel_h, content["after"], True, C)

    return slide
