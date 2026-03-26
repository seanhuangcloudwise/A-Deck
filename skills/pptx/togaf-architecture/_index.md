# TOGAF Architecture Skills Index

This folder contains four architecture skills aligned to TOGAF layers, each with production-level diagram specifications.

## Skills

| Layer | Skill | Diagrams | Spec Files |
|---|---|---|---|
| 1 - Business | `business-architecture` | 10 diagram types | [BA-01 ~ BA-10](business-architecture/diagrams/_catalog.md) |
| 2 - Application | `application-architecture` | 11 diagram types | [AA-01 ~ AA-11](application-architecture/diagrams/_catalog.md) |
| 3 - Data | `data-architecture` | 8 diagram types | [DA-01 ~ DA-08](data-architecture/diagrams/_catalog.md) |
| 4 - Technology | `technology-architecture` | 9 diagram types | [TA-01 ~ TA-09](technology-architecture/diagrams/_catalog.md) |

**Total: 38 diagram types with production-level specifications.**

## Parallel Domains

| Domain | Skill | Diagrams | Spec Files |
|---|---|---|---|
| Product Planning | `roadmap-architecture` | 10 diagram types | [RA-01 ~ RA-10](../roadmap-architecture/diagrams/_catalog.md) |
| GTM Communication | `gtm-architecture` | 17 diagram types | [GM-01 ~ GM-17](../gtm-architecture/diagrams/_catalog.md) |

The `roadmap-architecture` domain focuses on product planning visualization: strategic timelines, portfolio prioritization, KPI tracking, dependency/release management, governance gates, and scenario-based investment views.

The `gtm-architecture` domain covers Go-to-Market communication diagrams: value proposition, competitive positioning, solution architecture, ROI proof, GTM strategy, and category/analyst narrative — used in white papers, solution briefs, battle cards, and market PR materials.

Routing hint: When the request is about roadmap, release plan, initiative prioritization, KPI milestone, governance gate, risk board, capability evolution, or investment scenario → route to `roadmap-architecture`.

Routing hint: When the request is about market positioning, buyer persuasion, competitive differentiation, solution storytelling, ROI business case, customer journey, ICP segmentation, GTM strategy, or analyst briefing → route to `gtm-architecture`.

## Loader Architecture (Data Driven)

TOGAF architecture now supports a registry-based loader mechanism:

- `skills/pptx/togaf-architecture/loaders/common.py`: shared rendering logic
- `skills/pptx/togaf-architecture/loaders/ba_loader.py|aa_loader.py|da_loader.py|ta_loader.py`: layer-specific loaders
- `skills/pptx/togaf-architecture/loaders/registry.py`: 38 diagram IDs mapped to loaders
- `projects/togaf-architecture-full-demo/generate.py`: dynamic orchestrator using YAML config
- `projects/togaf-architecture-full-demo/data/config_template.yaml`: externalized content template

Pattern:

`config.yaml -> registry -> loader -> slide`

## Global Rules (Mandatory)

1. Titles and subtitles must use layout placeholders first.
2. Rounded rectangle corner radius must be small by default.
3. No decorative-only shapes or lines. Every line must carry semantics.
4. All visual colors (fill, line, text) must come from the active master theme via `ctx.colors` / `ctx.palette`. Only TOGAF-spec reserved semantic colors (RACI R/A/C/I, journey emotion +/~/−) may be loader-defined, and those are also derived from theme accents via `_semantic_from_theme()`.

## Routing Hint

When the request is strategy/process/organization/value oriented, route to `business-architecture` first.
When the request is app interaction/API/integration, route to `application-architecture`.
When the request is data domain/lineage/lifecycle, route to `data-architecture`.
When the request is deployment/platform/network/security-zone, route to `technology-architecture`.

## Cross-Layer Traceability

| Business Architecture | Application Architecture | Data Architecture | Technology Architecture |
|---|---|---|---|
| BA-01 Capability Map | AA-09 App-Capability Mapping | DA-04 Data Domain Map | TA-09 Platform Capability Map |
| BA-02 Value Stream | AA-01 Application Landscape | DA-03 Data Flow Diagram | TA-02 Deployment Architecture |
| BA-03 Business Process | AA-10 Application Sequence Flow | DA-03 Data Flow Diagram | TA-01 Infrastructure Topology |
| BA-04 Actor Interaction | AA-05 Service Interaction | DA-05 Data Governance Framework | TA-06 Security Architecture |
| BA-05 Service Decomposition | AA-08 Microservice Decomposition | DA-01 Conceptual Data Model | TA-05 Container Orchestration |
| BA-06 Function-Capability Mapping | AA-02 Component Diagram | DA-04 Data Domain Map | TA-09 Platform Capability Map |
| BA-07 As-Is / To-Be | AA-03 Integration Map | DA-07 Data Lineage | TA-04 Cloud Architecture |
| BA-08 Scenario Journey | AA-04 Bounded Context Map | DA-06 Master Data Lifecycle | TA-07 Monitoring & Observability |
| BA-09 KPI Alignment | AA-06 API Dependency Graph | DA-08 Data Catalog Structure | TA-07 Monitoring & Observability |
| BA-10 RACI Matrix | AA-07 Event-Driven Architecture | DA-05 Data Governance Framework | TA-08 Disaster Recovery |
| BA-01 Capability Map | AA-11 Product Capability Map (Layered) | DA-04 Data Domain Map | TA-09 Platform Capability Map |

Use this table to identify which diagrams across layers should be built together for a complete architecture story.
