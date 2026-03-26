# DA-06: Master Data Lifecycle — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 Chapter 9 Master Data Management | MDM Institute | Gartner MDM Reference Architecture_

---

## 1. Purpose & When to Use

**Definition**: A lifecycle flow diagram showing how master data entities (Customer, Product, Organization, etc.) are created, validated, distributed, maintained, and eventually archived or retired across the organization.

**Use When**:
- Designing or reviewing a Master Data Management (MDM) program
- Documenting the golden record creation process
- Identifying where data quality issues enter the master entity lifecycle
- Communicating MDM design to business stakeholders before implementation
- Auditing data for regulatory compliance (GDPR right-to-erasure, data retention)

**Questions Answered**:
- How is a master entity created and validated?
- Which systems are the authoritative source at each lifecycle stage?
- Where does data quality degradation occur?
- What happens when a master entity becomes obsolete (archive vs. delete)?

**Primary Audience**: Data Architects, MDM Program Managers, Data Quality teams, Compliance officers

---

## 2. Visual Layout Specification

**Structure**: Left-to-right stage flow from creation to archive — similar to value stream but for data lifecycle.

### Variant A: Linear Master Data Flow
- Stages: Request → Validate → Create Golden Record → Distribute → Maintain → Archive
- Per stage: source system, data quality gate, owning team
- Best for: MDM design overview

### Variant B: Hub-and-Spoke MDM Architecture
- Central "Golden Record Store" hub
- Surrounding systems: source systems (provide data), consuming systems (receive data)
- Data flows showing how data enters and exits the hub
- Best for: MDM system architecture design

### Variant C: Survivorship Process Flow
- Multiple source records at top, all flowing into a Survivorship Engine
- Survivorship Engine applies matching, merging, scoring rules
- Golden record produced at bottom
- Best for: MDM survivorship design, duplicate resolution

**Grid Proportions**:
- Lifecycle stage block: 100pt × 60pt
- Stage chevron/connector: 30pt
- Source/consumer system node: 80pt × 40pt
- Flow arrow stroke: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Creation stage | Master entity origination | `#44546A` + White |
| Validation stage | Quality gate | `#53E3EB` + `#2F2F2F` |
| Golden record stage | Authoritative source of truth | `#00CCD7` + White (bold border) |
| Distribution stage | Publishing to consumers | `#00CCD7` |
| Maintenance stage | Ongoing stewardship | `#53E3EB` |
| Archive / Retire stage | End of life | `#A5A7AA` |
| Source system | Data contributor | `#2F2F2F` + White |
| Consuming system | Data consumer | `#53E3EB` |
| Data quality gate | Validation checkpoint | `#44546A` diamond/checkpoint |
| Error path | Rejected records | Red dashed arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Stage Name | Lifecycle phase label | 11pt | SemiBold, White |
| Stage Description | What happens here | 9pt | Regular |
| System Label | Source/consumer name | 9pt | Regular, `#2F2F2F` |
| Quality Gate Label | Validation checkpoint | 9pt | Regular, `#44546A` |
| Error Path Label | Rejection/rework indicator | 8pt | Italic, Red |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Chevron block | Lifecycle stage |
| Diamond | Data quality gate / decision point |
| Cylinder | Data store / golden record repository |
| Rounded rect | Source or consuming system |
| Bold-border cylinder | Golden record store |
| Solid arrow | Normal data flow direction |
| Dashed red arrow | Data rejection / error path |
| Return arrow (above stage) | Rework / correction loop |
| Clock icon | Scheduled batch vs. real-time |

---

## 6. Annotation Rules

- **Data quality rules**: Per-stage annotation box listing key validation rules: "Must have: Name, DOB, NationalID"
- **SLA per stage**: Processing time SLA: "Validation: ≤ 4hrs"
- **Source system labels**: Each source system at creation stage labeled with system name
- **Survivorship score**: For Variant C: confidence score on golden record: "Match score: 0.94"
- **GDPR/retention note**: Archive stage annotation: "Retention: 7 years | Right-to-erasure: supported"

---

## 7. Content Density Rules

| Mode | Lifecycle Stages | Source/Consumer Systems | Per Slide |
|---|---|---|---|
| Minimum | 4 | 2 | — |
| Optimal | 6–8 | 5–10 | single slide |
| Maximum | 10 | 15 | → split at hub boundary |

**Overflow Strategy**: Variant B large architectures: split into "Data Ingestion" slide (sources → golden record) and "Data Distribution" slide (golden record → consumers).

---

## 8. Anti-Patterns

1. **Single source assumption**: Designing an MDM lifecycle that assumes only one source system — most real MDM scenarios require multi-source survivorship to establish the golden record.
2. **No survivorship logic**: Showing multiple sources flowing into a golden record without explaining the matching, merging, or scoring rules — this is the core MDM design decision.
3. **Missing error/rejection paths**: Showing only the happy path where all source records merge cleanly — data quality failures and rejection loops are inevitable and must be designed.
4. **No retention policy at archive stage**: Archive/retire stage without data retention rules is a GDPR and compliance risk.
5. **Mixing MDM entities**: Combining Customer and Product master data in one lifecycle diagram — each entity type has distinct lifecycle rules and should have its own diagram.

---

## 9. Industry Reference Patterns

**DAMA-DMBOK2 MDM Implementation Styles**:
DAMA defines 4 MDM architecture styles: Registry (link to source), Consolidation (collect from sources), Coexistence (source and hub both maintain), and Centralized (hub is the system of record). Variant B maps to Registry/Consolidation. Variant C (survivorship) maps to the Consolidation/Centralized styles where the hub creates the authoritative golden record.

**Gartner MDM Reference Architecture**:
Gartner's MDM reference architecture has 5 layers: Data Sources, Data Integration, Managed Master Data, MDM Services, and Data Consumers. The lifecycle flows through the Integration and Managed Master Data layers. Key insight: the "golden record" is not a data copy — it is a trusted curated view built from source contributions, with a clearly defined master data steward accountable for its quality.

**Informatica MDM Design Patterns**:
Informatica classifies MDM data states: Pending (initial creation), Active (validated and published), Superseded (replaced by merge), Deprecated (soft-delete pending review), Archived (end-of-life). These 5 states map directly to the lifecycle stages in Variant A, providing a standard vocabulary for state machine design.

---

## 10. Production QA Checklist

- [ ] All primary lifecycle stages (Create → Validate → Golden Record → Distribute → Maintain → Archive) are represented
- [ ] Data quality gate present between creation and golden record stages
- [ ] Error/rejection path shown with feedback loop to correction
- [ ] Source systems identified at creation stage
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] MDM architecture style (Registry/Consolidation/Coexistence/Centralized) is stated
- [ ] Golden record store is visually emphasized (bold border, prominent position)
- [ ] Data retention and right-to-erasure policy annotated at archive stage
- [ ] SLA or processing time annotations present on critical stages
- [ ] Presenter can explain the survivorship rule in 30 seconds
