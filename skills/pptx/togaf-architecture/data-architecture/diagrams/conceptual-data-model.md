# DA-01: Conceptual Data Model — Data Architecture Diagram Spec

_Ref: TOGAF ADM Phase C (Data Architecture) | OMG Conceptual Modeling | DAMA-DMBOK2 Chapter 5_

---

## 1. Purpose & When to Use

**Definition**: A high-level model showing the principal business entities and their key relationships — using business language, independent of any database or technology choices.

**Use When**:
- Establishing shared data vocabulary between business and IT at a program start
- Communicating data strategy to non-technical executives or board
- Scoping the data domains in a transformation program
- Serving as the starting input for Logical Data Model (DA-02) design
- Data governance: defining entity ownership and data domain boundaries

**Questions Answered**:
- What are the key business entities the organization manages?
- How do these entities relate to each other?
- Which entities are the most critical to the organization's operations?
- How do business entities map to organizational ownership?

**Primary Audience**: CDO, Executive sponsors, Data Architects, Business Analysts, Data Governance teams

---

## 2. Visual Layout Specification

**Structure**: Entity-relationship diagram using business language — no attributes, no database artifacts.

### Variant A: Entity Relationship Overview (5–12 entities)
- Entity boxes arranged spatially by organizational affinity
- Relationship lines with cardinality labels
- Best for: Executive communication, program kickoff

### Variant B: Domain-Clustered Model
- Entities grouped into domain clusters (dashed containers)
- Cross-cluster relationships shown as inter-container edges
- Best for: Data governance, domain ownership definition

### Variant C: Entity Importance Map
- Entities sized or visually weighted by criticality
- Central entities (like "Customer", "Product") shown larger
- Peripheral entities smaller
- Best for: Data strategy prioritization

**Grid Proportions**:
- Entity box: 100pt × 50pt
- Relationship line: 1.5pt stroke
- Domain container: auto-sized with 16pt padding
- Cardinality label: 9pt near edge endpoints

---

## 3. Color Semantics

| Entity Type | Meaning | Fill Color |
|---|---|---|
| Core business entity | Central, high-reuse entity | `#00CCD7` + White |
| Domain-specific entity | Contextual, domain-owned | `#53E3EB` + `#2F2F2F` |
| Reference/lookup entity | Stable classification entity | `#A5A7AA` + `#2F2F2F` |
| External entity | Origin outside organization | White + dashed `#A5A7AA` border |
| Domain container | Entity ownership boundary | Transparent + dashed `#44546A` |
| Relationship line | Association between entities | `#2F2F2F` solid 1.5pt |
| Composition relationship | Strong ownership | `#2F2F2F` thick 2pt |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Entity Name | Box label | 11–12pt | Bold, White |
| Domain Container | Ownership group | 10pt | SemiBold, `#44546A` |
| Cardinality Label | 1:N, N:M notation | 9pt | Regular, `#2F2F2F` |
| Relationship Label | Verb phrase on edge | 9pt | Italic, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (≤4pt) | Business entity |
| Dashed rounded rect | External entity |
| Dashed container | Data domain grouping |
| Solid line | Association relationship |
| Diamond on line | Composition (strong ownership) |
| "1" and "N" markers | One-to-many cardinality |
| Crow's foot notation | Optional: ER cardinality standard |

**Connector Labeling**: Every relationship line should carry a verb phrase label: "places" (Customer-places-Order), "contains" (Order-contains-LineItem). This makes the model readable as conceptual statements.

---

## 6. Annotation Rules

- **Entity description**: Optionally 1-line definition inside or below entity box (8pt italic)
- **Cardinality**: Required on all relationship endpoints — minimum "1", "N", "0..1"
- **Domain ownership tag**: Small pill under entity with owning team/domain name
- **PII indicator**: Shield icon on entities containing personal data (for governance context)
- **Record volume**: Optional annotation: "~50M records" for key high-volume entities

---

## 7. Content Density Rules

| Mode | Entities | Relationships | Per Slide |
|---|---|---|---|
| Minimum | 4 | 3 | — |
| Optimal | 7–15 | 8–20 | 15 entities max |
| Maximum | 25 | 40 | → split by domain |

**Overflow Strategy**: Split by domain cluster. Each domain's entities and their internal + border relationships on one slide. A master overview slide shows all domains as single boxes with cross-domain relationship counts.

---

## 8. Anti-Patterns

1. **Attribute inclusion**: Adding data attributes (fields, columns) to a conceptual model — conceptual = entities and relationships only, no attributes. Those belong in the Logical Data Model (DA-02).
2. **Technical entity names**: "Users_T", "order_rec" — conceptual entities must use business names: "Customer", "Sales Order".
3. **Missing cardinality**: Relationship lines without cardinality notation — impossible to validate data integrity requirements without this.
4. **Flat entity list**: All entities at same level with no domain grouping — loses the organizational affinity needed for governance.
5. **Circular relationships**: Entity A → B → C → A without explanation — conceptual circular relationships always need a business rationale note.

---

## 9. Industry Reference Patterns

**DAMA-DMBOK2 Conceptual Data Modeling**:
DAMA defines three levels of data modeling: Conceptual (business entities and relationships), Logical (normalized attributes and types), Physical (database implementation). Conceptual models must be understandable by business stakeholders — no SQL types, no primary keys, no foreign key notation. Standard practice: hold a joint modeling session with business and IT to validate entity names against business vocabulary.

**TOGAF Data Architecture — Conceptual Data Model Artifact**:
TOGAF requires a Conceptual Data Model as a baseline artifact in Phase C (Data Architecture). It identifies: entities and their business definitions, high-level relationships, and data classification (master data vs. transactional data vs. reference data). The conceptual model feeds the Information Map in the Architecture Repository.

**Zachman Framework — Row 2 (Business Owner Perspective)**:
In the Zachman Framework, Row 2 (Business Owner) describes the conceptual data model in the "Data" column: "Semantic Model" of business entities and key relationships. This is the authoritative business representation of organizational data, owned by the business owner, not IT.

---

## 10. Production QA Checklist

- [ ] No attributes, database columns, or technology artifacts present
- [ ] All entity names use business language (not technical names)
- [ ] All relationships have cardinality notation (minimum 1/N on both ends)
- [ ] All relationships have a verb phrase label
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Entities containing PII are marked with shield icon
- [ ] Domain ownership containers are present for entities with clear organizational owners
- [ ] Core/central entities (Customer, Product, etc.) are visually prominent
- [ ] Total entity count is ≤ 15 per slide
- [ ] Presenter can read two entities + their relationship as a business sentence in 10 seconds
