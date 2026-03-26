# TA-04: Cloud Architecture Diagram — Technology Architecture Diagram Spec

_Ref: AWS Well-Architected Framework | Azure Architecture Center | Google Cloud Architecture Framework | TOGAF Phase D_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing how workloads, services, and data are organized within a cloud provider's infrastructure — including regions, availability zones, VPC/VNet design, managed services, and connectivity to on-premises or other clouds.

**Use When**:
- Designing cloud-native or cloud-migrated architectures
- Presenting cloud platform design to technical and executive audiences
- Cloud vendor selection: comparing architectural patterns
- Well-Architected review: validating against reliability, security, performance pillars
- Cost optimization planning: showing resource organization for tagging and cost attribution

**Questions Answered**:
- How is the cloud infrastructure organized (regions, AZs, VPCs)?
- Which managed cloud services are used for each workload?
- How does the cloud environment connect to on-premises?
- Which components are deployed in which availability zones for resilience?

**Primary Audience**: Cloud Architects, DevOps/Platform Engineers, Solution Architects, CTO

---

## 2. Visual Layout Specification

**Structure**: Cloud region/account container with VPC/subnet sub-zones.

### Variant A: Single Cloud Region
- Cloud region boundary (outer dashed container)
- Inside: VPC/VNet with public and private subnets
- Per subnet: compute resources, load balancers, databases
- Best for: Standard cloud application design

### Variant B: Multi-Region / Multi-AZ
- Two region columns (Primary + DR)
- Each region shows AZ zones (AZ-1, AZ-2, AZ-3)
- Cross-region replication arrows
- Best for: High availability and disaster recovery design

### Variant C: Multi-Cloud / Hybrid
- Left: On-premises block
- Center: Cloud provider A
- Right: Cloud provider B (or additional cloud)
- Interconnects: VPN, Dedicated Connect, Interconnect
- Best for: Multi-cloud strategy, hybrid cloud migration

**Grid Proportions**:
- Region container: fills 85% of content area
- VPC inner container: 90% of region with 20pt padding
- Subnet block: horizontal bands within VPC
- Availability zone indicator: vertical division lines in subnet

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Cloud region boundary | Cloud provider scope | `#00CCD7` dashed outer container |
| VPC / VNet | Virtual network boundary | `#53E3EB` dashed container |
| Public subnet | Internet-accessible | `#44546A` |
| Private subnet | No direct internet access | `#2F2F2F` |
| On-premises zone | Datacenter boundary | `#A5A7AA` container |
| Managed service | Cloud PaaS/SaaS | `#00CCD7` service block |
| Compute resource | VM / container / function | White + `#2F2F2F` border |
| Storage service | Object/block/file | `#2F2F2F` cylinder |
| Connectivity service | VPN / DX / Interconnect | `#44546A` bold line |
| Availability zone | Within-region isolation | Dashed vertical dividers |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Region/Account Label | Cloud scope header | 12pt | Bold, `#44546A` |
| VPC/Subnet Label | Network boundary | 10pt | SemiBold |
| Service Name | Managed service block | 9pt | SemiBold, White |
| AZ Label | Availability zone indicator | 9pt | Regular, `#A5A7AA` |
| Resource Label | Compute instance name | 8pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Outer dashed rectangle | Cloud region / account boundary |
| Inner dashed rectangle | VPC / VNet |
| Horizontal band | Public / private subnet |
| Vertical dashed line | Availability zone boundary |
| Standard rect | Virtual machine or instance |
| Small hexagon / rounded rect | Managed cloud service |
| Cylinder | Managed database service |
| Cloud shape | External SaaS or internet |
| Zigzag line or VPN icon | VPN/Direct Connect |
| Global load balancer | Multi-region entry point |

---

## 6. Annotation Rules

- **Region label**: "us-east-1 (Primary)" or "EU-West-1 (DR)" in region header
- **Service tier tags**: "t3.large × 3", "RDS Multi-AZ"
- **SLA annotation**: Critical services: "SLA: 99.99%" or "0 RPO"
- **Cost tier**: Optional: $ / $$ / $$$ annotation on resource groups for cost planning
- **AZ distribution**: Each compute resource shows which AZ it's in: `[AZ-1a]`, `[AZ-1b]`

---

## 7. Content Density Rules

| Mode | Services | Zones | Per Slide |
|---|---|---|---|
| Minimum | 4 | 2 (1 VPC) | — |
| Optimal | 10–20 | 2–3 regions | single slide |
| Maximum | 35 | 4 regions | → split by workload cluster |

**Overflow Strategy**: Split by workload cluster. Customer-facing workloads on one slide; backend/data workloads on another. Add a master multi-region overview slide.

---

## 8. Anti-Patterns

1. **Single-AZ deployment**: Showing all compute in one availability zone — this is a high-availability anti-pattern. Always show multi-AZ distribution for production workloads.
2. **No VPC/subnet structure**: Placing all services inside a single "cloud" rectangle without subnet boundaries — VPC design is the foundation of cloud security.
3. **Missing connectivity for hybrid**: Hybrid cloud diagrams without explicit Direct Connect or VPN elements — the connectivity path is the most critical design decision.
4. **All services in public subnet**: Services that should be internal (databases, backend APIs) shown in public subnet — database instances must always be in private subnets.
5. **No managed service distinction**: Treating managed cloud services (RDS, S3, Lambda) identically to custom compute — visual distinction highlights the operational model difference.

---

## 9. Industry Reference Patterns

**AWS Well-Architected Framework — Reliability Pillar**:
AWS recommends multi-AZ deployment for all production workloads: compute across ≥ 2 AZs, databases with Multi-AZ standbys or Aurora global clusters, application load balancers spanning all AZs. For RPO=0 / RTO<1hr: active-active multi-region. The cloud architecture diagram is the validation artifact for reliability pillar review.

**Azure Landing Zone Architecture**:
Microsoft's Landing Zone design organizes cloud resources in a hierarchical structure: Management Group → Subscription → Resource Group → Resources. The networking pattern: Hub-Spoke VNet topology with central hub containing shared services (firewall, VPN gateway, DNS) and spokes containing workload VNets. This maps to Variant A with a hub-spoke VPC design.

**Google Cloud — Shared VPC Architecture**:
GCP's recommended enterprise pattern uses Shared VPC: a host project owns the VPC and subnets; service projects contain workloads. This centralized network design allows isolation of billing and IAM while sharing network infrastructure. Variant C with GCP shows: Host Project VPC (center) + Service Projects as connected workload blocks.

---

## 10. Production QA Checklist

- [ ] Cloud region boundary is clearly drawn with region label
- [ ] VPC/VNet structure is shown with public and private subnet bands
- [ ] Availability zone distribution shown for all production compute
- [ ] Database services are in private subnet (not public)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Connectivity to on-premises (if hybrid) shows VPN or Direct Connect explicitly
- [ ] Multi-AZ and multi-region services have AZ/region labels
- [ ] Internet gateway / NAT gateway shown for public subnet traffic
- [ ] Managed services distinguished from custom compute
- [ ] Presenter can explain the HA design in 45 seconds from the diagram
