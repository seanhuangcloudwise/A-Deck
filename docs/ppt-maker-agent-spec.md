# A-Deck Product Specification (中英双语)

## 1. Product Positioning / 产品定位
- EN: A-Deck is an enterprise-grade PPTX generation and editing agent focused on 90-point deliverable quality, master consistency, and architecture-friendly expression.
- 中文：A-Deck 是面向企业交付场景的 PPTX 生成与编辑智能体，定位"做90分的PPT"，强调可交付质量、母版一致性与架构表达能力。

## 2. Target Users & Scenarios / 目标用户与场景
- EN: Product managers, solution architects, pre-sales engineers, and operations teams.
- 中文：产品经理、解决方案架构师、售前工程师与运营团队。
- EN: Typical scenarios include product intro decks, architecture decks, roadmap updates, and template-based renewals.
- 中文：典型场景包括产品介绍、架构方案、路线图更新与模板化复用。

## 3. Scope In / Scope Out / 范围边界
### Scope In
- EN: Workflow 1-6 execution, template/master reuse, XML editing workflow, QA verification, and knowledge persistence.
- 中文：支持 Workflow 1-6、模板与母版复用、XML 编辑链路、QA 校验与知识沉淀。

### Scope In (Planned Upgrade Focus)
- EN: Workflow 7+ design for PPT scenarios, portfolio roadmap planning PPT design, and KPI framework PPT design.
- 中文：后续重点纳入 Workflow 7+ 的 PPT 场景设计、路线图规划体系 PPT 设计与 KPI 框架 PPT 设计。

### Scope Out
- EN: Non-PPT document generation outside PPT/PPTX deliverables.
- 中文：超出 PPT/PPTX 交付范围的非PPT文档生成不在本规范内。

## 4. Workflow Functional Contracts / 工作流功能说明

## W1 Create from Scratch / 从零创建
- Trigger / 触发：User asks to create a new PPT.
- Inputs / 输入：Topic, audience, duration, slide count, tone/style.
- Process / 处理：Requirement gathering -> outline confirmation -> design system selection -> layout planning -> generation + QA.
- Outputs / 输出：Runnable generator script + PPTX file + QA evidence.
- Guardrails / 边界：No placeholder text, no repeated layout abuse, strict visual QA.

## W2 Edit Existing PPTX / 编辑现有PPT
- Trigger / 触发：User provides PPTX and asks for modifications.
- Inputs / 输入：Existing PPTX, edit goals, page scope.
- Process / 处理：Analyze -> unpack -> structural edits -> content edits -> clean/pack -> QA.
- Outputs / 输出：Updated PPTX with structure integrity.
- Guardrails / 边界：No orphan slides, no malformed XML, relation consistency required.

## W3 Analyze PPTX / 分析PPT
- Trigger / 触发：User asks for review/check/audit.
- Inputs / 输入：PPTX file.
- Process / 处理：Text extraction + thumbnail generation + structural/visual audit.
- Outputs / 输出：Review findings, risks, and suggested fixes.
- Guardrails / 边界：Findings-first reporting, avoid cosmetic-only comments.

## W4 Template-based Generation / 模板化生成
- Trigger / 触发：User asks to generate using an existing style/template.
- Inputs / 输入：Template PPTX, target content, style constraints.
- Process / 处理：Layout inventory -> content mapping -> slot filling -> style QA.
- Outputs / 输出：Template-consistent PPTX.
- Guardrails / 边界：Preserve placeholders, maintain master/theme linkage.

## W5 Learn from PPTX / 从PPT学习
- Trigger / 触发：User asks to learn style/structure from attached PPTX.
- Inputs / 输入：Sample PPTX + target scene.
- Process / 处理：Extract style dimensions -> summarize -> confirm -> persist to knowledge base.
- Outputs / 输出：Updated style profile, slide structures, session log.
- Guardrails / 边界：No write without confirmation.

## W6 Master Extraction / 母版提取
- Trigger / 触发：User asks to extract and deposit master assets.
- Inputs / 输入：Source PPTX.
- Process / 处理：Unpack/analyze masters -> candidate summary -> gated confirmation -> deposit.
- Outputs / 输出：Master package in master-library with manifest/preview/assets.
- Guardrails / 边界：Strict deposit gate, no write on skip.

## W7 Strategic Product Roadmap Design / 战略产品路线图设计
- Trigger / 触发：User asks to create a strategic roadmap, annual plan, or multi-year product timeline.
- Inputs / 输入：Strategic themes, product lines, time horizon, target audience (executive/board).
- Process / 处理：Select RA diagram type (RA-01~RA-04) -> data collection -> roadmap layout -> visual QA.
- Outputs / 输出：PPTX with strategic roadmap slides (timeline/capability/heat matrix views).
- Guardrails / 边界：Must use RA-xx spec constraints; time axis mandatory; Cloudwise palette enforced.

## W8 Prioritization & Portfolio Balancing / 优先级排序与组合平衡
- Trigger / 触发：User asks to visualize initiative priorities, investment portfolio, or resource allocation.
- Inputs / 输入：Initiative list with scores (RICE/WSJF), resource data (FTE/budget), scenario assumptions.
- Process / 处理：Select RA diagram type (RA-02/RA-07/RA-10) -> scoring validation -> matrix/scenario layout -> QA.
- Outputs / 输出：PPTX with prioritization matrix, resource-priority view, or scenario investment slides.
- Guardrails / 边界：Scoring method must be annotated; bubble size legend required; ≤20 items per slide.

## W9 Quarterly Execution Planning / 季度执行规划
- Trigger / 触发：User asks to create quarterly plan, release train, dependency map, or governance gate chart.
- Inputs / 输入：Feature/initiative backlog, team assignments, dependencies, release milestones, gate criteria.
- Process / 处理：Select RA diagram type (RA-05/RA-06/RA-09) -> dependency analysis -> layout -> QA.
- Outputs / 输出：PPTX with release train, critical path map, or governance gate slides.
- Guardrails / 边界：Critical path must be highlighted; all milestones need Owner + date; gate criteria mandatory.

## W10 KPI Outcome Review & Replanning / KPI 结果回顾与再规划
- Trigger / 触发：User asks to create KPI progress view, risk board, or outcome review slides.
- Inputs / 输入：KPI actuals vs targets, risk register, mitigation status, review findings.
- Process / 处理：Select RA diagram type (RA-03/RA-08) -> data overlay -> plan-vs-actual comparison -> QA.
- Outputs / 输出：PPTX with KPI milestone ladder, risk kanban, or review summary slides.
- Guardrails / 边界：Baseline value required; Plan vs Actual overlay mandatory; P×I scoring method noted.

## 5. Non-Functional Baseline / 非功能基线
- EN: Deliverability first (file opens cleanly, no corruption).
- 中文：可交付优先（文件可正常打开、无损坏）。
- EN: Reproducibility (scripts and steps are traceable).
- 中文：过程可复现（脚本与步骤可追踪）。
- EN: Visual quality gate (content + rendering + structure checks).
- 中文：质量门禁（内容、视觉、结构三重校验）。
- EN: Safety controls for destructive/system-level operations.
- 中文：对删除与高权限操作保持安全门控。

## 6. Acceptance Checklist / 验收检查
- EN: Workflow intent is correctly identified.
- 中文：工作流识别正确。
- EN: Input/output contracts are met for selected workflow.
- 中文：输入/输出契约满足所选工作流。
- EN: QA evidence is available before completion.
- 中文：交付前具备QA证据。
- EN: Terminology is consistent across docs.
- 中文：术语在文档间一致。

## 7. Source-of-Truth Policy / 文档主源策略
- EN: The global agent file is runtime source; this file is the version-controlled mirror for repository collaboration.
- 中文：全局 agent 文件作为运行时主源；本文件作为仓库内可版本化镜像用于协作。
- EN: PROJECT.md and skills/pptx/SKILL.md should remain concise and link back here.
- 中文：PROJECT.md 与 skills/pptx/SKILL.md 保持摘要化并回链本文件。
