# BA-01: Capability Map — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B | Gartner Business Capability Model | OMG Business Architecture_

---

## 1. Purpose & When to Use

**Definition**: A heat-map style block matrix showing WHAT the business does — organized by capability domains independent of org structure, process, or technology.

**Use When**:
- Building or presenting enterprise strategy portfolio to C-suite or board
- Performing investment prioritization across business domains
- Identifying maturity gaps before digital transformation
- Communicating with IT to align capability demand with application supply
- Running M&A due diligence to compare capability coverage

**Questions Answered**:
- What capabilities does the organization have, need, or lack?
- Where are the maturity gaps relative to strategic ambition?
- Which domains are core differentiators vs. commodity support?
- Where should investment flow in the next planning cycle?

**Primary Audience**: C-suite, Strategy team, Enterprise Architects, Business Analysts

---

## 2. Visual Layout Specification

**Structure**: Hierarchical block matrix — rows = capability domains, columns = capability instances within each domain.

### Variant A: Executive Summary (1-level, 6–12 domain blocks)
- Arrangement: 3×2 or 4×3 grid of large blocks
- Each block: Domain name (bold 14pt) + maturity indicator (color fill)
- Best for: Board deck, 5-minute overview

### Variant B: Standard (2-level, domain → capabilities)
- Left edge: domain labels (15% of slide width, #44546A fill)
- Main area: capability rows with equal-width cells (4pt gutters)
- 12–28 capability cells total
- Best for: Strategy workshop, architecture review

### Variant C: Dense / Full (3-level with sub-capabilities)
- Sub-capability rows nested under capabilities
- Max 36 cells before overflow strategy triggers
- Label font drops to 8pt; legend mandatory
- Best for: Technical capability assessment, EA repository

**Grid Proportions**:
- Title placeholder: top 10% of slide
- Domain column (left): 16% of content area width
- Capability grid: 84% remaining width, equal-column split
- Legend strip: fixed 56px height at bottom (not part of grid)

---

## 3. Color Semantics

Cloudwise Palette Mapping for Maturity Encoding:

| Maturity Level | Chinese | Fill Color | Border |
|---|---|---|---|
| Undeveloped | 未建设 | `#FFFFFF` (white) | `#A5A7AA` dashed |
| Initial / Ad-hoc | 初级 | `#A5A7AA` | `#A5A7AA` solid |
| Developing | 发展中 | `#53E3EB` | `#00CCD7` |
| Managed | 受管理 | `#00CCD7` | `#00CCD7` |
| Optimized | 优化级 | `#00CCD7` bold border, +star badge | `#2F2F2F` |

Domain header background: `#44546A` (dark blue-gray), white text  
Strategic focus domain: Bold left border 3pt `#00CCD7`  
Investment target cell: Small upward triangle `#00CCD7` in top-right corner

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|---|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Domain Label | Row/section name | 11pt | SemiBold | White on `#44546A` |
| Capability Name | Cell text | 9–10pt | Regular | `#2F2F2F` |
| Maturity Badge | Level indicator | 7pt | Regular | `#2F2F2F` |
| Legend Label | Bottom key | 8pt | Regular | `#A5A7AA` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rectangle (sharp corners) | Leaf capability cell |
| Rounded rect (≤4pt radius) | Domain container |
| Bold left-border rect | Strategic / investment-priority domain |
| Color-filled rect | Maturity level encoding |
| Small filled triangle (top-right) | Planned investment indicator |
| Dashed border | Gap / critical absence |

**Connector Rule**: NO connectors in Capability Map. Adjacency within a row implies domain grouping. If you need to show capability interactions, switch to BA-05 Service Decomposition or BA-06 Function-Capability Mapping.

---

## 6. Annotation Rules

- **Maturity badge**: Small circle in cell top-right — label L1/L2/L3/L4
- **Investment arrow**: Filled upward triangle (6×6pt) in top-right for "planned investment next cycle"
- **Gap marker**: Red dashed border (`#FF4444`, 1.5pt) for critical capability gaps flagged in strategy
- **Owner tag**: 2-letter department code in bottom-left corner (8pt, gray)
- **Footnote**: "Assessment Date: YYYY-MM" + methodology note (8pt, gray, bottom of slide)

---

## 7. Content Density Rules

| Mode | Domains | Capabilities/Domain | Total Cells | Max per Slide |
|---|---|---|---|---|
| Minimum | 3 | 2–3 | 6–9 | 9 |
| Optimal | 5–7 | 3–5 | 15–35 | 35 |
| Maximum | 9 | 6 | 54 | → split to 2 slides |

**Overflow Strategy**: Split at domain cluster boundary. Slide 1: Core/Differentiating domains. Slide 2: Support/Enabling domains. Both slides share the same legend strip.

---

## 8. Anti-Patterns

1. **Org-chart disguise**: Naming capabilities after departments ("Finance", "IT Operations") — capabilities must be functional and technology-agnostic, stable across org changes.
2. **Process confusion**: Listing process steps as capabilities ("Approve Purchase Order") — capabilities are WHAT, processes are HOW.
3. **Technology leakage**: Including technologies as capabilities ("SAP Module", "Kubernetes") — technology serves capabilities, not the other way.
4. **Color arbitrage**: Assigning colors based on aesthetics rather than maturity semantics — every color must map to the defined legend.
5. **Missing legend**: A capability map without maturity legend is unreadable to any audience. Legend is mandatory on every slide.

---

## 9. Industry Reference Patterns

**TOGAF Business Architecture Working Group**:
The TOGAF standard defines capabilities as business-level building blocks representing a combination of processes, roles, technology, and information to produce outcomes. The recommended hierarchy is: Domain (L1, 6–10 items) → Capability (L2, 3–8 per domain) → Sub-capability (L3, optional). Level 1 domains typically mirror Porter's Value Chain adapted to the organization's business model.

**Gartner Enterprise Architecture Practice**:
Gartner's Business Capability Model organizes capabilities in four cross-cutting horizontal rows: Customer & Market, Product & Service Delivery, Enterprise Planning & Control, Enabling Services. Each row has 4–8 columns. Investment priority is encoded as Invest → Maintain → Harvest → Retire using a purple-green-orange-gray scale. This pattern cleanly separates capability value from capability maturity.

**McKinsey Capability Assessment Heat Map**:
McKinsey uses a 5-tier maturity scale with a "target state" overlay that shows both current maturity and the required lift. Delta arrows on each cell show the gap. The visualization uses a light-to-dark gradient (light gray baseline → deep brand blue target state). Cells with the largest delta and highest strategic priority are circled with a bold border to drive investment conversation.

---

## 10. Production QA Checklist

- [ ] All capability names are noun-based and technology-agnostic
- [ ] Domains cover complete business scope with no obvious gaps
- [ ] Maturity color encoding strictly follows the defined legend (no arbitrary fills)
- [ ] Title uses slide layout placeholder (idx=0), subtitle uses placeholder (idx=1)
- [ ] All rounded-corner radii ≤ 6pt; no decorative shapes present
- [ ] Legend strip present and readable (≥ 8pt font size)
- [ ] Every non-white cell has a corresponding maturity level defined
- [ ] Domain count is 4–9 (fewer = too abstract; more = split diagram)
- [ ] No two adjacent capabilities have names that overlap in meaning
- [ ] Presenter can explain each capability in one sentence without referencing org structure or technology
