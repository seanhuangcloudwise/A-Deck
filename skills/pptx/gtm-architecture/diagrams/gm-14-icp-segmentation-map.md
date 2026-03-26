# GM-14: ICP Segmentation Map — GTM Diagram Spec

_Ref: MEDDIC / MEDDPICC Sales Methodology | Ideal Customer Profile (ICP) Framework (Salesforce / HubSpot) | SiriusDecisions Target Demand Framework | a16z Market Sizing_

---

## 1. Purpose & When to Use

**Definition**: A visual classification of the target market into customer segments by priority tier — based on fit dimensions such as industry, company size, tech maturity, and buying trigger — enabling sales and marketing to align on whom to pursue first.

**Use When**:
- Building a sales enablement deck that helps reps identify priority accounts
- Aligning product, marketing, and sales on target segment priorities
- Communicating to investors which customer segment the company is winning
- Designing territory plans and account-based marketing programs

**Questions Answered**:
- Which type of customer is the ideal first target?
- Which attributes make a customer more likely to buy, land fast, and expand?
- How should sales prioritize between a startup vs. an enterprise vs. a mid-market account?
- What are the disqualifying signals that say "not a fit"?

**Primary Audience**: Sales leadership, Sales Ops, Marketing, Product Marketing, Investors

---

## 2. Visual Layout Specification

**Structure**: Tiered matrix or segmented priority map showing customer segment clusters by fit score.

### Variant A: Tier Priority Map (Recommended)
- Three horizontal tiers: Tier 1 (Ideal) / Tier 2 (Good Fit) / Tier 3 (Possible Fit)
- Each tier: list of qualifying attributes (industry, size, tech stack, trigger event)
- Color coded: T1 = brand cyan, T2 = light, T3 = gray
- Best for: sales enablement, territory planning, investor deck segment slide

### Variant B: 2×2 Fit-Urgency Matrix
- X-axis: Strategic Fit (Low → High)
- Y-axis: Buying Urgency / Trigger (Low → High)
- Customer segment circles plotted in quadrants
- Own product's sweet-spot: upper-right quadrant
- Best for: portfolio prioritization, ABM target selection

### Variant C: Attribute Grid
- Rows: Customer segments (by industry or company size)
- Columns: Fit dimensions (10–12 criteria)
- Cells: Score or ✓ / ~ / ✗
- Similar to GM-05, but for customer segments rather than competitors
- Best for: detailed ICP scoring documentation

**Grid Proportions**:
- Variant A tier height: 90pt each; attribute list: 4–6 bullets per tier
- Variant B axis: 4.5" × 3.5" quadrant area; segment circles: 24–36pt diameter
- Tier label badge on left: 80pt × 28pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Tier 1 — Ideal | Best fit, highest priority | `#00CCD7` |
| Tier 2 — Good Fit | High fit, pursue actively | `#53E3EB` |
| Tier 3 — Possible | Qualified, lower priority | `#D9EEF2` |
| Out of ICP | Disqualified segment | `#A5A7AA` |
| Qualifying attribute chip | Specific characteristic | White, `#2F2F2F` border |
| Trigger event badge | Buying signal | `#44546A` bg, white |
| Urgency marker | Time-bounded opportunity | `#00CCD7` bold |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "ICP Segmentation — [Market / Geo]" | 14pt | Regular |
| Tier Label | T1 / T2 / T3 | 11pt | Bold, white |
| Attribute Label | Qualifying dimension name | 9pt | Regular |
| Attribute Value | E.g., "500–5000 employees" | 9pt | SemiBold |
| Trigger Event | Buying signal description | 9pt | Bold, `#44546A` |
| Disqualifier Note | "Not for: [segment]" | 8pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Horizontal band | Tier container |
| Attribute chip | Qualifying criterion block |
| Trigger badge (pill) | Buying signal indicator |
| Segment circle (Variant B) | Customer cluster on matrix |
| ✓ / ✗ / ~ cell (Variant C) | Fit scoring cell |
| "Not ICP" zone | Out-of-scope segment marker |

**Connector Rule**: No connectors between tiers — vertical stacking implies priority order.

---

## 6. Annotation Rules

- **Tier population estimate**: Add "~N accounts in TAM" or "X% of total pipeline" per tier if data is known.
- **Trigger event examples**: List 2–3 specific trigger events per tier (e.g., "Cloud migration underway", "Post-funding >$30M Series B", "Compliance requirement due in 90 days").
- **Disqualifier list**: Add an explicit "Not a fit if…" section or strip — prevents wasted sales cycles.
- **Rep action note**: Per tier, add a "Rep action" line: "Tier 1: AE + SDR + executive outreach / Tier 2: SDR sequence + demo" — makes the segmentation actionable.
- **Data source**: Note if tiers are based on empirical win/loss data or a hypothesis ("Based on 87 closed-won deals FY2025").

---

## 7. Content Density Rules

| Mode | Tiers | Attributes per Tier | Per Slide |
|---|---|---|---|
| Minimum | 2 | 3 | — |
| Optimal | 3 | 5–7 | 1 slide |
| Maximum | 4 | 10 | → split into T1-T2 slide and T3-disqualifiers slide |

---

## 8. Anti-Patterns

1. **Only positive fit attributes**: An ICP with only "who to pursue" and no "who to avoid" — reps will waste cycles on poor-fit accounts that superficially match the positive criteria.
2. **Revenue-only segmentation**: "Tier 1 = > $1B revenue" — revenue is a proxy, not a fit signal. Use behavioral and situational attributes (cloud-first, digital project active, compliance trigger).
3. **No trigger events**: ICP without buying triggers fails to help prioritize which accounts are in-market NOW vs. abstractly fitting the profile.
4. **Too granular**: 12 tiers with 20 attributes each — create a decision tree, not a diagram.
5. **Misaligned tiers**: Sales pursuing Tier 3 accounts at the same intensity as Tier 1 — the map must be tied to rep action instructions to be operational.

---

## 9. Industry Reference Patterns

**MEDDIC / MEDDPICC Methodology**:
MEDDIC defines a qualified opportunity by: Metrics (economic impact), Economic Buyer (decision maker access), Decision Criteria (evaluation standards), Decision Process (buying steps), Identify Pain (specific business pain), Champion (internal advocate). The ICP segmentation map pre-qualifies which customer segments are most likely to exhibit all six MEDDIC signals — saving reps from investing in deals that cannot close.

**Salesforce / HubSpot ICP Framework**:
Both Salesforce and HubSpot advocate building ICP from empirical closed/won data: take the last 50 best customers, identify common attributes (industry, size, tech stack, trigger, champion profile), and reverse-engineer the ideal profile. The ICP segmentation map should therefore be validated by win-rate data, not hypotheses. Segments with confirmed >40% win rates qualify as Tier 1.

**a16z Market Sizing**:
Andreessen Horowitz's investment memos require segment-level TAM breakdowns — not just total market size. The ICP segmentation map maps directly to this: Tier 1 accounts represent the SAM (Serviceable Addressable Market), Tier 2 the broader TAM, and Tier 3 the hypothetical TAM with product evolution. This framing helps both investors and internal strategy teams align on near-term vs. long-term targeting logic.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Three tiers clearly distinguished by color and criteria
- [ ] Each tier has qualifying attributes AND trigger events
- [ ] Explicit "Not ICP / Disqualifier" section present
- [ ] Rep action guidance per tier (even 1 line)
- [ ] Data source for tier criteria noted (empirical vs. hypothesis)
- [ ] Account count estimate or pipeline % per tier (if known)
- [ ] Tiers are distinguished by behavioral / situational signals, not just demographics
- [ ] No tier has > 8 attributes (use appendix for full scoring)
- [ ] Sales leader can use this to qualify or disqualify an account in 60 seconds
