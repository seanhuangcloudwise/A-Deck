"""GM-04 Market Positioning Matrix — 2x2 quadrant with vendor dots."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
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

    grid_left = Inches(1.5)
    grid_top = Inches(1.5)
    grid_w = Inches(5.5)
    grid_h = Inches(3.5)

    quadrants = content.get("quadrants", ["", "", "", ""])
    quad_w = int(grid_w / 2)
    quad_h = int(grid_h / 2)
    quad_colors = [C["light"], C["light"], C["light"], C["light"]]

    positions = [
        (int(grid_left), int(grid_top)),
        (int(grid_left + quad_w), int(grid_top)),
        (int(grid_left), int(grid_top + quad_h)),
        (int(grid_left + quad_w), int(grid_top + quad_h)),
    ]
    for i, (qx, qy) in enumerate(positions):
        shape_rect(slide, qx, qy, quad_w, quad_h, fill_color=C["light"],
                    line_color=C["line"], line_width=1)
        if i < len(quadrants):
            textbox(
                slide, int(qx + Inches(0.1)), int(qy + Inches(0.1)),
                int(quad_w - Inches(0.2)), int(Inches(0.3)),
                quadrants[i], size="label", color=C["gray"], align=PP_ALIGN.CENTER,
            )

    x_axis = content.get("x_axis", ["Low", "High"])
    y_axis = content.get("y_axis", ["Low", "High"])
    x_label = content.get("x_label", "")
    y_label = content.get("y_label", "")

    textbox(slide, int(grid_left), int(grid_top + grid_h + Inches(0.05)),
            int(grid_w), int(Inches(0.3)), x_label,
            size="label", bold=True, color=C["text"], align=PP_ALIGN.CENTER)
    textbox(slide, int(grid_left - Inches(0.1)), int(grid_top + grid_h + Inches(0.05)),
            int(Inches(0.8)), int(Inches(0.25)), x_axis[0],
            size="label", color=C["gray"])
    textbox(slide, int(grid_left + grid_w - Inches(0.8)), int(grid_top + grid_h + Inches(0.05)),
            int(Inches(0.8)), int(Inches(0.25)), x_axis[1],
            size="label", color=C["gray"], align=PP_ALIGN.RIGHT)

    # Y-axis label (vertical text not trivially supported, use horizontal)
    textbox(slide, int(grid_left - Inches(1.0)), int(grid_top + grid_h / 2 - Inches(0.15)),
            int(Inches(0.9)), int(Inches(0.3)), y_label,
            size="label", bold=True, color=C["text"], align=PP_ALIGN.RIGHT)
    textbox(slide, int(grid_left - Inches(0.6)), int(grid_top + grid_h - Inches(0.3)),
            int(Inches(0.5)), int(Inches(0.25)), y_axis[0],
            size="label", color=C["gray"], align=PP_ALIGN.RIGHT)
    textbox(slide, int(grid_left - Inches(0.6)), int(grid_top),
            int(Inches(0.5)), int(Inches(0.25)), y_axis[1],
            size="label", color=C["gray"], align=PP_ALIGN.RIGHT)

    for vendor in content.get("vendors", []):
        vx = vendor.get("x", 0.5)
        vy = vendor.get("y", 0.5)
        is_self = vendor.get("is_self", False)
        dot_size = Inches(0.35) if is_self else Inches(0.22)
        dot_color = C["primary"] if is_self else C["gray"]

        cx = int(grid_left + vx * grid_w - dot_size / 2)
        cy = int(grid_top + (1 - vy) * grid_h - dot_size / 2)

        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, cx, cy, int(dot_size), int(dot_size)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*dot_color)
        dot.line.fill.background()

        textbox(
            slide,
            int(cx - Inches(0.3)),
            int(cy + dot_size + Inches(0.02)),
            int(dot_size + Inches(0.6)),
            int(Inches(0.25)),
            vendor.get("name", ""),
            size="caption",
            bold=is_self,
            color=C["text"] if is_self else C["gray"],
            align=PP_ALIGN.CENTER,
        )

    return slide
