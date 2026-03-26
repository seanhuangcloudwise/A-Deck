# AA-08: Microservice Decomposition — Application Architecture Diagram Spec

_Ref: Sam Newman "Building Microservices" | Chris Richardson Microservices.io | CNCF Microservice Architecture_

---

## 1. Purpose & When to Use

**Definition**: A decomposition diagram showing how a system is partitioned into autonomous microservices — grouped by domain, showing service boundaries, size, ownership, and inter-service communication patterns.

**Use When**:
- Designing the initial microservice decomposition from a monolith or business capability model
- Reviewing service granularity and boundary correctness
- Communicating microservice architecture to product or business teams
- Planning migration from monolith to microservices (Strangler Fig pattern)
- Evaluating service mesh adoption and team topology alignment

**Questions Answered**:
- How many microservices exist and how are they grouped by domain?
- Is each service appropriately sized (not too large, not too small)?
- Does service boundary align with team boundary (Conway's Law)?
- What are the inter-service communication patterns?

**Primary Audience**: Platform Architects, Engineering Managers, Senior Developers, Tech Leads

---

## 2. Visual Layout Specification

**Structure**: Domain-grouped block layout — services organized in domain clusters.

### Variant A: Domain Cluster View
- Services grouped in domain containers (rounded dashed containers)
- Domain label at top of container
- Inter-domain arrows showing key interactions
- Best for: High-level architecture overview, team planning

### Variant B: Capability Traceability View
- Left side: Business capability column (from BA-01)
- Right side: Corresponding microservice(s) per capability
- Mapping lines showing capability-to-service traceability
- Best for: Business-IT alignment, capability coverage audit

### Variant C: Strangler Fig Migration View
- Core monolith block at center (gray, labeled "Legacy Monolith")
- Extracted microservices shown around monolith
- % extracted or completion status per service
- Best for: Migration planning, transformation progress reporting

**Grid Proportions**:
- Service block: 100pt × 46pt
- Domain container: auto-size to contents + 20pt padding
- Inter-domain arrow stroke: 1.5pt
- Capability column (Variant B): 160pt wide

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Core domain services | Business-differentiating services | `#00CCD7` + White |
| Supporting services | Non-differentiating domain services | `#53E3EB` + `#2F2F2F` |
| Generic/shared services | Auth, notification, config | `#A5A7AA` |
| Legacy monolith (Variant C) | Being decomposed | `#A5A7AA` + dashed border thick |
| Domain container | Service grouping boundary | Transparent + dashed `#44546A` border |
| Team label | Owner team | `#44546A` pill annotation |
| Extracted service (Variant C) | Successfully migrated | `#00CCD7` |
| In-progress extraction | Mid-migration service | `#53E3EB` + progress badge |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Service Name | Block label | 10pt | SemiBold, White |
| Domain Container | Group header | 11pt | Bold, `#44546A` |
| Team Name | Owner annotation | 8pt | Regular, `#44546A` pill |
| Technology Tag | Runtime/language | 7pt | Italic, `#A5A7AA` |
| Migration Status | % extracted (Variant C) | 8pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Individual microservice |
| Dashed container (rounded) | Domain grouping |
| Gray thick-dashed rect | Legacy monolith (Variant C) |
| Dashed small pill | Shared library / sidecar |
| Solid arrow | Synchronous service call |
| Dashed arrow | Asynchronous event |
| Bold left border on container | Team boundary |
| Progress bar badge | Migration completion (Variant C) |

---

## 6. Annotation Rules

- **Service size indicator**: Annotate number of APIs or logical lines (rough) to signal bloat: "> 5 APIs" or "Complex — split candidate"
- **Team ownership**: Small colored pill below service with team name
- **Communication pattern**: Inter-domain arrows labeled "REST", "gRPC", "Event"
- **Deployment independence badge**: Services that can be deployed independently get a release icon `▶`
- **Database ownership**: Small DB cylinder icon labeled with DB name under each service owning its own data store

---

## 7. Content Density Rules

| Mode | Services | Domains | Per Slide |
|---|---|---|---|
| Minimum | 3 | 1 | — |
| Optimal | 8–20 | 3–5 | 25 services max |
| Maximum | 40 | 8 | → split by domain cluster |

**Overflow Strategy**: Split by domain cluster. Each cluster full detail on its own slide. Master overview slide shows all clusters as domain blocks with total service counts.

---

## 8. Anti-Patterns

1. **Nano-services**: Services so small they have no independent deployment value (1 endpoint, 50 lines) — services should represent a meaningful domain capability.
2. **Technical decomposition**: Services named by technology ("database-service", "cache-service") instead of domain ("inventory-service", "pricing-service").
3. **Shared database**: Multiple services sharing one database — directly violates service autonomy. Annotate any such violations as technical debt.
4. **Missing team boundaries**: Services without ownership assignments are unmanageable — every service needs a responsible team.
5. **Forgetting the API gateway**: Not showing the entry point (API Gateway / BFF) means the consumer-facing access layer is invisible.

---

## 9. Industry Reference Patterns

**Sam Newman's Microservice Decomposition Strategy (2nd Ed, 2022)**:
Newman's preferred decomposition strategies: Decompose by Business Capability (align to BA-01), Decompose by Subdomain (DDD), Strangler Fig Pattern (incrementally extract from monolith), Branch by Abstraction (feature-toggle-based extraction). The key test for correct granularity: "Can one small team own this service end-to-end in a two-week sprint cycle?"

**Chris Richardson's Microservices.io Pattern Language**:
Richardson defines a microservice as a service with its own database and owned by one team. Key patterns relevant to this diagram: Service per team, Database per service, API Gateway, Backend for Frontend (BFF), and Saga (for distributed transactions). These patterns should be annotated on the diagram when applicable.

**CNCF Microservice Trail Map**:
The CNCF's approach maps microservice capabilities to cloud-native tools: containerization → CI/CD → orchestration → observability → service mesh → distributed tracing. The architecture diagram should show which services have reached which CNCF maturity tier, using a maturity annotation system.

---

## 10. Production QA Checklist

- [ ] Every service has a domain-based name (not technical name)
- [ ] Services are grouped by domain in labeled containers
- [ ] Every service has an owning team annotation
- [ ] Shared databases (anti-pattern) are flagged if present
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] API Gateway / BFF entry point is shown
- [ ] Inter-domain communication arrows have pattern labels (REST/gRPC/Event)
- [ ] For Variant C (migration): migration % progress shown per service
- [ ] Service count per domain shown in domain container header
- [ ] Presenter can explain the decomposition rationale (business domain vs. technical) in 45 seconds
