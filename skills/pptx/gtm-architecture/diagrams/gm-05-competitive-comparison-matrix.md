# GM-05: Competitive Comparison Matrix — GTM Diagram Spec

_Ref: G2 Competitor Comparison Format | Battle Card Best Practices (SiriusDecisions / Forrester) | Salesforce vs Competitors Deck Patterns_

---

## 1. Purpose & When to Use

**Definition**: A structured table or grid comparing own product against named competitors across a set of buyer-relevant capability criteria — using ✓ / ✗ / ~ or scoring to make differentiation scannable in seconds.

**Use When**:
- Building a sales battle card for field teams to use in competitive deals
- Responding to RFP/RFI with a concise differentiation summary
- Adding to a product white paper's "Why Us" section
- Briefing analysts or partners on competitive positioning

**Questions Answered**:
- Where do we win vs each competitor?
- Which capabilities are table-stakes vs differentiators?
- What should a salesperson say when a prospect asks "what about Competitor X?"

**Primary Audience**: Sales reps, pre-sales, product marketing, technical evaluators

---

## 2. Visual Layout Specification

**Structure**: Matrix table — rows = capability criteria, columns = vendors (own product first).

### Variant A: ✓/✗/~ Grid (Recommended for battle cards)
- Rows: 8–15 buyer-relevant criteria grouped by theme
- Column 1: Own product (bold header, cyan fill)
- Columns 2–5: Named competitors (gray headers)
- Cells: ✓ (full support), ~ (partial), ✗ (no support)
- Best for: sales enablement, battle cards, 1-page comparison

### Variant B: Scored Evaluation Matrix
- Same structure as Variant A, but cells contain 1–5 score or "High/Med/Low"
- Color-coded: dark cyan = high, light = medium, gray = low/none
- Best for: technical evaluation, RFP response, SE/architect audience

### Variant C: Feature-by-Feature Callout Table
- Rows = product features/capabilities
- 2 columns only: "Ours" vs "Typical alternatives"
- Prose descriptions rather than checkmarks
- Best for: white paper technical section, analyst briefing backup

**Grid Proportions**:
- Criteria column: 180–200pt wide
- Vendor column: 80–100pt wide each
- Row height: 28–32pt
- Group separator row: 20pt, dark background
- Maximum visible without scroll: 15 rows

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Own product column header | Self | `#00CCD7` bg, white text |
| Competitor column headers | Alternative vendors | `#44546A` bg, white text |
| ✓ Full support | Capability present | `#00CCD7` text or chip |
| ~ Partial | Partial / limited | `#A5A7AA` text or dot |
| ✗ Not supported | Absent | `#F5F5F5` bg, `#A5A7AA` × |
| Group separator row | Category header | `#44546A` bg, white text |
| Win zone row | Differentiating criteria | Faint `#E6FAFB` row tint |
| Footnote source citation | Evidence reference | 7pt, gray |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "As of [date], [methodology] evaluation" | 14pt | Regular |
| Vendor Column Header | Product/company name | 10pt | Bold |
| Criteria Label | Row label left column | 9pt | Regular |
| Group Header | Category separator | 9pt | Bold, White |
| Cell Content | ✓ / ~ / ✗ or score | 9–10pt | SemiBold |
| Footnote | Source, date, caveat | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Full table grid | Comparison matrix |
| Filled circle + ✓ | Full capability chip |
| Half-circle + ~ | Partial support chip |
| × marker | Not supported |
| Bold left border on own column | Self-product highlight |
| Group separator bar | Category divider |

**Connector Rule**: No connectors in this diagram — table structure carries all relationships.

---

## 6. Annotation Rules

- **Methodology disclaimer**: "Evaluation methodology: [internal self-assessment / customer survey / public documentation review]. Not independently audited." in footnote.
- **Date stamp**: Competitive landscapes change quarterly — assessment date mandatory.
- **Criteria sourcing**: Criteria should be framed as buyer evaluation criteria, not internal feature names — reflect the language used in RFPs or analyst frameworks.
- **"Ask us about" row**: Optional last row for criteria where own product has a roadmap item not yet GA — label "Roadmap Q3 2026" rather than ✗.
- **Battle card annotation**: For field use, add a "When they say X, you say Y" callout box below the table for top 2–3 objection responses.

---

## 7. Content Density Rules

| Mode | Criteria (Rows) | Competitors (Cols) | Per Slide |
|---|---|---|---|
| Minimum | 5 | 2 | — |
| Optimal | 10–12 | 3–4 | 1 slide |
| Maximum | 20 | 5 | → split by criteria group |

**Overflow Strategy**: Split by criteria group heading onto separate slides; keep own product column consistent across splits.

---

## 8. Anti-Patterns

1. **Only own company gets ✓**: Every row showing own product as ✓ and all competitors as ✗ — this destroys credibility; be selective and accurate.
2. **Feature names as rows**: Criteria like "REST API", "Kubernetes support" — these are implementation details, not buyer criteria. Use "Integration flexibility", "Cloud-native deployment" instead.
3. **Too many competitors**: 7+ competitor columns make the table unreadable on a single slide.
4. **No source for claims**: ✗ markings on competitor cells without methodology cite create legal exposure.
5. **Static table**: Not updating after competitor product updates — a ✗ that becomes ✓ for a competitor and goes unnoticed destroys field trust.

---

## 9. Industry Reference Patterns

**G2 Comparison Format**:
G2's crowd-sourced comparison pages rank vendors by user-reviewed capability scores across 20–40 criteria. The highest-performing vendor pages focus on "satisfaction" scores (ease of use, implementation, support) alongside feature scores — showing that buyers compare along experience dimensions, not just capability lists. Own product matrices should include at least 2–3 experience/service dimensions, not only features.

**SiriusDecisions (Forrester) Battle Card Standard**:
SiriusDecisions' battle card framework recommends: Situation (when to use this card) → Competitor Strength/Weakness → Win/Loss Reasons → Top 5 Objection Handlers. The comparison matrix is the central artifact; the checklist-style ✓/✗/~ format enables a 60-second briefing for a rep before entering a meeting with a competitive prospect.

**Salesforce Competitive Intelligence Practice**:
Salesforce's competitive enablement team publishes weekly-updated BI cards segmented by competitor (HubSpot, Microsoft Dynamics, SAP). Each card leads with a "wins in these situations" scenario, followed by a 10-criterion comparison matrix. Criteria are sourced from actual RFP questions collected from field teams — ensuring relevance to real buying decisions.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Criteria labels reflect buyer evaluation language, not internal product names
- [ ] Own product column clearly distinguished (color/weight)
- [ ] At least 2–3 rows where competitors can win (honest representation)
- [ ] ✓ / ~ / ✗ legend present on slide
- [ ] Assessment date shown in subtitle or footnote
- [ ] Methodology/source disclaimer in footnote
- [ ] 3–5 competitors only (no more)
- [ ] "Battle card" version includes objection handler callouts if for field use
- [ ] Presenter can explain top 3 win criteria vs main competitor in 30 seconds
