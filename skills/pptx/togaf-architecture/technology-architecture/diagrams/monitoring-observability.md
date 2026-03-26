# TA-07: Monitoring & Observability Architecture — Technology Architecture Diagram Spec

_Ref: Google SRE Book (Site Reliability Engineering) | CNCF Observability TAG | OpenTelemetry Specification_

---

## 1. Purpose & When to Use

**Definition**: A diagram showing the observability stack architecture — how metrics, logs, and distributed traces are collected, aggregated, stored, and visualized from application and infrastructure sources.

**Use When**:
- Designing the observability platform for a microservice or cloud-native system
- Presenting SRE monitoring strategy to engineering leadership
- Planning centralized logging infrastructure or telemetry pipeline
- Establishing SLO/SLA monitoring architecture
- Evaluating observability tool stack choices (Prometheus, Datadog, ELK, Jaeger, OpenTelemetry)

**Questions Answered**:
- How are metrics, logs, and traces collected from each service?
- Where are they stored and for how long?
- Who receives alerts and through which channels?
- How do SLO/SLI measurements flow from services to dashboards?

**Primary Audience**: SRE Teams, Platform Engineers, DevOps, Engineering Managers

---

## 2. Visual Layout Specification

**Structure**: Left-to-right pipeline flow — Sources → Collection → Storage → Analysis → Alerting.

### Variant A: Three Pillars Pipeline
- Row 1: Metrics pipeline (Prometheus / StatsD → Thanos → Grafana)
- Row 2: Logs pipeline (Fluentd / Filebeat → Elasticsearch → Kibana)
- Row 3: Traces pipeline (Jaeger / Zipkin / OTel → Tempo → Grafana)
- Shared alert management: Alertmanager at right edge
- Best for: Full observability stack design, tool selection

### Variant B: OpenTelemetry-Unified Model
- OTel Collector as central hub at diagram center
- Sources fan-in to OTel Collector (left side)
- Storage backends fan-out from OTel Collector (right side)
- Single pipeline with signal-type routing inside collector
- Best for: OTel-native architectures, vendor-agnostic design

### Variant C: SLO / SRE Monitoring Map
- Application SLIs at top (latency p99, error rate, availability)
- SLIs flow into Prometheus recording rules
- SLOs shown as horizontal target lines
- Error budget burn rate → Alertmanager → PagerDuty → On-call
- Best for: SLO/Error budget review, SRE practice documentation

**Grid Proportions**:
- Source column: leftmost 20% — component icons
- Collection layer: 20% — agent/collector
- Storage layer: 20% — time-series DB, log store
- Analysis/Viz layer: 20% — dashboards
- Alert layer: rightmost 20% — channels and policies

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Application / service source | Telemetry producer | `#44546A` |
| OTel Collector / agent | Collection layer | `#00CCD7` |
| Metrics pipeline | Numeric time-series | `#00CCD7` fill |
| Logs pipeline | Text event logs | `#53E3EB` fill |
| Traces pipeline | Distributed request traces | `#44546A` fill |
| Storage backend | Long-term storage | `#2F2F2F` |
| Dashboard / visualization | Consumer-facing UI | White + `#00CCD7` border |
| Alert | Triggered condition | Amber/orange accent |
| SLO indicator | Service level objective | `#00CCD7` dashed line |
| On-call notification | Human response | `#A5A7AA` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Layer Header | "Collection Layer", "Storage Layer" | 11pt | Bold, `#44546A` |
| Component Name | "Prometheus", "OTel Collector" | 9–10pt | SemiBold |
| Metric/Signal Label | "p99 latency", "error_rate" | 8pt | Regular |
| Retention Note | "30d retention", "1yr cold" | 8pt | Regular, `#A5A7AA` |
| Alert Condition | "Error rate > 1%" | 8pt | Italic |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Hexagon | OTel Collector (central hub) |
| Rounded rect | Application or service (source) |
| Cylinder | Time-series or log database |
| Monitor icon | Dashboard / visualization layer |
| Bell icon | Alertmanager / alert rule |
| Arrow (solid) | Real-time data flow |
| Arrow (dashed) | Queried / pull-based collection |
| Horizontal dashed line | SLO target threshold |
| Badge on source | Instrumentation method (SDK, agent, sidecar) |

---

## 6. Annotation Rules

- **Retention period**: Storage cylinders labeled: `"30d hot / 13mo cold"`
- **Sampling rate**: Trace collection labeled: `"Tail sampling: 10%"`
- **Instrumentation method**: Source services labeled: `SDK` / `Sidecar` / `Agent`
- **SLO threshold**: Horizontal line labeled: `"SLO: 99.9% availability / 30d window"`
- **Alert routing**: Alert node labeled: `"P1 → PagerDuty → On-call"` / `"P3 → Slack #infra-alerts"`

---

## 7. Content Density Rules

| Mode | Source services | Pipeline stages | Storage backends | Per Slide |
|---|---|---|---|---|
| Minimum | 1 | 2 | 1 | — |
| Optimal | 5–10 | 3–5 | 2–4 | single slide |
| Maximum | 20 | 6 | 6 | → split into pipeline + SLO slides |

**Overflow Strategy**: Primary slide shows collection-to-storage pipeline. Supplemental slide shows SLO/alert routing topology. Service list moved to appendix table.

---

## 8. Anti-Patterns

1. **Tools without signals**: Listing tool names (Prometheus, ELK) without showing which signal type flows through each — the diagram must show the signal (metrics/logs/traces) not just the tool.
2. **No retention policy**: Storage backends shown without retention duration — retention drives infrastructure sizing and compliance decisions.
3. **Alert-less architecture**: A monitoring diagram with no alerting path — monitoring without alerting is a dashboard, not an operational system.
4. **Missing application instrumentation method**: Source services shown with arrows to collectors but no indication of how instrumentation is applied (SDK / agent / sidecar) — methodology choice is an architectural decision.
5. **No SLO / SLI anchor**: Observability architecture without reference to what is being measured against (SLOs/SLIs) — observability exists to serve reliability commitments, not as an end in itself.

---

## 9. Industry Reference Patterns

**Google SRE Book — The Four Golden Signals**:
Google SRE defines four signals for any service: Latency (time to serve requests), Traffic (demand volume), Errors (failed requests rate), Saturation (utilization fraction). Every monitoring diagram should trace how each signal is measured → recorded → compared to SLO target → triggers burn-rate alert. The observability pipeline diagram must show this end-to-end chain, not just tooling topology.

**CNCF Observability TAG Whitepaper**:
CNCF defines observability around three pillars (metrics, logs, traces) unified by a context propagation standard (W3C TraceContext). The OTel Collector model forms a vendor-neutral hub that ingests from multiple SDKs and exports to multiple backends. The CNCF reference architecture shows: OTel SDK in app → OTel Collector → Prometheus (metrics) / Loki (logs) / Tempo (traces) → Grafana unified. This maps directly to Variant B of this spec.

**OpenTelemetry Specification — Telemetry Collection Model**:
OpenTelemetry defines a semantic convention for signal attributes (service.name, service.version, deployment.environment). All diagram annotations should use standard attribute names. The collector pipeline model: Receivers → Processors → Exporters. Diagram each pipeline stage within the OTel Collector box to show: (1) which receivers accept data, (2) which processors apply sampling/enrichment, (3) which exporters route to backends.

---

## 10. Production QA Checklist

- [ ] All three signal types (metrics, logs, traces) have explicit pipelines shown
- [ ] Instrumentation method annotated for each source service
- [ ] Storage backends include retention policy annotation
- [ ] SLO target lines are present (Variant A or C) with numeric thresholds
- [ ] Alert routing chain shown with severity → channel mapping
- [ ] Title uses slide placeholder (idx=0)
- [ ] OTel Collector or equivalent collection agent is shown as a distinct layer
- [ ] Colors distinguish signal types (metrics / logs / traces) consistently
- [ ] On-call escalation path visible (Alertmanager → PagerDuty / Slack)
- [ ] Presenter can trace a single error event from service to alert notification in 60 seconds
