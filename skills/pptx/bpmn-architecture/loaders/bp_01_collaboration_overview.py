"""BP-01 Collaboration Overview — BPMN loader.

Renders a multi-pool collaboration diagram with message flows.
Official anchor: OMG BPMN 2.0 by Example — Pizza Collaboration.

Isolation: imports only from local primitives/style_tokens. No cross-skill refs.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, mid_x, mid_y, add_rounded_rect, add_start_event, add_end_event,
    add_task, add_gateway, add_sequence_flow, add_message_flow,
    add_pool_header, add_lane_header, set_title_subtitle,
    edge_endpoints, connect_seq, connect_msg, slide_scale,
)
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Inches, Pt


def load_slide(ctx, data):
    """Render a Collaboration Overview (BP-01) slide.

    Config format (nested pools):
        content.pools[]:
            id, name,
            tasks[]: {id, label, type}
            flows[]: {from, to, label?}
        content.message_flows[]:
            {from_pool, from_task, to_pool, to_task, label?}
    """
    prs = ctx.prs
    layout = _pick_layout(prs)
    slide = prs.slides.add_slide(layout)
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    pools = content.get("pools", [])
    msg_flows = content.get("message_flows", [])

    # --- Layout geometry ---
    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.5 * sx)
    margin_t = emu(1.0 * sy)
    avail_w = emu(9.0 * sx)
    pool_count = max(len(pools), 1)
    pool_gap = emu(Size.POOL_GAP * sy)
    total_h = emu(4.2 * sy)
    pool_h = (total_h - pool_gap * (pool_count - 1)) // pool_count
    header_w = emu(Size.POOL_HEADER_W * sx)

    task_w = emu(Size.TASK_W * su)
    task_h = emu(Size.TASK_H * su)
    ev_d = emu(Size.EVENT_DIAMETER * su)

    pool_regions = {}
    all_shapes = {}  # node_id -> (cx, cy, w, h, shape)

    for i, pool in enumerate(pools):
        pid = pool.get("id", f"pool_{i}")
        py = margin_t + i * (pool_h + pool_gap)

        # Pool border
        add_rounded_rect(slide, margin_l, py, avail_w, pool_h,
                         fill_rgb=C["white"],
                         line_rgb=C["dark"], line_width=LineWidth.POOL_BORDER,
                         corner_radius=Pt(0))
        # Pool header
        add_pool_header(slide, margin_l, py, header_w, pool_h, C,
                        name=pool.get("name", pid))

        reg = {
            "left": margin_l + header_w,
            "top": py,
            "width": avail_w - header_w,
            "height": pool_h,
        }
        pool_regions[pid] = reg

        # --- Place tasks within pool ---
        tasks = pool.get("tasks", [])
        n = len(tasks)
        if n == 0:
            continue

        # Content area with padding
        pad = emu(0.15 * su)
        content_left = reg["left"] + pad
        content_right = reg["left"] + reg["width"] - pad
        content_w = content_right - content_left

        # Items: start_event + n tasks + end_event
        items = n + 2
        slot_w = content_w // items
        effective_task_w = min(task_w, int(slot_w * 0.78))
        cy = reg["top"] + reg["height"] // 2

        # Start event
        se_cx = content_left + slot_w // 2
        se_shape = add_start_event(slide, se_cx, cy, C, ev_d)
        start_id = f"__start_{pid}"
        all_shapes[start_id] = (se_cx, cy, ev_d, ev_d, se_shape)

        # Tasks
        for j, task in enumerate(tasks):
            tid = task["id"]
            tx = content_left + (j + 1) * slot_w + (slot_w - effective_task_w) // 2
            ty = cy - task_h // 2
            shape = add_task(slide, tx, ty, effective_task_w, task_h, C,
                             label=task.get("label", ""),
                             task_type=task.get("type", "task"))
            all_shapes[tid] = (tx + effective_task_w // 2, cy,
                               effective_task_w, task_h, shape)

        # End event
        ee_cx = content_left + (n + 1) * slot_w + slot_w // 2
        ee_shape = add_end_event(slide, ee_cx, cy, C, ev_d)
        end_id = f"__end_{pid}"
        all_shapes[end_id] = (ee_cx, cy, ev_d, ev_d, ee_shape)

        # --- Sequence flows ---
        # Auto-connect: start → first task
        connect_seq(slide, all_shapes, start_id, tasks[0]["id"], C)
        # Explicit flows from config
        for flow in pool.get("flows", []):
            connect_seq(slide, all_shapes, flow["from"], flow["to"], C,
                        label=flow.get("label", ""))
        # Auto-connect: last task → end
        connect_seq(slide, all_shapes, tasks[-1]["id"], end_id, C)

    # --- Message flows (between pools) ---
    for mf in msg_flows:
        src_id = mf.get("from") or mf.get("from_task")
        dst_id = mf.get("to") or mf.get("to_task")
        connect_msg(slide, all_shapes, src_id, dst_id, C,
                    label=mf.get("label", ""))

    return slide


def _pick_layout(prs):
    """Pick a content layout from the presentation."""
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
