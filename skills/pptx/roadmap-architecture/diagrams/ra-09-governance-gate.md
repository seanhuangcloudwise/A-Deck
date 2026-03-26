# RA-09: 治理关口图 — Governance Gate Chart

_Ref: Stage-Gate® Model (Robert Cooper) | SAFe Lean-Agile Governance | PMI PMBOK Phase-Gate Review | PRINCE2 Decision Points | McKinsey Investment Approval Framework_

---

## 1. Purpose & When to Use

**Definition**: 以线性阶段块（Phases）+ 关口菱形（Gates）+ RACI 迷你表构成的横向流程图，展示从立项到收益实现的各阶段评审检查点，明确每个关口的决策标准和审批权限，服务于投资决策和阶段性过渡管理。

**Use When**:
- 新产品/新功能立项前说明评审流程和决策机制
- 向投资委员会/管理层展示"投多少钱"的分阶段决策逻辑
- PI/季度规划 Review 前，对齐各阶段关口标准
- 数字化转型项目管理，阶段边界清晰化
- 合规审计场景，展示产品/项目的治理流程

**Questions Answered**:
- 项目分为哪几个阶段，每个阶段的主要产出是什么？
- 每次阶段评审的判断标准是什么（Go / No-Go 依据）？
- 谁有权批准进入下一阶段？
- 当前项目处于哪个阶段，下一个关口何时到来？
- 对于未通过关口的项目，有哪些处置选项？

**Primary Audience**: Executive、投资委员会、Sponsor、PMO、产品委员会成员

---

## 2. Visual Layout Specification

**Structure**: 从左到右：起点（立项）→ [阶段块 → 关口菱形] × N → 终点（收益实现）

### Variant A: 标准 Stage-Gate 图（适合产品投资决策）
- 阶段数：4-6 个（Idea → Scope → Business Case → Development → Testing → Launch）
- 每个阶段块：宽度=相对耗时，标注阶段名 + 核心产出
- 关口菱形（G0~G5）：关口编号 + 1-2 行判断标准
- 关口下方 RACI 微表：Recommender / Decider 两行，标注角色简称
- Best for: 新产品立项评审、投资决策流程可视化

### Variant B: 精简关口地图（适合管理层快速汇报）
- 仅展示关口节点（菱形）+ 关口名称，阶段用水平距离表示
- 当前阶段用 `#00CCD7` 填充菱形高亮
- 每个关口旁标注"决策日期"（过去的用✓，未来的用○）
- Best for: 进度更新类幻灯片、当前状态快照

### Variant C: 多项目治理甘特（适合 Portfolio 治理）
- 纵轴：多个并行项目
- 横轴：时间（季度）
- 每个项目的关口时间点在时间轴上用菱形标注
- 颜色区分关口状态：绿（通过）/ 橙（推迟）/ 红（未通过）/ 灰（待审）
- Best for: PMO Portfolio Review、CPO 组合项目状态看板

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 阶段-关口主图: 中部 60% 高度
- 关口下方 RACI 区域: 固定高度 60px（选项：合并入菱形侧边注释）
- 项目当前状态标注行: 10% 高度（底部或顶部）
- 备选路径箭头: 从关口左侧分叉出"Hold / Kill / Recycle"支路

---

## 3. Color Semantics

| 元素 | 颜色 | 说明 |
|------|------|------|
| 阶段块 — 已完成 | `#E5E5E5` + ✓ | 当期前的已通过阶段 |
| 阶段块 — 当前进行 | `#E8FFFE` + 进度条 | 正在进行的阶段 |
| 阶段块 — 未来 | `#F5F5F5` 浅灰 | 尚未开始的阶段 |
| 关口菱形 — 待审 | `#A5A7AA` 灰 | 未到评审日期 |
| 关口菱形 — 已通过 GO | `#00CCD7` | 已批准进入下阶段 |
| 关口菱形 — 暂缓 HOLD | `#FF9500` 橙 | 需补充信息后重审 |
| 关口菱形 — 未通过 KILL | `#FF4444` 红 | 项目终止 |
| 关口菱形 — 当期活跃 | `#00CCD7` Bold border 3pt | 当前即将/正在评审 |
| 连接线（阶段-关口-阶段）| `#2F2F2F` 1pt | 正向流程线 |
| Kill/Hold 分叉线 | `#A5A7AA` 虚线 | 备选退出/暂缓路径 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 阶段块标题 | 阶段名 | 11pt | SemiBold | `#2F2F2F` |
| 阶段块内容 | 核心产出 1-2 行 | 8pt | Regular | `#44546A` |
| 关口菱形编号 | G0/G1... | 11pt | Bold | White 或 `#2F2F2F` |
| 关口判断标准 | 菱形下方 | 7pt | Regular | `#44546A` |
| RACI 标注 | Recommender/Decider | 7pt | Regular | `#2F2F2F` |
| 当前状态标注 | "当前阶段：XX" | 12pt | Bold | `#00CCD7` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 矩形（阶段块） | 规划/执行阶段，宽度可以表示相对历时 |
| 菱形 ◇（关口） | Go/No-Go 决策关口 |
| 圆形 ○ | 流程起点（立项启动）/ 终点（价值收益） |
| ✓ / ✕ / ⏸ 标记 | 关口结果（通过/终止/暂缓） |
| 向下分叉虚线 | Kill / Hold / Recycle 备选路径 |
| 进度条（阶段块内）| 当前阶段的完成度 |
| RACI 微表格 | 关口决策 RACI（2行2列） |

**Connector Rule**: 从左到右的主流程用实线连接；Kill/Hold/Recycle 分叉用虚线向下延伸，末端标注处置决策说明。

---

## 6. Annotation Rules

- **关口标准**: 每个菱形下方用 2 行 bullet 列出 Go 的最低满足条件（如 "商业 Case ROI > 20%" / "技术 PoC 通过"）
- **RACI**: 菱形旁注 "Recommender: @PM | Decider: @CPO" 格式
- **当前状态**: 当前所在阶段用深色边框高亮，配 "当前：第 X 期 | 评审日: YYYY-MM-DD"
- **关口结果历史**: 已通过关口内标 "GO ✓ YYYY-MM-DD"；未通过标 "HOLD ⏸ + 原因"
- **脚注**: 治理框架来源（Stage-Gate®/内部规范）+ 评审频率

---

## 7. Content Density Rules

| Mode | 阶段数 | 关口数 | Max per Slide |
|------|--------|--------|---------|
| Minimum | 3 | 2 | — |
| Optimal | 4-5 | 4-5 | — |
| Maximum | 6 | 6 | → 拆分为两页（立项前/立项后） |

**Overflow Strategy**: 超过 6 个阶段时，按"决策前"和"决策后"拆分为两页，共享同一治理标准说明页。

---

## 8. Anti-Patterns

1. **Gate without criteria（无判断标准的关口）**: 菱形只有名称没有 Go/No-Go 判断依据 — 空洞的流程图无法支撑实际决策，关口形同虚设。
2. **No RACI at gate（无授权说明）**: 关口没有标注谁有权决策 — 导致评审会上无法拍板，决策延迟。
3. **Missing Kill path（无终止路径）**: 所有路径都是 Go，没有 Kill/Hold 备选 — 隐含了"所有项目一定通过"的假设，违背治理纪律。
4. **Too many phases（阶段过多）**: 超过 7 个阶段挤在同一页 — 每个阶段块过窄，文字不可读，丢失实质内容。
5. **Gate disguised as checklist（关口变成打勾清单）**: 将 Go/No-Go 关口替换为"逐项打勾"的任务完成表 — 治理关口是决策点，不是任务列表，混淆了管理边界。

---

## 9. Industry Reference Patterns

**Stage-Gate® Model（Robert G. Cooper，1990s）**:
Robert Cooper 博士根据 NASA 和消费品行业新产品开发研究提出的 Stage-Gate® 模型。标准版分为 5 个阶段（Scoping → Build Business Case → Development → Testing & Validation → Launch）和 5 个关口（G1-G5）。每个关口由跨职能"守门人委员会"（Gate Keepers，通常是 BU 领导层）基于预定义的标准（must-meet & should-meet criteria）做出 Go/Kill/Hold/Recycle 四种决策。Stage-Gate 被 PMI 评为最广泛使用的新产品开发流程，超过 85% 的《财富》500 强企业使用某种形式的 Stage-Gate 模型。

**SAFe Lean-Agile Governance（精益敏捷治理）**:
SAFe 将传统的 Stage-Gate 模式改造为"Lean Portfolio Management (LPM)"中的"Guardrails + Funding Review"机制：不再基于特定里程碑触发评审，而是采用"持续价值假设验证"（Continuous Value Hypothesis）+ 固定节奏的 Portfolio Kanban Review（通常每季度一次）。SAFe 的 PI System Demo 可视为一种轻量级关口：每 12 周产出物向 Business Owners 演示，由其决定下一 PI 的投资是否持续。RA-09 的关口图可以适配为 SAFe 的 "funding gates" 视图。

**PRINCE2 Management Stage Boundaries（阶段边界决策）**:
PRINCE2 将项目分为"管理阶段"（Management Stages），阶段边界是 Project Board（由 Executive/Senior User/Senior Supplier 组成）的决策点。每个阶段结束时，PM 向 Project Board 提交"End Stage Report"，Board 决策：授权进入下一阶段 / 发起例外计划 / 前提变化触发关闭流程捷径。PRINCE2 的关口会议文化强调"关口不是形式"，而是真正的资金再承诺机制（阶段资金按阶段授权而非全额预批）。

**McKinsey Investment Committee Framework（投资委员会框架）**:
麦肯锡建议大型企业建立三级投资决策机制：L1（PM/BU 级，常规运营资金）/ L2（CPO/CFO 级，战略项目立项）/ L3（CEO/Board 级，平台级/收购级）。RA-09 的 RACI 微表格中，Recommender/Decider 的配置应与企业实际授权层级对齐。麦肯锡还建议每个关口至少包含三个维度的评估：战略契合度（Strategic Fit）/ 商业可行性（Commercial Viability）/ 执行可信度（Execution Credibility）。

---

## 10. Production QA Checklist

- [ ] 每个关口（菱形）有至少 2 条 Go 判断标准
- [ ] 每个关口标注了 RACI：Recommender + Decider
- [ ] Kill / Hold / Recycle 备选路径已画出（即使当前项目未触发）
- [ ] 当期所在阶段有高亮标注（加粗边框 + 进度条）
- [ ] 已通过关口内标注通过日期（"GO ✓ YYYY-MM-DD"）
- [ ] 阶段数 ≤ 6（超过则拆页）
- [ ] 幻灯片下方或侧边标注治理框架来源
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：下一个关口是什么、标准是什么、谁来决定
