#!/usr/bin/env python3
"""Generate the offline autonomous flow using the shared BA-03 business-process loader."""

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
OUTPUT = Path(__file__).resolve().parent / "offline-autonomous-process-cyan.pptx"


SLIDE_DATA = {
    "title": "断网自主作业流程",
    "subtitle": "任务下发后断网 · 机器人本地自主决策与处理",
    "content": {
        "note": "BA-03 business-process loader | offline autonomous handling flow",
        "lanes": ["触发 & 断网", "本地决策", "处理 & 存储"],
        "lane_header_w": 0.92,
        "lane_gap": 0.08,
        "flow_gap": 0.10,
        "left_pad_in": 0.14,
        "right_pad_in": 0.42,
        "columns": 7,
        "col_gap": 0.16,
        # 对齐组A (receive/can_handle/local_done): center_x=8.7  → step x=7.95, decision x=8.05
        # 对齐组B (material_ok/store_local):        center_x=3.0  → step x=2.25, decision x=2.35
        # lane1 三步 center: 1.5 / 5.1 / 8.7
        # lane3 三步 center: 3.0 / 5.85 / 8.7，且终点圆点单独预留右边距
        "step_w": 1.5,
        "step_h": 0.58,
        "nodes": [
            # lane 1 ── 触发 & 断网
            {"id": "start",    "type": "event", "lane": "触发 & 断网", "x_in": 0.05, "start": True},
            {"id": "dispatch", "type": "step",  "lane": "触发 & 断网", "x_in": 0.75,
             "name": "下发任务", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "offline",  "type": "step",  "lane": "触发 & 断网", "x_in": 4.35,
             "name": "断网\n（拔网线）", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "receive",  "type": "step",  "lane": "触发 & 断网", "x_in": 7.95,
             "name": "机器人\n接收任务", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            # lane 2 ── 本地决策
            {"id": "can_handle",  "type": "decision", "lane": "本地决策", "x_in": 8.05,
             "text": "本地能\n处理？", "w_in": 1.3, "h_in": 0.72},
            {"id": "material_ok", "type": "decision", "lane": "本地决策", "x_in": 2.35,
             "text": "素材\n合格？",  "w_in": 1.3, "h_in": 0.72},
            # lane 3 ── 处理 & 存储
            {"id": "store_local", "type": "step", "lane": "处理 & 存储", "x_in": 2.25,
             "name": "本地存储\n（等网络恢复）",
             "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "mark_bad",    "type": "step", "lane": "处理 & 存储", "x_in": 5.10,
             "name": "标记不合格\n等待人工处理",
             "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "local_done",  "type": "step", "lane": "处理 & 存储", "x_in": 7.95,
             "name": "本地处理\n完成", "fill_color": "primary", "line_color": "primary", "text_color": "white"},
            {"id": "end",         "type": "event", "lane": "处理 & 存储", "x_in": 9.55, "end": True},
        ],
        "links": [
            {"from": "start",       "to": "dispatch"},
            {"from": "dispatch",    "to": "offline"},
            {"from": "offline",     "to": "receive"},
            {"from": "receive",     "to": "can_handle",  "start_side": "bottom", "end_side": "top"},
            {"from": "can_handle",  "to": "local_done",  "label": "是 ✓", "start_side": "bottom", "end_side": "top"},
            {"from": "can_handle",  "to": "material_ok", "label": "否 ✗", "start_side": "left",   "end_side": "right"},
            {"from": "material_ok", "to": "store_local", "label": "合格 ✓",  "start_side": "bottom", "end_side": "top"},
            {"from": "material_ok", "to": "mark_bad",    "label": "不合格 ✗", "start_side": "right",  "end_side": "left"},
            {"from": "local_done",  "to": "end"},
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

    from pptx import Presentation

    prs = Presentation(str(OUTPUT))
    print(f"Slides: {len(prs.slides)}")
    slide_w = prs.slide_width
    overflow = sum(
        1 for slide in prs.slides
        for shape in slide.shapes
        if shape.left + shape.width > slide_w
    )
    print(f"Right overflow shapes: {overflow}")


if __name__ == "__main__":
    main()
