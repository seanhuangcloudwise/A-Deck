# BPMN Architecture Skills Index

This folder contains the BPMN 2.0 process modeling skill with 10 diagram types, based on the OMG BPMN 2.0.2 formal specification.

## Diagrams

| ID | Name | OMG Anchor |
|---|---|---|
| BP-01 | Collaboration Overview | §9 Collaboration, Pizza example |
| BP-02 | Orchestration Flow | §10 Process, Shipment example |
| BP-03 | Expanded Sub-Process | §10.2 Sub-Process, boundary events |
| BP-04 | Collapsed Sub-Process / Call Activity | §10.3 Call Activity |
| BP-05 | Lane / Nested Lane Flow | §10.8 Lanes |
| BP-06 | Choreography Interaction | §11 Choreography |
| BP-07 | Conversation Map | §9.5 Conversations |
| BP-08 | Event & Gateway Control Pattern | §10.5–10.6 Events & Gateways |
| BP-09 | Compensation / Transaction Pattern | §10.7 Compensation, §10.2.4 Transaction |
| BP-10 | Human vs System Split | §10.2.2 Task types, by-example §6.3 |

**Full catalog:** [diagrams/_catalog.md](diagrams/_catalog.md)

## Architecture

- **Loaders:** `loaders/bp_01_*.py` through `bp_10_*.py` — one file per diagram type
- **Primitives:** `loaders/primitives.py` — BPMN shape/connector rendering; smart anchor selection
- **Style Tokens:** `loaders/style_tokens.py` — semantic colors, sizing, fonts
- **Layout Engine:** `loaders/layout_engine.py` — Sugiyama layered graph layout (`auto_layout()` API)
- **Rules:** [ARCHITECTURE_RULES.md](ARCHITECTURE_RULES.md) — isolation boundaries, layout/connector mandates

## Layout Engine

`layout_engine.py` implements the classic Sugiyama method (4-step):
1. **Cycle removal** — DFS back-edge detection
2. **Layer assignment** — longest-path from sources (Kahn topological sort)
3. **Crossing minimization** — barycenter heuristic + transpose (24 sweeps)
4. **Coordinate assignment** — lane-band constrained; per-node width capped against `layer_spacing` to prevent overlap

All loaders with graph-like flows call `auto_layout()`. Hard exceptions with specialized layout (no `auto_layout()`):
- **BP-01** — pool-slot layout (two expanded Pools, fixed vertical positioning)
- **BP-06** — choreography band layout (participant bands top/bottom of each task)
- **BP-07** — conversation ring/network layout (hexagonal hexagons + participant nodes)

## Connector Strategy

All flows use `connect_seq()` / `connect_msg()` from `primitives.py`:
- Brute-force 4×4 anchor pair search — selects the pair with minimum Euclidean distance
- **python-pptx CCW index mapping**: 0=top, 1=**left**, 2=bottom, 3=**right** (counter-clockwise, not clockwise)
- All connectors use `MSO_CONNECTOR_TYPE.ELBOW` — never STRAIGHT
- `node_boxes` format per call: `{id: (cx_emu, cy_emu, w_emu, h_emu, shape_obj)}`

## Isolation Constraint

This skill imports **nothing** from `shared/`, `gtm-architecture/`, `roadmap-architecture/`, or `togaf-architecture/`. All drawing primitives are self-contained.

## Demo Project

`projects/bpmn-purple-demo/` — orchestrator + YAML config for all 10 diagrams, master: `light-cloudwise-purple`.

## Routing Hint

When the request involves: business process modeling, BPMN notation, workflow visualization, approval/escalation flow, process collaboration, choreography, conversation map, lane-based task assignment, compensation/transaction, or human-vs-system automation → use this skill.
