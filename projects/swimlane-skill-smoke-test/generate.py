#!/usr/bin/env python3
"""Smoke test for TOGAF BA-03 swimlane layout rules."""

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
OUTPUT = Path(__file__).resolve().parent / "swimlane-skill-smoke-test.pptx"


SLIDE_DATA = {
    "title": "Copilot 工作流泳道图",
    "subtitle": "需求进入后分析、实现、验证并交付",
    "content": {
        "note": "BA-03 swimlane smoke test | event occupancy + aligned handoffs + even spacing",
        "lanes": ["需求进入", "实现决策", "交付验证"],
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
            {"id": "start", "type": "event", "lane": "需求进入", "x_in": 0.05, "start": True},
            {"id": "intake", "type": "step", "lane": "需求进入", "x_in": 0.75,
             "name": "接收需求", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "clarify", "type": "step", "lane": "需求进入", "x_in": 4.35,
             "name": "澄清约束", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "handoff", "type": "step", "lane": "需求进入", "x_in": 7.95,
             "name": "移交实现", "fill_color": "primary", "line_color": "primary", "text_color": "white"},

            {"id": "feasible", "type": "decision", "lane": "实现决策", "x_in": 8.05,
             "text": "可直接\n实现？", "w_in": 1.3, "h_in": 0.72},
            {"id": "review", "type": "decision", "lane": "实现决策", "x_in": 2.35,
             "text": "需补充\n信息？", "w_in": 1.3, "h_in": 0.72},

            {"id": "update_req", "type": "step", "lane": "交付验证", "x_in": 2.25,
             "name": "补充需求", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "implement", "type": "step", "lane": "交付验证", "x_in": 5.10,
             "name": "实现并测试", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "deliver", "type": "step", "lane": "交付验证", "x_in": 7.95,
             "name": "交付结果", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "end", "type": "event", "lane": "交付验证", "x_in": 9.55, "end": True},
        ],
        "links": [
            {"from": "start", "to": "intake"},
            {"from": "intake", "to": "clarify"},
            {"from": "clarify", "to": "handoff"},
            {"from": "handoff", "to": "feasible", "start_side": "bottom", "end_side": "top"},
            {"from": "feasible", "to": "deliver", "label": "是", "start_side": "bottom", "end_side": "top"},
            {"from": "feasible", "to": "review", "label": "否", "start_side": "left", "end_side": "right"},
            {"from": "review", "to": "update_req", "label": "要补充", "start_side": "bottom", "end_side": "top"},
            {"from": "review", "to": "implement", "label": "信息足够", "start_side": "right", "end_side": "left"},
            {"from": "deliver", "to": "end"},
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