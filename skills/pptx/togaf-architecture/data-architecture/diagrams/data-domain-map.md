# DA-04: Data Domain Map — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 Data Governance | TOGAF Information Map | Data Mesh (Zhamak Dehghani)_

---

## 1. Purpose & When to Use

**Definition**: A strategic map showing how organizational data is partitioned into distinct data domains — each with defined ownership, boundaries, and key entity types — forming the foundation for data governance and data mesh architecture.

**Use When**:
- Starting a data governance or data management program
- Designing a data mesh architecture (product teams own their data domains)
- Clarifying data domain ownership before a data platform migration
- Resolving data quality disputes by clarifying which team owns the "golden record"
- Planning master data management scope across domains

**Questions Answered**:
- What are the major data domains in the organization?
- Who owns each data domain?
- What are the key entities within each domain?
- How do domains relate to each other (shared entities, cross-domain flows)?

**Primary Audience**: CDO, Data Architects, Data Governance Board, Domain Data Owners, Platform Engineers

---

## 2. Visual Layout Specification

**Structure**: Block map with domain regions — similar to Capability Map but for data domains.

### Variant A: Domain Block Map (Capability Map style)
- One block per data domain, arranged in a grid
- Domain name + owning team + key entities listed inside
- Best for: Executive overview, governance kickoff

### Variant B: Domain Relationship Map
- Domains as large nodes with descriptive content
- Inter-domain edges showing shared entity or data flow relationships
- Best for: Cross-domain integration design, MDM scope planning

### Variant C: Data Mesh Ownership View
- Domain blocks color-coded by owning product team
- "Data Product" nodes inside each domain
- Cross-domain integrations as labeled edges
- Best for: Data mesh architecture, platform product design

**Grid Proportions**:
- Domain block: 180pt × 90pt minimum
- Domain header: 30pt height
- Entity pill list: inside block, 8pt font, stacked vertically
- Inter-domain edge stroke: 2pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Core data domain | Central, high-reuse data | `#00CCD7` header + light fill |
| Supporting data domain | Secondary, domain-specific | `#53E3EB` header |
| Reference data domain | Stable classification data | `#A5A7AA` header |
| External/acquired domain | Data from outside org | White header + dashed border |
| Shared entity indicator | Entity used across domains | `#44546A` pill inside block |
| Inter-domain flow edge | Data exchange relationship | `#00CCD7` directed arrow |
| Domain ownership label | Team/department responsible | Small `#44546A` pill annotation |
| Data Mesh data product | Discrete publishable data set | Mini block inside domain |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Domain Name | Block header | 12pt | Bold, White |
| Owning Team | Annotation below header | 9pt | Regular |
| Entity Pill | Key entity name | 8pt | Regular |
| Inter-domain Label | Edge description | 8pt | Regular, `#2F2F2F` |
| Data Product Label | Mini-product identifier | 8pt | SemiBold |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large rounded rect | Data domain block |
| Small pill inside block | Key entity in domain |
| Bold-border large rect | Core / master data domain |
| Dashed border block | External or unowned domain |
| Solid directed arrow | Data exchange / dependency |
| Dashed arrow | Derived data / secondary use |
| Small hexagon inside block | Data product node (Data Mesh) |

---

## 6. Annotation Rules

- **Entity count**: Domain header includes entity count: "12 entities"
- **Record volume**: Optional: "~50M master records" in domain block
- **Golden record owner**: Label dominant domain owning the "golden record" for shared entities: "MDM Owner: Customer Domain"
- **Quality score**: Optional RAG badge on domain indicating current data quality maturity
- **SLA annotation**: For data products (Variant C): "SLA: Fresh within 1hr"

---

## 7. Content Density Rules

| Mode | Domains | Entities per Domain | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2–3 | — |
| Optimal | 5–8 | 4–8 | 8 domains max |
| Maximum | 12 | 10 | → 2 slides |

**Overflow Strategy**: Split by organizational line (Customer-facing domains / Operations domains / Finance domains). Each grouping on a dedicated slide with inter-group flows summarized as a single edge.

---

## 8. Anti-Patterns

1. **Domain = Database**: Creating one domain per database schema — domains are business concepts, not technology artifacts. One database can serve one or more business domains.
2. **Overlapping ownership**: Multiple teams claiming ownership of the same data domain — exactly one owner per domain is the cardinal rule of data governance.
3. **No entity content**: Domain blocks with names only and no key entity list — provides no actionable governance information.
4. **Mixing data and application**: Putting application names inside data domain blocks — domains represent data responsibility, not application ownership.
5. **Ignoring shared entities**: Not identifying "Customer", "Product", "Organization" as shared entities present in multiple domains — shared entities are the root cause of data quality conflicts.

---

## 9. Industry Reference Patterns

**Data Mesh Architecture (Zhamak Dehghani, ThoughtWorks)**:
Data Mesh introduces "Data Domain Ownership" as a first principle: teams that produce data also own the data as a product. Each domain produces "Data Products" — discoverable, addressable, trustworthy, natively accessible data sets. The Data Domain Map in Data Mesh shows: domain boundaries, data product offerings per domain, and cross-domain consumption patterns.

**DAMA-DMBOK2 Data Domain Definition**:
DAMA defines a Data Domain as "A named sphere of knowledge, influence, or activity" — the data equivalent of a business capability domain. Key governance rule: each Subject Area (domain) has a named Data Steward and a Data Owner. The domain map formalizes these accountability boundaries before attempting cross-domain data integration.

**TOGAF Information Map (Phase C Data Architecture)**:
TOGAF's Information Map shows: subject areas (domains), their data entities, and information flows between subject areas. This is the TOGAF equivalent of the Data Domain Map. Phase C Data Architecture output includes: Data Entity/Data Component Catalog, Data Entity/Business Function Matrix (BA→DA traceability), and Conceptual Data Model — the Domain Map contextualizes all three.

---

## 10. Production QA Checklist

- [ ] Every domain has exactly one owning team or data owner
- [ ] Key entities (3–8 per domain) are listed inside each domain block
- [ ] Shared entities appearing in multiple domains are marked and MDM ownership noted
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Inter-domain data exchange relationships are shown with direction
- [ ] External/unowned domains are visually distinguished
- [ ] Domain names are business-concept names (not database or system names)
- [ ] Data product nodes present if using Data Mesh model
- [ ] Total domain count matches what is stated in the data governance charter
- [ ] Presenter can explain the top data ownership conflict point in 30 seconds
