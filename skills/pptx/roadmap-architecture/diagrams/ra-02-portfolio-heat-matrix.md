# RA-02: 举措组合热力矩阵 — Initiative Portfolio Heat Matrix

_Ref: BCG Growth-Share Matrix | McKinsey 9-Box Portfolio Grid | Gartner Magic Quadrant | RICE/WSJF Prioritization | Sequoia Investment Framework_

---

## 1. Purpose & When to Use

**Definition**: 以两个关键维度（通常为"价值/收益"vs"投入/风险"）构建二维矩阵，将所有举措/产品功能/项目投资作为气泡定位其中，通过象限颜色热力和气泡大小揭示投资组合分布与优先序。

**Use When**:
- 季度 / 年度规划中有 5+ 个候选举措需要做优先级决策
- 向管理层説明"为什么选择这些，而不是那些"
- 进行投资组合再平衡（检查资源是否过度集中某象限）
- RICE 或 WSJF 评分完成后，将评分结果可视化
- 进行 PI Planning 前的 Epic 组合决策
- 预算分配前帮助 CPO / CFO 对齐投资逻辑

**Questions Answered**:
- 哪些举措是明星（高价值低成本），哪些是陷阱（低价值高成本）？
- 我们的资源是否过度集中在某个象限？
- 哪些举措是战略赌注（高价值高风险），如何平衡？
- 举措规模（人力/预算）是否与其战略优先级匹配？

**Primary Audience**: CPO、Product Manager、Strategy Lead、CFO、PMO

---

## 2. Visual Layout Specification

**Structure**: 二维散点/气泡图，嵌入 4 象限热力背景

### Variant A: 价值 vs 投入（标准优先级矩阵）
- X 轴：所需投入（Effort/Cost），从左到右 低→高
- Y 轴：预期价值（Value/Impact），从下到上 低→高
- 象限命名：
  - 右上：Strategic Bets（战略赌注）— `#00CCD7` 区
  - 左上：Quick Wins（快速胜利）— `#53E3EB` 区（最优先执行）
  - 左下：Fill-Ins（填充项）— `#F5F5F5` 区
  - 右下：Money Pits（资源陷阱）— `#FFE8E8` 淡红区
- Best for: 常规季度规划、功能优先级

### Variant B: RICE 评分可视化
- X 轴：Effort（人周）
- Y 轴：RICE Score = (Reach × Impact × Confidence) / Effort
- 气泡大小 = Reach（用户覆盖规模）
- 颜色 = 功能分类（增长/留存/变现/技术债）
- Best for: 产品功能评审会、Backlog 清理

### Variant C: 价值 vs 风险（战略赌注视图）
- X 轴：执行风险（低→高）
- Y 轴：战略价值（低→高）
- 气泡大小 = 投资金额
- 颜色 = 时间窗口（Now/Next/Later）
- Best for: 董事会战略汇报、年度预算对齐

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 矩阵区域: 占 80% 内容区（留足左轴标签和底轴标签空间）
- 左轴 Y 标签: 12% 宽度
- 底轴 X 标签: 8% 高度
- 右下角图例: 固定 120×80px 区域
- 象限标签: 每区角放置 12pt 文字标注象限名

---

## 3. Color Semantics

| 象限 / 元素 | 颜色 | 说明 |
|------------|------|------|
| Quick Wins 象限背景 | `#E8FFFE` (轻青) | 最优先执行 |
| Strategic Bets 象限背景 | `#E3F4FF` (轻蓝) | 高价值高投入，战略赌注 |
| Fill-Ins 象限背景 | `#F5F5F5` (浅灰) | 低优先，按容量填充 |
| Money Pits 象限背景 | `#FFF0F0` (浅红) | 应质疑或取消投资 |
| 气泡 — 增长类举措 | `#00CCD7` | Cloudwise 主色 |
| 气泡 — 留存类举措 | `#53E3EB` | Cloudwise 次色 |
| 气泡 — 效率类举措 | `#44546A` | 深蓝灰 |
| 气泡 — 探索/试验 | `#A5A7AA` | 灰色（不确定性高） |
| 象限分隔线 | `#2F2F2F` 0.75pt | 中心十字轴 |
| 选中/聚焦气泡 | Bold border 2pt `#2F2F2F` | 强调当前 Sprint 聚焦 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 象限标签 | 每象限左上角 | 11pt | SemiBold | `#44546A` |
| 轴标签 | X/Y 轴两端 | 9pt | Regular | `#A5A7AA` |
| 气泡内举措名 | 气泡中心 | 7-9pt | Regular | White 或 `#2F2F2F` |
| 数据标签 | 气泡旁 ID/名称 | 7pt | Regular | `#2F2F2F` |
| 图例标签 | 右下图例 | 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 圆形/椭圆气泡 | 单个举措/项目（大小 = 规模） |
| 背景矩形（4象限） | 热力象限底色（不超过 `#F5F5F5` 深度） |
| 十字轴实线 | X/Y 划分线，`#2F2F2F` 0.75pt |
| 轴端箭头 | 方向性说明（低→高） |
| 虚线圆圈 | 圈定一组相关举措（主题聚类） |
| 加粗边框气泡 | 当前 Sprint / 本季度聚焦举措 |

**Connector Rule**: 不在矩阵中使用连接箭头；如需表示举措间依赖关系，转用 RA-05。

---

## 6. Annotation Rules

- **气泡标签**: 尽量直接写入气泡中心（短名称 ≤ 6 字），长名用 ID + 图例对照表
- **气泡大小说明**: 图例中明确说明"气泡大小 = [人天/预算/用户规模]"
- **RICE 分值**: 鼠标悬停式注释可写在气泡旁小标签（7pt 括号内）如 "(RICE: 82)"
- **移动方向箭头**: 可用轻色箭头表示"战略重心迁移方向"（从一象限到另一象限的虚箭头）
- **脚注**: 标注评分日期 + 评分方法（如 "评分方法: RICE | 截至 2026-Q1"）

---

## 7. Content Density Rules

| Mode | 举措数 | Max per Slide |
|------|--------|---------|
| Minimum | 4 | — |
| Optimal | 8-15 | 15 |
| Maximum | 20 | → 分组后分2图展示 |

**Overflow Strategy**: 超过 20 个举措时，先按战略主题分组，每组用独立图展示，然后用 RA-01 时间轴汇总到综合路线图。

---

## 8. Anti-Patterns

1. **All bubbles same size（气泡大小一致）**: 失去规模信息，退化为普通散点图，无法辅助资源分配决策。
2. **No quadrant names（无象限命名）**: 四块颜色背景没有标签，受众无法理解象限的战略含义。
3. **Subjective scoring（主观打分无据）**: X/Y 轴的分值来自 PM 主观排序，缺乏 RICE/WSJF 支撑 — 管理层质疑时无法解释。
4. **Too many bubbles crowded（气泡堆叠重叠）**: 超过 20 个举措挤在矩阵中，关键信息被遮盖，应先分组。
5. **Missing legend（无图例）**: 气泡颜色/大小没有图例说明，受众无法解读颜色代表什么维度。
6. **Square axis（轴对称设计）**: X 轴和 Y 轴用相同的 0-100 刻度但语义不同，混淆"努力"和"价值"的相对含义。

---

## 9. Industry Reference Patterns

**BCG Growth-Share Matrix（波士顿矩阵）**:
BCG 矩阵是最经典的投资组合分析工具（Bruce Henderson, 1970），以"市场增速"vs"相对市占率"划分 Stars/Cash Cows/Question Marks/Dogs 四象限。产品规划借鉴其象限逻辑，将"市占率"替换为"战略价值/RICE得分"，"市场增速"替换为"用户增长潜力或战略紧迫性"。核心洞察：投资组合必须同时包含 Stars（高投高回报）和 Cash Cows（低投稳现金），不可偏废。

**McKinsey 9-Box Portfolio Grid**:
麦肯锡 9 宫格将维度细化为 3×3（而非 2×2），X 轴为"业务单元竞争强度"（低/中/高），Y 轴为"行业吸引力"（低/中/高）。产品领域的对应应用是"需求紧迫性 × 能力就绪度"的 3×3，将举措进一步细分为"立即行动 / 选择性投资 / 维持 / 退出"四种管理指令。3×3 格式在战略汇报中比 2×2 更显精细，但复杂度也更高。

**WSJF — Weighted Shortest Job First（SAFe）**:
SAFe 框架中 WSJF = (商业价值 + 时间紧迫性 + 风险降低/使能价值) / 任务规模。将 WSJF 分数映射到矩阵后：X 轴 = 任务规模（Story Points 或人天），Y 轴 = 分子之和（商业优先级），气泡大小 = Risk/Opportunity 分值。WSJF 矩阵特别适合已按 SAFe 或 Scrum 运作的团队，因为评分维度已有团队共识。

**Sequoia Capital Portfolio Review**:
红杉资本内部的投资组合评审矩阵以"战略契合度"（与基金主题对齐程度）vs"执行确定性"（团队能力、市场明确度）作为两轴，按"加仓/维持/减仓"管理投资。产品规划引申为：X 轴 = 执行不确定性，Y 轴 = 战略价值，气泡大小 = 当前资源投入，动作标签 = 加速/维持/缩减/停止。这使 CPO 在预算汇报中能清晰表达投资组合调整逻辑。

---

## 10. Production QA Checklist

- [ ] X 轴 / Y 轴标签清晰，两端分别标注"低"/"高"
- [ ] 每个象限有命名标签（如 Quick Wins / Strategic Bets 等）
- [ ] 气泡大小在图例中明确说明代表的维度
- [ ] 颜色编码在图例中说明代表的分类
- [ ] 评分方法注明（RICE/WSJF/主观）+ 评分截止日期
- [ ] 举措数量 ≤ 20；超过则分组展示
- [ ] 无气泡严重重叠导致文字不可读
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：为什么选了 Quick Wins，为什么暂缓 Money Pits
