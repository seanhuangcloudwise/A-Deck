# Technology Architecture Diagram Catalog

Layer: TOGAF Layer 4 — Technology Architecture  
Total Specs: 9  
Cloudwise Palette: #00CCD7 / #53E3EB / #2F2F2F / #A5A7AA / #44546A  
Audience: Infrastructure Engineer, DevOps, SRE, Cloud Architect, Security Engineer, CTO

---

## Diagram Index

| ID | File | Chinese Name | Primary Audience | Best For |
|----|------|-------------|-----------------|---------|
| TA-01 | [infrastructure-topology.md](infrastructure-topology.md) | 基础设施拓扑图 | SRE, Infra | Physical/logical infrastructure layout |
| TA-02 | [deployment-architecture.md](deployment-architecture.md) | 部署架构图 | DevOps, Architect | Application deployment across environments |
| TA-03 | [network-zoning.md](network-zoning.md) | 网络分区图 | Network, Security | Network segment design, zone isolation |
| TA-04 | [cloud-architecture.md](cloud-architecture.md) | 云架构图 | Cloud Architect | Multi-cloud, hybrid cloud, cloud-native design |
| TA-05 | [container-orchestration.md](container-orchestration.md) | 容器编排架构图 | Platform Eng, DevOps | Kubernetes cluster, pod/service/ingress design |
| TA-06 | [security-architecture.md](security-architecture.md) | 安全架构图 | Security, Compliance | Security domain, controls, zero-trust layout |
| TA-07 | [monitoring-observability.md](monitoring-observability.md) | 监控与可观测性图 | SRE, Ops | Observability stack, metrics/logs/traces coverage |
| TA-08 | [disaster-recovery.md](disaster-recovery.md) | 灾备架构图 | Infra, Risk | DR topology, RTO/RPO targets, failover design |
| TA-09 | [platform-capability-map.md](platform-capability-map.md) | 平台能力地图 | Platform Eng, CTO | Platform services taxonomy, capability coverage |

---

## Selection Guide

```
Input intent → Recommended diagram

Physical/logical node layout, rack diagrams          → TA-01 Infrastructure Topology
Deployment targets, environment mapping, CI/CD       → TA-02 Deployment Architecture
Network segments, firewall zones, VLANs              → TA-03 Network Zoning
AWS/Azure/GCP architecture, hybrid cloud design      → TA-04 Cloud Architecture
Kubernetes design, container layout, workloads       → TA-05 Container Orchestration
Security zones, IAM, zero-trust, controls            → TA-06 Security Architecture
Monitoring stack, SLO coverage, traces/logs/metrics  → TA-07 Monitoring & Observability
DR failover, backup strategy, RTO/RPO targets        → TA-08 Disaster Recovery
Platform service catalog, capability coverage gaps   → TA-09 Platform Capability Map
```

---

## Shared Constraints (All TA Diagrams)

1. Infrastructure nodes use labeled rectangle boxes — do NOT use vendor icon images as primary shapes
2. Network boundaries use dashed-border containers with zone label; solid rectangles for compute nodes
3. Zone hierarchy: Internet → DMZ → Application Zone → Data Zone — always flows left/top-to-right/bottom
4. Redundant components are shown with shadow duplication (two overlapping shapes offset 4pt) or explicit replica labels
5. Security controls (firewall, WAF, IAM) are shown as separate annotated shapes — never implied
