# RA-03: KPI里程碑阶梯 — KPI Milestone Ladder

_Ref: OKR Staircase / Result Ladder | Google OKR Progress Framework | Basecamp Hill Chart | McKinsey Performance Curve | WaterFall KPI Decomposition_

---

## 1. Purpose & When to Use

**Definition**: 以阶梯/瀑布状布局展示 KPI 从基准值到目标值、再到拉伸目标的逐阶递进，并将里程碑节点标注在阶梯踏步上，呈现"结果目标如何分阶段实现"的清晰路径。

**Use When**:
- OKR 季度汇报，展示 Key Result 的当前进展与剩余差距
- 年度战略规划，拆解年度 KPI 为季度/月度里程碑
- 管理层结果追踪会，对比"计划轨迹"vs"实际轨迹"
- 激励沟通，直观传递"再走几步就到目标"的可达感
- 产品 GA 后的增长目标拆解（MAU/Revenue/Retention 阶梯）

**Questions Answered**:
- 我们的 KPI 目标是什么，当前处于哪个阶段？
- 每个里程碑需要达到什么数值才算按计划推进？
- 我们是否符合预期节奏，还是已经落后？
- 达成拉伸目标（Stretch）需要做到什么？

**Primary Audience**: Executive、CPO、PMO、OKR Owner、Business Analyst

---

## 2. Visual Layout Specification

**Structure**: 从左到右上升的阶梯，每个踏步代表一个时间节点（季度或月份），踏步高度 = KPI 增量，宽度相等，踏步上标注里程碑事件与目标值。

### Variant A: 单 KPI 阶梯（适合单一核心指标）
- 阶梯级数：4-8 级（每季度或每两月一级）
- 每级踏步：左侧标注时间（Q1/Q2...），踏步顶部标注目标值，踏步上方可注里程碑名称
- 已完成踏步：`#00CCD7` 填充；未完成踏步：`#E5E5E5` 填充
- 当前位置：用闪光/星形标注当前实际值（RAG 颜色）
- Best for: 单 KPI OKR 汇报、月度经营会

### Variant B: 多 KPI 对比阶梯（适合 OKR/多指标概览）
- 2-4 个 KPI 并排展示，每个 KPI 独立阶梯
- 每个阶梯底部标注 KPI 名称和最终目标
- 当前进度以填充色区分（绿=On Track，橙=At Risk，红=Behind）
- Best for: 季度 OKR Review、管理层指标看板

### Variant C: 基准-目标-拉伸三段式（适合激励目标设定）
- 单条横向增长曲线，三段区域用颜色渐变区分：
  - 基准段（Baseline → Target）：`#53E3EB` 填充
  - 目标段（Target → Stretch）：`#00CCD7` 填充
  - 拉伸段（Stretch+）：`#44546A` 填充，星形标注
- 时间刻度为 X 轴，KPI 值为 Y 轴
- Best for: 年度目标设定会、激励设计沟通

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 阶梯图区域: 70% 高度，75% 宽度（居中）
- 左侧 KPI 名称条: 10% 宽度（仅 Variant B）
- 底部时间轴: 固定 28px
- 右侧当前进度标注: 10% 宽度（实际值 vs 计划值差异）

---

## 3. Color Semantics

| 状态 / 元素 | 颜色 | 说明 |
|------------|------|------|
| 已达成踏步 | `#00CCD7` | 按期或超额完成 |
| 当期进行中踏步 | `#53E3EB` | 当前季度 |
| 未来踏步（计划值） | `#E5E5E5` 浅灰 | 尚未到来 |
| On Track 状态 | `#00BF87` 绿色标记 | 实际值 ≥ 计划值 |
| At Risk 状态 | `#FF9500` 橙色标记 | 实际值 75-99% 计划值 |
| Behind 状态 | `#FF4444` 红色标记 | 实际值 < 75% 计划值 |
| 拉伸目标 Stretch | `#44546A` + 星形 | 超越目标的挑战值 |
| 当前实际值指针 | `#2F2F2F` 三角/箭头 | 当前实际位置标记 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| KPI 名称 | 阶梯旁/底部 | 12pt | SemiBold | `#2F2F2F` |
| 踏步目标值 | 踏步顶部 | 14pt | Bold | White 或 `#2F2F2F` |
| 时间标签 | 每级左/底 | 9pt | Regular | `#A5A7AA` |
| 里程碑事件名 | 踏步上短注 | 8pt | Regular | `#2F2F2F` |
| 实际值标注 | 当前位置旁 | 11pt | Bold | On Track 色码 |
| 差距标注 | 箭头旁 "+12%" | 9pt | Regular | `#2F2F2F` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 阶梯矩形（上升级数） | 每个时间节点的 KPI 阶段目标 |
| 菱形 ◇ / 星形 ★ | 关键里程碑 / 拉伸目标节点 |
| 三角形指针 ▲ | 当前实际值指示器 |
| 竖向虚线 | 当前时间线（"今天"分隔线） |
| 折线/曲线 | 实际值增长轨迹（叠加在阶梯上） |
| 双线箭头 ↕ | 目标差距/Gap 标注 |

**Connector Rule**: 允许用折线叠加在阶梯上显示"实际进度曲线"（Plan vs Actual），这是 KPI 阶梯图的核心价值叠加层。

---

## 6. Annotation Rules

- **里程碑标注**: 踏步顶端或旁边注标事件名，如 "Beta Launch" / "覆盖 100 城市"
- **Gap 标注**: 在当前实际值与计划值之间用双向箭头标注差距百分比
- **负责人**: 每个 KPI 旁标注 Owner（如 "@Growth PM"）
- **Review 节点**: 季度结束的踏步用粗边框标注（"Q1 Review"）
- **脚注**: 数据来源 + 截至日期（"数据来源: BI Dashboard | 截至 2026-03-25"）

---

## 7. Content Density Rules

| Mode | KPI 数 | 阶梯级数 | Max per Slide |
|------|--------|---------|---------|
| Single KPI | 1 | 4-8 | — |
| Multi KPI | 2-4 | 4-6/KPI | — |
| Maximum | 4 | 4 | → 超过则分 KPI 单独成页 |

**Overflow Strategy**: 超过 4 个 KPI 时，按层级拆分：第一页展示 OKR Level（3-4 个 Objective 的核心 KR），后续页分别展示每个 Objective 下的 KR 拆解阶梯。

---

## 8. Anti-Patterns

1. **Linear bars disguised as KPI ladder（拔高的柱状图）**: 将普通 Excel 柱形图称为"KPI 阶梯"，失去里程碑-事件-时序节点的叙事结构。
2. **No baseline（无基准值）**: 阶梯从 0 开始而非从真实历史基准出发，导致目标增长倍数失真。
3. **Missing stretch target（无拉伸目标）**: 只有"目标值"没有"Stretch目标"，失去激励层次，无法传递"做到 100% 及格，做到 120% 优秀"的认知结构。
4. **No Plan vs Actual overlay（无计划vs实际对比）**: KPI 阶梯只展示计划，没有实际值对比，变成愿望声明而非绩效追踪。
5. **Too many KPIs on one slide（单页 KPI 过多）**: 超过 5 个 KPI 在同一阶梯图中，每个阶梯太窄，数值不可读。

---

## 9. Industry Reference Patterns

**Google OKR Progress Grading（Googler's 0-1 Scale）**:
Google 的 OKR 体系中，Key Result 的进度评分遵循 0-1 连续量表：0.0-0.3 为失败，0.4-0.6 为一般，0.7 为理想（Google 认为 0.7 说明目标设定适当），1.0 意味着目标过于保守。KPI 阶梯图将这一进度可视化为阶梯踏步，每级对应 0.1 进度增量，配合颜色（红/橙/绿）传达当前评分区间。

**OKR Staircase / Waterfall KPI Decomposition（年度拆季）**:
成熟的 OKR 实践中，年度目标按"季度平均节奏"或"前慢后快"（如 Q1 20%/Q2 25%/Q3 25%/Q4 30%）分解为季度 KR。阶梯图可视化这种分解：踏步高度体现增量，踏步间距暗示增长节奏（均等踏步 = 线性增长，前低后高踏步 = 阶段积累型增长）。这种分解方式帮助团队在 Q1 就知道"是否在正确轨道上"。

**Basecamp Hill Chart（爬坡图）**:
Basecamp 提出的 Hill Chart 将任务状态分为两阶段：上坡（Problem Solving，需要探索和解决不确定性）和下坡（Execution，已明确方向稳步交付）。KPI 阶梯图借鉴这个思路，将里程碑分为"探索型"（上坡，较平阶梯）和"执行型"（下坡，较陡阶梯），视觉呈现工作性质的差异。

**McKinsey Performance Curve（增长 S 曲线）**:
麦肯锡在绩效叙事中常使用 S 曲线展示增长轨迹：起步缓慢（种子期）→ 加速（扩张期）→ 放缓（成熟期）。KPI 阶梯图可在阶梯顶部叠加 S 型增长曲线，标注"当前所处增长阶段"，帮助管理层理解增速变化背后的结构性原因，而非将增速下降简单视为执行问题。

---

## 10. Production QA Checklist

- [ ] 基准值（起点）已标注，不从零开始
- [ ] 每个踏步标注：时间节点 + 目标值 + 里程碑事件
- [ ] 拉伸目标（Stretch）已标注且视觉上有区分（星形/深色）
- [ ] 当前实际值已用指针标注（含 On Track / At Risk / Behind 颜色）
- [ ] KPI 数量 ≤ 4（单页）
- [ ] 阶梯级数 ≤ 8（超过则按半年拆分）
- [ ] 数据来源 + 截至日期标注于脚注
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：我们的 KPI 目标是什么、当前在哪里、差距多大、下一步做什么
