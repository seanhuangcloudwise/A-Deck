# GM-12: Customer Success Metrics Card — GTM Diagram Spec

_Ref: SiriusDecisions (Forrester) Customer Evidence Standards | SaaS Social Proof Best Practices | G2 Case Study Format | Gartner Peer Insights_

---

## 1. Purpose & When to Use

**Definition**: A structured single or multi-card slide presenting quantified customer outcome data — typically from case studies, survey results, or pilot deployments — as a scannable proof-of-value exhibit.

**Use When**:
- Adding social proof to a solution brief or white paper
- Creating the "Proven Results" or "Customer Outcomes" section of a pitch deck
- Responding to "Do you have references in our industry?" during sales cycles
- Building a leave-behind card for field sales to share after a meeting

**Questions Answered**:
- Has this product been proven with customers like us?
- What actual outcomes did real customers achieve?
- What metrics improved, by how much, within what timeframe?

**Primary Audience**: Business decision makers, IT buyers doing peer validation, Procurement, CFO-level economic buyers

---

## 2. Visual Layout Specification

**Structure**: One or more "metric proof cards" each containing: customer context + key metric + outcome statement.

### Variant A: 3-Up Metric Cards (Recommended)
- Three cards in a row: each represents one outcome theme
- Each card: large metric value (center) + outcome label + customer segment profile
- Consistent card size, spacing: 8pt gutter
- Best for: pitch deck, solution brief, email one-pager

### Variant B: Featured Case Study Card (Full slide)
- Single large card structure: customer profile badge + 3 KPI metrics + quote + logo area
- Left sidebar: customer profile (industry, size, use case)
- Right content: 3 metrics prominently displayed + 1–2 sentence outcome
- Bottom: testimonial quote (attributed to role, not name if confidential)
- Best for: white paper case study section, sales leave-behind

### Variant C: Metric Matrix (Multiple customers)
- Rows = customers (with anonymized profile), columns = metric dimensions
- Cell: specific number or "N/A"
- Best for: analyst briefing, competitive RFP response

**Grid Proportions**:
- Variant A card width: equal spread; height: 120–140pt
- Variant B card: full content area
- Metric value font size: 24–32pt
- Customer profile badge: 80pt × 32pt (top left of card)

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Metric value | Primary outcome number | `#00CCD7` bold |
| Customer profile badge | Industry/size context | `#44546A` bg, white |
| Card background | Success proof context | White |
| Card header band | Theme name | `#00CCD7` tint |
| Quote text | Customer testimony | `#2F2F2F` italic |
| Industry icon | Sector identifier | `#A5A7AA` |
| Time-to-value chip | Deployment timeline | `#53E3EB` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Customer Outcomes / [Industry] Examples" | 14pt | Regular |
| Metric Value | Headline number | 24–32pt | Bold, `#00CCD7` |
| Metric Label | What the number measures | 9pt | Regular, `#A5A7AA` |
| Customer Profile | "Global bank, 20K employees" | 9pt | Regular, white on `#44546A` |
| Outcome Statement | 1-line result description | 10pt | Regular |
| Quote | Verbatim testimonial | 9pt | Italic, `#2F2F2F` |
| Footnote | Source, anonymization note | 7pt | Regular, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect card | Success proof unit |
| Header band | Card theme label |
| Large number text | Headline metric (not a shape — text only) |
| Profile badge | Customer anonymized descriptor |
| Quote bubble | Optional testimonial container |
| Brand color divider | Metric separation line |

**Connector Rule**: No connectors between cards. Each card is independent proof.

---

## 6. Annotation Rules

- **Anonymization rule**: If customer name is confidential, use "Global [Industry] Company, [Size] employees" format. Never invent fictitious company names.
- **Metric precision**: Match precision to claim size — "35%" not "34.7%" for broad estimates; use exact figures only if from a formal study.
- **Methodology note**: Footnote must indicate how metrics were measured: customer self-reported, platform analytics, third-party audit.
- **Baseline note**: The denominator matters — "50% faster" must cite baseline: "vs. previous manual process / previous vendor / industry benchmark."
- **Replication caveat**: Add "Results vary by implementation" or "Median of surveyed customers" — prevents individual outliers from creating misleading impressions.

---

## 7. Content Density Rules

| Mode | Cards | Metrics per Card | Per Slide |
|---|---|---|---|
| Minimum | 1 | 1 | — |
| Optimal | 3 | 1–2 | 1 slide |
| Maximum | 6 | 3 | → 2 slides |

---

## 8. Anti-Patterns

1. **Logo wall without metrics**: Row of customer logos with no outcome data — proves adoption but not value. Logo walls belong in a different slide; this diagram exists for metric proof.
2. **"Up to X%" framing**: "Up to 90% improvement" for a best-case outlier — "up to" framing is distrusted by experienced buyers. Use median or typical range.
3. **Fabricated metrics**: Outcome cards with numbers that are not traceable to any customer evidence — immediate credibility destruction if challenged.
4. **No baseline**: "2× faster" without stating what the baseline was — a percentage or multiple is meaningless without a denominator.
5. **No profile context**: Metrics from an unnamed, unqualified customer in an unspecified scenario — buyers need to know if they're "like" the reference customer before trusting the outcome.

---

## 9. Industry Reference Patterns

**G2 Case Study Format**:
G2's case study template requires: Challenge → Solution → Results, with Results always in quantified form (specific metric + % improvement + time period). G2's platform shows that case studies with 3+ specific numeric outcomes convert at 2.4× the rate of text-only stories. The metric card format extracts the "Results" section for standalone use in deck slides.

**Forrester Customer Evidence Standards**:
Forrester's customer evidence framework classifies evidence by strength: Primary research (commissioned study) > Secondary research (public case study) > Self-reported (customer survey) > Anecdotal (quota). For enterprise B2B, the minimum bar is "verifiable self-reported with named customer segment" — anonymous metrics from unspecified customers do not qualify as Forrester-grade evidence.

**SiriusDecisions Social Proof Ladder**:
SiriusDecisions' social proof ladder for B2B goes: Reference call > Published case study > Metric card > Quote > Logo — in decreasing persuasiveness. The metric card is recommended as the highest-impact format that doesn't require a named reference interview — maximizing proof value while respecting customer confidentiality. It's the bridge format between "we have unnamed evidence" and "we can put a customer on the phone."

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Every metric has a baseline (vs. what?)
- [ ] Customer profile qualifies the segment (industry + size category)
- [ ] No fabricated or unverifiable metrics
- [ ] Source/methodology footnote present
- [ ] "Results vary" or median/range caveat if needed
- [ ] Anonymization applied correctly (no real names if confidential)
- [ ] Metric precision appropriate (no false precision)
- [ ] Card layout consistent: metric value visually dominant
- [ ] Buyer from same industry segment can identify with at least one card
