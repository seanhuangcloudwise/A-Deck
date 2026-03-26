# BA-05: Business Service Decomposition — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B/C | SOA (Service-Oriented Architecture) Business Services | BIZBOK Service Catalog_

---

## 1. Purpose & When to Use

**Definition**: A hierarchical breakdown of business services from a service domain root down to individual service units, showing how higher-level business intents are decomposed into specific, deliverable service instances.

**Use When**:
- Designing a business service catalog for internal or external consumption
- Mapping IT service investments to business service structure
- Planning shared service center setup or consolidation
- Identifying redundant or missing services across domains
- Creating the service architecture as input to application design (AA layer)

**Questions Answered**:
- What services does the business offer to internal or external stakeholders?
- How do high-level service promises decompose into specific service units?
- Which service units are shared vs. domain-specific?
- Where are the service gaps or overlaps?

**Primary Audience**: Enterprise Architects, Product Managers, IT Service Managers, Business Architects

---

## 2. Visual Layout Specification

**Structure**: Top-down tree or tiered hierarchy — root service at top, decomposed into service groups, then service units.

### Variant A: Tree Decomposition (1 root → 3–5 service groups → 8–15 service units)
- Root node at top center
- Branching downward through groups to leaf service units
- Best for: Building a new service catalog from scratch

### Variant B: Domain Matrix (horizontal service domains × vertical service tiers)
- Columns = service domains (e.g., Customer Services, Financial Services)
- Rows = service tiers (Core Services, Enablement Services, Governance Services)
- Cells = individual service units
- Best for: Portfolio rationalization, shared service planning

### Variant C: Layered Stack (top-layer shared services, bottom-layer domain-specific)
- Top horizontal band: Enterprise-wide shared services
- Middle band: Domain services (grouped by business domain)
- Bottom band: Operational/execution services
- Best for: Shared service center design, cloud service catalog

**Grid Proportions**:
- Root node: 200pt × 50pt, centered at top
- Service group nodes: 130pt × 45pt, second row
- Service unit nodes: 100pt × 40pt, leaf level
- Vertical spacing: 60pt between levels
- Horizontal spacing: 16pt between siblings

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Root service / domain anchor | Top-level service promise | `#44546A` + White |
| Core service group | Primary service domain | `#00CCD7` + White |
| Supporting service group | Enabling capabilities | `#53E3EB` + `#2F2F2F` |
| Shared service (cross-domain) | Reused across domains | `#00CCD7` dashed border |
| Leaf service unit | Atomic deliverable | White + `#2F2F2F` border |
| Planned/future service | Not yet available | White + `#A5A7AA` dashed border |
| Deprecated service | Being retired | `#A5A7AA` with strikethrough text |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Root Node Label | Top domain name | 13pt | Bold, White |
| Service Group Label | Second tier | 11pt | SemiBold, White |
| Service Unit Label | Leaf level | 9–10pt | Regular |
| Service Tier Row Header | Variant B/C row label | 10pt | SemiBold, White |
| Status Annotation | Current/Planned/Deprecated | 7pt | Italic, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Wide rounded rect (≤4pt radius) | Service group / root node |
| Standard rect or narrow rounded rect | Leaf service unit |
| Dashed border rect | Shared or planned service |
| Strikethrough rect | Deprecated service |
| Vertical lines (tree connectors) | Decomposition relationship |
| Bracket connector | Aggregation (group contains units) |
| Horizontal divider line | Tier boundary in Variant B/C |

**Connector Rule**: Tree connectors show decomposition only (is-a-part-of). Never use decorative horizontal lines between services at the same level. If two services have a dependency, show it as a dashed arrow rather than a spatial relationship.

---

## 6. Annotation Rules

- **Consumer label**: Small gray pill below each service unit indicating which stakeholder consumes it (e.g., "Customer-facing", "Internal")
- **SLA badge**: For operational service catalogs, small chip with SLA tier (Platinum/Gold/Silver) in service unit corner
- **Ownership tag**: 2-letter team code in top-right corner of each service group
- **Count summary**: Total service count per group shown in domain header (e.g., "12 services")
- **Cross-domain shared marker**: Dashed border + `↔` symbol for services shared across domains

---

## 7. Content Density Rules

| Mode | Service Groups | Service Units Total | Per Slide |
|---|---|---|---|
| Minimum | 2 | 4 | — |
| Optimal | 3–5 | 10–20 | 20 max |
| Maximum | 7 | 35 | → 2 slides |

**Overflow Strategy**: Split at service domain boundary. Each domain's full decomposition on a separate slide. Include a summary slide showing all domains as top-level blocks with service counts.

---

## 8. Anti-Patterns

1. **Process steps as services**: Listing "Approve Invoice" as a service — services are deliverable outcomes, not workflow steps.
2. **Technology as services**: Naming services after systems ("SAP Service", "CRM Service") — services should be business-outcome named ("Order Management Service", "Customer Profile Service").
3. **Missing shared service** identification: Duplicating identical services across multiple domains without marking them as shared — shared services need explicit identification to enable reuse.
4. **Flat list**: Presenting all services at the same level without hierarchy — loses the decomposition story that is the entire purpose of this diagram.
5. **Dead ends**: Service units with no consumer identified — every service should have a defined consumer or it shouldn't exist.

---

## 9. Industry Reference Patterns

**TOGAF Service Catalog (Phase B/C cross-layer)**:
TOGAF recommends a service-oriented architecture at the business layer where business services are mapped to application services (AA) and technology services (TA). The Business Service is defined as "a service that fulfills a business need". The catalog should be organized by service domain, with each service having: name, description, consumer, provider, SLA, and supporting capability.

**ITIL v4 Service Value System**:
ITIL 4 organizes IT services into a Service Value Chain with six activities: Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support. For business services, adapt this to: Define, Design, Enable, Deliver, Govern, Improve. This lifecycle framing helps position each service unit within an operational maturity cycle.

**SOA Business Service Layer (OASIS SOA Reference Model)**:
The OASIS SOA standard defines Business Services as the contractual interface between capability owners and service consumers. Key attributes: visibility (discoverable), interaction (standard interface), and effect (outcome-producing). The three-tier decomposition — Service Portfolio → Service Category → Service Instance — maps directly to Variant A of this spec.

---

## 10. Production QA Checklist

- [ ] Every service has a business-outcome name (not a process step or technology name)
- [ ] Service hierarchy is ≥ 2 levels deep (root → group → unit minimum)
- [ ] All shared services are explicitly marked with dashed border and shared indicator
- [ ] Consumer or stakeholder identified for every service unit
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Deprecated services are visually distinguished (gray fill + strikethrough)
- [ ] Total service count is visible in each domain header
- [ ] No decorative lines between sibling service units — only structural connectors
- [ ] Service names are consistent with terms used in BA-01 Capability Map
- [ ] Presenter can explain the decomposition rationale in 2 sentences
