# BP-10: Human-Driven vs System-Driven Split — BPMN Architecture Diagram Spec

_Ref: OMG BPMN 2.0.2 formal/13-12-09 §10.2.2 Task Types, §10.8 Lanes; BPMN 2.0 by Example dtc/10-06-02 §6.3 "Human-driven vs. system-driven control flows"_

---

## Purpose

Show how a **process splits its control flow between human actors and automated systems**, clearly delineating which work is manual/user-driven and which is fully automated/system-driven. This is critical for automation assessment, digital transformation planning, and process optimization.

## When to Use

- Assessing automation potential in a business process
- Planning RPA or workflow automation scope
- Showing the handoff boundary between human interaction and system execution
- Comparing as-is (mostly human) vs to-be (mostly automated) process

## Official Case Anchor

**Incident Management — Human-driven vs. system-driven** (OMG Examples §6.3): The incident management example explicitly separates the process into two tracks: human-driven activities (1st-level support handles the ticket manually) and system-driven activities (automated escalation, SLA timer, auto-notification). The two tracks are visually separated by Lanes or by a dividing line, showing where automation takes over from human judgment.

**Task Types** (OMG formal spec §10.2.2): BPMN defines specific task types that distinguish human from system work:
- **User Task**: performed by a human with system assistance (form-based interaction)
- **Manual Task**: performed by a human without system assistance
- **Service Task**: automated execution by a software service
- **Script Task**: automated execution of a script
- **Business Rule Task**: automated decision via business rules engine
- **Send/Receive Task**: message-based interaction with external systems

## Conformance Level

Analytic — Task type icons, Lanes for human/system separation.

## Structure

```
┌─ Pool: Incident Management ─────────────────────────────────────────────┐
│ ┌─ Lane: Human (Manual/User Tasks) ────────────────────────────────────┤
│ │  [●Start] → [👤 Receive Ticket] → ◇XOR → [👤 Investigate] ─────→    │
│ │                                      ↓                               │
│ ├─ Lane: System (Service/Script Tasks) ────────────────────────────────┤
│ │                              [⚙ Auto-Classify] → [⚙ Route] ─────→   │
│ │                              [⚙ SLA Monitor ⏰] → [⚙ Escalate] →   │
│ ├─ Lane: Decision Engine (Business Rule Tasks) ────────────────────────┤
│ │                                          [📋 Evaluate Priority]      │
│ └──────────────────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────────────────┘
```

### Variant A: Two-Lane Split (Human / System)
- Simple 2-lane layout: top lane = human tasks, bottom lane = system tasks
- Flow crosses between lanes at integration points
- Best for: clear-cut automation boundary

### Variant B: Three-Lane Split (Human / System / Decision Engine)
- Adds a third lane for Business Rule / AI decision tasks
- Best for: processes with a mix of manual work, automation, and intelligent decision-making

### Variant C: Before/After Comparison (As-Is / To-Be)
- Left half: current process (mostly in Human lane)
- Right half: future process (many tasks moved to System lane)
- Shared gateway/event at the transition point
- Best for: digital transformation proposals

### Variant D: Automation Percentage Overlay
- Standard lane flow + annotation showing % of tasks automated
- Progress bar or pie chart annotation
- Best for: executive summary of automation assessment

## Layout Rules

Node positions are computed automatically by `auto_layout(nodes, edges, region, lanes=...)` from `layout_engine.py`. Lane IDs constrain each node's y-center to its assigned horizontal band. **Do not hardcode x/y positions in config or loader.**

### Lane Region

Each lane (human, system, decision engine) gets an equal horizontal band. The `lane` field on each node determines which band it is constrained to. Task type icons are applied as shape overlays after node positions are set.

### Render Region (10" × 5.63" slide)

| Boundary | Value |
|----------|-------|
| Pool header width | 0.35" |
| Lane header width | 0.7–0.9" |
| Content left | ~1.1" (after headers) |
| top | 1.5" |
| height | 3.5" (pool body) |

### Sizing (canonical defaults — may be capped by layout engine)

| Element | Dimension |
|---------|-----------|
| Lane height (2-lane) | 2.0–2.5" each |
| Lane height (3-lane) | 1.3–1.6" each |
| Task box | 1.2" × 0.5" |
| Task type icon | 0.15" × 0.15" top-left corner |
| Integration flow (cross-lane) | Vertical segment, 1pt solid |

## Task Type Icons (Must Distinguish)

| Task Type | Icon | Default Lane |
|-----------|------|-------------|
| User Task | 👤 (person with gear) | Human |
| Manual Task | 🤚 (hand) | Human |
| Service Task | ⚙ (gear/cog) | System |
| Script Task | 📜 (scroll) | System |
| Business Rule Task | 📋 (table/grid) | Decision Engine |
| Send Task | ✉→ (filled envelope) | System |
| Receive Task | ✉ (open envelope) | Either |

## Color Semantics

| Element | Color Token |
|---------|-------------|
| Human lane header | `primary` |
| Human lane body | `white` |
| System lane header | `secondary` |
| System lane body | `light` very subtle tint |
| Decision lane header | `primary` lighter variant |
| User Task border | `primary` |
| Service Task border | `secondary` |
| Business Rule Task border | `primary` lighter |
| Integration handoff arrow | `dark` with a distinctive style (e.g., slightly thicker) |
| SLA timer boundary event | `secondary` |
| Automation annotation | `secondary` bold text |

## Typography

| Text | Location | Size |
|------|----------|------|
| Lane header | Left strip | 9pt SemiBold |
| Task label | Inside box | 8pt Regular |
| Task type indicator | Small text or icon | 7pt |
| Automation % annotation | Corner callout | 10pt Bold |
| Integration point label | Near cross-lane arrow | 7pt Italic |

## Anti-Patterns

1. **No lane distinction**: If human and system tasks are in the same lane, the automation boundary is invisible — the whole point of BP-10 is lost.
2. **Task type icons missing**: Without the 👤/⚙/📋 icons, the reader cannot distinguish human from system execution.
3. **All tasks in one lane**: If everything is in the "Human" lane, the diagram doesn't show any automation. If everything is in "System", it doesn't show any human touchpoints. The value is in the split.
4. **Cross-lane flow without explanation**: When a sequence flow crosses from Human to System lane, the integration mechanism (API call, form submission, trigger) should be annotated.

## Official Best Practice Notes

From OMG Examples §6.3 (Human-driven vs. system-driven):
> The Incident Management example separates human-driven activities (1st line support analyzing, investigating, resolving) from system-driven activities (auto-classification, SLA monitoring, escalation) to make clear where automation boundary lies.

From OMG formal spec §10.2.2 (Task Types):
> "A Task is an atomic Activity within a Process flow. A Task is used when the work in the Process cannot be broken down to a finer level of detail. The different task types are: Service, Send, Receive, User, Manual, Business Rule, Script, and a None Task."

> "A User Task is a typical 'workflow' Task where a human performer performs the Task with the assistance of a software application."

> "A Service Task is a Task that uses some sort of service, which could be a Web service or an automated application."

## Data Contract

```yaml
title: "Incident Resolution – Human vs System Split"
subtitle: "Automation boundary analysis for L1 support process"
content:
  pool:
    id: "incident_mgmt"
    name: "Incident Management"
  lanes:
    - id: "human"
      name: "Human (L1 Support)"
      lane_type: "human"
    - id: "system"
      name: "System (ITSM Platform)"
      lane_type: "system"
    - id: "rules"
      name: "Decision Engine"
      lane_type: "decision"
  nodes:
    - id: "start"
      type: "start_event"
      lane: "human"
      x_in: 0.2
    - id: "receive_ticket"
      type: "user_task"
      lane: "human"
      x_in: 1.2
      label: "Receive Ticket"
    - id: "auto_classify"
      type: "service_task"
      lane: "system"
      x_in: 2.5
      label: "Auto-Classify"
    - id: "eval_priority"
      type: "business_rule_task"
      lane: "rules"
      x_in: 3.8
      label: "Evaluate Priority"
    - id: "resolve_gw"
      type: "exclusive_gateway"
      lane: "human"
      x_in: 5.0
      label: "Can resolve?"
    - id: "investigate"
      type: "user_task"
      lane: "human"
      x_in: 6.2
      label: "Investigate"
      y_branch: 0
    - id: "escalate"
      type: "service_task"
      lane: "system"
      x_in: 6.2
      label: "Auto-Escalate"
      y_branch: 1
    - id: "resolve"
      type: "user_task"
      lane: "human"
      x_in: 7.5
      label: "Resolve & Close"
    - id: "end"
      type: "end_event"
      lane: "system"
      x_in: 8.8
  flows:
    - {from: "start", to: "receive_ticket"}
    - {from: "receive_ticket", to: "auto_classify"}
    - {from: "auto_classify", to: "eval_priority"}
    - {from: "eval_priority", to: "resolve_gw"}
    - {from: "resolve_gw", to: "investigate", label: "Yes"}
    - {from: "resolve_gw", to: "escalate", label: "No"}
    - {from: "investigate", to: "resolve"}
    - {from: "escalate", to: "resolve"}
    - {from: "resolve", to: "end"}
  boundary_events:
    - id: "sla_timer"
      type: "timer_boundary"
      attached_to: "investigate"
      interrupting: false
      label: "SLA 4h"
  automation_summary:
    human_tasks: 3
    system_tasks: 2
    decision_tasks: 1
    automation_pct: 50
```

## QA Checklist

- [ ] Lanes clearly separate Human / System / Decision responsibilities
- [ ] Task type icons visible (👤/⚙/📋) in each task box
- [ ] Cross-lane flows show integration points
- [ ] At least 1 task in each defined Lane
- [ ] SLA/Timer boundary events on long-running human tasks if applicable
- [ ] Automation % annotation present (optional but recommended)
- [ ] Colors from ctx.colors
