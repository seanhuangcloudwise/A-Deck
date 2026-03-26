"""GM-30 Cost of Inaction Table — 4-column table with total row."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, shape_rect

COL_HEADERS = ["Category", "Current State", "Annual Impact", "Trend"]
COL_WIDTHS_RATIO = [0.28, 0.32, 0.22, 0.18]


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
    rows_data = content.get("rows", [])
    total_val = content.get("total", "")

    table_left = Inches(0.5)
    table_top = Inches(1.3)
    table_w = Inches(8.5)
    row_h = int(Inches(0.45))
    header_h = int(Inches(0.45))
    pad = Inches(0.1)

    col_widths = [int(table_w * r) for r in COL_WIDTHS_RATIO]

    # --- Header row ---
    cx = int(table_left)
    for ci, hdr in enumerate(COL_HEADERS):
        cw = col_widths[ci]
        shape_rect(slide, cx, int(table_top), cw, header_h,
                    fill_color=C["dark"])
        textbox(slide, int(cx + pad), int(table_top + Inches(0.05)),
                int(cw - 2 * pad), int(header_h - Inches(0.1)),
                hdr, size="label", bold=True, color=C["white"],
                align=PP_ALIGN.CENTER)
        cx += cw

    # --- Data rows ---
    for ri, row in enumerate(rows_data):
        ry = int(table_top + header_h + ri * row_h)
        bg = C["white"] if ri % 2 == 0 else C["light"]
        fields = [
            row.get("category", ""),
            row.get("current", ""),
            row.get("impact", ""),
            row.get("trend", ""),
        ]

        cx = int(table_left)
        for ci, val in enumerate(fields):
            cw = col_widths[ci]
            shape_rect(slide, cx, ry, cw, row_h,
                        fill_color=bg, line_color=C["light"])
            text_color = C["text"]
            if ci == 3:  # Trend column
                text_color = C["primary"] if "↑" in val else C["gray"]
            textbox(slide, int(cx + pad), ry,
                    int(cw - 2 * pad), row_h,
                    val, size="caption", color=text_color,
                    align=PP_ALIGN.CENTER if ci >= 2 else PP_ALIGN.LEFT)
            cx += cw

    # --- Total row ---
    if total_val:
        ty = int(table_top + header_h + len(rows_data) * row_h)
        total_h = int(Inches(0.5))

        # Span first 2 columns for label
        label_w = col_widths[0] + col_widths[1]
        shape_rect(slide, int(table_left), ty, label_w, total_h,
                    fill_color=C["dark"])
        textbox(slide, int(table_left + pad), ty,
                int(label_w - 2 * pad), total_h,
                "TOTAL ANNUAL COST OF INACTION", size="label", bold=True,
                color=C["white"])

        # Impact column with cyan accent
        impact_x = int(table_left) + label_w
        impact_w = col_widths[2]
        shape_rect(slide, impact_x, ty, impact_w, total_h,
                    fill_color=C["primary"])
        textbox(slide, int(impact_x + pad), ty,
                int(impact_w - 2 * pad), total_h,
                total_val, size="h3", bold=True,
                color=C["white"], align=PP_ALIGN.CENTER)

        # Trend column
        trend_x = impact_x + impact_w
        trend_w = col_widths[3]
        shape_rect(slide, trend_x, ty, trend_w, total_h,
                    fill_color=C["dark"])

    return slide
