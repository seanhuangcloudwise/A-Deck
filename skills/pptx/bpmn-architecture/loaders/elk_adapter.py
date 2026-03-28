"""Optional ELK layered adapter for BPMN auto_layout backend.

This module keeps hard dependency optional:
- Requires Node.js + elkjs at runtime only when layout_backend='elk'.
- Returns None on any adapter failure so caller can safely fallback to native.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

RUNNER = Path(__file__).resolve().parent / "elk_layered_runner.js"
_ELK_UNITS_PER_INCH = 120.0


def _classify(node: dict) -> str:
    t = str(node.get("type", "task"))
    if "event" in t:
        return "event"
    if "gateway" in t:
        return "gateway"
    if "subprocess" in t:
        return "subprocess"
    return "task"


def elk_layered_adapter(
    *,
    nodes: list[dict],
    edges: list[dict],
    region: dict,
    node_sizes: dict,
    lanes: list[str],
    flow_dir: str,
    emu_fn,
):
    if not RUNNER.exists() or not nodes:
        return None

    size_by_type = {
        "task": node_sizes.get("task", (1.3, 0.55)),
        "event": node_sizes.get("event", (0.24, 0.24)),
        "gateway": node_sizes.get("gateway", (0.32, 0.32)),
        "subprocess": node_sizes.get("subprocess", node_sizes.get("task", (1.3, 0.55))),
    }

    payload = {
        "flow_dir": flow_dir,
        "nodes": [],
        "edges": [],
    }

    node_index = {}
    for n in nodes:
        nid = n.get("id")
        if not nid:
            continue
        ntype = _classify(n)
        w, h = size_by_type.get(ntype, (1.3, 0.55))
        payload["nodes"].append({
            "id": nid,
            "width": float(w) * _ELK_UNITS_PER_INCH,
            "height": float(h) * _ELK_UNITS_PER_INCH,
        })
        node_index[nid] = n

    for i, e in enumerate(edges or []):
        s = e.get("from")
        t = e.get("to")
        if s in node_index and t in node_index:
            payload["edges"].append({
                "id": f"e_{i}",
                "source": s,
                "target": t,
            })

    if not payload["nodes"]:
        return None

    try:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(payload, f)
            json_path = f.name

        proc = subprocess.run(
            ["node", str(RUNNER), json_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return None

        result = json.loads(proc.stdout)
        children = result.get("children", [])
        if not children:
            return None

        return _normalize_positions(children, region, emu_fn)
    except Exception:
        return None


def _normalize_positions(children: list[dict], region: dict, emu_fn):
    xs = [float(c.get("x", 0.0)) for c in children]
    ys = [float(c.get("y", 0.0)) for c in children]
    x2 = [float(c.get("x", 0.0)) + float(c.get("width", 0.0)) for c in children]
    y2 = [float(c.get("y", 0.0)) + float(c.get("height", 0.0)) for c in children]

    min_x, min_y = min(xs), min(ys)
    max_x, max_y = max(x2), max(y2)

    graph_w = max(0.01, max_x - min_x)
    graph_h = max(0.01, max_y - min_y)

    r_left = float(region["left"])
    r_top = float(region["top"])
    r_w = float(region["width"])
    r_h = float(region["height"])

    # Keep a conservative inner safe box to absorb connector labels/arrow caps.
    safe_pad_x = min(0.18, max(0.04, r_w * 0.06))
    safe_pad_y = min(0.12, max(0.03, r_h * 0.06))
    s_left = r_left + safe_pad_x
    s_top = r_top + safe_pad_y
    s_w = max(0.2, r_w - 2 * safe_pad_x)
    s_h = max(0.2, r_h - 2 * safe_pad_y)

    scale = min(s_w / graph_w, s_h / graph_h)
    scale = max(1e-4, scale)
    scale *= 0.92

    used_w = graph_w * scale
    used_h = graph_h * scale
    pad_x = (s_w - used_w) / 2.0
    pad_y = (s_h - used_h) / 2.0

    out = {}
    for c in children:
        nid = c.get("id")
        if not nid:
            continue
        left = s_left + (float(c.get("x", 0.0)) - min_x) * scale + pad_x
        top = s_top + (float(c.get("y", 0.0)) - min_y) * scale + pad_y
        w = float(c.get("width", 0.0)) * scale
        h = float(c.get("height", 0.0)) * scale
        out[nid] = (emu_fn(left), emu_fn(top), emu_fn(w), emu_fn(h))

    return out
