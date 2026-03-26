# BA-10: RACI Governance Matrix — Business Architecture Diagram Spec

_Ref: PMI PMBOK (RACI Chart) | COBIT 2019 (Responsibility Model) | IT4IT (Governance & Compliance)_

---

## 1. Purpose & When to Use

**Definition**: A structured responsibility-assignment matrix that maps activities or decisions to roles using four accountability types: Responsible (executes), Accountable (owns), Consulted (provides input), Informed (notified of outcome).

**Use When**:
- Launching a new cross-team initiative where accountability is unclear
- Resolving chronic coordination failures caused by unclear ownership
- Documenting governance decisions for a program or service lifecycle
- Designing operating model: clarifying who decides vs. who executes
- Auditing compliance: showing that every critical activity has an accountable owner

**Questions Answered**:
- Who is accountable for each activity or decision?
- Who must be consulted before proceeding?
- Are any activities missing an accountable owner?
- Does any role have too many "Accountable" assignments (single-point-of-failure)?

**Primary Audience**: Programme Directors, Governance Boards, Operating Model designers, Risk & Compliance, PMO

---

## 2. Visual Layout Specification

**Structure**: Matrix table — rows = activities/decisions, columns = roles.

### Variant A: Standard RACI Table
- Column headers: Role names (max 8 columns)
- Row labels: Activity/decision names (left column)
- Cells: R / A / C / I with color encoding
- Best for: Programme governance, initiative launch, compliance audit

### Variant B: RACI with Activity Grouping
- Activities grouped by phase or domain (section headers)
- Group header rows span full table width with `#44546A` fill
- Best for: Large programs with distinct workstreams (15–30 activities)

### Variant C: Decision-Focused RACI (DACI variant)
- Uses D (Driver) / A (Approver) / C (Contributor) / I (Informed)
- Focus on decision points rather than operational activities
- Add "Decision Context" column on right side
- Best for: Architecture Review Board, change governance

**Grid Proportions**:
- Activity column width (left): 200pt
- Role column width: 70–90pt each
- Row height: 28–32pt
- Header row height: 36pt
- Maximum 8 role columns on one slide

---

## 3. Color Semantics

| RACI Type | Meaning | Fill Color | Text |
|---|---|---|---|
| R — Responsible | Executes the activity | `#53E3EB` | `#2F2F2F` Bold |
| A — Accountable | Owns the outcome (max 1 per row) | `#00CCD7` | White Bold |
| C — Consulted | Must provide input (2-way) | `#44546A` | White |
| I — Informed | Receives notification (1-way) | `#A5A7AA` | `#2F2F2F` |
| Empty cell | No assignment | White | — |
| Group header row | Activity phase/domain | `#44546A` | White Bold |
| Role header cell | Role name | `#2F2F2F` | White Bold |
| Warning cell | Multiple A in one row | Red dashed border | — |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight |
|---|---|---|---|
| Slide Title | Placeholder idx=0 | 28pt | Bold |
| Role Header | Column header | 10pt | Bold, White |
| Activity Name | Row label | 9–10pt | Regular, `#2F2F2F` |
| RACI Abbreviation | Cell content | 10pt | Bold |
| Group Header | Activity domain label | 11pt | Bold, White |
| Footnote | RACI definition key | 8pt | Regular, `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

RACI matrices are table-based — standard table shapes apply:

| Element | Meaning |
|---|---|
| Filled table cell (R/A/C/I) | Responsibility assignment |
| Empty table cell | No assignment |
| Rows with group header | Activity cluster separator |
| Bold column border | High-priority role column |
| Red dashed cell border | Multiple-A violation warning |
| Bottom footnote block | RACI legend definition |

**Connector Rule**: RACI matrices have no flow connectors. Tables are the primary structure. Do not add arrows between cells — they imply workflow which belongs in BA-03 Process instead.

---

## 6. Annotation Rules

- **RACI Legend**: Always include at bottom: "R=Responsible, A=Accountable, C=Consulted, I=Informed"
- **Multiple-A warning**: If any row has more than one "A", highlight with red dashed border — RACI principle requires exactly one accountable per activity
- **Blank row analysis**: Count activities with no R assignment (0 executors) — flag as governance risk
- **Role overload warning**: If one role column has more "A" assignments than 30% of rows, annotate with a "⚠ Overloaded" tag on column header
- **Version and date**: Add "Version: 1.0 | Date: YYYY-MM" in slide footer area (not placeholder — use text box at bottom)

---

## 7. Content Density Rules

| Mode | Activities | Roles | Table Size | Per Slide |
|---|---|---|---|---|
| Minimum | 4 | 3 | 4×3 | — |
| Optimal | 8–15 | 5–8 | 12×6 | 15 rows max |
| Maximum | 25 | 10 | 25×10 | → 2 slides |

**Overflow Strategy**: Split at workstream boundary (Variant B group headers). Each slide covers one workstream. First slide includes a role legend and RACI definition. Summary slide shows role-level load analysis (A-count per role).

---

## 8. Anti-Patterns

1. **Multiple Accountable per row**: RACI's cardinal rule — exactly one "A" per activity row. Multiple "A" creates authority ambiguity and is one of the most common governance failures.
2. **Over-consulting**: Marking 5+ roles as "C" for every activity — over-consultation creates decision paralysis. C should mean truly must-consult, not "be nice and include".
3. **Treating RACI as org chart**: Assigning activities to individuals instead of roles — RACI is role-based; when the person changes, the role stays.
4. **Missing activities**: Listing only happy-path activities and omitting exception handling, monitoring, and improvement activities — gaps in the RACI leave accountability voids.
5. **I = Not important**: Treating I as a courtesy — if a role is Informed, they receive actionable notifications; silence after an activity is a process failure.

---

## 9. Industry Reference Patterns

**PMI PMBOK Responsibility Assignment Matrix**:
PMBOK defines the RAM (Responsibility Assignment Matrix) as a project management tool mapping work packages to team members. The RACI chart is the most common RAM variant. PMBOK recommends creating RACI at two levels: project level (major deliverables) and detailed level (work package activities). Scale of diagram should match audience: executives see project-level; teams see detailed-level.

**COBIT 2019 Governance Responsibility Model (ISACA)**:
COBIT 2019 uses an extended accountability model called RACI-VS: Responsible, Accountable, Consulted, Informed, Verified, Signed-off. The Verified and Signed-off roles apply to governance and compliance activities. For IT governance and compliance contexts, consider adding Verified (quality check) and Signed-off (formal approval) columns for high-stakes activities.

**ITIL v4 Service Value System — RACI for Service Practices**:
ITIL 4 uses RACI to map service management practice roles. Key ITIL pattern: Service Owner = Accountable; Service Manager = Responsible; Service Desk / Operation Teams = Informed. This three-tier pattern (owner / manager / executor) is a clean starting template for any service governance RACI.

---

## 10. Production QA Checklist

- [ ] Every activity row has exactly one "A" (Accountable)
- [ ] No activity row has zero "R" assignments (no executor)
- [ ] RACI legend is present at bottom of every slide
- [ ] Role column headers represent roles, not individual names
- [ ] Title uses slide layout placeholder (idx=0)
- [ ] Multiple-A violations are flagged with red dashed border
- [ ] Role overload (>30% A in one column) is annotated with a warning
- [ ] Version number and effective date are noted on slide
- [ ] Activity names use action verbs: "Approve", "Execute", "Review", "Notify"
- [ ] RACI coverage is complete — every activity in scope has at least R and A assigned
