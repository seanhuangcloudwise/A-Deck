"""GM-20: Feature-to-usecase mapping matrix."""
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


def _status_cell(slide, x, y, w, h, status, status_colors):
    st = (status or "none").lower()
    if st == "full":
        symbol = "●"
        color = status_colors["full"]
    elif st == "partial":
        symbol = "◑"
        color = status_colors["partial"]
    else:
        symbol = "○"
        color = status_colors["none"]
    textbox(slide, x, y, w, h, symbol, size="body", color=color, align=PP_ALIGN.CENTER)


def _fallback_content(content):
    sections = content.get("sections", [])
    features = [s.get("title", "") for s in sections if s.get("title")][:6]
    if not features:
        features = ["AI生成", "模板库", "协作", "审批", "SSO", "导出"]

    use_cases = []
    for idx, sec in enumerate(sections[:6], 1):
        use_cases.append(
            {
                "name": sec.get("title", f"UseCase {idx}"),
                "actor": "业务团队",
                "objective": "提升效率",
                "metric": "周期缩短",
                "support": {f: ("full" if i == idx % len(features) else "partial") for i, f in enumerate(features)},
            }
        )
    if not use_cases:
        use_cases = [
            {
                "name": "销售提案",
                "actor": "销售",
                "objective": "加速赢单",
                "metric": "提案周期-40%",
                "support": {"AI生成": "full", "模板库": "full", "协作": "partial", "审批": "partial", "SSO": "none", "导出": "full"},
            }
        ]
    return features, use_cases


def load_slide(ctx, data):
    C = ctx.colors
    _STATUS = {"full": C["primary"], "partial": C["secondary"], "none": C["gray"]}
    layout = layout_by_names(ctx.prs, ["内容", "內容"], 1)
    slide = ctx.prs.slides.add_slide(layout)
    header(slide, data.get("title", "GM-20 Feature-UseCase Mapping"))
    set_subtitle(ctx, slide, data.get("subtitle", "特性场景映射矩阵"), C["gray"])

    content = data.get("content", {})
    features = content.get("features")
    use_cases = content.get("use_cases")
    if not features or not use_cases:
        features, use_cases = _fallback_content(content)

    features = features[:6]
    use_cases = use_cases[:8]

    left = Inches(0.5)
    top = Inches(1.15)
    total_w = Inches(8.5)
    head_h = Inches(0.4)
    row_h = Inches(0.42)
    case_w = Inches(2.2)
    feat_w = (total_w - case_w) / max(1, len(features))

    # Header
    shape_rect(slide, left, top, case_w, head_h, fill_color=C["dark"])
    textbox(slide, left, top, case_w, head_h, "Use Case (角色/目标)", size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
    x = left + case_w
    for feat in features:
        shape_rect(slide, x, top, feat_w, head_h, fill_color=C["dark"])
        textbox(slide, x + Inches(0.02), top + Inches(0.02), feat_w - Inches(0.04), head_h - Inches(0.04), feat, size="label", bold=True, color=C["white"], align=PP_ALIGN.CENTER)
        x += feat_w

    # Rows
    for r_i, uc in enumerate(use_cases):
        y = top + head_h + r_i * row_h
        bg = C["white"] if r_i % 2 == 0 else C["light"]
        shape_rect(slide, left, y, case_w, row_h, fill_color=bg, line_color=C["line"])
        uc_label = f"{uc.get('name', '')} | {uc.get('actor', '')}"
        textbox(slide, left + Inches(0.03), y + Inches(0.02), case_w - Inches(0.06), Inches(0.16), uc_label, size="label", bold=True, color=C["text"])
        textbox(slide, left + Inches(0.03), y + Inches(0.18), case_w - Inches(0.06), Inches(0.2), uc.get("metric", uc.get("objective", "")), size="caption", color=C["gray"])

        x = left + case_w
        support_map = uc.get("support", {})
        for feat in features:
            shape_rect(slide, x, y, feat_w, row_h, fill_color=bg, line_color=C["line"])
            _status_cell(slide, x, y + Inches(0.06), feat_w, Inches(0.3), support_map.get(feat, "none"), _STATUS)
            x += feat_w

    # Legend
    ly = Inches(5.2)
    textbox(slide, Inches(0.55), ly, Inches(2.3), Inches(0.16), "图例: ● Full   ◑ Partial   ○ None", size="label", color=C["text"])
    return slide
