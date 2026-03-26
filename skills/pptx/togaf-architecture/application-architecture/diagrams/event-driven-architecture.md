# AA-07: Event-Driven Architecture Diagram — Application Architecture Diagram Spec

_Ref: CNCF Event-Driven Architecture | CloudEvents Specification | Apache Kafka Design Patterns | Martin Fowler EDA_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing how applications communicate via events — publishers producing events to topics/channels, consumers subscribing and reacting — revealing the event topology, data flow, and decoupling structure.

**Use When**:
- Designing or documenting an event-driven or message-driven system
- Planning a migration from synchronous to asynchronous architecture
- Reviewing Kafka / RabbitMQ / Event Grid topic and consumer design
- Communicating event streaming architecture to cross-functional teams
- Performing event-driven design (Event Storming → EDA Diagram)

**Questions Answered**:
- What events are produced, and by whom?
- Which services consume which events (subscriptions)?
- How does event schema versioning work?
- Where are the potential consumer lag or ordering issues?

**Primary Audience**: Platform Architects, Backend Developers, Data Engineers, SRE teams

---

## 2. Visual Layout Specification

**Structure**: Left-to-right flow — publishers → event bus/topics → consumers.

### Variant A: Topic-Centric Layout
- Left column: Publisher / Producer services
- Center column: Event topics/channels (one box per topic)
- Right column: Consumer services
- Best for: Kafka/RabbitMQ topology documentation

### Variant B: Event Flow Diagram
- Sequential event chain: Service emits event → downstream service reacts → emits next event
- Flows read left-to-right or top-to-bottom
- Best for: Choreography-based saga patterns, event chain tracing

### Variant C: Event Mesh Architecture
- Multiple event brokers connected in a mesh
- Publisher and consumer services distributed across the mesh
- Best for: Multi-region or multi-cloud event streaming design

**Grid Proportions**:
- Publisher node: 100pt × 45pt
- Topic/channel box: 100pt × 45pt (center, slightly different color)
- Consumer node: 100pt × 45pt
- Arrow stroke: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Producer/Publisher | Emits events | `#44546A` + White |
| Event Topic / Channel | Message transport pipe | `#00CCD7` + White (hexagon or wide rect) |
| Consumer | Subscribes to events | `#53E3EB` + `#2F2F2F` |
| Event payload edge | Events published | `#00CCD7` solid arrow |
| Command message edge | Direct command (not event) | `#2F2F2F` italic arrow |
| Dead Letter Queue (DLQ) | Failed event sink | `#A5A7AA` + red `!` badge |
| Event schema annotation | Schema version chip | White + `#44546A` border |
| Consumer group | Group of consumers sharing topic | Dashed container `#53E3EB` border |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Service Name | Node label | 10pt | SemiBold, White |
| Topic/Channel Name | Topic identifier | 10pt | Bold, White |
| Event Name | Edge or annotation label | 8pt | SemiBold, `#2F2F2F` |
| Schema Version | Event schema chip | 7pt | Monospace |
| Consumer Group Label | Group container header | 9pt | Regular, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect | Producer or consumer service |
| Hexagon or wide rounded rect | Event topic / message channel |
| Small hexagon | Sub-topic / partition annotation |
| Dashed container | Consumer group |
| Cylinder | Event store / log (Kafka partition) |
| Solid arrow (→) | Event publish |
| Dashed arrow | Event subscribe/consume |
| Double dashed arrow | Request-reply over events |
| Red container | Dead Letter Queue |

---

## 6. Annotation Rules

- **Event name on arrows**: Every publish arrow labeled with event name: "OrderPlaced", "PaymentFailed"
- **Schema version**: On event edge or topic node: "Schema v3.2 (Avro)"
- **Consumer lag indicator**: For operational diagrams: "Lag: 2.4M msgs ⚠" on consumer node
- **Retry policy**: On consumers: "Retry: 3x, DLQ after 3 failures"
- **Event ordering**: Annotation on topic: "Ordered by customerId" or "Unordered"

---

## 7. Content Density Rules

| Mode | Producers | Topics | Consumers | Per Slide |
|---|---|---|---|---|
| Minimum | 1 | 1 | 1 | — |
| Optimal | 3–6 | 5–10 | 4–8 | 10 topics max |
| Maximum | 10 | 20 | 15 | → split by domain |

**Overflow Strategy**: Split by event domain. Each domain (Order Events / Customer Events / Payment Events) on a separate slide. Add a master topology slide showing all domains as labeled rectangles with cross-domain event flows.

---

## 8. Anti-Patterns

1. **Event as command**: Naming events as imperative commands ("processOrder") instead of past-tense domain facts ("OrderPlaced") — events are immutable facts, not instructions.
2. **Single fat topic**: All events from all services go to one topic ("events-all") — destroys consumer autonomy and creates semantic overload.
3. **Missing schema versioning**: Events without schema version annotations — EDA systems break silently when event schemas change without governance.
4. **No DLQ representation**: Not showing Dead Letter Queue — every production event consumer needs a DLQ; omitting it signals operational immaturity.
5. **Synchronous call in EDA diagram**: Showing REST calls mixed with event flows without distinguishing them — command-query-event distinctions must be visually clear.

---

## 9. Industry Reference Patterns

**Martin Fowler's Event Types Taxonomy**:
Fowler distinguishes three event patterns: Event Notification (consumer decides action), Event-Carried State Transfer (event carries the full new state), and Event Sourcing (event log = system of record). Each requires different schema governance and consumer design. Annotate topic arrows with the event type when multiple types coexist.

**Apache Kafka Architecture Patterns**:
Kafka's topology: Topics are the core unit; partitions enable parallelism; consumer groups share partition load. Key producer patterns: transactional outbox (for exactly-once), idempotent producer, and event compaction. This diagram should show partitioning strategy for high-throughput topics and consumer group allocation.

**CNCF CloudEvents Specification**:
The CloudEvents standard defines a common event metadata envelope: specversion, id, source, type, time, datacontenttype, data. For architecture diagrams, the "type" field (e.g., "com.example.order.placed") is the event name shown on publish arrows. Using domain-reversed naming conventions on event labels makes cross-system event routing visible.

---

## 10. Production QA Checklist

- [ ] All published events are named in past-tense domain language ("OrderPlaced", not "processOrder")
- [ ] Every consumer has a Dead Letter Queue path shown or annotated
- [ ] Event schema versions are documented on all topic nodes
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Consumer groups are shown for topics with multiple consumers
- [ ] Ordering semantics (ordered/unordered) annotated on topics
- [ ] Distinction between events and commands is visually clear
- [ ] No spaghetti single-topic-all-events pattern
- [ ] Retry policies shown on consumers handling critical events
- [ ] Presenter can trace one event from producer to all consumers in 60 seconds
