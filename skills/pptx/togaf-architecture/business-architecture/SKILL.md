# Business Architecture Skill (TOGAF Layer 1)

Priority skill for architecture storytelling from business perspective.

## Scope

Use this skill when users ask for:
- business capability planning
- value delivery and process optimization
- organization/role collaboration
- KPI alignment and governance
- business transformation (As-Is vs To-Be)

Do not default to technical topology diagrams in this skill.

## Mandatory Rules

1. Title/subtitle must use master placeholders first.
2. Rounded rectangle corners stay small.
3. No decorative-only shapes/lines; each connector must represent a relationship.
4. BA-03 swimlane/process diagrams must follow layout-first rules: uniform activity sizing by default, cross-lane center alignment for related nodes, even horizontal distribution across the lane canvas, and explicit standalone space reservation for start/end event nodes.
5. Geometry constants are authored on base canvas 10.0\" x 5.625\" and must adapt to active master size at render time.
6. Colors must come from active theme tokens; dark mode must preserve contrast by separating connector/edge color and body text color.
7. Process/interaction connectors default to curved style unless strict notation requires another connector type.
8. Release candidate decks must pass business overflow gate with raw overflow = 0 and business overflow = 0.

## Diagram Catalog (Must Support)

1. Capability Map
- Purpose: show capability landscape and maturity focus
- Structure: domain -> capability block matrix
- Minimum input: domains[], capabilities[], maturity(optional)

2. Value Stream
- Purpose: show customer/business value delivery stages
- Structure: stage chain + output/value per stage
- Minimum input: stages[], outputs[], kpis(optional)

3. Business Process (L1/L2)
- Purpose: show process steps and ownership
- Structure: swimlane or linear flow with decisions
- Minimum input: steps[], owners[], decisions(optional)
- Layout defaults: equal-sized activity boxes unless text forces an exception; arrows must be directional; cross-lane handoff nodes should align vertically when semantically paired; start/end events must count as occupied layout nodes rather than being visually appended at the edge.

4. Organization & Actor Interaction
- Purpose: show cross-role collaboration and responsibilities
- Structure: role nodes + interaction edges
- Minimum input: roles[], interactions[]

5. Business Service Decomposition
- Purpose: break services from capability to service units
- Structure: root service -> sub-services hierarchy
- Minimum input: service_root, service_groups[]

6. Function-to-Capability Mapping
- Purpose: map functions to capabilities and gaps
- Structure: matrix or bipartite map
- Minimum input: functions[], capabilities[], mappings[]

7. As-Is / To-Be Comparison
- Purpose: baseline vs target business model
- Structure: dual-column comparison blocks
- Minimum input: as_is[], to_be[], delta[]

8. Scenario Journey
- Purpose: describe scenario path and friction points
- Structure: journey timeline with touchpoints
- Minimum input: stages[], actors[], painpoints[], outcomes[]

9. KPI-to-Objective Alignment
- Purpose: connect goals, metrics, and owners
- Structure: objective -> KPI -> target -> owner chains
- Minimum input: objectives[], kpis[], targets[], owners[]

10. RACI Governance Matrix
- Purpose: clarify accountability
- Structure: activity x role matrix with R/A/C/I marks
- Minimum input: activities[], roles[], raci_cells[]

## Slide Blueprint (Recommended 10-14 pages)

1. Cover
2. Business context and goals
3. Capability map
4. Value stream
5. Process L1/L2
6. Org and actor interaction
7. Service decomposition
8. Function-capability mapping
9. As-Is / To-Be
10. KPI alignment
11. RACI matrix
12. Summary and next actions

## Selection Logic

- If audience contains management/executive: prioritize capability map, value stream, KPI alignment.
- If audience contains operations/business team: prioritize process, scenario journey, RACI.
- If request contains transformation keywords: include As-Is/To-Be and function-capability mapping.

## Diagram Specifications

All diagrams in this skill have dedicated production-level specs with layout variants, color semantics, typography, anti-patterns, and industry references.

See `diagrams/` subdirectory:

- [BA-01: Capability Map](diagrams/capability-map.md)
- [BA-02: Value Stream](diagrams/value-stream.md)
- [BA-03: Business Process L1/L2](diagrams/business-process.md)
- [BA-04: Organization & Actor Interaction](diagrams/actor-interaction.md)
- [BA-05: Business Service Decomposition](diagrams/service-decomposition.md)
- [BA-06: Function-to-Capability Mapping](diagrams/function-capability-mapping.md)
- [BA-07: As-Is / To-Be Comparison](diagrams/as-is-to-be.md)
- [BA-08: Scenario Journey](diagrams/scenario-journey.md)
- [BA-09: KPI-to-Objective Alignment](diagrams/kpi-alignment.md)
- [BA-10: RACI Governance Matrix](diagrams/raci-matrix.md)

See [diagrams/_catalog.md](diagrams/_catalog.md) for selection guide.

## QA Checklist

- Are all connectors semantic (flow/dependency/ownership) rather than decorative?
- Are page titles/subtitles in placeholders?
- Is there at least one business meaning per shape group?
- Are business terms consistent (capability/process/service/role/KPI)?
- Is each diagram explainable in one sentence by presenter?
- Does dark theme keep readable contrast for lines, labels, and grouped regions?
- Do process/interaction connectors follow curved style by default where applicable?
- Is business overflow check passing (raw=0 and business=0)?

## Failure Fallbacks

- If graph complexity is too high: split into two slides by domain or stage.
- If data is incomplete: render simplified diagram and list missing fields explicitly.
- If layout cannot avoid overlap: switch to matrix or layered blocks instead of dense network.
