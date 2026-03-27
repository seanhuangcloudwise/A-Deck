#!/usr/bin/env python3
"""Generate a single-slide BA-03 swimlane for the template + skill PPT pipeline."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "skills" / "pptx" / "scripts"
TOGAF_LOADERS_DIR = ROOT / "skills" / "pptx" / "togaf-architecture" / "loaders"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(TOGAF_LOADERS_DIR))

from pptx_lib import build_pptx  # noqa: E402
from ba_loader import load_ba_03_business_process  # noqa: E402

TEMPLATE = ROOT / "skills" / "pptx" / "master-library" / "light-cloudwise-cyan" / "cloudwise-master.pptx"
OUTPUT = Path(__file__).resolve().parent / "ba03-codechain-flow.pptx"


SLIDE_DATA = {
    "title": "基于母版与 Skill 的 PPT 生成链路",
    "subtitle": "生成脚本、框架编排、Skill/Loader 渲染协同生成单页 BA-03 泳道图",
    "content": {
        "note": "BA-03 codechain flow | template -> build_pptx -> BA-03 loader -> swimlane render -> output pptx",
        "lanes": ["生成脚本", "框架编排", "Skill / Loader"],
        "lane_header_w": 0.92,
        "lane_gap": 0.08,
        "flow_gap": 0.10,
        "left_pad_in": 0.14,
        "right_pad_in": 0.42,
        "start_event_outer_pad_in": 0.05,
        "end_event_outer_pad_in": 0.08,
        "step_w": 1.5,
        "step_h": 0.58,
        "nodes": [
            {"id": "start", "type": "event", "lane": "生成脚本", "x_in": 0.05, "start": True},
            {"id": "select_template", "type": "step", "lane": "生成脚本", "x_in": 0.75,
             "name": "选定母版与输出路径", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "import_loader", "type": "step", "lane": "生成脚本", "x_in": 4.05,
             "name": "显式引用\nBA-03 loader", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "build_data", "type": "step", "lane": "生成脚本", "x_in": 7.35,
             "name": "build(ctx) 交付\nSLIDE_DATA", "fill_color": "primary", "line_color": "primary", "text_color": "white"},

            {"id": "build_pptx", "type": "step", "lane": "框架编排", "x_in": 0.75,
             "name": "build_pptx 载入母版", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "build_ctx", "type": "step", "lane": "框架编排", "x_in": 4.05,
             "name": "创建 BuildContext", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "call_loader", "type": "step", "lane": "框架编排", "x_in": 7.35,
             "name": "调用 BA-03\n业务流程 loader", "fill_color": "primary", "line_color": "primary", "text_color": "white"},

            {"id": "skill_rule", "type": "step", "lane": "Skill / Loader", "x_in": 0.75,
             "name": "Skill 文档提供\n布局规范", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "render_swimlane", "type": "step", "lane": "Skill / Loader", "x_in": 4.05,
             "name": "render_swimlane\n合并数据与主题", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "detailed_layout", "type": "step", "lane": "Skill / Loader", "x_in": 7.35,
             "name": "_swimlane_detailed\n布局并绘制", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "end", "type": "event", "lane": "Skill / Loader", "x_in": 9.55, "end": True},
        ],
        "links": [
            {"from": "start", "to": "select_template"},
            {"from": "select_template", "to": "import_loader"},
            {"from": "import_loader", "to": "build_data"},
            {"from": "select_template", "to": "build_pptx", "start_side": "bottom", "end_side": "top"},
            {"from": "import_loader", "to": "build_ctx", "start_side": "bottom", "end_side": "top"},
            {"from": "build_data", "to": "call_loader", "start_side": "bottom", "end_side": "top"},
            {"from": "build_pptx", "to": "build_ctx"},
            {"from": "build_ctx", "to": "call_loader"},
            {"from": "call_loader", "to": "skill_rule", "label": "按 BA-03", "start_side": "left", "end_side": "right"},
            {"from": "skill_rule", "to": "render_swimlane"},
            {"from": "render_swimlane", "to": "detailed_layout"},
            {"from": "detailed_layout", "to": "end"},
        ],
    },
}


def build(ctx):
    return load_ba_03_business_process(ctx, SLIDE_DATA)


def main():
    def slides(ctx):
        build(ctx)

    build_pptx(str(TEMPLATE), str(OUTPUT), slides)
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()