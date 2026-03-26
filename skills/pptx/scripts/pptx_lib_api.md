# pptx_lib API Reference

**Location**: `skills/pptx/scripts/pptx_lib.py`
**Import**: `import sys; sys.path.insert(0, "/Volumes/work/Workspace/A-Deck/skills/pptx/scripts"); from pptx_lib import *`

## Colors

### Theme Color Extraction (Dynamic)

```python
extract_theme_colors(prs) → dict[str, tuple[int,int,int]]
# Extracts color scheme from slide master theme XML.
# Keys: primary, secondary, accent3..accent6, dark, header, light, text, white, gray
# gray is derived as midpoint of dk2 and lt2.

lighter(rgb, factor=0.5) → tuple[int,int,int]
# Lighten toward white.  0.0 = original, 1.0 = pure white.

darker(rgb, factor=0.3) → tuple[int,int,int]
# Darken toward black.   0.0 = original, 1.0 = pure black.
```

### Legacy Static Palette (pptx_lib internals only)

- `C` — dict: cyan, cyan_2, cyan_3, dark, gray, mid_gray, light, line, white, soft_green, soft_blue, soft_yellow, domain_bg, brand_gray
- `MATURITY` — dict: GA/Managed/Beta/Alpha/Planned → {fill, border, text, dash}

## Canvas Constants

- `SAFE_LEFT`, `SAFE_RIGHT`, `SAFE_WIDTH` — safe area (0.3" – 9.68")
- `CONTENT_TOP`, `CONTENT_HEIGHT` — 1.08", 5.98"
- `FLOW_Y`, `LIST_Y` — default Y for flow (2.1") and list (4.1")
- `BASE_WIDTH_IN = 10.0` — design baseline width

## Drawing Primitives

```python
rect(slide, x, y, w, h, fill, line=None)           → shape
rrect(slide, x, y, w, h, fill, line=None, adj=8000) → shape
textbox(slide, x, y, w, h, text, size=16, bold=False, color=None, align=LEFT, valign=TOP) → shape
bullet_box(slide, x, y, w, h, lines, size=13)      → shape
add_text(shape, text, size, bold=False, color=None, align=CENTER, valign=MIDDLE)
set_rrect_adj(shape, adj=8000)
set_dash(shape)
```

## Slide Management

```python
layout_by_names(prs, names, fallback_index=1)    → layout
add_slide(prs, layout, keep_title=False)          → slide
clear_slides(prs)
fit_slide_to_canvas(slide, scale_x)
```

## Header / Footer

```python
header(slide, title, subtitle=None, num=None)     # uses placeholder idx=0
footer(slide)                                      # cyan line at y=7.26"
```

## Diagram Renderers

```python
render_flow(slide, steps, y=2.45)
  # steps: [{"title": str, "desc": str}, ...]

render_wide_list(slide, items, colors, y_start=1.22, h=0.76, gap=0.12, size=17)
  # items: [str, ...]  colors: [RGBColor, ...]

render_three_cols(slide, columns)
  # columns: [{"title": str, "items": [str, ...]}, ...]  (exactly 3)

render_relationship(slide, root_text, children)
  # children: [{"title": str, "items": [str, ...]}, ...]  (exactly 3)

render_capability_map(slide, domains, *, grid_top, grid_bottom, domain_w, cell_gap, row_gap, legend_y)
  # domains: [{"name": str, "caps": [(name, maturity), ...]}, ...]
  # maturity: "GA" | "Managed" | "Beta" | "Alpha" | "Planned"
```

## Build Entry Point

```python
def build_pptx(template, output, build_fn) → Path:
    # build_fn(ctx: BuildContext) — use ctx to add slides

class BuildContext:
    ctx.prs                  # python-pptx Presentation object
    ctx.scale_x              # horizontal scaling factor
    ctx.colors → dict        # theme colors (lazy, cached): primary, secondary, dark, text, white, light, gray, ...
    ctx.palette → list       # 7-color list: [dark, primary, secondary, accent3, accent4, accent5, accent6]
    ctx.add_cover_slide()    → slide
    ctx.add_content_slide()  → slide  (keeps title placeholder)
    ctx.add_thanks_slide()   → slide
    ctx.add_custom_slide(layout_names, fallback=1, keep_title=False) → slide
    ctx.finalize()           # applies scale_x to all slides (called automatically)
```

## Inline Verification

```python
verify_pptx(output, src_template=None) → dict
  # Prints: slides count, total shapes, first title, theme hash match
  # Returns: {"slides": int, "total_shapes": int, "first_title": str, "theme_match": bool|None}
```

## Example: Minimal Single-Slide Script

```python
import sys; sys.path.insert(0, "/Volumes/work/Workspace/A-Deck/skills/pptx/scripts")
from pptx_lib import *

TEMPLATE = Path("...template.pptx")
OUTPUT   = Path(__file__).resolve().parent / "output.pptx"

def my_slides(ctx):
    slide = ctx.add_content_slide()
    header(slide, "My Title", subtitle="Sub", num=1)
    render_flow(slide, [{"title":"Step 1","desc":"Do X"}, {"title":"Step 2","desc":"Do Y"}])

build_pptx(TEMPLATE, OUTPUT, my_slides)
verify_pptx(OUTPUT, TEMPLATE)
```
