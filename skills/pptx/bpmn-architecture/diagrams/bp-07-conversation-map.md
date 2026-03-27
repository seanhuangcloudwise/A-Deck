# BP-07: Conversation Map — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §9.5 Conversations, §9.5.1–9.5.7, Figures 9.16–9.31; BPMN 2.0 by Example dtc/10-06-02 §10.5 "Conversation Example"_

---

## Purpose

Show the **logical grouping of message exchanges between participants** at a high level. A Conversation diagram answers "which participants talk about what topics" without showing the sequence of messages or internal processes. It is the highest-level BPMN interaction view.

## When to Use

- Stakeholder communication overview — who communicates with whom
- Identifying integration domains before designing detailed collaborations
- Business domain mapping — grouping related message exchanges into Conversations
- Requirements elicitation — establishing communication channels between actors

## Official Case Anchor

**Conversation Example** (OMG Examples §10.5): A Conversation diagram showing multiple Participants connected by hexagonal Conversation nodes. Each hexagon represents a group of logically-related message exchanges. Lines connect Participants to the Conversations they participate in.

**Sub-Conversation** (OMG formal spec Figures 9.19–9.21): A hexagon with [+] marker, expanding into sub-conversations or detailed message flows. Demonstrates hierarchical conversation decomposition.

**Call Conversation** (OMG formal spec Figures 9.25–9.26): A hexagon with thick border calling a globally-defined Conversation or Collaboration.

## Conformance Level

Analytic — Conversation nodes (hexagon), Participants, Conversation Links.

## Structure

```
[Participant A] ─── ⬡ Conversation X ─── [Participant B]
                        │
                    ⬡ Conversation Y ─── [Participant C]
```

### Variant A: Simple Conversation Map
- 2–5 Participants connected by 2–4 Conversation hexagons
- Best for: quick communication overview

### Variant B: Sub-Conversation
- Conversation hexagons with [+] marker (collapsed sub-conversation)
- Can be expanded to show internal conversations or message flows
- Best for: hierarchical grouping of communication topics

### Variant C: Multi-Domain Conversation
- Multiple Conversation hexagons arranged by business domain
- Domain grouping via visual clustering (not BPMN Group shape)
- Best for: enterprise-level integration landscape mapping

## Layout Rules

**Specialized conversation ring/network layout** — this diagram does NOT use `auto_layout()`. Participant nodes are placed in a ring or network arrangement; Conversation hexagons are positioned midway on the line between their connected participants. This is an intentional exception because the diagram represents a bipartite network (Participants ↔ Conversations), not a DAG flow.

| Zone | Placement |
|------|-----------|
| Participants | Arranged as nodes in a network graph |
| Conversation hexagons | Between connected Participants |
| Conversation Links | Lines connecting Participants to Conversations |
| Sub-Conversation [+] | Hexagon with marker |

### Sizing

| Element | Dimension |
|---------|-----------|
| Participant rectangle | 1.0" × 0.5" |
| Conversation hexagon | 0.8" × 0.5" |
| Sub-Conversation hexagon | 0.9" × 0.55" (with [+]) |
| Conversation Link line | 1pt solid |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Participant fill | `primary` light variant |
| Participant border | `primary` |
| Participant text | `white` or `dark` depending on fill |
| Conversation hexagon fill | `secondary` |
| Conversation hexagon border | `dark` |
| Conversation hexagon text | `white` |
| Sub-Conversation [+] | `dark` |
| Call Conversation border | `primary` thick 2.5pt |
| Conversation Link | `dark` 1pt solid |

## Typography

| Text | Location | Size |
|------|----------|------|
| Participant name | Inside rectangle | 8pt SemiBold |
| Conversation name | Inside hexagon | 7pt Regular |
| Link annotation (optional) | Near link line | 6pt Italic |

## Shape Vocabulary

| Shape | BPMN Meaning |
|-------|-------------|
| Rectangle (with or without icon) | Participant |
| Hexagon | Conversation (group of related message exchanges) |
| Hexagon with [+] | Sub-Conversation (collapsed) |
| Hexagon with thick border | Call Conversation |
| Solid line (no arrowhead) | Conversation Link |
| Forked line (3-prong) | Conversation Association (linking to activities/events in other views) |

## Anti-Patterns

1. **Showing sequence in Conversation diagram**: Conversations do NOT imply ordering. For message sequence, use Choreography (BP-06) or Collaboration (BP-01).
2. **Arrow-headed Conversation Links**: Conversation Links have NO arrowheads — they represent bidirectional participation, not directed message flow.
3. **Single-participant Conversation**: Every Conversation must involve at least 2 Participants.
4. **Conversation as Process**: A Conversation hexagon is NOT a task/activity — it represents a collection of message exchanges.

## Official Best Practice Notes

From OMG formal spec §9.5:
> "A Conversation is a logical grouping of Message exchanges... The purpose of the Conversation diagram is to provide a quick overview of the Message exchanges between Participants."

From OMG formal spec §9.5.2 (Sub-Conversation):
> "A Sub-Conversation is a Conversation that can be 'opened up' (expanded) to show the lower-level Conversations or Message Flows."

## Data Contract

```yaml
title: "Enterprise Integration Conversation Map"
subtitle: "High-level message domain overview across departments"
content:
  participants:
    - id: "crm"
      name: "CRM System"
    - id: "erp"
      name: "ERP System"
    - id: "warehouse"
      name: "Warehouse"
    - id: "customer"
      name: "Customer Portal"
  conversations:
    - id: "order_mgmt"
      name: "Order Management"
      type: "conversation"  # conversation | sub_conversation | call_conversation
      connected_participants: ["customer", "crm", "erp"]
    - id: "fulfillment"
      name: "Fulfillment"
      type: "sub_conversation"
      connected_participants: ["erp", "warehouse"]
    - id: "billing"
      name: "Billing & Payment"
      type: "conversation"
      connected_participants: ["erp", "customer"]
```

## QA Checklist

- [ ] Hexagons used for Conversations (not rectangles or circles)
- [ ] Conversation Links have NO arrowheads
- [ ] Every Conversation connects ≥ 2 Participants
- [ ] No sequence/ordering implied in layout
- [ ] Sub-Conversations marked with [+]
- [ ] Colors from ctx.colors
