"""BP-09 Compensation and Transaction Pattern — BPMN loader.

Renders a Transaction Sub-Process with compensation handlers.
Official anchor: OMG BPMN 2.0.2 §10.7, §10.2.4, Examples §12 E-Mail Voting.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event, add_task,
    add_circle, add_sequence_flow, add_association, set_title_subtitle,
    connect_seq, edge_endpoints, slide_scale,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render a Compensation and Transaction Pattern (BP-09) slide."""
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})
    tx = content.get("transaction", {})
    comp_handlers = content.get("compensation_handlers", [])
    boundary_events = content.get("boundary_events", [])
    exception_flows = content.get("exception_flows", [])

    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.6 * sx)
    base_y = emu(1.2 * sy)

    # --- Transaction Sub-Process (double border) ---
    tx_x = margin_l + emu(1.5 * sx)
    tx_y = base_y
    tx_w = emu(6.0 * sx)
    tx_h = emu(1.8 * sy)

    # Outer border
    add_rounded_rect(slide, tx_x, tx_y, tx_w, tx_h,
                     fill_rgb=C["white"],
                     line_rgb=C["primary"],
                     line_width=LineWidth.TRANSACTION_OUTER,
                     corner_radius=Pt(5))
    # Inner border (2px inset)
    inset = emu(0.04 * su)
    add_rounded_rect(slide, tx_x + inset, tx_y + inset,
                     tx_w - 2 * inset, tx_h - 2 * inset,
                     fill_rgb=None,
                     line_rgb=C["primary"],
                     line_width=LineWidth.TRANSACTION_INNER,
                     corner_radius=Pt(4))

    # Transaction label
    add_rounded_rect(slide, tx_x + emu(0.15 * sx), tx_y + emu(0.08 * sy),
                     emu(2.0 * sx), emu(0.22 * sy),
                     fill_rgb=None, line_rgb=None,
                     text=tx.get("label", "Transaction"),
                     font_size=Pt(9), font_color=C["primary"], bold=True)

    # Internal nodes — auto layout within transaction rectangle
    int_nodes = tx.get("internal_nodes", [])
    int_flows = tx.get("internal_flows", [])
    ev_d = emu(Size.EVENT_DIAMETER * su)
    task_w = emu(Size.TASK_W_COMPACT * su)
    task_h = emu(Size.TASK_H_COMPACT * su)
    node_boxes = {}

    tx_pad = 0.3 * su
    tx_region = {
        "left": tx_x / 914400 + tx_pad,
        "top": tx_y / 914400 + tx_pad,
        "width": tx_w / 914400 - tx_pad * 2,
        "height": tx_h / 914400 - tx_pad * 2,
    }
    int_positions = auto_layout(
        nodes=int_nodes,
        edges=int_flows,
        region=tx_region,
        node_sizes={
            "task": (Size.TASK_W_COMPACT * su, Size.TASK_H_COMPACT * su),
            "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
            "gateway": (Size.GATEWAY_SIZE * su, Size.GATEWAY_SIZE * su),
        },
    )

    for node in int_nodes:
        nid = node["id"]
        if nid not in int_positions:
            continue
        nx, ny, nw, nh = int_positions[nid]
        ncx = nx + nw // 2
        ncy = ny + nh // 2

        ntype = node.get("type", "task")
        if ntype == "start_event":
            s = add_start_event(slide, ncx, ncy, C, ev_d)
            node_boxes[nid] = (ncx, ncy, ev_d, ev_d, s)
        elif ntype == "end_event":
            s = add_end_event(slide, ncx, ncy, C, ev_d)
            node_boxes[nid] = (ncx, ncy, ev_d, ev_d, s)
        elif ntype == "cancel_end_event":
            s = add_circle(slide, ncx, ncy, ev_d, fill_rgb=None,
                               line_rgb=C["cancel"], line_width=Pt(3),
                               text="\u00d7", font_size=Pt(8))
            node_boxes[nid] = (ncx, ncy, ev_d, ev_d, s)
        else:
            s = add_task(slide, nx, ny, nw, nh, C,
                     label=node.get("label", ""), task_type=ntype)
            node_boxes[nid] = (nx + nw // 2, ny + nh // 2, nw, nh, s)

    # Internal flows
    # Internal flows
    for fl in int_flows:
        connect_seq(slide, node_boxes, fl["from"], fl["to"], C)

    # --- Pre/Post transaction nodes ---
    # Start event before transaction
    start_x = margin_l
    start_cy = tx_y + tx_h // 2
    add_start_event(slide, start_x + ev_d // 2, start_cy, C, ev_d)
    add_sequence_flow(slide, start_x + ev_d, start_cy, tx_x, start_cy, C)

    # End event after transaction
    end_x = tx_x + tx_w + emu(0.5 * sx)
    add_end_event(slide, end_x + ev_d // 2, start_cy, C, ev_d)
    add_sequence_flow(slide, tx_x + tx_w, start_cy, end_x, start_cy, C)

    # --- Boundary events ---
    bev_y = tx_y + tx_h
    for i, bev in enumerate(boundary_events):
        bev_x = tx_x + tx_w // 3 + i * emu(1.5 * sx)
        bev_d = emu(Size.EVENT_DIAMETER * su)
        btype = bev.get("type", "cancel_boundary")
        if "cancel" in btype:
            color = C["cancel"]
            marker = "×"
        elif "error" in btype:
            color = C["error"]
            marker = "⚡"
        else:
            color = C["dark"]
            marker = "!"
        add_circle(slide, bev_x, bev_y - bev_d // 2, bev_d,
                   fill_rgb=C["white"],
                   line_rgb=color, line_width=Pt(1.5),
                   text=marker, font_size=Pt(7))
        node_boxes[bev["id"]] = (bev_x, bev_y, bev_d, bev_d)

    # --- Compensation handlers ---
    handler_y = tx_y + tx_h + emu(0.6 * sy)
    for j, ch in enumerate(comp_handlers):
        activity_id = ch.get("activity")
        handler = ch.get("handler", {})
        # Find activity position
        act_box = node_boxes.get(activity_id)
        if not act_box:
            continue
        hx = act_box[0] - emu(0.5 * sx)
        hy = handler_y
        h_w = emu(1.0 * sx)
        h_h = emu(0.4 * sy)
        # Compensation handler box (amber tint)
        add_rounded_rect(slide, hx, hy, h_w, h_h,
                         fill_rgb=_lighten(C["compensation"], 0.85),
                         line_rgb=C["compensation"],
                         line_width=Pt(1), corner_radius=Pt(3),
                         text=handler.get("label", "Undo"),
                         font_size=Pt(7))
        # Association line (dotted) from activity to handler
        add_association(slide, act_box[0], act_box[1] + act_box[3] // 2,
                        hx + h_w // 2, hy, C)
        # Compensation marker at association start
        comp_d = emu(0.15 * su)
        add_circle(slide, act_box[0] - comp_d // 2,
                   act_box[1] + act_box[3] // 2 + emu(0.05),
                   comp_d, fill_rgb=C["white"],
                   line_rgb=C["compensation"], line_width=Pt(1),
                   text="⟲", font_size=Pt(6))

    # --- Exception flows ---
    for ef in exception_flows:
        src = node_boxes.get(ef["from"])
        if src:
            ex = src[0] + emu(0.3 * sx)
            ey = src[1] + src[3] // 2 + emu(0.3 * sy)
            add_task(slide, ex, ey, emu(1.2 * sx), emu(0.4 * sy), C,
                     label=ef.get("label", "Handle"))

    return slide


def _lighten(rgb_tuple, factor=0.85):
    """Lighten an RGB tuple toward white."""
    return tuple(int(c + (255 - c) * factor) for c in rgb_tuple)


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
