# BA-02: Value Stream — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B | Business Architecture Guild Value Stream Standard | Lean Value Stream Mapping_

---

## 1. Purpose & When to Use

**Definition**: A linear chain of sequential stages that together deliver a specific outcome of value to a customer or stakeholder — showing what happens, what value is added, and what the trigger/output is at each stage.

**Use When**:
- Communicating how the business delivers value end-to-end to customers or stakeholders
- Identifying bottlenecks, waste, and handoff failures in delivery chains
- Designing to-be process architecture at a business abstraction level (above process maps)
- Aligning capabilities to value delivery stages before selecting applications
- Presenting business model improvements to executive sponsors

**Questions Answered**:
- How does value flow from triggering event to customer outcome?
- What KPIs govern each stage of delivery?
- Where do delays, handoffs, or losses occur in the value chain?
- Which capabilities or systems support each stage?

**Primary Audience**: Business leadership, Operations, Enterprise Architects, Product Managers

---

## 2. Visual Layout Specification

**Structure**: Horizontal stage chain — left-to-right progression with stage boxes connected by chevron arrows.

### Variant A: Executive Summary (4–6 stages)
- Large chevron blocks spanning full slide width
- Stage name only (no KPI detail)
- Optional: value output label below each chevron
- Best for: Leadership overview, investor presentation

### Variant B: Standard (5–8 stages with outputs)
- Stage block (top) + output value box (below) per stage
- KPI indicators shown as small metric chips below each stage
- Trigger icon at left, outcome/result icon at right
- Best for: Architecture review, strategy workshop

### Variant C: Dense / Operational (6–10 stages with capability + KPI)
- Three-row layout: Stage block / Supporting capability pills / KPI metrics
- Vertical space: 30% stage row / 30% capability row / 30% KPI row / 10% header
- Best for: Capability-to-value traceability, process improvement

**Grid Proportions**:
- Trigger label (left edge): 60pt wide
- Stage blocks: equal-width, 4pt gutters between chevrons
- Outcome block (right edge): 80pt wide
- KPI row height: 20% of content area

---

## 3. Color Semantics

| Element | Meaning | Fill Color | Text |
|---|---|---|---|
| Value stage block | Core stages in delivery | `#00CCD7` | White |
| Supporting/enabling stage | Non-core steps | `#53E3EB` | `#2F2F2F` |
| Delayed/problem stage | Bottleneck identified | `#A5A7AA` | `#2F2F2F` |
| Trigger event | Starting condition | `#44546A` | White |
| Value outcome | End customer output | `#44546A` | White |
| KPI chip | Metric indicator | White fill | `#2F2F2F` border |
| Connector arrow | Stage transition | `#00CCD7` | — |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|---|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Stage Name | Inside chevron/block | 11–12pt | SemiBold | White |
| Stage Output | Below stage block | 9pt | Regular | `#2F2F2F` |
| KPI Label | Metric chip | 8pt | Regular | `#2F2F2F` |
| Trigger/Outcome | Edge labels | 10pt | SemiBold | White |
| Capability Pill | Supporting capability | 8pt | Regular | `#00CCD7` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Chevron arrow shape | Value stage (directional flow implied) |
| Rounded rect (≤4pt radius) | KPI chip or output summary block |
| Pentagon or oval (leftmost) | Triggering event |
| Pentagon or oval (rightmost) | Value outcome / customer result |
| Small down-arrow | Handoff to another team/system |
| Dashed box outline | Planned future stage |

**Connector Rule**: Chevrons are self-connecting by layout. Use explicit `→` connectors only when breaking visual continuity (e.g., in dense variant). Label connectors with handoff type: "passes to", "triggers", "enables".

---

## 6. Annotation Rules

- **KPI chips**: Small rounded rect below each stage — one primary KPI per stage in format "Metric: Target" (e.g., "Cycle time: ≤2d")
- **Bottleneck indicator**: Red `⚠` icon above the delayed stage with hover-text note (8pt)
- **Capability pills**: Thin rounded pills below stage listing supporting capabilities by name
- **Delta annotation**: For Variant C, add "AS-IS: X → TO-BE: Y" pair beside each KPI in parentheses
- **Stage owner**: Small gray label under stage name (department or role, 8pt)

---

## 7. Content Density Rules

| Mode | Stages | KPIs | Capabilities shown | Per Slide |
|---|---|---|---|---|
| Minimum | 3 | 1/stage | 0 | 3 stages |
| Optimal | 5–7 | 1–2/stage | 1–2/stage | 6 stages |
| Maximum | 10 | 2/stage | 3/stage | → split at 7 |

**Overflow Strategy**: For value streams with more than 7 stages, split at the primary handoff boundary. Prefix each slide with its segment title ("Phase 1: Acquire" / "Phase 2: Deliver"). Add a mini overview strip at slide top showing full stage count.

---

## 8. Anti-Patterns

1. **Activity/task confusion**: Listing individual tasks instead of stages ("Send email", "Fill form") — each stage should represent a meaningful cluster of activities with a clear value output.
2. **Missing trigger and outcome**: Starting a value stream mid-flow without showing what triggered it or what the customer receives — the end-to-end story is lost.
3. **Equal width for unequal importance**: Giving equal visual weight to core stages and administrative/support stages — strategic stages should be visually primary.
4. **Metrics without targets**: Showing KPI names without target values ("Cycle time") provides no actionable information.
5. **Mixing process and capability levels**: Including both process steps (L2) and capability names (L1) in the same stage chain creates confusion — use consistent abstraction level throughout.

---

## 9. Industry Reference Patterns

**Business Architecture Guild (BIZBOK Guide)**:
The Guild defines a value stream as an end-to-end collection of value-adding activities that create an overall result for a customer, stakeholder, or end user. Each value stage must have a defined "value item" — the thing being processed — plus a triggering event, enabling capabilities, and a stakeholder value outcome. The Guild recommends 4–8 stages per value stream with one primary actor/stakeholder as the beneficiary.

**Lean Value Stream Mapping (VSM)**:
Lean VSM, adapted from Toyota Production System, maps material and information flows across production or service stages, quantifying cycle time, waiting time, and handoff costs. For business architecture use, adapt: replace physical flow symbols with business stage blocks; retain cycle time and WIP metrics. The "waste identification" overlay (highlighting non-value-adding stages in gray) is directly applicable to business architecture optimization.

**IBM Business Architecture Blueprint**:
IBM's approach pairs each value stream stage with "Value Stage Enablers" — the specific business capabilities, information flows, and organizational units that make the stage work. The canonical format is a three-tier diagram: Stage name (top row) / Enablers (middle) / Performance metrics (bottom). This pattern is the basis for Variant C in this spec.

---

## 10. Production QA Checklist

- [ ] Value stream has exactly one trigger event and one customer-facing outcome
- [ ] Each stage name is a gerund phrase or noun representing a value cluster (not a task)
- [ ] At least one KPI is specified per stage
- [ ] Stage coloring follows semantic mapping (not arbitrary color choices)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Chevron connectors are directional (left-to-right)
- [ ] No decorative separators between stages — chevron adjacency implies sequencing
- [ ] Presenter can walk through all stages in under 90 seconds
- [ ] For Dense variant: capability names reference the BA-01 Capability Map exactly
- [ ] Bottleneck stages (if identified) are explicitly marked, not just implied by color
