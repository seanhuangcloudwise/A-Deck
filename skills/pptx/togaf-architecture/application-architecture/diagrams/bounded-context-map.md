# AA-04: Bounded Context Map — Application Architecture Diagram Spec

_Ref: Domain-Driven Design (Eric Evans) | Team Topologies (Skelton & Pais) | TOGAF Partitioning_

---

## 1. Purpose & When to Use

**Definition**: A strategic diagram showing the boundaries between distinct domain models (bounded contexts), the relationships between them, and the team responsibilities — the foundation of Domain-Driven Design at macro scale.

**Use When**:
- Designing microservice decomposition boundaries from domain models
- Planning team autonomy boundaries using Team Topologies principles
- Resolving semantic conflicts between teams using the same terms differently
- Presenting domain strategy and ownership model to technology leadership
- Starting a DDD program and aligning teams on context boundaries

**Questions Answered**:
- What are the bounded contexts (autonomous domain models) in the system?
- How do bounded contexts integrate with each other (relationship patterns)?
- Which team owns which context?
- Where are context translation/mapping needs (shared kernel, anti-corruption layer)?

**Primary Audience**: Domain Architects, Senior Developers, Tech Leads, Engineering Managers

---

## 2. Visual Layout Specification

**Structure**: Network of bounded context regions with labeled relationship edges.

### Variant A: Context Map (Region Layout)
- Each bounded context = filled rounded rectangle with domain name
- Relationship edges show integration pattern type
- Team name shown as small annotation below context
- Best for: DDD strategic design, team boundary definition

### Variant B: Core/Supporting/Generic Classification
- Color-coded by context classification: Core Domain / Supporting Subdomain / Generic Subdomain
- Subdomains arranged spatially: core at center, supporting around it, generic at edges
- Best for: Investment prioritization, build vs. buy decisions

### Variant C: Team Ownership View
- Context blocks organized by team (each team group has a background container)
- Cross-team integrations shown as inter-container edges
- Best for: Team autonomy design, Conway's Law analysis

**Grid Proportions**:
- Context block: 140pt × 70pt standard
- Core domain context: 160pt × 80pt (larger to emphasize)
- Team container padding: 20pt
- Relationship edge stroke: 2pt

---

## 3. Color Semantics

| Context Type | Meaning | Fill Color |
|---|---|---|
| Core Domain | Differentiating, custom-built | `#00CCD7` |
| Supporting Subdomain | Customized but not differentiating | `#53E3EB` |
| Generic Subdomain | Commodity, buy/SaaS preferred | `#A5A7AA` |
| External System Context | Outside organizational boundary | White + dashed `#A5A7AA` border |
| Shared Kernel | Shared code across contexts | `#44546A` + double border |
| Relationship customer edge | Downstream context | `#00CCD7` arrow |
| Relationship supplier edge | Upstream context | `#2F2F2F` arrow |
| Anti-corruption layer | Translation boundary | `#44546A` small intervening box |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Context Name | Domain region label | 12pt | Bold, White |
| Context Type | Subdomain classification | 8pt | Italic, semi-transparent |
| Team Name | Owner annotation | 8pt | Regular, `#44546A` |
| Relationship Label | Edge pattern type | 8pt | Regular |
| Team Container | Team boundary header | 10pt | SemiBold, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Bounded context |
| Double-border rounded rect | Shared Kernel context |
| Dashed border rounded rect | External system / context |
| Dashed container | Team ownership boundary |
| Solid arrow | Downstream receives from upstream |
| Small intervening box | Anti-Corruption Layer |
| Bracket notation {} | Published Language interface |
| Annotation tag | Context Map relationship pattern label |

**Integration Pattern Labels** (required on edge):
- `U→D` = Upstream/Downstream
- `SK` = Shared Kernel
- `ACL` = Anti-Corruption Layer
- `OHS` = Open Host Service
- `CF` = Conformist
- `PL` = Published Language

---

## 6. Annotation Rules

- **Team assignment**: Small team name below each context block (8pt, `#44546A`)
- **Domain investment level**: For Variant B, add small $/$$ annotation in context corner
- **Context health**: Optional RAG indicator: Green = well-maintained model, Amber = model drift, Red = model conflict
- **Integration pattern legend**: Always include a legend table defining each relationship abbreviation
- **Conway's Law note**: For Variant C, annotation box: "Current team structure → expected architecture"

---

## 7. Content Density Rules

| Mode | Contexts | Relationships | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 5–10 | 6–15 | 12 contexts max |
| Maximum | 18 | 30 | → split by domain cluster |

**Overflow Strategy**: Split by domain cluster (Customer Domain / Product Domain / Operations Domain). Each cluster shows detail. A master context map shows all clusters as single blocks with inter-cluster relationships.

---

## 8. Anti-Patterns

1. **Naming contexts after technology**: "Microservice A", "Database Context" — contexts must be named after business domains: "Order Management", "Inventory".
2. **Missing relationship labels**: Context maps without integration pattern labels (SK/ACL/U-D) provide no design guidance.
3. **No team assignment**: Contexts without owners drift — every context must have a named team.
4. **Over-partitioning**: 30+ contexts for a mid-size system — each context needs a full team and domain model; too many contexts means too much coordination overhead.
5. **Ignoring Shared Kernels**: Letting teams independently redefine the same concept (e.g., "Customer" has 5 different definitions) — Shared Kernel or Published Language is needed.

---

## 9. Industry Reference Patterns

**Eric Evans DDD Context Mapping (2003, "Domain-Driven Design")**:
Evans defines the Strategic Design techniques: Bounded Context, Ubiquitous Language, and Context Map. The Context Map is not a diagram in Evans' original book but has become the standard visualization. The key principle: the Context Map must reflect the ACTUAL state of integration, not the desired state — it's a diagnostic before it's a design tool.

**Team Topologies (Skelton & Pais, 2019)**:
Team Topologies maps context ownership to four team types: Stream-aligned (owns a bounded context), Platform (provides shared context), Enabling (helps others adopt patterns), and Complicated Subsystem (owns complex generic subdomains). This maps to Variant C: stream-aligned teams own Core Domains; platform teams own Generic Subdomains.

**Sam Newman Microservice Decomposition Strategies**:
Newman's decomposition heuristic: start with business capabilities (from BA-01), then apply DDD to identify bounded contexts within each capability, then size each context for one team. The Context Map is the output of this process — not the starting point. Anti-pattern: decomposing by technical layer (front-end context / back-end context) instead of by domain.

---

## 10. Production QA Checklist

- [ ] Every context has a business-domain name (not technical name)
- [ ] Every context has an owning team identified
- [ ] All inter-context relationships are labeled with DDD pattern type
- [ ] Core Domains are visually distinct from Supporting/Generic Subdomains
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Anti-Corruption Layers are shown where upstream models are incompatible
- [ ] Shared Kernels have double-border and are explicitly labeled
- [ ] Integration pattern legend is present on every slide
- [ ] No context is isolated (every context has at least one relationship)
- [ ] Presenter can explain why the largest context is not split further (in 30 seconds)
