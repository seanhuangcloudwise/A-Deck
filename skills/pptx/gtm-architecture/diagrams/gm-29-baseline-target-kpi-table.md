# GM-29: Baseline vs Target KPI Table - GTM Diagram Spec

Ref: KPI commitment tables | Outcome contracting practices

## 1. Purpose and When to Use
Definition: A structured table comparing baseline KPI values with post-adoption targets and expected delta.
Use when: value alignment, executive agreement, success plan definition.
Questions answered: What changes, by how much, and by when?
Primary audience: PMM, finance, customer success, executives.

## 2. Visual Layout Specification
Variant A (recommended): Columns for KPI, baseline, target, delta, owner, review cadence.
Variant B: Add confidence band and source column.
Variant C: Split table by value stream (efficiency, growth, risk).

**Grid Proportions**:
- 6-column table: 8.5" wide at (0.5", 1.1")
- Column widths: KPI 2.0", Baseline 1.0", Target 1.0", Delta 0.8", Owner 1.2", Cadence 1.0"
- Row height: 28–32pt; header row: 36pt, `#44546A` fill
- Delta cell: optional inline spark bar, max width 0.6"
- Domain separator row: 20pt, light gray fill
- Maximum rows: 16; split by value stream if exceeding

## 3. Color Semantics
Baseline: #A5A7AA
Target: #00CCD7
Delta highlight: #53E3EB
Owner/cadence headers: #44546A

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, header 9pt bold, row text 8.5-9pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Table-based layout, optional spark bars in delta column.
No extra connectors needed.

## 6. Annotation Rules
KPI definitions must be explicit and non-ambiguous.
Baseline date and target period are mandatory.
Add data source and owner per KPI.

## 7. Content Density Rules
Minimum: 5 KPIs.
Optimal: 8-12 KPIs.
Maximum: 16 KPIs then split by domain.

## 8. Anti-Patterns
Target with no baseline.
Mixing KPI units in one column without labels.
No owner or cadence, making table non-operational.

## 9. Industry Reference Patterns
Successful value plans define owner and review cycle per KPI.
Delta presentation should emphasize both absolute and percentage changes.

## 10. Production QA Checklist
- [ ] Baseline and target period are shown
- [ ] KPI units are explicit
- [ ] Owner and cadence columns exist
- [ ] Delta calculation is consistent
- [ ] Source references are present
