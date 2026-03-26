# GM-09: Use Case Scenario Diagram — GTM Diagram Spec

_Ref: SAP Industry Cloud Solution Briefs | Salesforce Industry Scenarios | IBM Solution Architecture Scenarios | Gartner Use-Case Taxonomy_

---

## 1. Purpose & When to Use

**Definition**: A step-by-step narrative diagram tracing a specific business scenario from trigger event to resolution — showing which product modules are activated at each step, who the actors are, and what the outcome is.

**Use When**:
- Presenting industry-specific solution decks where one scenario demonstrates product depth
- Converting feature lists into "story mode" to engage non-technical buyers
- Showing integration orchestration across multiple product modules
- Enabling field teams to demo using a familiar customer scenario

**Questions Answered**:
- Concretely, how does this product work in a real situation?
- Which team members interact with it, and when?
- What triggers the process, and what does "done" look like?
- Which modules are involved, and how do they connect?

**Primary Audience**: Pre-Sales, Solution Architects, Business Decision Makers (non-technical)

---

## 2. Visual Layout Specification

**Structure**: Left-to-right flow of scenario steps with actor swim lanes or numbered step cards.

### Variant A: Numbered Step Cards (Recommended for external audiences)
- 5–8 step cards arranged horizontally left to right
- Each card: Step number + action title + which product module handles it
- Actor icon above card (role/team)
- Arrows connecting cards with decision diamonds where applicable
- Best for: solution brief pages, industry scenario slides

### Variant B: Actor Swim Lane Scenario
- 3–4 swim lanes (by role: Operator, Manager, System/AI, Customer)
- Steps flow across lanes showing handoffs
- Product module badges appear at each step where product is activated
- Best for: process-heavy products where role boundaries matter (ITSM, CMDB, workflow platforms)

### Variant C: Scenario Story Board (Visual narrative)
- 4–6 "panels" arranged in a 2×3 or 3×2 grid
- Each panel: small scene illustration + 2-line description
- Best for: executive keynote, printed brochure inserts

**Grid Proportions**:
- Variant A step card: 100pt × 88pt; spacing: 20pt gap
- Variant B swim lane height: 80–96pt per lane
- Actor icon: 24×24pt above each card
- Product module badge: pill shape, 64pt × 20pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Trigger event card | Scenario start | `#44546A` bg, white text |
| Process step card | Standard action | `#53E3EB` light |
| Product-activated card | Module engaged | `#00CCD7` |
| External action card | Customer/external actor | White, `#A5A7AA` border |
| Module badge | Product module name | `#44546A` bg, white |
| Decision diamond | Branch point | White, `#2F2F2F` border |
| Outcome card | Final result | `#00CCD7` bold border |
| Arrow | Flow direction | `#2F2F2F` |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Scenario: [Name] / [Industry]" | 14pt | Regular |
| Step Number | Card number label | 11pt | Bold |
| Step Title | Action name | 9–10pt | SemiBold |
| Module Badge | Product module name | 8pt | Bold, white |
| Actor Label | Role above card | 8pt | Regular, gray |
| Outcome Label | Result statement | 10pt | Bold, `#00CCD7` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Rounded rect card | Scenario step |
| Diamond | Branch/decision point |
| Pill badge | Product module activated |
| Actor icon (person shape) | Role at this step |
| Solid arrow | Sequential flow |
| Dashed arrow | Optional or asynchronous |
| Bold-border card | Critical/highlighted step |

---

## 6. Annotation Rules

- **Scenario header**: Always specify: Industry / Role / Trigger event in the subtitle (e.g., "IT Ops / NOC Engineer / Production Alert Spike")
- **Module annotation**: Every product-activated step must show which product module handles it — links to the product capability map
- **Time annotation**: For time-sensitive scenarios, add "~2m" or "auto" time indicators on each step
- **Outcome measurement**: The final step must include a measurable outcome ("MTTR reduced from 45min to 8min")
- **Audience qualifier**: If scenario is industry-specific, mark "Applicable: Financial Services / Telecom" in footnote

---

## 7. Content Density Rules

| Mode | Steps | Actors | Per Slide |
|---|---|---|---|
| Minimum | 4 | 1 | — |
| Optimal | 6–8 | 2–3 | 1 slide |
| Maximum | 10 | 5 | → split into "trigger+diagnose" and "resolve+learn" slides |

---

## 8. Anti-Patterns

1. **Generic scenario**: "User encounters problem → system detects → AI resolves" — 5 words per step with no specifics looks like a marketing brochure, not a use case.
2. **No product involvement**: A scenario that shows the customer journey without ever engaging any product module — this is a business process diagram, not a solution use case.
3. **All steps are product steps**: A scenario where every step is handled by own product with no external actors or handoffs — real scenarios always involve people and interfaces.
4. **Missing outcome**: Steps that trail off without a named outcome — every scenario must answer "what does done look like?"
5. **Industry mismatch**: Using a retail scenario to pitch to a financial services buyer — scenarios must be matched to the prospect's industry context.

---

## 9. Industry Reference Patterns

**SAP Industry Cloud**:
SAP structures its industry cloud solution decks around 3–5 "core scenarios" per industry vertical. Each scenario follows a fixed format: trigger event → process steps → integration points → outcome. The product's value is communicated by showing which SAP modules activate at each step — making the breadth of functionality visible without requiring a feature list. This format is directly adaptable to any platform product.

**Salesforce Industry Scenario Diagrams**:
Salesforce's industry slides show multi-cloud scenarios: a field service scenario might activate Service Cloud + IoT + Field Service Lightning across steps. Each step card shows the "actor" (field tech, dispatcher, customer) and the product component. The scenario format is central to Salesforce's land-and-expand motion — showing buyers how one scenario naturally pulls in adjacent cloud products.

**IBM Garage Method for Cloud**:
IBM's solution architecture practice uses scenario-driven design: each scenario begins with an "IBM Point of View" statement (What job is being done? What value does IBM create?), then traces the scenario steps. Scenarios are tied to NPS/ROI outcomes. The methodology emphasizes that scenarios must be validated with customer interviews — scenarios not grounded in real customer stories have low credibility with technical evaluators.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Scenario is scoped to industry + role + trigger event
- [ ] All product-activated steps have module badges
- [ ] At least 2 distinct actor roles present
- [ ] Measurable outcome in final step
- [ ] Decision diamond present if scenario has meaningful branch
- [ ] Time annotations present for time-sensitive workflows
- [ ] Steps are specific enough that a sales engineer could demo them
- [ ] Scenario is matched to target industry segment
- [ ] Presenter can walk the scenario in under 90 seconds
