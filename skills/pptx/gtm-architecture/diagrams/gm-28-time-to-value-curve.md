# GM-28: Time to Value Curve - GTM Diagram Spec

Ref: Forrester TEI payback analysis | Customer success value curve patterns

## 1. Purpose and When to Use
Definition: A curve showing how value accumulates over time from implementation to steady-state benefits.
Use when: business case storytelling, onboarding expectations, renewal defense.
Questions answered: When does value start, when is payback, and when does value peak?
Primary audience: Sales, CS, finance buyers.

## 2. Visual Layout Specification
Variant A (recommended): X-axis time, Y-axis cumulative value with implementation dip and acceleration.
Variant B: Multi-curve by customer segment.
Variant C: Value vs cost crossover curve.

**Grid Proportions**:
- Chart area: 7.5" × 3.5" at (0.75", 1.2")
- X-axis: time periods (months/quarters), labels 8.5pt, at chart bottom
- Y-axis: value scale, labels 8pt, at chart left
- Value curve line: 2pt, `#00CCD7`; cost line: 1.5pt, `#A5A7AA`
- Milestone dot: 14pt on curve; label 8.5pt above/below
- Payback marker: vertical dashed line 1pt `#44546A` with label
- Shaded period blocks (implementation/adoption/optimization): 60% opacity fills

## 3. Color Semantics
Value curve: #00CCD7
Cost curve or payback threshold: #A5A7AA
Milestone markers: #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, axis labels 9pt, milestone labels 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Curves, milestone dots, vertical reference lines for key dates.
Optional shaded period blocks (implementation, adoption, optimization).

## 6. Annotation Rules
Mark TTV point, payback point, and steady-state range.
State assumptions and sample profile in footnote.
Use consistent time unit (months or quarters).

## 7. Content Density Rules
Minimum: one curve and 2 milestones.
Optimal: one to three curves and 3-5 milestones.
Maximum: four curves; otherwise split by segment.

## 8. Anti-Patterns
No explicit baseline.
Mixing customers with incompatible profiles on one curve.
Using cumulative and period value without labeling.

## 9. Industry Reference Patterns
Best value curves separate implementation lag from benefit ramp.
TEI-style payback markers improve CFO readability.

## 10. Production QA Checklist
- [ ] Axes and units are explicit
- [ ] TTV and payback markers are present
- [ ] Assumptions are stated
- [ ] Curve narrative matches data source
- [ ] Visual remains readable at presentation distance
