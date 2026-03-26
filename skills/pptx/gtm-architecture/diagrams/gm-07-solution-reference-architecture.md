# GM-07: Solution Reference Architecture Diagram — GTM Diagram Spec

_Ref: IBM Reference Architecture | AWS Well-Architected Framework Workload Diagrams | TOGAF Phase C Solution Architecture | Gartner Solution Brief Standards_

---

## 1. Purpose & When to Use

**Definition**: A simplified architecture diagram showing how the product integrates into a customer's existing IT environment — illustrating data flows, integration points, adjacent systems, and the product's functional boundary within the buyer's architecture.

**Use When**:
- Writing a technical white paper that architects and IT buyers will evaluate
- Building the "How It Works" or "Architecture" section of a solution brief
- Enabling pre-sales SEs to explain integration complexity to technical evaluators
- Responding to RFP questions about system compatibility and integration approach

**Questions Answered**:
- Where does this product sit in our IT landscape?
- What does it integrate with (upstream/downstream)?
- What data flows in/out and at what layer?
- What replaces vs. complements existing systems?

**Primary Audience**: Solution Architects, Enterprise Architects, IT Decision Makers, Technical Pre-Sales

---

## 2. Visual Layout Specification

**Structure**: Layered system diagram showing product positioned within a reference customer IT stack.

### Variant A: Horizontal Integration View (Recommended)
- Left zone: Data sources / upstream systems
- Center zone: Product / solution (highlighted)
- Right zone: Downstream consumers / output systems
- Data flow arrows indicate direction and type
- Best for: integration-focused products (middleware, data platforms, observability tools)

### Variant B: Vertical Layer Architecture
- Top: User-facing layer (UI/API consumers)
- Middle: Product layer (own platform, highlighted)
- Bottom: Data/infrastructure layer (databases, cloud, on-prem)
- Best for: platform products, SaaS layers, infrastructure tools

### Variant C: Multi-Tenant Deployment View
- Shows multiple deployment patterns (cloud / on-prem / hybrid) as separate columns
- Product block present in all columns, with connectivity differences noted
- Best for: enterprise software with flexible deployment options

**Grid Proportions**:
- Product block (own): 180pt × 80pt minimum — must be visually dominant
- Adjacent system blocks: 100pt × 44pt
- Data flow arrows: 1.5pt width
- Zone boundary labels: 9pt, `#44546A`

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Own product block | Solution boundary | `#00CCD7` with bold border |
| Integration partner block | Certified integration | `#53E3EB` |
| Customer/3rd-party system | External system | White, `#A5A7AA` border |
| Data source | Upstream input | `#D9EEF2` |
| Data consumer | Downstream output | `#E6FAFB` |
| Security boundary | Trust zone perimeter | Dashed `#44546A` |
| Data flow arrow | API / event / batch | `#2F2F2F` directional |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | e.g., "Reference Architecture: [Industry]" | 14pt | Regular |
| Zone Header | Layer/zone label | 10pt | Bold, `#44546A` |
| System Name | Block label | 9pt | SemiBold |
| Data Flow Label | Arrow annotation | 8pt | Regular, `#2F2F2F` |
| Integration Type | Protocol tag (REST/Kafka/etc.) | 7pt | Regular, gray |
| Footnote | Version, topology notes | 7pt | Italic, gray |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Bold-border rect | Own product (focal point) |
| Standard rect | System / component block |
| Dashed rect container | System boundary / trust zone |
| Solid arrow | Primary data / API flow |
| Dashed arrow | Optional / asynchronous flow |
| Database cylinder | Data store |
| Cloud shape (simple) | Cloud service integration |

**Connector Rule**: All arrows must be labeled with: data type or protocol (REST, Kafka, S3, gRPC). Unlabeled arrows are not permitted.

---

## 6. Annotation Rules

- **Integration protocol labels**: Every flow arrow must annotate the integration mechanism (REST API, Kafka topic, webhook, batch ETL, SDK, etc.)
- **Deployment scope note**: Add a topology badge showing which components are cloud-hosted vs customer-hosted vs shared
- **Security perimeter**: Draw a dashed boundary around trust zones (what is inside the customer's network perimeter)
- **"Not in scope" zone**: Grey out systems that are NOT part of this solution (avoids scope confusion in technical evaluation)
- **Version note**: "Supported integrations as of [version/date]" in footnote

---

## 7. Content Density Rules

| Mode | System Blocks | Flows | Per Slide |
|---|---|---|---|
| Minimum | 4 | 3 | — |
| Optimal | 8–12 | 6–10 | 1 slide |
| Maximum | 18 | 15 | → split by integrate domain |

---

## 8. Anti-Patterns

1. **Marketing diagram posing as architecture**: Vague "connects to everything" diagram with generic cloud/database icons and no labels — fails technical evaluator scrutiny immediately.
2. **Missing integration types**: Flow arrows with no protocol labels force engineers to ask basic questions that should have been pre-answered.
3. **Own product too small**: Solutions where the product block is the same size as a third-party system — the own product must be visually dominant.
4. **No trust zone boundary**: For enterprise software, omitting the security perimeter leaves architects unable to assess data residency and compliance risk.
5. **Technology jargon overload**: Block labels using internal codenames ("Nexus-Core-v2") rather than functional descriptions ("AI Anomaly Detection Engine").

---

## 9. Industry Reference Patterns

**AWS Well-Architected Framework**:
AWS prescribes reference architecture diagrams for every service workload — showing VPCs, subnets, IAM roles, and service boundaries. The discipline of explicit boundary labeling, protocol annotation, and separation of control plane vs data plane has become the de-facto standard for enterprise software reference architectures. The "AWS Architecture Icons" icon library provides standardized shapes.

**IBM Reference Architecture Pattern**:
IBM's middleware and cloud architecture follows a "reference architecture" model with: functional zones (channels, services, data), integration patterns (API gateway, event bus, ESB), and deployment tiers. The IBM approach explicitly identifies "shared services" vs "domain-specific" services — mapping well to enterprise buyers who think in domain boundaries.

**TOGAF Phase C Solution Architecture**:
TOGAF Phase C mandates a Solution Architecture that shows how applications realize business capabilities (from Phase B). The solution reference architecture diagram is the "Bridge Document" between the business architecture (what we need) and the technology architecture (what we build). GTM-facing version of this removes TOGAF-specific notation but preserves the boundary/zone/flow structure.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Own product block is visually dominant (larger, branded)
- [ ] All integration flows are labeled with protocol/type
- [ ] Trust/security boundary is marked explicitly
- [ ] Customer-hosted vs cloud-hosted zones are differentiated
- [ ] Upstream and downstream systems are present
- [ ] No internal codenames — all blocks use functional descriptions
- [ ] "Not in scope" systems are visually distinguished (greyed out)
- [ ] Integration version/date in footnote
- [ ] Solution architect can explain all labeled integration points in 2 minutes
