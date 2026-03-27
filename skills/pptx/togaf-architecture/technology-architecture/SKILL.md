# Technology Architecture Skill (TOGAF Layer 4)

This skill covers platform layers, deployment topology, network/security zones, and infrastructure dependencies.

## Scope

Use this skill when users ask for:
- infrastructure topology and platform design
- deployment architecture (container, VM, serverless)
- network zoning and security architecture
- cloud architecture (multi-cloud, hybrid, landing zone)
- Kubernetes/container orchestration design
- monitoring and observability stack
- disaster recovery and business continuity
- platform capability mapping

Do not use this skill for business process flows, application logic, or data modeling.

## Mandatory Rules

1. Title/subtitle must use master placeholders first.
2. Rounded rectangle corners stay small.
3. No decorative-only shapes/lines; each connector must represent a relationship.
4. Geometry constants are authored on base canvas 10.0\" x 5.625\" and must adapt to active master size at render time.
5. Colors must come from active theme tokens; dark mode must preserve contrast by separating connector/edge color and body text color.
6. Topology/dependency/replication connectors default to curved style unless strict notation requires another connector type.
7. Release candidate decks must pass business overflow gate with raw overflow = 0 and business overflow = 0.

## Diagram Catalog (Must Support)

1. Infrastructure Topology — physical/virtual compute, storage, network topology
2. Deployment Architecture — deployment units, environments, CI/CD pipeline
3. Network Zoning — network segments, firewalls, DMZ, trust boundaries
4. Cloud Architecture — cloud service mapping, landing zones, well-architected
5. Container Orchestration — Kubernetes clusters, namespaces, pods, services
6. Security Architecture — security domains, controls, zero-trust, defense layers
7. Monitoring & Observability — metrics/logs/traces pipelines, SLO/SLI monitoring
8. Disaster Recovery — DR topology, RTO/RPO targets, failover design
9. Platform Capability Map — platform services taxonomy and maturity

## Diagram Specifications

All diagrams in this skill have dedicated production-level specs with layout variants, color semantics, typography, anti-patterns, and industry references.

See `diagrams/` subdirectory:

- [TA-01: Infrastructure Topology](diagrams/infrastructure-topology.md)
- [TA-02: Deployment Architecture](diagrams/deployment-architecture.md)
- [TA-03: Network Zoning](diagrams/network-zoning.md)
- [TA-04: Cloud Architecture](diagrams/cloud-architecture.md)
- [TA-05: Container Orchestration](diagrams/container-orchestration.md)
- [TA-06: Security Architecture](diagrams/security-architecture.md)
- [TA-07: Monitoring & Observability](diagrams/monitoring-observability.md)
- [TA-08: Disaster Recovery](diagrams/disaster-recovery.md)
- [TA-09: Platform Capability Map](diagrams/platform-capability-map.md)

See [diagrams/_catalog.md](diagrams/_catalog.md) for selection guide.

## Selection Logic

- If request mentions infra/server/compute/storage: prioritize infrastructure-topology.
- If request mentions deploy/CI-CD/pipeline/environment: prioritize deployment-architecture.
- If request mentions network/firewall/DMZ/zone: prioritize network-zoning.
- If request mentions cloud/AWS/Azure/GCP/landing zone: prioritize cloud-architecture.
- If request mentions Kubernetes/container/pod/helm: prioritize container-orchestration.
- If request mentions security/zero-trust/IAM/compliance: prioritize security-architecture.
- If request mentions monitoring/observability/SRE/alerts: prioritize monitoring-observability.
- If request mentions DR/disaster/recovery/RTO/RPO/failover: prioritize disaster-recovery.
- If request mentions platform/capability/IDP/golden path: prioritize platform-capability-map.

## QA Checklist

- Are all connectors semantic (data flow/dependency/replication) rather than decorative?
- Are page titles/subtitles in placeholders?
- Are environment/region/zone boundaries clearly drawn?
- Are infrastructure sizing and capacity notes included where relevant?
- Does dark theme keep readable contrast for lines, labels, and grouped regions?
- Do dependency/topology connectors follow curved style by default where applicable?
- Is business overflow check passing (raw=0 and business=0)?
