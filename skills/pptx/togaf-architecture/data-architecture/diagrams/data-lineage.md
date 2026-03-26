# DA-07: Data Lineage — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 | Apache Atlas Lineage Model | OpenLineage Specification | GDPR Article 30_

---

## 1. Purpose & When to Use

**Definition**: A directed graph tracing the ancestry and transformation history of data from its originating sources through all transformations to its consuming targets — enabling traceability, impact analysis, and compliance auditing.

**Use When**:
- Performing impact analysis before changing a data source or transformation
- Auditing data for regulatory compliance (GDPR, SOX, BCBS 239)
- Diagnosing data quality issues by tracing where incorrect values were introduced
- Documenting data provenance for AI/ML model governance
- Building a data catalog with lineage metadata

**Questions Answered**:
- Where did this data field originate?
- Which transformations affected this data?
- Which downstream reports/models consume this data?
- If I change source X, what downstream systems break?

**Primary Audience**: Data Engineers, Data Architects, Compliance/Audit teams, ML Engineers

---

## 2. Visual Layout Specification

**Structure**: Left-to-right directed acyclic graph (DAG) — sources on left, transformations in middle, consumers on right.

### Variant A: Field-level Lineage (Detailed)
- Source fields → transformation steps → target fields
- Each node represents a data attribute/column
- Transformation bubbles in between show the logic
- Best for: Data quality debugging, field impact analysis

### Variant B: Entity-level Lineage (Standard)
- Source entities/tables → pipeline jobs/transforms → target entities/reports
- Nodes are tables or datasets, not individual fields
- Best for: Architecture review, compliance documentation

### Variant C: System-level Lineage (Summary)
- Source systems → data platform/pipelines → consuming systems/reports
- Course-grained overview for executive communication
- Best for: Strategic data flow overview, CDO presentation

**Grid Proportions**:
- Source node: 100pt × 40pt
- Transform node: 80pt × 40pt (intermediate)
- Target node: 100pt × 40pt
- Horizontal flow spacing: 100pt between tiers
- Node vertical spacing: 12pt minimum

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Source system / table | Data origin | `#44546A` + White |
| Transformation step | Data processing logic | `#00CCD7` (rounded, center) |
| Target / output | Final destination | `#53E3EB` + `#2F2F2F` |
| Report / BI dashboard | End consumer | `#2F2F2F` + White |
| PII-containing node | Sensitive data path | Bold orange border |
| Lineage edge (standard) | Data flow direction | `#00CCD7` solid arrow |
| Transformation edge | With transform context | `#44546A` labeled arrow |
| Anomaly-flagged node | Known quality issue | Red `⚠` badge |
| Critical path | High-impact lineage | Bold `#00CCD7` 2.5pt arrows |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Source/Target Name | Node label | 9–10pt | SemiBold, White |
| Transform Logic | Transform node description | 8pt | Regular |
| Field Name | Variant A attribute label | 8pt | Monospace |
| Lineage Tier Header | Source / Transform / Target | 10pt | Bold, `#44546A` |
| Quality Flag | Anomaly annotation | 8pt | Red Bold |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rectangle | Source or target data entity |
| Rounded rect | Transformation / processing step |
| Cylinder | Database table or data store |
| Diamond | Branch / conditional transformation |
| Document icon | Report or BI dashboard |
| Solid arrow | Data flow with lineage trace |
| Dashed arrow | Derived / indirect lineage |
| Bold arrow | Critical lineage path |
| Red badge | Data quality anomaly at node |

---

## 6. Annotation Rules

- **Transformation rule**: Label on transform node with logic description: "Join on CustomerID", "Aggregate by Month"
- **Field mapping**: For Variant A: small arrow annotation: "source.customer_id → target.cust_id"
- **PII indicator**: Nodes containing PII: orange border + `🔒` annotation
- **Impact count**: Source nodes annotated with downstream count: "Impacts: 8 downstream systems"
- **Data quality score**: Node badge showing quality: "DQ: 94%" or "⚠ 3% nulls"

---

## 7. Content Density Rules

| Mode | Nodes | Edges | Tiers | Per Slide |
|---|---|---|---|---|
| Minimum | 3 | 2 | 2 | — |
| Optimal | 8–15 | 10–20 | 3–4 | 20 nodes max |
| Maximum | 30 | 50 | 5 | → split by subject area |

**Overflow Strategy**: Split by subject area or lineage path. Each critical lineage path gets its own slide. A master summary slide shows the full lineage graph at system level (Variant C).

---

## 8. Anti-Patterns

1. **One-way completeness**: Showing only forward lineage (source → target) but not backward lineage (target → what changed it) — full lineage needs both directions.
2. **No transformation content**: Lineage graphs where transformation nodes say "Transform" with no details — transformation steps must describe what logic they apply.
3. **Field-level on executive slide**: Showing column-level lineage for a CDO presentation — executive audiences need system-level Variant C, not field-level detail.
4. **Missing PII annotation**: Data lineage graphs for systems processing personal data without PII path highlighting are compliance risks.
5. **Cycles in DAG**: If the lineage graph has cycles (A→B→A), this indicates a circular dependency that creates undefined data freshness — always flag and annotate.

---

## 9. Industry Reference Patterns

**Apache Atlas Lineage Model**:
Apache Atlas captures lineage metadata using a property graph: entities (datasets, processes, columns) and relationships (lineage edges). Atlas supports both column-level and entity-level lineage. The Atlas UI renders lineage as a DAG — exactly the structure of this diagram. Key Atlas concept: a "Process" entity connects input datasets to output datasets through a job execution.

**OpenLineage Specification (Linux Foundation)**:
OpenLineage is a standard API for capturing lineage events from data pipelines (Spark, dbt, Airflow, Flink). It defines: Run, Job, Dataset, DatasetFacet (schema, quality, usage). For architecture diagrams, the Job node in OpenLineage maps to the Transformation step, and the DatasetFacet maps to field-level annotations.

**BCBS 239 Risk Data Aggregation Standard (Basel Committee)**:
BCBS 239 requires financial institutions to have comprehensive data lineage for risk data. Key requirements: accuracy of data origin, completeness of transformation chain, and ability to trace any reported risk metric back to transactional source data. Data lineage diagrams are the primary evidence artifact for BCBS 239 compliance; they must show end-to-end field-level traceability for material risk metrics.

---

## 10. Production QA Checklist

- [ ] All lineage arrows show direction (source → target)
- [ ] Transformation nodes describe their logic (not just "Transform")
- [ ] PII-containing data paths are annotated with sensitivity indicator
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Source systems match those documented in AA-03 Integration Map
- [ ] Impact count shown on high-impact source nodes
- [ ] Data quality anomalies flagged on nodes with known issues
- [ ] No cycles in the lineage graph (acyclic verification)
- [ ] Abstraction level is consistent throughout diagram (field/entity/system)
- [ ] Presenter can trace one field from origin to final report in 60 seconds
