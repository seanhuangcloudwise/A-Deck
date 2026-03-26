# Data Architecture Diagram Catalog

Layer: TOGAF Layer 3 — Data Architecture  
Total Specs: 8  
Cloudwise Palette: #00CCD7 / #53E3EB / #2F2F2F / #A5A7AA / #44546A  
Audience: Data Architect, Data Engineer, CDO, Analyst, Business Stakeholder

---

## Diagram Index

| ID | File | Chinese Name | Primary Audience | Best For |
|----|------|-------------|-----------------|---------|
| DA-01 | [conceptual-data-model.md](conceptual-data-model.md) | 概念数据模型 | Business, CDO | Business entity definitions, strategic data planning |
| DA-02 | [logical-data-model.md](logical-data-model.md) | 逻辑数据模型 | Data Architect, Analyst | Normalized data structure, attribute definition |
| DA-03 | [data-flow-diagram.md](data-flow-diagram.md) | 数据流图 | Data Engineer, Architect | Data movement, transformation, pipeline design |
| DA-04 | [data-domain-map.md](data-domain-map.md) | 数据域地图 | CDO, Architect | Data domain ownership, domain boundary definition |
| DA-05 | [data-governance-framework.md](data-governance-framework.md) | 数据治理框架图 | CDO, Governance | Data ownership, policy, quality, and stewardship |
| DA-06 | [master-data-lifecycle.md](master-data-lifecycle.md) | 主数据生命周期图 | Data Architect, MDM | Master data management, creation-to-retirement |
| DA-07 | [data-lineage.md](data-lineage.md) | 数据血缘图 | Data Engineer, Auditor | Data traceability, transformation chain, compliance |
| DA-08 | [data-catalog-structure.md](data-catalog-structure.md) | 数据目录结构图 | Data Steward, Analyst | Data catalog organization, metadata classification |

---

## Selection Guide

```
Input intent → Recommended diagram

Business entity relationships, strategic data view   → DA-01 Conceptual Data Model
Entity attributes, normalized schema, ERD            → DA-02 Logical Data Model
Data pipeline, ETL, data movement between systems    → DA-03 Data Flow Diagram
Data domain ownership, boundary definition           → DA-04 Data Domain Map
Data governance policies, stewardship, quality       → DA-05 Data Governance Framework
MDM lifecycle, master data creation to archive       → DA-06 Master Data Lifecycle
Data traceability, lineage tracking, audit            → DA-07 Data Lineage
Data catalog taxonomy, metadata organization          → DA-08 Data Catalog Structure
```

---

## Shared Constraints (All DA Diagrams)

1. Data entities use rectangle shapes with entity name in bold header + attributes list below
2. Relationship connectors are labeled with cardinality (1:1, 1:N, N:M) or transformation type
3. Data domains use rounded rectangle containers — cyan (#00CCD7) for owned, gray (#A5A7AA) for shared
4. Source systems are always at left; target/consuming systems on right (left-to-right data flow)
5. PII/sensitive data fields are marked with a shield annotation annotation; no field values should appear in diagrams
