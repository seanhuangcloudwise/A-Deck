# AA-10: Application Sequence Flow — Application Architecture Diagram Spec

_Ref: UML Sequence Diagram (OMG) | C4 Dynamic Diagram | TOGAF Application Behavior View_

---

## 1. Purpose & When to Use

**Definition**: A time-ordered diagram showing the sequence of calls, messages, and responses between application actors and services for a specific use case or scenario — combining service identity with temporal ordering.

**Use When**:
- Documenting the technical implementation of a critical business use case
- Debugging a production issue by mapping the actual call sequence
- Designing the interaction protocol for a new feature before coding
- Reviewing latency and critical path for SLA violations
- Communicating technical flow to security reviewers or compliance auditors

**Questions Answered**:
- In what exact order do services interact for this use case?
- Where is the latency accumulated?
- What data is passed between services at each step?
- Which step is the most likely failure point?

**Primary Audience**: Developers, Tech Leads, SRE, Security Architects, QA Engineers

---

## 2. Visual Layout Specification

**Structure**: Lifeline-based sequence diagram — participants as vertical bars, interactions as horizontal timed arrows.

### Variant A: Standard Presentation Sequence (Simplified UML)
- Participants as boxes at top, ordered by call sequence
- Numbered arrows between participants
- Return arrows shown as dashed
- Best for: Architecture review, onboarding

### Variant B: Swimlane Sequence (Role-plus-System)
- Two types of participants: Human roles (oval) + System services (rect)
- Human-to-system calls on top; system-to-system calls below
- Best for: Business-technical hybrid flows

### Variant C: Timing-Annotated Sequence
- Same structure as Variant A
- Elapsed time noted on each arrow: "+50ms", "+200ms"
- Critical path highlighted in bold/cyan
- Total cumulative time shown at each lifecycle point
- Best for: Performance review, SLA analysis

**Grid Proportions**:
- Participant box: 90pt × 36pt
- Lifeline: vertical line, dashed, below participant box
- Interaction arrow: horizontal, spanning lifelines
- Participant spacing: equal-width, minimum 100pt apart

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| External client / user | Request originator | `#44546A` + White |
| Internal service lifeline | Service interaction lane | `#00CCD7` |
| Gateway / proxy participant | Interceptor service | `#44546A` |
| Database / data store | Persistence layer | `#2F2F2F` cylinder |
| External service | 3rd party / partner | `#A5A7AA` |
| Sync call arrow | Request → direction | `#00CCD7` solid |
| Return arrow | Response ← direction | `#A5A7AA` dashed |
| Async call | Non-blocking request | `#44546A` dashed |
| Critical path arrow | Latency-limiting step | `#00CCD7` bold (3pt) |
| Error / exception arrow | Failure path | Red dashed |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Participant Name | Lifeline header | 10pt | SemiBold, White |
| Call Label | Arrow description | 8pt | Regular |
| Message Payload | Data annotation below arrow | 7pt | Monospace, `#2F2F2F` |
| Sequence Number | Numbered badge on arrow | 9pt | Bold in circle |
| Timing Annotation | "+Xms" elapsed time | 8pt | Italic, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rectangle box | Service / system participant |
| Oval | Human role participant |
| Cylinder | Database or storage participant |
| Dashed vertical line | Lifeline (participant timeline) |
| Filled rect on lifeline | Activation bar (processing period) |
| Solid horizontal arrow | Synchronous call |
| Dashed horizontal arrow | Response or async message |
| Red dashed arrow | Error / exception |
| Self-call arrow (curved) | Internal call within same service |
| Fragment frame | Loop / Alternative / Optional grouping |

---

## 6. Annotation Rules

- **Message payload**: Below each call arrow: abbreviated payload (8pt monospace): `{orderId, customerId}`
- **Activation bar shading**: Filled bar on lifeline shows when service is processing (not idle)
- **Error handling frame**: Use "alt" fragment box when showing error vs. success paths side by side
- **Timing markers**: Elapsed time on arrows: "+50ms". Total at last step: "Total: ~350ms"
- **External reference**: Link to API contract or schema: "→ POST /orders (API v2)"

---

## 7. Content Density Rules

| Mode | Participants | Steps | Per Slide |
|---|---|---|---|
| Minimum | 2 | 3 | — |
| Optimal | 4–7 | 8–15 | 15 steps max per slide |
| Maximum | 10 | 25 | → split at transaction boundary |

**Overflow Strategy**: Split at a transaction boundary (e.g., "Request Phase" / "Processing Phase" / "Notification Phase"). Add a mini participant-strip header on each continuation slide for orientation.

---

## 8. Anti-Patterns

1. **All-at-once layout**: Showing a 40-step sequence on one slide — microscopic arrows that no one can read. Respect the 15-step limit per slide.
2. **Missing return arrows**: Omitting response flows when synchronous calls need them — one-way representation implies async, which may be wrong.
3. **Unnamed participant boxes**: "Service 1 → Service 2 → Service 3" — every participant must have its actual service name.
4. **No error path**: Only happy-path sequence — for any call that can fail in production, the error path must be shown.
5. **Payload detail overload**: Showing full JSON request bodies inline — payload annotations should be field names only, not full messages (use API spec for details).

---

## 9. Industry Reference Patterns

**UML Sequence Diagram (OMG UML 2.5)**:
UML formalized the sequence diagram with lifelines, activation bars, combined fragments (loop, alt, opt, par), and message types (synchronous, asynchronous, return, create, destroy). For presentation use, retain: lifelines, numbered arrows, activation bars, and alt fragments for error paths. Drop: object lifecycle (create/destroy) unless relevant to the scenario.

**C4 Dynamic Diagram (Simon Brown)**:
The C4 Model's Dynamic Diagram is a sequence flow at the Container or Component level (C4 levels 2 and 3). It uses numbered arrows between containers/components to describe a specific runtime scenario. The key C4 principle: one dynamic diagram = one scenario / use case. Don't try to show multiple use cases in one diagram.

**Netflix Operational Design Reviews**:
Netflix's architecture review process requires a sequence diagram for any new service interaction that crosses team boundaries. Each sequence must include: latency budget per call, circuit breaker strategy, fallback behavior when downstream unavailable. This "operational sequence diagram" pattern extends the standard UML sequence with SRE concerns directly in the design phase.

---

## 10. Production QA Checklist

- [ ] All participants are named with actual service/system names
- [ ] Every interaction arrow has a call description label
- [ ] Return arrows present for all synchronous calls
- [ ] Error path shown for at least the most critical failure scenario
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Sequence numbers present on all arrows
- [ ] Payload annotations present on all significant data-carrying calls (field names, not full payloads)
- [ ] For Variant C: timing annotations present, critical path highlighted in bold
- [ ] Maximum 15 interactions per slide (split if more)
- [ ] Presenter can walk through the sequence exactly as it executes in production in under 90 seconds
