# DA-03: Data Flow Diagram — Data Architecture Diagram Spec

_Ref: Gane & Sarson DFD (1979) | TOGAF Data Flow View | NIST SP 800-188 Data Flow Documentation_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing how data moves between systems, processes, and data stores — including transformation steps, inputs, outputs, and storage points.

**Use When**:
- Designing or documenting a data pipeline, ETL/ELT process, or data integration flow
- Performing data security review (illustrating data at rest vs. in motion)
- Mapping data lineage from source to consumer systems
- Analyzing data quality injection points
- Regulatory compliance (GDPR, data residency): showing where data flows across boundaries

**Questions Answered**:
- Where does data originate?
- Through what processes and transformations does it pass?
- Where is it stored (at rest)?
- Does any data cross regulatory/geographic boundaries?

**Primary Audience**: Data Engineers, Data Architects, Compliance/Security officers, Data Governance teams

---

## 2. Visual Layout Specification

**Structure**: Left-to-right flow — external entities as sources, processes in the middle, data stores as destinations.

### Variant A: Level 0 Context DFD
- Single central "System" process bubble
- External entities (data sources/consumers) around it
- Data flows in and out of the central process
- Best for: System boundary definition, compliance scope

### Variant B: Level 1 DFD (Process Decomposition)
- Central system decomposed into 3–7 sub-processes
- Data flows between processes and to/from data stores
- External entities at edges
- Best for: Pipeline design, ETL architecture

### Variant C: Streaming Data Flow
- Left: Source systems (streaming producers)
- Center: Streaming processing layer (Kafka/Spark)
- Right: Consuming systems and stores
- Best for: Real-time data architecture

**Grid Proportions**:
- External entity box: 80pt × 40pt
- Process circle/bubble: 80pt diameter
- Data store rectangle (open-ended): 140pt × 36pt
- Flow arrow stroke: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| External entity | Data source or consumer outside system | `#A5A7AA` + `#2F2F2F` text |
| Process | Data transformation | `#00CCD7` circle |
| Data store | Persisted data | `#44546A` open rect |
| PII data flow | Contains personal data | `#AA0000` dashed arrow |
| Regulated data flow | Crosses compliance boundary | `#AA4400` dashed arrow |
| Standard data flow | Normal data movement | `#2F2F2F` solid arrow |
| Streaming flow | Real-time continuous | `#00CCD7` thick arrow |
| Batch flow | Periodic bulk transfer | `#A5A7AA` dashed thick arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| External Entity Label | Source/consumer name | 10pt | SemiBold |
| Process Label | Transformation name | 10pt | SemiBold, White |
| Data Store Label | Store name | 9pt | Regular, White |
| Flow Label | Data description on arrow | 8pt | Regular |
| Boundary Label | Compliance/geo zone label | 9pt | Italic, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rectangle | External entity (source or consumer) |
| Circle / rounded oval | Process (transformation) |
| Open-ended rectangle (both ends open) | Data store (classic DFD notation) |
| Cylinder | Database / structured store |
| Solid arrow | Data flow (direction of data movement) |
| Dashed border zone | Compliance or geographic boundary |
| Shield icon | PII/regulated data annotation |

**Flow Label Convention**: Arrow labels describe what data flows: "Customer Orders (JSON)", "Invoice Records (CSV)", "Auth Tokens". Not the process name — the data name.

---

## 6. Annotation Rules

- **Data classification on flows**: "PII: Name, Email" annotated on personal data flows
- **Frequency/volume**: "Daily batch: ~500K records" on batch flows; "~2K events/sec" on streaming
- **Transformation type**: Label on process node: "Validate, Enrich", "Aggregate, Anonymize"
- **Boundary markers**: Dashed zone borders labeled "EU Data Zone", "Production Boundary", "PCI Scope"
- **Encryption indicator**: `🔒` on arrows where data is encrypted in transit

---

## 7. Content Density Rules

| Mode | Entities | Processes | Stores | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 1 | 1 | — |
| Optimal | 3–5 | 4–7 | 3–6 | — |
| Maximum | 8 | 10 | 8 | → split by domain |

**Overflow Strategy**: Split at the major processing boundary (ingestion layer / transformation layer / serving layer). Each layer on a dedicated slide. Add a master context DFD slide (Level 0) as overview.

---

## 8. Anti-Patterns

1. **Two-headed data flows**: Arrow pointing both ways without explanation — every data flow has direction; if truly bidirectional, show two separate arrows with different labels.
2. **Process as data store**: Showing a database inside a process circle — processes transform data, stores persist it. They are distinct elements.
3. **Missing flow labels**: Unlabeled arrows — data flow diagrams without flow labels provide no information about what data is moving.
4. **No external entity identification**: Starting the flow from a system without showing where the data originates — source must always be an external entity or existing data store.
5. **Compliance boundaries invisible**: Flows crossing regulatory or geographic boundaries without annotation — creates compliance review risk.

---

## 9. Industry Reference Patterns

**Gane & Sarson DFD Notation (1979)**:
The foundational DFD notation: rectangles for external entities, rounded rectangles for processes, open-ended double-lines for data stores, and arrows for data flows. This notation has been augmented for modern architectures: cylinders for databases, hexagons for streaming processors. Maintain the core distinction: entities, processes, stores, flows.

**NIST SP 800-188 Data Flow Documentation**:
NIST recommends that organizations document data flows for systems processing federal data. DFDs must show: data at rest (stores), data in motion (flows), processing locations, and system boundaries. The DFD boundary diagram (Level 0) is the recommended artifact for system authorization documentation.

**Modern Data Stack — ELT Pipeline Architecture**:
Modern data engineering uses an ELT (Extract, Load, Transform) pattern: Source systems extract raw data → Land in cloud data lake (raw zone) → Transform in warehouse → Serve to analytics/ML. The DFD for this pattern shows: source systems → ingestion pipeline → raw storage → transformation compute → curated/modeled storage → BI/ML consumers. Each stage transition is a data flow with defined schema and SLA.

---

## 10. Production QA Checklist

- [ ] All external data sources and consumers are identified at diagram edges
- [ ] Every arrow has a data description label
- [ ] Data flows are directed (single-headed arrows)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] PII and regulated data flows are annotated with classification
- [ ] Compliance/geographic boundaries shown as dashed zones
- [ ] Processes are labeled with transformation type (not just step numbers)
- [ ] Data stores are shown as persistent elements, not processes
- [ ] Flow frequency/volume annotated on batch and streaming flows
- [ ] No data flow crosses the diagram edge without being traced to an external entity
