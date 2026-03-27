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
from pptx.util import Inches


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
