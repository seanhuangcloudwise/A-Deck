"""GM-34: Proof evidence ladder."""
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
        (s for s in slide.shapes if getattr(s, "is_placeholder", False) and s.placeholder_format.idx == 1),
        None,
    )
    if subtitle_ph and subtitle_ph.has_text_frame:
        tf = subtitle_ph.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(ctx.typography["subtitle"])
        p.font.color.rgb = RGBColor(*(gray_color or ctx.colors["gray"]))


def _fallback_levels(content):
    levels = []
    for idx, sec in enumerate(content.get("sections", []), 1):
        levels.append(
            {
                "level": f"L{idx}",
                "title": sec.get("title", f"Level {idx}"),
                "examples": sec.get("items", [])[:2],
                "confidence": idx,
            }
        )
    return levels


def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-34 Proof Evidence Ladder"))
    set_subtitle(ctx, slide, data.get("subtitle", "证据成熟度阶梯"), C["gray"])

    content = data.get("content", {})
    levels = content.get("levels") or _fallback_levels(content)
    levels = levels[:5]

    bottom_w = Inches(8.0)
    shrink = Inches(1.1)
    block_h = Inches(0.62)
    gap = Inches(0.08)
    left_base = Inches(0.65)
    top = Inches(4.9)

    textbox(slide, Inches(0.45), Inches(1.15), Inches(0.25), Inches(3.8), "↑", size="title", color=C["primary"], align=PP_ALIGN.CENTER)
    textbox(slide, Inches(0.4), Inches(4.95), Inches(0.5), Inches(0.2), "Low", size="label", color=C["gray"], align=PP_ALIGN.CENTER)
    textbox(slide, Inches(0.35), Inches(1.05), Inches(0.65), Inches(0.2), "High", size="label", color=C["dark"], align=PP_ALIGN.CENTER)

    for i, lv in enumerate(levels):
        w = bottom_w - (len(levels) - 1 - i) * shrink
        x = left_base + (bottom_w - w) / 2
        y = top - i * (block_h + gap)
        color = C["light"] if i < 2 else (C["secondary"] if i < 4 else C["dark"])
        text_color = C["text"] if i < 4 else C["white"]

        shape_rect(slide, x, y, w, block_h, fill_color=color, line_color=C["line"])
        textbox(slide, x + Inches(0.08), y + Inches(0.06), Inches(1.9), Inches(0.2), f"{lv.get('level', '')} {lv.get('title', '')}", size="label", bold=True, color=text_color)

        examples = lv.get("examples", [])
        if examples:
            textbox(slide, x + Inches(2.1), y + Inches(0.06), w - Inches(2.2), Inches(0.2), examples[0], size="caption", color=text_color)

        conf = int(lv.get("confidence", i + 1))
        dots = "●" * max(1, min(5, conf))
        textbox(slide, x + w - Inches(0.9), y + Inches(0.06), Inches(0.8), Inches(0.2), dots, size="caption", color=text_color, align=PP_ALIGN.RIGHT)

    textbox(slide, Inches(0.6), Inches(5.93), Inches(8.2), Inches(0.18), "每级证据均需可审计来源，避免将内部轶事等同第三方验证", size="caption", color=C["gray"])
    return slide

