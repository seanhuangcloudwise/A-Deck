# BA-08: Scenario Journey Map — Business Architecture Diagram Spec

_Ref: IDEO Design Thinking | Service Blueprint (G. L. Shostack) | TOGAF Business Scenario Technique_

---

## 1. Purpose & When to Use

**Definition**: A chronological narrative diagram showing how a specific actor moves through a business scenario — stage by stage — capturing touchpoints, pain points, emotions, supporting capabilities, and desired outcomes.

**Use When**:
- Presenting a complex business scenario to stakeholders in a storytelling format
- Identifying friction points and improvement opportunities in a multi-stage experience
- Designing business requirements for digital transformation from the user perspective
- Building executive empathy for operator or customer pain points
- Pre-sales or solution selling: illustrating how a product solves specific scenario problems

**Questions Answered**:
- What stages does the actor go through in this business scenario?
- Where does friction, delay, or failure occur?
- What capabilities or systems support each stage?
- What outcomes does the actor receive at the end of the journey?

**Primary Audience**: Product teams, UX designers (business context), Sales consultants, Business owners, Executive sponsors

---

## 2. Visual Layout Specification

**Structure**: Horizontal timeline with vertical swim-zones — one row per analysis dimension, reading left-to-right.

### Variant A: Simple Journey (3–5 stages, actor + pain points only)
- Top row: Stage name boxes (chevron or rect)
- Bottom row: Pain point annotations per stage
- Best for: Sales presentation, executive summary

### Variant B: Standard Journey (5–7 stages, multi-row)
- Row 1: Stage names (with icons optional)
- Row 2: Actor actions / tasks per stage
- Row 3: Pain points / friction (red indicators)
- Row 4: Supporting capabilities / systems
- Row 5: Opportunity / improvement actions
- Best for: Product design, business solution design

### Variant C: Service Blueprint (6–8 stages, front/back-stage split)
- Above the line: Customer-facing actions
- Line of Visibility: "---" horizontal separator
- Below the line: Backstage processes + IT systems
- Best for: Service design, operating model design, digital transformation

**Grid Proportions**:
- Stage header row: 18% of content area height
- Per additional row: equal-height distribution of remaining 82%
- Stage width: equal across all stages, 8pt gutters
- Row label column (left): 90pt width

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Stage block | Current scenario stage | `#00CCD7` |
| Normal actor action | Expected / smooth action | `#53E3EB` |
| Pain point / friction | Problem or delay | `#FF6B6B` (red-orange) text on white |
| Pain point indicator | Alert marker | Red `⚠` icon |
| Opportunity action | Improvement idea | `#44546A` + White text |
| Supporting capability | Enabler of the stage | `#A5A7AA` pill |
| Line of visibility (blueprint) | Front / back stage divider | `#2F2F2F` dashed line |
| Outcome marker | End-state achieved | `#00CCD7` star or check |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Stage Name | Chevron/block header | 11pt | SemiBold, White |
| Actor Name | Row label | 10pt | Bold |
| Row Label | Dimension label (left) | 9pt | SemiBold, `#44546A` |
| Action Description | Row cell content | 9pt | Regular |
| Pain Point Fragment | Red annotation | 8.5pt | Regular, `#CC0000` |
| Opportunity Note | Improvement text | 8.5pt | Italic, White |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Chevron (stage blocks) | Journey stage with direction |
| Rounded rect (≤4pt) | Action or task block |
| Red `⚠` icon + annotation | Pain point marker |
| Cyan check / star badge | Positive outcome / moment of delight |
| Dashed separator line | Line of visibility (Variant C) |
| Gray pill | Capability or system support annotation |
| Bracket or callout | Extended annotation / quote from actor |

**Connector Rule**: No explicit connectors between stage blocks — the chronological left-to-right layout implies sequencing. Within a cell, use brief bullet text, not sub-connectors. Cross-row dependencies (action → system) can use thin dashed vertical lines.

---

## 6. Annotation Rules

- **Pain intensity score**: Optional 1–3 flame icons (`🔥`) indicating severity of pain point
- **Frequency note**: Chip on pain point showing how often this friction occurs: "Daily", "Per transaction"
- **Outcome metrics**: At the final stage, add metric chips: "Avg. Resolution: 3.2 days" or "NPS impact: -15"
- **Actor quote bubble**: Optional callout bubble with a verbatim pain-point quote (8pt italic) — adds authenticity
- **Stage ownership**: Small department/team label in stage block footer (7pt, gray)

---

## 7. Content Density Rules

| Mode | Stages | Rows | Pain Points | Per Slide |
|---|---|---|---|---|
| Minimum | 3 | 2 | 1 | — |
| Optimal | 5–6 | 3–5 | 3–8 | 5 rows max |
| Maximum | 8 | 6 | 12 | → 2 slides |

**Overflow Strategy**: Split at a natural scenario phase boundary (e.g., "Before Service" / "During Service" / "After Service"). Each slide shows a complete sub-journey. Connect slides with a mini stage-map strip at the top.

---

## 8. Anti-Patterns

1. **Generic journey**: Using stock journey stages ("Discover → Consider → Purchase → Use → Advocate") without tailoring to the specific business scenario — generic templates defeat the purpose of scenario specificity.
2. **Missing actor identity**: Journeys without a named actor type ("Regional Branch Manager", not just "User") lose stakeholder relevance.
3. **Pain points without evidence**: Listing pain points without source data or observed frequency — claimed vs. evidenced pain points have very different credibility.
4. **No outcome definition**: Stopping the journey at the last process step rather than the actor's received outcome — the journey only completes when the actor gets what they needed.
5. **Overloaded cells**: Paragraph text in each cell — journey maps should be scannable in 30 seconds; each cell holds ≤ 10 words.

---

## 9. Industry Reference Patterns

**IDEO Design Thinking Journey Map**:
IDEO's human-centered design approach uses journey maps with 5 rows: Actions, Thoughts, Emotions, Pain Points, Opportunities. The emotion row uses a line graph showing highs and lows. For business architecture use, substitute "Emotions" with "Business Impact" (financial/operational effect of each stage). The principle of starting with human experience before designing solutions is core to the approach.

**G. Lynn Shostack's Service Blueprint (1984)**:
The original service blueprint, published in Harvard Business Review, introduced the front-stage/back-stage separation (Line of Visibility) and customer/employee/support process separation. For Variant C, use Shostack's three swim-zone structure: Customer Actions (above visibility line) / Onstage Employee Actions (below line, visible) / Backstage Operations (below line, invisible to customer) / Supporting Processes.

**TOGAF Business Scenario Technique (ADM Prerequisite Phase)**:
TOGAF uses Business Scenarios to identify requirements for architecture. A Business Scenario defines: environment, actors, desired outcome, and affected capabilities. The scenario journey map visualizes this narrative. Key TOGAF guideline: each scenario has one primary "problem owner" (the beneficiary of the architecture solution) — this actor anchors the journey.

---

## 10. Production QA Checklist

- [ ] A specific, named actor type is identified at the top of the diagram
- [ ] Stages are tailored to this specific scenario (not a generic template)
- [ ] Pain points have severity indicators and/or frequency notes
- [ ] Every pain point has a corresponding opportunity/improvement action
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Stage blocks are sequential left-to-right (no back-loops on single slide)
- [ ] No cell contains more than 10 words of body text
- [ ] Final stage shows a clear actor outcome (not just "process ends")
- [ ] Supporting capabilities reference BA-01 Capability Map vocabulary
- [ ] Presenter can walk through the scenario in under 2 minutes using the slide as visual anchor
