# GM-21: Feature Depth Ladder - GTM Diagram Spec

Ref: Capability maturity ladders | Product sophistication narratives

## 1. Purpose and When to Use
Definition: A ladder that shows how one capability evolves from basic support to advanced closed-loop intelligence.
Use when: differentiating against parity competitors, showcasing product depth.
Questions answered: How deep is this capability and why it matters for outcomes?
Primary audience: CTO office, pre-sales, technical buyers.

## 2. Visual Layout Specification
Variant A (recommended): 4-level vertical ladder (L1 Basic, L2 Managed, L3 Automated, L4 Intelligent).
Variant B: Horizontal maturity track with evidence chips under each level.
Variant C: Dual ladder comparing our depth versus typical alternatives.

**Grid Proportions**:
- Ladder block total: 5.5" wide, centered horizontally at x = 1.75"
- Level height: 72pt each; vertical gap: 8pt
- Level width (all equal): 5.5"; color intensity increases upward
- Level label: left 1.5" within block; capability text: remaining width
- Side evidence badge: 1.8" wide panel right of ladder at x = 7.5"
- Arrow (upward): 24pt tall, centered to left of ladder blocks

## 3. Color Semantics
L1: #A5A7AA
L2: #53E3EB
L3: #00CCD7
L4: #44546A with white text

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, ladder level title 10-11pt bold, detail text 8.5-9pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Stacked rounded rectangles and upward arrows.
Optional side badges for evidence and customer impact.

## 6. Annotation Rules
Every level needs capability statement plus business implication.
At least one level should include measurable evidence.
If competitor comparison is used, include source basis.

## 7. Content Density Rules
Minimum: 3 levels.
Optimal: 4 levels.
Maximum: 5 levels; beyond this readability drops.

## 8. Anti-Patterns
Only technical terms, no business implication.
Skipping middle maturity levels.
Calling planned features as current top-level depth.

## 9. Industry Reference Patterns
Maturity ladders are common in platform and automation storytelling.
Best practice: show progression logic and measurable payoff at upper levels.

## 10. Production QA Checklist
- [ ] Level names reflect true maturity
- [ ] Each level has capability and impact text
- [ ] Upward progression is logical and defensible
- [ ] Top level includes evidence or named customer outcome
- [ ] No roadmap disguised as GA
