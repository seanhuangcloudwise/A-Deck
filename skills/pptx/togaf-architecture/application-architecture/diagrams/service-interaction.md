# AA-05: Service Interaction Diagram — Application Architecture Diagram Spec

_Ref: TOGAF Application Collaboration View | ArchiMate 3.1 Application Interaction | SOA Collaboration Pattern_

---

## 1. Purpose & When to Use

**Definition**: A runtime collaboration diagram showing how application services interact with each other at the service level — calls, events, and responses — for a specific business scenario or user flow.

**Use When**:
- Designing the runtime interaction model between services for a feature
- Reviewing inter-service coupling before deployment
- Documenting the application architecture for a specific business process
- Identifying which services are involved in a given use case
- Serving as design input for contract testing and interface specification

**Questions Answered**:
- Which services collaborate to fulfill this business scenario / use case?
- What is the interaction type (sync call, event, callback)?
- What is the dependency chain and critical path?
- Which services are potential bottlenecks or failure propagation points?

**Primary Audience**: Solution Architects, Developers, Tech Leads, Product Architects

---

## 2. Visual Layout Specification

**Structure**: Left-to-right collaborating services with directed interaction arrows.

### Variant A: Flow-Oriented Interaction
- Services arranged left-to-right in approximate call sequence
- Arrows show call direction with sequence numbers
- Best for: Sync call chains (REST, gRPC)

### Variant B: Event-Driven Interaction
- Publisher services on left, event channel in center, consumer services on right
- Event topic shown on channel element
- Best for: Async event-driven or messaging architectures

### Variant C: Hub-Orchestration View
- Orchestrating service at center
- Participant services around hub (star topology)
- Orchestration arrows show directed calls/responses
- Best for: Saga orchestration, API gateway orchestration

**Grid Proportions**:
- Service node: 100pt × 50pt
- Event channel: 80pt × 40pt (narrow)
- Horizontal service spacing: 100pt
- Numbered sequence badge: 20pt circle

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Initiating service | Entry point / caller | `#44546A` + White |
| Core domain service | Primary business logic | `#00CCD7` + White |
| Supporting service | Infrastructure, shared utility | `#53E3EB` + `#2F2F2F` |
| External/3rd party service | Outside own codebase | `#A5A7AA` + dashed border |
| Event channel / topic | Message bus, Kafka topic | `#44546A` hexagon |
| Sync call arrow | REST/gRPC request | `#00CCD7` solid |
| Async event arrow | Published event | `#44546A` dashed |
| Response arrow | Return path | `#A5A7AA` thin arrow |
| Error/failure path | Exception flow | Red dashed arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Service Name | Node label | 10–11pt | SemiBold, White |
| Interaction Label | Arrow description | 8pt | Regular |
| Sequence Number | Call order badge | 9pt | Bold, White in circle |
| Event Topic Label | Channel identifier | 9pt | SemiBold, White |
| Protocol Tag | HTTP/gRPC/Kafka | 7pt | Italic, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Application service |
| Hexagon or cylinder | Event channel / message broker |
| Bold border rounded rect | Orchestrator service |
| Dashed border rounded rect | External service |
| Solid arrow with sequence # | Synchronous call (numbered) |
| Dashed arrow | Async event publish/subscribe |
| Return arrow (thin) | Response / callback |
| Red dashed arrow | Error handling path |

---

## 6. Annotation Rules

- **Sequence numbers**: Numbered badges (①②③) on call arrows to show order
- **SLA on critical calls**: Key interaction arrows annotated with max latency: "≤200ms"
- **Failure propagation**: When one service fails, annotate which downstream services are affected
- **Retry policy**: Critical calls: "3 retries, exponential backoff" as annotation
- **Contract reference**: Arrow annotation linking to API spec: "→ API Contract v2.1"

---

## 7. Content Density Rules

| Mode | Services | Interactions | Per Slide |
|---|---|---|---|
| Minimum | 2 | 1 | — |
| Optimal | 4–8 | 5–12 | 10 interactions max |
| Maximum | 12 | 20 | → split by scenario phase |

**Overflow Strategy**: Split complex interactions by scenario phase. Phase 1: "Initiation" (3–4 services). Phase 2: "Processing" (4–5 services). Phase 3: "Completion" (3–4 services). Add mini flow indicator at top of each slide.

---

## 8. Anti-Patterns

1. **Sequence diagram disguise**: Drawing a full UML sequence diagram in a presentation — service interaction diagrams should show service topology, not message-by-message sequences.
2. **No sequence ordering**: Showing all interactions without numbered sequence badges — viewers can't understand the order of operations.
3. **Missing failure paths**: Only showing the happy path — production-grade diagrams must show at least the primary error handling path.
4. **Star-with-all-directions**: Every service calling every other service — demonstrates coupling without showing the orchestration pattern.
5. **Generic service names**: "Service A → Service B → Service C" — names must reflect actual service identity ("Order Service", "Payment Service").

---

## 9. Industry Reference Patterns

**TOGAF Application Interaction View (ADM Phase C)**:
TOGAF defines an Application Interaction Matrix showing which applications interact with which, in what direction, and what data they exchange. The Service Interaction Diagram is the visual representation of this matrix for a specific scenario. TOGAF recommends defining interactions at Feature/Use-Case granularity for Phase C.

**ArchiMate 3.1 Application Interaction**:
ArchiMate formalizes Application Interaction as a behavior element: when two or more Application Components collectively perform behavior to produce a result. The Application Collaboration element contains the interacting components. Relationships used: Triggering (chain of calls), Association (informal link), and Composition (component within system).

**Netflix Microservice Collaboration Diagrams**:
Netflix's approach to inter-service architecture visualization uses a "Service Dependency Graph" with circuit breaker overlays. Services that are critical-path are shown with bold borders; services with active circuit breakers are shown in amber. This real-world operational context makes the diagram actionable for both design and operations teams.

---

## 10. Production QA Checklist

- [ ] All interaction arrows have sequence numbers in the order they occur
- [ ] Every arrow has a protocol and interaction description label
- [ ] Error/failure paths are shown for critical interactions
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] External services are visually distinct (dashed border)
- [ ] SLA annotations present on latency-sensitive interactions
- [ ] Services are named after their actual domain identity
- [ ] No unconnected service nodes
- [ ] Presenter can walk through the full interaction sequence in under 90 seconds
- [ ] Service names consistent with AA-01 Application Landscape vocabulary
