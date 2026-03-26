# GM-19: Feature Differentiation Radar - GTM Diagram Spec

Ref: Competitive radar visualization patterns | Product positioning comparisons

## 1. Purpose and When to Use
Definition: A radar chart comparing product feature strength versus named alternatives across selected buyer-relevant dimensions.
Use when: sales pitch, competitive positioning, analyst brief, executive summary.
Questions answered: Where are we clearly stronger? Where are we parity or weaker?
Primary audience: Sales, PMM, strategy.

## 2. Visual Layout Specification
Variant A (recommended): Single radar with 6-8 axes, our product plus 2-3 competitors.
Variant B: Split radar (core features vs enterprise governance) on two charts.
Variant C: Weighted radar with confidence marker per axis.
Axis naming should reflect buyer language, not internal component names.

**Grid Proportions**:
- Chart area: 7.5" × 4.0", starting at (1.0", 1.2")
- Axis label column: 1.5" left; bars extend rightward
- Bar height per dimension: 20pt; gap between dimension groups: 16pt
- Product line colors differentiated; own product bar first (cyan)
- Legend: bottom-right, 2.0" × 0.3"
- Alternative (if radar): polygon inscribed in 3.5" diameter circle, centered

## 3. Color Semantics
Our product line: #00CCD7 thick line and filled alpha.
Competitors: #A5A7AA, #44546A, and light gray.
Highlight zone: light cyan for strategic strength area.

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, axis labels 8.5-9pt, legend 8pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Radial axes, polygon lines, optional score point markers.
No unrelated callout arrows unless clarifying one key differentiator.

## 6. Annotation Rules
Mandatory: scoring methodology and scale definition in footnote.
Mandatory: date stamp and source type (self-assessment, analyst, customer data).
Optional: confidence score per axis.

## 7. Content Density Rules
Minimum: 5 axes.
Optimal: 6-8 axes and up to 4 products.
Maximum: 10 axes; beyond this move to matrix format.

## 8. Anti-Patterns
Cherry-picked axes designed only for one-sided win.
No scoring rubric, making the radar non-defensible.
Using too many competitors causing unreadable overlap.

## 9. Industry Reference Patterns
Gartner-like comparisons emphasize clear axis definitions and methodology notes.
Winning battlecards limit dimensions to buyer decision criteria.
Use consistent scale to avoid visual distortion.

## 10. Production QA Checklist
- [ ] Axis names are buyer-relevant
- [ ] Scale and scoring method are shown
- [ ] Competitor names and date are explicit
- [ ] Our strengths and gaps are both visible
- [ ] Radar remains readable at presentation distance
