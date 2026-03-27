# BP-02: Orchestration Flow (Single Pool) — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10 Process, §10.2–10.4 Activities; BPMN 2.0 by Example dtc/10-06-02 "Shipment Process of a Hardware Retailer", "Travel Booking Example"_

---

## Purpose

Show the **end-to-end control flow of a single process** within one Pool — the classic orchestration perspective. Tasks, gateways, and events are laid out to reveal the complete decision logic, branching, parallelism, and handoffs within one organizational boundary.

## When to Use

- Documenting a standard operating procedure (SOP)
- Detailing an approval pipeline or onboarding workflow
- Showing the internal logic of a microservice or automation script
- Explaining a process to the team that owns and executes it

## Official Case Anchor

**Shipment Process of a Hardware Retailer** (OMG Examples §4): A single-pool process with parallel gateway (fork) splitting into "Decide Shipment Mode" and "Package Goods", an exclusive gateway choosing between "Normal Shipment" / "Extra Insurance" paths, a parallel join before "Deliver Goods", ending at an End Event. Demonstrates parallel + exclusive gateway combination in one flow.

**Travel Booking** (OMG Examples §9): Shows a sequential booking flow with an event-based gateway waiting for either a booking confirmation or a timeout timer — demonstrating event-based decision within a single-pool orchestration.

## Conformance Level

Analytic — single pool, no message flows, includes gateways, boundary events, data objects.

## Structure

```
[●Start] → [Task 1] → ◇AND-Fork → [Task 2a] → ◇XOR → [Task 3a] → ◇AND-Join → [Task 4] → [◉End]
                                  → [Task 2b] ──────→ [Task 3b] ─→
```

### Variant A: Linear Flow (3–6 tasks)
- Simple left-to-right sequence with occasional XOR branch
- Best for: simple SOPs, quick process overview

### Variant B: Parallel Split-Join (Shipment pattern)
- AND-fork → parallel paths → AND-join
- Best for: processes with concurrent work streams

### Variant C: Event-Based Decision (Travel pattern)
- Event-based gateway → message event / timer event race
- Best for: processes with external trigger dependencies

## Layout Rules

Node positions are computed automatically by `auto_layout()` from `layout_engine.py` (Sugiyama method). **Do not hardcode x/y positions in config or loader.** Sequential flows → left-to-right layers; parallel branches → vertically stacked layers.

### Render Region (10" × 5.63" slide)

| Boundary | Value |
|----------|-------|
| left | 0.6" |
| top | 1.5" |
| width | 8.5" |
| height | 3.5" |

### Sizing (canonical defaults — may be capped by layout engine if nodes are dense)

| Element | Dimension |
|---------|-----------|
| Activity box | 1.3" × 0.55" |
| Event circle | 0.24" diameter |
| Gateway diamond | 0.32" × 0.32" |
| Horizontal task gap | 0.3–0.5" |
| Vertical branch gap | 0.5–0.7" |
| Data object icon | 0.25" × 0.30" |

## Color Semantics

| Element | Color Token | Usage |
|---------|-------------|-------|
| Task fill | `white` | Standard user/service task |
| Task border | `dark` | 1pt solid |
| User task icon | `primary` | Small person icon top-left |
| Service task icon | `secondary` | Gear icon top-left |
| Gateway fill | `white` | Outline only |
| Gateway border | `dark` | 1.25pt |
| Gateway marker (X/+/O) | `dark` | Internal symbol |
| Start event | `primary` | Thin circle stroke |
| End event | `dark` | Thick circle stroke |
| Sequence flow | `dark` | Solid arrow, 1pt |
| Default flow | `dark` | Solid arrow with tick mark |
| Conditional flow | `dark` | Solid arrow with diamond start |
| Data object | `light` fill, `dark` border | Folded-corner document icon |
| Association | `dark` | Dotted line, no arrowhead |

## Typography

| Text | Location | Size | Weight | Color |
|------|----------|------|--------|-------|
| Task label | Inside box, centered | 8pt | Regular | `text` |
| Gateway condition | Near outgoing branch | 7pt | Regular | `dark` |
| Event label | Below event circle | 7pt | Regular | `dark` |
| Data object label | Below icon | 7pt | Regular | `dark` |
| Slide title | Placeholder idx=0 | Per master | Bold | Per master |
| Slide subtitle | Placeholder idx=1 | Per master | Regular | Per master |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rounded rectangle | Task (User/Service/Manual/Script per icon) |
| Rounded rect + [+] marker | Sub-Process (collapsed) |
| Thin circle ● | Start Event |
| Thick circle ◉ | End Event |
| Double circle | Intermediate Event |
| Diamond ◇ with X | Exclusive Gateway |
| Diamond ◇ with + | Parallel Gateway |
| Diamond ◇ with O | Inclusive Gateway |
| Diamond ◇ with pentagon | Event-Based Gateway |
| Solid arrow → | Sequence Flow |
| Dotted line | Association |
| Folded-corner rect | Data Object |

## Annotation & Labeling Rules

- Every task must have a verb-noun label (e.g., "Package Goods", not just "Packaging")
- Every exclusive/inclusive gateway must label each outgoing branch
- Default flow branch should be marked with a tick on the sequence flow
- Data objects must name the artifact (e.g., "Shipment Details", not "Data")

## Density Modes

| Mode | Tasks | Gateways | Parallel Branches | Max per Slide |
|------|-------|----------|-------------------|---------------|
| Light | 3–5 | 1–2 | 0–1 | 1 |
| Standard | 5–8 | 2–4 | 1–2 | 1 |
| Dense | 8–12 | 3–5 | 2–3 | 1 |

**Overflow**: If > 12 tasks, split with Link Intermediate Events (throw on slide N, catch on slide N+1). Note the link event pair in both slides.

## Anti-Patterns (Must Avoid)

1. **Gateway without labeled branches**: An XOR gateway with two outgoing arrows but no condition labels — the reader cannot understand the decision.
2. **Parallel gateway used as XOR**: Using AND-gateway where only one path should execute — this causes the process to always take all paths simultaneously.
3. **Missing join gateway**: A parallel fork without a corresponding join — the process has no synchronization point.
4. **Start event with incoming flow**: Start events MUST NOT have incoming sequence flows per BPMN spec §10.5.
5. **End event with outgoing flow**: End events MUST NOT have outgoing sequence flows.
6. **Spaghetti flow**: More than 2 crossing sequence flow lines on a single slide — reorganize layout to eliminate crossings.

## Official Best Practice Notes

From OMG formal spec §10.6 (Gateways):
> "Gateways are used to control how the Process flows (how Tokens flow) through Sequence Flows as they converge and diverge within a Process."

From OMG Examples §4 (Shipment):
> The Shipment example demonstrates that parallel execution paths (AND-fork) and exclusive decisions (XOR) can be composed in the same process to model both concurrency and choice.

From OMG Examples §9 (Travel Booking):
> The Event-Based Gateway "represents a branching point in the Process where the alternative paths that follow the Gateway are based on Events that occur at that point in the Process, rather than the evaluation of Expressions using Process data."

## Data Contract

```yaml
title: "Hardware Shipment Process"
subtitle: "End-to-end orchestration with parallel packaging and shipping"
content:
  nodes:
    - id: "start"
      type: "start_event"
      x_in: 0.3
      label: ""
    - id: "check_goods"
      type: "user_task"
      x_in: 1.2
      label: "Check Goods"
    - id: "fork1"
      type: "parallel_gateway"
      x_in: 2.8
      label: ""
    - id: "package"
      type: "task"
      x_in: 4.0
      y_branch: 0
      label: "Package Goods"
    - id: "decide_ship"
      type: "exclusive_gateway"
      x_in: 4.0
      y_branch: 1
      label: "Shipment Mode?"
    # ... more nodes
  flows:
    - from: "start"
      to: "check_goods"
      type: "sequence"
    - from: "check_goods"
      to: "fork1"
      type: "sequence"
    - from: "fork1"
      to: "package"
      type: "sequence"
    - from: "fork1"
      to: "decide_ship"
      type: "sequence"
    # ...
  data_objects:
    - id: "shipment_details"
      label: "Shipment Details"
      associated_to: "decide_ship"
  annotations: []
```

## QA Checklist

- [ ] All activities have verb-noun labels
- [ ] All gateway branches labeled (except default flow with tick mark)
- [ ] Parallel forks have matching parallel joins
- [ ] No sequence flow crossing Pool boundaries (this is a single-pool diagram)
- [ ] Start has no incoming, End has no outgoing
- [ ] No crossing sequence flow lines (reorganize if needed)
- [ ] Colors from ctx.colors only
- [ ] Title/subtitle in placeholders
