# BA-07: As-Is / To-Be Comparison — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phases B/E | Kotter 8-Step Change Model | McKinsey Transformation Framework_

---

## 1. Purpose & When to Use

**Definition**: A structured side-by-side or overlay diagram showing the current state (As-Is) of a business model, process, or capability landscape alongside the target future state (To-Be), with explicit delta indicators showing the nature and magnitude of required change.

**Use When**:
- Opening or anchoring a transformation program narrative
- Justifying investment decisions by quantifying the gap
- Communicating change scope to executive sponsors and change boards
- Aligning multiple stakeholders around a shared target state picture
- Presenting transformation results after a change program

**Questions Answered**:
- What is the current state of the business model/process/capability?
- What is the target state we are designing toward?
- What specifically must change, and by how much?
- What stays the same (continuity points)?

**Primary Audience**: Executive sponsors, Change Management, Programme Directors, Management consultants

---

## 2. Visual Layout Specification

**Structure**: Dual-column comparison — As-Is on left, To-Be on right, with a delta zone in center or below.

### Variant A: Side-by-Side Blocks (clean comparison)
- Left panel (45% width): As-Is blocks with gray-toned fills
- Center divider (10%): "→ Transform" label or delta summary
- Right panel (45%): To-Be blocks with cyan fills
- Best for: Capability or structure comparison

### Variant B: Overlay / Transition Diagram
- Single diagram frame showing existing elements (gray, dashed) overlaid with new elements (cyan, solid)
- Delta arrows showing "add / remove / transform" per element
- Best for: Process or org structure changes where most elements evolve

### Variant C: Before/After Column Comparison Table
- Table format: rows = dimensions, Col 1 = As-Is state, Col 2 = Change type, Col 3 = To-Be state
- Change type icons: ➕ Add, ➖ Remove, ♻ Transform, ✓ Retain
- Best for: Management reporting, governance review boards

**Grid Proportions**:
- Header row: 10% of slide height
- As-Is panel: 45% width
- Delta zone: 10% width
- To-Be panel: 45% width
- Delta description row (bottom): 15% height (optional)

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| As-Is element (current state) | Existing structure/process | `#A5A7AA` fill, `#2F2F2F` text |
| To-Be element (target state) | Future structure/process | `#00CCD7` fill, White text |
| Retained element (no change) | Continuity through transformation | `#53E3EB` fill (same both sides) |
| Added element | New in To-Be | `#00CCD7` with `+` badge |
| Removed element | Gone in To-Be | `#A5A7AA` with `−` badge + strikethrough |
| Transformed element | Changed but not replaced | `#53E3EB` → `#00CCD7` gradient / split box |
| Delta connector | Change direction indicator | `#00CCD7` solid arrow, labeled |
| Risk/dependency note | Change dependency | `#44546A` annotation box |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Panel Header ("As-Is" / "To-Be") | Column anchor | 16pt | Bold, `#44546A` |
| Element Label | Content block label | 10–11pt | SemiBold |
| Change Type Badge | ➕➖♻ indicator | 10pt | Regular |
| Delta Description | Change narrative text | 9pt | Regular |
| Dependency Note | Risk/constraint annotation | 8pt | Italic, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Gray rounded rect | As-Is state block |
| Cyan rounded rect (≤4pt) | To-Be state block |
| Split half-gray, half-cyan rect | Transformed element (Variant B) |
| Strikethrough rect | Removed element |
| `+` badge (green circle) | Added element |
| `−` badge (red circle) | Removed element |
| Bold horizontal arrow (→) | Transformation direction |
| Delta triangle (Δ) | Quantified change indicator |
| Vertical center divider | As-Is / To-Be boundary |

**Connector Rule**: Horizontal arrows show transformation direction (As-Is → To-Be). Vertical arrows within a panel show structural relationships. Never use decorative diagonal lines to "connect" As-Is to To-Be — use aligned horizontal arrows instead.

---

## 6. Annotation Rules

- **Delta badges**: Quantified change amounts on connecting arrows — "−40% headcount", "+2 new capabilities", "12→5 systems"
- **Timeline indicator**: Optional "Target Date: Q3 2026" annotation on To-Be panel
- **Dependency flag**: Red `!` annotation on To-Be elements whose realization depends on external factors (technology, budget, org change)
- **Pilot indicator**: Star badge on To-Be elements that will be piloted before full rollout
- **Source reference**: Small "Source: Strategy 2025 Plan" note at bottom of As-Is panel

---

## 7. Content Density Rules

| Mode | Elements per Side | Delta Descriptions | Per Slide |
|---|---|---|---|
| Minimum | 3 | 2 | — |
| Optimal | 5–8 | 4–6 | 8 per side max |
| Maximum | 12 | 10 | → split by dimension |

**Overflow Strategy**: Split by dimension type. Slide 1: Capability / Structure comparison. Slide 2: Process comparison. Slide 3: Technology / System comparison. Each slide uses consistent framing and visual language.

---

## 8. Anti-Patterns

1. **Vague To-Be**: Drawing the To-Be panel with abstract labels ("Improved", "Optimized", "Better") that don't specify what changes structurally — a valid To-Be must be as specific as the As-Is.
2. **Missing continuity elements**: Showing only what changes and omitting what stays the same — continuity elements provide anchoring context for change communication.
3. **No delta quantification**: Side-by-side diagram with no delta arrows or change metrics — produces a decoration, not a transformation narrative.
4. **Aspirational fantasy**: To-Be designed without regard to actual constraints (budget, technology, regulation) — must include dependency flags where assumptions apply.
5. **Misaligned levels**: Mixing capability-level As-Is with process-level To-Be — both sides must operate at the same abstraction level throughout.

---

## 9. Industry Reference Patterns

**Kotter 8-Step Change Model (Harvard Business School)**:
Kotter emphasizes that establishing urgency requires showing the gap between the current state and the danger of inaction. The As-Is/To-Be diagram visualizes this gap explicitly. Step 4 of Kotter ("Communicate the Change Vision") uses a clear visual contrast — gray/muted As-Is vs. vibrant/energetic To-Be — to create emotional alignment with the target state.

**TOGAF Migration Planning (Phase E/F)**:
TOGAF's Architecture Roadmap is built on a baseline-target gap analysis: the current architecture (Baseline) vs. the target architecture (Target). The gap analysis identifies: required changes (add/modify/remove), transition architecture states, and dependencies. The AS-IS / TO-BE diagram is the visual representation of the TOGAF Architecture Gap Analysis report.

**McKinsey Transformation Blueprint**:
McKinsey uses a structured "Current State — Performance Frontier — Target State" framework. Current state maps performance against competitors. Performance frontier shows the theoretical maximum. Target state positions where the organization needs to be in 3–5 years. The delta is the transformation agenda. For internal use, simplify to As-Is vs. To-Be with quantified gap.

---

## 10. Production QA Checklist

- [ ] Both As-Is and To-Be operate at the same abstraction level (capability, process, or org)
- [ ] Every changed element (add/remove/transform) is explicitly marked with a change-type badge
- [ ] At least one quantified delta is shown (number, percentage, or metric change)
- [ ] Retained/continuity elements are visually identified
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Panel headers "As-Is" and "To-Be" (or Chinese equivalents) are clearly visible
- [ ] Delta arrows are directional (As-Is → To-Be)
- [ ] Where transformation has dependencies, a dependency flag is present
- [ ] Target date or program timeline is referenced somewhere on the slide
- [ ] Presenter can describe the single most important change in 15 seconds
