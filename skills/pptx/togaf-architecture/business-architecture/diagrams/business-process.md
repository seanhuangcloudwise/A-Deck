# BA-03: Business Process (L1/L2) — Business Architecture Diagram Spec

_Ref: TOGAF ADM Phase B | BPMN 2.0 (OMG) | ISO 19510 | Rummler-Brache Swimlane Method_

---

## 1. Purpose & When to Use

**Definition**: A structured sequence of steps, decisions, and actors showing HOW a business activity is executed — at Level 1 (high-level flow between departments) or Level 2 (detailed steps within a department/role).

**Use When**:
- Documenting standard operating procedures (SOPs) for governance or training
- Analyzing process efficiency, bottlenecks, or compliance issues
- Designing future-state processes in transformation programs
- Communicating cross-departmental handoffs requiring accountability
- Serving as input to application and integration design (AA layer)

**Questions Answered**:
- What are the exact steps to complete an activity?
- Who owns each step?
- Where are the decision points and exception paths?
- What triggers the process and what ends it?

**Primary Audience**: Operations teams, Business analysts, Process owners, Auditors, IT architects (for integration input)

---

## 2. Visual Layout Specification

**Structure**: Horizontal swimlane diagram — one row per actor/department, read left-to-right.

### Variant A: L1 Process (3–5 lanes, 5–8 major steps)
- Each lane is one department or major role
- Steps shown as large activity boxes, one decision diamond per key junction
- Best for: Executive overview, transformation design, cross-org alignment

### Variant B: L2 Process (4–7 lanes, 8–15 detailed steps)
- Each lane is one role or team
- Includes sub-steps, system annotations, and multiple decision branches
- Exception paths shown in dashed-border flow
- Best for: SOP documentation, IT integration design, compliance audit

### Variant C: Linear Flow (no swimlanes)
- Left-to-right step chain with role labels inside each step box
- Suitable when all steps belong to one actor or when swimlane rows exceed 7
- Best for: Compact process summary, onboarding materials

**Grid Proportions**:
- Lane header column: 120pt (left edge, #44546A background)
- Lane rows: equal height, minimum 90pt per row
- Step spacing: 8pt gutters between step boxes
- Connector line stroke: 1.5pt, #2F2F2F

**Layout Heuristics (Mandatory for production output)**:
- Keep standard activity boxes globally consistent in width and height on the same slide. Only enlarge an individual box when text density genuinely requires it.
- For nodes that hand off between adjacent upper/lower lanes, prefer shared horizontal centers so the vertical transition reads as one aligned column.
- Use the lane canvas evenly from left to right. Do not cluster nodes on the left/middle while leaving large empty space on the right.
- When a process has 3 major steps in one lane, prefer near-equal center spacing before introducing custom offsets.
- Decision diamonds may use a separate standard size from activity boxes, but all diamonds on the same slide should stay consistent.
- Start and end event nodes must be treated as independent occupied nodes in the layout calculation. They need their own visible outer margin and may not overlap or visually merge into the nearest activity box.

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Lane header background | Role/department identity | `#44546A` + White text |
| Standard activity step | Normal process step | `#53E3EB` |
| Critical / high-risk step | Must-not-fail steps | `#00CCD7` border 2pt |
| Decision diamond | Branch point | White + `#2F2F2F` border |
| Start event | Process trigger | `#44546A` circle |
| End event | Process termination | `#2F2F2F` filled circle |
| Exception/error path | Alt flow | `#A5A7AA` + dashed connector |
| System annotation | IT system supporting step | `#44546A` small pill |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Lane Header | Role/department label | 11pt | SemiBold, White |
| Step Label | Activity name in box | 10pt | Regular |
| Decision Label | Branch condition text | 8pt | Italic |
| System Annotation | IT annotation pill | 7–8pt | Regular |
| Connector Label | Arrow annotation | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rectangle (≤4pt) | Standard activity step |
| Diamond | Decision / branch point |
| Filled circle (small) | Start event |
| Double-border circle | End event |
| Parallelogram | Input/Output data artifact |
| Dashed border rect | Offline/manual step |
| Cylinder | System / database involved |
| Solid arrow | Directional sequence flow (within lane) |
| Curved/dashed arrow | Directional cross-lane handoff |

**Connector Rule**: All process connectors must be directional arrows, not plain lines. Sequence flows between steps in same lane → solid arrow. Cross-lane handoffs → directional elbow/curved arrow with brief label. Exception paths → dashed directional arrow. Never use arrows merely as separators. When a connector terminates at an end event, keep enough trailing space so the event remains visually separate from the previous activity box.

---

## 6. Annotation Rules

- **System pills**: Small #44546A pill below each step that involves a system — label with system name (e.g., "CRM", "ERP")
- **Duration badge**: Small gray chip (7pt) inside each major step showing target cycle time (e.g., "≤1d")
- **Risk flag**: Red `!` icon in top-right corner of high-risk steps
- **Automation indicator**: Lightning-bolt icon for fully automated steps (no human touchpoint)
- **Decision Yes/No**: Decision diamonds must have both branches labeled "Yes/No" or conditions

---

## 7. Content Density Rules

| Mode | Lanes | Steps | Decisions | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 4 | 1 | 4 steps |
| Optimal | 3–5 | 7–12 | 2–4 | 12 steps |
| Maximum | 7 | 18 | 6 | → 2 slides |

**Overflow Strategy**: Split L2 processes by phase boundary. Add "Continued from slide N" callout at slide top. Keep start/end events on each partial slide so each page is self-explanatory.

---

## 8. Anti-Patterns

1. **Too fine-grained at L1**: Showing individual keystrokes or system clicks in a leadership-facing L1 diagram — L1 should show department-level steps only (5–8 steps).
2. **Missing decision branches**: Showing only the happy path without exception or error branches — real processes have decision points; omitting them gives false confidence.
3. **Lane overload**: More than 7 swimlanes on one slide — text becomes unreadable and the structure looks like a spreadsheet.
4. **System boxes as process steps**: Placing system names (e.g., "SAP") as process steps implies the system does the work instead of the role — always use role lanes.
5. **Orphaned steps**: Steps with no incoming or outgoing connector — breaks the flow narrative and confuses reviewers.
6. **Inconsistent step sizing**: Similar activity nodes rendered at visibly different sizes without content reason — weakens process rhythm and makes the page look unstructured.
7. **Broken cross-lane alignment**: A handoff node in lane A and its paired node in lane B are close in meaning but far apart horizontally — creates unnecessary zig-zag routing.
8. **Unbalanced canvas use**: Most nodes occupy only the left 60–70% of the lane width while the right side remains empty — signals poor composition.
9. **Collapsed end event**: The end event circle is pushed against or partially overlaps the last activity box because it was not given its own layout slot.

---

## 9. Industry Reference Patterns

**BPMN 2.0 (OMG Standard)**:
Business Process Model and Notation defines a complete vocabulary for process diagrams including swimlanes (Pools and Lanes), flow elements (Activities, Gateways, Events), and connecting objects (Sequence Flows, Message Flows). For PPTX presentation, use BPMN-inspired shapes but optimize for visual clarity over full BPMN compliance — not every audience needs strict notation.

**Rummler-Brache Swimlane Method**:
Originated by Geary Rummler and Alan Brache in "Improving Performance" (1990). Defines three levels of analysis: Organization level (cross-department), Process level (cross-function), and Job/Performer level (individual role). The swimlane format arose directly from this framework. Key insight: most performance problems occur at cross-lane handoffs, not within individual steps.

**TOGAF Phase B Process Decomposition**:
TOGAF advises treating business process documentation as input to application architecture design. L1 process maps define the applications needed per stage; L2 maps define the interfaces required between systems. This cross-layer linkage (BA-03 → AA-03 Integration Map) is a canonical TOGAF pattern.

---

## 10. Production QA Checklist

- [ ] Every process has exactly one start event and at least one end event
- [ ] All decision diamonds have all branches labeled with conditions
- [ ] No orphaned steps (every step has at minimum one incoming and one outgoing connector)
- [ ] Cross-lane handoffs use directional arrows and align cleanly with paired nodes where possible
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Lane headers use #44546A fill with white text
- [ ] System annotations present for every step that involves an IT system
- [ ] Level (L1 or L2) is stated in subtitle (placeholder idx=1) or slide body
- [ ] Exception paths are shown with dashed arrows and labeled
- [ ] Process name, owner, and version are noted in slide footer or subtitle area
- [ ] Standard activity boxes use one default size unless a content-driven exception is documented
- [ ] Node centers are distributed evenly enough that no large empty region remains on the right side of the lane canvas
- [ ] Start/end event nodes have their own visible margin and do not visually merge with adjacent steps
