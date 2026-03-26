"""Common helpers for XSean loaders."""

import sys
from pathlib import Path

from pptx.dml.color import RGBColor
from pptx.util import Pt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))


def set_subtitle(ctx, slide, text):
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
        p.font.color.rgb = RGBColor(*ctx.colors["gray"])


def content_region(ctx, top_pad_in=0.22, bottom_pad_in=0.12):
    """Return safe content region in integer EMU."""
    from pptx.util import Inches

    x = int(ctx.safe_left)
    y = int(ctx.content_top + Inches(top_pad_in))
    w = int(ctx.safe_width)
    h = int(ctx.safe_bottom - y - Inches(bottom_pad_in))
    return x, y, w, h
