# AA-02: Application Component Diagram — Application Architecture Diagram Spec

_Ref: TOGAF C2 Component View | ArchiMate 3.1 Application Layer | C4 Model (Component Level)_

---

## 1. Purpose & When to Use

**Definition**: A structural diagram showing the internal components, modules, or layers of an application system — their boundaries, dependencies, and interfaces.

**Use When**:
- Designing the internal structure of a new application system
- Reviewing the modularity and separation of concerns in an existing system
- Planning refactoring: visualizing which components are tightly vs. loosely coupled
- Communicating technical design to non-developer stakeholders
- Providing architectural context for development teams

**Questions Answered**:
- What are the major components inside this application?
- How do components depend on each other?
- Which components expose external interfaces?
- What is the technical layering (presentation / business logic / data)?

**Primary Audience**: Solution Architects, Senior Developers, Tech Leads, CTO

---

## 2. Visual Layout Specification

**Structure**: Layered or network layout — components shown as labeled blocks with dependency arrows.

### Variant A: Layered Architecture (top-down tiers)
- Top: API Gateway / Presentation Layer
- Middle: Application Services / Business Logic Layer
- Bottom: Data Access / Infrastructure Layer
- Best for: Standard multi-tier application design

### Variant B: Domain-Group Layout
- Components grouped by domain context (bounded by dashed containers)
- Dependencies shown as arrows with interface labels
- Best for: Microservice-friendly decomposition, single application DDD

### Variant C: Module Dependency Graph
- All components as nodes in a force-directed or radial layout
- Edge thickness = coupling strength
- Best for: Refactoring analysis, coupling visualization

**Grid Proportions**:
- Layer label (left edge or row header): 80pt
- Component block: 110pt × 50pt minimum
- Domain container padding: 16pt internal
- Dependency arrow stroke: 1.5pt

---

## 3. Color Semantics

| Component Type | Meaning | Fill Color |
|---|---|---|
| API / Entry point | External access layer | `#44546A` + White |
| Core business logic | Domain service, use case | `#00CCD7` + White |
| Shared/utility module | Cross-cutting concerns | `#53E3EB` + `#2F2F2F` |
| Data layer / repository | Persistence components | `#2F2F2F` + White |
| External dependency | 3rd party lib or service | `#A5A7AA` + dashed border |
| Domain boundary container | Bounded context grouping | Transparent + dashed `#44546A` border |
| High-coupling indicator | Arrow with warning annotation | `#A5A7AA` thick arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Component Name | Block label | 10–11pt | SemiBold |
| Component Type | Layer tag below name | 8pt | Regular, italic |
| Domain Container | Boundary group label | 10pt | SemiBold, `#44546A` |
| Interface Label | Arrow annotation | 8pt | Regular, `#2F2F2F` |
| Layer Header | Tier label | 10pt | Bold, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Internal component / module |
| Dashed rounded rect | External dependency |
| Dashed container | Domain / layer boundary group |
| Standard rect | Infrastructure component |
| Solid arrow | Dependency / uses relationship |
| Dashed arrow | Optional / indirect dependency |
| Double-line border | Exposed interface / API |
| Small ball-and-socket | Interface notation (C4 style) |

---

## 6. Annotation Rules

- **Technology tag**: Small gray pill below component: "Spring Boot", "React", "PostgreSQL"
- **Interface label on arrows**: What the dependency uses: "REST API", "Event Bus", "Database Query"
- **Coupling score**: Optional: for refactoring diagrams, add coupling metric (e.g., "Afferent: 3") in corner
- **Owned vs. External**: Internal components have no border extra styling; external = dashed border
- **Version annotation**: For interface arrows in production context: "API v2.1"

---

## 7. Content Density Rules

| Mode | Components | Dependencies | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 8–15 | 10–20 | 15 components max |
| Maximum | 25 | 40 | → split by domain |

**Overflow Strategy**: Split by domain container. Each domain shows internal component detail on a dedicated slide. A summary slide shows all domain containers with public interfaces only.

---

## 8. Anti-Patterns

1. **God component**: One component with arrows to every other component — signals a monolith, not an architecture. Flag and suggest decomposition.
2. **Missing boundaries**: Components floating without layer or domain grouping — no spatial context means no architectural communication.
3. **Implementation detail overload**: Listing method names, database table names inside component boxes — component diagrams operate at module/service level, not code level.
4. **Circular dependencies**: A → B → A — always highlight and annotate as an architecture violation requiring resolution.
5. **Unnamed interfaces**: Dependency arrows with no labels — "uses what?" - every arrow must describe the interaction type.

---

## 9. Industry Reference Patterns

**C4 Model — Component Level (Simon Brown)**:
The C4 Model defines four levels of abstraction: System Context (L1), Container (L2), Component (L3), Code (L4). This diagram operates at L3. Each component in C4 is defined as a grouping of related code behind an interface, with a responsibility and a technology. C4's rule: one diagram = one container's internals. Link to the L2 Container Diagram for context.

**TOGAF Application Component View (Phase C)**:
TOGAF's Application Architecture includes a Component View (also called C2 view) that shows application components and their dependencies. TOGAF extends the component view with: interface definition, technology realization, and mapping to application functions. The component catalog in TOGAF's Architecture Repository corresponds to the component blocks in this diagram.

**ArchiMate 3.1 Application Layer**:
ArchiMate defines Application Components as structural elements implementing application behavior. The Application Interface element represents the exposed behavior. Relationships include: Serving (component provides interface), Realization (component implements application function), and Association (informal dependency). This vocabulary maps to the shape and connector vocabulary in this spec.

---

## 10. Production QA Checklist

- [ ] All components are grouped by layer or domain (no floating components)
- [ ] Every dependency arrow has an interface/relationship label
- [ ] Circular dependencies are flagged with warning annotation
- [ ] External dependencies are visually distinct (dashed border)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Technology tags present on all components
- [ ] No single component has more than 5 outgoing dependencies without refactoring note
- [ ] Domain containers use dashed borders (not solid — solid is for data-containing components)
- [ ] Component names are nouns representing modules, not verbs representing functions
- [ ] Presenter can explain the most critical dependency path in 45 seconds
