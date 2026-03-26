# TA-01: Infrastructure Topology Map — Technology Architecture Diagram Spec

_Ref: TOGAF ADM Phase D (Technology Architecture) | IEEE 1471 | Gartner Infrastructure Reference Architecture_

---

## 1. Purpose & When to Use

**Definition**: A high-level map showing the physical and logical infrastructure components — servers, networks, storage, and their interconnections — organized by deployment zone or tier.

**Use When**:
- Documenting the current infrastructure state for architecture review
- Planning capacity changes, hardware refresh, or data center migrations
- Communicating infrastructure architecture to IT operations teams
- Supporting disaster recovery planning by showing topology dependencies
- Infrastructure security review: identifying single points of failure and exposure zones

**Questions Answered**:
- What infrastructure components exist and how are they connected?
- What are the network tiers and connectivity paths?
- Where are the redundancy points and single points of failure?
- Which components are on-premises vs. cloud vs. co-lo?

**Primary Audience**: Infrastructure Engineers, SRE teams, CTO, IT Operations Managers

---

## 2. Visual Layout Specification

**Structure**: Tiered zones from internet-facing to internal — top-to-bottom or left-to-right.

### Variant A: Standard Three-Tier Topology
- Internet → DMZ → Application Zone → Data Zone
- Each zone is a horizontal band with components inside
- Best for: Web application infrastructure

### Variant B: Multi-Site Topology
- Multiple site columns (Site A / Disaster Recovery Site / Cloud)
- Horizontal WAN/connection layer between sites
- Best for: Multi-datacenter or hybrid cloud

### Variant C: Cloud + On-Prem Hybrid
- Cloud region block (left or top)
- On-premises block (right or bottom)
- Connectivity: VPN / Direct Connect between them
- Best for: Cloud migration, hybrid cloud architecture

**Grid Proportions**:
- Zone band height: ~22% content area per zone
- Component node: 80pt × 40pt
- Network link stroke: 2pt
- Zone label column (left): 80pt wide

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Internet-facing zone | Public exposure | `#A5A7AA` |
| DMZ Zone | Semi-trusted perimeter | `#44546A` |
| Application zone | Internal trusted | `#00CCD7` |
| Data zone | High-security data tier | `#2F2F2F` |
| Cloud provider zone | AWS/Azure/GCP boundary | `#53E3EB` dashed container |
| On-premises zone | Physical datacenter | `#44546A` solid container |
| Component node | Server, appliance | White fill + `#2F2F2F` border |
| Network link | Connectivity path | `#2F2F2F` solid |
| High-bandwidth link | Dedicated connection | `#00CCD7` thick solid |
| Redundant pair | HA component | Shadow-offset duplicated box |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Zone Label | Tier/zone name | 11pt | Bold, White |
| Component Label | Node identifier | 9pt | SemiBold |
| Component Type | Server/LB/FW tag | 7pt | Regular italic |
| Network Link Label | Protocol/bandwidth | 8pt | Regular |
| Site Label (Variant B) | Site name header | 12pt | Bold, `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rectangle | Server or compute node |
| Trapezoid or cloud shape | Cloud service |
| Half-cylinder | Load balancer |
| Shield / wedge | Firewall |
| Cylinder | Storage array |
| Cylinder (short) | Database |
| Horizontal zone band | Network tier boundary |
| Dashed container | Cloud or external boundary |
| Solid line | Network connection |
| Wavy line | Internet connection |
| Double-line | High-availability link |
| `[x2]` or shadow offset | Redundant component pair |

**Connector Rule**: Use straight horizontal/vertical lines only — avoid diagonal wiring. Network connections must show directionality when asymmetric (e.g., DMZ → App is allowed, App → DMZ is blocked).

---

## 6. Annotation Rules

- **Bandwidth labels**: Network links annotated: "1Gbps", "10Gbps", "100Mbps"
- **Redundancy notation**: HA pairs labeled `[Active]` / `[Standby]` or `[x2]`
- **Component specs**: Optional: "4 vCPU / 16GB / 500GB SSD" annotation
- **Port/protocol**: Firewall links: "Port 443 HTTPS", "Port 5432 DB"
- **Single-point-of-failure marker**: `⚠ SPOF` annotation on non-redundant critical components

---

## 7. Content Density Rules

| Mode | Components | Zones | Per Slide |
|---|---|---|---|
| Minimum | 4 | 2 | — |
| Optimal | 10–20 | 3–5 | 20 components max |
| Maximum | 35 | 6 | → split by zone cluster |

**Overflow Strategy**: Split by zone pair (Internet + DMZ on one slide; App + Data on another). Always maintain inter-zone connectors on each slide with stubs pointing off-slide.

---

## 8. Anti-Patterns

1. **No zone separation**: All components flat on a slide with no network tier structure — loses the security and trust boundary information.
2. **Vendor logos as shapes**: Using vendor product logos (Cisco, VMware, Dell) as shape elements — use abstract shapes; vendor logos are irrelevant to architecture decisions.
3. **Missing firewall / security controls**: Drawing direct connections across zone boundaries without firewall/WAF elements — security controls must be explicit.
4. **IP addresses in diagrams**: Including static IP ranges in architecture diagrams — IPs change; use logical component names.
5. **Missing SPOF identification**: Presenting a non-redundant architecture without labeling SPOFs — every critical path needs SPOF flags.

---

## 9. Industry Reference Patterns

**Gartner Infrastructure Reference Architecture**:
Gartner's tiered infrastructure model: Edge (CDN, DNS, DDoS protection) → DMZ (WAF, Load Balancer, API Gateway) → Application Tier (Application Servers, Container Clusters) → Data Tier (Databases, Cache, Search). Each tier is separately secured with firewall rules and network policies. This four-tier model maps directly to Variant A.

**TOGAF Technology Architecture Artifacts (Phase D)**:
TOGAF Phase D produces: Technology Portfolio Catalog, Technology Standards Catalog, and the Technology Architecture Diagram. The Technology Architecture Diagram should show: physical and virtual nodes, system software on each node, and communications paths with protocols. TOGAF recommends a two-level view: Platform Decomposition View (technology domains) and Network Computing Infrastructure View (detailed topology).

**NIST Cybersecurity Framework — Infrastructure Segmentation**:
NIST SP 800-125 recommends infrastructure segmentation via security zones: external, DMZ, internal, and management zones. Each zone has explicit trust levels and allowed traffic flows. The topology diagram is the evidence artifact showing logical segmentation compliance. NIST also requires identification of "security perimeter" — the boundary between external and internal trust zones.

---

## 10. Production QA Checklist

- [ ] Network zones are clearly labeled and visually separated
- [ ] All zone-crossing connections pass through a firewall or security control
- [ ] Single points of failure (non-redundant critical components) are labeled `⚠ SPOF`
- [ ] Component labels use logical/functional names, not IP addresses
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Redundant components are shown as pairs with Active/Standby labels
- [ ] Network link bandwidth annotated on primary connections
- [ ] Cloud boundary (if hybrid) is shown as a dashed container
- [ ] External internet connection uses wavy line or distinctive notation
- [ ] Presenter can identify the highest-risk SPOF in 15 seconds
