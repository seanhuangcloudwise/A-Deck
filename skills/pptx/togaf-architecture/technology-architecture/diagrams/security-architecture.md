# TA-06: Security Architecture Diagram — Technology Architecture Diagram Spec

_Ref: NIST SP 800-207 (Zero Trust Architecture) | ISO/IEC 27001:2022 | SABSA Security Framework_

---

## 1. Purpose & When to Use

**Definition**: A diagram illustrating the security domain boundaries, control placement, identity zones, trust relationships, and defense-in-depth layers across the technology stack. Shows "where security is enforced" across the architecture.

**Use When**:
- Designing security architecture for a new system or platform
- Presenting security posture to CISO or compliance team
- Preparing for ISO 27001, SOC 2, or PCI-DSS audit documentation
- Designing Zero Trust migration from a perimeter-based model
- Architectural threat modeling using STRIDE or PASTA methodology

**Questions Answered**:
- Where are security control enforcement points?
- Which zones require explicit authentication/authorization?
- What is the trust model between system components?
- What are the network boundaries and blast radius of a breach?

**Primary Audience**: CISO, Security Engineers, IT Risk & Compliance, Enterprise Architects

---

## 2. Visual Layout Specification

**Structure**: Concentric security zone model (outer = public, inner = protected assets) with control annotations.

### Variant A: Defense-in-Depth Zones
- Outermost ring: Internet / Untrusted Zone
- Edge zone: WAF, DDoS protection, CDN
- DMZ: Load balancers, API Gateways
- Application zone: Services and APIs (mTLS)
- Data zone: Databases, secrets, vaults
- Innermost: Admin / privileged access
- Best for: Classic layered security architecture

### Variant B: Zero Trust Architecture
- No perimeter rings — instead: Identity Provider at center
- Component clusters connected via policy enforcement points (PEP)
- Policy Decision Point (PDP) shown as central authority
- All service-to-service calls pass through PEP arrows
- Best for: Zero Trust, cloud-native, micro-segmentation

### Variant C: Threat Surface Map
- System components mapped across exposure tiers
- Threat vectors shown as red arrows attacking surfaces
- Controls shown as shields blocking specific vectors
- STRIDE categories annotated on vectors
- Best for: Threat model presentations, security review boards

**Grid Proportions**:
- Zone rings: 15% band width each
- Control icons: 24px × 24px, labeled with control type
- Trust arrows: 2pt line weight, color = trust level

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Untrusted / Internet zone | External, unverified source | Light gray `#F5F5F5` with gray border |
| DMZ / Perimeter | Edge security controls | `#A5A7AA` |
| Application zone | Controlled internal services | `#53E3EB` |
| Data zone | Highest sensitivity tier | `#44546A` |
| Admin zone | Privileged access only | `#2F2F2F` |
| Security control (shield icon) | Enforced control point | `#00CCD7` |
| Trust boundary (solid line) | Enforced segmentation | `#2F2F2F` 2pt solid |
| Trust boundary (dashed) | Soft boundary / monitored | `#A5A7AA` dashed |
| Threat vector | Attack path | Red `#D32F2F` arrow |
| Verified/authenticated flow | Trusted mTLS, OIDC | `#00CCD7` arrow |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Zone Label | "Application Zone", "DMZ" | 12pt | Bold, `#44546A` |
| Control Label | "WAF", "RBAC", "mTLS" | 9pt | SemiBold |
| Component Name | Application/service name | 9–10pt | Regular |
| Risk Level | "(HIGH)", "(MEDIUM)" | 8pt | Regular, Red/Orange |
| Reference Label | CVE/control ID footnote | 7pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Concentric container | Security zone (defense-in-depth) |
| Shield icon | Security control enforcement point |
| Lock icon | Encrypted channel |
| Key icon | Authentication boundary |
| Cloud shape | External/SaaS service (untrusted) |
| Cylinder | Database (protected asset) |
| Solid arrow | Authenticated, authorized flow |
| Dashed arrow | Monitored, partially trusted flow |
| Red arrow | Threat vector (attack path) |
| Blocked arrow (X) | Denied/filtered flow |

---

## 6. Annotation Rules

- **Control label**: Every shield labeled with control type: `WAF`, `IDS/IPS`, `RBAC`, `MFA`, `TLS 1.3`
- **Protocol annotation**: All connection arrows labeled: `HTTPS/443`, `gRPC/TLS`, `mTLS mutual`
- **RBAC note**: Privileged access paths labeled: `Role: Admin`, `Break-glass: Audited`
- **Encryption marker**: Lock icon on every data-at-rest store
- **Compliance callout**: Control boxes with compliance reference note: `[PCI-DSS 6.6]` `[ISO A.9.4]`

---

## 7. Content Density Rules

| Mode | Zones | Controls | Components | Per Slide |
|---|---|---|---|---|
| Minimum | 2 | 3 | 4 | — |
| Optimal | 4–5 | 8–12 | 8–15 | single slide |
| Maximum | 6 | 16 | 25 | → split by zone pair |

**Overflow Strategy**: Split into: (1) Perimeter + Edge Controls slide, (2) Internal Services + Data Zone slide. Both slides reference the full zone color legend.

---

## 8. Anti-Patterns

1. **Flat network diagram**: Showing only network components without security controls — a network diagram is not a security architecture diagram.
2. **Perimeter-only model**: A single firewall at the edge with no internal segmentation — this is a 1990s model; every modern design needs internal zero-trust or micro-segmentation.
3. **Missing identity authority**: No identity provider (IdP/IAM) shown — identity is the new perimeter; it must be the central element or explicitly anchored.
4. **All arrows green/approved**: Showing only happy-path traffic without showing the controls that enforce it — security diagrams must show the enforcement points, not just flows.
5. **Controls without owners**: Security controls floating in the diagram without indicating who operates them (Cloud provider/ Platform team/ App team) — leads to governance gaps.

---

## 9. Industry Reference Patterns

**NIST SP 800-207 Zero Trust Architecture**:
NIST's ZTA model: "Never trust, always verify." Core components: Policy Decision Point (PDP), Policy Enforcement Point (PEP), Trust Algorithm, CDM system, SIEM. The enterprise resource (subject) connects to PEP, which queries PDP, which uses identity, device posture, and context. All lateral movement is explicitly evaluated. Map this to Variant B of this spec.

**SABSA Security Framework**:
SABSA (Sherwood Applied Business Security Architecture) maps security attributes from Business context down to Technology. The six-layer model: Contextual → Conceptual → Logical → Physical → Component → Operational. The security architecture diagram at the Technology layer must trace back to business risk attributes — annotating each control with its business risk mitigation rationale. Show traceability with footnote references.

**ISO/IEC 27001:2022 Annex A Controls**:
27001:2022 restructures controls into 4 categories: Organizational (37), People (8), Physical (14), Technological (34). A technology security architecture diagram should map the 34 technological controls to diagram zones: A.8 (Access Control) → Identity zone; A.8.21 (Network Security) → DMZ/Perimeter; A.8.24 (Use of Cryptography) → Data zone. Show compliance coverage as a coverage table in an appendix slide.

---

## 10. Production QA Checklist

- [ ] Security zones are drawn as explicit, labeled containers (not implied)
- [ ] Every data flow has an associated security control annotation
- [ ] Identity provider / IAM system is the first element placed in the diagram
- [ ] Encryption indicated for all data at rest and in transit
- [ ] No connection crosses a security boundary without a control intercepting it
- [ ] Privileged access paths are explicitly labeled and distinct from normal flows
- [ ] Title uses slide placeholder (idx=0)
- [ ] Color used to encode trust level, not arbitrary decoration
- [ ] At least one compliance or standards reference visible in the diagram
- [ ] Presenter can identify the "blast radius" of a single-component breach in 30 seconds
