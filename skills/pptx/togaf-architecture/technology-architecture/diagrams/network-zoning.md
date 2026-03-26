# TA-03: Network Zoning Diagram — Technology Architecture Diagram Spec

_Ref: NIST SP 800-125 | CIS Controls v8 | Zero Trust Architecture (NIST SP 800-207) | TOGAF Security View_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing network segments, security zones, trust boundaries, and connectivity policies — defining where data and traffic are allowed to flow and what security controls exist at each boundary.

**Use When**:
- Designing network segmentation for a new application or system
- Security architecture review: validating zone isolation and control placement
- Regulatory compliance documentation (PCI DSS, HIPAA, ISO 27001)
- Zero Trust Architecture design: illustrating trust zone elimination
- Incident response planning: showing blast radius of a network-level breach

**Questions Answered**:
- What are the network security zones and their trust levels?
- What security controls exist at each zone boundary?
- Which traffic flows are allowed vs. blocked between zones?
- Does the design conform to zero-trust or perimeter-based security model?

**Primary Audience**: Network Engineers, Security Architects, Compliance teams, CISO

---

## 2. Visual Layout Specification

**Structure**: Concentric rings or horizontal bands from internet-exposed to internal secure.

### Variant A: Concentric Zone Model
- Outermost ring: Internet / Untrusted
- Second ring: DMZ / Semi-trusted
- Third ring: Application network
- Inner zone: Data / Highly sensitive
- Firewall/WAF at each ring boundary
- Best for: Traditional perimeter architecture

### Variant B: Horizontal Zone Tiers
- Horizontal bands from top (internet) to bottom (data)
- Security control elements between each tier
- Best for: Detailed security architecture documentation

### Variant C: Zero Trust Segmentation
- No perimeter — every resource is its own micro-segment
- Identity-aware proxy at center
- Policy engine connecting all zones
- Segments: User → Identity Provider → Policy Engine → Resource
- Best for: Zero Trust Architecture presentation

**Grid Proportions**:
- Zone band height: ~20% of content area
- Security control shape: 50pt × 30pt
- Left-side trust-level label: 80pt wide
- Right-side allowed-traffic annotation: 100pt wide

---

## 3. Color Semantics

| Zone | Trust Level | Fill Color |
|---|---|---|
| Internet / Untrusted | Zero trust | `#A5A7AA` dashed container |
| DMZ | Low trust | `#44546A` with light fill |
| Internal Application Zone | Medium trust | `#00CCD7` container |
| Internal Data Zone | High trust | `#2F2F2F` container |
| Admin / Management Zone | Restricted | `#44546A` dotted container |
| Firewall / WAF | Security control | Red/orange border element |
| Allowed traffic flow | Permitted connection | `#00CCD7` solid arrow |
| Blocked traffic | Denied connection | `#A5A7AA` dashed red-x |
| Zero Trust segment | Micro-perimeter | `#53E3EB` with identity badge |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Zone Name | Tier / zone label | 11pt | Bold, White |
| Trust Level | "Untrusted / Medium / High" | 9pt | Italic, colored |
| Security Control | FW, WAF, IDS label | 9pt | SemiBold |
| Traffic Rule | Allowed port/protocol | 8pt | Regular, `#00CCD7` |
| Block Rule | Denied traffic | 8pt | Regular, strikethrough |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Wide dashed container | Network zone |
| Shield / wedge shape | Firewall |
| `[WAF]` rectangle | Web Application Firewall |
| `[IDS/IPS]` rectangle | Intrusion detection/prevention |
| `[LB]` cylinder | Load balancer |
| `[NAT]` box | Network address translation |
| Solid arrow | Allowed traffic direction |
| Dashed red arrow with ✗ | Blocked traffic |
| Key icon | Authentication / encryption checkpoint |
| Identity badge | Identity-aware access control (ZTA) |

---

## 6. Annotation Rules

- **Port/protocol table**: Allowed flows annotated: "443/HTTPS" or "3306/MySQL (DB zone only)"
- **Firewall rule count**: Firewall shapes annotated: "FW-01 | 248 rules"
- **Compliance scope box**: Dashed boundary box labeled "PCI Scope", "HIPAA Scope" around regulated zones
- **Alert threshold**: IDS/IPS shapes: "Alert on: >100 failed auths/min"
- **Encryption indicator**: `🔒 TLS 1.3` annotations on connections requiring encryption in transit

---

## 7. Content Density Rules

| Mode | Zones | Security Controls | Connection Rules | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 1 | 2 | — |
| Optimal | 4–6 | 4–8 | 8–15 | single slide |
| Maximum | 8 | 12 | 25 | → split by trust domain |

**Overflow Strategy**: Split by security domain. Core ingress zone details on one slide; internal application-to-data zone rules on another. Add a summarizing legend slide.

---

## 8. Anti-Patterns

1. **Flat network**: All components in one zone with no boundary definitions — provides no security architecture information.
2. **Missing security controls at boundaries**: Zone transitions without explicit firewall or security control elements — implies zone crossing without inspection.
3. **Allowing all inbound**: DMZ to application zone shown with a generic "→ all traffic" arrow — every crossing must specify allowed ports and protocols.
4. **Bidirectional management connections**: Admin/management zone connections shown as bidirectional when they should be unidirectional — management flows only inward, never outward.
5. **Compliance scope invisible**: PCI or HIPAA-regulated systems not showing their compliance scope boundary — regulatory zones must be explicitly called out.

---

## 9. Industry Reference Patterns

**NIST SP 800-125 Network Segmentation Guidelines**:
NIST recommends that networks be segmented into security zones based on data sensitivity and trust level. Minimum required zones: external, DMZ, internal, and management. Communication between zones must be mediated by security controls (firewall, proxy, gateway). Each inter-zone connection must have a documented business justification.

**CIS Controls v8 — Control 12 (Network Infrastructure Management)**:
CIS Control 12 requires: network diagrams showing the current architecture with all trust boundaries; change-managed firewall rules aligned to business use cases; network monitoring at trust boundaries. The Network Zoning Diagram is the primary evidence artifact for CIS Control 12 compliance.

**NIST SP 800-207 Zero Trust Architecture**:
For Variant C, NIST's ZTA defines: Resource (what is being accessed), Policy Engine (what's permitted), Policy Administrator (decision enforcer), and Policy Enforcement Point (gateway). The ZTA model eliminates implicit network trust — every access request is evaluated by the policy engine regardless of source network. The diagram shows PEPs at each resource boundary connecting to the central Policy Engine.

---

## 10. Production QA Checklist

- [ ] All security zones are named and labeled with trust level
- [ ] Every zone boundary has an explicit security control element (firewall, WAF, IDS)
- [ ] Allowed traffic flows are annotated with port/protocol
- [ ] Blocked traffic flows are explicitly shown (not implied by absence)
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Compliance scope boundaries (PCI/HIPAA) are labeled if applicable
- [ ] Management/admin zone is isolated from other zones
- [ ] Encryption requirements shown on sensitive data flows
- [ ] Internet-facing entry points are minimized and explicitly identified
- [ ] Presenter can trace an inbound HTTP request from internet to application in 45 seconds
