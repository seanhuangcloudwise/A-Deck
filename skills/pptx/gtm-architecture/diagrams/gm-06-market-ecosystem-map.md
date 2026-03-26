# GM-06: Market Ecosystem Map — GTM Diagram Spec

_Ref: CB Insights Market Map Methodology | a16z Industry Landscape Format | Gartner Market Guide | Startup Genome Ecosystem Framework_

---

## 1. Purpose & When to Use

**Definition**: A visual landscape that maps the full set of players in a market ecosystem — organized by category, domain, or layer — showing where the product fits relative to partners, competitors, and complementary vendors.

**Use When**:
- Briefing analysts on the company's view of market structure
- Showing investors proof of a real, defined market with identifiable players
- Communicating partnership and integration ecosystem strategy
- Launching a new product category and demonstrating market context
- Onboarding enterprise buyers who need to understand the vendor landscape before selecting

**Questions Answered**:
- Who are all the players in this market, and how do they relate?
- Where does this product sit in the ecosystem?
- What are the natural integration partners vs competitors?
- Is there white space (unclaimed territory) in this market?

**Primary Audience**: CMO, BD (Business Development), Analyst Relations, Investors, Enterprise Procurement evaluators

---

## 2. Visual Layout Specification

**Structure**: Segmented grid or concentric zone layout with vendors placed by category.

### Variant A: Category Grid (Recommended — CB Insights style)
- Columns = product categories (e.g., Monitoring / ITSM / AIOps / CMDB)
- Rows = market tier (Leader / Challenger / Niche) or nothing (flat list)
- Each cell: vendor logo tile (or name block if logo unavailable)
- Own product: highlighted with brand border or pinned position
- Best for: analyst briefing, investor deck market slide

### Variant B: Zone Concentric Map
- Center zone: core market (what the product directly addresses)
- Middle ring: adjacent market (integration partners, complementary tools)
- Outer ring: ecosystem enablers (cloud platforms, dev tools, standards bodies)
- Own product at map center
- Best for: whitepaper ecosystem section, partnership strategy slides

### Variant C: Value Chain Position Map
- Horizontal value chain (data collection → processing → action → outcome)
- Vendors placed along the chain by primary function
- Own product shown spanning multiple stages (platform advantage visualization)
- Best for: executive positioning, digital transformation narratives

**Grid Proportions**:
- Variant A grid: 3–6 columns, 3–4 rows; vendor tile: 72pt × 28pt
- Variant B: 3 concentric ovals occupying 80% of slide content area
- Own product tile/node: 120% size of competitor tiles

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Own product tile | Self | `#00CCD7` bg, white text |
| Partner tiles | Tech integration partners | `#53E3EB` light tint |
| Competitor tiles | Direct competitors | `#A5A7AA` |
| Market category header | Column/zone label | `#44546A` bg, white |
| Unclaimed zone | White space opportunity | Dashed `#00CCD7` outline |
| Adjacent market zone | Nearby category | `#F5F5F5` bg |
| Standards / platforms | Infrastructure layer | `#D9EEF2` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Market landscape as of [date]" | 14pt | Regular |
| Category Header | Column / zone label | 10pt | Bold, White |
| Vendor Name | Tile label | 8–9pt | Regular or SemiBold |
| Zone Label | Concentric ring name | 10pt | Bold, colored |
| Footnote | Source, date, inclusion criteria | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Named tile (rect) | Individual vendor placement |
| Category column | Product segment grouping |
| Concentric oval | Ecosystem proximity zone |
| Dashed rect outline | Unclaimed market opportunity |
| Bold-border tile | Own product highlight |

**Connector Rule**:
- Variant A and B: No connectors — proximity implies relationship.
- Variant C (value chain): Directional connectors showing data/value flow between stages.

---

## 6. Annotation Rules

- **Source**: "Landscape as of [date]. Inclusion criteria: [e.g., minimum ARR $5M or publicly referenced enterprise customers]." in footnote.
- **Segment count**: Add "N vendors across X categories" as a subtitle or annotation — communicates market size credibility.
- **Partner / competitor distinction**: Use color or badge to distinguish "Partner" from "Competitor" tiles — avoid ambiguity.
- **White space call-out**: If highlighting an unclaimed zone, add a callout: "Unaddressed: [capability gap]" with a brief description.
- **Own product span**: If the product spans multiple categories, show it with a colored spanning bar or connection rather than placing it in just one cell.

---

## 7. Content Density Rules

| Mode | Vendors | Categories | Per Slide |
|---|---|---|---|
| Minimum | 10 | 3 | — |
| Optimal | 20–40 | 4–6 | 1 slide |
| Maximum | 80 | 10 | → split by category cluster |

**Overflow Strategy**: For 50+ vendor landscapes, cluster minor vendors and show only category leaders named. Add "And 35 others" tag. Never let individual tiles become unreadable (< 7pt font).

---

## 8. Anti-Patterns

1. **Only competitors, no partners**: Ecosystem maps that only show competitive vendors miss the partner and integration story — buyers and analysts want to see how the product plays well with others.
2. **Own product in the center of everything**: Placing own product at the center of every diagram without meaningful category distinction makes it look defensive rather than factual.
3. **Logo farm without structure**: Dumping 60 vendor logos in no particular order with no category grouping — this signals the creator doesn't understand the market.
4. **No inclusion criteria**: A map with no stated basis for which vendors are included cannot be defended when a prospect asks "Why isn't [Vendor X] here?"
5. **Outdated landscape**: Ecosystems change every 6–12 months in fast-moving markets. An ecosystem map with no date stamp signals staleness.

---

## 9. Industry Reference Patterns

**CB Insights Market Map Format**:
CB Insights pioneered the "market map" format as a research product — categorized grids of vendors by capability segment. Their methodology requires: explicit category definitions, inclusion rationale, and no value judgments (no "leaders" labeling). The format has become the de-facto analyst briefing standard. Own-published market maps should follow the same neutrality principles, then highlight own position separately.

**a16z Industry Landscape Diagrams**:
Andreessen Horowitz publishes landscape diagrams for emerging markets (AI, infrastructure, FinTech) that show vendor concentration by category, investment volume, and time of founding. The layered architecture model — data layer / model layer / application layer / distribution layer — is specifically influential for infrastructure and platform products. This four-layer structure maps well to enterprise software markets.

**Gartner Market Guide**:
The Gartner Market Guide (distinct from the Magic Quadrant) is published for markets that are not yet mature enough for MQ evaluation. It lists "Representative Vendors" by category without ranking them. The self-published analog is this ecosystem map: it establishes category legitimacy without forcing a ranking that might disadvantage the presenter.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Inclusion criteria stated in footnote
- [ ] Date of assessment shown
- [ ] Categories are clearly labeled with distinct names
- [ ] Partner vs. competitor tiles are visually distinguishable
- [ ] Own product tile is larger or highlighted without being dishonestly prominent
- [ ] Unclaimed / white space zones are explicitly called out if relevant
- [ ] No single tile font size below 7pt
- [ ] Segment count summary annotation present
- [ ] Presenter can explain category structure and own position in 45 seconds
