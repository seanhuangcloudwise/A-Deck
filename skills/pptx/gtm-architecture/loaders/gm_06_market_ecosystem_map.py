"""GM-06 Market Ecosystem Map — Category grid with vendor tiles."""

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

    categories = data["content"]["categories"]
    num_cats = len(categories)
    if num_cats == 0:
        return slide

    content_left = Inches(0.5)
    content_top = Inches(1.2)
    total_w = Inches(8.5)
    col_gap = Inches(0.15)
    col_w = int((total_w - (num_cats - 1) * col_gap) / num_cats)
    header_h = int(Inches(0.4))
    tile_h = int(Inches(0.35))
    tile_gap = int(Inches(0.08))

    for ci, cat in enumerate(categories):
        cx = int(content_left + ci * (col_w + col_gap))

        shape_rect(slide, cx, int(content_top), col_w, header_h,
                    fill_color=C["dark"])
        textbox(slide, int(cx + Inches(0.05)), int(content_top + Inches(0.05)),
                int(col_w - Inches(0.1)), int(header_h - Inches(0.1)),
                cat["name"], size="caption", bold=True, color=C["white"],
                align=PP_ALIGN.CENTER)

        vendors = cat.get("vendors", [])
        for vi, v in enumerate(vendors):
            vy = int(content_top + header_h + Inches(0.1) + vi * (tile_h + tile_gap))
            is_self = v.get("is_self", False)
            bg = C["primary"] if is_self else C["light"]
            txt_color = C["white"] if is_self else C["text"]

            shape_rect(slide, int(cx + Inches(0.05)), vy,
                        int(col_w - Inches(0.1)), tile_h, fill_color=bg)
            textbox(slide, int(cx + Inches(0.1)), vy,
                    int(col_w - Inches(0.2)), tile_h,
                    v["name"], size="label", bold=is_self, color=txt_color,
                    align=PP_ALIGN.CENTER)

    return slide
