# TA-09: Platform Capability Map — Technology Architecture Diagram Spec

_Ref: CNCF Cloud Native Trail Map | Gartner Platform Engineering Report 2024 | TOGAF ADM Phase D_

---

## 1. Purpose & When to Use

**Definition**: A capability-oriented view of the technology platform — showing the taxonomy of platform services (infrastructure, runtime, data, security, DevOps, observability) that underpin application development and operations, mapped against maturity and ownership.

**Use When**:
- Documenting the internal developer platform (IDP) capability set
- Presenting platform investment roadmap to CTO or Technology Board
- Assessing platform maturity against CNCF Cloud Native Trail Map
- Onboarding product teams to available platform capabilities
- Defining platform team responsibilities vs. application team responsibilities

**Questions Answered**:
- What platform capabilities exist and are available for application teams?
- What is the maturity and ownership status of each capability?
- What capabilities are missing, planned, or deprecated?
- How is the platform organized into domains?

**Primary Audience**: CTO, Platform Engineers, Developer Experience Teams, Application Architecture Teams

---

## 2. Visual Layout Specification

**Structure**: Two-axis grid with Platform Domains on the Y-axis and Maturity/Status on the X-axis (or a single layered block map).

### Variant A: Domain Block Map
- Rows = Platform Domains (Infrastructure, Runtime, Data, Security, DevOps, Observability, AI/ML)
- Each row contains capability tiles: service name + maturity status
- Color encoding: maturity tier (Planned / Alpha / Beta / GA / Deprecated)
- Best for: Executive overview, investor presentations

### Variant B: CNCF Trail Map Layered View
- Vertical layers matching CNCF Trail Map categories:
  1. Containerization
  2. CI/CD
  3. Orchestration & Application Definition
  4. Observability & Analysis
  5. Service Proxy, Discovery, Mesh
  6. Networking & Policy
  7. Distributed Database & Storage
  8. Streaming & Messaging
  9. Container Registry & Runtime Security
  10. Software Distribution
- Each layer shows installed tools with maturity badge
- Best for: Platform roadmap reviews, CNCF benchmark

### Variant C: Ownership Responsibility Map
- Platform capabilities in rows
- Columns: Platform Team / Application Team / Cloud Provider / Shared
- Matrix cells: Responsible (R) / Accountable (A) / Consulted (C) / Informed (I) (RACI)
- Best for: Operating model clarity, team boundary definition

**Grid Proportions**:
- Domain header column: 18% of width
- Capability tile: 80–100pt × 50pt
- Maturity badge: top-right corner of tile, 20px × 16px
- Ownership RACI matrix: full-width table format

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Infrastructure domain | Compute, network, storage | `#44546A` |
| Runtime domain | Containers, serverless, FaaS | `#2F2F2F` |
| Data domain | Databases, cache, streaming | `#44546A` |
| DevOps domain | CI/CD, GitOps, artifact management | `#00CCD7` |
| Security domain | IAM, secrets, policy enforcement | `#2F2F2F` |
| Observability domain | Metrics, logs, traces, alerting | `#53E3EB` |
| AI/ML platform domain | Feature store, training, serving | `#00CCD7` |
| GA (Generally Available) | Fully productionized | `#00CCD7` fill |
| Beta | Production but evolving | `#53E3EB` fill |
| Alpha | Early access / experimental | `#A5A7AA` fill |
| Planned | Not yet built | White + dashed border |
| Deprecated | Being decommissioned | `#A5A7AA` strikethrough |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Domain Label | "DevOps Domain", "Data Domain" | 12pt | Bold, White |
| Capability Name | Service or tool name | 9–10pt | SemiBold |
| Maturity Badge | "GA", "Beta", "Alpha" | 7pt | Bold, White |
| Ownership Label | "Plt Team", "App Team" | 8pt | Regular |
| Version Tag | "v2.4.1", "Helm chart" | 7pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Horizontal band / row | Platform domain |
| Tile (outlined rectangle) | Individual platform capability |
| Colored badge (top-right) | Maturity status indicator |
| Dotted tile outline | Planned capability (not yet available) |
| Strikethrough tile | Deprecated / sunset capability |
| Lock icon on tile | Security-gated / restricted capability |
| Arrow linking tiles | Capability dependency |
| Star icon | Recommended / default capability |

---

## 6. Annotation Rules

- **Maturity badge**: Every capability tile has a badge: `GA`, `Beta`, `Alpha`, `Planned`, or `Deprecated`
- **Team ownership**: Bottom edge of tile: `by: Platform SRE` or `by: Cloud Provider`
- **Version**: Small version label below capability name: `v2.4`, `Chart v5.1`
- **Deprecation**: Deprecated tiles use strikethrough name text + amber banner: `"Deprecated: Migrate by Q4"`
- **Dependency arrows**: Capability → Capability dashed arrow labeled: `"Requires"` or `"Replaces"`

---

## 7. Content Density Rules

| Mode | Domains | Capabilities | Per Slide |
|---|---|---|---|
| Minimum | 3 | 6 | — |
| Optimal | 5–7 | 20–40 | single slide |
| Maximum | 9 | 60 | → split by domain cluster |

**Overflow Strategy**: Split into General Platform (Infra + Runtime + DevOps) slide and Specialist Platform (Data + ML + Security + Observability) slide. Cross-slide reference table in appendix.

---

## 8. Anti-Patterns

1. **Tools as capabilities**: Listing specific tool names (Terraform, Jenkins) as the only content — capabilities are the function provided, tools are how it's delivered. Label the capability first, tool second.
2. **No maturity indication**: All capabilities show as equally complete — platform maturity is uneven; hiding this creates incorrect expectations for application teams.
3. **Missing ownership**: Capabilities without team ownership — creates "orphan" capabilities that lack SLAs and support paths.
4. **Completeness theater**: Showing 80+ capabilities in one diagram — above 40 capabilities the diagram becomes unreadable; split by domain or use a summary level.
5. **Static snapshot**: Platform capability maps with no roadmap indicators (what's GA vs. planned vs. deprecated) — a platform map without temporal context creates incorrect commitments to application teams.

---

## 9. Industry Reference Patterns

**CNCF Cloud Native Trail Map**:
CNCF's 10-step trail map defines the standardized path for cloud-native capability adoption. Each step represents a capability domain that must appear in the platform capability map. The CNCF Landscape catalog (1000+ projects) categorizes tools exactly into the domains used in this spec. Platform teams should explicitly label which CNCF-approved tools they've selected per domain, creating a "CNCF Compliance" overlay on Variant A.

**Gartner Platform Engineering Report 2024**:
Gartner recognizes platform engineering as a discipline where internal developer platforms (IDPs) reduce cognitive load on application teams. The Gartner IDP model defines a "golden path" — a set of stamped, opinionated, pre-approved platform capabilities that development teams use by default. The platform capability map should designate "golden path" capabilities with a star indicator, distinct from "available but not recommended" capabilities.

**TOGAF ADM Phase D — Technology Architecture**:
TOGAF Phase D produces technology architecture deliverables including the Technology Portfolio Catalog, which enumerates all technology components across the platform. The Platform Capability Map is the visual equivalent of the Technology Portfolio Catalog. TOGAF's recommended approach: categorize by Technology Domain → Technology Category → Technology Component, with lifecycle status (Active / Phasing In / Phasing Out / Retired) for each component. Map lifecycle status directly to the maturity badges in this spec.

---

## 10. Production QA Checklist

- [ ] All platform domains are represented (Infra, Runtime, DevOps, Data, Security, Observability)
- [ ] Every capability tile has a maturity/status badge
- [ ] Ownership is indicated per capability or per domain
- [ ] Golden path or recommended capabilities are visually distinguished
- [ ] Deprecated capabilities are clearly marked with migration deadline
- [ ] Title uses slide placeholder (idx=0)
- [ ] Domain headers use consistent font size and color
- [ ] Planned capabilities use dashed or grayed borders to clearly distinguish from available
- [ ] Dependency arrows shown only where platform capability A requires B to function
- [ ] Presenter can describe the platform's golden path in 90 seconds
