# DA-05: Data Governance Framework — Data Architecture Diagram Spec

_Ref: DAMA-DMBOK2 Chapter 3 | COBIT 2019 | Gartner Data & Analytics Governance Framework_

---

## 1. Purpose & When to Use

**Definition**: A framework diagram showing the organizational structures, roles, policies, processes, and standards that govern data — illustrating how data accountability is structured across the organization.

**Use When**:
- Launching or communicating a data governance program to executive sponsors
- Clarifying governance roles: who makes which data decisions
- Designing the data governance operating model (federated, centralized, hybrid)
- Presenting data governance maturity assessment to CDO or board
- Connecting data governance to business outcomes and risk management

**Questions Answered**:
- What governance bodies, roles, and processes are in place for data?
- Who owns data quality, definitions, and access policies?
- How does data governance connect to business strategy and IT delivery?
- What is the maturity of data governance and where are the gaps?

**Primary Audience**: CDO, Data Governance Board, Compliance/Risk teams, Executive sponsors

---

## 2. Visual Layout Specification

**Structure**: Layered or wheel framework diagram — governance bodies at top, domains in middle, processes and tools at bottom.

### Variant A: Governance Operating Model (Layered)
- Top layer: Executive governance (CDO, Data Council)
- Middle layer: Domain stewardship (data domain owners + stewards)
- Bottom layer: Operational governance (tools, processes, policies)
- Best for: Communicating governance structure to executive audience

### Variant B: Governance Wheel / Radar
- Central hub: Data Strategy
- Spokes: 6–8 governance functions (Quality, Security, Catalog, Lineage, MDM, Privacy, Compliance, Architecture)
- Outer ring: Governance maturity levels per function
- Best for: Maturity assessment, gap planning

### Variant C: RACI-Linked Governance Model
- Governance bodies as nodes in upper section
- Data domains in middle
- Decision types (Define / Approve / Enforce / Monitor) as labeled connections
- Best for: Operating model design, role clarity

**Grid Proportions**:
- Layer height: equal thirds for Variant A
- Wheel radius: 40% of slide height for Variant B
- Governance body block: 130pt × 60pt
- Connecting line stroke: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Executive governance body | Strategic decision authority | `#44546A` + White |
| Domain owner / steward | Operational accountability | `#00CCD7` + White |
| Tool / platform | Enabling technology | `#53E3EB` + `#2F2F2F` |
| Policy / standard element | Rule or constraint | `#2F2F2F` + White |
| Governance function (wheel) | Capability area | `#00CCD7` segment |
| Mature function (wheel) | High maturity | `#00CCD7` filled to outer ring |
| Developing function | Medium maturity | `#53E3EB` filled to mid-ring |
| Immature function | Low maturity | `#A5A7AA` minimal fill |
| Mandated connection | Formal authority flow | `#2F2F2F` solid thick arrow |
| Advisory connection | Consulting/informing | `#A5A7AA` dashed arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Governance Body Name | Block label | 11pt | Bold, White |
| Role Description | Sub-label in block | 8pt | Regular |
| Function Label (wheel) | Spoke label | 9pt | SemiBold |
| Policy Reference | Document link | 8pt | Regular, `#44546A` |
| Maturity Level | Score annotation | 9pt | Bold, color-coded |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Wide rounded rect | Governance body or committee |
| Standard rounded rect | Data owner / steward role |
| Small pill | Governance tool or policy reference |
| Filled segment (wheel) | Governance function area with maturity |
| Central circle (wheel) | Data strategy hub |
| Solid thick arrow | Formal accountability / authority |
| Dashed arrow | Advisory or consultative relationship |
| Horizontal divider | Governance layer boundary |

---

## 6. Annotation Rules

- **Role count**: Number of people/teams in each governance role: "3 Domain Stewards"
- **Meeting cadence**: Governance body has frequency annotation: "Monthly Data Council"
- **Policy reference**: Arrow from policy-making bodies: "→ Data Classification Policy v2"
- **Maturity score**: Wheel variants include numeric score: "Data Quality: L2 (3/5)"
- **Gap indicator**: Empty or red-dashed segment on wheel showing capability with no governance in place

---

## 7. Content Density Rules

| Mode | Governance Bodies | Functions/Spokes | Per Slide |
|---|---|---|---|
| Minimum | 2 | 4 | — |
| Optimal | 3–5 | 6–8 | single slide |
| Maximum | 8 | 10 | → 2 slides |

**Overflow Strategy**: For large organizations, separate Executive Governance (strategic) and Domain Governance (operational) onto separate slides. Add a connecting arch diagram showing how the two tiers interact.

---

## 8. Anti-Patterns

1. **Tool-centric governance**: Presenting a governance framework as a set of tools ("We use Collibra + Great Expectations") — governance is people, process, and policy first; tools are enablers, not the framework.
2. **Missing decision rights**: Showing bodies without explaining what decisions each makes — governance is about decision authority, not org charts.
3. **Federated without process**: Claiming federated governance without showing how domain stewards coordinate — decentralization requires explicit coordination mechanisms.
4. **Executive-only framework**: Showing only the CDO and Data Council — operational governance (stewards, owners, quality processes) must be equally visible.
5. **No maturity baseline**: Governance framework without maturity assessment leaves stakeholders without a benchmark for progress.

---

## 9. Industry Reference Patterns

**DAMA-DMBOK2 Data Governance Framework (Wheel Model)**:
DAMA's DMBOK2 organizes data management into 11 knowledge areas: Data Governance, Data Architecture, Data Modeling, Data Storage, Data Security, Data Integration, Documents & Content, Reference & Master Data, Data Warehousing & BI, Metadata, Data Quality. Data Governance sits at the center, coordinating all other areas. The Variant B wheel model directly represents this framework.

**Gartner Data & Analytics Governance Framework**:
Gartner defines governance across three domains: Organizational (roles, accountabilities, decision rights), Operational (policies, standards, processes), and Technology-Enabled (tools, catalogs, automation). Good governance connects all three. A common maturity gap: organizations have strong Organizational governance but weak Operational process governance — maturity assessment reveals this.

**COBIT 2019 Data Governance Objectives**:
COBIT's governance objectives for data include: Managed Data (APO14) — define and maintain data architecture; Managed Information Security (DSS05); and Monitored, Evaluated, and Assessed Performance (MEA). COBIT's RACI chart for these objectives maps to Variant C.

---

## 10. Production QA Checklist

- [ ] All governance bodies have a named decision authority defined
- [ ] Data Domain Owners and Data Stewards are distinct roles with clear responsibilities
- [ ] Tool/technology layer shown separately from organizational governance
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Connection arrows between governance layers are labeled with authority type (Mandate/Advisory)
- [ ] Maturity assessment present if framework is used for gap analysis
- [ ] Governance gaps (functions with no body ownership) are explicitly shown
- [ ] Meeting cadences are shown for key governance bodies
- [ ] Data governance framework connects to business strategy (explicit arrow or annotation)
- [ ] Presenter can explain the key governance accountability in 30 seconds
