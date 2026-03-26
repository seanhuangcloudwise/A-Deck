# GM-24: Feature Release Timeline - GTM Diagram Spec

Ref: Product launch timeline practices | Release governance communication

## 1. Purpose and When to Use
Definition: A timeline showing completed, in-progress, and planned feature deliveries aligned with GTM milestones.
Use when: roadmap communication, launch planning, stakeholder expectation setting.
Questions answered: What was delivered, what is next, and when value-facing milestones occur?
Primary audience: Product, sales enablement, marketing, leadership.

## 2. Visual Layout Specification
Variant A (recommended): Quarterly horizontal timeline with three swimlanes (Delivered, In Progress, Planned).
Variant B: Milestone-based timeline by launch wave.
Variant C: Timeline plus dependency markers across teams.

**Grid Proportions**:
- Timeline axis: full content width (8.5") at y = 2.5", line weight 1.5pt
- Quarter markers: equal intervals along axis; label 8.5pt below axis
- Swimlane card: 100pt × 40pt; positioned above or below axis by status
- Milestone dot: 14pt diameter on axis; label 8.5pt
- Delivered cards above axis (cyan fill); Planned cards below (gray dashed)
- Card gap: 8pt minimum horizontal

## 3. Color Semantics
Delivered: #00CCD7
In progress: #53E3EB
Planned: #A5A7AA dashed border
Critical launch milestone: #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, milestone label 9pt bold, detail 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Timeline axis, milestone nodes, swimlane cards, dependency arrows.
Use dashed connectors for conditional dependencies.

## 6. Annotation Rules
Each feature should show status and confidence.
Planned milestones require assumption note.
Mark customer-facing launch versus internal readiness separately.

## 7. Content Density Rules
Minimum: 6 milestones.
Optimal: 8-14 milestones.
Maximum: 18 milestones then split by release train.

## 8. Anti-Patterns
Mixing commitment and aspiration in one style.
No distinction between GA and preview.
Overloaded timeline with unreadable labels.

## 9. Industry Reference Patterns
Effective launch timelines separate product readiness and GTM readiness.
Confidence-coded milestones reduce over-commitment risk.

## 10. Production QA Checklist
- [ ] Delivered/in-progress/planned are visually distinct
- [ ] GA/Preview labels are explicit
- [ ] Timeline period is clear
- [ ] Dependencies are only shown when material
- [ ] Roadmap caveat note is present
