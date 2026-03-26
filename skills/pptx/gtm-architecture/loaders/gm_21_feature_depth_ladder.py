"""GM-21 Feature Depth Ladder — 4-level vertical ladder (bottom to top)."""

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
    LEVEL_COLORS = [C["light"], C["secondary"], C["primary"], C["dark"]]
    LEVEL_TEXT = [C["text"], C["text"], C["white"], C["white"]]
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])

    levels = data["content"]["levels"]
    n = len(levels)
    if n == 0:
        return slide

    ladder_left = Inches(0.5)
    ladder_top = Inches(1.2)
    ladder_w = Inches(4.5)
    total_h = Inches(3.6)
    level_gap = Inches(0.08)
    level_h = int((total_h - (n - 1) * level_gap) / n)

    evidence_x = int(ladder_left + ladder_w + Inches(0.3))
    evidence_w = int(Inches(3.7))

    # Render bottom to top: levels[0] = L1 at bottom
    for i, level in enumerate(levels):
        idx = n - 1 - i  # visual index from top
        ly = int(ladder_top + idx * (level_h + level_gap))

        bg = LEVEL_COLORS[i % len(LEVEL_COLORS)]
        txt = LEVEL_TEXT[i % len(LEVEL_TEXT)]

        shape_rect(slide, int(ladder_left), ly, int(ladder_w), level_h,
                    fill_color=bg)

        textbox(slide, int(ladder_left + Inches(0.15)), ly,
                int(ladder_w - Inches(0.3)), int(Inches(0.3)),
                level.get("label", ""), size="body", bold=True, color=txt)

        textbox(slide, int(ladder_left + Inches(0.15)),
                int(ly + Inches(0.3)),
                int(ladder_w - Inches(0.3)),
                int(level_h - Inches(0.35)),
                level.get("capability", ""), size="caption", color=txt)

        # Evidence badge on the right
        evidence = level.get("evidence", "")
        impact = level.get("impact", "")
        badge_text = f"{impact}\n{evidence}" if evidence else impact
        if badge_text.strip():
            shape_rect(slide, evidence_x, ly, evidence_w, level_h,
                        fill_color=C["light"])
            textbox(slide, int(evidence_x + Inches(0.1)), ly,
                    int(evidence_w - Inches(0.2)), level_h,
                    badge_text, size="label", color=C["text"])

    return slide
