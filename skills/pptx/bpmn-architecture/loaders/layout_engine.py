"""
Sugiyama-style layered graph layout engine for BPMN diagrams.

Implements the classic 4-step algorithm:
  1. Cycle removal (DFS-based back-edge reversal)
  2. Layer assignment (longest-path from sources)
  3. Crossing minimization (barycenter heuristic, 24 sweeps)
  4. Coordinate assignment (median positioning + compaction)

Usage:
    from layout_engine import auto_layout

    positions = auto_layout(
        nodes=[{"id": "a"}, {"id": "b", "lane": "L1"}, ...],
        edges=[{"from": "a", "to": "b"}, ...],
        region={"left": 0.6, "top": 1.2, "width": 8.5, "height": 3.8},
        node_sizes={"task": (1.3, 0.55), "event": (0.24, 0.24), "gateway": (0.32, 0.32)},
        lanes=["L1", "L2"],  # optional: force vertical band per lane
    )
    # Returns: {"a": (x_emu, y_emu, w_emu, h_emu), "b": ...}

Isolation: only stdlib, no pptx or skill imports.
"""

from __future__ import annotations
from collections import defaultdict
import sys
from pathlib import Path
from typing import Any, Callable
from pptx.util import Inches

_HERE = Path(__file__).resolve().parent
_SHARED = _HERE.parent.parent / "shared"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from semantic_layout_constraints import apply_semantic_constraints_emu  # pyright: ignore[reportMissingImports]


def emu(inches: float) -> int:
    return int(Inches(inches))


# ── Public API ────────────────────────────────────────────────────────────

def auto_layout(
    nodes: list[dict],
    edges: list[dict],
    region: dict,
    node_sizes: dict | None = None,
    lanes: list[str] | None = None,
    flow_dir: str = "LR",   # LR (left-to-right) or TB (top-to-bottom)
    layout_backend: str = "native",  # native | elk | auto
    backend_options: dict | None = None,
    semantic_constraints: dict | None = None,
) -> dict[str, tuple[int, int, int, int]]:
    """
    Return EMU positions for each node: {id: (left, top, width, height)}.

    Parameters
    ----------
    nodes : list of {"id", "type"?, "lane"?}
    edges : list of {"from", "to", "label"?}
    region : {"left", "top", "width", "height"} in inches
    node_sizes : mapping type → (w_inches, h_inches); defaults provided
    lanes : ordered lane id list; nodes with "lane" field are band-constrained
    flow_dir : "LR" (default) or "TB"
    """
    backend = _normalize_backend(layout_backend)
    opts = backend_options or {}

    if backend == "elk":
        elk_positions = _auto_layout_elk(
            nodes=nodes,
            edges=edges,
            region=region,
            node_sizes=node_sizes,
            lanes=lanes,
            flow_dir=flow_dir,
            backend_options=opts,
        )
        if elk_positions:
            return _apply_semantic_constraints(elk_positions, nodes, region, semantic_constraints)

    native_positions = _auto_layout_native(
        nodes=nodes,
        edges=edges,
        region=region,
        node_sizes=node_sizes,
        lanes=lanes,
        flow_dir=flow_dir,
    )
    return _apply_semantic_constraints(native_positions, nodes, region, semantic_constraints)


def _normalize_backend(layout_backend: str) -> str:
    backend = (layout_backend or "native").strip().lower()
    if backend == "auto":
        return "elk"
    if backend not in {"native", "elk"}:
        return "native"
    return backend


def _auto_layout_native(
    nodes: list[dict],
    edges: list[dict],
    region: dict,
    node_sizes: dict | None,
    lanes: list[str] | None,
    flow_dir: str,
) -> dict[str, tuple[int, int, int, int]]:
    if not nodes:
        return {}

    sizes = _DEFAULT_SIZES.copy()
    if node_sizes:
        sizes.update(node_sizes)

    # Build adjacency
    id_set = {n["id"] for n in nodes}
    adj: dict[str, list[str]] = defaultdict(list)
    in_adj: dict[str, list[str]] = defaultdict(list)
    for e in edges:
        s, t = e["from"], e["to"]
        if s in id_set and t in id_set:
            adj[s].append(t)
            in_adj[t].append(s)

    # Node type lookup
    type_of = {n["id"]: _classify(n) for n in nodes}
    lane_of = {n["id"]: n.get("lane") for n in nodes}

    # ── Step 1: Cycle removal ──
    dag_edges, reversed_set = _remove_cycles(list(id_set), adj)

    # ── Step 2: Layer assignment (longest path from sources) ──
    layers = _assign_layers(list(id_set), dag_edges)

    # ── Step 3: Ordering — barycenter heuristic ──
    layer_order = _minimize_crossings(layers, dag_edges)

    # ── Step 4: Coordinate assignment ──
    positions = _assign_coordinates(
        layer_order, type_of, lane_of, sizes, region, lanes, flow_dir
    )

    return positions


def _auto_layout_elk(
    nodes: list[dict],
    edges: list[dict],
    region: dict,
    node_sizes: dict | None,
    lanes: list[str] | None,
    flow_dir: str,
    backend_options: dict,
) -> dict[str, tuple[int, int, int, int]] | None:
    """Optional ELK adapter hook.

    This function intentionally avoids hard-binding to a specific ELK package.
    If no adapter is provided, caller should safely fall back to native layout.
    """
    adapter = backend_options.get("adapter")
    if not callable(adapter):
        return None

    result = adapter(
        nodes=nodes,
        edges=edges,
        region=region,
        node_sizes=node_sizes or {},
        lanes=lanes or [],
        flow_dir=flow_dir,
        emu_fn=emu,
    )
    if not isinstance(result, dict):
        return None
    return result


def _apply_semantic_constraints(
    positions: dict[str, tuple[int, int, int, int]],
    nodes: list[dict],
    region: dict,
    semantic_constraints: dict | None,
) -> dict[str, tuple[int, int, int, int]]:
    return apply_semantic_constraints_emu(positions, nodes, region, semantic_constraints)


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
        h_in = h / 914400
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
        h_in = h / 914400
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
        # de-duplicate while preserving order
        node_ids = list(dict.fromkeys(node_ids))


        for nid in node_ids:
            if nid not in adjusted:
                continue
            x, y, w, h = adjusted[nid]
            x_in = x / 914400
            y_in = y / 914400
            w_in = w / 914400
            h_in = h / 914400

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


# ── Default node sizes (inches) ──────────────────────────────────────────

_DEFAULT_SIZES = {
    "task":         (1.3,  0.55),
    "event":        (0.24, 0.24),
    "gateway":      (0.32, 0.32),
    "subprocess":   (1.3,  0.55),
}


def _classify(node: dict) -> str:
    t = node.get("type", "task")
    if "event" in t:
        return "event"
    if "gateway" in t:
        return "gateway"
    if "subprocess" in t:
        return "subprocess"
    return "task"


# ── Step 1: Cycle removal (DFS back-edge detection) ─────────────────────

def _remove_cycles(vertices, adj):
    """Return (dag_adj, reversed_edges_set)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in vertices}
    reversed_edges = set()
    dag: dict[str, list[str]] = defaultdict(list)

    def dfs(u):
        color[u] = GRAY
        for v in adj.get(u, []):
            if color[v] == GRAY:
                reversed_edges.add((u, v))
            elif color[v] == WHITE:
                dfs(v)
        color[u] = BLACK

    for v in vertices:
        if color[v] == WHITE:
            dfs(v)

    # Build DAG adjacency
    for u in vertices:
        for v in adj.get(u, []):
            if (u, v) in reversed_edges:
                dag[v].append(u)  # reverse the edge
            else:
                dag[u].append(v)

    return dag, reversed_edges


# ── Step 2: Layer assignment (longest-path from sources) ────────────────

def _assign_layers(vertices, dag):
    """Assign each vertex to a layer index (0 = leftmost)."""
    in_deg = defaultdict(int)
    for u in vertices:
        for v in dag.get(u, []):
            in_deg[v] += 1

    # Topological order via Kahn's
    queue = [v for v in vertices if in_deg[v] == 0]
    topo = []
    visited = set()
    while queue:
        # Sort for determinism
        queue.sort()
        u = queue.pop(0)
        if u in visited:
            continue
        visited.add(u)
        topo.append(u)
        for v in dag.get(u, []):
            in_deg[v] -= 1
            if in_deg[v] == 0 and v not in visited:
                queue.append(v)

    # Assign layer = longest path from any source
    layer = {v: 0 for v in vertices}
    for u in topo:
        for v in dag.get(u, []):
            layer[v] = max(layer[v], layer[u] + 1)

    # Group by layer
    max_layer = max(layer.values()) if layer else 0
    layers = [[] for _ in range(max_layer + 1)]
    for v in vertices:
        layers[layer[v]].append(v)

    return layers


# ── Step 3: Crossing minimization (barycenter + transpose) ──────────────

def _minimize_crossings(layers, dag, iterations=24):
    """Reduce crossings using barycenter heuristic."""
    if len(layers) <= 1:
        return [list(l) for l in layers]

    # Build edge index: layer i→i+1 adjacency
    layer_of = {}
    for i, layer in enumerate(layers):
        for v in layer:
            layer_of[v] = i

    best = [list(l) for l in layers]
    best_crossings = _count_all_crossings(best, dag, layer_of)

    current = [list(l) for l in layers]
    for it in range(iterations):
        # Sweep forward or backward
        if it % 2 == 0:
            sweep = range(1, len(current))
        else:
            sweep = range(len(current) - 2, -1, -1)

        for li in sweep:
            _barycenter_order(current, li, dag, layer_of, forward=(it % 2 == 0))

        _transpose_improve(current, dag, layer_of)

        c = _count_all_crossings(current, dag, layer_of)
        if c < best_crossings:
            best = [list(l) for l in current]
            best_crossings = c

    return best


def _barycenter_order(layers, layer_idx, dag, layer_of, forward=True):
    """Reorder layer[layer_idx] by barycenter of neighbors in adjacent layer."""
    layer = layers[layer_idx]
    if not layer:
        return

    if forward:
        adj_idx = layer_idx - 1
    else:
        adj_idx = layer_idx + 1

    if adj_idx < 0 or adj_idx >= len(layers):
        return

    adj_layer = layers[adj_idx]
    pos = {v: i for i, v in enumerate(adj_layer)}

    bary = {}
    for v in layer:
        neighbors = []
        if forward:
            # Find predecessors in adj_layer
            for u in adj_layer:
                if v in dag.get(u, []):
                    neighbors.append(pos[u])
        else:
            # Find successors in adj_layer
            for w in dag.get(v, []):
                if w in pos:
                    neighbors.append(pos[w])
        if neighbors:
            bary[v] = sum(neighbors) / len(neighbors)
        else:
            bary[v] = pos.get(v, len(adj_layer) / 2)

    layers[layer_idx] = sorted(layer, key=lambda v: bary.get(v, 0))


def _transpose_improve(layers, dag, layer_of):
    """Swap adjacent vertices in each layer if it reduces crossings."""
    improved = True
    while improved:
        improved = False
        for li in range(len(layers)):
            layer = layers[li]
            for j in range(len(layer) - 1):
                # Try swapping j and j+1
                c_before = _count_layer_crossings(layers, li, dag, layer_of)
                layer[j], layer[j + 1] = layer[j + 1], layer[j]
                c_after = _count_layer_crossings(layers, li, dag, layer_of)
                if c_after >= c_before:
                    # Revert
                    layer[j], layer[j + 1] = layer[j + 1], layer[j]
                else:
                    improved = True


def _count_all_crossings(layers, dag, layer_of):
    total = 0
    for li in range(len(layers)):
        total += _count_layer_crossings(layers, li, dag, layer_of)
    return total


def _count_layer_crossings(layers, layer_idx, dag, layer_of):
    """Count edge crossings between layer_idx and layer_idx+1."""
    if layer_idx >= len(layers) - 1:
        return 0

    current = layers[layer_idx]
    next_layer = layers[layer_idx + 1]
    pos_curr = {v: i for i, v in enumerate(current)}
    pos_next = {v: i for i, v in enumerate(next_layer)}

    # Collect edges (pos_in_current, pos_in_next)
    edge_positions = []
    for u in current:
        for v in dag.get(u, []):
            if v in pos_next:
                edge_positions.append((pos_curr[u], pos_next[v]))

    # Count inversions
    crossings = 0
    for i in range(len(edge_positions)):
        for j in range(i + 1, len(edge_positions)):
            a1, b1 = edge_positions[i]
            a2, b2 = edge_positions[j]
            if (a1 - a2) * (b1 - b2) < 0:
                crossings += 1

    return crossings


# ── Step 4: Coordinate assignment ───────────────────────────────────────

def _assign_coordinates(
    layer_order, type_of, lane_of, sizes, region, lanes, flow_dir
):
    """Assign EMU coordinates to each node."""
    r_left = region["left"]
    r_top = region["top"]
    r_width = region["width"]
    r_height = region["height"]

    n_layers = len(layer_order)
    if n_layers == 0:
        return {}

    # Compute max nodes in any layer (for spacing)
    max_per_layer = max(len(l) for l in layer_order)

    # Lane band constraints (vertical bands in LR mode)
    lane_bands = {}
    if lanes:
        band_h = r_height / max(len(lanes), 1)
        for i, lid in enumerate(lanes):
            lane_bands[lid] = r_top + i * band_h + band_h / 2  # center y

    # Layer spacing: distribute node centers evenly across the region.
    # Individual node widths are capped per-slot to prevent overlap.
    if n_layers > 1:
        layer_spacing = r_width / (n_layers - 1)
    else:
        layer_spacing = r_width

    # Per-node overlap prevention constants (inches)
    _INTER_NODE_GAP = 0.12   # minimum clear gap between adjacent node edges
    _MIN_NODE_W     = 0.25   # smallest readable node width

    positions = {}

    for li, layer in enumerate(layer_order):
        if flow_dir == "LR":
            cx = r_left + li * layer_spacing
        else:
            cx = r_left + r_width / 2  # TB mode: center x

        n_in_layer = len(layer)
        if n_in_layer == 0:
            continue

        for vi, nid in enumerate(layer):
            ntype = type_of.get(nid, "task")
            w_in_orig, h_in_orig = sizes.get(ntype, (1.3, 0.55))
            # Cap this node's width to fit in its layer slot (prevents overlap)
            if n_layers > 1 and layer_spacing < w_in_orig + _INTER_NODE_GAP:
                w_in = max(_MIN_NODE_W, layer_spacing - _INTER_NODE_GAP)
                h_in = h_in_orig * (w_in / w_in_orig)
            else:
                w_in, h_in = w_in_orig, h_in_orig

            # Y position: lane-constrained or evenly distributed
            lane_id = lane_of.get(nid)
            if lane_id and lane_id in lane_bands:
                cy = lane_bands[lane_id]
                # Spread multiple nodes within same lane+layer
                same_lane = [n for n in layer if lane_of.get(n) == lane_id]
                idx_in_lane = same_lane.index(nid)
                n_same = len(same_lane)
                if n_same > 1:
                    spread = min(r_height / max(len(lanes or []), 1) * 0.7, h_in * 2)
                    cy += (idx_in_lane - (n_same - 1) / 2) * spread
            else:
                if n_in_layer == 1:
                    cy = r_top + r_height / 2
                else:
                    slot_h = r_height / n_in_layer
                    cy = r_top + vi * slot_h + slot_h / 2

            left = emu(cx - w_in / 2)
            top = emu(cy - h_in / 2)
            w = emu(w_in)
            h = emu(h_in)

            positions[nid] = (left, top, w, h)

    return positions
