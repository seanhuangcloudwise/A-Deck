"""GM-11 KPI Dashboard Mockup — 2x3 grid of metric cards."""

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
    # Semantic status colors (domain-specific)
    STATUS_COLORS = {"healthy": C["primary"], "warning": (230, 180, 50), "critical": (210, 70, 70)}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    metrics = data["content"]["metrics"]
    cols = 3
    rows = 2
    card_gap = Inches(0.15)
    content_left = Inches(0.5)
    content_top = Inches(1.2)
    total_w = Inches(8.5)
    total_h = Inches(3.6)

    card_w = int((total_w - (cols - 1) * card_gap) / cols)
    card_h = int((total_h - (rows - 1) * card_gap) / rows)

    for idx, metric in enumerate(metrics[:6]):
        row = idx // cols
        col = idx % cols
        cx = int(content_left + col * (card_w + card_gap))
        cy = int(content_top + row * (card_h + card_gap))

        shape_rect(slide, cx, cy, card_w, card_h,
                    fill_color=C["white"], line_color=C["light"])

        status = metric.get("status", "healthy")
        accent = STATUS_COLORS.get(status, C["primary"])
        shape_rect(slide, cx, cy, card_w, int(Inches(0.06)),
                    fill_color=accent)

        textbox(slide, int(cx + Inches(0.12)), int(cy + Inches(0.15)),
                int(card_w - Inches(0.24)), int(Inches(0.25)),
                metric.get("name", ""), size="caption", color=C["gray"])

        textbox(slide, int(cx + Inches(0.12)), int(cy + Inches(0.45)),
                int(card_w - Inches(0.24)), int(Inches(0.6)),
                metric.get("value", ""), size="display", bold=True,
                color=C["text"], align=PP_ALIGN.LEFT)

        trend = metric.get("trend", "")
        trend_color = C["primary"] if "↓" in trend or "+" in trend else C["gray"]
        textbox(slide, int(cx + Inches(0.12)), int(cy + card_h - Inches(0.4)),
                int(card_w - Inches(0.24)), int(Inches(0.25)),
                trend, size="body", bold=True, color=trend_color)

    return slide
