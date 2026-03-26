# Application Architecture Diagram Catalog

Layer: TOGAF Layer 2 — Application Architecture  
Total Specs: 11  
Cloudwise Palette: #00CCD7 / #53E3EB / #2F2F2F / #A5A7AA / #44546A  
Audience: Application Architect, Solution Architect, Developer, Product Manager, Integration Team

---

## Diagram Index

| ID | File | Chinese Name | Primary Audience | Best For |
|----|------|-------------|-----------------|---------|
| AA-01 | [application-landscape.md](application-landscape.md) | 应用全景图 | CTO, Architect | IT portfolio overview, application rationalization |
| AA-02 | [component-diagram.md](component-diagram.md) | 应用组件图 | Developer, Architect | Internal component structure, module decomposition |
| AA-03 | [integration-map.md](integration-map.md) | 集成与接口地图 | Integration Team | System integration, API landscape, middleware |
| AA-04 | [bounded-context-map.md](bounded-context-map.md) | 限界上下文图 | DDD Architect | Domain-driven design, bounded context mapping |
| AA-05 | [service-interaction.md](service-interaction.md) | 服务交互图 | Architect, Developer | Service collaboration, runtime interaction |
| AA-06 | [api-dependency-graph.md](api-dependency-graph.md) | API 依赖关系图 | Developer, SRE | API coupling, dependency risk, versioning |
| AA-07 | [event-driven-architecture.md](event-driven-architecture.md) | 事件驱动架构图 | Architect | Event streams, producers/consumers, async flows |
| AA-08 | [microservice-decomposition.md](microservice-decomposition.md) | 微服务分解图 | Platform Architect | Microservice boundary design, domain grouping |
| AA-09 | [app-capability-mapping.md](app-capability-mapping.md) | 应用-能力覆盖图 | Architect, Analyst | App-to-capability traceability, gap identification |
| AA-10 | [application-sequence-flow.md](application-sequence-flow.md) | 应用序列流图 | Developer, Architect | Runtime flow, request-response chains, debugging |
| AA-11 | [product-capability-map.md](product-capability-map.md) | 分层产品能力架构图 | Product Architect, Architect | Layered product architecture, shared capability planning |

---

## Selection Guide

```
Input intent → Recommended diagram

Full IT portfolio, rationalization, portfolio view   → AA-01 Application Landscape
Component internals, module decomposition            → AA-02 Component Diagram
System integration, middleware, ETL, APIs            → AA-03 Integration Map
DDD bounded contexts, domain boundaries              → AA-04 Bounded Context Map
Service collaboration, runtime calls                 → AA-05 Service Interaction
API coupling, versioning, dependency risk            → AA-06 API Dependency Graph
Event-driven flows, message queues, Kafka            → AA-07 Event-Driven Architecture
Microservice decomposition, grouping, sizing         → AA-08 Microservice Decomposition
App-to-capability traceability, coverage gaps        → AA-09 App-Capability Mapping
Runtime sequence, request-response, step-by-step    → AA-10 Application Sequence Flow
Layered product architecture, domestic-style layering → AA-11 Product Capability Map (Layered)
```

---

## Shared Constraints (All AA Diagrams)

1. Application boxes use standard rectangle with system name; no technology logo images inside shapes
2. All connectors are directed (arrowhead) to indicate call direction or event flow
3. External systems outside the architecture boundary use gray (#A5A7AA) fill
4. Internal systems use cyan (#00CCD7) fill for primary and (#53E3EB) for secondary
5. Boundary regions use dashed borders, not solid lines, to differentiate from data flow
