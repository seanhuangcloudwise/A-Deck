# GM-25: Feature Proof Card - GTM Diagram Spec

Ref: Sales proof card practices | Evidence-based product messaging

## 1. Purpose and When to Use
Definition: A compact card format that ties one feature claim to one measurable result and one proof artifact.
Use when: sales deck proof slides, one-pagers, analyst backup appendix.
Questions answered: What claim is made, what result proves it, and where is evidence?
Primary audience: Sales, PMM, analyst relations.

## 2. Visual Layout Specification
Variant A (recommended): 3-up cards per slide, each card with Claim / Metric / Evidence / Scope.
Variant B: Single hero proof card for flagship feature.
Variant C: Proof matrix with confidence scoring.

**Grid Proportions**:
- 3-up card layout starting at (0.55", 1.1"); card gap: 0.2"
- Card size: 2.6" × 3.8"
- Claim strip: full card width, 32pt height, `#44546A` fill, white text
- Metric badge: 80pt × 36pt, centered within card, `#00CCD7` bold value
- Evidence note area: bottom 1.0" of card, 8pt text
- Scope tag: pill shape below evidence, `#53E3EB` fill, 7pt text

## 3. Color Semantics
Claim strip: #44546A
Metric highlight: #00CCD7
Evidence tag: #53E3EB
Unverified placeholder: #A5A7AA

## 4. Typography Hierarchy
Title 28pt, subtitle 14pt, claim 10pt bold, metric 18pt bold, evidence note 8pt, footnote 7pt.

## 5. Shape and Connector Vocabulary
Card container, metric badge, evidence chips, optional confidence icon.
No connectors required unless using matrix variant.

## 6. Annotation Rules
Metric must include baseline and time window.
Evidence must state source type (customer report, telemetry, benchmark).
Include applicability scope (segment, environment, scale).

## 7. Content Density Rules
Minimum: 1 card.
Optimal: 3 cards.
Maximum: 6 cards then split by capability cluster.

## 8. Anti-Patterns
Claim with no metric.
Metric with no source or scope.
Using vanity metric unrelated to buyer concern.

## 9. Industry Reference Patterns
Strong proof cards mirror analyst evidence standards.
Best sales assets combine concise claim with traceable proof.

## 10. Production QA Checklist
- [ ] Each card includes claim, metric, and evidence
- [ ] Metric has baseline and period
- [ ] Source type is explicit
- [ ] Scope constraints are stated
- [ ] No unsupported superlatives
