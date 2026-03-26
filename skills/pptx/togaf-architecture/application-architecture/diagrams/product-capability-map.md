# AA-11: Product Capability Map (Layered) — Application Architecture Diagram Spec

_Ref: TOGAF ADM Phase C (Application Architecture) | Product Line Engineering | China-style Layered Product Architecture Practice_

---

## 1. Purpose & When to Use

**Definition**: A layered product architecture map commonly used in domestic enterprise software design, showing product layers (channel, business domain, shared capability, platform, data/intelligence) and their capability modules, with ownership and reuse boundaries.

**Use When**:
- Designing or presenting a layered product architecture for B2B enterprise platforms
- Explaining product-line composition (core platform + domain solutions + channel apps)
- Aligning product capabilities with architecture boundaries before roadmap planning
- Identifying duplicated capabilities across product lines and deciding platform consolidation
- Building a bridge artifact from business capability (BA-01) to application capability realization

**Questions Answered**:
- What are the canonical product layers and what capabilities belong to each layer?
- Which capabilities are product-specific vs platform-shared?
- Where are the likely duplication or coupling risks across layers?
- Which layer should own new capability investment?

**Primary Audience**: Product Architect, Enterprise Architect, Product Manager, R&D Director

---

## 2. Visual Layout Specification

**Structure**: Horizontal layered bands from top (experience) to bottom (platform/foundation), with capability blocks in each band.

### Variant A: Five-Layer Standard (Recommended)
- Layer 1: Channel & Experience (Web/App/Partner/API Portal)
- Layer 2: Domain Product Capabilities (sales, service, operation, delivery)
- Layer 3: Shared Business Capabilities (workflow, rules, orchestration, notification)
- Layer 4: Platform Technical Capabilities (IAM, integration, observability, DevOps)
- Layer 5: Data & Intelligence Capabilities (data model, metrics, AI service)
- Best for: Most product architecture reviews and executive communication

### Variant B: Product Line Matrix Overlay
- Rows = Product lines (Standard / Advanced / Industry edition)
- Columns = Layered capabilities
- Filled cells = capability included by product line
- Best for: SKU/version planning and packaging discussion

### Variant C: Evolution Overlay
- Base = Five-layer map
- Add migration arrows and target-state tags (Now / T+1 / T+2)
- Best for: Transformation planning and phased platform consolidation

**Grid Proportions**:
- Layer title column: 130pt width
- Capability block minimum: 88pt × 34pt
- Band spacing: 8pt
- Legend + ownership strip at bottom: 56pt height

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Channel/Experience layer | User-facing interaction layer | `#53E3EB` |
| Domain product layer | Differentiating business product capabilities | `#00CCD7` |
| Shared business layer | Reusable shared business services | `#B9F2F6` |
| Platform technical layer | Non-functional and technical platform services | `#D9EEF2` |
| Data & intelligence layer | Data model, analytics, AI capabilities | `#44546A` with white text |
| External ecosystem capability | Partner/SaaS/outside boundary | White with `#A5A7AA` border |
| Deprecated capability | Planned decommission | `#A5A7AA` + strikethrough label |
| Strategic capability | Priority investment | Bold border `#2F2F2F` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular |
| Layer Label | Left band label | 10pt | Bold |
| Capability Name | Capability block text | 8.5–9.5pt | SemiBold |
| Owner/Tag | Team/code/reuse tag | 7pt | Regular |
| Legend Label | Bottom semantics | 8pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rect (small radius) | Capability module |
| Full-width band | Architecture layer boundary |
| Dashed group container | Product line or bounded context grouping |
| Solid arrow (down/up) | Dependency or invocation across layers |
| Dashed arrow | Optional/conditional dependency |
| Badge chip | Reuse/owner/SLA annotation |

**Connector Rule**:
- Only show cross-layer dependencies that are architecturally meaningful (for example, domain capability depending on shared workflow engine).
- Do not draw intra-layer decorative links.

---

## 6. Annotation Rules

- **Owner tag**: Each critical capability has owner code (e.g., `PDT`, `PLT`, `DATA`) in a 7pt chip.
- **Reuse tag**: Mark shared capability with `Shared` chip.
- **Volatility marker**: Use `V` badge for frequently changing modules.
- **Constraint note**: Add max 3 architectural constraints on right margin (e.g., "All channel requests must go through API gateway").
- **Coverage note**: Subtitle or footer should include "N capabilities / M shared / K strategic" summary.

---

## 7. Content Density Rules

| Mode | Layers | Capabilities | Per Slide |
|---|---|---|---|
| Minimum | 3 | 8–12 | — |
| Optimal | 5 | 15–28 | 28 max |
| Maximum | 6 | 36 | split by product line or domain |

**Overflow Strategy**:
- Split into two slides: Slide A = channel + domain + shared layers; Slide B = platform + data/intelligence + governance notes.
- Keep layer order and color semantics identical across split slides.

---

## 8. Anti-Patterns

1. **Process steps posing as capability**: "Approve Order" or "Submit Ticket" belongs to process, not capability.
2. **Technology product as capability name**: "Kubernetes", "Redis" should not appear as business/shared capability labels.
3. **No shared layer distinction**: Putting reusable workflow/rules in each domain block hides duplication risk.
4. **Too many crossing arrows**: More than ~12 visible cross-layer arrows usually means architecture decomposition is unclear.
5. **No owner mapping**: Capability map without ownership cannot support delivery governance.

---

## 9. Industry Reference Patterns

**Domestic Enterprise Product Layering Pattern**:
Many China enterprise software teams standardize product architecture into five layers: channel, domain product, shared business, technical platform, and data/intelligence. This pattern improves communication between product and R&D by making ownership and reuse explicit.

**TOGAF Capability Realization Traceability**:
TOGAF emphasizes traceability from business capabilities to application realization. A layered product capability map is a practical intermediate artifact between BA-01 capability map and detailed AA component/integration views.

**Product Platform Strategy (Core vs Domain Extension)**:
Product-line engineering practices separate platform core capabilities from domain extensions. Platform investment focuses on high-reuse capabilities, while domain teams iterate differentiating modules quickly. The layered map makes this boundary visible for budgeting and governance.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] At least one explicit shared capability layer is present
- [ ] Capability names are noun-based and architecture-level
- [ ] Cross-layer arrows are semantic and limited to meaningful dependencies
- [ ] Ownership tags are shown for strategic/critical capabilities
- [ ] Color semantics are consistent with legend and Cloudwise palette
- [ ] Strategic capabilities are visually distinguishable (bold border/tag)
- [ ] Deprecated capabilities (if any) are clearly marked
- [ ] Footer/subtitle includes capability summary counts
- [ ] Presenter can explain layer boundaries and top 3 consolidation opportunities in under 60 seconds
