# RA-07: 资源-优先级矩阵 — Resource-Priority Matrix

_Ref: Eisenhower Matrix (Urgent/Important) | McKinsey Resource Allocation Matrix | RICE Effort Allocation | FTE Portfolio Allocation | OKR Resource Commitment Framework_

---

## 1. Purpose & When to Use

**Definition**: 以"战略优先级"（Y 轴）× "所需资源投入"（X 轴）构建的 2×2 象限图，将举措/项目/团队目标定位为气泡，通过象限位置揭示资源分配的合理性，识别"高优先级但资源不足"和"低优先级却占用大量资源"两种典型失衡情况。

**Use When**:
- 年度/季度预算分配前，对齐资源投入与战略优先级
- 向 CPO/CFO 说明当前资源分配是否支撑战略重心
- 团队扩编申请前，说明"投入更多资源到 X 的战略依据"
- OKR 检视中，评估 Key Result 的资源保障充分性
- Portfolio 再平衡讨论，找出可减少投入的低优先级举措

**Questions Answered**:
- 高优先级举措是否获得了足够的资源？
- 哪些举措占用了大量资源但战略优先级偏低？
- 资源分配结构是否与战略宣言一致？
- 如果削减预算 20%，应该首先压缩哪些举措？

**Primary Audience**: CPO、CFO、PMO、Budget Owner、HR Partner（人力规划）

---

## 2. Visual Layout Specification

**Structure**: 标准 2×2 象限图，气泡大小 = 当前实际资源投入（FTE 或预算）

### Variant A: 优先级 × 资源投入（标准版）
- X 轴：所需资源投入（低→高），单位可为人月/季度 FTE/预算
- Y 轴：战略优先级（低→高），来自 WSJF 或管理层打分
- 气泡大小：当前实际分配资源（FTE 数量）
- 象限含义：
  - 左上（高优先 × 低投入）：Under-invested — 需要加仓 ↑
  - 右上（高优先 × 高投入）：Justified Investment — 维持 ✓
  - 左下（低优先 × 低投入）：Low Overhead — 监控 👁
  - 右下（低优先 × 高投入）：Over-invested — 需要减仓 ↓
- Best for: 资源再平衡决策、CFO budget review

### Variant B: 优先级 × 时间紧迫性（艾森豪威尔变体）
- X 轴：完成紧迫度（Not Urgent → Urgent）
- Y 轴：战略重要性（Low → High）
- 象限对应行动指令：Do / Schedule / Delegate / Eliminate
- Best for: 团队工作排期、PM 个人优先级管理

### Variant C: ROI 对比视图（适合预算汇报）
- X 轴：投入（Cost，预算 K 元或 FTE）
- Y 轴：预期回报（ROI 倍数或增量 KPI）
- 气泡大小 = 时间周期（短期/中期/长期）
- 颜色 = 确信度（High/Med/Low）
- Best for: 董事会或 CFO 投资回报论证

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 矩阵图区域: 80% 内容区（留出轴标签空间）
- X 轴标签区: 8% 高度（底部）
- Y 轴标签区: 10% 宽度（左侧）
- 右下角行动指令图例: 固定 100×80px

---

## 3. Color Semantics

| 象限 / 状态 | 颜色 | 行动 |
|------------|------|------|
| 高优× 低投（Under-invested）| `#E8FFFE` 背景 + 上箭头标签 | 加仓 |
| 高优× 高投（Justified）| `#E3F4FF` 背景 | 维持 |
| 低优× 低投（Low Overhead）| `#F5F5F5` 背景 | 监控 |
| 低优× 高投（Over-invested）| `#FFF0F0` 背景 + 下箭头标签 | 减仓 |
| 气泡 — 增长举措 | `#00CCD7` | 核心增长类 |
| 气泡 — 效率举措 | `#44546A` | 内部效率/降本 |
| 气泡 — 探索举措 | `#53E3EB` | 创新探索 |
| 气泡 — 维护举措 | `#A5A7AA` | 存量维护 |
| 中心轴线 | `#2F2F2F` 0.75pt | X/Y 中心分隔线 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 象限标签 | 每象限左上角 | 11pt | SemiBold | `#44546A` |
| 行动指令标签 | 象限右下角 | 9pt | Bold | 对应象限颜色的深色版 |
| 轴标签（两端）| X/Y 轴端注 | 9pt | Regular | `#A5A7AA` |
| 气泡内举措名 | 气泡中心 | 7-9pt | Regular | White 或 `#2F2F2F` |
| 气泡大小图例 | 右下图例 | 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 圆形/椭圆气泡 | 举措（大小 = 资源投入量） |
| 四象限背景矩形 | 资源分配健康度区域 |
| 中心十字轴实线 | X/Y 分隔 |
| 带文字箭头标签 | 行动建议（加仓↑ / 减仓↓） |
| 虚线圆圈 | 资源战略调整目标位置（Current→Target 迁移） |
| Delta 箭头 | 从当前位置指向建议调整后的目标位置 |

**Connector Rule**: 不在举措气泡之间使用连接线。如需表示举措间依赖，转用 RA-05。

---

## 6. Annotation Rules

- **气泡标签**: 优先在气泡内标注举措短名；若气泡过小，用数字 ID + 侧边图例对照
- **气泡大小**: 图例中说明气泡大小代表的量纲（"气泡面积 ∝ 当前 FTE 数" 或 "气泡面积 ∝ 季度预算 K 元"）
- **调整方向**: 用虚线箭头从当前气泡位置指向建议移动方向（同一个气泡的原位 + 目标位）
- **总资源标注**: 幻灯片右上角或脚注标注"总 FTE: XX 人 | 总预算: XXX K"
- **脚注**: 打分方法 + 资源数据截至日期 + 数据来源

---

## 7. Content Density Rules

| Mode | 举措数 | Max per Slide |
|------|--------|---------|
| Minimum | 4 | — |
| Optimal | 6-12 | 12 |
| Maximum | 16 | → 分组展示 |

**Overflow Strategy**: 超过 16 个举措时，分按产品线/事业群分组为多页矩阵，在汇总页用总气泡（每个战略主题的合并气泡）展示全局资源分配结构。

---

## 8. Anti-Patterns

1. **Arbitrary priority scoring（主观优先级无根据）**: Y 轴"战略重要性"来自于 PM 个人判断，没有 WSJF 或管理层对齐数据支撑 — 失去说服力，在预算需要时无法说服 CFO。
2. **Same-size bubbles（气泡大小一致）**: 所有举措气泡用相同大小 — 失去"资源规模"这一最重要的信息维度，退化为简单散点图。
3. **No action implication（无行动暗示）**: 矩阵只显示当前状态，没有"加仓/减仓"行动建议 — 矩阵图的价值在于触发决策，不只是现状展示。
4. **Single-dimension drift（单维度偏倚）**: 所有举措都挤在"高优先 × 高投入"象限 — 通常是评分膨胀（每个 PM 都给自己的项目打高分），应引入强制排名（rank-ordered）机制。
5. **Missing total resources（无总量标注）**: 不标注总 FTE / 总预算基数 — 气泡大小无法被读者定量理解，只能比较相对大小。

---

## 9. Industry Reference Patterns

**Eisenhower Matrix（艾森豪威尔矩阵）**:
德怀特·艾森豪威尔的时间管理名言 "What is important is seldom urgent and what is urgent is seldom important" 催生了 Urgent × Important 四象限。Stephen Covey 在《高效能人士的七个习惯》中将其系统化。产品规划中将"紧迫性"替换为"资源消耗（Effort）"，将"重要性"替换为"战略优先级（Strategic Priority）"，得到资源分配矩阵。核心原则：大量时间/资源应集中在第二象限（高重要/低紧迫），而非被第一象限（高重要/高紧迫）的救火模式占据。

**McKinsey Quarterly Resource Allocation Review（资源动态再配置）**:
McKinsey 研究（《Strategy Beyond the Hockey Stick》）显示：战略成功率与资源动态再配置能力强相关。顶尖公司每年再配置约 20% 资源（从低增长业务流向高增长业务），而资源再配置不足的公司战略失败率是其 3 倍。RA-07 的"减仓→加仓"分析直接服务于这一动态再配置决策。McKinsey 建议每季度至少做一次资源-优先级对齐检查（而非年度一次）。

**OKR Resource Linkage（OKR 与资源承诺挂钩）**:
Google 的高级 OKR 实践要求每个 Objective 在设立时同步声明"资源承诺（Resource Commitment）"：XX 名全职人员 + XX% 的时间专注于此目标。RA-07 将这一承诺可视化，使 CPO 和团队能检查"OKR 的优先级声明"与"实际 FTE 分配"是否匹配。Google Ventures 在 OKR coaching 中强调：只有"有资源承诺的 OKR"才是真正的优先级，其余只是愿望。

**Staffing Ratio Analysis（人力比例分析，Amazon/Meta Practice）**:
大型科技公司（Amazon/Meta）在年度 Planning 中会计算各产品线的 Engineering:PM:Design:Data Science 人力比例，并与行业基准对比。投资过度在某些类别（如过多 PM vs Engineering）会导致协调成本指数级上升。RA-07 的气泡大小可以细化为"职能角色分布"饼状（在气泡内用迷你饼图表示），辅助人力结构分析。

---

## 10. Production QA Checklist

- [ ] X 轴 / Y 轴标签清晰，含量纲说明（FTE/预算/WSJF 分）
- [ ] 每个象限有命名（Under-invested / Justified / Low Overhead / Over-invested）
- [ ] 气泡大小图例明确说明量纲（人月或预算 K 元）
- [ ] 颜色图例说明举措分类（增长/效率/探索/维护）
- [ ] 总资源基数标注于脚注或右上角
- [ ] 打分方法 + 数据截至日期有脚注
- [ ] 举措数量 ≤ 16（超过则分组）
- [ ] 每个象限至少有简短的行动建议标注
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：哪里资源错配、建议如何调整
