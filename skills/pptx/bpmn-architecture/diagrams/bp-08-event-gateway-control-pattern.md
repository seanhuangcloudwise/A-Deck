# BP-08: Event and Gateway Control Pattern — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.5 Events, §10.6 Gateways, §13.4–13.5 Execution Semantics; BPMN 2.0 by Example dtc/10-06-02 §6 "Incident Management" (gateway patterns), §9 "Travel Booking" (event-based gateway)_

---

## Purpose

Serve as a **pattern reference slide** showing combinations of BPMN 2.0 Events and Gateways in realistic control flow patterns — a "cheat sheet" or "pattern card" for audiences who need to understand BPMN decision and event semantics.

## When to Use

- Teaching BPMN to business analysts or developers
- Documenting the specific gateway and event patterns used in a project
- Showing the difference between XOR, AND, Inclusive, Event-Based, and Complex gateways
- Demonstrating boundary events, intermediate catch/throw events, and link events

## Official Case Anchor

**Incident Management — gateway patterns** (OMG Examples §6.1–6.3): The incident management example uses multiple gateway types: Exclusive (XOR) for "Is first-line resolution possible?", Parallel (AND) for simultaneous notification, and the human/system split uses an Inclusive gateway.

**Travel Booking — Event-Based Gateway** (OMG Examples §9): An Event-Based Gateway where the process waits for either a message ("Booking Confirmation") or a timer ("7-day Timeout"), whichever comes first. This is the canonical pattern for event-based decisions.

**Gateway Catalog** (OMG formal spec §10.6, Figures 10.102–10.120): Formal specification of all 5 gateway types with visual markers and execution semantics.

**Event Catalog** (OMG formal spec §10.5, Figures 10.69–10.100): All event types with their markers: None, Message, Timer, Escalation, Conditional, Link, Error, Cancel, Compensation, Signal, Multiple, Parallel Multiple, Terminate.

## Conformance Level

Common Executable — all gateway and event types.

## Structure

The slide is organized as a **pattern card grid** rather than a single process flow:

```
┌────────────────────────────────────────────┐
│ Pattern 1: XOR Split-Merge                 │
│  → ◇X → [A] →                             │
│       → [B] → ◇X →                        │
├────────────────────────────────────────────┤
│ Pattern 2: AND Fork-Join                   │
│  → ◇+ → [A] →                             │
│       → [B] → ◇+ →                        │
├────────────────────────────────────────────┤
│ Pattern 3: Event-Based Gateway             │
│  → ◇⬠ → ✉[Message] →                     │
│        → ⏰[Timer]   →                     │
├────────────────────────────────────────────┤
│ Pattern 4: Boundary Events                 │
│  [Task ⏰] → (exception path)             │
│  [Task ⚡] → (error path)                 │
└────────────────────────────────────────────┘
```

### Variant A: Gateway Pattern Card (4–6 patterns)
- Grid layout with small self-contained patterns
- Each pattern: 2–4 shapes showing one gateway or event type
- Best for: training/reference material

### Variant B: Combined Control Flow
- Single realistic process using multiple gateway/event types
- Based on Incident Management example
- Best for: showing how patterns compose in real processes

### Variant C: Event Taxonomy Card
- Grid organized by event position (Start/Intermediate/End) × type (Message/Timer/Error/...)
- Visual catalog of BPMN event markers
- Best for: notation reference

## Gateway Types (Must Render)

| Gateway | Marker | Behavior | OMG Ref |
|---------|--------|----------|---------|
| Exclusive (XOR) | X | One path taken based on data condition | §10.6.2, Fig 10.105 |
| Parallel (AND) | + | All paths taken simultaneously; join waits for all | §10.6.3, Fig 10.110 |
| Inclusive (OR) | O | One or more paths based on conditions; join waits for active paths | §10.6.4, Fig 10.108 |
| Event-Based | ⬠ | Waits for first event to occur; race condition | §10.6.6, Fig 10.115 |
| Complex | * | Custom merge/split logic | §10.6.5, Fig 10.113 |

## Event Types (Must Render)

| Event | Position | Marker | OMG Ref |
|-------|----------|--------|---------|
| None | Start/End | Empty | Fig 10.91 |
| Message | Start/Intermediate/End/Boundary | ✉ | Fig 10.88 |
| Timer | Start/Intermediate/Boundary | ⏰ | Fig 10.96 |
| Error | End/Boundary (interrupting only) | ⚡ | Fig 10.79 |
| Escalation | Start/Intermediate/End/Boundary | ↑ | Fig 10.81 |
| Signal | Start/Intermediate/End/Boundary | △ | Fig 10.94 |
| Compensation | Intermediate/End/Boundary | ⟲ | Fig 10.75 |
| Cancel | End/Boundary | × | Fig 10.74 |
| Conditional | Start/Intermediate/Boundary | ≡ | Fig 10.77 |
| Link | Intermediate (throw/catch pair) | → | Fig 10.83 |
| Terminate | End only | ⊗ | Fig 10.95 |
| Multiple | Start/Intermediate/End/Boundary | ⬠ | Fig 10.90 |

## Layout Rules

Each **pattern card** uses `auto_layout()` for the nodes within its card region. The card grid (2×2 or 2×3) is a fixed structural grid; `auto_layout()` operates inside each card's content area independently. **Do not hardcode node x/y within cards.**

### Card Grid

| Property | Value |
|----------|-------|
| Grid layout | 2×2 (4 patterns) or 2×3 (6 patterns) |
| Card border | Thin `light` line between cards |
| Card title | Fixed: top-left of each card, reserved 0.25" title band |
| Pattern flow region | Remainder of card area below title band |

### Sizing (canonical defaults — may be capped per-card by layout engine)

| Element | Dimension |
|---------|-----------|
| Card area | 3.5–4.5" × 1.0–1.5" |
| Activity box (mini) | 0.8" × 0.35" |
| Gateway diamond | 0.25" × 0.25" |
| Event circle | 0.18" diameter |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Pattern card background | `white` |
| Card border | `light` 0.5pt |
| Card title | `primary` |
| Gateway markers | `dark` |
| Event markers (normal) | `primary` for start, `dark` for end |
| Event markers (error) | semantic red `#D94040` |
| Event markers (timer) | `secondary` |
| Event markers (compensation) | semantic amber `#E6A817` |
| Flow arrows | `dark` |

## Anti-Patterns

1. **Mixing pattern card with full process**: Either show a pattern reference OR a full process — not both on the same slide.
2. **Unlabeled gateway type**: Every gateway MUST have its type marker visible (X/+/O/⬠/*). An empty diamond is ambiguous.
3. **Interrupting vs non-interrupting not distinguished**: Interrupting boundary events have solid double circle; non-interrupting have dashed double circle — this distinction MUST be visible.
4. **Link events without pairs**: A throw Link Event must have a corresponding catch Link Event. Orphan link events are meaningless.

## Official Best Practice Notes

From OMG formal spec §10.6:
> "Each type of Gateway will have an internal indicator or marker to show the type of behavior control."

From OMG formal spec §10.6.6 (Event-Based Gateway):
> "The Event-Based Gateway represents a branching point in the Process where the alternative paths that follow the Gateway are based on Events that occur at that point."

From OMG formal spec §10.5.3 (Boundary Events):
> "If the Event is Interrupting... the Activity will be cancelled. If the Event is Non-Interrupting... the Activity continues."

## Data Contract

```yaml
title: "BPMN Gateway & Event Pattern Reference"
subtitle: "Standard control flow patterns from BPMN 2.0 specification"
content:
  variant: "pattern_card"  # pattern_card | combined_flow | event_taxonomy
  patterns:
    - id: "xor_split"
      title: "Exclusive (XOR) Split-Merge"
      nodes:
        - {id: "s", type: "start_event", x: 0.1}
        - {id: "t1", type: "task", x: 0.5, label: "Evaluate"}
        - {id: "gw1", type: "exclusive_gateway", x: 1.5}
        - {id: "t2a", type: "task", x: 2.3, label: "Path A", y_branch: 0}
        - {id: "t2b", type: "task", x: 2.3, label: "Path B", y_branch: 1}
        - {id: "gw2", type: "exclusive_gateway", x: 3.5}
        - {id: "e", type: "end_event", x: 4.2}
      flows:
        - {from: "s", to: "t1"}
        - {from: "t1", to: "gw1"}
        - {from: "gw1", to: "t2a", label: "Condition A"}
        - {from: "gw1", to: "t2b", label: "Else"}
        - {from: "t2a", to: "gw2"}
        - {from: "t2b", to: "gw2"}
        - {from: "gw2", to: "e"}
    - id: "and_fork"
      title: "Parallel (AND) Fork-Join"
      # ... similar structure
    - id: "event_based"
      title: "Event-Based Gateway"
      # ...
    - id: "boundary_events"
      title: "Boundary Event Patterns"
      # ...
```

## QA Checklist

- [ ] All 5 gateway types have correct internal markers
- [ ] Interrupting vs non-interrupting boundary events visually distinct
- [ ] Event markers match BPMN 2.0 standard notation
- [ ] Pattern cards are self-contained (readable independently)
- [ ] No ambiguous empty diamonds (every gateway typed)
- [ ] Colors from ctx.colors (except documented semantic colors for error/timer/compensation)
