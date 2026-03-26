# BA-04: Organization & Actor Interaction — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B | ArchiMate 3.1 Business Layer | UML Collaboration Diagram_

---

## 1. Purpose & When to Use

**Definition**: A structured diagram showing how different organizational roles, actors, and units collaborate, communicate, or depend on each other to achieve a shared business outcome.

**Use When**:
- Mapping cross-team or cross-department collaboration models
- Clarifying role boundaries and interaction responsibilities before an org change
- Designing operating model changes (centralize, decentralize, federate)
- Communicating who is accountable vs. consulted for shared outcomes
- Supporting business case for a new team or function

**Questions Answered**:
- Who interacts with whom in this business scenario?
- What is the nature of each interaction (service, information, decision)?
- Where are the structural gaps or overloaded interfaces?
- What is the correct authority relationship between roles?

**Primary Audience**: Management, HR, Business Architects, Change Management, Operating Model designers

---

## 2. Visual Layout Specification

**Structure**: Node-edge network — role nodes connected by labeled interaction edges.

### Variant A: Hub-and-Spoke (1 central coordinator, 4–8 peripheral actors)
- Central role node (larger box, #44546A fill) at center
- Surrounding role nodes arranged in a ring
- Edges from center to each peripheral with interaction labels
- Best for: Service center, PMO, shared service models

### Variant B: Multi-Party Collaboration (3–7 equal actors, peer interactions)
- Role nodes arranged in a horizontal or slight arc layout
- Bidirectional and unidirectional edges between peers
- Edge labels describe collaboration type
- Best for: Cross-functional team models, partnership ecosystems

### Variant C: Layered Hierarchy (org-level top, operational-level bottom)
- Top row: strategic roles (C-suite, committees)
- Middle row: management roles
- Bottom row: operational/delivery roles
- Vertical edges show authority; horizontal edges show coordination
- Best for: Operating model definition, new org design

**Grid Proportions**:
- Role node standard size: 100pt × 50pt
- Central hub node (Variant A): 120pt × 60pt
- Edge line stroke: 1.5pt
- Interaction label font: 8pt on edge

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Primary role (subject of diagram) | Central actor | `#44546A` + White text |
| Internal organizational role | Team/department | `#00CCD7` + White text |
| External actor / customer | Outside org boundary | `#A5A7AA` + `#2F2F2F` text |
| Automated system/bot role | Non-human actor | `#53E3EB` + `#2F2F2F` text dashed border |
| Service interaction edge | Provides service to | `#00CCD7` solid arrow |
| Information flow edge | Sends information to | `#2F2F2F` dashed arrow |
| Decision/approval authority | Governance relationship | `#44546A` thick arrow |
| Collaboration edge | Works together with | `#53E3EB` double-headed arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Role/Actor Name | Node label | 10–11pt | SemiBold |
| Role Description | Small label under node | 8pt | Regular, `#A5A7AA` |
| Edge Label | Interaction description | 7–8pt | Regular |
| Boundary Label | Org unit or zone label | 9pt | Regular italic |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Internal organizational role |
| Rounded rect with dashed border | External or automated actor |
| Ellipse/oval | Customer or end-user persona |
| Bold-border rounded rect | Primary subject role |
| Dashed enclosure | Organizational unit boundary |
| Solid arrow | Directed service/information provision |
| Double-headed arrow | Mutual collaboration |
| Thick arrow | Decision authority / mandated instruction |
| Dashed arrow | Optional or indirect information flow |

---

## 6. Annotation Rules

- **Interaction type labels**: Every edge must carry a short label (≤4 words): "reviews", "approves", "provides data to", "escalates to"
- **Frequency badge**: Small gray chip on edge for recurring interactions — "Daily", "Weekly", "Ad-hoc"
- **Pain-point marker**: Red `⚠` near an edge known to have friction or SLA issues
- **NEW indicator**: Green `★` badge on nodes or edges introduced in a proposed operating model
- **Boundary box**: Dashed container labeled with org unit name to visually group related roles

---

## 7. Content Density Rules

| Mode | Role Nodes | Interaction Edges | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 5–8 | 6–15 | 10 edges max |
| Maximum | 12 | 20 | → split by boundary |

**Overflow Strategy**: If more than 10 roles, split by organizational unit. Each split-off slide shows one unit's interactions in detail. A master slide shows all units as high-level nodes only (Variant A hub-and-spoke style).

---

## 8. Anti-Patterns

1. **Showing every possible interaction**: Mapping all 30 edges in a 10-person team results in spaghetti — select only structurally significant interactions.
2. **Unlabeled edges**: Connections with no labels provide no information about the relationship — every edge must be described.
3. **Org chart disguise**: Drawing a strict top-down hierarchy without any interaction edges — an org chart is not an actor interaction diagram.
4. **Including system names as actors**: Mixing IT systems with human roles — system interactions belong in AA-03 Integration Map, not here.
5. **Symmetric diagrams for asymmetric relationships**: Using the same visual style for a service provider and a service consumer — authority and service direction must be visually distinct.

---

## 9. Industry Reference Patterns

**ArchiMate 3.1 Business Layer (The Open Group)**:
ArchiMate defines Business Actors as structural elements performing behavior, and Business Roles as named responsibilities. Interactions between them use Association, Triggering, Flow, and Composition relationships. The Business Collaboration element models two or more roles working together — directly applicable to this diagram type. ArchiMate recommends limiting one diagram to one collaboration scenario.

**TOGAF Operating Model Design (Phase B)**:
TOGAF connects organization design to capability delivery: each capability is "owned" by a role, and the interaction between capability owners forms the functional organization structure. The Operating Model Canvas (Dave Gray's patterns) identifies four interaction types: Decide, Inform, Execute, and Support — use these as edge label vocabulary.

**McKinsey Operating Model Interaction Map**:
McKinsey's team interaction mapping distinguishes three interaction modes: Coordination (peer-to-peer sharing), Cooperation (aligned but independent), and Collaboration (joint problem-solving). Each mode has different visual treatment: coordination = dashed, cooperation = solid thin, collaboration = thick double-headed. This three-mode framework prevents all edges from looking the same.

---

## 10. Production QA Checklist

- [ ] Every edge has a descriptive interaction label (≤4 words)
- [ ] External actors are visually distinct from internal roles (gray or dashed border)
- [ ] Arrow directions are correct and consistent (arrowhead at the receiver)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] No shape is present without at least one edge connecting to it
- [ ] Boundary boxes used when grouping roles within an org unit
- [ ] Pain-point markers present when diagram is used for gap/improvement context
- [ ] Role names match those used in BA-10 RACI Matrix for consistency
- [ ] Maximum 12 nodes per slide; split to additional slides for larger ecosystems
- [ ] Presenter can explain the most critical interaction in 30 seconds
