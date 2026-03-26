# GM-13: GTM Motion Diagram — GTM Diagram Spec

_Ref: Openview Partners PLG Framework | a16z Go-to-Market Motions | Winning by Design Revenue Architecture | SiriusDecisions Demand Waterfall_

---

## 1. Purpose & When to Use

**Definition**: A strategic diagram showing how the product enters and expands in a market — indicating the primary sales motion (PLG / SLG / CLG / Partner-led), channel mix, expansion triggers, and the customer acquisition-to-expansion lifecycle.

**Use When**:
- Building a GTM strategy section for an investor deck or board presentation
- Internally aligning product, marketing, and sales on the go-to-market model
- Briefing analysts on growth strategy and channel priorities
- Communicating to channel partners how they fit in the GTM motion

**Questions Answered**:
- How does this product reach new customers (acquisition)?
- What drives expansion from initial land to full platform adoption?
- What is the role of marketing, sales, and product in each stage?
- Where is the primary growth lever — product virality, direct sales, or partners?

**Primary Audience**: CEO, CRO, CMO, Investors, Channel Partners, Internal GTM teams

---

## 2. Visual Layout Specification

**Structure**: Horizontal lifecycle flow showing acquisition → land → expand → renew, with motion type and stage owners annotated.

### Variant A: Land-and-Expand Funnel with Motion Labels (Recommended)
- Stages: Awareness → Interest → Trial/POC → Land → Expand → Advocate
- Above each stage: primary motion owning it (Marketing / Product / Sales / CS)
- Below each stage: channel or mechanism (Web / Demo / Self-serve / AE / CSM)
- Best for: investor deck, executive alignment, board update

### Variant B: PLG + SLG Dual-Motion Flow
- Two parallel swim lanes: PLG lane (product-led) / SLG lane (sales-led)
- PLG lane: self-serve sign-up → product activation → viral loop → expansion
- SLG lane: outreach → demo → POC → close → handoff to CS
- Conversion arrows between lanes (PLG → SLG hand-raise)
- Best for: hybrid GTM model disclosure to investors or analysts

### Variant C: Revenue Architecture Bow-Tie
- Left side (funnel): Awareness → Qualified Lead → Close
- Center: Customer (the value delivery node)
- Right side (expansion): Adoption → Expansion → Advocacy
- Best for: Winning by Design / Customer Success-centric businesses

**Grid Proportions**:
- Stage block: 88pt × 56pt
- Stage arrow gap: 16pt
- Owner label height: 24pt above stage blocks
- Channel label height: 24pt below stage blocks

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Marketing-owned stage | Demand generation | `#53E3EB` |
| Product-owned stage (PLG) | Product-led growth | `#00CCD7` |
| Sales-owned stage | Sales-led conversion | `#44546A` |
| CS-owned stage | Customer success | `#B9F2F6` |
| Expansion arrow | Revenue growth trigger | `#00CCD7` bold |
| Motion type label | PLG / SLG / CLG badge | `#2F2F2F` bg, white |
| Hand-raise transition | PLG → SLG conversion | Dashed arrow, `#44546A` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "GTM Motion: [Company/Product]" | 14pt | Regular |
| Stage Label | Phase name | 10pt | Bold |
| Owner Label | Function responsible | 9pt | Regular, `#A5A7AA` |
| Channel Label | Mechanism below stage | 8pt | Regular, italic |
| Motion Badge | PLG / SLG / CLG label | 8pt | Bold, white |
| Metric Annotation | Conversion rate or volume | 8pt | SemiBold, `#00CCD7` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Stage block (rect) | Funnel/lifecycle stage |
| Motion badge (pill) | PLG/SLG/CLG label |
| Horizontal arrow | Forward stage progression |
| Curved return arrow | Renewal / advocacy loop |
| Dashed arrow | Optional / conditional flow |
| Bracket (top/bottom) | Owner/channel grouping |

---

## 6. Annotation Rules

- **Conversion rate annotations**: Add key conversion metrics where known ("3% trial → paid", "T+90d expansion trigger") as small annotations on stage transitions.
- **Motion type badge**: Each stage should state whether the motion is product-led, sales-led, or partner-led via a badge.
- **Time-to-stage labels**: "Avg T+14d to activation" on the PLG stages shows investors the product velocity.
- **Expansion trigger definition**: The expansion stage must note what triggers expansion upsell (usage threshold / feature unlock / renewal event).

---

## 7. Content Density Rules

| Mode | Stages | Per Slide |
|---|---|---|
| Minimum | 4 | — |
| Optimal | 6–7 | 1 slide |
| Maximum | 9 | → split by acquisition / expansion |

---

## 8. Anti-Patterns

1. **PLG label without evidence**: Claiming PLG motion without showing a self-serve path or product activation mechanism — PLG requires a reproducible product-led acquisition loop.
2. **Sales-only funnel**: A traditional marketing funnel without any CS/expansion stage — signals to investors that there is no land-and-expand strategy.
3. **No owner assignment**: GTM motion without naming which team owns each stage — this is a picture, not a strategy.
4. **Missing hand-off definition**: Not showing how leads and customers transfer between PLG and SLG motions (or between Sales and CS) — these handoffs are where most GTM failures occur.
5. **Too many motions for stage 1**: PLG + SLG + Partner all running from day 1 on a slide for a 30-person company — investors will challenge resource focus.

---

## 9. Industry Reference Patterns

**Openview Partners PLG Framework**:
Openview's PLG framework defines three types of PLG motion: Freemium (free tier → paid conversion), Free Trial (time-limited → paid), and Usage-Based (consumption → contract). Each type has different funnel metrics and expansion triggers. The PLG diagram should indicate which type is in use and show the conversion mechanism explicitly.

**Winning by Design Revenue Architecture**:
Winning by Design introduced the "bow-tie" model as an alternative to the funnel — the left side is acquisition (marketing/sales), the center is the customer, the right side is expansion (CS/account management). The insight is that for subscription businesses, 80%+ of lifetime revenue comes from the right side of the bow-tie — GTM investment should be balanced accordingly.

**SiriusDecisions (Forrester) Demand Waterfall**:
The SiriusDecisions Demand Waterfall tracks demand from Inquiry → MQL → SAL → SQL → Won → Adopted → Expanded. The 2019 "Demand Unit Waterfall" update added the "Demand Unit" concept — recognizing that B2B buying is done by groups, not individuals. The GTM motion diagram should reflect whether the product's acquisition unit is individual, team, or enterprise.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Acquisition stage clearly separated from expansion stage
- [ ] Primary GTM motion (PLG/SLG/CLG) is labeled
- [ ] Each stage has an owner (Marketing/Product/Sales/CS)
- [ ] Expansion trigger is named (usage threshold, event, renewal)
- [ ] Conversion rates or time-to-stage annotations present if known
- [ ] Hand-off between motions or teams is shown explicitly
- [ ] Renewal/advocacy loop shown for subscription products
- [ ] Stage count is 6–7 (not more)
- [ ] CRO/CMO can explain the primary growth lever in 30 seconds from this slide
