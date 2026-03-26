# DA-08: Data Catalog Structure — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 Chapter 12 Metadata Management | Gartner Data Catalog Magic Quadrant | DataHub / Collibra Reference_

---

## 1. Purpose & When to Use

**Definition**: A structural diagram showing how the organization's data catalog is organized — its taxonomy layers, metadata classification system, domain hierarchy, and how it connects to data governance and data quality processes.

**Use When**:
- Designing or communicating the organizational data catalog architecture
- Presenting the metadata management strategy to data governance board
- Planning data catalog implementation (tool selection, taxonomy design)
- Onboarding new data consumers to available data assets
- Demonstrating data discoverability maturity to external auditors

**Questions Answered**:
- How is the organization's data organized and classified in the catalog?
- What metadata is captured per data asset?
- How does the catalog connect to governance, quality, and lineage?
- Who is responsible for maintaining catalog entries?

**Primary Audience**: CDO, Data Stewards, Data Engineers, Analytics teams, Compliance teams

---

## 2. Visual Layout Specification

**Structure**: Hierarchical taxonomy tree or layered architecture showing catalog organization.

### Variant A: Taxonomy Hierarchy (Tree)
- Root: Organization data catalog
- Level 1: Data domains
- Level 2: Subject areas within domains
- Level 3: Schema / Dataset groups
- Level 4: Individual datasets/tables
- Best for: Onboarding data consumers, catalog design

### Variant B: Metadata Architecture (Layer Stack)
- Layer 1 (top): Business metadata (definitions, ownership, policies)
- Layer 2: Operational metadata (lineage, quality scores, freshness)
- Layer 3: Technical metadata (schema, pipeline, storage)
- Layer 4 (bottom): Physical data assets
- Best for: Metadata management strategy, catalog platform design

### Variant C: Catalog Integration Diagram
- Data Catalog at center
- Connected systems: Data Sources, Data Lineage Engine, Data Quality Engine, Governance Platform, Discovery/Search UI
- Best for: Catalog platform architecture, tool selection

**Grid Proportions**:
- Tree node (Variant A): 90pt × 36pt
- Layer stack row (Variant B): equal height bands, 80pt each
- Catalog hub (Variant C): 150pt × 70pt
- Connector stroke: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Root catalog node | Organization-wide catalog | `#44546A` + White |
| Domain node | Data domain level | `#00CCD7` + White |
| Subject area node | Sub-domain grouping | `#53E3EB` + `#2F2F2F` |
| Dataset node | Individual data asset | White + `#2F2F2F` border |
| Business metadata layer | Human-readable governance layer | `#44546A` |
| Operational metadata layer | Runtime data health info | `#00CCD7` |
| Technical metadata layer | Schema, storage, pipeline | `#53E3EB` |
| Physical data layer | Actual data stores | `#2F2F2F` |
| Compliance-tagged asset | GDPR/regulated data | Shield icon annotation |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Catalog Name | Root or central node | 12pt | Bold, White |
| Domain Label | Level 1 node | 11pt | Bold, White |
| Subject Area | Level 2 node | 9–10pt | SemiBold |
| Dataset Name | Leaf node | 9pt | Regular |
| Layer Label (Variant B) | Stack tier name | 10pt | SemiBold, White |
| Metadata Field | Example metadata items | 8pt | Regular, italic |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large rounded rect | Catalog root or domain block |
| Standard rounded rect | Subject area or dataset group |
| Small rect | Individual dataset asset |
| Cylinder | Physical data store |
| Document icon | Dataset / table asset (Variant A leaf) |
| Horizontal band rect | Metadata layer (Variant B) |
| Directed arrow | Catalog integration relationship |
| Dashed border | Planned / in-progress catalog scope |

---

## 6. Annotation Rules

- **Asset count badge**: Domain blocks show: "142 datasets" — total assets registered
- **Coverage percentage**: "Cataloged: 67% of known datasets"
- **Ownership label**: Each domain shows named Data Steward: "Steward: Data Team Alpha"
- **Quality score**: Dataset nodes optionally show DQ score: "DQ: 88%"
- **Last updated**: Catalog freshness: "Updated: 2026-03-25" on operational metadata layer

---

## 7. Content Density Rules

| Mode | Domains | Subject Areas | Assets shown | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 3 | sample | — |
| Optimal | 4–6 | 10–20 | representative samples | single slide |
| Maximum | 10 | 40 | — | → split by domain |

**Overflow Strategy**: Split by domain for detailed views. Master overview slide shows domain blocks with asset counts. Domain detail slides show full subject area and representative dataset list.

---

## 8. Anti-Patterns

1. **Catalog = tool**: Presenting the data catalog as the DataHub/Collibra tool interface screenshots — the catalog structure diagram is architecture, not a demo.
2. **Flat list**: All datasets at the same level with no domain hierarchy — no taxonomy means no governance structure.
3. **Steward-free catalog**: Subject areas or domains with no assigned data steward — every catalog area needs a responsible party to maintain quality and definitions.
4. **100% coverage claim**: Showing full catalog coverage without evidence — cataloging projects almost always have gaps; honest gap identification is more credible.
5. **Technical metadata only**: Catalog showing only schema and technical metadata without business definitions and ownership — this is a schema registry, not a data catalog.

---

## 9. Industry Reference Patterns

**Gartner Data Catalog Evaluation Framework**:
Gartner evaluates data catalogs on: metadata ingestion breadth, automated lineage, active metadata (real-time quality/usage), social collaboration (ratings, comments), policy enforcement integration. A production data catalog should cover all five dimensions. Use the Variant B layer stack to show which metadata layers a proposed catalog platform covers.

**DataHub Open-Source Metadata Platform (LinkedIn)**:
DataHub's data model: Urns (unique identifiers for entities), Aspects (facets of entity metadata: schema, ownership, lineage, usage, tags, glossary terms). Entities: Dataset, Dashboard, DataJob, DataFlow, User, Group, GlossaryTerm. The Variant C integration diagram maps DataHub's integration with upstream data sources (Spark, dbt, Airflow) and downstream consumers (BI tools, Looker, Superset).

**DAMA-DMBOK2 Metadata Types**:
DAMA classifies metadata into three categories: Business (definitions, ownership, policies, business rules), Technical (schema, storage, formats, lineage), and Operational (processing logs, quality scores, usage statistics, freshness). This three-category taxonomy is the direct source for Variant B's three metadata layers. Each layer has different governance ownership: Business = Data Steward; Technical = Data Engineer; Operational = Platform/SRE.

---

## 10. Production QA Checklist

- [ ] Catalog taxonomy has at least 3 levels (domain → subject area → dataset)
- [ ] Every domain has a named data steward
- [ ] Asset counts shown per domain
- [ ] Cataloged vs. uncataloged coverage percentage shown
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Business metadata (definitions, ownership) distinguished from technical metadata
- [ ] Data quality scores present on representative datasets
- [ ] Compliance-tagged assets (GDPR/regulated) are indicated
- [ ] Connection to data governance and lineage systems shown (Variant C)
- [ ] Presenter can explain the catalog taxonomy in 45 seconds
