# BP-09: Compensation and Transaction Pattern — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.7 Compensation, §10.2.4 Transaction Sub-Process, Figures 10.33–10.34, 10.121; BPMN 2.0 by Example dtc/10-06-02 §12 "E-Mail Voting Example"_

---

## Purpose

Show **exception handling, rollback, and compensation flows** using BPMN Transaction Sub-Processes, Compensation Boundary Events, and Cancel/Error End Events. This is the pattern for "if something goes wrong, here's how we undo/compensate."

## When to Use

- Documenting saga patterns in microservice architectures
- Showing transactional boundaries with rollback/compensation paths
- Modeling business processes with cancellation and partial completion handling
- Payment/booking systems where failed steps require undo of prior steps

## Official Case Anchor

**E-Mail Voting Example** (OMG Examples §12): A process with an embedded non-interrupting Event Sub-Process for receiving votes. If a quorum is not reached within the time limit, a compensation activity undoes the partial vote tally. Uses Timer, Compensation, and Event Sub-Process patterns.

**Transaction Sub-Process** (OMG formal spec Figures 10.33–10.34): A special Sub-Process with a double-lined border, supporting three outcomes:
1. Successful completion (normal End Event)
2. Cancellation (Cancel End Event → Cancel Boundary Event)
3. Hazard/Error (Error End Event → Error Boundary Event)

**Compensation Handler** (OMG formal spec §10.7, Figure 10.121): An activity attached to a Compensation Boundary Event via Association (dotted line). When compensation is triggered, the handler executes to undo the completed activity's effects.

## Conformance Level

Common Executable — Transaction, Compensation, Cancel events.

## Structure

```
[●Start] → ╔═ Transaction Sub-Process ══════════╗ → [◉End]
            ║ [●S] → [Book Flight] → [Book Hotel] → [◉E]  ║
            ║          ↺Compensate     ↺Compensate         ║
            ╚═══════════⊗Cancel════⚡Error═══════════════════╝
                         ↓              ↓
                   [Cancel Booking]  [Handle Error]
                   (compensation of   → [◉End₂]
                    Book Flight +
                    Book Hotel)
```

### Variant A: Transaction with Compensation
- Transaction Sub-Process (double-border) with Cancel/Error outcomes
- Compensation handlers attached to specific activities
- Best for: booking/payment saga patterns

### Variant B: Compensation Chain
- Multiple activities each with a Compensation Boundary Event
- Compensation is triggered in reverse order
- Best for: showing undo sequence explicitly

### Variant C: Simple Cancel/Error Handling
- Non-transaction Sub-Process with boundary Error/Cancel events
- Simpler than full Transaction pattern
- Best for: error handling without formal compensation

## Layout Rules

**Dual-region `auto_layout()`** — the transaction interior and the parent process each call `auto_layout()` independently. **Do not hardcode x/y positions in config or loader.**

- **Transaction internal nodes** (e.g., Book Flight, Book Hotel): `auto_layout()` within the transaction rect interior
- **Parent process nodes** (Start, Transaction box, End, exception paths): `auto_layout()` across the full slide content area, treating the transaction box as a single opaque node

### Structural Zones (applied after layout)

| Zone | Constraint |
|------|-----------|
| Transaction Sub-Process | Center, 50–70% of content width; position set by parent `auto_layout()` |
| Double border | 2pt outer + 1.5pt inner with 2px gap; applied after position is set |
| Compensation handlers | Below transaction; fixed y-offset from transaction bottom |
| Cancel/Error boundary events | Bottom edge of transaction rectangle |
| Cancel/Error exception flow | Downward from boundary event |
| Successful outcome flow | Right side of transaction → End |

### Sizing

| Element | Dimension |
|---------|-----------|
| Transaction box | 4.0–6.0" × 1.5–2.0" |
| Double border gap | 2px between borders |
| Compensation handler box | 1.0" × 0.4" |
| Association (dotted line) | 1pt dotted |
| Boundary event | 0.22" on Transaction border |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Transaction border (double) | `primary` |
| Transaction fill | `white` |
| Compensation event (⟲) | semantic amber `#E6A817` |
| Compensation handler fill | semantic amber `#E6A817` 15% opacity |
| Compensation handler border | semantic amber `#E6A817` |
| Cancel event (×) | semantic orange `#E68A17` |
| Error event (⚡) | semantic red `#D94040` |
| Successful End event | `dark` |
| Association (to compensation handler) | `dark` dotted |
| Normal activities | Same as BP-02 |

## Typography

| Text | Location | Size |
|------|----------|------|
| Transaction label | Top-left inside double border | 9pt SemiBold |
| Internal task labels | Inside boxes | 8pt Regular |
| Compensation handler label | Inside handler box | 7pt Regular |
| Boundary event label | Below event | 7pt Regular |
| Outcome path label | Near path | 7pt Italic |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rectangle with double border | Transaction Sub-Process |
| ⟲ in circle (on border) | Compensation Boundary Event |
| ⟲ in circle (standalone) | Compensation Intermediate Throw Event |
| × in thick circle (end) | Cancel End Event |
| × in double circle (boundary) | Cancel Boundary Event |
| ⚡ in thick circle | Error End Event |
| ⚡ in double circle (boundary) | Error Boundary Event |
| Dotted line (no arrowhead) | Association (connecting compensation handler) |
| Activity with ⟲ marker | Compensation Activity (handler) |

## Anti-Patterns

1. **Compensation handler with incoming sequence flow**: Compensation handlers are triggered by the compensation mechanism, NOT by sequence flow. They connect via Association (dotted), NOT arrows.
2. **Cancel event outside Transaction**: Cancel End Event and Cancel Boundary Event are ONLY meaningful inside/on a Transaction Sub-Process.
3. **Missing compensation for early activities**: If Activity A and Activity B are in a transaction, and B fails, Activity A's compensation handler MUST be defined — otherwise partial completion is not properly undone.
4. **Transaction without three outcomes**: A well-formed Transaction should show all three possible outcomes: success, cancel, and error.
5. **Double border not visible**: The double border is the ONLY visual distinction of a Transaction Sub-Process — it must be clearly rendered.

## Official Best Practice Notes

From OMG formal spec §10.7 (Compensation):
> "Compensation is a mechanism for undoing the effects of a completed Activity. A Compensation Handler is an Activity that is 'associated' with an Activity that has completed normally."

From OMG formal spec §10.7.2 (Compensation Triggering):
> "Compensation can be triggered in two ways: by a Cancel End Event (within a Transaction) or by a Compensation Intermediate Event (throw)... When compensation is invoked, all Compensation Handlers associated with successfully completed Activities are triggered in reverse order."

From OMG formal spec §10.2.4 (Transaction):
> "A Transaction is a specialized type of Sub-Process that will have a special behavior that is controlled through a transaction protocol... The boundary of the Sub-Process will be double-lined."

## Data Contract

```yaml
title: "Travel Booking Saga Pattern"
subtitle: "Transaction with compensation for flight + hotel booking"
content:
  transaction:
    id: "booking_tx"
    label: "Booking Transaction"
    internal_nodes:
      - {id: "tx_start", type: "start_event"}
      - {id: "book_flight", type: "service_task", label: "Book Flight"}
      - {id: "book_hotel", type: "service_task", label: "Book Hotel"}
      - {id: "confirm", type: "task", label: "Confirm Booking"}
      - {id: "tx_end", type: "end_event"}
      - {id: "tx_cancel", type: "cancel_end_event"}
    internal_flows:
      - {from: "tx_start", to: "book_flight"}
      - {from: "book_flight", to: "book_hotel"}
      - {from: "book_hotel", to: "confirm"}
      - {from: "confirm", to: "tx_end"}
  compensation_handlers:
    - activity: "book_flight"
      handler: {id: "cancel_flight", label: "Cancel Flight"}
    - activity: "book_hotel"
      handler: {id: "cancel_hotel", label: "Cancel Hotel"}
  boundary_events:
    - {id: "cancel_boundary", type: "cancel_boundary", attached_to: "booking_tx"}
    - {id: "error_boundary", type: "error_boundary", attached_to: "booking_tx"}
  exception_flows:
    - {from: "cancel_boundary", to: "notify_cancel", label: "Cancelled"}
    - {from: "error_boundary", to: "error_handler", label: "Error"}
```

## QA Checklist

- [ ] Transaction Sub-Process has visible double border
- [ ] Compensation handlers connected by Association (dotted), NOT sequence flow
- [ ] Cancel events only inside/on Transaction Sub-Process
- [ ] All completed activities within Transaction have Compensation handlers
- [ ] Three outcomes visible: success, cancel, error
- [ ] Color semantics: amber for compensation, red for error, orange for cancel
- [ ] Colors from ctx.colors where possible; semantic reserved colors documented
