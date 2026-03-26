# TA-05: Container Orchestration Architecture — Technology Architecture Diagram Spec

_Ref: CNCF Kubernetes Architecture | Cloud Native Trail Map | Kubernetes Documentation_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing the Kubernetes (or equivalent) cluster design — nodes, namespaces, workloads, services, ingress, and control plane — illustrating how containerized applications are organized and orchestrated.

**Use When**:
- Designing a new Kubernetes cluster for a platform or product team
- Reviewing cluster architecture for reliability, security, or scaling capacity
- Communicating platform design to application teams
- Planning multi-cluster or multi-tenant Kubernetes strategy
- Preparing for platform security audit (RBAC, network policy, secrets management)

**Questions Answered**:
- How are workloads organized within the cluster (namespaces, nodes)?
- How is traffic ingressed into the cluster?
- What platform services (monitoring, logging, service mesh) are deployed?
- How are secrets, configs, and RBAC managed?

**Primary Audience**: Platform Engineers, DevOps, SRE, Cloud Architects

---

## 2. Visual Layout Specification

**Structure**: Cluster boundary container with control plane, worker nodes, and namespace layers.

### Variant A: Single Cluster Architecture
- Control Plane at top (API Server, etcd, Controller Manager, Scheduler)
- Worker nodes below, each showing deployable pods
- Ingress / Service Mesh at cluster entry edge
- Best for: Single cluster design, platform overview

### Variant B: Multi-Cluster / Tenant Architecture
- Multiple cluster columns (Prod Cluster / Dev Cluster / Platform Cluster)
- Cross-cluster service connections
- Global traffic management at top
- Best for: Multi-cluster strategy, environment separation

### Variant C: Namespace View (Zoom-in)
- Single namespace detail
- All workloads, services, ConfigMaps, Secrets in namespace
- Network policy boundaries shown
- Best for: Application team onboarding, security review

**Grid Proportions**:
- Cluster container: 80% content area
- Control plane band: top 20% of cluster
- Worker node: 110pt × 80pt
- Namespace: dashed container within worker nodes, 20pt padding

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Kubernetes cluster boundary | Platform scope | `#00CCD7` dashed outer border |
| Control plane | Orchestration components | `#44546A` |
| Worker node | Compute unit | `#2F2F2F` |
| Namespace | Tenant isolation | `#53E3EB` dashed container |
| Pod / workload | Running container instance | White + `#00CCD7` border |
| Service (ClusterIP) | Internal service | `#53E3EB` |
| Ingress / LoadBalancer | External entry | `#44546A` |
| PersistentVolume | Storage | Gray cylinder |
| Monitoring stack | Platform service | `#A5A7AA` |
| Service Mesh sidecar | Envoy / Istio proxy | Small `#00CCD7` badge on pod |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Cluster Label | Cluster name header | 12pt | Bold, `#44546A` |
| Namespace Label | `ns: production` | 10pt | SemiBold, `#44546A` |
| Workload Name | Pod/Deployment name | 9pt | Regular |
| Control Plane Component | API Server, etcd, etc. | 9pt | Regular, White |
| Resource Count | "3 replicas", "2 nodes" | 8pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Large dashed container | Kubernetes cluster |
| Horizontal band (top) | Control plane |
| Rounded rect | Worker node |
| Inner dashed container | Namespace |
| Small rounded rect | Pod or container |
| Shield | RBAC / security policy |
| Arrow (ingress) | External traffic entering cluster |
| Dashed arrows between pods | Service mesh / internal traffic |
| Cylinder | PersistentVolume / storage |
| Small badge on pod edge | Sidecar proxy (service mesh) |

---

## 6. Annotation Rules

- **Replica count**: Deployment blocks labeled: `×3 pods` or `HPA: 3–10`
- **Resource limits**: Optional: `CPU: 0.5 / Mem: 512MB` per pod
- **RBAC badge**: Namespace or workload with restricted RBAC: `RBAC: Read-only`
- **Network policy**: Namespace labeled: "NetworkPolicy: Deny-all default"
- **Helm chart**: Workload annotation: "Chart: nginx-ingress v4.2"

---

## 7. Content Density Rules

| Mode | Nodes | Namespaces | Workloads | Per Slide |
|---|---|---|---|---|
| Minimum | 1 | 1 | 3 | — |
| Optimal | 3–5 | 3–6 | 10–20 | single slide |
| Maximum | 10 | 10 | 40 | → split by namespace group |

**Overflow Strategy**: Split by namespace grouping (Platform namespaces / Application namespaces / Monitoring namespaces). Each group on a dedicated slide.

---

## 8. Anti-Patterns

1. **No namespace isolation**: All workloads in the "default" namespace — production Kubernetes requires namespace isolation for security and multi-tenancy.
2. **No ingress shown**: Internal cluster diagram without showing how traffic enters — the ingress design is the most visible operational concern.
3. **Control plane as a black box**: Showing only worker nodes without the control plane — at minimum, label that the control plane exists (managed or self-hosted).
4. **Pod-to-pod direct coupling**: Showing pods calling pods directly without a Kubernetes Service abstraction — services are mandatory for stable communication.
5. **Missing persistent volume**: Stateful workloads (databases, message queues) shown without their storage component — storage is a critical platform decision.

---

## 9. Industry Reference Patterns

**CNCF Kubernetes Cluster Architecture**:
Standard Kubernetes architecture: Control Plane (API Server, Scheduler, Controller Manager, etcd) + Worker Nodes (kubelet, kube-proxy, container runtime) + Networking (CNI plugin) + Storage (CSI driver). Each diagram must show the control plane-dataplane separation. For managed Kubernetes (EKS, AKS, GKE), control plane is labeled as "Managed" and simplified.

**CNCF Cloud Native Trail Map**:
CNCF's recommended adoption sequence: Containerize → CI/CD → Orchestration (Kubernetes) → Observability → Service Mesh → Networking Policies → Distributed Tracing → Secrets Management. At each stage, new components are added to the cluster diagram — making this spec the visualization tool for trail map progression documentation.

**Istio Service Mesh Architecture**:
Istio extends the cluster diagram with a control plane (Istiod) and data plane (Envoy sidecars injected into each pod). The diagram shows: sidecar proxies `[E]` badge on every pod, mTLS connections between pods, and Istiod policy management. Network policies are replaced by Istio authorization policies. This maps to the service mesh sidecar annotations in this spec.

---

## 10. Production QA Checklist

- [ ] Kubernetes cluster boundary is clearly drawn
- [ ] Control plane is shown (labeled as managed or self-hosted)
- [ ] Namespaces are used to organize workloads with isolation boundaries
- [ ] Ingress controller or load balancer shown at cluster entry
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Replica counts shown for critical workloads
- [ ] PersistentVolumes shown for stateful workloads
- [ ] RBAC and network policies indicated for sensitive namespaces
- [ ] Platform services (monitoring, logging, mesh) are distinguished from application workloads
- [ ] Presenter can explain how external traffic reaches a specific pod in 45 seconds
