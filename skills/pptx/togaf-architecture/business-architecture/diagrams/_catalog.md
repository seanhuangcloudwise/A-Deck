# Business Architecture Diagram Catalog

Layer: TOGAF Layer 1 — Business Architecture  
Total Specs: 10  
Cloudwise Palette: #00CCD7 / #53E3EB / #2F2F2F / #A5A7AA / #44546A  
Audience: Executive, Strategy, Operations, Business Analyst, Enterprise Architect

---

## Diagram Index

| ID | File | Chinese Name | Primary Audience | Best For |
|----|------|-------------|-----------------|---------|
| BA-01 | [capability-map.md](capability-map.md) | 业务能力地图 | C-suite, Strategy | Strategic portfolio review, transformation planning |
| BA-02 | [value-stream.md](value-stream.md) | 价值流图 | Business, Operations | Value delivery analysis, process sequencing |
| BA-03 | [business-process.md](business-process.md) | 业务流程图 L1/L2 | Operations, Analyst | Process documentation, SOP, swimlane analysis |
| BA-04 | [actor-interaction.md](actor-interaction.md) | 组织与角色协作图 | Management, HR | Cross-role collaboration, responsibility mapping |
| BA-05 | [service-decomposition.md](service-decomposition.md) | 业务服务分解图 | Architect, Product | Service catalog design, business domain breakdown |
| BA-06 | [function-capability-mapping.md](function-capability-mapping.md) | 功能-能力映射图 | Architect, Analyst | Gap analysis, capability realization assessment |
| BA-07 | [as-is-to-be.md](as-is-to-be.md) | As-Is / To-Be 对比图 | Management, Sponsor | Business transformation, before-after communication |
| BA-08 | [scenario-journey.md](scenario-journey.md) | 业务场景旅程图 | Product, UX, Sales | Scenario storytelling, pain-point identification |
| BA-09 | [kpi-alignment.md](kpi-alignment.md) | KPI-业务目标对齐图 | Executive, PMO | OKR alignment, performance management communication |
| BA-10 | [raci-matrix.md](raci-matrix.md) | 业务治理责任矩阵 | Management, Governance | Accountability clarity, cross-team governance |

---

## Selection Guide

```
Input intent → Recommended diagram

Strategic planning, capability gap analysis        → BA-01 Capability Map
End-to-end value delivery, customer journey        → BA-02 Value Stream
SOP, workflow, process step documentation          → BA-03 Business Process
Roles, actors, collaboration, responsibility       → BA-04 Actor Interaction
Service decomposition, business domain split       → BA-05 Service Decomposition
Capability realization, IT-business alignment      → BA-06 Function-Capability Mapping
Transformation, before-after, change impact        → BA-07 As-Is / To-Be
Scenario storytelling, UX pain-points              → BA-08 Scenario Journey
OKR, KPI, target alignment, performance review     → BA-09 KPI Alignment
Governance, accountability, RACI, decision rights  → BA-10 RACI Matrix
```

---

## Shared Constraints (All BA Diagrams)

1. Titles and subtitles MUST use slide layout placeholders (idx=0 for title, idx=1 for subtitle)
2. All rounded rectangle corners ≤ 6pt radius
3. Every shape must carry semantic meaning; no decorative lines or borders
4. Cloudwise color palette is mandatory — no ad-hoc colors
5. Connectors must represent directional flow, dependency, or ownership — never used as visual separators
