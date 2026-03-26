# GM-18: Feature Capability Matrix - GTM Diagram Spec

Ref: Product Capability Matrix patterns | Kano Model | Enterprise RFP response templates

## 1. Purpose and When to Use
Definition: A matrix that lists core product features by module, maturity, and scenario coverage to show complete capability scope at a glance.
Use when: product overview, solution brief, pre-sales capability confirmation, and RFP response summary.
Questions answered: What features exist? Which are GA/Beta/Planned? Which scenarios are covered now?
Primary audience: Product marketing, pre-sales, procurement evaluators.

## 2. Visual Layout Specification
Variant A (recommended): Rows as feature modules, columns as capability, maturity, scenario, and proof reference.
Variant B: Grouped table with module section headers and weighted importance score column.
Variant C: Heatmap matrix where color intensity shows capability depth.
Recommended density: 8-16 rows per slide, split by module if over 16.

**Grid Proportions**:
- Table area: full content width (8.5"), starting at y = 1.1"
- Column widths: Module 1.8", Capability 2.2", Maturity 1.0", Scenario 2.0", Proof 1.5"
- Row height: 28–32pt; header row: 36pt, bold, `#44546A` fill
- Module group separator row: 20pt height, dark background
- Maximum rows per slide: 16; split into two slides by module if exceeding

## 3. Color Semantics
GA: #00CCD7; Managed/Beta: #53E3EB; Planned: #A5A7AA; Header: #44546A; text: #2F2F2F.

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, table headers 9-10pt bold, cell text 8.5-9pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Primary shape: structured table cells with row group bars.
No decorative connectors. Optional marker icons only for maturity or risk flags.

## 6. Annotation Rules
Include evaluation date and maturity definition in footnote.
Each row should include at least one scenario or user role tag.
Add evidence id for important claims (for example E1, E2).

## 7. Content Density Rules
Minimum: 6 feature rows.
Optimal: 10-14 rows.
Maximum: 20 rows then split to two slides by module.

## 8. Anti-Patterns
Feature dumping without scenario mapping.
Mixing roadmap promises with GA features without explicit label.
Using internal engineering terminology not understood by buyers.

## 9. Industry Reference Patterns
Kano-inspired framing distinguishes table stakes and delighters.
Enterprise battlecards commonly include maturity and evidence columns.
Best practice is capability + scenario + proof in one row.

## 10. Production QA Checklist
- [ ] Title/subtitle use placeholder idx=0/1
- [ ] Maturity legend is explicit
- [ ] Each capability maps to a scenario or role
- [ ] Key claims have evidence reference
- [ ] No ambiguous roadmap statements
