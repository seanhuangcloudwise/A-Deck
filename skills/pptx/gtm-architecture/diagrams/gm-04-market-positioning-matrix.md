# GM-04: Market Positioning Matrix — GTM Diagram Spec

_Ref: Gartner Magic Quadrant Methodology | Forrester Wave | Geoffrey Moore Competitive Positioning | Blue Ocean Strategy (Kim & Mauborgne)_

---

## 1. Purpose & When to Use

**Definition**: A 2×2 matrix diagram with self-selected axes that positions the product relative to the competitive landscape — framing the company in its own terms rather than by a third-party analyst's framework.

**Use When**:
- Making competitive differentiation visible in a single glance
- Choosing the two dimensions where the product wins and competitors are weak
- Building a category narrative that compels analyst and press attention
- Showing investors or partners a unique market position

**Questions Answered**:
- What two dimensions matter most to buyers in this market?
- Where do competitors cluster? Where is the white space?
- Can we define the axes such that our quadrant is the only desirable one?

**Primary Audience**: CMO, PMM, Investors, Analysts (analyst briefings), Sales leadership

---

## 2. Visual Layout Specification

**Structure**: Standard 2×2 quadrant with labeled axes; own product positioned in a clearly superior quadrant.

### Variant A: Self-Positioned Quadrant (Recommended)
- X-axis: Dimension 1 (e.g., from "Narrow scope" to "Full platform")
- Y-axis: Dimension 2 (e.g., from "Manual" to "Automated")
- Competitor dots: gray circles with company names; clustered in 1–2 quadrants
- Own product: bold cyan circle; positioned in upper-right (desired quadrant)
- Quadrant names: label each of the 4 quadrants with a 2-3 word descriptor
- Best for: pitch deck, analyst briefing, conference slides

### Variant B: Evaluation Criteria Matrix (Weighted)
- X = Completeness of vision / breadth
- Y = Ability to execute / depth
- Mimics Gartner MQ aesthetics but is self-published (clearly labeled "Internal Assessment")
- Circle size = optional scale indicator (market share / revenue)
- Best for: analyst briefing where Gartner/Forrester has not yet published

### Variant C: Strategy Canvas (Blue Ocean)
- X-axis: List of competing factors (6–10 items evenly spaced)
- Y-axis: Offering level (0–5 scale)
- Multiple lines: one per competitor / own product
- Best for: differentiation workshop outputs, category creation narratives

**Grid Proportions**:
- Quadrant area: 5.5" × 4" minimum
- Axis labels at both ends of each axis (min value / max value)
- Own product dot: 24–32pt diameter; competitor dots: 16–20pt
- Quadrant label text: 9pt, italic, in each quadrant corner

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Own product dot | Self | `#00CCD7` filled circle |
| Competitor dots | Alternative vendors | `#A5A7AA` fill, white text |
| "Winners" quadrant | Where own product sits | Faint `#E6FAFB` background tint |
| Axis lines | Scale indicators | `#2F2F2F` lines |
| Quadrant labels | Zone descriptors | `#44546A`, italic |
| White space zone | Unclaimed opportunity | Dashed `#00CCD7` border outline |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular |
| Axis Min/Max Labels | Scale anchor text | 9pt | Regular, `#2F2F2F` |
| Quadrant Labels | Zone name | 9pt | Italic, `#44546A` |
| Vendor Labels | Company name on dot | 8pt | Regular |
| Own Product Label | Product name | 10pt | Bold, `#00CCD7` |
| Footnote | "Internal self-assessment / not audited" | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Filled circle | Vendor position on matrix |
| Bold-border circle | Own product node |
| Dashed outline rect | White space / opportunity zone |
| Solid cross lines | Quadrant dividers |
| Directional label on axis | Low → High scale |

**Connector Rule**: No connectors between vendor dots. Position implies relationship — explicit arrows create "we beat X" claims that create legal/PR risk.

---

## 6. Annotation Rules

- **"Internal Assessment" disclaimer**: Mandatory for all self-published MQ-style diagrams. "This is an internal self-assessment, not an independent analyst evaluation" in 7pt footnote.
- **Axis choice rationale**: Add a callout or subtitle note explaining why these two axes were chosen (buyer relevance)
- **Own product "why here" label**: Small tooltip or balloon calling out why the product is positioned in this specific quadrant
- **Competitor name handling**: Use competitor names as-is (no nicknames); ensure accuracy; 3–5 competitors maximum
- **Date stamp**: Assessment date in footnote (market positions change quickly)

---

## 7. Content Density Rules

| Mode | Vendors | Per Slide |
|---|---|---|
| Minimum | 3 (own + 2 comp) | — |
| Optimal | 5–7 total | 1 slide |
| Maximum | 10 | → cluster minor competitors as "Others" |

---

## 8. Anti-Patterns

1. **Rigged axes**: Choosing axes where every competitor is in the "bad" quadrant — audiences recognize this as dishonest positioning and it backfires in credibility.
2. **Gartner brand mimicry without disclaimer**: Using visual design identical to Gartner Magic Quadrant without clearly labeling it as a self-assessment — direct IP and reputation risk.
3. **Too many competitors**: 15 competitor dots make the chart unreadable and imply a commodity market.
4. **Undefined axes**: Axis labels like "Better" vs "Worse" or "Strong" vs "Weak" — axes must name the specific dimension with a clear pole.
5. **Circle size = arbitrary**: Varying circle sizes without a stated mapping (e.g., circle = revenue) creates confusion.

---

## 9. Industry Reference Patterns

**Gartner Magic Quadrant**:
Gartner's MQ uses Completeness of Vision (X) and Ability to Execute (Y), producing four zones: Niche Players, Challengers, Visionaries, Leaders. The upper-right "Leaders" quadrant is the coveted position. Companies that appear in the Leaders quadrant see average 15% increase in inbound RFP invitations (Gartner Buyer Survey 2022). The self-published version must be clearly labeled to avoid trademark infringement.

**Forrester Wave**:
Forrester Wave uses a multi-criteria scoring model (30+ criteria) to plot Current Offering (X), Strategy (Y), and bubble size = market presence. Unlike Gartner MQ, Forrester Wave criteria are published in advance, allowing vendors to prepare evidence. The Wave radar chart format is more complex; the simpler 2×2 version is used for vendor-published summaries.

**Blue Ocean Strategy Canvas (Kim & Mauborgne)**:
Rather than positioning within existing dimensions, the Blue Ocean strategy canvas identifies new dimensions where competition is irrelevant. The canvas plots competing factors on the X-axis and offering intensity on Y-axis — showing differentiated curves between incumbents and the innovator's position. Recommended when competing on existing dimensions is unfavorable.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Both axis poles are labeled with specific dimension names
- [ ] Own product is clearly visually distinguishable (bold/branded)
- [ ] 3–7 competitors shown (not more)
- [ ] "Internal self-assessment" disclaimer present in footnote
- [ ] Axes were chosen because they reflect buyer evaluation criteria, not internal preference
- [ ] Axis rationale note or subtitle present
- [ ] Date of assessment shown in footnote
- [ ] No legally risky absolute claims in quadrant labels
- [ ] Presenter can justify placement of own product and 2 largest competitors within 30 seconds
