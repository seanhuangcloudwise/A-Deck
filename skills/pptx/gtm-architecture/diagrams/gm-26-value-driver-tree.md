# GM-26: Value Driver Tree - GTM Diagram Spec

Ref: McKinsey Value Driver Tree | Forrester TEI value mapping

## 1. Purpose and When to Use
Definition: A hierarchical tree that links product capabilities to operational outcomes and then to financial impact.
Use when: business case building, executive value narrative, procurement defense.
Questions answered: How does each capability translate into business and financial value?
Primary audience: Finance, PMM, executive sponsors.

## 2. Visual Layout Specification
Variant A (recommended): 3-level tree (Capability -> Operational Driver -> Financial Outcome).
Variant B: 4-level tree with KPI layer.
Variant C: Split tree by value streams (cost, revenue, risk).

**Grid Proportions**:
- 3-column tree layout at (0.4", 1.1"), total area 9.0" × 4.5"
- Column 1 (Capability): x = 0.4", node width 2.2"
- Column 2 (Operational Driver): x = 3.2", node width 2.2"
- Column 3 (Financial Outcome): x = 6.0", node width 2.5"
- Node height: 44pt; vertical gap between nodes: 16pt
- Branch connector: 1.5pt, `#A5A7AA`, horizontal with right-angle bends
- Quantified KPI label on connector: 7pt, `#00CCD7`

## 3. Color Semantics
Capability nodes: #53E3EB
Operational drivers: #00CCD7
Financial outcomes: #44546A
Assumption nodes: #A5A7AA

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, node title 9.5-10pt bold, node detail 8.5pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Rounded nodes and directional connectors with optional weight labels.

## 6. Annotation Rules
Each branch should include one quantified KPI or formula.
Assumptions must be marked and traceable.
Show value period (monthly, annualized, 3-year).

## 7. Content Density Rules
Minimum: 3 branches.
Optimal: 5-8 branches.
Maximum: 12 branches then split by value stream.

## 8. Anti-Patterns
Unquantified branches.
Mixing outputs and outcomes in same level.
No financial endpoint.

## 9. Industry Reference Patterns
Best practice links each value branch to owner metric.
TEI-style mapping improves procurement credibility.

## 10. Production QA Checklist
- [ ] Capability-to-outcome chain is complete
- [ ] KPI or formula exists per major branch
- [ ] Assumptions are explicit
- [ ] Time period is consistent
- [ ] Financial outcomes are buyer-relevant
