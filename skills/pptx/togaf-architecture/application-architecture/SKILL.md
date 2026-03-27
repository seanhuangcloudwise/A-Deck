# Application Architecture Skill (TOGAF Layer 2)

This skill covers application collaboration, communication, interface dependency, and app-to-business mapping.

## Scope

Use this skill when users ask for:
- application landscape and portfolio visualization
- component or microservice decomposition
- integration and interface mapping
- bounded context design (DDD)
- API dependency analysis
- event-driven architecture design
- application-to-capability alignment

Do not use this skill for infrastructure topology, network design, or data modeling.

## Mandatory Rules

1. Title/subtitle must use master placeholders first.
2. Rounded rectangle corners stay small.
3. No decorative-only shapes/lines; each connector must represent a relationship.
4. Geometry constants are authored on base canvas 10.0\" x 5.625\" and must adapt to active master size at render time.
5. Colors must come from active theme tokens; dark mode must preserve contrast by separating connector/edge color and body text color.
6. Sequence/integration/dependency connectors default to curved style unless strict notation requires another connector type.
7. Release candidate decks must pass business overflow gate with raw overflow = 0 and business overflow = 0.

## Diagram Catalog (Must Support)

1. Application Landscape — portfolio view of all apps with lifecycle status
2. Component Diagram — internal modules/classes of a single app
3. Integration Map — inter-system interfaces and protocols
4. Bounded Context Map (DDD) — context boundaries and relationships
5. Service Interaction — synchronous/async call graph between services
6. API Dependency Graph — API provider-consumer dependency chain
7. Event-Driven Architecture — event producers, brokers, consumers
8. Microservice Decomposition — service cut from monolith
9. Application-to-Capability Mapping — app portfolio → business capability overlay
10. Application Sequence Flow — time-ordered interaction (sequence diagram)
11. Product Capability Map (Layered) — layered product architecture and shared capability boundaries

## Diagram Specifications

All diagrams in this skill have dedicated production-level specs with layout variants, color semantics, typography, anti-patterns, and industry references.

See `diagrams/` subdirectory:

- [AA-01: Application Landscape](diagrams/application-landscape.md)
- [AA-02: Component Diagram](diagrams/component-diagram.md)
- [AA-03: Integration Map](diagrams/integration-map.md)
- [AA-04: Bounded Context Map](diagrams/bounded-context-map.md)
- [AA-05: Service Interaction](diagrams/service-interaction.md)
- [AA-06: API Dependency Graph](diagrams/api-dependency-graph.md)
- [AA-07: Event-Driven Architecture](diagrams/event-driven-architecture.md)
- [AA-08: Microservice Decomposition](diagrams/microservice-decomposition.md)
- [AA-09: Application-to-Capability Mapping](diagrams/app-capability-mapping.md)
- [AA-10: Application Sequence Flow](diagrams/application-sequence-flow.md)
- [AA-11: Product Capability Map (Layered)](diagrams/product-capability-map.md)

See [diagrams/_catalog.md](diagrams/_catalog.md) for selection guide.

## Selection Logic

- If request mentions apps/portfolio/landscape: prioritize application-landscape, app-capability-mapping.
- If request mentions API/integration/interface: prioritize integration-map, api-dependency-graph.
- If request mentions microservice/DDD/bounded context: prioritize bounded-context-map, microservice-decomposition.
- If request mentions event/message/async: prioritize event-driven-architecture.
- If request mentions sequence/flow/call chain: prioritize service-interaction, application-sequence-flow.
- If request mentions layered product architecture/分层产品架构/产品能力分层: prioritize product-capability-map.

## QA Checklist

- Are all connectors semantic (call/event/dependency) rather than decorative?
- Are page titles/subtitles in placeholders?
- Is protocol or interface type labeled on every integration arrow?
- Are application lifecycle statuses shown where appropriate?
- Does dark theme keep readable contrast for lines, labels, and grouped regions?
- Do flow/interaction connectors follow curved style by default where applicable?
- Is business overflow check passing (raw=0 and business=0)?
