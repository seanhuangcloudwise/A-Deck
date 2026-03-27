# BP-01: Collaboration Overview — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §9 Collaboration, §9.2–9.4; BPMN 2.0 by Example dtc/10-06-02 "The Pizza Collaboration", "Vertical Collaboration Example"_

---

## Purpose

Show the **message-based interaction between two or more participants** (Pools), each containing their own internal process. The diagram answers: who talks to whom, via which messages, at what point in their respective processes.

## When to Use

- Documenting cross-organization or cross-department handoffs
- Showing buyer ↔ seller, requester ↔ provider, customer ↔ service interaction
- Communicating B2B integration points to business stakeholders
- Aligning IT message exchange design with business process owners

## Official Case Anchor

**The Pizza Collaboration** (OMG Examples §5): Customer Pool places an order, Pizza Vendor Pool receives the order, prepares pizza, delivers; message flows connect "Order Pizza" → "Receive Order" and "Deliver Pizza" → "Receive Pizza". Two expanded Pools with 4–6 activities each, 2–4 message flows crossing pool boundaries.

**Vertical Collaboration** (OMG Examples §10.4): Demonstrates an alternative vertical layout with Pools stacked left-to-right rather than top-to-bottom, showing that orientation is a DI concern, not a semantic one.

## Conformance Level

Analytic — includes Pools, Lanes, Message Flows, intermediate message events.

## Structure

```
┌─────────────────────────────── Pool A (Participant A) ────────────────────────┐
│  [Start] → [Task A1] → [Task A2] → ◇XOR → [Task A3] → [End]                │
│                  │                                          ↑                 │
└──────────────────┼──────────────────────────────────────────┼─────────────────┘
                   ↓ Message Flow                             ↑ Message Flow
┌──────────────────┼──────────────────────────────────────────┼─────────────────┐
│  [Start] → [Task B1] → [Task B2] → [Task B3] → [End]                        │
│                         Pool B (Participant B)                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Variant A: Expanded Collaboration (default)
- Both Pools are expanded showing internal processes
- Message flows connect specific activities/events across Pools
- Best for: detailed process-to-process mapping

### Variant B: Black-Box Collaboration
- One or both Pools are collapsed (no internal activities visible)
- Message flows attached to Pool boundary
- Best for: high-level interaction overview, external partner process is unknown
- Ref: OMG formal spec Figure 7.6

### Variant C: Multi-Pool (3+ Participants)
- Three or more expanded or mixed Pools
- Message flows form a mesh between Pools
- Best for: supply chain, multi-party business process

## Layout Rules

**Specialized pool-slot layout** — this diagram does NOT use `auto_layout()`. Pool slot positions are fixed vertically (top Pool occupies upper half, bottom Pool lower half), and activities are distributed horizontally within each Pool using uniform spacing. This is an intentional exception due to the two-Pool structure requiring explicit vertical partitioning.

### Zone Constraints

| Zone | Placement | Notes |
|------|-----------|-------|
| Pool header | Left vertical strip or top horizontal strip | 12–15% of pool width/height |
| Activities | Horizontal left-to-right within each Pool | Evenly distributed |
| Message flows | Vertical dashed arrows crossing Pool boundaries | Must connect to specific shapes, not floating |
| Gateways | Diamond shapes inline with sequence flow | Same vertical alignment as connected tasks |
| Start/End events | Circle shapes at flow extremes | Reserve dedicated space |

### Sizing (10" × 5.63" slide)

| Element | Dimension |
|---------|-----------|
| Pool height (2-pool) | 2.0–2.4" each |
| Pool gap (message flow space) | 0.4–0.6" |
| Activity box | 1.2" × 0.5" |
| Event circle | 0.22" diameter |
| Gateway diamond | 0.30" × 0.30" |
| Message flow arrow | dashed, 1.5pt |

## Color Semantics

All colors from theme via `ctx.colors`. No hardcoded brand RGB in loader.

| Element | Color Token | Usage |
|---------|-------------|-------|
| Pool A header fill | `primary` | Initiating participant |
| Pool B header fill | `secondary` | Responding participant |
| Pool body fill | `white` or `light` | Clean background |
| Activity fill | `white` | Standard task |
| Activity border | `dark` | 1pt solid |
| Gateway fill | `white` | Diamond outline only |
| Gateway border | `dark` | 1.25pt solid |
| Start event | `primary` | Thin circle, 1.5pt stroke |
| End event | `dark` | Thick circle, 3pt stroke |
| Sequence flow | `dark` | Solid arrow, 1pt |
| Message flow | `secondary` | Dashed arrow, 1.5pt, open arrowhead |
| Message envelope | `secondary` | Small rectangle on message flow |

## Typography

| Text | Location | Size | Weight | Color |
|------|----------|------|--------|-------|
| Pool name | Pool header | 11pt | Bold | White |
| Activity label | Inside activity box | 8pt | Regular | `text` |
| Gateway condition | Near gateway | 7pt | Regular | `dark` |
| Event label | Below event | 7pt | Regular | `dark` |
| Message name | On message flow | 7pt | Italic | `secondary` |
| Slide title | Placeholder idx=0 | Per master | Bold | Per master |
| Slide subtitle | Placeholder idx=1 | Per master | Regular | Per master |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rounded rectangle | Task / Activity |
| Thin circle | Start Event |
| Thick circle | End Event |
| Double circle | Intermediate Event (on boundary or inline) |
| Diamond | Gateway (XOR/AND/OR marker inside) |
| Horizontal rectangle with header | Pool |
| Solid arrow | Sequence Flow (within Pool) |
| Dashed arrow with open head | Message Flow (across Pools) |
| Small envelope on dashed line | Named Message |
| Dotted line | Association (to annotation) |
| Bracket text box | Text Annotation |

## Annotation & Labeling Rules

- **Pool names**: Always labeled; must not be generic ("Pool 1")
- **Message flow labels**: Every message flow must carry a message name (e.g., "Purchase Order", "Confirmation")
- **Gateway labels**: Exclusive gateways must label each outgoing branch with the condition
- **No orphan message flows**: Every message flow must connect two specific shapes across two different Pools; never connect to empty space

## Density Modes

| Mode | Pools | Activities/Pool | Message Flows | Max per Slide |
|------|-------|----------------|---------------|---------------|
| Light | 2 | 3–5 | 2–3 | 1 |
| Standard | 2 | 5–8 | 3–5 | 1 |
| Dense | 3 | 4–6 | 4–8 | 1 |

**Overflow**: If > 8 activities per pool or > 3 pools, split into multiple slides. Use Link events or "continued" annotation to connect across slides.

## Anti-Patterns (Must Avoid)

1. **Message flow within a Pool**: Message flows ONLY cross Pool boundaries. Within a Pool, use Sequence Flows. This is the most common BPMN error.
2. **Sequence flow across Pools**: Sequence flows NEVER cross Pool boundaries. Between Pools, use Message Flows.
3. **Unlabeled message flow**: A dashed arrow with no message name conveys zero information about what is being exchanged.
4. **Collapsed Pool with internal details**: If a Pool is collapsed (black-box), do not show any internal activities — that contradicts the semantics.
5. **Floating message flow**: A message flow that connects to empty space inside a Pool instead of a specific task/event.

## Official Best Practice Notes

From OMG formal spec §9.3 (Pool and Participant):
> "Pools are used when the diagram involves two or more separate business entities or Participants... A Pool acts as the container for the Sequence Flows between Activities within the Participant's Process."

From OMG formal spec §9.4 (Message Flow):
> "A Message Flow is used to show the flow of Messages between two Participants that are prepared to send and receive them... A Message Flow MUST connect two separate Pools."

Constraint from §7.6.2:
> "A Message Flow MUST NOT connect two objects within the same Participant (Pool)."

## Data Contract

```yaml
title: "Order Processing Collaboration"
subtitle: "Customer ↔ Vendor message exchange"
content:
  pools:
    - id: "customer"
      name: "Customer"
      variant: "expanded"    # expanded | collapsed
    - id: "vendor"
      name: "Pizza Vendor"
      variant: "expanded"
  lanes: []  # optional sub-lanes within pools
  nodes:
    - id: "c_start"
      type: "start_event"
      pool: "customer"
      x_in: 0.3
      label: ""
    - id: "c_order"
      type: "task"
      pool: "customer"
      x_in: 1.5
      label: "Place Order"
    # ... more nodes
  flows:
    - from: "c_start"
      to: "c_order"
      type: "sequence"
    # ... more sequence flows
  message_flows:
    - from: "c_order"
      to: "v_receive"
      label: "Purchase Order"
    # ... more message flows
  annotations: []
```

## QA Checklist

- [ ] Slide title/subtitle in master placeholders (idx=0, idx=1)
- [ ] All message flows cross Pool boundaries (never within a Pool)
- [ ] All sequence flows stay within a single Pool (never across Pools)
- [ ] Every message flow has a label
- [ ] Every exclusive gateway has labeled outgoing branches
- [ ] No floating or orphan arrows
- [ ] Pool names are meaningful business participant names
- [ ] Colors from ctx.colors, no hardcoded brand RGB
- [ ] Diagram explainable in 30 seconds by presenter
