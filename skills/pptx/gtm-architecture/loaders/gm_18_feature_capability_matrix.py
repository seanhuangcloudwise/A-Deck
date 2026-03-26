"""GM-23:Feature-Capability Matrix"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from pptx_lib import layout_by_names, header
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from renderer_utils import textbox, shape_rect

def _level_to_score(level):
    if not level:
        return 0
    lvl = str(level).strip()
    if lvl in {"-", "none", "None", "0"}:
        return 0
    if lvl.isdigit():
        return max(0, min(3, int(lvl)))
    # Support legacy symbols like ●●● / ●● / ●.
    return max(0, min(3, lvl.count("●")))


def _mix_color(c1, c2, ratio):
    ratio = max(0.0, min(1.0, float(ratio)))
    return tuple(int(c1[i] * (1.0 - ratio) + c2[i] * ratio) for i in range(3))


def _heat_color(score, colors):
    base = colors.get("light", (244, 246, 247))
    accent = colors.get("cyan", colors.get("accent", colors.get("dark", (0, 204, 215))))
    palette = {
        0: base,
        1: _mix_color(base, accent, 0.35),
        2: _mix_color(base, accent, 0.65),
        3: _mix_color(base, accent, 0.92),
    }
    return palette.get(score, palette[0])


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
    header(slide, data.get("title", "GM-23 Feature-Capability Matrix"))
    set_subtitle(ctx, slide, data.get("subtitle", "产品特性与能力矩阵"), C["gray"])
    
    content = data.get("content", {"features": [], "capabilities": []})
    features = content.get("features", [])
    capabilities = content.get("capabilities", [])

    # Backward compatibility: old schema used sections/items.
    if (not features or not capabilities) and content.get("sections"):
        sections = content.get("sections", [])
        capabilities = [sec.get("title", "") for sec in sections][:4]
        features = []
        for sec in sections:
            for item in sec.get("items", []):
                name = item.split("：", 1)[0] if "：" in item else item
                levels = []
                for cap in capabilities:
                    level = "●●●" if cap == sec.get("title", "") else "●"
                    levels.append({"capability": cap, "level": level})
                features.append({"name": name, "capability_levels": levels})

    capabilities = capabilities[:4]
    headers = ["特性"] + [c[:12] for c in capabilities]
    rows = []
    for feat in features[:5]:
        level_map = {
            lv.get("capability", ""): lv.get("level", "")
            for lv in feat.get("capability_levels", [])
        }
        row_levels = [level_map.get(cap, "-") for cap in capabilities]
        rows.append([feat.get("name", "")] + row_levels)

    # Ensure table has visible content even when input is sparse.
    if not rows:
        rows = [["（待补充特性）", "-", "-", "-", "-"]]

    # Heatmap matrix layout
    left = Inches(0.5)
    top = Inches(1.15)
    feature_w = Inches(2.25)
    cell_w = Inches(1.45)
    head_h = Inches(0.4)
    row_h = Inches(0.52)

    # Header row
    shape_rect(slide, left, top, feature_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top + Inches(0.04), feature_w, Inches(0.28), headers[0], size="caption", bold=True, color=C["white"], align=PP_ALIGN.CENTER)

    for i, h in enumerate(headers[1:]):
        x = left + feature_w + i * cell_w
        shape_rect(slide, x, top, cell_w, head_h, fill_color=C["dark"])
        textbox(slide, x + Inches(0.03), top + Inches(0.04), cell_w - Inches(0.06), Inches(0.28), h, size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)

    # Data rows
    for r_i, row in enumerate(rows):
        y = top + head_h + r_i * row_h
        # Feature name column
        name_bg = C["white"] if r_i % 2 == 0 else C["light"]
        shape_rect(slide, left, y, feature_w, row_h, fill_color=name_bg, line_color=C["line"])
        textbox(slide, left + Inches(0.06), y + Inches(0.05), feature_w - Inches(0.12), row_h - Inches(0.1), row[0], size="label", color=C["text"])

        # Capability heat cells
        for c_i, lv in enumerate(row[1:]):
            x = left + feature_w + c_i * cell_w
            score = _level_to_score(lv)
            fill = _heat_color(score, C)
            shape_rect(slide, x, y, cell_w, row_h, fill_color=fill, line_color=C["line"])
            label = f"L{score}" if score > 0 else "-"
            text_color = C["white"] if score >= 2 else C["text"]
            textbox(slide, x, y + Inches(0.1), cell_w, Inches(0.25), label, size="caption", bold=True, color=text_color, align=PP_ALIGN.CENTER)

    # Legend
    legend_y = Inches(5.15)
    textbox(slide, Inches(0.5), legend_y - Inches(0.02), Inches(0.9), Inches(0.2), "强度:", size="label", bold=True, color=C["text"])
    for i in range(4):
        lx = Inches(1.15) + i * Inches(0.85)
        shape_rect(slide, lx, legend_y, Inches(0.22), Inches(0.12), fill_color=_heat_color(i, C), line_color=C["line"])
        textbox(slide, lx + Inches(0.26), legend_y - Inches(0.03), Inches(0.5), Inches(0.18), "None" if i == 0 else f"L{i}", size="caption", color=C["text"])

    textbox(slide, Inches(4.2), legend_y - Inches(0.02), Inches(4.7), Inches(0.2), "L1=基础支持, L2=重点支持, L3=核心优势", size="caption", color=C["gray"], align=PP_ALIGN.RIGHT)
    return slide
