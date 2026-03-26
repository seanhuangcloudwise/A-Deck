# GM-16: Category Creation Diagram — GTM Diagram Spec

_Ref: Play Bigger《Category Creation》(2016) | Christopher Lochhead Category Design | Andreessen Horowitz "Define Your Category" | Gartner Hype Cycle_

---

## 1. Purpose & When to Use

**Definition**: A visual that establishes a new market category — defining the problem space, naming the category, placing the product as the defining example, and showing why existing alternatives are insufficient — to own analyst and press descriptors before competitors do.

**Use When**:
- Launching a genuinely novel product without an established market category
- Reframing an existing product to escape a crowded, commoditized category
- Briefing analysts to get them to write about the company using the desired category label
- Building the "Category" section of a Series B+ investor deck

**Questions Answered**:
- What new category of problem or solution does this product define?
- Why do existing categories fail to describe what this product does?
- Who are the first companies/buyers to need this new category?
- What would the world look like if this category reaches full market adoption?

**Primary Audience**: CMO, CEO, Analyst Relations, PR team, Series B+ investors

---

## 2. Visual Layout Specification

**Structure**: Visual argument for a new problem space — showing the gap in existing solutions and the position of the new category.

### Variant A: Problem Space Gap Map (Recommended)
- Left cluster: Legacy solutions (with category names) — show what they do well
- Center gap zone: "The unaddressed space" — annotated with the problem description
- Right cluster: Emerging/future-state needs that legacy solutions can't serve
- Own product: centered in the gap zone, with new category name
- Best for: analyst briefing, media pitch, investor deck

### Variant B: Category Landscape Timeline
- X-axis: Time (market maturity / Gartner Hype Cycle phase)
- Y-axis: Buyer awareness / adoption
- Existing categories plotted on the curve (earlier, flatter)
- New category shown as rising line (innovation trigger)
- Own product positioned at the innovation inflection point
- Best for: market timing argument; justifying category creation investment

### Variant C: Venn Diagram Category Intersection
- 3 overlapping circles: Domain A / Domain B / Domain C
- Center intersection = new category definition
- Own product = the intersection realized
- Best for: categories created by combining previously separate domains (e.g., ITSM + AIOps + CMDB → next-generation IT Operations)

**Grid Proportions**:
- Gap zone: central 35% of content area
- Legacy cluster blocks: 2–3 blocks per side; each 80pt × 40pt
- New category label: large, 18pt, centered in gap zone
- Own product badge: 120pt × 40pt, bold `#00CCD7` border

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Legacy solution blocks | Existing category players | `#A5A7AA` |
| Gap zone (unclaimed) | Problem space to own | `#E6FAFB` tint, dashed border |
| New category label | Category naming moment | `#00CCD7` bold text |
| Own product badge | Category definer | `#00CCD7` bg, white text |
| Emerging need items | Future buyer requirements | `#44546A` text, light bg |
| Category boundary | Definition perimeter | Dashed `#2F2F2F` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Defining a new category of [domain]" | 14pt | Regular |
| New Category Name | Center headline | 16–18pt | Bold, `#00CCD7` |
| Legacy Category Labels | Existing solution types | 10pt | Regular, gray |
| Gap Problem Description | What's missing | 10pt | Italic, `#2F2F2F` |
| Own Product Badge | Company/product name | 11pt | Bold, white |
| Footnote | Analyst reference / methodology | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Named block | Legacy category/solution |
| Dashed-border zone | Unclaimed problem space |
| Bold-border badge | Own product as category anchor |
| Arrow (→) | Market direction / evolution |
| Bracket annotation | Category definition boundary |
| Overlap zone (Venn) | Category intersection (Variant C) |

**Connector Rule**: Arrows show market evolution direction (from legacy → new category), not data flows.

---

## 6. Annotation Rules

- **Category name**: The new category label must be a proper noun phrase — not a generic description. "AI-Native IT Operations Platform" not "better ITSM."
- **Category problem statement**: A 1–2 line description of the problem that the new category was created to solve — answer "what was broken that required a new category?"
- **Legacy limitations**: Per legacy block, add 1-line description of what it fails to do that the new category addresses.
- **Analyst acknowledgment**: If any analyst firm has used the category label in published research, cite it ("Gartner identified this as emerging in 2024 IT Infrastructure Hype Cycle").
- **First mover claim**: Add a timeline marker or footnote establishing when own company first used this category label publicly.

---

## 7. Content Density Rules

| Mode | Legacy Blocks | Per Slide |
|---|---|---|
| Minimum | 2 | — |
| Optimal | 3–5 | 1 slide |
| Maximum | 8 | → cluster legacy solutions by type |

---

## 8. Anti-Patterns

1. **Fake category**: Combining two existing product category names with a conjunction — "AI-powered ITSM" is not a new category, it's a feature claim.
2. **No buyer pull**: A category defined by the technology ("vector database observability") rather than the buyer problem — category names must lead with the buyer outcome.
3. **Own product = only member**: A category where only own product qualifies — this signals competitive defensiveness, not market creation.
4. **No legacy acknowledgment**: Ignoring that buyers are already using something — declaring a new category without acknowledging what it replaces looks out of touch.
5. **Category definition too broad**: "The platform for modern companies" — category definition must be specific enough to exclude buyers and focus investment.

---

## 9. Industry Reference Patterns

**Play Bigger《Category Creation》**:
Play Bigger analyzed 100 "category kings" (companies that defined their market) and found they captured 76% of the total market value of their category. The framework: Define the problem (what is the "before" world?) → Name the category → Mobilize the ecosystem (analyst + press + customer) → Scale with category awareness. The diagram should render the "define the problem" phase — visualizing the gap that the category fills.

**Christopher Lochhead Category Design**:
Lochhead argues that the best marketing isn't selling a product — it's designing a category that makes competitors irrelevant by framing the buyer's problem in a new way that only your product can solve. The "problem map" shows where legacy categories pull buyers in the wrong direction, and the new category redirects them toward the right problem definition.

**Gartner Hype Cycle**:
The Gartner Hype Cycle plots emerging technologies by maturity and adoption. New categories typically appear at the "Innovation Trigger" phase. Category creators who successfully brief Gartner analysts get their category label placed on the Hype Cycle, which triggers mainstream analyst/press attention and validates market legitimacy. The Category Creation diagram can be positioned against the Hype Cycle to show where the new category is in its adoption journey.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] New category has a proper noun name (not a generic description)
- [ ] Category problem statement (1-2 lines) is present
- [ ] At least 2–3 legacy categories are shown with their limitations
- [ ] Own product positioned as the category anchor (not the only member)
- [ ] Category label reflects buyer problem framing, not technology name
- [ ] Analyst acknowledgment present if applicable
- [ ] Gap zone is visually central and clearly labeled
- [ ] First-mover date or context note present
- [ ] CMO can pitch the category to a reporter in 3 sentences using this slide
