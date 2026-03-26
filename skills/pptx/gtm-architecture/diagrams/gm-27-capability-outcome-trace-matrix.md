# GM-27: Capability to Outcome Trace Matrix - GTM Diagram Spec

Ref: Traceability matrix practices | Outcome-based product marketing

## 1. Purpose and When to Use
Definition: A matrix tracing each product capability to expected outcomes, KPI measures, and proof references.
Use when: validating claims, analyst prep, audit-friendly value presentations.
Questions answered: Which capability supports which outcome, and what proof exists?
Primary audience: PMM, RevOps, analyst relations.

## 2. Visual Layout Specification
Variant A (recommended): Columns for Capability, Outcome, KPI, Baseline, Target, Evidence.
Variant B: Outcome-centric matrix with multiple capabilities per row.
Variant C: Trace matrix with confidence score column.

**Grid Proportions**:
- 6-column table: 8.5" wide at (0.5", 1.1")
- Column widths: Capability 1.5", Outcome 1.8", KPI 1.2", Baseline 0.8", Target 0.8", Evidence 1.0"
- Row height: 28–32pt; header row: 36pt, `#44546A` fill
- Evidence ID badge: 7pt, pill shape within cell
- Confidence chip (Variant C): 8pt circle, color-coded by confidence level
- Maximum rows: 20; split by domain if exceeding

## 3. Color Semantics
Capability column accents: #53E3EB
Outcome/KPI highlight: #00CCD7
Evidence confidence low: #A5A7AA
Header: #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, headers 9pt bold, row cells 8.5-9pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Table-centric layout; no connectors required.
Optional confidence chips.

## 6. Annotation Rules
Every row should include metric definition and measurement period.
Evidence references should be uniquely tagged (E1, E2...).
If target is projected, mark assumption level.

## 7. Content Density Rules
Minimum: 6 rows.
Optimal: 8-14 rows.
Maximum: 20 rows then split by domain.

## 8. Anti-Patterns
Capabilities not tied to outcomes.
Outcome claims without baseline.
Evidence references that cannot be traced.

## 9. Industry Reference Patterns
Traceability tables are common in regulated and enterprise procurement settings.
Confidence tagging helps separate verified vs estimated value.

## 10. Production QA Checklist
- [ ] Every capability maps to at least one outcome
- [ ] KPI definition is explicit
- [ ] Baseline and target are both present
- [ ] Evidence id is unique and traceable
- [ ] Assumed values are clearly labeled
