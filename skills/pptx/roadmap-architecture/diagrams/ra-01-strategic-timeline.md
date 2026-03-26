# RA-01: 战略路线图时间轴 — Strategic Roadmap Timeline

_Ref: ProductPlan Now/Next/Later | McKinsey Three Horizons | Spotify Squad Roadmap | Aha! Roadmap Standard_

---

## 1. Purpose & When to Use

**Definition**: 以横向时间轴为主轴，按战略主题/产品线分泳道排布举措与里程碑，直观呈现"做什么、何时做、做到什么程度"的全景战略地图。

**Use When**:
- 向 C-suite / 董事会展示年度或跨年产品战略
- 对齐多个团队或产品线的交付节奏
- 在策略沟通中同时呈现"Now/Next/Later"三域
- 季度规划启动会前同步战略共识
- 路线图 OKR 汇报，需要"主题 → 举措 → 里程碑"的完整叙事链

**Questions Answered**:
- 本年/下年我们聚焦哪些战略主题？
- 每个主题下有哪些关键举措，分别落在哪个时间窗口？
- 各举措之间存在哪些时序依赖？
- 何时会有重大里程碑或发布节点？

**Primary Audience**: CPO、CEO、Product Manager、Strategy Lead、投资人

---

## 2. Visual Layout Specification

**Structure**: 横向时间轴 × 纵向泳道（每道 = 一个战略主题/产品线）

### Variant A: Now/Next/Later（适合战略沟通）
- 时间划分为 3 列：Now（当前季度）/ Next（下 1-2 季度）/ Later（未来/未定）
- 每列内举措块自由堆叠，无严格时间刻度
- 重点突出"方向"，隐藏精确交付日期有利于沟通灵活性
- Best for: 管理层路线图对齐、融资/BD 沟通、跨团队共识

### Variant B: 季度滚动路线图（适合交付管理）
- 横轴：Q1 / Q2 / Q3 / Q4（可扩展至 2 年 8 个季度）
- 每个举措块按开始-结束季度横向拉伸为矩形色条
- 里程碑用菱形标注于对应日期刻度
- Best for: 季度规划会、PI Planning、跨职能对齐

### Variant C: 三地平线（适合中长期战略）
- 横轴分为 H1（核心业务拓展，0-12M）/ H2（新兴增长，1-3Y）/ H3（探索未来，3Y+）
- 泳道 = 业务维度（增长/留存/效率/创新）
- Best for: 战略规划年会、向董事会展示长期愿景

**Slide Proportions**:
- Title placeholder: 顶部 12% 高度
- 时间轴刻度行: 固定 28px 高度，紧贴内容区顶部
- 泳道区域: 按主题数量等分（3-6 道最佳）
- 每条泳道左端标题列: 宽度 12-15% 幻灯片宽度，`#44546A` 填充，白色文字
- 最右侧图例条: 固定 48px 宽度（可选，当颜色编码举措分类时必须）

---

## 3. Color Semantics

Cloudwise 色板映射：

| 元素 | 颜色 | 说明 |
|------|------|------|
| 泳道标题背景 | `#44546A` | 深蓝灰，白色文字 |
| 举措色条 — 核心/已确认 | `#00CCD7` | 主色青绿 |
| 举措色条 — 在研/试验 | `#53E3EB` | 次色浅青 |
| 举措色条 — 暂缓/待排期 | `#A5A7AA` | 灰色 |
| 里程碑菱形 | `#2F2F2F` 或 `#00CCD7` | 重要节点深色，达标绿色 |
| Now 区域背景 | 轻度 `#E8FFFE` | 强调"当前"象限 |
| Later 区域背景 | `#F5F5F5` | 弱化"未来"不确定性 |
| 关键路径依赖线 | `#FF6B35` 虚线 | 仅在必要时使用 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 泳道标题 | 左侧标题列 | 10pt | SemiBold | White |
| 时间轴刻度 | Q1/Q2 等标记 | 9pt | Regular | `#2F2F2F` |
| 举措名称 | 色条内文字 | 8-9pt | Regular | White 或 `#2F2F2F` |
| 里程碑标签 | 菱形附近 | 7-8pt | Regular | `#2F2F2F` |
| 图例标签 | Legend 条 | 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 横向圆角矩形色条 | 举措/功能（宽度 = 时间跨度） |
| 菱形 ◇ | 里程碑 / 发布节点 |
| 左侧矩形列 | 泳道标题区（`#44546A` fill） |
| 细实线 | 时间轴刻度分隔线（`#A5A7AA`，0.5pt） |
| 粗虚线箭头 | 举措间的关键依赖（仅当需要时） |
| DONE badge | 已完成举措打勾标记（`#00CCD7` circle + ✓） |

**Connector Rule**: 原则上路线图不显示依赖线（干净）；如需展示依赖，只标示关键路径上的 1-3 条。多依赖场景转用 RA-05。

---

## 6. Annotation Rules

- **里程碑标签**: 菱形下方标注 "事件名 (日期)" 格式，如 "GA Launch (Q2'26)"
- **举措色条内**: 举措名首行 + 负责人简称（如 "搜索重构 · @PM-A"）
- **进度指示**: 完成比例用色条左半段实心填充，未完成段半透明，仅用于"执行状态"视图
- **区域分隔**: Now/Next/Later 区域用竖向细线分隔，顶部用 10pt 区域标签区分
- **脚注**: 幻灯片底部标注 "数据截至: YYYY-MM-DD | 版本: v1.x" （8pt，灰色）

---

## 7. Content Density Rules

| Mode | 泳道数 | 举措数/道 | 总举措数 | Max per Slide |
|------|--------|---------|---------|---------|
| Minimum | 2 | 2 | 4 | — |
| Optimal | 3-5 | 3-5 | 9-25 | 25 |
| Maximum | 6 | 6 | 36 | → split |

**Overflow Strategy**: 按产品线或战略视角分拆为多页。第一页展示总览（核心举措），第二页展示详情展开（具体功能拆解）。

---

## 8. Anti-Patterns

1. **Fake precision（伪精度）**: 在 Now/Next/Later 视图中标注精确到天的日期 — 破坏沟通灵活性，误导执行团队理解为硬承诺。
2. **Missing owner（无归属）**: 举措没有负责人标注 — 路线图变成愿望清单而非可执行计划。
3. **Too many swimlanes（泳道过多）**: 超过 6 条泳道 — 幻灯片失去可读性，应合并或分拆为多图。
4. **All items same priority（无优先级差异化）**: 所有举措用相同颜色和大小 — 无法传递"什么最重要"信息，失去路线图选择价值。
5. **No milestone（无里程碑）**: 只有色条没有节点 — 缺少时间锚点，路线图变成纯方向声明。

---

## 9. Industry Reference Patterns

**ProductPlan / Aha! — Now/Next/Later Standard**:
Now/Next/Later 是 Janna Bastow（ProdPad）推广的轻量路线图格式，被 ProductPlan、Aha! 等主流工具作为默认模板。其核心优势是不绑定精确日期，聚焦战略优先序。在管理层沟通、融资 pitching、跨团队共识场景中效果显著。实践中 "Now" 列通常填充度最高（已有 committed 举措），"Later" 列意图表达长期方向而非承诺。

**McKinsey Three Horizons Framework**:
麦肯锡三地平线模型将创新投资分为：H1（核心业务强化，通常 0-12 个月）/ H2（新兴业务建立，1-3 年）/ H3（转型探索，3 年以上）。路线图视图中以颜色深度区分不确定性（H1 最实、H3 最虚），帮助高管平衡"现在赚钱"与"未来押注"的资源张力。

**Spotify Squad Roadmap**:
Spotify 的路线图以最终用户结果（outcome）为泳道而非功能团队（squad），避免资源视角导致的局部优化。举措按"我们相信……会带来……"（hypothesis format）写入色条，保留执行灵活性。季度结束时路线图不是交付清单对账，而是 outcome 验证。这一模式被称为 "Outcome Roadmap" 或 "Opportunity Roadmap"，与 OST 方法论天然契合。

**Amplitude / Teresa Torres — Continuous Discovery Roadmap**:
Teresa Torres 的持续发现方法论强调路线图应按 OST（机会-方案树）组织：顶层是 desired outcome（如 "提升用户 30 日留存"），中层是 Opportunity（"用户搜索后无法找到想要内容"），底层才是具体 Solution（"语义检索优化"）。路线图只展示 Opportunity 和 Outcome 层，Solution 层由团队自主探索，避免 PM 过度规定实现路径。

---

## 10. Production QA Checklist

- [ ] 时间轴刻度标注清晰（季度或 Now/Next/Later 分区）
- [ ] 每条举措色条包含：举措名 + Owner + 所属战略主题
- [ ] 里程碑菱形标注了日期（或季度）和事件名称
- [ ] 泳道数量 ≤ 6；超过则拆分为多页
- [ ] 举措总数 ≤ 25；超过则使用 RA-02 先筛选优先级
- [ ] 颜色编码含义在图例中说明
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] 所有圆角矩形 corner radius ≤ 6pt
- [ ] 幻灯片底部标注数据截至日期
- [ ] Presenter 能在 3 分钟内用此图讲完：战略重心 → 年度节奏 → 关键里程碑
