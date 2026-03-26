# RA-08: 风险与缓解看板 — Risk & Mitigation Kanban

_Ref: NASA Risk Matrix (5×5) | PRINCE2 Risk Register | Agile Risk Board | ISO 31000 Risk Management | PMI PMBOK Risk Management Plan_

---

## 1. Purpose & When to Use

**Definition**: 以看板列（工作流状态）组织风险项，每张风险卡片含概率×影响热力评分，展示风险从"已识别"到"已缓解/已关闭"的全生命周期状态，使规划期风险可见可管。

**Use When**:
- 年度/季度规划启动时，识别并登记规划期主要风险
- Go/No-Go 决策前，内部评审当前已识别风险和缓解状态
- 投资人/Sponsor 汇报，展示风险管控能力
- PI Planning 结束后，登记 PI 阶段的风险项
- 月度/季度风险复审，更新风险状态和缓解进展

**Questions Answered**:
- 当前规划期有哪些已识别风险？
- 每个风险的概率和影响程度如何？
- 各风险处于哪个处置阶段（识别/评估/缓解/关闭）？
- 哪些高概率高影响的风险尚未进入缓解行动？
- 整体风险敞口是否在可接受范围内？

**Primary Audience**: PM、PMO、Risk Owner、Sponsor、审计/合规

---

## 2. Visual Layout Specification

**Structure**: 4 列看板（Identified → Assessed → Mitigating → Closed/Accepted）× 风险卡片行，卡片内含 P×I 热力评分

### Variant A: 标准 4 列看板（适合规划期风险追踪）
- 4 列：已识别 | 评估中 | 缓解中 | 已关闭/已接受
- 每列内风险卡片从上到下按风险等级降序排列（高风险在顶）
- 卡片格式：风险标题 / P×I 热力色块 / Owner / 下次评审日期
- Best for: 月度风险复审会、PMO 看板

### Variant B: 风险热力矩阵 + 待处理清单（适合管理层快照）
- 左半：5×5 风险热力矩阵，风险项以编号标注在矩阵上
- 右半：对应编号的风险简要清单（名称 + 状态 + Owner）
- Best for: 管理层风险汇报、董事会风险简报

### Variant C: 风险演进时间线（适合项目复盘）
- 横轴：时间（季度/月）
- 纵轴：风险等级（高/中/低）
- 风险项以带颜色的点随时间移动，轨迹显示风险升降历程
- Best for: 项目复盘、Risk Retrospective

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 看板区域: 占 80% 内容高度
- 每列宽度: 等分（4列约 22% 各）
- 列标题行: 固定 36px 高度，`#44546A` 填充，白字
- 底部风险等级图例 + 统计: 固定 40px 高度

---

## 3. Color Semantics

风险热力分级（概率 × 影响，5×5 矩阵简化版）：

| 等级 | P×I 范围 | 卡片颜色 | 说明 |
|------|---------|---------|------|
| 极高 Critical | 20-25 | `#FF4444` 红 | 立即行动 |
| 高 High | 12-19 | `#FF9500` 橙 | 优先缓解 |
| 中 Medium | 6-11 | `#FFD700` 黄 | 监控 + 缓解计划 |
| 低 Low | 1-5 | `#A5A7AA` 灰 | 接受或监控 |
| 已缓解 Mitigated | — | `#00BF87` 绿 | 风险已降低到可接受 |
| 已关闭 Closed | — | `#E5E5E5` 浅灰 + ✓ | 风险已消除/已接受 |
| 列标题背景 | — | `#44546A` | 统一看板列头 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 看板列标题 | 列头 | 11pt | SemiBold | White |
| 风险卡标题 | 卡片首行 | 9pt | SemiBold | `#2F2F2F` |
| P×I 分值 | 卡片热力色块内 | 11pt | Bold | White |
| Owner / 日期 | 卡片末行 | 7pt | Regular | `#44546A` |
| 统计摘要 | 底部（总数/状态分布）| 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 看板列矩形 | 风险处理工作流阶段 |
| 圆角卡片 | 单个风险项（颜色=等级） |
| 热力色块（卡片内）| P×I 分值可视化 |
| 向右箭头（列间）| 风险流动方向（可隐含不画） |
| 红圆圈 ⭕ | 本期新增风险标记 |
| 绿圆圈 ✓ | 本期关闭的风险标记 |
| 统计气泡 | 底部各等级数量汇总 |

**Connector Rule**: 看板内的状态流动方向（左→右）隐含，不需要画连接箭头。只有当同一风险跨列移动需要追溯时，才在卡片上标注"来自列 X"。

---

## 6. Annotation Rules

- **P×I 评分**: 卡片内用热力色块标注 "P:3 × I:4 = 12（High）"，或用 3×3 迷你矩阵图标在卡片右上角
- **缓解行动**: 在"缓解中"列的卡片下方标注当前缓解行动（1 行），如 "正在引入备用供应商"
- **新增标记**: 本次评审新增的风险卡片右上角贴 "New" 标签（红色椭圆）
- **升级标记**: 风险等级比上次升高的卡片旁加向上红箭头
- **脚注**: "风险评估日期: YYYY-MM-DD | 评分方法: P(1-5)×I(1-5) | 高风险阈值: P×I ≥ 12"

---

## 7. Content Density Rules

| Mode | 风险总数 | Max per Slide |
|------|---------|---------|
| Minimum | 4 | — |
| Optimal | 8-15 | 15 |
| Maximum | 20 | → 分高/中/低三级看板或按风险类别拆分 |

**Overflow Strategy**: 超过 20 个风险时，主页仅展示 Critical + High 级风险（通常 ≤ 10 个），中低风险放入附录页或单独的"低级风险登记册"。

---

## 8. Anti-Patterns

1. **Risk as issues（风险与问题混淆）**: 将"已发生的问题"放入风险看板——风险是未来可能发生的事件，已发生的是 Issue，应放入问题跟踪，不占用风险看板空间。
2. **All risks medium（风险等级膨胀到中级）**: 为避免升级汇报，所有风险都评为 Medium——失去风险区分度，管理层无法识别需要关注的高风险项。
3. **No owner（无责任人）**: 风险卡没有 Risk Owner——没有人负责的风险必然被遗忘。
4. **Static register（静态登记册）**: 风险看板季度只更新一次，卡片状态从不移动——看板的价值在于状态流动和动态更新，静态登记可以用 Excel 替代。
5. **Missing mitigation action（只有风险无缓解行动）**: 进入"缓解中"列的卡片没有标注实际缓解举措——无法区分"正在行动"和"被动等待结果"。

---

## 9. Industry Reference Patterns

**NASA Risk Matrix（5×5 标准）**:
NASA 在太空项目管理中采用严格的 5×5 风险矩阵（Probability 1-5 × Consequence 1-5），将矩阵单元着色为绿/黄/橙/红四级。NASA Risk Management Handbook 要求每个高风险项必须有详细的 Risk Mitigation Plan（包含：减轻行动/触发条件/应急预案/监控指标）。RA-08 的 P×I 分值体系和缓解计划标准直接源于此实践。

**PRINCE2 Risk Register（企业级风险登记）**:
PRINCE2 的 Risk Register 要求每个风险记录：Risk ID / 类别 / 描述 / 概率 / 影响 / 风险接近度（Proximity，何时可能发生）/ 风险应对策略（Avoid/Reduce/Transfer/Accept）/ Owner / 状态。RA-08 Variant A 的看板卡片字段设计与 PRINCE2 Risk Register 高度对齐，确保风险数据与传统项目管理工具的兼容性。

**Agile Risk Board（SAFe / Scrum 实践）**:
在敏捷语境中，风险管理被轻量化为 ROAM Board（Resolved/Owned/Accepted/Mitigated），是 SAFe PI Planning 结束时的标准产出——团队将识别的风险便签按 ROAM 四类分别贴在白板上，未被 ROAM 处理的风险项变成待处理的行动。RA-08 Variant A 的 4 列看板与 ROAM Board 直接对应（Identified=待 ROAM / Assessed=已 Own / Mitigating=Mitigated / Closed=Resolved+Accepted）。

**ISO 31000 Risk Management Principles**:
ISO 31000 强调风险管理应是"系统的、结构化的、及时的、透明的、融入组织流程的"。其风险处理流程：风险识别 → 风险分析（P×I）→ 风险评价（与风险容忍度对比）→ 风险应对（Avoid/Reduce/Share/Retain）→ 监控与评审。RA-08 的看板列流程与 ISO 31000 的风险处理步骤直接映射，使风险看板图既是汇报工具也是管理工具。

---

## 10. Production QA Checklist

- [ ] 所有看板列清晰标注（已识别/评估中/缓解中/已关闭）
- [ ] 每个风险卡片包含：风险名 + P×I 分值 + Owner + 下次评审日期
- [ ] 风险按等级排序（高→中→低，从上到下）
- [ ] "缓解中"列的每个卡片有具体缓解行动描述
- [ ] 新增风险有 "New" 标记；等级上升风险有上箭头标记
- [ ] P×I 评分方法和高风险阈值在脚注中说明
- [ ] 风险总数 ≤ 20（超过则仅展示 High+ 级）
- [ ] 底部有各等级风险数量统计摘要
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：当前最高风险是什么、谁负责、如何缓解
