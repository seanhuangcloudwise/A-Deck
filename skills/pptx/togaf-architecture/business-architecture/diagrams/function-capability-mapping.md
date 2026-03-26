# BA-06: Function-to-Capability Mapping — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B | Gartner Capability Realization Map | Business Architecture Guild_

---

## 1. Purpose & When to Use

**Definition**: A matrix or bipartite map that explicitly connects organizational functions (what a department does day-to-day) to business capabilities (what the business needs to achieve), revealing coverage, gaps, and overlaps.

**Use When**:
- Performing IT investment gap analysis against capability demands
- Assessing which functions support which strategic capabilities
- Planning transformation: identifying functions that need to be redesigned or eliminated
- Supporting operating model redesign by clarifying functional responsibilities
- Providing input to application architecture for capability-to-app alignment

**Questions Answered**:
- Which functions directly support each business capability?
- Are any capabilities unsupported (no function mapped to them)?
- Do any functions support too many or too few capabilities (overload/waste)?
- Where should we invest to close capability gaps?

**Primary Audience**: Enterprise Architects, Business Architects, Operations Leaders, IT Strategy teams

---

## 2. Visual Layout Specification

**Structure**: Matrix (functions as rows, capabilities as columns) or bipartite network (functions on left, capabilities on right, edges showing mappings).

### Variant A: Matrix View
- Rows = Functions (labeled with function name + owning department)
- Columns = Capability domains/capabilities from BA-01 Capability Map
- Cells = filled chip if function maps to capability; empty if no mapping
- Color intensity indicates strength of contribution
- Best for: Gap analysis, rationalization, management review

### Variant B: Bipartite Network
- Left column: Function nodes (7–15 functions)
- Right column: Capability nodes (5–12 capabilities)
- Edges: solid = primary mapping, dashed = supporting mapping
- Best for: Showing complex, many-to-many relationships clearly

### Variant C: Heatmap with Gap Overlay
- Same matrix structure as Variant A
- Color fill = coverage score (full = #00CCD7, partial = #53E3EB, none = white/red)
- Gap cells (capability with no supporting function) highlighted in red dashed border
- Best for: Executive investment decisions, transformation roadmap justification

**Grid Proportions** (Matrix):
- Row header (function name): 180pt wide
- Column header (capability name): 80pt wide
- Cell size: 60pt × 40pt minimum
- Column headers rotated 45° if > 8 capabilities

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Full mapping (primary support) | Function directly realizes capability | `#00CCD7` filled cell |
| Partial mapping (contributing) | Function partially supports capability | `#53E3EB` filled cell |
| No mapping | Function offers nothing to capability | White (empty cell) |
| Critical gap | Capability with zero supporting functions | Red dashed border |
| Overloaded function | Function maps to 5+ capabilities | `#44546A` row header border |
| Redundant mapping | Multiple functions provide same capability | `#A5A7AA` (flag for consolidation) |
| Function node (bipartite) | Organizational function | White + `#2F2F2F` border |
| Capability node (bipartite) | Target capability | `#00CCD7` fill |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Row/Column Header | Function or capability name | 9–10pt | SemiBold |
| Cell Content | Mapping indicator | 8pt | Regular |
| Gap Label | "No Coverage" annotation | 8pt | Red, Bold |
| Legend Label | Color key | 8pt | Regular, `#A5A7AA` |
| Bipartite node label | Function / capability name | 10pt | Regular |

---

## 5. Shape & Connector Vocabulary

**Matrix Variant**:
| Shape | Meaning |
|---|---|
| Filled square/rect cell | Mapping exists |
| Empty cell | No mapping |
| Red dashed border cell | Critical gap |
| Row highlight bar | Overloaded function |
| Column highlight bar | Strategic capability (priority) |

**Bipartite Variant**:
| Shape | Meaning |
|---|---|
| Rounded rect left | Function node |
| Rounded rect right | Capability node |
| Solid edge | Primary realization link |
| Dashed edge | Supporting / contributing link |
| Double-edge | Must-have critical link |

---

## 6. Annotation Rules

- **Coverage score**: For matrix variant, show a "coverage %" summary column on the right (e.g., "Capability Coverage: 67%")
- **Gap count**: In slide subtitle or annotation box: "3 critical capability gaps identified"
- **Function owner tag**: Small department abbreviation in each function row header
- **Redundancy marker**: When 3+ functions map to same capability, add `∩` (intersection symbol) in column header
- **Priority flag**: Star icon in capability column header for capabilities flagged as strategic priority

---

## 7. Content Density Rules

| Mode | Functions | Capabilities | Matrix Cells | Per Slide |
|---|---|---|---|---|
| Minimum | 4 | 3 | 12 | — |
| Optimal | 8–12 | 6–10 | 48–120 | 100 cells max |
| Maximum | 15 | 15 | 225 | → split by domain |

**Overflow Strategy**: For large matrices, split by capability domain. Each split slide shows all functions vs. one domain's capabilities. Include a summary matrix slide showing coverage percentages by domain.

---

## 8. Anti-Patterns

1. **All cells filled**: Marking every function as supporting every capability (100% matrix coverage) — this means the mapping was not done critically and provides no analytical value.
2. **Functions = org units**: Using department names instead of function names ("Finance" instead of "Financial Reporting", "Budget Control") — functions must be specific activities, not org labels.
3. **No gap identification**: Presenting a complete mapping without highlighting gaps or redundancies — the purpose of this diagram is gap analysis, not just documentation.
4. **Mismatched capability names**: Using different capability names than those defined in BA-01 Capability Map — all 4 layers must share a common capability vocabulary.
5. **Network hairball (bipartite)**: Too many edges in bipartite variant creates unreadable tangle — limit to 15 functions × 10 capabilities maximum; use matrix for larger scope.

---

## 9. Industry Reference Patterns

**Gartner Capability Realization Map**:
Gartner's pattern maps IT capabilities (not business services) to the business capabilities they enable. The realization map uses a 2×2 matrix of coverage vs. quality: High coverage + High quality = Leverage; High coverage + Low quality = Fix; Low coverage + High quality = Expand; Low coverage + Low quality = Redesign. This 2×2 overlay on the function-capability matrix makes investment decisions immediately actionable.

**TOGAF Application Portfolio Rationalization**:
TOGAF uses function-to-capability mapping as the bridge between business architecture (Phase B) and application architecture (Phase C): identify capabilities → map to functions → map functions to applications → identify redundant or unsupported applications. This 3-hop traceability is the foundation of rationalization programs.

**McKinsey Organizational Health Analysis**:
McKinsey maps organizational functions to strategic capabilities to identify "performance anchors" — functions that are over-resourced relative to their strategic contribution, and "capability voids" — strategic capabilities with no functioning organizational owner. The heat map variant (Variant C) with gap overlay directly implements this analysis approach.

---

## 10. Production QA Checklist

- [ ] All capability names match exactly those defined in BA-01 Capability Map
- [ ] At least one critical gap (capability with zero mapping) is identified
- [ ] Coverage percentage is shown per capability column
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Every function row identifies its owning department/team
- [ ] No cell is filled without a confirmed, documented mapping rationale
- [ ] Redundant mappings (3+ functions → same capability) are flagged
- [ ] Legend for color encoding is present on each slide
- [ ] Presenter can explain the top 3 gaps or investment priorities in 60 seconds
- [ ] Gap identification is consistent with BA-07 As-Is/To-Be if both diagrams are in same deck
