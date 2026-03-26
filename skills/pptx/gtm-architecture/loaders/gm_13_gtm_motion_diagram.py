"""GM-18: Go-To-Market Motion"""
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

def load_slide(ctx, data):
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data["title"])
    set_subtitle(ctx, slide, data.get("subtitle", ""), C["gray"])
    
    motions = data["content"]["motions"]
    col_width = Inches(2.8)
    top = Inches(1.1)
    
    for i, motion in enumerate(motions[:3]):
        left = Inches(0.5) + i * (col_width + Inches(0.2))
        
        shape_rect(slide, left, top, col_width, Inches(0.35), fill_color=C["dark"])
        textbox(slide, left, top + Inches(0.05), col_width, Inches(0.25), motion["motion"], size="caption", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        
        y = top + Inches(0.45)
        textbox(slide, left + Inches(0.1), y, col_width - Inches(0.2), Inches(0.4), motion["description"], size="caption", color=C["text"])
        y += Inches(0.5)
        
        textbox(slide, left + Inches(0.1), y, Inches(0.5), Inches(0.2), "分段:", size="label", bold=True, color=C["gray"])
        textbox(slide, left + Inches(0.65), y, col_width - Inches(0.75), Inches(0.2), motion["target_segments"], size="caption", color=C["text"])
        
        y += Inches(0.3)
        for chan in motion.get("channels", []):
            textbox(slide, left + Inches(0.1), y, col_width - Inches(0.2), Inches(0.25), f"• {chan}", size="caption", color=C["gray"])
            y += Inches(0.25)
    
    return slide
