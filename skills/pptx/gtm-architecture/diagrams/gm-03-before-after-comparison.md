# GM-03: Before/After Comparison Diagram — GTM Diagram Spec

_Ref: SaaS Sales Storytelling Best Practices | Intercom / Drift / Figma Pitch Patterns | SPIN Selling (Neil Rackham)_

---

## 1. Purpose & When to Use

**Definition**: A side-by-side visual contrasting the customer's current state (pain, fragmentation, cost, risk) with the future state enabled by the product — making the value delta visceral and immediate.

**Use When**:
- Opening a sales pitch with immediate buyer recognition of their pain
- Justifying investment by making the "cost of doing nothing" visible
- Replacing prose problem statements with a scannable visual
- Summarizing the solution story in a single slide for an exec audience

**Questions Answered**:
- What does the customer's world look like without this product?
- What specifically gets better, faster, or cheaper with it?
- How dramatic is the before-to-after transformation?

**Primary Audience**: Sales, Pre-Sales, Solution Architects, End-buyer executives who need to justify purchase

---

## 2. Visual Layout Specification

**Structure**: Two-panel layout, left = Before (current state), right = After (with product).

### Variant A: Split Panel with Pain/Gain Cards (Recommended)
- Left panel (Before): `#A5A7AA` / warm gray background; 3–5 pain cards
- Right panel (After): `#00CCD7` / brand cyan background; 3–5 gain cards
- Center divider: vertical line with a transformation icon or arrow
- Best for: sales opener, pitch deck problem/solution slide pair

### Variant B: Before/After Table Comparison
- Rows = specific dimensions (e.g., Time to Resolve, # of Tools, Error Rate)
- Left column = with old approach (red / gray value)
- Right column = with product (green / cyan value)
- Delta column = % improvement or absolute change
- Best for: procurement defense, RFP response, business case slides

### Variant C: Emotional Journey Contrast
- Left: journey illustration (chaos, manual steps, missed signals)
- Right: simplified journey (automated, connected, visible)
- Icons replace text for executive audiences
- Best for: conference keynote, executive summary

**Grid Proportions**:
- Split: 48% / 4% / 48% (left panel / divider / right panel)
- Card height: 44–56pt; 3 cards per panel minimum
- Transformation glyph in center: 24×24pt arrow or ⚡

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Before panel background | Current-state problem zone | `#F5F5F5` light gray |
| After panel background | Future-state success zone | `#E6FAFB` light cyan tint |
| Before pain card | Specific pain instance | White with `#A5A7AA` border |
| After gain card | Specific gain instance | White with `#00CCD7` border |
| Transformation divider | Change marker | `#00CCD7` |
| Metric delta chip | Improvement quantifier | `#00CCD7` bg, white text |
| Problem icon/emoji | Visual anchor for pain | `#A5A7AA` |
| Gain icon | Visual anchor for outcome | `#00CCD7` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular |
| Panel Header | "Before" / "After" | 16–18pt | Bold |
| Card Title | Primary pain/gain name | 11–12pt | SemiBold |
| Card Body | 1–2 line descriptor | 9pt | Regular |
| Delta Chip | "↓40% time" | 9pt | Bold, white |
| Footnote | Source for any metric | 7pt | Regular, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large rounded rect | Panel container (Before/After) |
| Small rounded rect | Individual pain/gain card |
| Transformation arrow/glyph | Center change symbol |
| Metric chip (pill shape) | Quantified improvement badge |
| Icon glyph (optional) | ⚠ for pain, ✓ for gain |

**Connector Rule**: No connectors between Before and After panels — the delta is communicated through visual contrast, not explicit arrows.

---

## 6. Annotation Rules

- **Panel labels**: "Before" (without product / current state) and "After" (with product / future state) must be explicitly labeled — do not assume audience will infer
- **Metric deltas**: Every gain card should carry a metric delta chip if data is available ("3 weeks → 2 hours", "↓60% cost", "+35 NPS")
- **Source note**: Metrics in the After panel must cite their source (customer data / analyst study / internal benchmark) in a 7pt footnote
- **Industry qualifier**: Add "(Mid-market SaaS)" or similar segment qualifier near the panel headers to scope the claims

---

## 7. Content Density Rules

| Mode | Cards per Panel | Total Words | Per Slide |
|---|---|---|---|
| Minimum | 2 | 40 | — |
| Optimal | 3–4 | 60–80 | 1 slide |
| Maximum | 6 | 120 | → split into 2 Before/After slides by theme |

---

## 8. Anti-Patterns

1. **Before panel with no empathy**: Listing "Before: no tool" without naming the pain — must describe what the customer experiences, not just the absence of the product.
2. **After panel = feature list**: "After: AI-powered, cloud-native, scalable" — After must describe business outcomes, not product attributes.
3. **Symmetric layouts with no visual hierarchy**: Both panels should not have equal visual weight — "After" panel should feel lighter, more spacious, more positive.
4. **No metrics**: A Before/After without any quantified delta is a storytelling assertion, not evidence. At least two metrics required.
5. **Overpromising the "after"**: Claims in the After panel that are not achievable for the target segment reduce credibility rather than increasing interest.

---

## 9. Industry Reference Patterns

**SPIN Selling (Neil Rackham)**:
SPIN methodology shows that the highest-performing sales conversations progress through Situation → Problem → Implication → Need-payoff. The Before/After diagram is the visual rendering of Implication + Need-payoff: the Before panel makes implications of the problem visible; the After panel demonstrates the need-payoff. Salespeople trained in SPIN use this diagram before any product demo.

**SaaS Sales Deck Patterns (Intercom, Figma, Notion)**:
Analysis of 50+ SaaS pitch decks shows the most effective follow a Problem → Solution → Evidence structure where the "Problem" slide is always a Before/After split — not a bullet list. The left panel uses red or gray tones to evoke pain; the right uses the brand primary color to indicate relief. Viewers recall visual contrast 4× more effectively than prose problem statements.

**McKinsey Change Story Framework**:
McKinsey's "change story" structure for executive presentations always begins with "the burning platform" — what happens if nothing changes — before presenting the solution path. The Before/After diagram renders this as a single page: left column shows the burning platform; right column shows the safe future state enabled by the recommended action.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Both panels are explicitly labeled ("Before" / "After")
- [ ] Before panel describes customer experience, not absence of product
- [ ] After panel describes business outcomes, not product features
- [ ] At least 2 quantified metric deltas with sources cited
- [ ] Visual contrast is clear: Before = gray/heavy; After = light/brand cyan
- [ ] Segment qualifier scopes the claims to prevent overpromising
- [ ] Icon or glyph visually distinguishes pain vs gain cards
- [ ] No connectors between panels (contrast carries the message)
- [ ] Presenter can name top 3 pains and gains from memory in 20 seconds
