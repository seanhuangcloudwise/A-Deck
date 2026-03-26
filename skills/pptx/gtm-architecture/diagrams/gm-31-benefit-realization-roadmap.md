# GM-31: Benefit Realization Roadmap - GTM Diagram Spec

Ref: Benefit realization management | PMO value delivery plans

## 1. Purpose and When to Use
Definition: A phased roadmap connecting initiatives to expected benefits and KPI checkpoints over time.
Use when: post-sale planning, executive steering, transformation storytelling.
Questions answered: Which value arrives in which phase, and how progress is governed?
Primary audience: CS, PMO, transformation sponsors.

## 2. Visual Layout Specification
Variant A (recommended): Timeline with phases (Foundation, Adoption, Optimization, Scale), each with benefit milestones.
Variant B: Swimlane roadmap by function (IT, Ops, Business).
Variant C: Milestone map with benefit confidence trend.

**Grid Proportions**:
- Timeline bar: full content width (8.5") at y = 1.1", height 4pt, `#A5A7AA`
- Phase columns: equal distribution (typically 4 phases, each ~2.0" wide), gap 0.15"
- Phase header bar: 2.0" × 0.4", `#44546A` fill, white text 10pt bold
- Phase content area: 2.0" × 3.5" below header
- Milestone node: 14pt diameter on timeline; KPI badge: 80pt × 24pt below node
- Dependency arrow: 1pt dashed, `#A5A7AA`

## 3. Color Semantics
Phase headers: #44546A
Benefit milestones: #00CCD7
Dependency milestones: #53E3EB
Risk flags: #A5A7AA

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, phase labels 10pt bold, milestone text 8.5-9pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Timeline bars, milestone nodes, dependency arrows.
Optional KPI checkpoint badges per phase.

## 6. Annotation Rules
Each phase needs owner, KPI checkpoint, and expected benefit statement.
Dependencies should be explicitly marked when value is contingent.
Show confidence level per milestone.

## 7. Content Density Rules
Minimum: 3 phases.
Optimal: 4-5 phases with 2-3 milestones each.
Maximum: 6 phases then split by workstream.

## 8. Anti-Patterns
Roadmap only listing activities, not benefits.
Missing KPI checkpoints.
No ownership per phase.

## 9. Industry Reference Patterns
Benefit roadmaps are stronger when value milestones are tied to adoption milestones.
Executive steering decks often require confidence and dependency cues.

## 10. Production QA Checklist
- [ ] Each phase includes value milestone
- [ ] KPI checkpoints are visible
- [ ] Owner and dependencies are shown
- [ ] Confidence labeling is present
- [ ] Timeline units are explicit
