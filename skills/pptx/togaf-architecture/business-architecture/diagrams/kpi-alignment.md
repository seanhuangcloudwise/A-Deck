# BA-09: KPI-to-Objective Alignment — Business Architecture Diagram Spec

_Ref: Balanced Scorecard (Kaplan & Norton) | OKR Framework (Doerr/Google) | TOGAF Architecture Principles_

---

## 1. Purpose & When to Use

**Definition**: A cascading alignment diagram that connects strategic objectives to measurable KPIs, target values, and accountable owners — showing that every metric is traceable to a business goal and every goal has measurable evidence of progress.

**Use When**:
- Setting up or reviewing a performance management framework
- Presenting strategy execution progress to executives or board
- Aligning departmental KPIs to corporate strategic objectives
- Designing OKR systems and making the objective-result chain visible
- Conducting architecture review: confirming each capability investment drives a measurable KPI

**Questions Answered**:
- Which KPIs serve which strategic objectives?
- Who is accountable for each KPI?
- Are there objectives without measurable KPIs (coverage gaps)?
- Are there KPIs that don't connect to any strategic objective (vanity metrics)?

**Primary Audience**: Executives, PMO, Strategy teams, Department heads, Governance boards

---

## 2. Visual Layout Specification

**Structure**: Cascading tree or alignment matrix — strategic objectives at top, KPIs below, targets and owners at leaf level.

### Variant A: Cascading Tree (1–3 strategic objectives → 3–5 KPIs each → targets + owners)
- Strategic objective nodes at top (large, #44546A)
- KPI nodes in middle tier (medium, #00CCD7)
- Target / Owner chips at bottom (small, gray pills)
- Best for: Leadership deck, annual strategy review

### Variant B: Balanced Scorecard Matrix
- 4 rows = BSC perspectives: Financial / Customer / Process / Learning & Growth
- Columns = Objectives, KPIs, Targets, Status (RAG)
- Status color: Green = on track, Amber = at risk, Red = below target
- Best for: Board and governance reporting

### Variant C: OKR Alignment Diagram
- Objective blocks at top row (large, bold)
- Key Results listed as bullet chips below each Objective
- Progress bar inside each Key Result chip (% complete)
- Initiative tags at bottom connecting to Key Results
- Best for: OKR quarterly reviews, agile organizations

**Grid Proportions**:
- Objective tier: 25% of content height
- KPI tier: 45% of content height
- Target/owner tier: 30% of content height
- Tree connector lines stroke: 1.5pt `#A5A7AA`

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Strategic objective | Top-level goal | `#44546A` + White |
| KPI on track | Target being met | `#00CCD7` + White |
| KPI at risk | Within 80–99% of target | `#53E3EB` + `#2F2F2F` |
| KPI below target | Below 80% of target | `#A5A7AA` + Red `!` |
| Target chip | Numeric target value | White + `#2F2F2F` border |
| Owner tag | Responsible party | `#44546A` pill |
| BSC row header | Perspective label | `#44546A` |
| Progress bar fill | OKR completion % | `#00CCD7` left-to-right fill |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Objective Label | Strategic goal statement | 12–13pt | Bold, White |
| KPI Name | Metric identifier | 10–11pt | SemiBold, White |
| Target Value | Numeric goal | 10pt | Regular |
| Actual Value | Current performance | 10pt | Bold (colored by RAG) |
| Owner Name | Accountability label | 8–9pt | Regular |
| Period Label | Q1/H1/FY annotation | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large rounded rect (≤4pt) | Strategic objective block |
| Medium rounded rect | KPI metric block |
| Small rect or pill | Target value or owner name |
| Progress bar (thin rect) | OKR completion indicator |
| RAG circle | Status indicator (Green/Amber/Red) |
| Tree branch connectors | Objective → KPI cascade |
| Dashed container | KPI cluster per perspective (BSC) |

**Connector Rule**: Tree connectors show parent→child cascade (objective contains KPIs). Use solid lines for confirmed links; dashed lines for proposed/provisional. Never use decorative curved lines — straight orthogonal connectors maintain clarity.

---

## 6. Annotation Rules

- **Progress vs. target**: Dual-line format inside each KPI block: "Target: 95% / Actual: 88%" in 10pt
- **Trend arrow**: Small `↑` / `↓` / `→` indicator showing trend direction vs. last period
- **Period label**: Annotation in slide subtitle or KPI block footer: "Q1 2026 Review"
- **Gap highlight**: Bold red border + `!` for KPIs more than 20% below target
- **Coverage gap**: Empty slot below Objective labeled "KPI TBD" in dashed/gray outline

---

## 7. Content Density Rules

| Mode | Objectives | KPIs Total | Per Slide |
|---|---|---|---|
| Minimum | 1 | 3 | — |
| Optimal | 2–4 | 8–16 | 15 KPIs max |
| Maximum | 6 | 24 | → split by perspective |

**Overflow Strategy**: For BSC, each perspective can have its own slide. Connect with a summary dashboard slide showing overall RAG status per perspective. For OKR, split by team/department if > 5 objectives.

---

## 8. Anti-Patterns

1. **Vanity KPIs**: Metrics that always go up ("Number of features launched") without meaningful target ceilings — add challenging targets or remove the KPI.
2. **Orphaned KPIs**: KPIs listed without connection to any strategic objective — "vanity metrics" that measure activity, not value. Flag and remove.
3. **Missing owners**: KPIs without accountable owners are unenforceable commitments — every KPI needs a named or role-based owner.
4. **Too many KPIs per objective**: Cascading one objective to 10+ KPIs makes accountability diffuse — limit to 3–5 KPIs per objective.
5. **Status without definition**: RAG status without defining what Green/Amber/Red means in numeric terms — each slide must include threshold definitions.

---

## 9. Industry Reference Patterns

**Kaplan & Norton Balanced Scorecard (1992, HBR)**:
The BSC organizes performance measurement into four perspectives: Financial (shareholder value), Customer (value proposition), Internal Process (operational excellence), Learning & Growth (organizational capabilities). The key insight is strategy causality: Learning & Growth capabilities → improve Internal Processes → deliver Customer Value → drive Financial Results. Use this causal flow as the vertical ordering in Variant B.

**OKR Framework (John Doerr, "Measure What Matters", 2018)**:
OKRs separate aspirational Objectives (qualitative direction) from measurable Key Results (quantitative milestones). Key Results should be: specific, time-bound, aggressive-but-achievable, and owned. Doerr's rule: "if it doesn't have a number, it's a task, not a Key Result." The cascading OKR tree (Company → Team → Individual) maps directly to Variant C.

**TOGAF Architecture Principles → KPI Linkage**:
TOGAF recommends that each Architecture Principle is supported by metrics that measure compliance. Each capability investment should have a corresponding performance measure. The KPI Alignment diagram serves as the governance tool showing that investment decisions are traceable to measurable business outcomes.

---

## 10. Production QA Checklist

- [ ] Every KPI connects to exactly one strategic objective (no orphaned KPIs)
- [ ] Every strategic objective has at least 2 measurable KPIs
- [ ] Target values and actual/current values are shown (not labels only)
- [ ] Owner is specified for every KPI
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] RAG status thresholds are defined (what constitutes Green/Amber/Red)
- [ ] Trend indicators (up/down/flat) are present for each KPI with prior-period comparison
- [ ] Period of measurement is clearly stated on the slide
- [ ] Presenter can identify the top 2 at-risk KPIs in 10 seconds
- [ ] Alignment between KPIs and BA-01 Capability Map investment priorities is traceable
