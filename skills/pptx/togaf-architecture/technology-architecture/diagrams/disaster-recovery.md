# TA-08: Disaster Recovery Architecture — Technology Architecture Diagram Spec

_Ref: NIST SP 800-34 Rev.1 (BCP/DR) | AWS Disaster Recovery Whitepaper | Google SRE — Reliability Principles_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing the topology of primary and recovery sites, data replication mechanisms, failover sequences, and RTO/RPO characteristics — illustrating how systems recover from a disaster scenario.

**Use When**:
- Designing business continuity and disaster recovery (BC/DR) architecture
- Documenting recovery strategy for compliance (ISO 22301, SOC 2, HIPAA)
- Presenting recovery posture to board, audit committee, or risk owners
- Planning multi-region cloud DR design (active-active, active-passive, pilot-light)
- Performing RTO/RPO gap analysis against business requirements

**Questions Answered**:
- What are the RTO and RPO targets per system tier?
- How does data replicate from primary to recovery site?
- What is the failover activation sequence?
- Which workloads are in which recovery tier?

**Primary Audience**: IT Risk Officers, CTO, Infrastructure Architects, Compliance Teams

---

## 2. Visual Layout Specification

**Structure**: Geographic dual-region layout with primary site (left) and DR site (right) connected by replication links.

### Variant A: Active-Passive DR (Warm/Cold Standby)
- Primary region: Full production stack (all colored, active)
- DR region: Mirrored but partially provisioned (grayed out = cold; partially colored = warm)
- Replication arrows: Continuous from primary to DR
- Failover sequence numbered on arrows: ①②③...
- Best for: SME enterprise DR, cost-constrained architectures

### Variant B: Active-Active Multi-Region
- Both regions fully operational
- Global Traffic Manager / GeoDNS at top routing to both
- Bi-directional data synchronization arrows
- Health check indicators on each region edge
- Best for: Zero-downtime high-availability, mission-critical SaaS

### Variant C: Tiered Recovery Classification
- Recovery tiers arranged in rows (Tier 0 = Mission Critical, Tier 1, Tier 2, Tier 3)
- Each tier row shows: RTO target, RPO target, Recovery strategy, systems in tier
- No geographic layout — this is a tabular + classification view
- Best for: Initial DR strategy documentation, business impact analysis

**Grid Proportions**:
- Primary site container: left 44% of content area
- Replication channel: center 12%
- DR site container: right 44%
- Failover timing band at bottom: 80px height

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Primary site | Active production workloads | `#00CCD7` |
| DR site (hot standby) | Fully active mirror | `#00CCD7` at lower opacity |
| DR site (warm standby) | Partially provisioned | `#53E3EB` |
| DR site (cold standby) | Not running, infrastructure-only | `#A5A7AA` |
| Replication link | Data synchronization | `#44546A` double-arrow |
| Health check | Monitoring probe | `#00CCD7` small diamond |
| Failover path | Activation sequence | `#2F2F2F` bold arrow |
| Mission-critical workload | Tier 0 — RPO minutes | `#44546A` border |
| Deferred workload | Tier 3 — RPO days | `#A5A7AA` fill |
| Global Traffic Manager | Traffic routing layer | White + `#00CCD7` border |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Site Label | "Primary — ap-east-1" | 12pt | Bold, `#44546A` |
| Tier Label | "Tier 0: Mission Critical" | 11pt | SemiBold |
| Component Name | Application/DB name | 9–10pt | Regular |
| RTO/RPO Tag | "RTO: 1h / RPO: 15min" | 8pt | SemiBold, `#00CCD7` |
| Sequence Number | ① ② ③ failover steps | 10pt | Bold, White on `#44546A` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large container | Site / region boundary |
| Rounded rect | Application workload |
| Cylinder | Database (primary or replica) |
| Cloud shape with region label | Cloud region (AWS AZ, Azure region) |
| Circle with flag | Failover activation trigger point |
| Double-headed arrow | Bidirectional replication |
| Single-headed arrow | Unidirectional replication (primary → DR) |
| Numbered circle badge | Failover sequence step order |
| Dashed container | Standby infrastructure (not provisioned by default) |
| Diamond | Health check / probe |

---

## 6. Annotation Rules

- **RTO/RPO badge**: Every workload tier or system labeled: `"RTO: 4h / RPO: 1h"`
- **Replication type**: Replication arrows labeled: `Sync`, `Async 5min lag`, `Daily backup`
- **RPO indicator**: Arrow labeled with recovery point: `Last backup: T-24h`
- **Failover steps**: Numbered sequence on activation arrows: `① DNS Failover → ② DB Promote → ③ App Scale-up`
- **Compliance callout**: Tier box annotated with applicable standards: `[ISO 22301 BIA]`

---

## 7. Content Density Rules

| Mode | Sites | Tiers | Workloads | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 1 | 3 | — |
| Optimal | 2 | 3–4 | 8–15 | single slide |
| Maximum | 3 | 5+ | 25 | → split: (1) Topology, (2) Tiering Table |

**Overflow Strategy**: Slide 1 = Geographic topology (sites + replication). Slide 2 = Recovery tiering table (workload → tier → RTO/RPO → strategy). The tiering table can handle unlimited workloads as a tabular appendix.

---

## 8. Anti-Patterns

1. **RTO/RPO missing**: A DR diagram without RTO/RPO targets is just a topology diagram — recovery objectives must be shown for every tier or system group.
2. **Manual failover assumed**: Showing a failover path with no indication of how it is triggered (automated health check vs. manual activation) — unspecified means assumed-manual, which dramatically increases actual RTO.
3. **Single replication method**: All data shown with the same replication arrow — databases, file systems, and object storage have fundamentally different replication mechanisms and must be distinguished.
4. **"DR" without specifying what fails**: "DR" can mean zone failure, region failure, or data center failure — the scope of disaster must be described in the diagram header.
5. **All workloads Tier 0**: Classifying everything as mission-critical negates the purpose of tiered recovery and inflates DR costs 3–5×. Business Impact Analysis must drive tiered classification.

---

## 9. Industry Reference Patterns

**NIST SP 800-34 Rev.1 — Contingency Planning Guide**:
NIST defines Information System Contingency Plan (ISCP) with four recovery strategies: Cold Site, Warm Site, Hot Site, and Mobile Recovery. Each strategy maps to specific RTO windows: Cold = days (>24h), Warm = hours (4–24h), Hot = minutes (<4h), Active-Active = seconds. The DR architecture diagram should clearly state which NIST strategy is implemented per tier and visually distinguish active vs. standby components as in this spec.

**AWS Disaster Recovery Whitepaper — Four Strategies**:
AWS defines four DR strategies on a cost/RTO matrix: Backup & Restore (hours RTO), Pilot Light (minutes RTO), Warm Standby (minutes RTO), Multi-Site Active-Active (real-time). Each strategy has a visual pattern: Backup & Restore = S3 snapshot arrows; Pilot Light = minimal core services running in DR region; Warm Standby = scaled-down mirror; Multi-Site = full duplicate with traffic balancer. Map each system tier to an AWS DR strategy as the annotation.

**Google SRE — Resilience and Recovery Principles**:
Google SRE's approach to data integrity and recovery focuses on: (1) Canary testing on recovery procedures, (2) Regular failover fire drills (GameDays), (3) Error budget as the driver for DR investment level. SRE recommends annotating DR diagrams with the "blast radius" of each failure domain — how many users or transactions are affected if that component fails. Include blast radius annotation as an optional overlay in Variant B (active-active).

---

## 10. Production QA Checklist

- [ ] RTO and RPO targets annotated for each tier or system group
- [ ] Primary and DR sites clearly geographically labeled (region / AZ / data center)
- [ ] Replication mechanism annotated on every data replication link
- [ ] Failover activation sequence numbered (manual vs. automated indicated)
- [ ] Recovery tiering table present (Tier 0–3) or linked to appendix
- [ ] Title uses slide placeholder (idx=0)
- [ ] Color used to distinguish active (full color) from standby (grayed) components
- [ ] Global traffic routing or DNS failover shown at the entry layer
- [ ] Data retention / backup frequency annotated for key stores
- [ ] Presenter can walk through complete failover sequence in 2 minutes
