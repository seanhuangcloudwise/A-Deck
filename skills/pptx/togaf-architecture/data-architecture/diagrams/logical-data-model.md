# DA-02: Logical Data Model — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 | ER Modeling Standards (OMG) | Third Normal Form (Codd) | TOGAF Data Architecture_

---

## 1. Purpose & When to Use

**Definition**: A normalized, technology-independent representation of data entities, their attributes, data types, and relationships — serving as the definitive data contract between business requirements and physical database design.

**Use When**:
- Designing the data structure for a new domain or application
- Formalizing data contracts between teams in an API-first or microservice architecture
- Documenting the canonical data model for a shared entity (Master Data)
- Preparing input for database schema generation (Physical Data Model)
- Data quality program: defining data rules and constraints at the entity level

**Questions Answered**:
- What attributes does each entity have?
- What are the data types and constraints?
- How are relationships formalized (foreign keys, join conditions)?
- Which attributes are mandatory vs. optional?

**Primary Audience**: Data Architects, Database Administrators, Senior Developers, Data Engineers

---

## 2. Visual Layout Specification

**Structure**: Entity-Relationship diagram with attribute compartments — each entity shows name header + attribute list.

### Variant A: Classic ER Diagram
- Entity = three-compartment box: Name / Key Attributes / Non-Key Attributes
- Primary Key (PK) and Foreign Key (FK) labeled
- Crow's foot notation for cardinality
- Best for: DBA handoff, schema generation input

### Variant B: Domain-Focused Logical Model
- Key entities with full attribute lists
- Supporting/lookup entities shown as simple boxes (no attribute detail)
- Best for: Architecture review, design discussion

### Variant C: Master Data Entity Focus
- One central master entity (e.g., "Customer", "Product") with full attributes
- Child / related entities with abbreviated attributes
- Best for: MDM design, canonical model definition

**Grid Proportions**:
- Entity box width: 140pt
- Entity name header height: 28pt
- Attribute list row height: 18pt per attribute
- Max attributes per entity before overflow: 10

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Entity header | Entity name background | `#44546A` + White |
| PK attribute row | Primary key | `#00CCD7` + underlined |
| FK attribute row | Foreign key reference | `#53E3EB` |
| Mandatory attribute | NOT NULL field | `#2F2F2F` text, `*` prefix |
| Optional attribute | Nullable field | `#A5A7AA` text |
| Master Data entity | Shared, cross-domain entity | `#00CCD7` header with star badge |
| Reference/Lookup entity | Static classification | `#A5A7AA` header |
| Relationship line | Association | `#2F2F2F` |
| Identifying relationship | Mandatory child existence | `#2F2F2F` thick solid |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Entity Name | Header compartment | 11pt | Bold, White |
| Attribute Name | List row | 9pt | Regular, `#2F2F2F` |
| PK Indicator | "PK" prefix + underline | 9pt | Bold, `#00CCD7` |
| FK Indicator | "FK" prefix | 9pt | Regular, `#53E3EB` |
| Data Type | "(varchar)", "(int)" notation | 8pt | Monospace italic |
| Constraint | NOT NULL, UNIQUE markers | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Three-compartment rect | Entity with attributes |
| Simple header-only rect | Reference/simple entity |
| Crow's foot on line end | Many side of relationship |
| Single tick on line end | One side of relationship |
| Circle on line end | Optional (zero or one) |
| Double line | Mandatory (must exist) |
| Bold line | Identifying relationship |

---

## 6. Annotation Rules

- **Business rule notes**: Annotation box connected to attribute with constraint rule: "Must match ISO 3166 country code"
- **Data classification**: PII attributes marked with `🔒` prefix; sensitive with `⚠`
- **Value constraints**: Optional annotations: "Values: ACTIVE|INACTIVE|PENDING"
- **Cross-entity notes**: Business rule annotations connecting two entities when constraint spans entities
- **Version marker**: Entity version in header: "Customer v3.2"

---

## 7. Content Density Rules

| Mode | Entities | Attributes/Entity | Per Slide |
|---|---|---|---|
| Minimum | 2 | 3 | — |
| Optimal | 4–8 | 5–12 | 10 entities max |
| Maximum | 12 | 20 | → split by subject area |

**Overflow Strategy**: Split by subject area (e.g., "Customer & Contact" / "Order & Fulfillment"). Each subject area on dedicated slide. Show foreign key references to off-slide entities as stubs with abbreviated box.

---

## 8. Anti-Patterns

1. **Physical design leakage**: Including physical database artifacts (indexes, partitions, tablespace names) in the logical model — logical must remain implementation-independent.
2. **Denormalized attributes**: Storing redundant/calculated fields in a logical model — logical models should be 3NF normalized.
3. **Missing PK/FK notation**: Attributes without key designations make the model unusable for database design handoff.
4. **Non-mandatory mandatory fields**: Marking business-critical attributes as nullable when they must always have a value — critical data integrity issue.
5. **Over-large entities**: Entities with 30+ attributes — signals poor granularity. Sub-entity decomposition is likely needed.

---

## 9. Industry Reference Patterns

**E.F. Codd's Third Normal Form (3NF)**:
Codd's relational normalization rules: 1NF (no repeating groups), 2NF (full functional dependency on PK), 3NF (no transitive dependencies). Logical data models following 3NF eliminate data redundancy and update anomalies. For complex domains, Boyce-Codd Normal Form (BCNF) handles multi-valued dependencies. Annotation on the logical model: "Normalized to: 3NF".

**DAMA-DMBOK2 Logical Data Modeling Standards**:
DAMA recommends that logical models contain: entity names and definitions, attribute names and definitions, primary and foreign keys, cardinality and optionality of relationships, and attribute data types (logical, not physical: Text, Date, Integer). Version-controlled logical models should be stored in a data modeling tool and linked to the transformation roadmap.

**Inmon Corporate Information Factory (CIF)**:
William Inmon's Enterprise Data Warehouse approach uses a normalized Operational Data Store (ODS) driven from logical data models. The logical model defines the "single version of truth" for enterprise data. The CIF pattern: Normalized LDM → ODS → Data Warehouse Staging → Subject Area Marts.

---

## 10. Production QA Checklist

- [ ] All entities have a primary key identified
- [ ] All foreign keys are labeled and reference the correct parent entity
- [ ] Cardinality notation (crow's foot) is present on every relationship
- [ ] Mandatory (NOT NULL) vs. optional attributes are distinguished
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] PII and sensitive attributes are marked with appropriate icon
- [ ] No physical implementation artifacts (indexes, partitions) in the model
- [ ] Entity names match the Conceptual Data Model (DA-01) vocabulary
- [ ] Data type annotations present for each attribute
- [ ] Normalization level stated in subtitle or annotation box
