# GM-10: ROI / Business Case Frame Diagram — GTM Diagram Spec

_Ref: Forrester TEI (Total Economic Impact) Methodology | Gartner Business Value Framework | McKinsey Business Case Structure | IDC Business Value White Paper_

---

## 1. Purpose & When to Use

**Definition**: A structured visual model showing the investment-to-outcome chain — from product investment (cost) through efficiency/risk gains (benefits) to measurable financial outcomes — enabling CFO-level justification of purchase.

**Use When**:
- Building a business case section in a solution brief or white paper
- Supporting procurement approval by making ROI visual
- Responding to "prove the ROI" objections in enterprise deals
- Summarizing a commissioned TEI (Total Economic Impact) study

**Questions Answered**:
- What are the measurable financial benefits of this product?
- How long before we see payback?
- How do the benefits compare to the total investment?
- What risks does the investment avoid?

**Primary Audience**: CFO, Finance team, IT budget owners, Procurement, Economic buyers in enterprise deals

---

## 2. Visual Layout Specification

**Structure**: Input-output chain showing cost → benefit categories → top-line financial outcome.

### Variant A: Waterfall Investment-to-Benefit (Recommended)
- Left: Investment (license + implementation + training)
- Center: Benefit categories (time savings / risk reduction / revenue acceleration)
- Right: Net financial outcome (NPV / payback period / ROI %)
- Connecting flow arrows left to right
- Best for: executive summary of TEI study, solution brief business case page

### Variant B: Benefit Category Breakdown Cards
- 3–4 horizontal benefit cards: each showing category name + metric + $ value
- Total aggregate at bottom right
- Timeline label: "Year 1 / Year 3 / Year 5" benefit accumulation
- Best for: detailed business case, procurement review

### Variant C: Payback Curve Point Graphic
- X-axis: Time (quarters)
- Y-axis: Cumulative cost vs cumulative benefit
- Lines cross = payback point (annotated)
- Best for: CFO audiences, high-investment enterprise deals

**Grid Proportions**:
- Variant A flow: 3 zones, each 28% width; connectors 4%
- Benefit card: 150pt × 80pt
- ROI outcome badge: 80pt × 48pt, bold border

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Investment block | Cost inputs | `#A5A7AA` |
| Time savings benefit | Efficiency gain | `#53E3EB` |
| Risk reduction benefit | Avoided cost | `#00CCD7` |
| Revenue acceleration | Growth benefit | `#44546A` |
| Net outcome metric | Total financial result | `#00CCD7` bold bg |
| Cost lines (chart) | Investment curve | `#A5A7AA` dashed |
| Benefit lines (chart) | Benefit curve | `#00CCD7` solid |
| Payback marker | Break-even point | `#2F2F2F` diamond |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "3-Year Business Case / TEI Summary" | 14pt | Regular |
| Benefit Category Label | Card header | 11pt | Bold |
| Metric Value | Key number ($, %, months) | 14–16pt | Bold, `#00CCD7` |
| Metric Description | What the number means | 9pt | Regular |
| ROI Headline | Overall ROI result | 20–24pt | Bold, white on cyan |
| Footnote | "Based on [source] / assumptions in appendix" | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Block with flow arrow | Investment → Benefit stage |
| Metric card | Individual benefit category |
| ROI result badge (bold) | Final headline number |
| Line chart (optional) | Cost vs. benefit over time |
| Diamond annotation | Payback period marker |
| Bracket (right side) | Aggregation of individual benefits |

---

## 6. Annotation Rules

- **Source mandatory**: All financial figures must cite their source — "Forrester TEI study 2024 / n=6 enterprise customers / median values" in 7pt footnote.
- **Customer size qualifier**: ROI figures should be qualified with customer profile ("Applicable to enterprises 500–5000 employees").
- **Assumption note**: Add "Key assumptions" annotation or appendix reference for major input variables.
- **Confidence brackets**: For estimated (vs. measured) figures, add ±% range rather than point estimates.
- **Time period**: All financial benefits must specify over what time period (e.g., "3-year NPV", "Year 1 savings").

---

## 7. Content Density Rules

| Mode | Benefit Categories | Per Slide |
|---|---|---|
| Minimum | 2 | — |
| Optimal | 3–4 | 1 slide |
| Maximum | 6 | → split: executive summary + detailed breakdown |

---

## 8. Anti-Patterns

1. **Unverifiable headline ROI**: "350% ROI" with no source, methodology, or customer profile — economic buyers ask "for who / under what assumptions" and will dismiss unsupported claims.
2. **Only cost savings**: ROI models showing only cost reduction miss revenue-side benefits (faster time to market, increased capacity) that often have larger impact.
3. **Overly complicated waterfall**: 15-step calculation chain in one slide — simplify to 3–4 benefit categories with a footnote reference to the detailed model.
4. **Missing payback period**: CFOs care about time-to-payback, not just total ROI — always include both.
5. **Generic numbers": "Customers save 40% time" from an unspecified survey of unspecified customers — the benefit must be qualified by customer type.

---

## 9. Industry Reference Patterns

**Forrester Total Economic Impact (TEI) Methodology**:
Forrester's TEI framework structures value in four components: Benefits (operational efficiency, risk reduction, revenue acceleration), Flexibility (optionality value of the platform), Risks (probability adjustment on benefit estimates), Costs (license, implementation, training, opportunity). This produces a risk-adjusted NPV, payback period, and ROI %. The TEI is the gold standard for enterprise software business cases — a self-published ROI model should follow the same structure even if not commissioned.

**Gartner Business Value Framework**:
Gartner identifies three types of business value evidence: Cost reduction (hard savings), Business enablement (productivity, cycle time), and Strategic value (competitive advantage, optionality). The framework prescribes that financial benefits be mapped to measurable KPIs (not assumptions) — benefit categories must map to metrics the customer already tracks.

**McKinsey Business Case Structure**:
McKinsey's business case always separates "Base case" (keep doing what you're doing) from "Target case" (with investment). The delta between the two cases is the business case value. For GTM slides, this translates to the Before/After framework applied to financial metrics: baseline cost/risk profile vs. improved profile with product.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] All financial figures have cited source and customer profile qualifier
- [ ] Both payback period AND total ROI are shown
- [ ] Benefit categories cover both efficiency (cost) and enablement (revenue) dimensions
- [ ] Time period specified for all financial claims (Year 1 / 3-year NPV)
- [ ] Key assumptions noted (appendix reference acceptable)
- [ ] "Not audited / based on self-reported customer data" disclaimer if applicable
- [ ] Confidence brackets on estimated (vs. measured) values
- [ ] CFO can find the headline ROI number in under 5 seconds
- [ ] Presenter can defend the top benefit category with one customer example
