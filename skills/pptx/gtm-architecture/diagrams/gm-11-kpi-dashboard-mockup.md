# GM-11: KPI Dashboard Mockup — GTM Diagram Spec

_Ref: Tableau / Looker Dashboard Design Best Practices | SaaS Metrics Framework (David Skok) | Gartner I&O Dashboard Standards | ITIL Performance Management_

---

## 1. Purpose & When to Use

**Definition**: A presentation-quality mockup of the operational or executive dashboard that the product enables — showing before/after metric states or a representative set of live KPI cards to make the product's measurement capability tangible to buyers.

**Use When**:
- Supplementing a demo with a "what your dashboard would look like" preview slide
- Showing monitoring/observability/analytics products in the context of real metrics
- Making abstract platform capabilities concrete for non-technical buyers
- Adding visual proof to business value claims in solution briefs

**Questions Answered**:
- What does "improved" look like as a dashboard view?
- What metrics can I track after deploying this product?
- How do I show my team/management we're getting value?

**Primary Audience**: IT Operations, Business Analysts, Operations Managers, Data-informed executives

---

## 2. Visual Layout Specification

**Structure**: Grid of KPI cards / gauge tiles arranged as a representative dashboard panel.

### Variant A: Metric Card Grid (Recommended — PowerPoint-native)
- 4–6 metric cards arranged in 2×2 or 2×3 grid
- Each card: metric name + current value (large) + trend indicator + context bar
- Optional: small sparkline or mini bar chart in each card
- Best for: solution brief, executive deck, sales proof slide

### Variant B: Before/After Dashboard Panel
- Two panels side-by-side (old monitoring / new AI-powered)
- Left: sparse, gray, manual metrics; Right: dense, cyan, automated insights
- Maps well with GM-03 Before/After Comparison
- Best for: differentiation when competing against legacy tools

### Variant C: Layered Operational View
- Three card layers: Real-time alerts (top) / Trend analysis (middle) / Business KPIs (bottom)
- Represents data → insight → decision hierarchy
- Best for: monitoring/observability products, AIOps platforms

**Grid Proportions**:
- KPI card: 130pt × 70pt minimum
- Metric value: 20–22pt font (large numeric)
- Card grid gutter: 8pt
- Dashboard outer border (full area): subtle gray or brand tint

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Card background | Individual metric tile | White |
| Metric value (healthy) | Good status | `#00CCD7` |
| Metric value (warning) | Attention needed | `#F5A623` (amber) |
| Metric value (critical) | Problem state | `#C0392B` (red) |
| Trend up arrow | Positive change | `#00CCD7` |
| Trend down arrow | Negative change | `#C0392B` |
| Sparkline | Trend visualization | `#00CCD7` line |
| Dashboard background | Container area | `#F9FAFB` very light gray |
| Dashboard title bar | Panel header | `#44546A` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Sample Dashboard: [product/scenario]" | 14pt | Regular |
| Dashboard Panel Title | Top bar label | 10pt | Bold, White |
| Metric Name | Card label | 8pt | Regular, `#A5A7AA` |
| Metric Value | Large number | 20–22pt | Bold, see color |
| Trend Indicator | "↑12% vs last week" | 8pt | SemiBold |
| Card Context Bar | Threshold or target vs actual | 7pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect card | Individual metric tile |
| Thin bar / progress bar | Remaining capacity / threshold |
| Sparkline (polyline) | Trend visualization |
| ▲ / ▼ arrow glyph | Positive / negative trend |
| Alert badge (circle) | Status indicator (green/amber/red) |
| Dashboard frame rect | Container boundary |

**Connector Rule**: No logical connectors between cards — layout proximity implies grouping. If relationships are needed, use a separate diagram.

---

## 6. Annotation Rules

- **"Sample data" disclaimer**: All numbers in the mock dashboard must be labeled "Sample data for illustration" — either as a footnote or a watermark-style overlay.
- **Source annotation**: If based on real customer scenario, add "Inspired by [Industry] customer deployment" (anonymized).
- **Threshold lines**: If showing a threshold or SLA target, annotate with the threshold value and what it means.
- **Time range**: Add a small "Last 7 days / Last 30 days" label to each relevant metric card.
- **Role callout**: Add a small annotation indicating which team role primarily reads this dashboard.

---

## 7. Content Density Rules

| Mode | Metric Cards | Per Slide |
|---|---|---|
| Minimum | 3 | — |
| Optimal | 4–6 | 1 slide |
| Maximum | 9 | → split by dashboard section |

---

## 8. Anti-Patterns

1. **Screenshot paste**: Pasting a screenshot of an actual UI dashboard — resolution is too low for presentation quality, brand inconsistency, and may contain confidential customer data.
2. **All green metrics**: A mock dashboard where every KPI shows perfect health — buyers don't find this credible or useful. Show at least one warning or improving metric.
3. **Unreadable micro-text**: Dashboard cards with 6pt font — metric names must be readable at projection distance.
4. **No sample data disclaimer**: A mock showing specific numbers like "99.97% uptime" without a disclaimer may be read as a contractual commitment.
5. **Too many metrics**: 20+ cards on a single deck slide — choose the 5 metrics that best demonstrate product value, not all available metrics.

---

## 9. Industry Reference Patterns

**Tableau Dashboard Best Practices**:
Tableau's design guidelines prescribe a visual hierarchy: headline metrics at top (large, single number), trend context in middle (sparkline, bar), dimensional breakdown at bottom. Colors are strictly semantic: red = problem, orange = warning, green/brand = healthy. The same hierarchy applies to PPT mockups.

**SaaS Metrics Framework (David Skok / ForEntrepreneurs)**:
SaaS performance dashboards typically surface: ARR growth rate, NRR (Net Revenue Retention), CAC payback, LTV:CAC ratio, and churn rate. For operator-level products, equivalent operational metrics:  MTTR (Mean Time to Resolve), change failure rate, deployment frequency. Selecting the right tier of metrics for the right buyer audience is as important as the layout.

**ITIL Performance Management**:
ITIL's performance management model separates metrics into three layers: Operational (real-time, ≤5 min lag), Tactical (daily/weekly trend), Strategic (monthly/quarterly business KPIs). Dashboard mockups for IT products gain credibility when these three layers are visually distinct — it shows the product's understanding of how IT teams actually consume operational data.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] "Sample data for illustration" disclaimer present
- [ ] At least one warning-state metric (not all green)
- [ ] All metric values are readable at 80% zoom
- [ ] Time range labeled per metric card
- [ ] Color semantics: healthy=cyan, warning=amber, critical=red
- [ ] No screenshot pastes (PPT-native shapes only)
- [ ] Dashboard panel title identifies product/dashboard name
- [ ] Maximum 6 metric cards per slide
- [ ] Presenter can explain what each metric measures and why it matters in 30 seconds total
