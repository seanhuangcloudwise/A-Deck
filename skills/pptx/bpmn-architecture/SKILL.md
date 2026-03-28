# BPMN 2.0 Architecture Skill

BPMN 2.0 process planning and communication skill for presentation diagrams.
This domain is parallel to GTM/Roadmap and is intentionally isolated.

## Scope

Use this skill for:
- process planning and optimization storytelling
- cross-team collaboration and handoff flow
- approval/escalation/timeout paths
- executable-like process communication for product, ops, and IT

Do not use this skill for:
- product GTM narrative diagrams
- roadmap planning heatmaps or timeline-only views
- TOGAF application/data/technology topology diagrams

## Official Source Policy

Spec details and case anchors must come from official BPMN source pages:
- OMG BPMN main page: https://www.omg.org/spec/BPMN
- OMG BPMN 2.0.2 About page: https://www.omg.org/spec/BPMN/2.0.2/About-BPMN
- OMG BPMN 2.0 examples (informative): https://www.omg.org/cgi-bin/doc.cgi?dtc/10-06-02.pdf
- OMG BPMN 2.0.2 formal specification: https://www.omg.org/cgi-bin/doc.cgi?formal/13-12-09.pdf

## Conformance Baseline

Each diagram spec should state intended modeling depth aligned with BPMN conformance terms:
- Descriptive
- Analytic
- Common Executable

Reference anchor terms are present in the BPMN formal document (Process Modeling Conformance and sub-classes).

## Diagram Catalog (Must Support)

1. BP-01 Collaboration Overview
2. BP-02 Orchestration Flow (Single Pool)
3. BP-03 Expanded Sub-Process
4. BP-04 Collapsed Sub-Process + Call Activity
5. BP-05 Lane and Nested Lane Flow
6. BP-06 Choreography Interaction
7. BP-07 Conversation Map
8. BP-08 Event and Gateway Control Pattern
9. BP-09 Compensation and Transaction Pattern
10. BP-10 Human-driven vs System-driven Split

See diagrams in the diagrams folder and selection guide in diagrams/_catalog.md.

## Hard Architecture Constraints

1. One diagram = one loader file.
2. No code-level cross references to other drawing skills.
3. No imports from skills/pptx/shared or togaf/roadmap/gtm loaders.
4. BPMN local primitives and helpers must live only in this domain.
5. Data-driven render contract is mandatory: load_slide(ctx, data).

## Rendering Implementation

### Auto Layout (Sugiyama Method)

`layout_engine.py` provides `auto_layout(nodes, edges, region, lanes=None)` → `{id: (left, top, w, h)}` in EMU.

- **Cycle removal** via DFS back-edge detection
- **Layer assignment** via longest-path / Kahn topological sort
- **Crossing minimization** via barycenter heuristic + transpose (24 sweeps)
- **Coordinate assignment**: evenly distributed per layer; per-node width capped to `layer_spacing - 0.12"` (min 0.25") to guarantee no overlap

**Mandatory usage**: all loaders with graph-like node flows must call `auto_layout()` and then draw nodes at the returned positions. Hardcoding x/y is forbidden.

**Exceptions** (specialized layout, no `auto_layout()`): BP-01 pool-slots, BP-06 choreography bands, BP-07 conversation ring.

After computing positions, always use the returned `w, h` for drawing — the engine may shrink them to fit the region:
```python
positions = auto_layout(nodes, edges, region)
for nid, (left, top, w, h) in positions.items():
	s = add_task(slide, left, top, w, h, C, ...)
	node_boxes[nid] = (left + w//2, top + h//2, w, h, s)
```

### Connector Routing

Always use `connect_seq()` and `connect_msg()` from `primitives.py`. Never draw connectors manually.

```python
connect_seq(slide, node_boxes, src_id, dst_id, colors, label="")
connect_msg(slide, node_boxes, src_id, dst_id, colors, label="")
```

**anchor selection**: brute-force 4×4 pair search picks minimum Euclidean distance anchor pair.

**CCW index mapping** (python-pptx internal):
- 0 = top, 1 = **left**, 2 = bottom, 3 = **right** (counter-clockwise)

**Connector type**: `MSO_CONNECTOR_TYPE.CURVE` always. Never STRAIGHT.

## QA Checklist

- title/subtitle placeholder-first
- no decorative-only connectors
- each flow has explicit semantics (sequence/message/association)
- gateway direction is explainable in speaker notes
- event usage is intentional (start/intermediate/end/boundary)
- pools and lanes are used according to BPMN semantics

## Selection Logic

- Cross participant interaction first: BP-01 or BP-06
- Single process control logic first: BP-02 or BP-08
- Reusable process block first: BP-03 or BP-04
- Message context first: BP-07
- exception/rollback first: BP-09
- org+automation split first: BP-10
