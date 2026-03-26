# GM-02: Value Pyramid — GTM Diagram Spec

_Ref: Bain & Company "Elements of Value" (HBR 2016) | McKinsey Value Driver Tree | Forrester Business Value Framework_

---

## 1. Purpose & When to Use

**Definition**: A layered pyramid diagram that maps product capabilities to progressively higher levels of value — from functional (what it does) to business (what it improves) to strategic (what it transforms) — enabling communication to mixed audiences from engineers to C-suite.

**Use When**:
- Building the "value" section of a white paper or executive presentation
- Justifying a price premium by showing higher-order value delivery
- Aligning multi-level stakeholder communication in the same deck
- Transitioning a feature-led narrative to an outcome-led one

**Questions Answered**:
- Why should a CIO care about this product (not just their engineering team)?
- How does a feature create business value and ultimately strategic value?
- What is the highest-level claim this product can make?

**Primary Audience**: Pre-Sales, PMM, C-suite pitch decks, investor decks

---

## 2. Visual Layout Specification

**Structure**: Triangular pyramid with 3–4 horizontal tiers, widest at bottom (functional) and smallest at top (strategic/inspirational).

### Variant A: Three-Level Classic (Recommended)
- Level 1 (bottom, widest): Functional Value — features and capabilities
- Level 2 (middle): Business Value — operational improvements, KPIs
- Level 3 (top, apex): Strategic Value — transformation, competitive advantage
- Best for: most enterprise software and platform pitches

### Variant B: Four-Level Extended
- Add Level 0 below: Table Stakes / Qualification — must-haves (parity features)
- Use this to explicitly acknowledge "we meet the baseline, then go further"
- Best for: mature markets with strong incumbents

### Variant C: Paired Pyramid (Stacked Perspective)
- Left pyramid: Customer perspective (pain → gain → transformation)
- Right pyramid: Our product perspective (features → outcomes → mission)
- Aligned tier-by-tier with horizontal connectors
- Best for: high-stakes pitches, enterprise renewal conversations

**Grid Proportions**:
- Full pyramid height: 3.5–4 inches on slide
- Level height ratio: top 20%, middle 35%, bottom 45%
- Level width ratio: top 40%, middle 65%, bottom 90%
- Right-side callouts: specific feature names or data points aligned to each tier

---

## 3. Color Semantics

| Tier | Meaning | Fill Color |
|---|---|---|
| Table Stakes (L0) | Qualification baseline | `#A5A7AA` |
| Functional Value (L1) | Feature capabilities | `#53E3EB` light |
| Business Value (L2) | Operational impact | `#00CCD7` brand |
| Strategic Value (L3) | Transformation / vision | `#44546A` dark |
| Callout bullets (right) | Evidence items per tier | White text on colored strip |
| Connector lines to callouts | Tier to evidence link | `#A5A7AA` dashed |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular |
| Tier Label | Pyramid tier name | 12–14pt | Bold, White |
| Tier Description | Short phrase inside tier | 9–10pt | Regular, White |
| Callout Item | Evidence bullet on right | 9pt | Regular, `#2F2F2F` |
| Tier Axis Label | "Functional / Business / Strategic" | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Trapezoid tiers (stacked) | Value level bands |
| Apex triangle cap | Highest-order value claim |
| Horizontal bracket (right) | Evidence grouping per tier |
| Dashed connector | Tier to callout linkage |
| Small icon (optional) | Visual anchor per tier (tools/people/growth icon) |

**Connector Rule**: Connectors run only from tier to callout items — never between tiers. The pyramid's vertical stacking already implies the bottom-up value chain.

---

## 6. Annotation Rules

- **Tier labels**: Each tier must have a 2–4 word name AND a 1-line description inside, readable at full-slide viewing distance
- **Right callouts**: 2–4 bullets per tier citing specific features, metrics, or customer outcomes
- **Audience markers**: Add small audience tags in top-right corner per tier: "CTO", "CFO", "CEO" — indicating who cares most about this tier
- **Data anchors**: At least one tier should have a quantified claim (e.g., "40% reduction in MTTR")
- **Top-tier differentiator**: The strategic apex must state the unique competitive advantage, not a generic aspiration

---

## 7. Content Density Rules

| Mode | Tiers | Callout Items | Per Slide |
|---|---|---|---|
| Minimum | 2 | 2 per tier | — |
| Optimal | 3 | 3 per tier | 1 slide |
| Maximum | 4 | 4 per tier | split callouts to appendix |

---

## 8. Anti-Patterns

1. **Generic strategic claim**: "Helps with digital transformation" at the apex achieves nothing — the apex must name the specific transformation mechanism.
2. **All features, no outcomes**: Filling all tiers with feature names rather than progressing to business/strategic language — the pyramid becomes a feature list with decoration.
3. **Equal tier widths**: A pyramid where all tiers are the same width loses the visual hierarchy that communicates "higher = rarer and more powerful."
4. **No audience differentiation**: Treating the pyramid as a single-audience artifact — the point is that different stakeholders read at different levels.
5. **Unsubstantiated apex**: A strategic claim at the top tier with no evidence trail from lower tiers — the pyramid logic requires each tier to support the one above.

---

## 9. Industry Reference Patterns

**Bain & Company "Elements of Value" (HBR 2016)**:
Bain's research across 10,000 consumer and B2B buyers identified 40 elements of value organized in a pyramid: Functional (saves time, reduces risk, quality) → Ease of Doing Business (productivity, accessibility) → Individual (design, brand, self-actualization) → Inspirational (social impact, vision). For B2B enterprise software, the top-performing vendors consistently compete on Business + Strategic tiers, not just Functional.

**McKinsey Value Driver Tree**:
McKinsey's value framework links product capabilities to financial outcomes: Feature → Process Efficiency → Revenue/Cost Impact → EBITDA Effect → Enterprise Value. The pyramid renders this chain visually, showing that every feature investment eventually connects to shareholder value — a critical framing for executive justification of new platform investment.

**Forrester Business Value Framework (TEI)**:
Forrester's Total Economic Impact (TEI) methodology structures value in four categories: Benefits (operational gains), Flexibility (optionality value), Risks (avoided downside), Costs. Translating TEI findings into a value pyramid makes the ROI story accessible — the pyramid's tiers map to TEI benefit categories for easier buyer communication.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Bottom tier lists specific functional capabilities (not generic)
- [ ] Middle tier states measurable business outcomes (KPI / metric language)
- [ ] Top tier states a specific, differentiated strategic claim
- [ ] Each tier has at least one quantified data point or customer evidence
- [ ] Audience labels (CTO/CFO/CEO) present per tier
- [ ] Tier widths decrease visually from bottom to top
- [ ] Callout items are right-aligned and connected to correct tier
- [ ] No tier contains generic aspirational language without specifics
- [ ] Presenter can explain each tier in one sentence without looking at notes
