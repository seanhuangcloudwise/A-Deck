# AA-03: Integration & Interface Map — Application Architecture Diagram Spec

_Ref: TOGAF Phase C Integration View | Enterprise Integration Patterns (Hohpe & Woolf) | API Management Standards_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing all significant integration points, interfaces, and data exchange channels between application systems — including directionality, protocol, and data payload types.

**Use When**:
- Designing or reviewing system integration architecture
- Identifying integration complexity and bottlenecks (point-to-point spaghetti)
- Planning API-led connectivity or ESB middleware strategy
- Supporting integration platform selection
- Auditing integration landscape for security, reliability, or compliance review

**Questions Answered**:
- Which systems integrate with each other?
- What protocol and data format does each integration use?
- Where are the integration bottlenecks or single points of failure?
- Is there a hub (ESB/API gateway) or point-to-point topology?

**Primary Audience**: Integration Architects, Solution Architects, Middleware teams, IT Operations

---

## 2. Visual Layout Specification

**Structure**: Node-edge network — application nodes connected by typed integration edges.

### Variant A: Hub-and-Spoke (Integration Platform Centric)
- Integration platform (ESB/API Gateway/MQ) at center
- Application systems arranged around hub
- All integrations route through center
- Best for: Mature integration architecture, API-led pattern

### Variant B: Point-to-Point Network
- Systems as nodes, integrations as direct edges
- Color-coded by protocol type
- Complexity score annotation showing total integration count
- Best for: Current-state spaghetti documentation (As-Is integration audit)

### Variant C: Layered with Data Flow
- Top layer: External/Partner-facing systems
- Middle layer: Core business applications
- Bottom layer: Data platforms / warehouses
- Directional arrows showing data flow direction
- Best for: End-to-end data lineage and integration design

**Grid Proportions**:
- System node: 110pt × 50pt
- Hub node (Variant A): 130pt × 60pt
- Integration layer separation: 80pt between tiers
- Arrow stroke: 2pt for primary flows, 1pt for secondary

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Core system node | Internal primary application | `#00CCD7` |
| Peripheral system | Supporting application | `#53E3EB` |
| External/partner system | Outside organizational boundary | `#A5A7AA` |
| Integration platform | ESB / API GW / MQ hub | `#44546A` + White |
| Synchronous integration edge | REST/SOAP real-time call | `#00CCD7` solid arrow |
| Asynchronous edge | Message queue, event bus | `#44546A` dashed arrow |
| Batch/file transfer edge | Nightly batch, SFTP | `#A5A7AA` dashed thick arrow |
| High-risk integration | No retry, no monitoring | Red border on edge |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| System Name | Node label | 10–11pt | SemiBold, White |
| Integration Label | Edge annotation | 8pt | Regular, `#2F2F2F` |
| Protocol Tag | Edge protocol chip | 7–8pt | Regular italic |
| Layer Header | Tier title | 10pt | Bold, `#44546A` |
| Integration Count | Summary annotation | 9pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect | Internal application system |
| Rounded rect (dashed border) | External/partner system |
| Hexagon or cylinder | Integration platform / message broker |
| Solid directed arrow | Synchronous integration |
| Dashed directed arrow | Asynchronous / event-driven |
| Thick dashed arrow | Batch/file-based integration |
| Bi-directional arrow | Bidirectional sync or mutual subscription |
| Cloud shape | External SaaS service |

**Edge Labeling (Required on every arrow)**:
- Format: "Protocol | Frequency | Payload"
- Example: "REST/JSON | Real-time | Order Events"
- For batch: "SFTP/CSV | Nightly | Customer Records"

---

## 6. Annotation Rules

- **Integration count**: Total number of integrations on slide: "Total: 24 integrations" in annotation box
- **SLA annotation**: Critical integrations (system-of-record level) labeled with availability SLA: "99.9% SLA"
- **Point-to-point count**: For Variant B, show "n×n integrations = X total" as complexity indicator
- **Error handling note**: Integrations with no retry/circuit breaker are annotated with `⚠ No fallback`
- **Security indicator**: Integrations carrying sensitive data tagged with shield icon `🔒`

---

## 7. Content Density Rules

| Mode | Systems | Integration Edges | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 6–10 | 8–20 | 20 edges max |
| Maximum | 15 | 35 | → split by domain or hub |

**Overflow Strategy**: For large integration landscapes, split by integration domain (Customer Domain / Finance Domain / Operations Domain). Each domain shows 5–8 systems and their integration fabric in detail.

---

## 8. Anti-Patterns

1. **Unlabeled edges**: Integration arrows without protocol or payload information — every integration edge must describe what it carries and how.
2. **Bidirectional ambiguity**: Using two-headed arrows without specifying which direction carries which payload — show two separate arrows when flows differ.
3. **Missing integration platform**: In hub-and-spoke architectures, not showing the ESB/API gateway removes the central architectural decision from the diagram.
4. **System cloud diagrams**: Showing cloud/SaaS bubbles without integration type annotations — SaaS systems must also have defined protocols and contracts.
5. **Port-level detail overload**: Listing every field of every message — integration maps operate at system/flow level, not message field level (use API spec for that).

---

## 9. Industry Reference Patterns

**Enterprise Integration Patterns (Hohpe & Woolf, 2003)**:
The EIP catalog defines 65 messaging patterns including: Message Channel, Message Router, Message Translator, Message Filter, Aggregator. For integration maps, the most important structural patterns are: Pipe-and-Filter (sequential processing), Publish-Subscribe (event broadcast), Request-Reply (synchronous call), and Dead Letter Channel (failure handling). Annotate integration edges with the relevant EIP pattern name when communication mode is complex.

**MuleSoft API-Led Connectivity**:
MuleSoft's architecture divides integrations into three tiers: System APIs (connecting to core systems), Process APIs (orchestrating business logic), Experience APIs (exposing data to consumers). This three-tier model maps to Variant C's three-layer layout. Each tier has different SLA, security, and governance requirements.

**TOGAF Integration Architecture Standard**:
TOGAF recommends an Integration Architecture view as a sub-view of Application Architecture. Key artifacts: Integration Matrix (which systems integrate with which), Interface Catalog (per-integration protocol and data contract), and Integration Diagram (this diagram). The Integration Matrix is the tabular companion to this visual.

---

## 10. Production QA Checklist

- [ ] Every integration edge has a protocol and payload type label
- [ ] Integration directionality is unambiguous on every arrow
- [ ] External/partner systems are visually distinct from internal systems
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Hub/platform node is present and labeled if hub-and-spoke topology
- [ ] High-risk integrations (no fallback) are flagged
- [ ] Security annotations present on integrations carrying sensitive data
- [ ] Total integration count is stated in annotation or subtitle
- [ ] No unconnected system nodes (every system has at least one integration)
- [ ] Presenter can explain the integration strategy (hub-and-spoke vs. P2P) in 30 seconds
