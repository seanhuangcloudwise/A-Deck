# BPMN Skill Isolation Rules

This document defines non-negotiable implementation boundaries.

## Loader Isolation

- Every BPMN diagram has its own loader module.
- Loader filename pattern: bp_XX_<name>.py
- Each loader exposes only one entrypoint:
  - load_slide(ctx, data)

## No Cross-Skill References

Forbidden imports:
- skills/pptx/shared/*
- skills/pptx/gtm-architecture/*
- skills/pptx/roadmap-architecture/*
- skills/pptx/togaf-architecture/*

Allowed imports:
- Python standard library
- python-pptx
- local package modules under skills/pptx/bpmn-architecture/*

## Local Primitives Only

All BPMN shape and connector primitives must be implemented locally under this skill.
Required local modules:
- loaders/primitives.py — shape/connector drawing + smart anchor selection
- loaders/style_tokens.py — semantic colors, sizing, fonts
- loaders/layout_engine.py — Sugiyama graph layout algorithm

Required geometry helpers in `loaders/primitives.py`:
- `slide_size_in(prs)` — returns actual slide width/height in inches
- `slide_scale(prs)` — returns input-space scaling factors for current master
- `scaled_region(prs, left, top, width, height)` — converts base-canvas region to current master input region

## Data Contract

Minimal loader contract:

- title: str
- subtitle: str
- content: object

Common content keys:
- pools
- lanes
- nodes
- flows
- message_flows
- annotations

## Layout Engine — Mandatory Rules

**All loaders that render nodes + flows MUST use `auto_layout()` from `layout_engine.py`.**
Do not hardcode `x_in` / `y_in` pixel positions; let the layout engine compute positions.

### auto_layout() contract
```python
from layout_engine import auto_layout

positions = auto_layout(
    nodes=[{"id": "...", "type": "...", "lane": "..."}],
    edges=[{"from": "...", "to": "..."}],
    region={"left": float, "top": float, "width": float, "height": float},  # inches
    node_sizes={"task": (w, h), "event": (d, d), "gateway": (s, s)},       # inches
    lanes=["lane_id_1", "lane_id_2"],  # optional, ordered list
)
# Returns {node_id: (left_emu, top_emu, width_emu, height_emu)}
```

### Anti-overlap guarantee
The layout engine caps each node's rendered width to `layer_spacing - 0.12"` so that no two
peer nodes at adjacent x-positions overlap, regardless of how many layers exist.
Loaders must use `w, h` from position output — not their own hardcoded task_w/task_h — when
drawing task boxes, so the cap is honoured.

### Exceptions (specialized layouts, no auto_layout)
- BP-01: pool-slot evenly spaced (start → n tasks → end per pool)
- BP-06: choreography band (initiator/center/responder stacked rectangle)
- BP-07: conversation ring (participants polar-placed, hexagons at centroid)

## Master Size Adaptation — Mandatory Rules

**All BPMN loaders MUST adapt to the active master size.**
Do not assume the slide is always `10.0" × 5.625"`.

### Base canvas
The BPMN skill uses a **base logical canvas** of `10.0" × 5.625"` for authoring geometry.
All hardcoded layout constants in specs/loaders are interpreted relative to this base canvas.

### Adaptation helpers
Loaders must derive geometry through the shared helpers in `primitives.py`:

```python
from primitives import slide_scale, scaled_region

sx, sy, su = slide_scale(prs)
region = scaled_region(prs, 0.6, 1.5, 8.5, 3.0)
```

### Cloudwise master compensation rule
Cloudwise masters have an observed **horizontal render stretch** in the template pipeline.
To avoid double-scaling BPMN content:

- **X/input width scale** is kept at base-canvas scale (`sx = 1.0`)
- **Y/input height scale** adapts to the actual slide height (`sy = slide_h / 5.625`)
- **Uniform node size scale** remains base size (`su = 1.0`)

This is a rendering compensation rule, not a BPMN semantic rule. All BPMN loaders must follow it.

### What must be adaptive
- outer content region (`left/top/width/height`)
- pool/lane heights and vertical offsets
- vertical annotations and boundary-event offsets
- specialized layouts such as choreography base line and conversation center/radius

### What must NOT be independently re-scaled in X
- task width constants
- gateway size constants
- event diameter constants
- x-axis slot spacing inside the BPMN logical canvas

These values should remain on the base logical canvas unless a loader has a diagram-specific reason to shrink content for density.

## Connector Anchor Rules — Mandatory

All connectors (sequence flow, message flow, association) MUST use the smart anchor helpers
from `primitives.py`. **Never compute raw (x1,y1,x2,y2) start/end points manually.**

### Required helpers
```python
from primitives import connect_seq, connect_msg, edge_endpoints
```

- `connect_seq(slide, node_boxes, src_id, dst_id, colors, label="")` — sequence flow
- `connect_msg(slide, node_boxes, src_id, dst_id, colors, label="")` — message flow
- `edge_endpoints(src_box, dst_box)` — returns (x1,y1,x2,y2) at nearest bounding-box edges

### node_boxes format
Every rendered node must be stored as:
```python
node_boxes[id] = (cx_emu, cy_emu, w_emu, h_emu, shape_object)
```

### Nearest anchor selection (python-pptx index mapping)
python-pptx connection point indices are **counter-clockwise**:
- 0 = top, 1 = left, 2 = bottom, 3 = right

`_best_cxn_pair()` brute-forces all 16 (4×4) anchor combinations and picks the pair
with minimum Euclidean distance — guaranteeing e.g. right-anchor→left-anchor for left-to-right
adjacent shapes, never the incorrect opposite.

### Connector line type
All BPMN flows use `MSO_CONNECTOR_TYPE.CURVE` (curved connector style).
Do not use `STRAIGHT` or `ELBOW` for BPMN flow rendering.

Implementation note:
- `primitives.py` centralizes this with `_FLOW_CONNECTOR_TYPE = MSO_CONNECTOR_TYPE.CURVE`.
- `add_sequence_flow`, `add_message_flow`, `add_association`, and `add_conversation_link`
  must all use this shared connector type.

## Quality Gates

1. Static import check: no forbidden import prefix.
2. Runtime smoke test: every loader can create one slide independently.
3. Automated overlap check: `python3 /tmp/check_peer.py` — peer-node overlap pairs must be 0
   (structural containment such as pool borders ⊇ task nodes is expected and allowed).
4. Business overflow check: `python qa/check_business_overflow.py <pptx>` — raw overflow and business overflow must both be 0 for release candidates.
5. Visual check: no overlap, no orphan arrows, no unlabeled decision branch.

