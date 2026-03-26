# GM-33: Risk Reduction Heatmap - GTM Diagram Spec

Ref: Risk matrices | Security and operations value framing

## 1. Purpose and When to Use
Definition: A heatmap showing risk exposure before and after adoption across impact and likelihood dimensions.
Use when: risk-focused value storytelling, security/compliance discussions, executive governance.
Questions answered: Which risks are reduced and by how much?
Primary audience: Risk officers, operations leaders, security buyers.

## 2. Visual Layout Specification
Variant A (recommended): 5x5 impact-likelihood matrix with before and after markers.
Variant B: Category heatmap by risk domain and residual score.
Variant C: Heatmap plus cost impact table.

**Grid Proportions**:
- Grid: 5 × 5 cells, total area 4.5" × 4.5" at (2.0", 1.2")
- Cell size: ~65pt × 65pt
- Y-axis label zone: 1.5" left of grid (Impact: Critical → Low, top to bottom)
- X-axis label zone: 0.5" below grid (Likelihood: Rare → Almost Certain, left to right)
- Before marker: filled circle 18pt; After marker: outlined circle 14pt, `#00CCD7` border 2pt
- Reduction arrow: 1pt `#00CCD7` from before to after position
- High-risk cells (upper-right): `#44546A` fill; low-risk (bottom-left): `#A5A7AA` fill
- Color gradient: 5 levels from `#44546A` (highest) through `#53E3EB` to white (lowest)

## 3. Color Semantics
High risk: #44546A
Medium risk: #53E3EB
Low risk: #A5A7AA
Risk reduction highlight: #00CCD7 arrows/labels

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, axis labels 9pt, cell labels 8pt, legend 8pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Grid cells, before/after markers, reduction arrows.
Optional domain tags for risk category.

## 6. Annotation Rules
State scoring rubric (1-5) and owner of scoring.
Show baseline and residual period.
Mark assumptions for projected reductions.

## 7. Content Density Rules
Minimum: 6 key risks.
Optimal: 8-15 risks.
Maximum: 20 risks then split by domain.

## 8. Anti-Patterns
No scoring method.
Only showing reduced risks while hiding unchanged risks.
Mixing qualitative and quantitative scales without note.

## 9. Industry Reference Patterns
Security and operations value decks often use before/after heatmaps.
Residual risk presentation is expected in governance reviews.

## 10. Production QA Checklist
- [ ] Scoring rubric is explicit
- [ ] Before and after markers are both shown
- [ ] Residual period is stated
- [ ] Unchanged/high residual risks are visible
- [ ] Reduction claims are supported
