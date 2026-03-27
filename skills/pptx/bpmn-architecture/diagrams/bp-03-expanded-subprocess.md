# BP-03: Expanded Sub-Process — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.2.4 Sub-Process, Figures 10.25–10.32; BPMN 2.0 by Example dtc/10-06-02 §10.1 "Expanded Sub Process Example"_

---

## Purpose

Show a **process fragment wrapped inside a visible sub-process boundary**, revealing its internal detail in-place. The expanded sub-process acts as a "zoom-in" box within a parent process, providing hierarchical decomposition.

## When to Use

- Breaking a complex process into manageable chunks without leaving the slide
- Showing exception handling scope (boundary events attach to the sub-process)
- Grouping related activities that share a common transaction or compensation scope
- Documenting reusable process fragments that may be called from multiple parents

## Official Case Anchor

**Expanded Sub-Process Example** (OMG Examples §10.1): Demonstrates an outer process containing an expanded sub-process rectangle that itself holds a Start → Task → Gateway → End mini-flow. Boundary events (e.g., Timer, Error) are placed on the sub-process border, with exception paths branching from those events.

**Event Sub-Process** (OMG formal spec Figures 10.30–10.32): Special sub-process variant started by an event (e.g., non-interrupting message event sub-process inside a parent). Shown with dashed border.

## Conformance Level

Analytic — expanded sub-process, boundary events, event sub-process.

## Structure

```
┌─ Parent Process ──────────────────────────────────────────────────────────┐
│ [●Start] → [Task A] → ┌─ Sub-Process ─────────────────┐ → [Task C] → [◉End] │
│                        │ [●S] → [Task B1] → [Task B2] → [◉E] │              │
│                        │                                │              │
│                        └───⏰Timer──♦Error──────────────┘              │
│                             ↓           ↓                              │
│                         [Timeout]   [Handle Error]                     │
└───────────────────────────────────────────────────────────────────────┘
```

### Variant A: Simple Expanded (default)
- One expanded sub-process in a linear parent flow
- Internal flow visible (3–5 tasks)
- Best for: process decomposition storytelling

### Variant B: With Boundary Events
- Timer/Error/Signal boundary events on sub-process border
- Exception flow branches from boundary event
- Best for: showing SLA timeouts, error handling, escalation

### Variant C: Event Sub-Process (dashed border)
- Non-interrupting or interrupting event sub-process
- Triggered by message/timer/signal within parent scope
- Best for: showing inline exception handling (E-Mail Voting pattern)
- Ref: OMG Examples §12 E-Mail Voting

## Layout Rules

**Dual-region `auto_layout()`** — the subprocess interior and the parent process each call `auto_layout()` independently. **Do not hardcode x/y positions in config or loader.**

- **Subprocess internal nodes**: `auto_layout()` within the subprocess rectangle interior
- **Parent process nodes** (Start, Sub-Process box, downstream tasks, End): `auto_layout()` across the full slide content area, treating the subprocess box as a single opaque node

### Structural Zones (applied after layout)

| Zone | Constraint |
|------|-----------|
| Subprocess rectangle | Center region, 40–60% of parent width; position set by parent `auto_layout()` |
| Boundary events | On the bottom or right edge of subprocess rectangle |
| Exception flow | Downward from boundary event |

### Sizing

| Element | Dimension |
|---------|-----------|
| Sub-process rectangle | 3.5–5.0" × 1.2–1.8" |
| Sub-process corner radius | ≤ 6pt |
| Internal activity box | 1.0" × 0.45" |
| Boundary event circle | 0.22" diameter, on border |
| Parent activity box | 1.2" × 0.5" |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Sub-process border | `primary` 1.5pt solid |
| Sub-process fill | `white` with slight alpha or `light` |
| Sub-process header strip (optional) | `primary` 10% opacity |
| Boundary timer event | `secondary` thin circle + clock icon |
| Boundary error event | semantic red (hardcoded `#D94040`) |
| Exception flow arrow | same color as boundary event |
| Event sub-process border | `primary` dashed 1.5pt |
| All other elements | Same as BP-02 base palette |

## Typography

| Text | Location | Size | Weight |
|------|----------|------|--------|
| Sub-process label | Top-left inside box or header strip | 9pt | SemiBold |
| Internal task labels | Inside boxes | 7pt | Regular |
| Boundary event label | Below or right of event circle | 7pt | Regular |
| Exception task label | Inside exception path box | 8pt | Regular |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rounded rectangle with [+] marker | Sub-Process (collapsed) |
| Rounded rectangle (expanded, no [+]) | Sub-Process (expanded) — shows internal flow |
| Dashed rounded rectangle | Event Sub-Process |
| Circle on rectangle border (thin) | Non-interrupting boundary event |
| Circle on rectangle border (thick) | Interrupting boundary event |
| ⏰ inside boundary circle | Timer boundary event |
| ⚡ inside boundary circle | Error boundary event |
| ✉ inside boundary circle | Message boundary event |

## Anti-Patterns

1. **Nested expansion too deep**: More than 2 levels of visible sub-process nesting makes the slide unreadable. Collapse inner sub-processes.
2. **Boundary event inside the box**: Boundary events must be ON the border (half-in, half-out), not floating inside the sub-process.
3. **No internal Start/End in expanded sub-process**: BPMN requires expanded sub-processes to have their own Start and End events.
4. **Exception path re-entering sub-process**: The exception flow from a boundary event exits the sub-process scope and must NOT re-enter it.

## Official Best Practice Notes

From OMG formal spec §10.2.4:
> "A Sub-Process is an Activity whose internal work is modeled... When expanded, the internal details (a Process) are visible."

From OMG formal spec §10.5 (Boundary Events):
> "An Intermediate Event can be attached to the boundary of an Activity... It will be triggered while the Activity is being performed."

From OMG Examples §12 (E-Mail Voting):
> The E-Mail Voting example shows a non-interrupting Event Sub-Process receiving votes while the main process continues running — the event sub-process is drawn with a dashed border and a non-interrupting message start event.

## Data Contract

```yaml
title: "Order Fulfillment with Payment Sub-Process"
subtitle: "Expanded sub-process showing payment handling and timeout"
content:
  nodes:
    - id: "start"
      type: "start_event"
      x_in: 0.3
    - id: "receive_order"
      type: "task"
      x_in: 1.2
      label: "Receive Order"
    - id: "payment_sub"
      type: "expanded_subprocess"
      x_in: 3.0
      width_in: 4.0
      height_in: 1.5
      label: "Payment Processing"
      internal_nodes:
        - id: "ps_start"
          type: "start_event"
          x_in: 0.2
        - id: "charge"
          type: "service_task"
          x_in: 1.2
          label: "Charge Card"
        - id: "confirm"
          type: "task"
          x_in: 2.5
          label: "Send Confirmation"
        - id: "ps_end"
          type: "end_event"
          x_in: 3.5
      internal_flows:
        - from: "ps_start"
          to: "charge"
        - from: "charge"
          to: "confirm"
        - from: "confirm"
          to: "ps_end"
    - id: "ship"
      type: "task"
      x_in: 7.5
      label: "Ship Order"
    - id: "end"
      type: "end_event"
      x_in: 8.8
  boundary_events:
    - id: "timeout"
      type: "timer_boundary"
      attached_to: "payment_sub"
      interrupting: true
      position: "bottom"
      label: "30min timeout"
    - id: "payment_error"
      type: "error_boundary"
      attached_to: "payment_sub"
      interrupting: true
      position: "bottom-right"
      label: "Payment Failed"
  flows:
    - from: "start"
      to: "receive_order"
    - from: "receive_order"
      to: "payment_sub"
    - from: "payment_sub"
      to: "ship"
    - from: "ship"
      to: "end"
  exception_flows:
    - from: "timeout"
      to: "notify_timeout"
    - from: "payment_error"
      to: "handle_error"
```

## QA Checklist

- [ ] Expanded sub-process has internal Start and End events
- [ ] Boundary events visually sit ON the sub-process border
- [ ] Exception flows exit sub-process scope (no re-entry)
- [ ] No more than 2 levels of expanded nesting visible
- [ ] Dashed border only for Event Sub-Processes
- [ ] Timer/Error/Message icons correct inside boundary circles
- [ ] Colors from ctx.colors
