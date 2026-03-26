"""GM-19: Market Segmentation"""
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
    
    segments = data["content"]["segments"]
    seg_height = Inches(1.1)
    top = Inches(1.1)
    
    for i, seg in enumerate(segments):
        left = Inches(0.5)
        y = top + i * seg_height
        
        shape_rect(slide, left, y, Inches(8.5), seg_height, fill_color=C["light"])
        
        textbox(slide, left + Inches(0.2), y + Inches(0.05), Inches(2.5), Inches(0.25), seg["segment"], size="label", bold=True, color=C["dark"])
        textbox(slide, left + Inches(2.8), y + Inches(0.05), Inches(1.0), Inches(0.25), seg["tam"], size="caption", color=C["text"], align=PP_ALIGN.CENTER)
        textbox(slide, left + Inches(3.9), y + Inches(0.05), Inches(2.0), Inches(0.25), seg["characteristics"], size="label", color=C["gray"])
        
        y_personas = y + Inches(0.35)
        for persona in seg.get("personas", []):
            textbox(slide, left + Inches(0.3), y_personas, Inches(8.0), Inches(0.2), f"→ {persona}", size="label", color=C["text"])
            y_personas += Inches(0.2)
    
    return slide
