# AA-06: API Dependency Graph — Application Architecture Diagram Spec

_Ref: API Management Maturity (Gartner) | OpenAPI Specification (OAI) | Netflix API Gateway Patterns_

---

## 1. Purpose & When to Use

**Definition**: A directed graph showing API producers, API consumers, and the dependency relationships between them — exposing coupling, versioning risks, and potential cascading failures.

**Use When**:
- Analyzing the impact of an API change or deprecation
- Designing API governance strategy (versioning, breaking-change policy)
- Identifying APIs with too many consumers (high blast radius)
- Planning API-first architecture adoption
- Security review: tracing which services can reach sensitive APIs

**Questions Answered**:
- Which services consume which APIs?
- Which APIs have the highest number of consumers (high blast-radius risk)?
- Are there deprecated APIs still in use?
- Which API changes would trigger a cascade across multiple consumers?

**Primary Audience**: API Architects, Platform Engineers, Tech Leads, Security Architects

---

## 2. Visual Layout Specification

**Structure**: Directed bipartite or network graph — producer services on left/top, consumer services on right/bottom.

### Variant A: Producer-Consumer Bipartite
- Left column: API producer services
- Right column: API consumer services
- Edges: API name + version label
- Best for: API dependency audit, impact analysis

### Variant B: API Centricity (API as node)
- Center nodes: API endpoints (named resources)
- Surrounding nodes: Consuming services
- Edge from producer to API: "exposes"
- Edge from API to consumer: "consumed by"
- Best for: API governance, deprecation planning

### Variant C: Dependency Topology Graph
- Force-directed layout with API endpoints and services as nodes
- Edge thickness = call frequency / consumer count
- Color = API health status
- Best for: Real-time observability-informed architecture review

**Grid Proportions**:
- Service node: 100pt × 45pt
- API node (Variant B): 80pt × 36pt (smaller, secondary role)
- Edge stroke: 1.5pt base; thicker = more consumers
- Consumer count badge: 18pt circle on edge or node

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| API Producer | Service exposing API | `#44546A` + White |
| API Consumer | Service calling API | `#00CCD7` + White |
| Stable API | Version locked, no breaking change | `#53E3EB` edge |
| Deprecated API edge | Scheduled for removal | `#A5A7AA` dashed red-annotated |
| Breaking-change risk API | Unstable contract | Orange-bordered edge (or annotation `!`) |
| Internal API | Cross-team internal use | `#00CCD7` solid edge |
| Public/External API | Exposed outside org | `#44546A` thick border edge |
| API Gateway | Centralized control point | `#44546A` hexagon |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Service Name | Node label | 10pt | SemiBold, White |
| API Name | Edge or node label | 8pt | Regular |
| Version Tag | API version annotation | 7pt | Monospace, `#A5A7AA` |
| Consumer Count | Badge on high-traffic APIs | 9pt | Bold, White in circle |
| Deprecation Notice | Warning annotation | 8pt | Red, Bold |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect | API service (producer or consumer) |
| Hexagon | API Gateway |
| Small pill/rect | API endpoint node (Variant B) |
| Solid directed arrow | Active API dependency |
| Dashed arrow | Deprecated API still in use |
| Thick arrow | High-traffic / high-consumer API |
| Consumer count circle | Number of consumers badge on arrow |
| Red `!` annotation | Breaking-change risk |

---

## 6. Annotation Rules

- **Consumer count badge**: Circle on each API edge/node showing count: "×8 consumers"
- **Version label**: API version on every edge: "v2.3", "v1 (deprecated)"
- **Blast radius indicator**: For high-consumer APIs, annotation: "Blast radius: 12 services"
- **Deprecation timeline**: Deprecated API edges: "Retire: 2026-06-30"
- **Rate limit annotation**: Public/External APIs: "Rate limit: 1000 req/min"

---

## 7. Content Density Rules

| Mode | Services | API Dependencies | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 6–12 | 8–20 | 20 edges max |
| Maximum | 20 | 40 | → split by domain cluster |

**Overflow Strategy**: Split by business domain. Show one domain's full API dependency mesh per slide. Add summary slide showing cross-domain API gateways only.

---

## 8. Anti-Patterns

1. **Database-level dependencies**: Showing direct database access dependencies in an API dependency graph — APIs abstract over storage; direct DB calls indicate missing API layer violations.
2. **Unsigned versions**: API edges without version annotations — unversioned APIs are a governance anti-pattern in themselves; document "v1" even for implicit versions.
3. **Missing deprecated API tracking**: Deprecated APIs not shown — deprecated > removed gap is a production risk window that must be explicitly visible.
4. **All edges equal weight**: Not distinguishing high-traffic from low-traffic API calls — edge thickness or consumer count is critical for blast-radius assessment.
5. **Circular dependencies**: Service A calls Service B's API, which calls Service A's API — always flag and annotate as architecture violation.

---

## 9. Industry Reference Patterns

**Gartner API Management Maturity Model**:
Gartner defines 5 API maturity levels: Ad-hoc → Managed → Standardized → Productized → Platform. At Level 2 (Managed), organizations begin tracking API dependencies. At Level 3 (Standardized), formal API versioning and deprecation policies apply. This diagram is the artifact produced at Level 3 API governance maturity.

**Netflix API Gateway Evolution**:
Netflix's evolution from monolith to API graph: starting with direct service-to-service REST calls, then introducing the API Gateway (Zuul/Gateway) as a centralized dependency point, then evolving to a GraphQL federation model where each service exposes a schema that the Gateway federates. The API Dependency Graph captures the pre/post state of each evolutionary step.

**OpenAPI Specification (OAI) + Service Mesh Integration**:
Modern organizations pair the OpenAPI Specification registry (Swagger Hub, Apicurio) with service mesh observability (Istio, Linkerd) to produce real-time API dependency graphs. API calls traced through the service mesh populate the dependency graph automatically. For architecture presentations, normalize this live data into a static diagram showing top-20 dependency relationships.

---

## 10. Production QA Checklist

- [ ] All API edges have version annotations
- [ ] Deprecated APIs are flagged with retirement date
- [ ] Consumer count is shown on high-traffic APIs (≥ 5 consumers)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] API Gateway is shown if one exists in the architecture
- [ ] Circular dependencies are flagged with warning annotation
- [ ] Blast radius annotation on APIs with 5+ consumers
- [ ] Breaking-change risk APIs are highlighted with warning border
- [ ] No arrows without direction — all edges are directed
- [ ] Presenter can identify the top 3 API risks (high blast-radius, deprecated, breaking-change) in 30 seconds
