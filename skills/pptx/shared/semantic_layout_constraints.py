"""Shared semantic layout constraints for flow-like diagrams.

This module applies semantic post-processing to EMU node boxes so different
skills can share the same branch/lane/container behaviors.
"""

from __future__ import annotations

EMU_PER_INCH = 914400.0


def emu(inches: float) -> int:
    return int(inches * EMU_PER_INCH)


def apply_semantic_constraints_emu(
    positions: dict[str, tuple[int, int, int, int]],
    nodes: list[dict],
    region: dict,
    semantic_constraints: dict | None,
) -> dict[str, tuple[int, int, int, int]]:
    """Apply semantic constraints to EMU node boxes.

    Args:
        positions: Mapping id -> (left, top, width, height) in EMU.
        nodes: Source node data list.
        region: Layout region in inches with left/top/width/height.
        semantic_constraints: Constraint dict with optional keys:
            lane_attr/lane_order, branch_attr, container_regions/container_attr.
    """
    if not semantic_constraints:
        return positions

    constrained = dict(positions)

    lane_attr = semantic_constraints.get("lane_attr")
    lane_order = semantic_constraints.get("lane_order")
    if lane_attr and lane_order:
        constrained = _apply_lane_bands(constrained, nodes, region, lane_attr, lane_order)

    branch_attr = semantic_constraints.get("branch_attr")
    if branch_attr:
        constrained = _apply_branch_attr_spread(constrained, nodes, region, semantic_constraints)

    container_regions = semantic_constraints.get("container_regions")
    if container_regions:
        constrained = _apply_container_clamp(
            constrained,
            nodes,
            container_regions,
            semantic_constraints.get("container_attr"),
        )

    return constrained


def _apply_branch_attr_spread(
    positions: dict[str, tuple[int, int, int, int]],
    nodes: list[dict],
    region: dict,
    constraints: dict,
) -> dict[str, tuple[int, int, int, int]]:
    branch_attr = constraints.get("branch_attr")
    if not branch_attr:
        return positions

    values = sorted({n.get(branch_attr) for n in nodes if n.get(branch_attr) is not None})
    if not values:
        return positions

    index = {value: i for i, value in enumerate(values)}
    count = len(values)

    center_ratio = float(constraints.get("branch_center_ratio", 0.52))
    spread_ratio = float(constraints.get("branch_spread_ratio", 0.28))
    spread_max_in = float(constraints.get("branch_spread_max_in", 0.66))

    r_top = float(region["top"])
    r_h = float(region["height"])
    center_y = r_top + r_h * center_ratio
    spread = min(r_h * spread_ratio, spread_max_in)

    if count == 1:
        offsets = {values[0]: 0.0}
    else:
        step = (spread * 2.0) / (count - 1)
        offsets = {v: (-spread + index[v] * step) for v in values}

    adjusted = dict(positions)
    node_by_id = {n.get("id"): n for n in nodes}

    for nid, box in positions.items():
        node = node_by_id.get(nid)
        if not node:
            continue
        val = node.get(branch_attr)
        if val is None or val not in offsets:
            continue
        left, top, w, h = box
        h_in = h / EMU_PER_INCH
        new_top = emu(center_y + offsets[val] - h_in / 2.0)
        adjusted[nid] = (left, new_top, w, h)

    return adjusted


def _apply_lane_bands(
    positions: dict[str, tuple[int, int, int, int]],
    nodes: list[dict],
    region: dict,
    lane_attr: str,
    lane_order: list[str],
) -> dict[str, tuple[int, int, int, int]]:
    if not lane_order:
        return positions

    lane_index = {lid: i for i, lid in enumerate(lane_order)}
    lane_count = max(1, len(lane_order))
    r_top = float(region["top"])
    r_h = float(region["height"])
    band_h = r_h / lane_count

    node_by_id = {n.get("id"): n for n in nodes}
    adjusted = dict(positions)

    for nid, box in positions.items():
        node = node_by_id.get(nid)
        if not node:
            continue
        lane_id = node.get(lane_attr)
        if lane_id not in lane_index:
            continue
        idx = lane_index[lane_id]
        left, top, w, h = box
        h_in = h / EMU_PER_INCH
        center_y = r_top + idx * band_h + band_h / 2.0
        new_top = emu(center_y - h_in / 2.0)
        adjusted[nid] = (left, new_top, w, h)

    return adjusted


def _apply_container_clamp(
    positions: dict[str, tuple[int, int, int, int]],
    nodes: list[dict],
    container_regions: list[dict],
    container_attr: str | None = None,
) -> dict[str, tuple[int, int, int, int]]:
    adjusted = dict(positions)
    node_by_id = {n.get("id"): n for n in nodes if n.get("id")}

    regions_by_id = {}
    ordered = []
    for idx, r in enumerate(container_regions):
        rid = r.get("id") or f"container_{idx}"
        entry = dict(r)
        entry["id"] = rid
        regions_by_id[rid] = entry
        ordered.append(entry)

    def _bounds(region_entry):
        left = float(region_entry.get("left", 0.0))
        top = float(region_entry.get("top", 0.0))
        width = float(region_entry.get("width", 0.0))
        height = float(region_entry.get("height", 0.0))
        if width <= 0 or height <= 0:
            return None
        min_x = left
        min_y = top
        max_x = left + width
        max_y = top + height

        parent_id = region_entry.get("parent_id")
        if parent_id and parent_id in regions_by_id:
            parent = _bounds(regions_by_id[parent_id])
            if parent is not None:
                pmin_x, pmin_y, pmax_x, pmax_y = parent
                min_x = max(min_x, pmin_x)
                min_y = max(min_y, pmin_y)
                max_x = min(max_x, pmax_x)
                max_y = min(max_y, pmax_y)

        return (min_x, min_y, max_x, max_y)

    cached_bounds = {r["id"]: _bounds(r) for r in ordered}

    for region in ordered:
        bounds = cached_bounds.get(region["id"])
        if bounds is None:
            continue
        min_x, min_y, max_x, max_y = bounds

        pad = float(region.get("padding_in", 0.0))
        min_x += pad
        min_y += pad
        max_x -= pad
        max_y -= pad
        if max_x <= min_x or max_y <= min_y:
            continue

        node_ids = list(region.get("node_ids", []))
        if container_attr:
            node_ids.extend([
                nid for nid, node in node_by_id.items()
                if node.get(container_attr) == region["id"]
            ])
        node_ids = list(dict.fromkeys(node_ids))

        for nid in node_ids:
            if nid not in adjusted:
                continue
            x, y, w, h = adjusted[nid]
            x_in = x / EMU_PER_INCH
            y_in = y / EMU_PER_INCH
            w_in = w / EMU_PER_INCH
            h_in = h / EMU_PER_INCH

            if x_in < min_x:
                x_in = min_x
            if y_in < min_y:
                y_in = min_y
            if x_in + w_in > max_x:
                x_in = max(min_x, max_x - w_in)
            if y_in + h_in > max_y:
                y_in = max(min_y, max_y - h_in)

            adjusted[nid] = (emu(x_in), emu(y_in), w, h)

    return adjusted