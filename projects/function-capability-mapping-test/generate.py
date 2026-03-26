#!/usr/bin/env python3
"""Generate one-slide Function-Capability Mapping diagram (BA-06 Matrix Variant)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "skills" / "pptx" / "scripts"))
from pptx_lib import *  # noqa: E402,F403

from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


TEMPLATE = Path("/Volumes/work/Workspace/A-Deck/projects/ppt-maker-intro-cloudwise-2025"
                "/ppt-maker-agent-self-intro-cloudwise.pptx")
OUTPUT = Path(__file__).resolve().parent / "ppt-maker-function-capability-mapping.pptx"


FUNCTIONS = [
    ("需求分析", "PMO"),
    ("内容生成", "ENG"),
    ("模板治理", "DES"),
    ("架构制图", "ARCH"),
    ("质量校验", "QA"),
    ("知识运营", "OPS"),
    ("交付发布", "DEV"),
    ("成本控制", "FIN"),
]

CAPABILITIES = [
    "提纲规划",
    "页面内容编排",
    "母版继承输出",
    "业务架构",
    "样式一致性",
    "知识库体系",
    "PPTX 文件输出",
    "多模板并行",  # keep one critical gap column (all empty)
]

# Mapping values: P=Primary, S=Supporting, ""=No mapping
MATRIX = [
    ["P", "S", "",  "",  "",  "S", "",  ""],
    ["S", "P", "P", "",  "S", "S", "S", ""],
    ["",  "S", "P", "",  "P", "",  "",  ""],
    ["",  "",  "",  "P", "S", "",  "",  ""],
    ["",  "S", "S", "",  "P", "",  "S", ""],
    ["",  "",  "",  "",  "S", "P", "",  ""],
    ["",  "",  "S", "",  "",  "",  "P", ""],
    ["",  "",  "",  "",  "",  "",  "",  ""],
]


def _coverage_count(col_idx):
    cnt = 0
    for row in MATRIX:
        if row[col_idx] in ("P", "S"):
            cnt += 1
    return cnt


def _row_load(row_idx):
    cnt = 0
    for v in MATRIX[row_idx]:
        if v in ("P", "S"):
            cnt += 1
    return cnt


def _draw_legend(slide, y):
    items = [
        ("Primary", C["cyan"], C["cyan"]),
        ("Supporting", C["cyan_2"], C["cyan"]),
        ("No Mapping", C["white"], C["line"]),
        ("Critical Gap", C["white"], RGBColor(0xC0, 0x39, 0x2B)),
    ]
    x = SAFE_LEFT + Inches(0.1)
    for label, fill, line_c in items:
        box = rrect(slide, x, y, Inches(0.22), Inches(0.16), fill, line=line_c, adj=2500)
        box.line.width = Pt(0.8)
        if label == "Critical Gap":
            set_dash(box)
        textbox(slide, x + Inches(0.28), y - Inches(0.01), Inches(1.25), Inches(0.2),
                label, size=8, color=C["gray"], align=PP_ALIGN.LEFT)
        x += Inches(1.55)


def my_slides(ctx):
    slide = ctx.add_content_slide()

    header(slide, "PPT Maker Agent — Function Capability Mapping")
    textbox(slide, SAFE_LEFT + Inches(0.04), Inches(0.68), Inches(7.2), Inches(0.22),
            "BA-06 Matrix Variant · Coverage & Gap Analysis", size=10, color=C["brand_gray"])

    left = SAFE_LEFT
    top = Inches(1.18)
    func_w = Inches(2.0)
    col_w = Inches(0.78)
    cov_w = Inches(0.95)
    row_h = Inches(0.52)
    header_h = Inches(0.56)

    # Header: function column
    rect(slide, left, top, func_w, header_h, C["domain_bg"])
    textbox(slide, left + Inches(0.08), top + Inches(0.15), func_w - Inches(0.16), Inches(0.24),
            "Function (Owner)", size=10, bold=True, color=C["white"], align=PP_ALIGN.LEFT)

    # Header: capability columns + coverage marks
    for j, cap in enumerate(CAPABILITIES):
        x = left + func_w + j * col_w
        cov = _coverage_count(j)
        redundant = cov >= 3
        gap = cov == 0
        star = cap in ("提纲规划", "母版继承输出", "样式一致性")
        hdr_fill = C["cyan_3"] if not gap else C["white"]
        hdr_line = C["line"] if not gap else RGBColor(0xC0, 0x39, 0x2B)
        head = rrect(slide, x, top, col_w, header_h, hdr_fill, line=hdr_line, adj=2500)
        head.line.width = Pt(1.0)
        if gap:
            set_dash(head)

        cap_name = cap
        if redundant:
            cap_name += " ∩"
        if star:
            cap_name = "★" + cap_name

        textbox(slide, x + Inches(0.03), top + Inches(0.04), col_w - Inches(0.06), Inches(0.25),
                cap_name, size=8, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)
        textbox(slide, x + Inches(0.03), top + Inches(0.29), col_w - Inches(0.06), Inches(0.20),
                f"{int(cov/len(FUNCTIONS)*100)}%", size=7, color=C["brand_gray"], align=PP_ALIGN.CENTER)

    cov_x = left + func_w + len(CAPABILITIES) * col_w
    rect(slide, cov_x, top, cov_w, header_h, C["domain_bg"])
    textbox(slide, cov_x + Inches(0.04), top + Inches(0.15), cov_w - Inches(0.08), Inches(0.24),
            "Load", size=9, bold=True, color=C["white"], align=PP_ALIGN.CENTER)

    # Body rows
    gap_cols = []
    for j in range(len(CAPABILITIES)):
        if _coverage_count(j) == 0:
            gap_cols.append(j)

    for i, (fname, owner) in enumerate(FUNCTIONS):
        y = top + header_h + i * row_h
        load = _row_load(i)
        overloaded = load >= 5

        row_fill = C["white"]
        row_line = C["line"]
        label = rrect(slide, left, y, func_w, row_h, row_fill, line=row_line, adj=2500)
        label.line.width = Pt(2.0 if overloaded else 1.0)
        if overloaded:
            label.line.color.rgb = C["domain_bg"]

        textbox(slide, left + Inches(0.08), y + Inches(0.09), Inches(1.30), Inches(0.18),
                fname, size=9, bold=True, color=C["dark"], align=PP_ALIGN.LEFT)
        tag = rrect(slide, left + Inches(1.44), y + Inches(0.11), Inches(0.45), Inches(0.22), C["soft_blue"], line=C["line"], adj=2200)
        add_text(tag, owner, size=7, bold=True, color=C["gray"], align=PP_ALIGN.CENTER)

        for j in range(len(CAPABILITIES)):
            x = left + func_w + j * col_w
            v = MATRIX[i][j]

            fill = C["white"]
            line = C["line"]
            if v == "P":
                fill = C["cyan"]
                line = C["cyan"]
            elif v == "S":
                fill = C["cyan_2"]
                line = C["cyan"]

            cell = rrect(slide, x, y, col_w, row_h, fill, line=line, adj=2200)
            cell.line.width = Pt(0.8)

            if j in gap_cols:
                cell.line.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
                set_dash(cell)

            if v == "P":
                textbox(slide, x + Inches(0.02), y + Inches(0.16), col_w - Inches(0.04), Inches(0.2),
                        "P", size=8, bold=True, color=C["white"], align=PP_ALIGN.CENTER)
            elif v == "S":
                textbox(slide, x + Inches(0.02), y + Inches(0.16), col_w - Inches(0.04), Inches(0.2),
                        "S", size=8, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)

        load_fill = C["soft_yellow"] if overloaded else C["light"]
        load_box = rrect(slide, cov_x, y, cov_w, row_h, load_fill, line=C["line"], adj=2200)
        load_box.line.width = Pt(1.0)
        textbox(slide, cov_x + Inches(0.04), y + Inches(0.14), cov_w - Inches(0.08), Inches(0.2),
                f"{load}/8", size=9, bold=True, color=C["dark"], align=PP_ALIGN.CENTER)

    # Summary & annotations
    total_cells = len(FUNCTIONS) * len(CAPABILITIES)
    mapped_cells = sum(1 for row in MATRIX for v in row if v in ("P", "S"))
    coverage = int(mapped_cells * 100 / total_cells)
    gap_count = len(gap_cols)

    textbox(slide, SAFE_LEFT, Inches(6.45), Inches(4.8), Inches(0.2),
            f"Capability Coverage: {coverage}%  |  Critical Gaps: {gap_count}",
            size=8, color=C["gray"], align=PP_ALIGN.LEFT)
    if gap_count > 0:
        textbox(slide, SAFE_LEFT + Inches(5.1), Inches(6.45), Inches(4.2), Inches(0.2),
                "No Coverage: 多模板并行", size=8, bold=True,
                color=RGBColor(0xC0, 0x39, 0x2B), align=PP_ALIGN.RIGHT)

    _draw_legend(slide, Inches(6.84))


if __name__ == "__main__":
    build_pptx(TEMPLATE, OUTPUT, my_slides)
    verify_pptx(OUTPUT, TEMPLATE)
