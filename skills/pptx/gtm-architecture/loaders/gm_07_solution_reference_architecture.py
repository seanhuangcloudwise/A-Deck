"""GM-09: Solution Architecture"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from renderer_utils import textbox, shape_rect
from pptx.enum.text import PP_ALIGN

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
    
    layers = data["content"]["layers"]
    layer_height = Inches(1.0)
    top = Inches(1.1)
    
    for i, layer in enumerate(layers):
        y = top + i * layer_height
        shape_rect(slide, Inches(0.5), y, Inches(8.5), layer_height, fill_color=C["light"])
        textbox(slide, Inches(0.7), y + Inches(0.05), Inches(1.5), Inches(0.25), layer["name"], size="body", bold=True, color=C["dark"])
        
        comp_left = Inches(2.5)
        for comp in layer["components"][:3]:
            textbox(slide, comp_left, y + Inches(0.2), Inches(2.0), Inches(0.6), comp, size="label", color=C["text"])
            comp_left += Inches(2.1)
    
    return slide
