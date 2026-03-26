# GM-23: Feature Adoption Funnel - GTM Diagram Spec

Ref: Product analytics funnel practices | PLG activation frameworks

## 1. Purpose and When to Use
Definition: A funnel that tracks user progression from feature exposure to frequent advanced usage.
Use when: product ops review, value proof, CS enablement, launch retrospective.
Questions answered: Where does adoption drop? Which step blocks realized value?
Primary audience: Product ops, CS, PMM, growth teams.

## 2. Visual Layout Specification
Variant A (recommended): 5-stage funnel (Exposed, Tried, Activated, Repeated, Advanced).
Variant B: Cohort funnel by segment.
Variant C: Funnel plus intervention panel (recommended actions per drop-off stage).

**Grid Proportions**:
- Funnel centered at x = 1.5", starting at y = 1.1"
- Top (widest) stage width: 6.5"; bottom (narrowest): 2.5"
- Stage height: 52pt each; vertical gap: 4pt
- Total funnel height: ~4.2"
- Conversion rate label: right of each stage gap, 1.5" wide
- Intervention panel (Variant C): 2.5" × 4.0" right of funnel

## 3. Color Semantics
Healthy conversion: #00CCD7
Warning drop stage: #A5A7AA
Intervention highlight: #53E3EB

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, stage label 9-10pt bold, conversion metric 11-12pt bold, footnote 7pt.

## 5. Shape and Connector Vocabulary
Trapezoid funnel stages, down arrows between stages, optional annotation badges.

## 6. Annotation Rules
Include denominator definition and measurement window.
Show both count and conversion rate at each stage.
Mark major drop stage with likely cause and action.

## 7. Content Density Rules
Minimum: 4 stages.
Optimal: 5 stages.
Maximum: 7 stages; otherwise split by journey phase.

## 8. Anti-Patterns
No denominator or timeframe.
Only percentages without absolute counts.
Comparing different segments without normalized definitions.

## 9. Industry Reference Patterns
PLG teams use activation and retained usage as key milestones.
Best practice combines data funnel with intervention guidance.

## 10. Production QA Checklist
- [ ] Stage definitions are explicit
- [ ] Counts and rates both shown
- [ ] Time window and source are present
- [ ] Drop-off stage includes action note
- [ ] Metrics align with product analytics terms
