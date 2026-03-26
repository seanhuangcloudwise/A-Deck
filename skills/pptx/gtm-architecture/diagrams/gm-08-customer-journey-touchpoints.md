# GM-08: Customer Journey with Touchpoints — GTM Diagram Spec

_Ref: Nielsen Norman Group Service Blueprint | JTBD (Jobs-to-be-Done) Framework | Salesforce Customer Success Journey | CEB (Gartner) Challenger Customer_

---

## 1. Purpose & When to Use

**Definition**: A horizontal timeline showing the customer's end-to-end experience with a problem domain — from awareness/trigger through evaluation, adoption, usage, and outcome — with own product's specific features or capabilities shown as touchpoints at each stage.

**Use When**:
- Showing how the product fits into the customer's work life rather than listing features
- Building empathy with buyers by naming their experience at each stage
- Differentiating by showing depth of support at stages competitors ignore
- Creating the "product story" section of a solution brief or white paper

**Questions Answered**:
- At what moment does the customer encounter the problem we solve?
- How does the product improve each stage of the journey?
- Where are the handoffs between teams, and how does the product support them?
- What is the measurable outcome at the end of the journey?

**Primary Audience**: PMM, Pre-Sales, Value Consultants, CX-aware executive buyers

---

## 2. Visual Layout Specification

**Structure**: Horizontal staged timeline with stacked detail rows.

### Variant A: Three-Row Journey (Recommended)
- Row 1: Journey stages (5–7 phases as horizontal bands)
- Row 2: Customer actions/concerns per stage (pain points or goals)
- Row 3: Product touchpoints per stage (feature or capability name)
- Best for: solution brief, playbook slides

### Variant B: Full Service Blueprint (5 rows)
- Row 1: Customer stages
- Row 2: Customer touchpoints (what they do/feel)
- Row 3: Front-stage product actions (visible to customer)
- Row 4: Back-stage product actions (automated/invisible)
- Row 5: Supporting processes / integrations
- Best for: deep-dive white paper, enterprise architect audience

### Variant C: Before/After Journey Overlay
- Two parallel horizontal lanes: Old journey (top, gray) / New journey (bottom, cyan)
- Stage-by-stage contrast showing product's impact
- Best for: opening slides of solution pitch, combining GM-03 + GM-08

**Grid Proportions**:
- Stage column width: equal distribution across content area
- Stage header height: 40pt
- Detail row height: 36–44pt per row
- Touchpoint block: 80pt × 28pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Stage header band | Journey phase | `#44546A` text, light bg |
| Customer action cells | What customer does | `#F5F5F5` |
| Product touchpoint blocks | Product capability here | `#00CCD7` fill |
| Pain point annotations | Friction or gap | `#A5A7AA` with warning icon |
| Outcome cell | Final measurable result | `#00CCD7` with ✓ |
| Back-stage automation | Invisible product action | `#53E3EB` light |
| Gap / no touchpoint | Product not present | White, dashed border |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Journey: [Role] / [Scenario]" | 14pt | Regular |
| Stage Label | Phase name | 10pt | Bold, `#44546A` |
| Row Label | Left-side row identifier | 9pt | Regular, `#A5A7AA` |
| Touchpoint Block | Feature/capability name | 9pt | Bold, white |
| Customer Action | Pain/goal text | 8–9pt | Regular |
| Outcome Label | Measured result | 10pt | Bold, `#00CCD7` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Wide horizontal band | Journey stage column |
| Pill / rounded rect | Product touchpoint |
| Speech bubble icon | Customer quote/reaction |
| Warning badge ⚠ | Pain point or friction |
| ✓ checkmark chip | Resolved/achieved outcome |
| Dashed vertical line | Stage transition |

**Connector Rule**: Downward arrows between customer action and product touchpoint are optional — should only be drawn when the connection is non-obvious.

---

## 6. Annotation Rules

- **Role specification**: Always specify "journey of [Job Title] at [company type]" in subtitle or callout — generic journeys are useless.
- **Pain quote**: Add at least one verbatim customer quote per major friction stage (short, in quotation marks, attributed to role not name)
- **Outcome metric**: The final stage must include a measurable outcome ("Resolved in 2h vs previous 3 days avg")
- **Touchpoint depth**: For each product touchpoint, note whether it's automated, assisted, or self-service
- **Coverage gap note**: If product does not cover a stage, keep the cell but mark "Partner: [X]" or "Roadmap Q3" rather than omitting it

---

## 7. Content Density Rules

| Mode | Stages | Rows | Touchpoints | Per Slide |
|---|---|---|---|---|
| Minimum | 4 | 2 | 4 | — |
| Optimal | 5–6 | 3–4 | 12–18 | 1–2 slides |
| Maximum | 8 | 5 | 30 | → split by journey arc |

---

## 8. Anti-Patterns

1. **Generic journey**: "Discover → Evaluate → Purchase → Use → Renew" — this is a sales funnel, not a customer journey. Journey must show what the customer is actually experiencing and doing.
2. **Every stage has a touchpoint**: Products that claim full-journey coverage for every stage should support it — otherwise it looks like a feature mapping exercise.
3. **No customer perspective**: Journey filled only with product features, with no customer actions, emotions, or goals — this isn't a customer journey, it's a product map.
4. **Missing pain points**: Journey without friction stages — the value of the journey map is identifying where pain occurs and where the product neutralizes it.
5. **Text overflow in cells**: Cells stuffed with 4–5 sentences — each cell should hold one precise statement or feature name.

---

## 9. Industry Reference Patterns

**Nielsen Norman Group Service Blueprint**:
NNG's service blueprint adds "evidence" (physical artifacts customer sees), "frontstage" (visible interactions), and "backstage" (behind-the-scenes processes) to the basic journey map. For GTM purposes, the "frontstage / backstage" separation is powerful — it shows customers what they experience while revealing the technical depth of the automation running beneath. NNG research shows that service blueprints are the most persuasive format for complex solution selling.

**Jobs-to-be-Done (JTBD) Framework**:
JTBD (Christensen / Ulwick) reframes the customer journey around the "job" the customer is hiring the product to do — not around product features or sales stages. Each stage of the journey should be mapped to a JTBD statement: "When [situation], I want to [motivation], so I can [expected outcome]." The journey diagram becomes the visualization of the jobs across the customer experience arc.

**CEB / Gartner Challenger Customer**:
Gartner's research on B2B buying shows that 6.8 stakeholders participate in enterprise buying decisions. The journey map must account for multiple concurrent roles visiting the same stage at different depths. The most effective solution narratives show how the product supports the "mobilizer" (internal champion) at each stage, not just the end user — creating a multi-persona layer in the journey diagram.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Journey is scoped to a specific role and scenario (not generic)
- [ ] Customer actions/goals are in each stage (not just product touchpoints)
- [ ] At least 2 friction/pain stages are marked
- [ ] At least one customer verbatim quote present
- [ ] Measurable outcome in final stage
- [ ] Product gap stages are marked (Partner / Roadmap), not hidden
- [ ] Touchpoint type noted (automated / assisted / self-service)
- [ ] Color semantics: pain = gray/warning, touchpoint = brand cyan
- [ ] Audience can follow the journey story without narration in 45 seconds
