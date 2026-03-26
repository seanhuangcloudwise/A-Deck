# GM-20: Feature to Use Case Mapping - GTM Diagram Spec

Ref: JTBD mapping tables | Solution narrative mapping

## 1. Purpose and When to Use
Definition: A matrix mapping product features to concrete business use cases with support depth labels.
Use when: solution design, vertical pitch, product training, proposal writing.
Questions answered: Which feature supports which use case, and at what depth?
Primary audience: Solution architects, pre-sales, product managers.

## 2. Visual Layout Specification
Variant A (recommended): Rows as use cases, columns as key features, cells marked Full/Partial/None.
Variant B: Swimlane map by journey stage with feature chips per stage.
Variant C: Sector-specific mapping with one slide per industry.

**Grid Proportions**:
- Matrix area: 8.0" × 4.5", starting at (0.5", 1.1")
- Use-case label column: 2.0" wide
- Feature columns: equal distribution of remaining width (typically 6–8 columns)
- Header row: 36pt; data row: 28–32pt
- Support indicator: ● Full (12pt, `#00CCD7`), ◑ Partial (12pt, `#53E3EB`), ○ None (12pt, `#A5A7AA`)
- Roadmap cell: dashed `#A5A7AA` border, white fill

## 3. Color Semantics
Full support: #00CCD7
Partial support: #53E3EB
No support: #A5A7AA
Roadmap: white fill with #A5A7AA dashed border

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, use case row labels 9pt bold, cell labels 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Primary shape: matrix grid with optional stage separators.
Optional connectors: only when one feature spans multiple non-adjacent use cases.

## 6. Annotation Rules
Use case descriptions must include actor and objective.
Each major use case should include one success metric.
Mark roadmap cells with expected quarter.

## 7. Content Density Rules
Minimum: 4 use cases x 4 features.
Optimal: 6-10 use cases x 6-8 features.
Maximum: 12x10 then split by use case cluster.

## 8. Anti-Patterns
Generic use cases without role or context.
Feature names that are too technical for business audience.
Implicit roadmap claims hidden as current support.

## 9. Industry Reference Patterns
JTBD-based mapping improves buyer relevance.
Enterprise RFP responses often use support-depth tables.
High-quality mappings include measurable success criteria.

## 10. Production QA Checklist
- [ ] Use cases are role-specific
- [ ] Support depth legend is visible
- [ ] Roadmap items are explicitly tagged
- [ ] At least one metric appears per key use case
- [ ] Claims are consistent with product maturity
