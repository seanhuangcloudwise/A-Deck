#!/usr/bin/env python3
"""RA-01 Strategic Roadmap Timeline — A-Deck 产品路线图
Layout: Variant B 季度滚动路线图 (Q2'26 ~ Q1'27)
Swimlanes: 6 (知识沉淀/核心能力/母版体系/AI辅助/TOGAF/路线图)
Milestones: 3 (Q2核心稳定/Q3专精/Q4推广)
Audience: 产品团队内部对齐
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../skills/pptx/scripts"))
from pptx_lib import *
from pathlib import Path

TEMPLATE = os.path.join(os.path.dirname(__file__),
    "../ppt-maker-intro-cloudwise-2025/ppt-maker-agent-self-intro-cloudwise.pptx")
TEMPLATE_SPEC = os.path.join(os.path.dirname(__file__), 
    "../../skills/pptx/templates/cloudwise-spec.yaml")
OUTPUT = os.path.join(os.path.dirname(__file__), "ppt-maker-ra-01-strategic-timeline.pptx")

# ── Colors ──
CYAN       = RGBColor(0x00, 0xCC, 0xD7)
CYAN_LT    = RGBColor(0x53, 0xE3, 0xEB)
DARK       = RGBColor(0x2F, 0x2F, 0x2F)
GRAY       = RGBColor(0xA5, 0xA7, 0xAA)
DOMAIN_BG  = RGBColor(0x44, 0x54, 0x6A)
NOW_BG     = RGBColor(0xE8, 0xFF, 0xFE)
LIGHT_BG   = RGBColor(0xF5, 0xF5, 0xF5)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
HOLD_GRAY  = RGBColor(0xE5, 0xE5, 0xE5)
ORANGE     = RGBColor(0xFF, 0x6B, 0x35)
MS_GREEN   = RGBColor(0x00, 0xBF, 0x87)

# ── Layout constants ──
SL = Inches(0.3)            # safe left
SW = Inches(9.38)           # safe width
TITLE_H = Inches(0.9)       # title zone
LABEL_W = Inches(1.36)      # swimlane label column
TIME_H  = Inches(0.32)      # time axis row height
LANE_GAP = Inches(0.04)     # gap between lanes
FOOT_H  = Inches(0.28)      # footer

QUARTERS = ["Q2'26", "Q3'26", "Q4'26", "Q1'27"]
Q_COLORS = [NOW_BG, WHITE, WHITE, LIGHT_BG]  # Q2=now highlight

# ── Data ──
SWIMLANES = [
    {
        "name": "知识沉淀与复用",
        "items": [
            {"text": "知识场景框架 (6场景)", "q": [0], "status": "done"},
            {"text": "product-brochure 2轮学习", "q": [0], "status": "done"},
            {"text": "product-roadmap 场景激活", "q": [0, 1], "status": "wip"},
            {"text": "全场景 ≥2轮学习沉淀", "q": [1, 2], "status": "wip"},
            {"text": "跨场景模式复用引擎", "q": [2, 3], "status": "plan"},
        ],
    },
    {
        "name": "PPT 创建与编辑\n核心能力",
        "items": [
            {"text": "W1-W6 全流程文档化", "q": [0], "status": "done"},
            {"text": "pptx_lib 20+ API", "q": [0], "status": "done"},
            {"text": "XML 编辑链路稳定化", "q": [0, 1], "status": "wip"},
            {"text": "错误恢复与边界用例覆盖", "q": [1, 2], "status": "plan"},
            {"text": "批量生成与Pipeline优化", "q": [2, 3], "status": "plan"},
        ],
    },
    {
        "name": "母版与模板体系",
        "items": [
            {"text": "Cloudwise 母版入库", "q": [0], "status": "done"},
            {"text": "母版提取工作流 (W6)", "q": [0], "status": "done"},
            {"text": "≥3 母版沉淀", "q": [1, 2], "status": "plan"},
            {"text": "模板推荐与自动匹配", "q": [2, 3], "status": "plan"},
        ],
    },
    {
        "name": "AI 辅助能力升级",
        "items": [
            {"text": "Agent 驱动工作流编排", "q": [0], "status": "done"},
            {"text": "结构化数据→PPT 自动生成", "q": [1, 2], "status": "plan"},
            {"text": "多模态内容提取 (图→图)", "q": [2, 3], "status": "plan"},
            {"text": "智能模板推荐引擎", "q": [3], "status": "plan"},
        ],
    },
    {
        "name": "TOGAF\n架构图能力",
        "items": [
            {"text": "37图规范全量完成", "q": [0], "status": "done"},
            {"text": "BA层 4图实战验证", "q": [0], "status": "done"},
            {"text": "AA/DA/TA层 样例覆盖", "q": [0, 1], "status": "wip"},
            {"text": "全37图 ≥1 样例PPT", "q": [1, 2], "status": "plan"},
            {"text": "用户场景驱动自动选图", "q": [2, 3], "status": "plan"},
        ],
    },
    {
        "name": "路线图规划体系\n(Roadmap Arch)",
        "items": [
            {"text": "RA 10图规范完成", "q": [0], "status": "done"},
            {"text": "W7-W10 工作流定义", "q": [0], "status": "done"},
            {"text": "RA-01 首图实战 (本图)", "q": [0], "status": "wip"},
            {"text": "RA 10图 样例PPT覆盖", "q": [1, 2], "status": "plan"},
            {"text": "规划方法论知识沉淀", "q": [2, 3], "status": "plan"},
        ],
    },
]

MILESTONES = [
    {"text": "核心能力稳定", "q": 0, "desc": "W1-W6 可用 · TOGAF 规范 · RA 规范"},
    {"text": "垂直领域图形专精", "q": 1, "desc": "37+10 图 样例覆盖 · 全场景知识沉淀"},
    {"text": "全面市场推广", "q": 2, "desc": "AI 自动生成 · 模板推荐 · Pipeline 优化"},
]


def _status_style(status):
    if status == "done":
        return CYAN, WHITE, False
    elif status == "wip":
        return CYAN_LT, DARK, False
    else:
        return HOLD_GRAY, GRAY, True


def slide_roadmap(ctx):
    slide = ctx.add_content_slide()

    # ── Title ──
    header(slide, "A-Deck — 战略产品路线图",
           subtitle="Variant B: 季度滚动路线图 | 2026 Q2 ~ 2027 Q1 | 产品团队内部对齐")

    # ── Geometry ──
    content_top = Inches(1.04)
    chart_left = SL + LABEL_W + Inches(0.04)
    chart_w = SW - LABEL_W - Inches(0.04)
    q_w = chart_w / len(QUARTERS)

    n_lanes = len(SWIMLANES)
    avail_h = Inches(7.0) - content_top - TIME_H - FOOT_H - Inches(0.52)
    lane_h = (avail_h - LANE_GAP * (n_lanes - 1)) / n_lanes

    # ── Quarter header row ──
    t_top = content_top
    for qi, qlabel in enumerate(QUARTERS):
        x = chart_left + qi * q_w
        bg = rect(slide, x, t_top, q_w, TIME_H, Q_COLORS[qi], line=GRAY)
        add_text(bg, qlabel, 9, bold=True, color=DARK)
    # "Now" indicator on Q2
    now_tag = rrect(slide, chart_left + Inches(0.06), t_top + Inches(0.02),
                    Inches(0.38), Inches(0.18), CYAN, adj=6000)
    add_text(now_tag, "NOW", 7, bold=True, color=WHITE)

    # ── Swimlanes ──
    lane_top = t_top + TIME_H + Inches(0.06)
    for li, lane in enumerate(SWIMLANES):
        y = lane_top + li * (lane_h + LANE_GAP)

        # Label column
        lbl = rrect(slide, SL, y, LABEL_W, lane_h, DOMAIN_BG, adj=4000)
        add_text(lbl, lane["name"], 9, bold=True, color=WHITE)

        # Quarter background stripes
        for qi in range(len(QUARTERS)):
            x = chart_left + qi * q_w
            rect(slide, x, y, q_w, lane_h,
                 Q_COLORS[qi] if qi == 0 else LIGHT_BG if qi == 3 else WHITE,
                 line=RGBColor(0xE0, 0xE0, 0xE0))

        # Initiative bars
        items = lane["items"]
        n_items = len(items)
        bar_h = min(Inches(0.19), (lane_h - Inches(0.08)) / n_items - Inches(0.02))
        bar_top = y + (lane_h - n_items * (bar_h + Inches(0.02))) / 2

        for ii, item in enumerate(items):
            q_start = item["q"][0]
            q_end = item["q"][-1]
            bx = chart_left + q_start * q_w + Inches(0.06)
            bw = (q_end - q_start + 1) * q_w - Inches(0.12)
            by = bar_top + ii * (bar_h + Inches(0.02))
            fill, text_c, dashed = _status_style(item["status"])

            bar = rrect(slide, bx, by, bw, bar_h, fill,
                        line=GRAY if dashed else None, adj=4000)
            if dashed:
                set_dash(bar)
            add_text(bar, item["text"], 7, bold=False, color=text_c)

            # DONE badge
            if item["status"] == "done":
                badge_x = bx + bw - Inches(0.18)
                badge_y = by + Inches(0.01)
                bdg = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, badge_x, badge_y,
                    Inches(0.16), Inches(0.16))
                bdg.fill.solid()
                bdg.fill.fore_color.rgb = MS_GREEN
                bdg.line.fill.background()
                add_text(bdg, "✓", 6, bold=True, color=WHITE)

    # ── Milestones (diamonds below the chart) ──
    ms_y = lane_top + n_lanes * (lane_h + LANE_GAP) + Inches(0.06)
    # Milestone row label
    ms_lbl = rrect(slide, SL, ms_y, LABEL_W, Inches(0.4), DARK, adj=4000)
    add_text(ms_lbl, "关键里程碑", 9, bold=True, color=WHITE)

    for mi, ms in enumerate(MILESTONES):
        qi = ms["q"]
        cx = chart_left + qi * q_w + q_w * 0.5
        dy = ms_y + Inches(0.04)
        # Diamond
        diamond = slide.shapes.add_shape(
            MSO_SHAPE.DIAMOND, cx - Inches(0.14), dy, Inches(0.28), Inches(0.28))
        diamond.fill.solid()
        diamond.fill.fore_color.rgb = CYAN if qi == 0 else ORANGE if qi == 2 else DARK
        diamond.line.fill.background()
        # Label
        textbox(slide, cx - Inches(0.7), dy + Inches(0.3), Inches(1.4), Inches(0.14),
                ms["text"], size=7, bold=True, color=DARK, align=PP_ALIGN.CENTER)
        textbox(slide, cx - Inches(0.9), dy + Inches(0.42), Inches(1.8), Inches(0.12),
                ms["desc"], size=6, color=GRAY, align=PP_ALIGN.CENTER)

    # ── Legend (bottom-right) ──
    lg_x = SL + SW - Inches(3.4)
    lg_y = ms_y + Inches(0.62)
    legend_items = [
        ("已完成", CYAN, WHITE),
        ("进行中", CYAN_LT, DARK),
        ("计划中", HOLD_GRAY, GRAY),
    ]
    for idx, (lbl_text, fill, _tc) in enumerate(legend_items):
        lx = lg_x + idx * Inches(1.1)
        dot = rrect(slide, lx, lg_y, Inches(0.24), Inches(0.14), fill, adj=4000)
        textbox(slide, lx + Inches(0.28), lg_y - Inches(0.01), Inches(0.6), Inches(0.16),
                lbl_text, size=7, color=GRAY)

    # ── Footer meta ──
    ft_y = lg_y + Inches(0.22)
    textbox(slide, SL, ft_y, SW, Inches(0.14),
            "数据截至: 2026-03-25 | 版本: v1.0 | 受众: 产品团队内部对齐",
            size=7, color=GRAY, align=PP_ALIGN.RIGHT)


# ── Build ──
build_pptx(TEMPLATE, OUTPUT, slide_roadmap, TEMPLATE_SPEC)
verify_pptx(OUTPUT)
