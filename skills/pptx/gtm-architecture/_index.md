# GTM Architecture Skills Index

This folder contains diagram skills for Go-to-Market communication, covering product white papers, solution briefs, sales battle cards, and market PR materials.

Parallel to TOGAF (system architecture) and Roadmap (product planning), this domain focuses on persuasion and market positioning, making products understandable, differentiated, and desirable to buyers, analysts, and press.

## Diagram Groups

| Group | Focus | Diagrams | Spec Files |
|---|---|---|---|
| G1 - Value Proposition | What we do and why it matters | 3 diagram types | [GM-01 ~ GM-03](diagrams/_catalog.md) |
| G2 - Market and Competition | Why us over alternatives | 3 diagram types | [GM-04 ~ GM-06](diagrams/_catalog.md) |
| G3 - Solution Architecture | How it works in context | 3 diagram types | [GM-07 ~ GM-09](diagrams/_catalog.md) |
| G4 - Proof and ROI | Prove the value claim | 3 diagram types | [GM-10 ~ GM-12](diagrams/_catalog.md) |
| G5 - GTM Strategy | How we go to market | 3 diagram types | [GM-13 ~ GM-15](diagrams/_catalog.md) |
| G6 - Category and Analyst | Own the narrative | 2 diagram types | [GM-16 ~ GM-17](diagrams/_catalog.md) |
| G7 - Product Feature Expression | Show feature depth and uniqueness | 8 diagram types | [GM-18 ~ GM-25](diagrams/_catalog.md) |
| G8 - Value Realization | Show measurable business value | 10 diagram types | [GM-26 ~ GM-35](diagrams/_catalog.md) |

**Total: 35 diagram types with production-level specifications.**

## Parallel Domains

| Domain | Skill | Purpose |
|---|---|---|
| TOGAF Architecture | `togaf-architecture` | System/application/data/technology blueprints |
| Roadmap Architecture | `roadmap-architecture` | Product planning, prioritization, KPI tracking |
| GTM Architecture | `gtm-architecture` | Market positioning, buyer persuasion, feature proof, value realization |

## Routing Hint

- Request is about market positioning, differentiation, buyer value, feature proof, or value realization: GTM Architecture
- Request is about product features, demo, how-to operations: `knowledge/product-feature`
- Request is about product roadmap, release plan: `roadmap-architecture`
- Request is about technical architecture, API, infrastructure: `togaf-architecture`

## Material x Diagram Group Mapping

| Material Type | Primary Groups | Secondary Groups |
|---|---|---|
| 产品白皮书 | G1 Value Proposition, G3 Solution Architecture, G8 Value Realization | G4 Proof and ROI |
| 产品解决方案 | G3 Solution Architecture, G4 Proof and ROI, G7 Product Feature Expression | G8 Value Realization |
| 销售一指禅 (Battle Card) | G2 Market and Competition, G7 Product Feature Expression | G4 Proof and ROI |
| 市场宣传 PR / Pitch | G1 Value Proposition, G6 Category and Analyst | G2 Market and Competition, G8 Value Realization |
| 分析师 Briefing | G6 Category and Analyst, G2 Market and Competition | G3 Solution Architecture, G8 Value Realization |
| 产品功能介绍 | G7 Product Feature Expression | G1 Value Proposition, G3 Solution Architecture |
| 商务价值说明 | G8 Value Realization, G4 Proof and ROI | G2 Market and Competition |

## Global Rules (Mandatory)

1. Titles and subtitles must use layout placeholders (idx=0, idx=1) first.
2. Rounded rectangle corner radius must be small (<=6pt); no PowerPoint default large radius.
3. No decorative-only shapes. Every connector carries semantic meaning.
4. Cloudwise brand palette: `#00CCD7` (primary) / `#53E3EB` (secondary) / `#2F2F2F` (text) / `#A5A7AA` (inactive) / `#44546A` (domain headers).
5. GTM-specific: each claim should be supported by at least one data point or reference on the same slide.
6. Competitive claims must be defensible; avoid unverifiable superlatives.