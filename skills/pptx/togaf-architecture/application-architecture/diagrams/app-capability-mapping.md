# AA-09: Application-to-Capability Mapping — Application Architecture Diagram Spec

_Ref: TOGAF ADM Phase C→B Traceability | Gartner APM Business Value Analysis | EA Traceability Matrix_

---

## 1. Purpose & When to Use

**Definition**: A traceability matrix or bipartite map connecting applications in the IT portfolio to the business capabilities they realize — enabling investment justification, gap identification, and portfolio rationalization.

**Use When**:
- Justifying IT investment with business capability language (for non-IT stakeholders)
- Identifying capabilities without application support (coverage gaps)
- Finding redundant applications supporting the same capability
- Prioritizing application modernization by capability strategic importance
- Building the cross-layer traceability required by TOGAF architecture governance

**Questions Answered**:
- Which applications support which business capabilities?
- Are strategic capabilities adequately supported by applications?
- Which applications can be retired because their capabilities are covered elsewhere?
- Where must new applications be built or purchased to fill capability gaps?

**Primary Audience**: Enterprise Architects, CIO, Application Portfolio Managers, Business Transformation Leaders

---

## 2. Visual Layout Specification

**Structure**: Matrix (capabilities as columns, applications as rows) or bipartite graph.

### Variant A: Traceability Matrix
- Rows = Applications (with lifecycle status indicator)
- Columns = Business capabilities (grouped by domain)
- Cells = filled if application realizes that capability
- Best for: Portfolio rationalization, EA governance review

### Variant B: Coverage Heatmap
- Same structure as Variant A
- Cell fill intensity = strength of support (Full / Partial / Marginal)
- Domain summary row at bottom: "Coverage: 83%"
- Best for: Executive investment decision storytelling

### Variant C: Bipartite Value Map
- Left: Application nodes (color-coded by lifecycle status)
- Right: Capability nodes (color-coded by strategic importance)
- Edges: solid = primary support, dashed = marginal/accidental
- Best for: Rationalization workshop, investment prioritization

**Grid Proportions**:
- Application row header: 160pt wide
- Capability column header: 70pt wide
- Cell: 50pt × 32pt minimum
- Domain separator bar: full-width, #44546A fill

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Full/Primary support | Application is core to capability | `#00CCD7` filled cell |
| Partial support | Application contributes some functions | `#53E3EB` filled cell |
| Marginal support | Minor, non-essential contribution | `#A5A7AA` filled cell |
| No support | No mapping between app and capability | White (empty) |
| Critical gap | Strategic capability with no app support | Red dashed border column |
| Redundant coverage | 3+ apps supporting same capability | `#44546A` column header marker |
| Strategic capability column | High investment priority capability | Bold column header |
| Legacy/retire-status application row | Lifecycle risk apps | `#A5A7AA` row header, strikethrough |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Application Name | Row label | 9–10pt | Regular |
| Application Status | Lifecycle tag | 8pt | Italic, gray |
| Capability Name | Column header | 9pt | SemiBold, rotated 45° if >8 |
| Domain Group Header | Column group | 10pt | Bold, White on `#44546A` |
| Gap Note | "No Coverage" annotation | 8pt | Red Bold |

---

## 5. Shape & Connector Vocabulary

**Matrix Variant**:
| Shape | Meaning |
|---|---|
| Filled cell (`#00CCD7`) | Primary capability support |
| Half-filled cell (`#53E3EB`) | Partial support |
| Empty cell | No mapping |
| Red dashed column border | Critical coverage gap |
| Bold row border | Strategic investment-locked application |
| Group header bar | Capability domain separator |

**Bipartite Variant**:
| Shape | Meaning |
|---|---|
| Rounded rect (left) | Application node |
| Rounded rect (right) | Capability node |
| Solid edge | Primary application-capability link |
| Dashed edge | Marginal contribution |
| Bold border | Strategic priority capability |

---

## 6. Annotation Rules

- **Coverage percentage**: Summary row at bottom of matrix: "Overall Capability Coverage: 76%"
- **Gap count annotation**: "4 strategic capability gaps identified" in subtitle or annotation box
- **Redundancy marker**: `∩` symbol in column header when 3+ applications support same capability
- **Investment arrow**: Upward triangle in column header for capability receiving planned investment
- **Retirement flag**: Strikethrough on application row with "Retire: Q2 2026" annotation

---

## 7. Content Density Rules

| Mode | Applications | Capabilities | Matrix Cells | Per Slide |
|---|---|---|---|---|
| Minimum | 4 | 4 | 16 | — |
| Optimal | 10–15 | 8–12 | 80–180 | 150 cells max |
| Maximum | 20 | 15 | 300 | → split by capability domain |

**Overflow Strategy**: Split by capability domain. Each domain's columns shown against full application row list. Use consistent row ordering across all split slides for row-tracking.

---

## 8. Anti-Patterns

1. **Technology capabilities**: Using IT capabilities ("Cloud Hosting", "Database") instead of business capabilities from BA-01 — the mapping must be business-language to make it meaningful to non-IT stakeholders.
2. **100% filled matrix**: Every application marked as supporting everything — destroys analytical value. Be critical about what "supports" means (primary function only).
3. **No lifecycle status on applications**: Matrix without investment status (Invest/Maintain/Retire) fails to support rationalization decisions.
4. **Missing gap identification**: A matrix without highlighted gaps is a documentation exercise, not an architectural analysis tool.
5. **Granularity mismatch**: Mixing application-level rows with module-level rows — all rows must represent complete deployable application systems.

---

## 9. Industry Reference Patterns

**Gartner Application Portfolio Management Business Value Scoring**:
Gartner's APM methodology scores each application on two axes: Business Value (capability coverage + fitness) and Technical Condition (code quality, security, maintainability). Overlaying this 2×2 score on the traceability matrix guides rationalization: High Value + Good Condition = Invest; High Value + Poor Condition = Fix; Low Value + Good Condition = Consolidate; Low Value + Poor Condition = Retire.

**TOGAF Architecture Cross-View Traceability (Phase C→B)**:
TOGAF mandates that Application Architecture (Phase C) traces back to Business Architecture (Phase B). The application-to-capability mapping IS this traceability artifact. TOGAF's Architecture Repository should contain this matrix as part of the Application Architecture catalog. Version it alongside capability map updates.

**McKinsey Technology Simplification**:
McKinsey's IT simplification framework identifies "stranded investments" — applications supporting capabilities that are no longer strategically relevant. The app-to-capability matrix is the tool that makes stranded investments visible: applications aligned only to low-priority or retired capabilities can be safely decommissioned.

---

## 10. Production QA Checklist

- [ ] All capability names match exactly those in BA-01 Capability Map
- [ ] All application names match exactly those in AA-01 Application Landscape
- [ ] Each application row has lifecycle status (Invest/Maintain/Retire)
- [ ] Coverage percentage is calculated and shown
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Critical gaps (strategic capabilities with no application support) are highlighted
- [ ] Redundant coverage (3+ apps per capability) is flagged
- [ ] Application retirement timeline present for Retire-status rows
- [ ] Investment direction aligns with capability strategic priority
- [ ] Presenter can explain top 2 rationalization recommendations in 45 seconds
