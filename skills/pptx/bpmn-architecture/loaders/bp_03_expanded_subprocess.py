"""BP-03 Expanded Sub-Process — BPMN loader.

Renders an expanded sub-process with boundary events and internal flow.
Official anchor: OMG BPMN 2.0 by Example §10.1, E-Mail Voting §12.

Isolation: imports only from local primitives/style_tokens.
"""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (
    emu, add_rounded_rect, add_start_event, add_end_event, add_task,
    add_gateway, add_sequence_flow, add_circle, set_title_subtitle,
    connect_seq, slide_scale,
)
from layout_engine import auto_layout
from style_tokens import resolve_colors, Size, LineWidth, FontSize
from pptx.util import Pt


def load_slide(ctx, data):
    """Render an Expanded Sub-Process (BP-03) slide.

    Supports two config formats:
      A) Flat:  content.nodes[] (incl. expanded_subprocess), content.flows[]
      B) Structured: content.parent_nodes[], content.subprocess{}, content.parent_flows[]
    """
    prs = ctx.prs
    slide = prs.slides.add_slide(_pick_layout(prs))
    C = resolve_colors(ctx.colors)

    set_title_subtitle(slide, data.get("title", ""), data.get("subtitle", ""))

    content = data.get("content", {})

    sx, sy, su = slide_scale(prs)
    margin_l = emu(0.6 * sx)
    base_y = emu(1.5 * sy)

    task_w = emu(Size.TASK_W * su)
    task_h = emu(Size.TASK_H * su)
    ev_d = emu(Size.EVENT_DIAMETER * su)
    gw_s = emu(Size.GATEWAY_SIZE * su)

    node_boxes = {}

    # ------ Detect config format ------
    sp_cfg = content.get("subprocess")
    if sp_cfg:
        # Format B: structured
        parent_nodes = content.get("parent_nodes", [])
        parent_flows = content.get("parent_flows", [])
        boundary_events = sp_cfg.get("boundary_events", [])
        exception_flows = content.get("exception_flows", [])
        sp_id = sp_cfg.get("id", "subprocess")

        # Subprocess rectangle
        sp_x = margin_l + emu(sp_cfg.get("x", 1.5) * sx)
        sp_y = base_y + emu(sp_cfg.get("y", 0.3) * sy)
        sp_w = emu(sp_cfg.get("w", 5.0) * sx)
        sp_h = emu(sp_cfg.get("h", 2.0) * sy)
        sp_shape = add_rounded_rect(slide, sp_x, sp_y, sp_w, sp_h,
                                    fill_rgb=C["white"], line_rgb=C["primary"],
                                    line_width=LineWidth.SUBPROCESS,
                                    corner_radius=Pt(Size.SUBPROCESS_CORNER_RADIUS))
        add_rounded_rect(slide, sp_x + emu(0.1 * sx), sp_y + emu(0.05 * sy),
                 emu(2.0 * sx), emu(0.22 * sy),
                         fill_rgb=None, line_rgb=None,
                         text=sp_cfg.get("label", "Sub-Process"),
                         font_size=FontSize.TASK_LABEL,
                         font_color=C["primary"], bold=True)
        node_boxes[sp_id] = (sp_x + sp_w // 2, sp_y + sp_h // 2,
                             sp_w, sp_h, sp_shape)

        # Internal nodes — auto layout within subprocess rectangle
        itw = emu(Size.TASK_W_COMPACT)
        ith = emu(Size.TASK_H_COMPACT)
        int_nodes = sp_cfg.get("internal_nodes", [])
        int_flows = sp_cfg.get("internal_flows", [])

        # Compute region inside subprocess rect (with padding)
        sp_pad = 0.3 * su
        sp_region = {
            "left": sp_x / 914400 + sp_pad,
            "top": sp_y / 914400 + sp_pad,
            "width": sp_w / 914400 - sp_pad * 2,
            "height": sp_h / 914400 - sp_pad * 2,
        }
        int_positions = auto_layout(
            nodes=int_nodes,
            edges=int_flows,
            region=sp_region,
            node_sizes={
                "task": (Size.TASK_W_COMPACT * su, Size.TASK_H_COMPACT * su),
                "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
                "gateway": (Size.GATEWAY_SIZE * su, Size.GATEWAY_SIZE * su),
            },
        )

        for inode in int_nodes:
            inid = inode["id"]
            if inid not in int_positions:
                continue
            ix, iy, iw, ih = int_positions[inid]
            icx = ix + iw // 2
            icy = iy + ih // 2
            itype = inode.get("type", "task")
            if itype == "start_event":
                s = add_start_event(slide, icx, icy, C, ev_d)
                node_boxes[inid] = (icx, icy, ev_d, ev_d, s)
            elif itype == "end_event":
                s = add_end_event(slide, icx, icy, C, ev_d)
                node_boxes[inid] = (icx, icy, ev_d, ev_d, s)
            elif "gateway" in itype:
                gtype = itype.replace("_gateway", "")
                s = add_gateway(slide, icx, icy, C, gateway_type=gtype, size=gw_s)
                node_boxes[inid] = (icx, icy, gw_s, gw_s, s)
            else:
                s = add_task(slide, ix, iy, iw, ih, C,
                             label=inode.get("label", ""), task_type=itype)
                node_boxes[inid] = (ix + iw // 2, iy + ih // 2, iw, ih, s)

        # Internal flows
        for iflow in sp_cfg.get("internal_flows", []):
            connect_seq(slide, node_boxes, iflow["from"], iflow["to"], C,
                        label=iflow.get("label", ""))

        # Parent nodes — auto layout in the full slide region
        all_parent_and_sp = parent_nodes + [{"id": sp_id, "type": "subprocess"}]
        parent_flows_ext = list(parent_flows)
        parent_region = {
            "left": 0.4 * sx, "top": base_y / 914400,
            "width": 9.0 * sx, "height": sp_h / 914400 + 0.6 * sy,
        }
        parent_positions = auto_layout(
            nodes=all_parent_and_sp,
            edges=parent_flows_ext,
            region=parent_region,
            node_sizes={
                "task": (Size.TASK_W * su, Size.TASK_H * su),
                "event": (Size.EVENT_DIAMETER * su, Size.EVENT_DIAMETER * su),
                "subprocess": (sp_w / 914400, sp_h / 914400),
            },
        )

        for pn in parent_nodes:
            nid = pn["id"]
            if nid not in parent_positions:
                continue
            px, py, pw, ph = parent_positions[nid]
            pcx = px + pw // 2
            # Align parent nodes vertically to subprocess center
            pcy = sp_y + sp_h // 2
            ntype = pn.get("type", "task")
            if ntype == "start_event":
                s = add_start_event(slide, pcx, pcy, C, ev_d)
                node_boxes[nid] = (pcx, pcy, ev_d, ev_d, s)
            elif ntype == "end_event":
                s = add_end_event(slide, pcx, pcy, C, ev_d)
                node_boxes[nid] = (pcx, pcy, ev_d, ev_d, s)
            else:
                s = add_task(slide, px, pcy - task_h // 2, task_w, task_h, C,
                             label=pn.get("label", ""), task_type=ntype)
                node_boxes[nid] = (px + task_w // 2, pcy, task_w, task_h, s)

        # Parent flows
        for flow in parent_flows:
            connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                        label=flow.get("label", ""))

        # Boundary events
        for bev in boundary_events:
            bev_d = emu(Size.EVENT_DIAMETER * su)
            bev_type = bev.get("type", "timer_boundary")
            if "error" in bev_type:
                color, marker = C["error"], "\u26a1"
            elif "timer" in bev_type:
                color, marker = C["timer"], "\u23f0"
            else:
                color, marker = C["dark"], "!"
            bx = sp_x + sp_w // 3 + boundary_events.index(bev) * emu(1.5 * sx)
            by = sp_y + sp_h - bev_d // 2
            s = add_circle(slide, bx, by, bev_d, fill_rgb=C["white"],
                           line_rgb=color, line_width=Pt(1.5),
                           text=marker, font_size=Pt(7))
            node_boxes[bev["id"]] = (bx, by, bev_d, bev_d, s)

        # Exception flows
        for ef in exception_flows:
            src = node_boxes.get(ef["from"])
            if src:
                ex = src[0]
                ey = src[1] + src[3] // 2 + emu(0.3 * sy)
                add_task(slide, ex - emu(0.5 * sx), ey, emu(1.0 * sx), emu(0.4 * sy), C,
                         label=ef.get("label", ef.get("to", "Handle")))

    else:
        # Format A: flat nodes[] / flows[]
        nodes = content.get("nodes", [])
        flows = content.get("flows", [])
        boundary_events = content.get("boundary_events", [])

        for node in nodes:
            nid = node["id"]
            ntype = node.get("type", "task")
            if ntype == "expanded_subprocess":
                sp_x = margin_l + emu(node.get("x_in", 2.0) * sx)
                sp_y = base_y + emu(node.get("y_in", 0.3) * sy)
                sp_w = emu(node.get("width_in", 4.0) * sx)
                sp_h = emu(node.get("height_in", 1.5) * sy)
                add_rounded_rect(slide, sp_x, sp_y, sp_w, sp_h,
                                 fill_rgb=C["white"], line_rgb=C["primary"],
                                 line_width=LineWidth.SUBPROCESS,
                                 corner_radius=Pt(Size.SUBPROCESS_CORNER_RADIUS))
                add_rounded_rect(slide, sp_x + emu(0.1 * sx), sp_y + emu(0.05 * sy),
                                 emu(1.5 * sx), emu(0.2 * sy), fill_rgb=None, line_rgb=None,
                                 text=node.get("label", "Sub-Process"),
                                 font_size=FontSize.TASK_LABEL,
                                 font_color=C["primary"], bold=True)
                node_boxes[nid] = (sp_x + sp_w // 2, sp_y + sp_h // 2,
                                   sp_w, sp_h, None)
                for inode in node.get("internal_nodes", []):
                    inid = inode["id"]
                    ix = sp_x + emu(inode.get("x_in", 0.2) * sx)
                    iy = sp_y + sp_h // 2 - task_h // 2
                    itype = inode.get("type", "task")
                    itw = emu(Size.TASK_W_COMPACT * su)
                    ith = emu(Size.TASK_H_COMPACT * su)
                    if itype == "start_event":
                        cx2, cy2 = ix + ev_d // 2, iy + task_h // 2
                        s = add_start_event(slide, cx2, cy2, C, ev_d)
                        node_boxes[inid] = (cx2, cy2, ev_d, ev_d, s)
                    elif itype == "end_event":
                        cx2, cy2 = ix + ev_d // 2, iy + task_h // 2
                        s = add_end_event(slide, cx2, cy2, C, ev_d)
                        node_boxes[inid] = (cx2, cy2, ev_d, ev_d, s)
                    else:
                        s = add_task(slide, ix, iy, itw, ith, C,
                                     label=inode.get("label", ""), task_type=itype)
                        node_boxes[inid] = (ix + itw // 2, iy + ith // 2,
                                            itw, ith, s)
                for iflow in node.get("internal_flows", []):
                    connect_seq(slide, node_boxes, iflow["from"], iflow["to"], C)
            else:
                x = margin_l + emu(node.get("x_in", 0) * sx)
                y = base_y + emu(node.get("y_in", 0.8) * sy)
                if ntype == "start_event":
                    cx2, cy2 = x + ev_d // 2, y + task_h // 2
                    s = add_start_event(slide, cx2, cy2, C, ev_d)
                    node_boxes[nid] = (cx2, cy2, ev_d, ev_d, s)
                elif ntype == "end_event":
                    cx2, cy2 = x + ev_d // 2, y + task_h // 2
                    s = add_end_event(slide, cx2, cy2, C, ev_d)
                    node_boxes[nid] = (cx2, cy2, ev_d, ev_d, s)
                else:
                    s = add_task(slide, x, y, task_w, task_h, C,
                                 label=node.get("label", ""), task_type=ntype)
                    node_boxes[nid] = (x + task_w // 2, y + task_h // 2,
                                       task_w, task_h, s)

        for flow in flows:
            connect_seq(slide, node_boxes, flow["from"], flow["to"], C,
                        label=flow.get("label", ""))

    return slide


def _pick_layout(prs):
    for layout in prs.slide_layouts:
        name = (layout.name or "").lower()
        if any(k in name for k in ["内容", "content", "blank"]):
            return layout
    return prs.slide_layouts[min(2, len(prs.slide_layouts) - 1)]
