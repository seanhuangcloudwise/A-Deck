# GM-15: Sales Playbook Flow — GTM Diagram Spec

_Ref: Challenger Sale (CEB/Gartner) | Force Management Command of the Message | SPIN Selling (Neil Rackham) | Sandler Sales Methodology_

---

## 1. Purpose & When to Use

**Definition**: A visual step-by-step flow representing the standard sales motion — from pre-call preparation through discovery, demonstration, objection handling, and close — designed to make the selling methodology visual and repeatable for field teams.

**Use When**:
- Building the core page of a sales battle card for field reps
- Onboarding new sales team members to the standard methodology
- Creating a "one-page play" sales rep can carry into a meeting
- Training channel partners on how to sell the product

**Questions Answered**:
- What are the standard steps in every sales conversation?
- What questions must be asked at each stage?
- How should common objections be handled (specifically)?
- What is the expected output/deliverable at each stage?

**Primary Audience**: Sales reps, Sales Ops, Channel partners, Sales enablement team

---

## 2. Visual Layout Specification

**Structure**: Vertical or horizontal step-by-step flow showing sales motion stages with sub-actions and outputs.

### Variant A: Horizontal Stage Cards (Recommended for deck usage)
- 5–6 stage cards arranged horizontally
- Each card: Stage name + 2–3 key actions + expected output
- Arrow connectors between stages
- Optional: common objection callout box below each stage
- Best for: sales enablement deck, deal review meetings

### Variant B: Vertical Swim Lane Playbook (Battle card format)
- Left column: Stage
- Middle column: Rep actions + questions to ask
- Right column: Expected output / success criteria
- Bottom row per stage: Common objection + counter-message
- Best for: printed or digital 1-page battle card

### Variant C: Decision Tree Flow
- Stages as boxes with decision diamonds at key branch points
- Branches based on prospect response ("Has executive sponsor? → Yes / No")
- Best for: complex sales with multiple paths (enterprise vs. SMB, PLG hand-raise vs. outbound)

**Grid Proportions**:
- Variant A stage card: 100pt × 88pt; spacing: 20pt
- Variant B row height: 52pt; column widths: 15% / 50% / 35%
- Arrow width: 1.5pt

---

## 3. Color Semantics

| Element | Meaning | Fill Color |
|---|---|---|
| Stage card | Sales process phase | `#00CCD7` header, white body |
| Output chip | Expected deliverable | `#44546A` bg, white |
| Objection callout | Common objection | `#F5F5F5` bg, `#A5A7AA` border |
| Counter-message | Response to objection | White bg, `#00CCD7` left border |
| Decision diamond | Branch point | White, `#2F2F2F` border |
| Warning indicator | Disqualify signal | `#A5A7AA` with ✗ |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Slide Subtitle | "Sales Playbook: [Product/Segment]" | 14pt | Regular |
| Stage Name | Card header | 11pt | Bold, White |
| Action Item | Step within stage | 9pt | Regular |
| Output Label | Deliverable name | 9pt | Bold, `#44546A` |
| Objection | "When prospect says…" | 8pt | Italic, gray |
| Counter-message | Response language | 9pt | Regular |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|---|---|
| Stage card (rect) | Process phase |
| Output chip (pill) | Deliverable at end of stage |
| Diamond | Branch / decision |
| Speech bubble | Prospect objection |
| Bold-left-border rect | Counter-message frame |
| ✓ badge | Stage completion criterion |

---

## 6. Annotation Rules

- **Output per stage**: Every stage must name what the rep should "walk away with" (discovery notes, qualification score, confirmed stakeholders list, verbal commit, signed order form).
- **Objection-counter pairs**: For the top 2–3 objections, include the verbatim objection and the suggested counter-message (max 2 sentences, tested language).
- **Role specification**: Note whether each stage is executed by SDR, AE, SE, or CSM — prevents confusion in team-selling environments.
- **Exit criteria**: Define what "done" means for each stage: "Discovery complete when MEDDIC score ≥ 4/6."
- **Version control**: Sales playbooks become outdated fast — include "Playbook version / last updated [date]" in footer.

---

## 7. Content Density Rules

| Mode | Stages | Actions per Stage | Per Slide |
|---|---|---|---|
| Minimum | 4 | 2 | — |
| Optimal | 5–6 | 3 | 1–2 slides |
| Maximum | 8 | 5 | → split: Acquisition / Expansion plays |

---

## 8. Anti-Patterns

1. **Discovery stage with no discovery questions**: A "Discovery" box with "Understand customer needs" — discovery must contain the specific questions the rep asks, not a generic description.
2. **Objection list without counter-messages**: Listing objections without responses — the playbook exists to give reps words, not just awareness of challenges.
3. **No exit criteria**: Stages without success criteria lead to deals staying in "stage 2" indefinitely with no progression discipline.
4. **Too many stages**: An 11-step playbook on a deck slide creates cognitive overload — maximum 6 stages for a one-page play.
5. **Generic methodology labels**: Copying "SPIN" or "Challenger" stage names without adapting them to own product — reps need product-specific language.

---

## 9. Industry Reference Patterns

**Challenger Sale (CEB / Gartner)**:
The Challenger model prescribes a 3-step sales approach: Teach (provide insight the buyer didn't know), Tailor (adapt the insight to the buyer's specific situation), Take Control (lead the buying process proactively). The playbook diagram renders "Teach → Tailor → Take Control" as a flow with specific talk-tracks and materials at each step. Challenger-trained sales teams outperformed by 67% in complex B2B opportunities (CEB → Gartner 2011 research).

**Force Management Command of the Message**:
Command of the Message (CoM) is a sales training framework built around: Required Business Outcomes (RBOs) → Metrics (of those outcomes) → Decision Criteria → Unique Differentiators → Competitive Traps (questions that disadvantage competitors). The playbook flow activates CoM by embedding RBO discovery questions in the Discovery stage and competitive trap questions in the Demonstration stage.

**SPIN Selling (Neil Rackham)**:
SPIN structures discovery into four question types: Situation (baseline facts), Problem (implicit pain), Implication (consequences of the problem), Need-payoff (value of the solution). The highest-impact stage is "Implication" — helping the buyer understand the magnitude of their problem. The playbook flow should show SPIN question sequencing in the discovery stage.

---

## 10. Production QA Checklist

- [ ] Title/subtitle use placeholders (idx=0/idx=1)
- [ ] Each stage has specific actions (not generic descriptions)
- [ ] Exit criteria defined per stage
- [ ] Expected output (deliverable) visible per stage
- [ ] Top 2–3 objection + counter-message pairs present
- [ ] Rep role (SDR/AE/SE/CSM) noted per stage
- [ ] Methodology source cited if using a named framework
- [ ] Version and date in footnote
- [ ] 5–6 stages maximum on one slide
- [ ] Rep can navigate a live deal conversation using this card without additional reference material
