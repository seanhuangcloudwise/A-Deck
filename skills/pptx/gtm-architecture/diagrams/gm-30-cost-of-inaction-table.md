# GM-30: Cost of Inaction Table - GTM Diagram Spec

Ref: Opportunity cost framing | Decision urgency models

## 1. Purpose and When to Use
Definition: A table quantifying business and risk losses if the organization does not adopt the proposed solution.
Use when: creating urgency, executive decision support, stalled deal recovery.
Questions answered: What is lost by delaying action?
Primary audience: Executives, finance, procurement sponsors.

## 2. Visual Layout Specification
Variant A (recommended): Rows by risk/loss category, columns for current state, annual impact, trend, mitigation.
Variant B: Time-based inaction cost ladder (month 0, 3, 6, 12).
Variant C: Scenario table (best/likely/worst inaction outcomes).

**Grid Proportions**:
- 4-column table: 8.5" wide at (0.5", 1.1")
- Column widths: Category 2.5", Current State 2.0", Annual Impact 2.0", Trend 1.5"
- Row height: 32pt; header row: 36pt, `#44546A` fill
- Total row: 40pt, bold text, `#00CCD7` accent border
- Severity chip: 8pt circle left-aligned within category cell
- Trend arrow: 12pt, inline within Trend column (↑ red / → gray / ↓ green)

## 3. Color Semantics
Loss severity high: #44546A
Medium: #53E3EB
Low: #A5A7AA
Urgency highlight: #00CCD7

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, headers 9pt bold, cell text 8.5-9pt, total row 10pt bold, footnote 7pt.

## 5. Shape and Connector Vocabulary
Table with severity chips and optional trend arrows.
No decorative connectors.

## 6. Annotation Rules
All cost estimates should state assumptions and confidence.
Use conservative ranges where precision is limited.
Include non-financial risk where material (compliance, reputation).

## 7. Content Density Rules
Minimum: 4 categories.
Optimal: 6-10 categories.
Maximum: 14 categories then split by cost type.

## 8. Anti-Patterns
Fear-only slide without data.
Double-counting losses across categories.
Presenting speculative values as audited numbers.

## 9. Industry Reference Patterns
Decision acceleration assets often pair inaction cost with payback model.
Balanced tables include both hard and soft cost with confidence levels.

## 10. Production QA Checklist
- [ ] Categories are mutually exclusive where possible
- [ ] Assumptions and confidence are shown
- [ ] Total impact calculation is traceable
- [ ] Financial and non-financial risks are balanced
- [ ] Claims are defensible and non-exaggerated
