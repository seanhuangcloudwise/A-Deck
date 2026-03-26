# GM-34: Proof Evidence Ladder - GTM Diagram Spec

Ref: Evidence hierarchy frameworks | Analyst-grade claim confidence models

## 1. Purpose and When to Use
Definition: A ladder ranking proof quality from anecdotal claims to independently validated evidence.
Use when: analyst briefing, enterprise trust building, claim governance.
Questions answered: How strong is our evidence for each key claim?
Primary audience: PMM, AR, enterprise buyers.

## 2. Visual Layout Specification
Variant A (recommended): 5-level ladder (Assertion, Internal Data, Customer Data, Third-party Benchmark, Independent Validation).
Variant B: Ladder per claim cluster.
Variant C: Ladder plus coverage matrix by product capability.

**Grid Proportions**:
- 5 stacked blocks centered horizontally, starting at y = 1.2", total height ~4.5"
- Block widths (bottom L1 to top L5): 8.0", 6.8", 5.5", 4.2", 3.0"
- Block height: 64pt each; vertical gap: 6pt
- Block labels: left-aligned within block, 10pt bold
- Evidence examples: right column, 2.5" wide, 8.5pt text
- Upward progression arrow: 24pt wide, `#00CCD7`, left of ladder
- Confidence badge (per claim): 8pt colored circle at block right edge

## 3. Color Semantics
Low evidence levels: #A5A7AA
Mid levels: #53E3EB
High confidence levels: #00CCD7 and #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, level title 9.5pt bold, evidence examples 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Stacked ladder blocks with upward progression arrow.
Optional confidence badges.

## 6. Annotation Rules
Each level should include accepted evidence examples.
Claims should reference current evidence level.
Add gap note for high-priority claims lacking strong evidence.

## 7. Content Density Rules
Minimum: 4 levels.
Optimal: 5 levels with 1-2 examples each.
Maximum: 6 levels then simplify labels.

## 8. Anti-Patterns
Treating internal anecdote as independent proof.
No linkage between claims and evidence levels.
Too many labels causing unreadable ladder.

## 9. Industry Reference Patterns
Analyst briefings favor transparent evidence maturity.
Evidence ladders help prevent overclaiming in GTM content.

## 10. Production QA Checklist
- [ ] Levels are clearly defined
- [ ] Claims are tagged with evidence level
- [ ] Examples per level are concrete
- [ ] Evidence gaps are visible
- [ ] Messaging avoids unsupported certainty
