# BP-05: Lane and Nested Lane Flow — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.8 Lanes, Figures 10.123–10.126; BPMN 2.0 by Example dtc/10-06-02 §10.3 "Multiple Lanes and Nested Lanes Example"_

---

## Purpose

Show **process flow with organizational responsibility assignment** using Lanes within a single Pool. Each Lane represents a role, department, or system. Nested Lanes allow hierarchical grouping (e.g., Department → Teams).

## When to Use

- Documenting who does what in a process (role-based swimlanes)
- Showing handoffs between teams/departments
- Mapping human vs. system responsibility in a hybrid process
- Organizational process mapping with nested team structures

## Official Case Anchor

**Multiple Lanes and Nested Lanes Example** (OMG Examples §10.3): A Pool with 3 Lanes representing different roles. One Lane is further subdivided into 2 nested Lanes. Process flow crosses Lane boundaries via sequence flows, with activities placed in the Lane of the responsible role.

**Lanes in Vertical/Horizontal Pool** (OMG formal spec Figures 10.123–10.124): Demonstrates both vertical and horizontal Lane orientations. Horizontal Lanes (top-to-bottom stacking) with left-to-right flow is the standard presentation layout.

## Conformance Level

Descriptive to Analytic — Lanes + tasks + gateways, no message flows required.

## Structure

```
┌─ Pool: Order Processing Department ─────────────────────────────────────┐
│ ┌─ Lane: Sales Rep ─────────────────────────────────────────────────────┤
│ │  [●Start] → [Receive Request] → [Validate Info] ─────────────────→   │
│ ├─ Lane: Finance ───────────────────────────────────────────────────────┤
│ │                                     ↓                                │
│ │               [Check Credit] → ◇XOR → [Approve] ─────────────────→   │
│ ├─ Lane: Warehouse ─────────────────────────────────────────────────────┤
│ │                                              ↓                       │
│ │                                    [Pick & Pack] → [Ship] → [◉End]   │
│ └───────────────────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────────────────┘
```

### Variant A: Simple Lanes (2–4 lanes)
- Horizontal lanes, left-to-right flow
- Activities placed in owning Lane
- Best for: standard RACI-like process maps

### Variant B: Nested Lanes
- Parent Lane contains child Lanes
- Ref: OMG Examples §10.3 — Department → Sub-Team structure
- Best for: large organizations with team hierarchy

### Variant C: Vertical Lanes
- Lanes stacked left-to-right, flow goes top-to-bottom
- Ref: OMG formal spec Figure 10.123
- Best for: timeline-oriented process or when horizontal space is limited

## Layout Rules

Node positions are computed automatically by `auto_layout(nodes, edges, region, lanes=...)` from `layout_engine.py`. Lane IDs constrain each node's y-center to its assigned horizontal band. **Do not hardcode x/y positions in config or loader.**

### Lane Flattening

Nested lanes are **flattened** before calling `auto_layout()`. Example: `dept.nested_lanes=[emp, mgr]` → flat lane IDs `['emp', 'mgr', 'finance', 'system']`. Each flat lane gets an equal horizontal band in the content area.

### Render Region (10" × 5.63" slide)

| Boundary | Value |
|----------|-------|
| Pool header width | 0.35" |
| Lane header width | 0.7–0.9" |
| Content left | ~1.1" (after pool + lane headers) |
| top | 1.5" |
| height | 3.5" (pool body) |

### Sizing (canonical defaults — may be capped by layout engine)

| Element | Dimension |
|---------|-----------|
| Lane height (3 lanes) | 1.3–1.5" each |
| Lane height (4 lanes) | 1.0–1.2" each |
| Lane header width | 0.7–0.9" |
| Nested lane header width | 0.5–0.7" (additional indent) |
| Activity box | 1.1" × 0.45" |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Pool header fill | `primary` |
| Lane header fill | `secondary` lighter variant |
| Nested Lane header fill | `light` |
| Lane separator line | `dark` 0.75pt |
| Lane body fill | `white` (alternating: white / very light gray for readability) |
| Activity/Gateway/Event | Same as BP-02 |
| Cross-lane sequence flow | `dark` solid arrow |

## Typography

| Text | Location | Size | Weight |
|------|----------|------|--------|
| Pool name | Pool header, rotated 90° | 11pt | Bold |
| Lane name | Lane header, rotated 90° or horizontal | 9pt | SemiBold |
| Nested Lane name | Nested header | 8pt | Regular |
| Activity label | Inside box | 8pt | Regular |

## Anti-Patterns

1. **Activity spanning multiple Lanes**: Each activity must be placed in exactly ONE Lane — the responsible role. If multiple roles participate, decompose into separate tasks in separate Lanes.
2. **Too many Lanes (> 6)**: More than 6 Lanes on a single slide makes each Lane too thin to draw readable activities. Split into multiple slides.
3. **No cross-lane flows**: If all activities are in one Lane, Lanes add no value — use BP-02 instead.
4. **Lane = system component**: Lanes represent organizational roles/departments, not technical components. For system-to-system flows, use BP-01 Collaboration with Pools.
5. **Nested too deep**: More than 2 levels of Lane nesting becomes unreadable.

## Official Best Practice Notes

From OMG formal spec §10.8:
> "A Lane is a sub-partition within a Process... used to organize and categorize Activities within a Pool. The meaning of the Lanes is up to the modeler."

> "A Lane can be nested within another Lane, providing hierarchical organization."

From OMG Examples §10.3:
> The nested lanes example shows that child lanes inherit the parent lane's Pool scope, and sequence flows can freely cross between sibling and cousin lanes.

## Data Contract

```yaml
title: "Purchase Requisition Approval"
subtitle: "Cross-department handoff flow with nested team structure"
content:
  pool:
    id: "procurement"
    name: "Procurement Department"
  lanes:
    - id: "requester"
      name: "Requester"
    - id: "finance"
      name: "Finance"
      nested_lanes:
        - id: "ap_team"
          name: "AP Team"
        - id: "controller"
          name: "Controller"
    - id: "purchasing"
      name: "Purchasing"
  nodes:
    - id: "start"
      type: "start_event"
      lane: "requester"
      x_in: 0.2
    - id: "submit"
      type: "user_task"
      lane: "requester"
      x_in: 1.5
      label: "Submit Request"
    - id: "review"
      type: "user_task"
      lane: "ap_team"
      x_in: 3.0
      label: "Review Budget"
    - id: "approve_gw"
      type: "exclusive_gateway"
      lane: "controller"
      x_in: 4.5
      label: "Budget OK?"
    - id: "create_po"
      type: "task"
      lane: "purchasing"
      x_in: 6.0
      label: "Create PO"
    - id: "reject"
      type: "task"
      lane: "requester"
      x_in: 6.0
      label: "Notify Rejection"
      y_branch: 1
    - id: "end"
      type: "end_event"
      lane: "purchasing"
      x_in: 7.8
  flows:
    - from: "start"
      to: "submit"
    - from: "submit"
      to: "review"
    - from: "review"
      to: "approve_gw"
    - from: "approve_gw"
      to: "create_po"
      label: "Yes"
    - from: "approve_gw"
      to: "reject"
      label: "No"
    - from: "create_po"
      to: "end"
```

## QA Checklist

- [ ] Every activity placed in exactly one Lane
- [ ] Lane headers clearly label roles/departments
- [ ] Cross-lane sequence flows are clean (minimal crossings)
- [ ] ≤ 6 Lanes per slide, ≤ 2 nesting levels
- [ ] Pool header present if Lanes are used
- [ ] Colors from ctx.colors
