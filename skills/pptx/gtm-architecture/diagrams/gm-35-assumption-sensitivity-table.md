# GM-35: Assumption Sensitivity Table - GTM Diagram Spec

Ref: Financial sensitivity analysis | Scenario modeling in business cases

## 1. Purpose and When to Use
Definition: A table showing how ROI or payback changes when core assumptions vary across scenarios.
Use when: CFO discussions, procurement scrutiny, risk-adjusted business case.
Questions answered: Is the value case robust under realistic assumption changes?
Primary audience: Finance, procurement, executive sponsors.

## 2. Visual Layout Specification
Variant A (recommended): Rows as assumptions, columns for Base, Conservative, Aggressive, and impact on ROI/payback.
Variant B: Tornado-style ranked sensitivity table.
Variant C: Scenario table with probability weights.

**Grid Proportions**:
- 5-column table: 8.5" wide at (0.5", 1.1")
- Column widths: Assumption 2.5", Base 1.2", Conservative 1.2", Aggressive 1.2", Impact on ROI 1.8"
- Row height: 32pt; header row: 36pt, `#44546A` fill
- Summary row: 40pt, bold, `#00CCD7` accent border
- Impact bar (inline): max width 1.4", color coded by scenario
- High-sensitivity row highlight: `#44546A` left border 3pt
- Footnote area: bottom 0.3" of slide, 7pt text for source and confidence notes

## 3. Color Semantics
Base case: #00CCD7
Conservative case: #A5A7AA
Aggressive case: #53E3EB
Critical sensitivity assumption: #44546A outline

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, headers 9pt bold, row values 8.5-9pt, summary row 10pt bold, footnote 7pt.

## 5. Shape and Connector Vocabulary
Table format with optional impact bars.
No decorative connectors.

## 6. Annotation Rules
Assumption definitions must be explicit and measurable.
State source and confidence for each assumption.
Highlight top 2-3 assumptions with greatest outcome impact.

## 7. Content Density Rules
Minimum: 5 assumptions.
Optimal: 8-12 assumptions.
Maximum: 16 assumptions then split by value driver.

## 8. Anti-Patterns
Hidden assumptions inside formula notes.
Single deterministic ROI value with no sensitivity.
Unrealistic aggressive scenario presented as likely.

## 9. Industry Reference Patterns
Robust business cases include base and downside scenarios.
Sensitivity tables reduce risk perception in procurement reviews.

## 10. Production QA Checklist
- [ ] Assumptions are explicit and measurable
- [ ] Base/conservative/aggressive scenarios are complete
- [ ] Impact on ROI or payback is shown
- [ ] High-sensitivity assumptions are highlighted
- [ ] Sources and confidence levels are present
