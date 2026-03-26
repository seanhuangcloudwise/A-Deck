# GM-22: Unique Mechanism Diagram - GTM Diagram Spec

Ref: Product moat storytelling | Technical differentiation diagrams

## 1. Purpose and When to Use
Definition: A mechanism diagram that explains why the product can deliver unique outcomes through a specific technical or process design.
Use when: explaining defensibility, analyst briefing, deep-dive product pages.
Questions answered: What is unique, how it works, and why alternatives struggle to replicate it?
Primary audience: Technical buyers, analysts, strategy teams.

## 2. Visual Layout Specification
Variant A (recommended): Input -> Engine -> Decision -> Action -> Feedback loop.
Variant B: Layered mechanism stack with data, model, orchestration, governance.
Variant C: Side-by-side mechanism comparison (ours vs conventional flow).

**Grid Proportions**:
- Flow block: 120pt × 56pt each; corner radius ≤ 6pt
- Arrow gap between blocks: 24pt horizontal
- Feedback loop arrow: 40pt radius, positioned above or below the main flow
- Total flow area: full content width (8.5"), vertically centered
- Critical control point block: 1.5pt `#44546A` border, slight scale-up (130pt × 60pt)
- Proof annotation badge: pill shape, 80pt × 20pt, `#53E3EB` fill

## 3. Color Semantics
Core mechanism blocks: #00CCD7
Supporting blocks: #53E3EB
Conventional path: #A5A7AA
Critical control point: #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, block title 9.5-10pt bold, block detail 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Rounded rectangles for components, directional arrows for causality, loop arrow for feedback.
Use labeled connectors for key transformations.

## 6. Annotation Rules
Mark at least one non-obvious control or optimization point.
Attach one proof note to the claimed unique link.
Add assumptions if mechanism relies on specific data quality.

## 7. Content Density Rules
Minimum: 4 mechanism blocks.
Optimal: 5-7 blocks.
Maximum: 9 blocks then split by layer.

## 8. Anti-Patterns
Black-box diagram without causal labels.
Confusing architecture map with mechanism narrative.
Uniqueness claim without evidence.

## 9. Industry Reference Patterns
High-conviction product narratives show mechanism, not only outcomes.
Defensible diagrams connect unique design to measurable effect.

## 10. Production QA Checklist
- [ ] Causal flow is explicit
- [ ] Unique point is clearly marked
- [ ] At least one claim has proof annotation
- [ ] Diagram avoids unnecessary architecture detail
- [ ] Business implication is stated
