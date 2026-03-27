# BP-04: Collapsed Sub-Process + Call Activity — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.2.4 Sub-Process, §10.2.5 Call Activity, Figures 10.25, 10.28, 10.39–10.42; BPMN 2.0 by Example dtc/10-06-02 §10.2_

---

## Purpose

Show a **high-level orchestration where reusable process blocks are represented as collapsed boxes**, either as collapsed Sub-Processes (internal detail hidden) or Call Activities (invoking a globally-defined reusable process). This is the "L1 view" of a process hierarchy.

## When to Use

- Executive-level process overview where detail is hidden on purpose
- Showing which sub-processes are reusable vs. one-off
- Process architecture — mapping the hierarchy of process levels (L0 → L1 → L2)
- Documenting a service orchestration that calls shared sub-services

## Official Case Anchor

**Collapsed Sub-Process Example** (OMG Examples §10.2): Shows a parent process with collapsed sub-processes displayed as rounded rectangles with a [+] marker at the bottom center. Internal detail is intentionally hidden.

**Call Activity** (OMG formal spec Figures 10.39–10.42): A special activity that invokes a globally-defined Process or Global Task. Rendered with a thick border to distinguish from local sub-processes. When collapsed, it is a single box referencing external behavior.

## Conformance Level

Descriptive — collapsed sub-processes visible as opaque boxes; no internal detail shown.

## Structure

```
[●Start] → [Sub-Process A [+]] → [Call Activity B ║] → ◇XOR → [Sub-Process C [+]] → [◉End]
                                                       ↓
                                                  [Task D] → [◉End₂]
```

### Variant A: Collapsed Sub-Process Chain
- Linear flow of collapsed sub-processes
- Each box hides 3–10 internal activities
- Best for: L1 or L0 process map

### Variant B: Mixed Collapsed + Call Activity
- Some activities are local sub-processes ([+] marker)
- Some are Call Activities (thick border, referencing shared process)
- Best for: showing reuse and process modularity

### Variant C: Hierarchical Decomposition View
- One parent slide with collapsed boxes; annotation or legend references child slides
- "Drill-down" navigation structure
- Best for: multi-level process documentation sets

## Layout Rules

Node positions are computed automatically by `auto_layout()` from `layout_engine.py` (Sugiyama method). **Do not hardcode x/y positions in config or loader.**

### Render Region (10" × 5.63" slide)

| Boundary | Value |
|----------|-------|
| left | 0.6" |
| top | 1.5" |
| width | 8.5" |
| height | 3.5" |

### Shape-Level Rules (applied after layout)

| Element | Rule |
|---------|------|
| [+] marker | Drawn at bottom center of collapsed sub-process box after position is set |
| Thick border (Call Activity) | Applied as 2.5pt border to the Call Activity node after layout |
| Legend | Bottom-right corner; fixed position, not part of graph layout |

### Sizing (canonical defaults — may be capped by layout engine)

| Element | Dimension |
|---------|-----------|
| Collapsed sub-process box | 1.4" × 0.6" |
| Call Activity box | 1.4" × 0.6" (thick border 2.5pt) |
| [+] marker | 0.12" square, centered at bottom |
| Regular task box | 1.2" × 0.5" |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Collapsed sub-process fill | `light` |
| Collapsed sub-process border | `dark` 1pt |
| [+] marker | `dark` |
| Call Activity fill | `white` |
| Call Activity border | `primary` 2.5pt (thick to signal "reusable") |
| Regular task fill | `white` |
| Regular task border | `dark` 1pt |
| Gateway/Event | Same as BP-02 |

## Typography

| Text | Location | Size |
|------|----------|------|
| Sub-process label | Inside box, centered | 8pt Regular |
| Call Activity label | Inside box, centered | 8pt SemiBold |
| [+] marker | Bottom center | 8pt |
| Process reference note | Below Call Activity | 7pt Italic |

## Anti-Patterns

1. **Collapsed sub-process with visible internal flow**: If [+] is present, do NOT show internal nodes — that is "expanded" mode.
2. **Call Activity without reference**: A Call Activity must clearly state which process it calls (via label or annotation).
3. **No visual distinction**: Collapsed sub-processes and Call Activities must be visually different (thick border vs. normal border + [+] marker).
4. **Too many collapsed boxes with no context**: More than 8 collapsed boxes in a row without description makes the slide meaningless — add brief annotations.

## Official Best Practice Notes

From OMG formal spec §10.2.4:
> "If the Sub-Process is in a collapsed state, then the details of the Sub-Process are not visible... A [+] marker is displayed at the bottom center of the shape."

From OMG formal spec §10.2.5 (Call Activity):
> "A Call Activity identifies a point in the Process where a global Process or a Global Task is used. The Call Activity acts as a 'wrapper' for the invocation... It SHALL be marked with a thick border."

## Data Contract

```yaml
title: "Loan Processing – L1 Overview"
subtitle: "Collapsed sub-processes with reusable credit check call activity"
content:
  nodes:
    - id: "start"
      type: "start_event"
      x_in: 0.3
    - id: "intake"
      type: "collapsed_subprocess"
      x_in: 1.5
      label: "Application Intake"
    - id: "credit_check"
      type: "call_activity"
      x_in: 3.5
      label: "Credit Check"
      reference: "Global Credit Check Process"
    - id: "risk_gw"
      type: "exclusive_gateway"
      x_in: 5.3
      label: "Risk Level?"
    - id: "approval"
      type: "collapsed_subprocess"
      x_in: 6.8
      label: "Approval Workflow"
      y_branch: 0
    - id: "reject"
      type: "task"
      x_in: 6.8
      label: "Send Rejection"
      y_branch: 1
    - id: "end"
      type: "end_event"
      x_in: 8.5
  flows:
    - from: "start"
      to: "intake"
    - from: "intake"
      to: "credit_check"
    - from: "credit_check"
      to: "risk_gw"
    - from: "risk_gw"
      to: "approval"
      label: "Low/Medium"
    - from: "risk_gw"
      to: "reject"
      label: "High"
    - from: "approval"
      to: "end"
    - from: "reject"
      to: "end"
  legend:
    - symbol: "[+]"
      meaning: "Collapsed Sub-Process (detail hidden)"
    - symbol: "thick border"
      meaning: "Call Activity (reusable shared process)"
```

## QA Checklist

- [ ] Collapsed sub-processes show [+] marker and NO internal flow
- [ ] Call Activities have thick border and reference label
- [ ] Visual distinction between collapsed sub-process and Call Activity is clear
- [ ] Optional legend explains the marker meanings
- [ ] ≤ 8 collapsed boxes per slide
- [ ] Colors from ctx.colors
