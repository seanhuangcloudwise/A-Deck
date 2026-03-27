# BP-06: Choreography Interaction — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §11 Choreography, §11.2–11.5, Figures 11.1–11.21; BPMN 2.0 by Example dtc/10-06-02 §10.6 "Choreography Example", §6.2 "Detailed Collaboration and Choreography"_

---

## Purpose

Show the **expected ordering of message exchanges between participants** without revealing any participant's internal process. A Choreography diagram focuses on "what messages are exchanged, in what order, between whom" — the behavioral contract.

## When to Use

- Defining a B2B interaction protocol (message exchange agreement)
- Specifying service choreography before implementation
- Documenting message ordering requirements between microservices
- Contract-first design: what each party commits to send and receive

## Official Case Anchor

**Choreography Example** (OMG Examples §10.6): A standalone choreography diagram showing a sequence of Choreography Tasks between two participants, with one participant band on top (initiator) and one on bottom (responder) of each task. The message name appears on the task itself.

**Detailed Collaboration and Choreography** (OMG Examples §6.2): Shows how the same incident management scenario can be modeled as both a Collaboration diagram (with Pools) and a Choreography diagram (with Choreography Tasks). Demonstrates the duality between the two viewpoints.

**Logistics Choreography** (OMG formal spec Figures 11.3–11.4): A logistics collaboration view is shown alongside the equivalent choreography diagram, illustrating 1:1 mapping between message flows in collaboration and choreography tasks in choreography.

## Conformance Level

Choreography Conformance — dedicated BPMN conformance sub-class for choreography modeling.

## Structure

```
[●Start] → ┌──Participant A──┐ → ┌──Participant B──┐ → ◇XOR → ┌──Participant A──┐ → [◉End]
            │  Order Request  │   │ Order Confirm   │         │  Ship Notice    │
            └──Participant B──┘   └──Participant A──┘         └──Participant B──┘
```

Each Choreography Task is a **rounded rectangle** with:
- Top band: Initiating participant (shaded/dark)
- Center: Task name (message/interaction name)
- Bottom band: Responding participant (light)

### Variant A: Linear Choreography
- Sequential choreography tasks
- Best for: simple request-response-confirm patterns

### Variant B: Choreography with Gateways
- XOR/AND gateways between choreography tasks
- Best for: conditional or parallel message exchanges

### Variant C: Sub-Choreography
- Collapsed or expanded sub-choreography box
- Ref: OMG formal spec Figures 11.17–11.21
- Best for: reusable interaction patterns

## Layout Rules

**Specialized choreography band layout** — this diagram does NOT use `auto_layout()`. Each Choreography Task is laid out left-to-right at equal spacing; participant bands (initiator top, responder bottom) are drawn as fixed sub-regions of each task box. This is an intentional exception due to the unique stacked-band shape requiring per-task band partitioning rather than node-graph layout.

| Zone | Placement |
|------|-----------|
| Choreography tasks | Left-to-right, evenly spaced |
| Participant bands | Top and bottom bands of each task box |
| Initiator band | Always the TOP band (shaded) |
| Gateways | Inline between choreography tasks |
| Start/End events | Leftmost / rightmost |

### Sizing

| Element | Dimension |
|---------|-----------|
| Choreography Task box | 1.4" × 0.8" total (top band 0.2", center 0.4", bottom band 0.2") |
| Participant band height | 0.2" |
| Event circle | 0.22" |
| Gateway diamond | 0.30" |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Initiator band (top) | `primary` fill, white text |
| Responder band (bottom) | `light` fill, `dark` text |
| Task center | `white` |
| Task border | `dark` 1pt |
| Multi-participant marker | Small "≡" lines in band |
| Envelope icon (message) | `secondary` on initiator side |
| Gateway / Event | Same as BP-02 |
| Sequence flow | `dark` solid arrow |

## Typography

| Text | Location | Size |
|------|----------|------|
| Participant name | In band | 7pt SemiBold |
| Interaction name | Task center | 8pt Regular |
| Message name | Small label near envelope icon | 7pt Italic |
| Gateway condition | Near branch | 7pt Regular |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rectangle with top/bottom bands | Choreography Task |
| Rectangle with [+] and bands | Sub-Choreography (collapsed) |
| Expanded rectangle with bands | Sub-Choreography (expanded) |
| Shaded band | Initiating participant |
| Light band | Responding participant |
| Envelope (✉) | Message associated with the interaction |
| "≡" in band | Multi-instance participant |

## Anti-Patterns

1. **Showing internal process in choreography**: Choreography tasks do NOT reveal what happens inside each participant — that is the Collaboration view's job.
2. **Missing initiator identification**: One participant must be clearly marked as the initiator (shaded band). Without it, the message direction is ambiguous.
3. **Choreography Task with only one participant**: Each task must have at least two participant bands — it represents an interaction between participants.
4. **Sequence flow between participants**: In choreography, sequence flow connects Choreography Tasks, NOT participants. Participants appear only as bands on tasks.

## Official Best Practice Notes

From OMG formal spec §11.2:
> "A Choreography is a type of Process, but differs in purpose and behavior. Instead of orchestrating the work performed within a Participant, it tracks the exchange of Messages (interactions) between Participants."

From OMG formal spec §11.5 (Choreography Task):
> "A Choreography Task can have two or more Participants. One of the Participants is the initiator of the Choreography Task... The initiator Participant sends the initial Message of the task. The non-initiator Participants receive this message."

## Data Contract

```yaml
title: "Order Processing Choreography"
subtitle: "Message exchange protocol between Buyer and Seller"
content:
  participants:
    - id: "buyer"
      name: "Buyer"
    - id: "seller"
      name: "Seller"
    - id: "shipper"
      name: "Shipper"
  choreography_tasks:
    - id: "request_quote"
      initiator: "buyer"
      responder: "seller"
      name: "Request Quote"
      message: "RFQ Document"
    - id: "send_quote"
      initiator: "seller"
      responder: "buyer"
      name: "Send Quote"
      message: "Price Quote"
    - id: "place_order"
      initiator: "buyer"
      responder: "seller"
      name: "Place Order"
      message: "Purchase Order"
    - id: "arrange_shipping"
      initiator: "seller"
      responder: "shipper"
      name: "Arrange Shipping"
      message: "Shipping Request"
  flows:
    - from: "start"
      to: "request_quote"
    - from: "request_quote"
      to: "send_quote"
    - from: "send_quote"
      to: "place_order"
    - from: "place_order"
      to: "arrange_shipping"
    - from: "arrange_shipping"
      to: "end"
  gateways: []
```

## QA Checklist

- [ ] Every Choreography Task has initiator (shaded) and responder bands
- [ ] Initiator band is consistently on top
- [ ] Each task names the interaction and optionally the message
- [ ] No internal process detail shown
- [ ] Gateways connect Choreography Tasks (not participants)
- [ ] Colors from ctx.colors
