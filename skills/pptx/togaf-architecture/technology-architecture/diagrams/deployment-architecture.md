# TA-02: Deployment Architecture — Technology Architecture Diagram Spec

_Ref: TOGAF Phase D Deployment View | C4 Deployment Diagram | 12-Factor App | GitOps Principles_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing where applications and services are deployed — across environments, compute nodes, containers, and cloud regions — and how configuration and code flow through the deployment pipeline.

**Use When**:
- Designing or reviewing deployment topology for a new application or system
- Planning environment promotion flow (Dev → Test → Staging → Production)
- Communicating deployment architecture to DevOps teams or operations
- Identifying environment configuration drift or consistency issues
- Designing multi-region or multi-cloud deployment for resilience

**Questions Answered**:
- Which applications are deployed to which environments and compute nodes?
- How does code flow from development to production?
- Are environments consistent in their configuration?
- Where is geographic distribution and failover deployed?

**Primary Audience**: DevOps Engineers, Platform Engineers, Solution Architects, SRE

---

## 2. Visual Layout Specification

**Structure**: Environment columns or pipeline flow showing deployment targets.

### Variant A: Environment Columns (Dev→Test→Prod)
- Columns = environments (Development, Testing, Staging, Production)
- Rows = application components/services deployed
- Arrow between columns shows promotion flow
- Best for: Environment planning, release management

### Variant B: Deployment Target View
- Compute targets at top: Kubernetes Cluster / VM / Serverless / Edge
- Applications shown as blocks within compute targets
- Best for: Infrastructure-to-application mapping

### Variant C: Multi-Region Deployment
- Regions as side-by-side columns or geographic layout
- Primary and secondary regions shown
- Global load balancer / CDN at top
- Best for: High availability, disaster recovery planning

**Grid Proportions**:
- Environment column width: equal-width partitions
- Application block: 90pt × 40pt
- Promotion arrow: 30pt gap between columns
- Region container padding: 20pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Production environment | Live traffic | `#44546A` column header |
| Staging environment | Pre-prod validation | `#00CCD7` column header |
| Test environment | QA testing | `#53E3EB` column header |
| Development environment | Active development | `#A5A7AA` column header |
| Application service | Deployable unit | White + `#2F2F2F` border |
| Database / data store | Persistent store | `#2F2F2F` cylinder |
| Kubernetes cluster | Container orchestration | `#00CCD7` dashed container |
| Serverless function | Event-triggered compute | `#53E3EB` rounded |
| Promotion arrow | Code/config promotion | `#00CCD7` solid arrow |
| Configuration drift flag | Inconsistent environment | `⚠` annotation |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Environment Header | Column/zone name | 12pt | Bold, White |
| Service Name | Application block label | 9–10pt | SemiBold |
| Version Tag | Deployed version | 8pt | Monospace, `#44546A` |
| Region Label | Geographic location | 10pt | Bold, `#44546A` |
| CI/CD Pipeline Label | Promotion path | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect | Deployed application service |
| Dashed container | Environment or cluster boundary |
| Cylinder | Database deployment |
| Small lambda λ | Serverless function |
| Horizontal arrow | Code/config promotion direction |
| Gear icon annotation | Configuration-managed component |
| Solid container | Physical or dedicated compute |
| `[v2.1.3]` tag badge | Deployed version annotation |

---

## 6. Annotation Rules

- **Version tags**: Every deployed service shows version: `v3.2.1` in top-right corner
- **Replica count**: In production: `×3 replicas` annotation on services with horizontal scaling
- **Config source**: Annotate: "Config from: Vault / ConfigMap / Environment Variables"
- **Pipeline reference**: Promotion arrows labeled: "CI/CD: GitHub Actions"
- **Drift indicator**: `⚠ Config differs from Prod` on environment blocks with known configuration drift

---

## 7. Content Density Rules

| Mode | Services | Environments | Per Slide |
|---|---|---|---|
| Minimum | 2 | 2 | — |
| Optimal | 5–10 | 3–4 | single slide |
| Maximum | 20 | 5 | → split by application domain |

**Overflow Strategy**: Split by application domain. Each domain's deployment topology on a dedicated slide. A master slide shows all domains summarized per environment with service counts.

---

## 8. Anti-Patterns

1. **Production-only view**: Showing only the production environment — deployment architecture must show the full environment chain to communicate promotion and testing gates.
2. **No version annotations**: Services without version numbers provide no deployment state information.
3. **Missing database deployment**: Applications shown without their persistence components — every stateful service needs its database deployment shown.
4. **Flat feature-by-feature deployment**: Treating each feature as a separate deployment unit — deployment diagrams show services, not feature branches.
5. **No CI/CD pipeline reference**: Deployment architecture without promotion path — the diagram must show both the target state and the mechanism to reach it.

---

## 9. Industry Reference Patterns

**12-Factor App (Heroku)**:
The 12-Factor App defines environment parity: development, staging, and production should be as similar as possible. Deployment architecture diagrams must reflect this — showing environment inconsistencies (different configurations, missing components) as deployment risks. Factor 10 (Dev/Prod Parity) is directly visualized by comparing environment column contents.

**GitOps (Weaveworks / Argo CD)**:
GitOps defines the Git repository as the single source of truth for infrastructure configuration. Deployment diagrams in a GitOps model show: Git repo → CI pipeline → container registry → CD pipeline → Kubernetes cluster. Each stage is a deployable artifact transformation. The promotion arrows in Variant A represent the gitops promotion flow.

**C4 Model Deployment Diagram (Level 4)**:
Simon Brown's C4 Deployment Diagram is the deployment view at L4: showing where containers (L2) or components (L3) run in the infrastructure. The C4 nodes are: Deployment Node (environment, server, cluster), Container Instance (running software), and Infrastructure Node (external service, DNS, CDN). This spec's Variant B maps to the C4 Deployment Diagram structure.

---

## 10. Production QA Checklist

- [ ] All target environments (Dev/Test/Staging/Prod) are shown
- [ ] Every deployed service has a version tag
- [ ] Database/persistence deployments shown alongside application services
- [ ] Promotion flow arrow between environments present and labeled
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Kubernetes/container clusters shown as dashed containers
- [ ] Replica counts shown for production services
- [ ] Configuration source annotated for environment-configurable services
- [ ] Multi-region services show region labels and load balancer
- [ ] Presenter can explain the deployment promotion process in 45 seconds
