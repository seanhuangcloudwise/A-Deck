# AA-01: Application Landscape Map — Application Architecture Diagram Spec

_Ref: TOGAF ADM Phase C (Application Architecture) | Gartner Application Rationalization | EA Repository Standards_

---

## 1. Purpose & When to Use

**Definition**: A portfolio-level map showing all significant applications in scope, organized by capability domain or business function, with portfolio attributes (health, investment status, lifecycle stage) visually encoded.

**Use When**:
- Performing application rationalization or portfolio review
- Communicating the current IT application estate to business or executive audiences
- Preparing input for transition architecture planning
- Identifying redundancy, obsolescence, and coverage gaps in the application portfolio
- Onboarding new architects or presenting IT landscape to external consultants

**Questions Answered**:
- What applications exist and what business functions do they serve?
- Which applications are core, supporting, or legacy?
- Where are redundancies (multiple apps serving same capability)?
- Which areas have no application support (coverage gaps)?

**Primary Audience**: CTO, CIO, Enterprise Architects, Application Portfolio Managers

---

## 2. Visual Layout Specification

**Structure**: Grid or heat-map organized by business function domain — applications placed in capability cells.

### Variant A: Capability-Aligned Grid
- Rows = capability domains (from BA-01 Capability Map)
- Columns = application layers (System of Record / Engagement / Insight)
- Application boxes placed in cells where they serve that capability
- Best for: Business-IT alignment communication

### Variant B: Business Function Map
- Business functions arranged spatially (top = customer-facing, bottom = infrastructure)
- Applications shown as blocks within function zones
- Size of block proportional to investment or criticality
- Best for: Portfolio rationalization, executive overview

### Variant C: Lifecycle Roadmap View
- X-axis = time (Current / 2026 / 2027)
- Y-axis = application layers
- Application blocks shown with lifecycle status (Invest/Maintain/Retire)
- Best for: Migration planning, budget planning

**Grid Proportions**:
- Domain row header: 120pt wide
- Application block: 90pt × 36pt minimum
- Block gutters: 6pt
- Legend strip at bottom: 50pt height

---

## 3. Color Semantics

| Application Status | Meaning | Fill Color |
|---|---|---|
| Strategic / Invest | Core, growing investment | `#00CCD7` |
| Maintain / Sustain | Stable, business-as-usual | `#53E3EB` |
| Harvest / Retire | Phasing out | `#A5A7AA` |
| Legacy / Risk | Critical risk, needs replacement | `#A5A7AA` + dashed red border |
| New / Planned | Not yet deployed | White + `#00CCD7` dashed border |
| External / SaaS | Third-party application | White + `#44546A` border |
| Domain header | Capability domain background | `#44546A` |
| Coverage gap zone | No application assigned | Faint red hatch pattern |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Domain Header | Capability domain label | 10pt | Bold, White |
| Application Name | Block label | 8–9pt | SemiBold |
| Layer Label | SoR / SoE / SoI | 9pt | Regular, `#A5A7AA` |
| Lifecycle Tag | Invest/Retire/Maintain | 7pt | Regular |
| Legend Label | Color key | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Standard rect | Application block |
| Dashed rect | New/planned application |
| Gray + dashed red border | Legacy/at-risk application |
| Domain container (wide) | Capability domain zone |
| Bold border | Strategic priority application |
| No connectors | (Landscape maps show portfolio, not flow) |

**Connector Rule**: Application landscape maps do NOT use connectors — spatial proximity implies functional relationship. If integration flows are needed, use AA-03 Integration Map.

---

## 6. Annotation Rules

- **Application ID**: Short code in top-left of block (e.g., "CRM-01") for cross-reference
- **User count badge**: Optional chip showing user base scale (e.g., "2,000 users")
- **Health RAG**: Small circle in top-right: Green (healthy), Amber (at risk), Red (critical)
- **Cost tier**: Small "$" / "$$" / "$$$" icon for relative investment tier
- **Overlap marker**: When 2+ apps serve same function, draw an overlap rectangle with `∩` symbol

---

## 7. Content Density Rules

| Mode | Applications | Domains | Per Slide |
|---|---|---|---|
| Minimum | 5 | 3 | — |
| Optimal | 15–30 | 5–8 | 30 max |
| Maximum | 60 | 10 | → split by domain cluster |

**Overflow Strategy**: Split by domain cluster (e.g., "Customer & Sales Applications" / "Operations & Finance Applications"). Each slide shows 2–3 domains in full detail.

---

## 8. Anti-Patterns

1. **One box per vendor**: Mapping applications by vendor contract instead of functional scope — one ERP can serve 5 capability domains and needs 5 placement instances.
2. **Missing lifecycle status**: Application blocks with no investment status encoding — portfolio maps without health indicators are incomplete.
3. **Adding connectors**: Drawing integration lines between all apps on the landscape map — creates spaghetti; save integration for AA-03.
4. **Individual screens as applications**: Each module or feature as a separate block — keep at application system level.
5. **No coverage gap identification**: A landscape map that doesn't highlight any gaps fails to justify rationalization investment.

---

## 9. Industry Reference Patterns

**Gartner Application Portfolio Management (APM)**:
Gartner's APM framework categorizes applications by Business Value vs. Technical Condition. High Value + Good Condition = Invest. High Value + Poor Condition = Fix. Low Value + Good Condition = Migrate. Low Value + Poor Condition = Retire. This 2×2 matrix, overlaid on the landscape, turns a descriptive catalog into an actionable decision map.

**The Open Group IT4IT Portfolio Management Reference Architecture**:
IT4IT's Portfolio & Project Management capability includes Application Portfolio Rationalization, where applications are mapped to services in a Service Model. Applications serving the same service are rationalization candidates. The three-layer model (System of Record / System of Engagement / System of Insight) is the organizing framework for Variant A.

**McKinsey Digital Architecture Simplification**:
McKinsey's observation from 200+ digital transformations: organizations that reduce application portfolio complexity by 40% achieve 30% faster delivery cycles. The landscape map is the diagnostic tool. Key simplification rules: consolidate applications serving same capability, externalize non-differentiating applications to SaaS, and retain as custom only what creates competitive advantage.

---

## 10. Production QA Checklist

- [ ] All applications have lifecycle status encoding (Invest/Maintain/Retire)
- [ ] Coverage gaps (capability domains with no application) are identified
- [ ] Redundant applications (multiple apps per capability) are flagged
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Domain rows align with capability names from BA-01 Capability Map
- [ ] Legend strip with color semantics is present
- [ ] No integration connectors on landscape (save for AA-03)
- [ ] Health RAG indicators present on application blocks
- [ ] Total application count is visible in subtitle or annotation
- [ ] Presenter can identify the top 3 portfolio risks in 30 seconds
