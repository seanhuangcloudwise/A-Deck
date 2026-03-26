# GM-17: Analyst Briefing Framework — GTM Diagram Spec

_Ref: Gartner Vendor Briefing Program | Forrester Vendor Inquiry Format | IDC Vendor Assessment | 451 Research Briefing Standards_

---

## 1. Purpose & When to Use

**Definition**: A structured visual framework summarizing the company's analyst briefing narrative — organized around market context, product differentiation, customer proof, and forward vision — designed to support a 30–45 minute analyst briefing and leave behind as a reference document.

**Use When**:
- Preparing for a Gartner, Forrester, IDC, or 451/S&P briefing
- Building the annual analyst relations (AR) narrative deck
- Creating a structured company overview for media/press briefings
- Onboarding a new AR lead on the core briefing story

**Questions Answered**:
- What is the market context we're briefing the analyst on?
- What problem do we solve, and why is the market ready now?
- What makes our approach differentiated (product and company)?
- What is the vision for our category and our product roadmap?

**Primary Audience**: CMO, CEO, AR team, Senior PMM, Communications leads

---

## 2. Visual Layout Specification

**Structure**: A structured 5-section briefing narrative layout used as a briefing deck overview page.

### Variant A: Five-Section Briefing Arc (Recommended)
- Section 1: Market Context — size, growth, key trends driving category
- Section 2: Problem Statement — the specific problem the category addresses
- Section 3: Product Differentiation — what makes our approach unique
- Section 4: Customer Evidence — representative customer proof (tier / segment / outcomes)
- Section 5: Vision & Roadmap — where the category and product are heading
- Layout: horizontal timeline flow or stacked card structure
- Best for: briefing overview slide, AR leave-behind summary

### Variant B: Analyst Evaluation Readiness Grid
- Rows: Analyst evaluation criteria (completeness of vision / ability to execute / etc.)
- Columns: own product response to each criterion
- Evidence cell: data point or reference supporting the response
- Best for: pre-MQ or pre-Wave preparation; internal readiness assessment

### Variant C: Message House for Analysts
- Top: Corporate positioning statement (1 sentence)
- Three pillars: Market leadership / Product innovation / Customer proof
- Foundation: Market context / Company background
- Best for: message consistency alignment across multiple analyst briefings

**Grid Proportions**:
- Variant A: 5 sections, each 17% width; total: full content width
- Section header band: 32pt height; content area: 80pt height
- Variant B grid: criteria column 160pt; response column: remaining

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Section 1: Market Context | Background | `#44546A` bg, white text |
| Section 2: Problem | Pain framing | `#A5A7AA` |
| Section 3: Differentiation | Solution narrative | `#00CCD7` |
| Section 4: Customer Evidence | Proof | `#53E3EB` |
| Section 5: Vision | Forward-looking | `#44546A` dark |
| Evaluation ready ✓ | Strength area | `#00CCD7` chip |
| Gap area | Needs work | `#A5A7AA` dashed |
| Evidence citation | Reference marker | 7pt italic |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Analyst Briefing Arc / [Analyst Firm]" | 14pt | Regular |
| Section Label | Nav header | 10pt | Bold, White |
| Section Content | Key message bullets | 9pt | Regular |
| Proof Point | Data / customer reference | 9pt | SemiBold |
| Vision Statement | Forward claim | 10pt | Italic, `#2F2F2F` |
| Footnote | Confidentiality / version note | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Section band | Briefing narrative section |
| Numbered section header | Arc position indicator |
| Evidence chip | Customer proof reference |
| Vision arrow | Forward direction indicator |
| Grid rows + cells (Variant B) | Evaluation criterion responses |
| Message house pyramid (Variant C) | Hierarchy of messages |

---

## 6. Annotation Rules

- **Analyst audience note**: At the top or subtitle, note which analyst firm/program this brief is for ("Gartner Magic Quadrant inquiry / Forrester Wave"). Different firms have different emphases.
- **Confidentiality label**: "Confidential — Prepared for Analyst Briefing. Not for distribution." in footer.
- **Evidence qualification**: Any customer reference in Section 4 must be authorized for use in analyst contexts (some customers authorize press use but not analyst briefings).
- **Roadmap caveat**: Section 5 vision items that are not GA must be labeled "Roadmap / Not GA" — analysts enforce this rigorously and violations damage trust.
- **Version / date**: Briefing arcs change quarterly — include "Briefing Narrative v2.1 / Q1 2026" in footer.

---

## 7. Content Density Rules

| Mode | Sections | Key Points per Section | Per Slide |
|---|---|---|---|
| Minimum | 4 | 2 | — |
| Optimal | 5 | 3 | 1 overview slide + detail slides |
| Maximum | 6 | 5 | split into arc overview + section detail slides |

---

## 8. Anti-Patterns

1. **Briefing deck = marketing deck**: Using a customer-facing pitch deck for an analyst briefing — analysts expect market analysis, technical depth, and unvarnished competitive honesty; marketing optimization destroys credibility.
2. **Roadmap without GA distinction**: Describing future capabilities in the present tense — analysts track this across briefings and will cite discrepancies in published research.
3. **No customer names / no proxy metrics**: Section 4 with vague "customers in financial services" without any metrics or reference — analysts need evidence tiers (named customer, named but metric-only, or sector-qualified metric).
4. **Competitive avoidance**: Not addressing the primary 2–3 competitors — analysts ask about them; not being prepared looks like a weakness.
5. **Oversized vision claims**: "We will own 30% of the $50B market in 5 years" without a believable path — analysts publish skeptical commentary on unsupported claims.

---

## 9. Industry Reference Patterns

**Gartner Vendor Briefing Program**:
Gartner accepts vendor briefings as the primary input for MQ research. A briefing must cover: Company overview (ARR, headcount, geo) → Product capabilities (features, roadmap) → Differentiation (vs. named alternatives) → Customer base (count, segment, retention/NRR) → Strategy (vision, M&A, partnerships). Gartner analysts rate vendors on "Completeness of Vision" AND "Ability to Execute" — the briefing framework must evidence BOTH, not just product features.

**Forrester Wave Vendor Inquiry**:
Forrester publishes evaluation criteria 90 days before Wave due dates — giving vendors time to prepare evidence. The Forrester Wave scores 20–35 criteria across Current Offering, Strategy, and Market Presence. The briefing framework must map company statements to Forrester's criteria categories, not to internal product naming. Misalignment between how Forrester defines a criterion and how the vendor uses the same term is the most common cause of low scores.

**IDC Vendor Assessment Process**:
IDC's primary analyst product is the MarketScape, which evaluates vendors on Capabilities (product) and Strategy (market). IDC additionally produces "Technology Spotlights" for vendors that are emerging or category-defining. The Technology Spotlight format leads with Market Context → Problem → Vendor Approach → Customer Outcomes — mapping directly to the 5-section briefing arc in Variant A.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Analyst firm/program named in subtitle or footer
- [ ] Section 1 (Market Context) includes market size data with source
- [ ] Section 3 (Differentiation) names at least 2 competitors with specific contrasts
- [ ] Section 4 (Evidence) has at minimum a sector-qualified customer metric
- [ ] Section 5 (Vision/Roadmap) distinguishes GA vs. Roadmap items
- [ ] "Confidential / Not for distribution" present in footer
- [ ] Version and date in footer
- [ ] All roadmap items labeled "Roadmap / Not GA"
- [ ] AR team can complete a 30-minute briefing using this framework without off-script improvisation
