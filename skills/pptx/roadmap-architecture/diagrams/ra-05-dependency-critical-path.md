# RA-05: 依赖与关键路径图 — Dependency & Critical Path Map

_Ref: CPM/PERT Network Diagram | PMI PMBOK Critical Path Method | Atlassian Jira Dependency Tracker | Linear.app Dependency View | SAFe Program Board_

---

## 1. Purpose & When to Use

**Definition**: 以有向无环图（DAG）的形式呈现举措/功能/系统之间的前置依赖关系，并高亮显示关键路径（从起点到终点不可压缩的最长路径），用于识别交付瓶颈和阻塞风险。

**Use When**:
- PI Planning 或季度规划中，识别跨团队 Epic/Story 的依赖
- 多系统并行开发，分析哪些模块是关键瓶颈
- 项目交付风险评审，说明"如果 X 延期，Y 受何影响"
- 路线图中举措数量超过 5 个且存在明确先后关系
- 里程碑节点受到多个上游任务约束，需要找到关键链路

**Questions Answered**:
- 哪些举措/任务必须先完成，才能启动其他？
- 整个项目的最短交付周期是多少（关键路径总工期）？
- 如果当前某个关键节点延期，整体计划受何影响？
- 哪些任务有浮动时间（Float），可以优先级调整？

**Primary Audience**: PM、Delivery Lead、Tech Lead、PMO、Engineering Manager

---

## 2. Visual Layout Specification

**Structure**: 从左到右有向图，节点 = 举措/任务/里程碑，有向边 = 依赖关系；关键路径用颜色特别标注

### Variant A: 标准 DAG（适合中等复杂度依赖）
- 节点排列：按层级从左到右（第 0 层=起点，末层=终点）
- 节点形状：圆角矩形，宽度=任务 ID+名称
- 关键路径边：红/橙色粗实线箭头（`#FF6B35` 2pt）
- 非关键路径边：灰色细虚线箭头（`#A5A7AA` 1pt）
- Best for: 交付计划评审、Sprint 依赖分析

### Variant B: 里程碑网络图（适合高层汇报）
- 节点仅保留关键里程碑（≤ 10 个）
- 每个里程碑节点：事件名 + 计划日期 + Owner
- 关键路径用贯穿全图的红线从头标注到末
- 非关键支线节点变小（半透明）
- Best for: 董事会/Sponsor 风险汇报、跨部门拉通

### Variant C: SAFe Program Board（适合 PI 规划）
- 横向为迭代（Sprint 1-6），纵向为团队泳道
- Feature 卡片在交叉格中放置
- 依赖用彩色线弦连接不同团队的 Feature 卡片
- 风险/阻塞标记：红色圆圈覆盖在有阻塞的连接线上
- Best for: PI Planning 大房间输出、Scrum of Scrums 可视化

**Slide Proportions**:
- Title placeholder: 顶部 12%
- DAG 图区域: 占 78% 内容高度，满宽
- 左端起点节点距左边距: 5% 幻灯片宽度
- 右端终点节点距右边距: 5% 幻灯片宽度
- 底部图例: 固定 56px 高度（关键路径线/非关键线/阻塞标记说明）

---

## 3. Color Semantics

| 元素 | 颜色 | 说明 |
|------|------|------|
| 关键路径节点边框 | `#FF6B35` 橙红 2pt | 在关键路径上的节点 |
| 关键路径连接线 | `#FF6B35` 橙红 2pt 实线 | 关键路径上的依赖边 |
| 非关键节点 | `#A5A7AA` 灰色边框 | 有浮动时间的任务 |
| 非关键连接线 | `#A5A7AA` 1pt 虚线 | 非关键依赖边 |
| 节点内容填充 | `#E8FFFE` 浅青（关键）/ `#F5F5F5`（非关键） | 节点背景色 |
| 完成节点 | `#00CCD7` 填充 + ✓ | 已完成的节点 |
| 阻塞节点 | `#FF4444` 边框 + ⚡ | 当前已阻塞的节点 |
| 里程碑节点 | `#44546A` 菱形或加粗 | 关键里程碑（非普通任务） |
| 起点/终点 | `#2F2F2F` 椭圆 | 项目开始/结束节点 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 节点任务名 | 节点内首行 | 8-9pt | SemiBold | `#2F2F2F` |
| 节点日期/工期 | 节点内次行 | 7pt | Regular | `#44546A` |
| 连接线标签 | 箭头中段（可选） | 7pt | Regular | `#A5A7AA` |
| 关键路径工期标注 | 末节点旁 | 11pt | Bold | `#FF6B35` |
| 图例标签 | 底部 | 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 圆角矩形 | 举措/任务节点（小圆角 ≤ 4pt） |
| 菱形 ◇ | 里程碑节点 |
| 椭圆 | 起点 / 终点 |
| 有向实线箭头（橙粗） | 关键路径依赖 |
| 有向虚线箭头（灰细） | 非关键路径依赖 |
| 红色圆圈 ⭕ | 阻塞标记（覆盖在节点上） |
| 绿色对勾 ✓ | 节点已完成 |

**Connector Rule**: 所有箭头方向必须一致（从前置任务指向后置任务，即从依赖方指向被依赖方），不允许循环依赖出现在图中。如发现循环依赖，在脚注标注"存在循环依赖，需先解耦"。

---

## 6. Annotation Rules

- **关键路径总工期**: 在终点节点旁标注"Critical Path: XX 天/周"
- **Float 浮动时间**: 在非关键节点旁可选标注 "Float: +X 天"（说明可延期范围）
- **阻塞原因**: 阻塞节点旁简短标注阻塞原因，如 "等待 API 规范确认 @Team-B"
- **Owner**: 每个节点内含或旁边标注负责团队/人简写
- **脚注**: 关键路径计算方法（CPM/手工估算）+ 截至日期

---

## 7. Content Density Rules

| Mode | 节点数 | 依赖边数 | Max per Slide |
|------|--------|---------|---------|
| Minimum | 4 | 3 | — |
| Optimal | 8-15 | 10-20 | — |
| Maximum | 20 | 30 | → split or simplify |

**Overflow Strategy**: 超过 20 个节点时：
1. 第一页：仅显示关键路径节点 + 直接阻塞节点（精简视图）
2. 第二页：完整依赖图（附录级别，供技术评审用）

---

## 8. Anti-Patterns

1. **Spaghetti graph（面条图）**: 节点和边过多且交叉杂乱，无法识别关键路径 — 应精简到只保留关键链路和直接依赖。
2. **Bidirectional arrows（双向箭头）**: 使用双向箭头表示"相互依赖" — 应拆解为两个单向依赖并检查是否存在循环设计问题。
3. **Missing critical path highlight（无关键路径高亮）**: 所有边颜色相同 — 关键路径图的核心价值在于区分关键和非关键，必须用颜色区分。
4. **Dates without owners（有日期无Owner）**: 里程碑节点标注了日期但没有负责人 — 无人负责的里程碑是风险，必须标注 Owner。
5. **Feature-level overload（功能级细节过载）**: 将所有 Story 级别的依赖放进同一张图 — 应提升为 Epic/Initiative 级别，Story 级依赖在 Scrum Board 中管理。

---

## 9. Industry Reference Patterns

**Critical Path Method (CPM) — PMI/PMBOK Standard**:
CPM 由 DuPont/Remington Rand 于 1950 年代提出，核心：在活动网络图中找出从项目开始到结束工期最长的路径（即关键路径）。关键路径上的任何活动延期将直接导致项目整体延期；非关键路径上的活动有"浮动时间（Float）"，可以在不影响整体进度的范围内延迟。RA-05 采用 CPM 逻辑，将关键路径用橙红色高亮，帮助 PM 和 Sponsor 快速识别需要重点保护的交付节点。

**PERT (Program Evaluation and Review Technique)**:
PERT 是 CPM 的概率化版本，每个活动有乐观/最可能/悲观三种工期估算。在 RA-05 的节点上可以标注 PERT 三点估算（O/M/P），在箭头上标注期望工期 `E = (O+4M+P)/6`。PERT 特别适合创新性工作（工期不确定性高），帮助团队表达"最坏情况下关键路径会延长多少"。

**Atlassian Jira Dependency Tracker / Linear.app**:
现代研发工具中，依赖关系可视化已成为团队协作标配。Jira Advanced Roadmap 的依赖线用颜色区分"阻塞中（红）/正常（蓝）/完成（绿）"，Linear.app 的依赖视图以最小化节点+清晰箭头为设计原则。RA-05 的节点设计借鉴 Linear 的"干净卡片+语义颜色"原则，避免 PERT 图常见的过度复杂。

**SAFe Program Board（PI 规划墙）**:
SAFe 的 Program Increment Planning 产出物之一是 Program Board：横轴为迭代（Sprint），纵轴为团队，Feature 便签卡贴在对应格中，依赖用线绳在物理看板上连接。数字化版本（如 Miro/Jira）中，依赖线用不同颜色区分内部/跨团队/外部依赖。RA-05 Variant C 直接对应此格式，适合 PI Planning 结束后的管理层汇报和依赖追踪。

---

## 10. Production QA Checklist

- [ ] 所有箭头方向一致（前置 → 后置）
- [ ] 关键路径节点和连线用特殊颜色（橙红）标注
- [ ] 关键路径总工期标注在终点节点旁
- [ ] 每个节点包含：任务名 + Owner + 预计完结日期
- [ ] 阻塞节点已标注原因和等待方
- [ ] 图中无循环依赖（如有则在脚注说明）
- [ ] 节点总数 ≤ 20；超过则拆分为精简视图+详细视图
- [ ] 图例包含：关键路径线/非关键线/阻塞标记说明
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：关键路径是什么、当前哪里阻塞、如何解除
