"""Template for XSean loaders.

Copy this file to xs_xx_your_diagram.py and replace TODO sections.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "shared"))

from pptx_lib import header, layout_by_names
from renderer_utils import shape_rect, textbox

from .common import set_subtitle, content_region


def load_slide(ctx, data):
    """Standard entry for XSean loader.

    Args:
        ctx: BuildContext from pptx_lib
        data: dict with title/subtitle/content
    """
    C = ctx.colors
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)

    header(slide, data.get("title", "XS-XX Diagram"))
    set_subtitle(ctx, slide, data.get("subtitle", "XSean diagram template"))

    x, y, w, h = content_region(ctx)

    # TODO: replace this placeholder rendering with real diagram logic.
    shape_rect(slide, x, y, w, h, fill_color=C["light"], line_color=C["line"])
    textbox(
        slide,
        x,
        y + int(h * 0.4),
        w,
        int(h * 0.2),
        "TODO: Implement XS-XX loader",
        size="label",
        bold=True,
        color=C["text"],
    )
    return slide
