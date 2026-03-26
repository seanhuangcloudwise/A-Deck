# GM-01: Positioning Statement Diagram — GTM Diagram Spec

_Ref: Geoffrey Moore《Crossing the Chasm》Positioning Template | April Dunford《Obviously Awesome》| SiriusDecisions Messaging Framework_

---

## 1. Purpose & When to Use

**Definition**: A structured visual that renders the product's positioning statement — who the target is, what pain they have, what the product does, and why it's different from alternatives — in a diagram format readable without narration.

**Use When**:
- Opening a white paper, pitch deck, or solution brief with precise positioning
- Aligning internal teams (product, marketing, sales) on the single positioning message
- Explaining what the product is and isn't to analyst or press audiences
- Differentiating from a crowded competitive set with a self-defined frame

**Questions Answered**:
- Who exactly is this product for?
- What specific problem does it solve that alternatives do not?
- What is the key differentiating mechanism?
- What category does this product belong to (or create)?

**Primary Audience**: Product Marketing Manager, CMO, Sales Enablement, Board/Investor audiences

---

## 2. Visual Layout Specification

**Structure**: Structured statement rendered as connected semantic blocks — not prose.

### Variant A: Chain Block (Recommended for pitches)
- 5 horizontally connected blocks: Target → Problem → Product → Differentiator → Category
- Each block: label (role name, 9pt) + value text (12pt, bold)
- Connector arrows linking target → problem → product → differentiator → category
- Best for: pitch deck opening, one-liner alignment

### Variant B: Diamond/Cross Layout (for white paper intro page)
- Center: Product name (large, 18pt)
- Top: Category ("We are a…")
- Left: Target ("For…")
- Right: Differentiator ("Unlike…, we…")
- Bottom: Proof claim ("Proven by…")
- Best for: white paper cover section, press one-pager

### Variant C: Table-Structured Statement (for analyst briefing)
- Two-column table: Label | Content
- Rows: Category / Target Segment / Problem / Solution / Key Differentiator / Proof Point
- Best for: Gartner/Forrester analyst briefing packets

**Grid Proportions**:
- Variant A chain block width: 120pt each, height: 64pt, gap: 20pt
- Variant B diamond center: 120pt × 60pt; satellite blocks: 100pt × 48pt
- Variant C row height: 32pt; label column: 120pt; content column: remaining width

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Target block | Who is the buyer/user | `#53E3EB` light |
| Problem block | Pain being solved | `#A5A7AA` light gray |
| Product block | Our solution name/claim | `#00CCD7` brand cyan |
| Differentiator block | Unique mechanism | `#44546A` dark |
| Category block | Market category label | White with `#00CCD7` border |
| Connector arrow | Statement flow | `#2F2F2F` dark |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular |
| Block Label | Role label above block (e.g., "Target") | 8pt | Regular, `#A5A7AA` |
| Block Content | Statement fragment | 11–12pt | SemiBold |
| Connector Label | "For / Who / Unlike / We" | 8pt | Italic, `#A5A7AA` |
| Footnote | Source / method note | 7pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect (small radius) | Statement segment block |
| Solid directional arrow | Statement logical flow |
| Label chip above block | Segment role identifier |
| Bold border rect | Product/solution block (focal point) |
| Diamond center | Product identity hub (Variant B) |

**Connector Rule**: Arrows show the logical flow of the positioning statement. Direction is always Target → Problem → Solution → Differentiator → Category.

---

## 6. Annotation Rules

- **Confidence level note**: Add a footnote if the positioning is early-stage or hypothesis ("Positioning v1.2 — under validation")
- **Segment qualifier**: Add industry + company size qualifier in the Target block (e.g., "Mid-market SaaS / 200–2000 employees")
- **Differentiator evidence**: The differentiator block should link to a proof point — add a small citation number if evidence is on an adjacent slide
- **"Not for"** strip: Optional mini-row or badge listing "Not for: [out-of-scope segments]" — prevents scope creep in sales

---

## 7. Content Density Rules

| Mode | Blocks | Statement Words | Per Slide |
|---|---|---|---|
| Minimum | 3 | 20 total | — |
| Optimal | 5 | 30–50 total | 1 slide |
| Maximum | 7 | 80 | → 2-slide split: statement + evidence |

**Single slide rule**: Positioning Statement Diagram must fit on one slide. If evidence is needed, it goes on a subsequent slide.

---

## 8. Anti-Patterns

1. **Prose paragraph disguise**: Writing the positioning statement as running prose and wrapping it in a box — this fails the 30-second scanability test.
2. **Superlative target**: "All enterprises" or "any company with software" — positioning must be specific enough to make someone feel excluded.
3. **Technology differentiator**: "Our differentiator is Rust-based performance" for a business audience — differentiators must be business impact, not stack choices.
4. **Category = generic**: "Enterprise software" as the category — must define a specific named category.
5. **No "unlike" contrast**: A positioning without naming what it is different from has no anchor for buyer memory.

---

## 9. Industry Reference Patterns

**Geoffrey Moore's Positioning Template**:
"For [target customer] who [has this need/problem], [product name] is a [product category] that [key benefit]. Unlike [primary competitive alternative], our product [primary differentiation statement]." Moore's framework forces specificity on three axes: segment, alternative, and mechanism. The diagram version renders this as a scannable chain rather than a sentence.

**April Dunford《Obviously Awesome》Context Framing**:
Dunford argues the most powerful positioning reframes the competitive context rather than just listing features. Her five-component framework: Competitive Alternatives → Unique Attributes → Value → Target Segments → Market Category. The diagram should render these five in a way that shows how each component constrains and sharpens the others.

**SiriusDecisions (Forrester) Messaging House**:
SiriusDecisions structures messaging from the top: the "Corporate Claim" (single overarching value statement), then "Pillars" (3 supporting themes), then "Proof Points" per pillar. The positioning statement diagram is the foundation layer below the Corporate Claim — it establishes WHO before WHAT.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Target segment is specific (industry + size/stage qualifiers)
- [ ] Differentiator is stated as business impact, not technology feature
- [ ] Category name is a defined, named category (not generic)
- [ ] "Unlike" alternative is named or described (even implicitly)
- [ ] Statement fits 30-second read by target audience
- [ ] No prose paragraphs — content in structured blocks only
- [ ] Color semantics match role of each block (Target/Problem/Solution/Diff/Category)
- [ ] Footnote includes version or validation status
- [ ] Presenter can recite the full statement from the diagram without notes
