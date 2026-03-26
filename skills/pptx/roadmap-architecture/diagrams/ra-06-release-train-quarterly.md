# RA-06: 发布列车/季度计划 — Release Train / Quarterly Plan

_Ref: SAFe Program Increment (PI) Planning | Spotify Release Cadence | Amazon Two-Pizza Team Release Train | LeSS Sprint Planning | Shape Up (Basecamp) Cycles_

---

## 1. Purpose & When to Use

**Definition**: 以时间盒（Quarter / Sprint / PI）为横轴，以团队/产品线为纵轴泳道，展示各团队在每个迭代内计划交付的 Feature/举措，以及关键发布里程碑和依赖连接，服务于季度交付协调和 Release Governance。

**Use When**:
- SAFe PI Planning 前后，汇总各团队的 Feature 交付计划
- 季度规划写报时，向管理层说明"下季度我们会发布什么"
- 多产品线/多 Team 并行迭代，需要协调发布节奏
- Release Manager 进行发布窗口排期管理
- 向 Stakeholder 说明"功能何时上线"的发布路线图

**Questions Answered**:
- 各团队在 Q1/Q2 分别计划交付哪些功能？
- 哪些功能有跨团队依赖，需要协调发布顺序？
- 本季度的 Release 窗口在哪里，哪些功能会包含？
- 当前 Sprint/迭代的完成情况如何？

**Primary Audience**: PM、Engineering Manager、Release Manager、PMO、团队代表

---

## 2. Visual Layout Specification

**Structure**: 时间盒（迭代/季度）为列，团队/产品线为行（泳道），Feature 卡片放置于对应格中

### Variant A: 季度 Feature 计划（适合季度规划汇报）
- 横轴：Q1 月1 / 月2 / 月3 （每月或每两周一列）
- 纵轴：团队泳道（2-6 个团队）
- Feature 卡片：含 Feature 名称 + 状态 + 负责人首字母
- 发布里程碑：横跨所有泳道的竖向深色线 + "Release X.X" 标签
- 依赖连接：用带颜色的弧线连接不同泳道的关联 Feature
- Best for: 季度计划会、季度复盘

### Variant B: SAFe PI Planning Board（适合规模化敏捷）
- 横轴：Sprint 1-6（PI 内的所有 Sprint）
- 纵轴：Squad/Team 泳道
- Feature 便签格式：ID + 名称 + Story Points + 风险标记
- IP Sprint（创新与规划迭代）列：固定最后一列，灰色底
- 跨团队依赖：红色（阻塞）/ 黄色（风险）/ 绿色（已协调）三色弧线
- Best for: PI Planning 输出展示、Scrum of Scrums

### Variant C: 发布列车甘特（适合发布管理）
- 横轴：精确日历日期（月/周）
- 纵轴：发布版本（v2.1 / v2.2 / v3.0）
- 每个版本用色条表示开发周期，末端菱形=发布日期
- Feature 名称列表附在色条内
- Best for: Release Manager 发布协调、上线倒计时管理

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 时间轴列标题行: 固定 32px
- 泳道区域: 等分剩余高度（2-6 道）
- 每条泳道左侧队名列: 12-15% 宽度，`#44546A` 填充
- 顶部/底层发布里程碑标注行: 可选 24px 高度

---

## 3. Color Semantics

| 元素 | 颜色 | 说明 |
|------|------|------|
| 泳道标题背景 | `#44546A` | 深蓝灰，白色队名 |
| Feature 卡片 — 核心 | `#00CCD7` | 本 PI/季度承诺交付 |
| Feature 卡片 — 探索 | `#53E3EB` | 规划中，非硬承诺 |
| Feature 卡片 — 技术债 | `#44546A` 半透明 | 技术债/基础设施 |
| Feature 卡片 — 完成 | `#E5E5E5` + ✓ | 已完成状态 |
| 发布里程碑竖线 | `#2F2F2F` 2pt 实线 | 发布窗口分隔线 |
| 发布里程碑标签 | `#2F2F2F` 矩形框 | Release X.X 版本号 |
| 跨团队依赖 — 已协调 | `#00BF87` 绿色弧线 | 依赖已确认 |
| 跨团队依赖 — 风险 | `#FF9500` 橙色弧线 | 依赖存在风险 |
| 跨团队依赖 — 阻塞 | `#FF4444` 红色弧线 | 当前阻塞状态 |
| IP Sprint / Buffer 列 | `#F5F5F5` 浅灰背景 | 规划/缓冲迭代 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 泳道队名 | 左侧列 | 10pt | SemiBold | White |
| 时间轴列标题 | Sprint/月份 | 9pt | SemiBold | `#2F2F2F` |
| Feature 卡片名称 | 卡片内首行 | 8pt | Regular | White 或 `#2F2F2F` |
| Feature 负责人/ID | 卡片内次行 | 7pt | Regular | `#44546A` |
| 发布里程碑标签 | 竖线顶部 | 10pt | Bold | `#2F2F2F` |
| 依赖弧线标签 | 弧线中部 | 7pt | Regular | 对应状态颜色 |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 圆角矩形卡片 | Feature 交付单元 |
| 竖向深色实线 | 发布里程碑分隔线 |
| 弧线箭头 | 跨泳道/团队依赖 |
| 菱形 ◇ | 上线/发布日期节点 |
| 三角形 △ | 风险标记（贴在卡片右上角） |
| 圆圈内号码 | 依赖编号（对应底部依赖清单） |
| IP Sprint 灰底格 | 规划/缓冲时段 |

**Connector Rule**: 仅跨泳道依赖使用弧线连接；同泳道内顺序依赖通过卡片左右位置隐含表达，不画额外线条。

---

## 6. Annotation Rules

- **发布版本标签**: 竖线顶部标注版本号 + 计划日期，如 "v2.5 | 2026-06-30"
- **阻塞标注**: 阻塞弧线旁注明阻塞原因（1 行内），如 "等待 @Team-Infra 完成 K8s 升级"
- **Feature 状态**: 卡片右上角三角=风险，圆圈✓=完成，无标记=进行中
- **容量警告**: 当某个泳道的 Story Point 总和超过团队容量时，用红色虚线框圈出超载区域
- **脚注**: "PI X | 规划日期: YYYY-MM-DD | Story Points: 已规划 XXX / 团队容量 XXX"

---

## 7. Content Density Rules

| Mode | 团队泳道数 | Sprint/月列数 | Feature/泳道 | Max per Slide |
|------|---------|------------|------------|---------|
| Minimum | 2 | 3 | 2 | — |
| Optimal | 3-5 | 4-6 | 3-5 | 25 Features |
| Maximum | 6 | 6 | 6 | → split by release |

**Overflow Strategy**: Feature 数量 > 30 时，按发布版本分页更清晰（一页一个 Release Train）。

---

## 8. Anti-Patterns

1. **Feature shopping list（功能购物清单）**: 卡片内容仅有功能名，没有负责人也没有 Story Points — 无法作为交付承诺基础。
2. **No release marker（无发布里程碑）**: 季度计划没有明确的发布节点 — 不知道功能何时能到用户手中，失去发布管理价值。
3. **All dependencies red（全部标红）**: 所有依赖都标为阻塞 — 失去优先级判断；阻塞应仅用于当前真正阻塞状态，而非"可能风险"。
4. **Missing IP Sprint（缺少缓冲迭代）**: SAFe PI Planning 中不留 IP Sprint — 实践中迭代末期必须有验证/偿还技术债的缓冲，否则 PI 末期必然超载。
5. **Team swimlane = org chart（泳道=组织架构）**: 泳道按组织结构（前端组/后端组）划分而非按价值流/Product Area — 导致 Feature 总是跨泳道割裂，无法完整交付。

---

## 9. Industry Reference Patterns

**SAFe Program Increment Planning（规模化敏捷 PI 规划）**:
SAFe 的 PI 是一个固定时长（通常 10-12 周 = 5个 Sprint + 1个 IP Sprint）的规划/交付周期。PI Planning 是一个大型仪式（2天），所有 ART（Agile Release Train）成员聚集，协调 Feature 到 Sprint 的分配，识别跨团队依赖（用实物便签和红线表示）。产出的 Program Board 是 RA-06 Variant B 的直接原型——横轴为 Sprint，纵轴为 Team，红/黄/绿线弦表示依赖状态。SAFe 的 ART Velocity 和 Predictability 指标从 PI 计划数据中直接计算。

**Spotify Release Cadence（Spotify Squad 发布节奏）**:
Spotify 的 Squad 采用持续部署（Continuous Delivery）+ Feature Flags 的组合，"发布列车"概念体现在：每周四是全公司的固定 Release Window，所有 Squad 允许上线的 Feature 在此窗口合并。RA-06 的"发布里程碑竖线"直接对应这个 Release Window 概念。Spotify 在月度规划中用 "Opportunity Backlog" 代替 "Feature Backlog"，强调 "解决了什么用户问题" 而非 "上了什么功能"。

**Amazon Two-Pizza Team Release Train**:
Amazon 的 "Two-Pizza Team" 原则（团队人数不超过两张披萨能喂饱）推导出每个服务/产品由一个小团队完全负责（Full Ownership）。Amazon 的 Release Process 要求每个 PR 通过 One-Click Deployment 进入 Release Train，配合严格的 Rollback SLA（1 分钟内可回滚）。在大型项目的季度计划中，Amazon 使用"Working Backwards"文档 + Release Checklist 而非甘特图；RA-06 的发布版本色条和 Release Notes 结构借鉴了 Amazon 的 Release Package 概念。

**Shape Up（Basecamp 37signals）— Cycles & Cool-Down**:
Shape Up 提出"每 6 周一个 Cycle + 2 周 Cool-Down"的固定节奏，与 SAFe PI 结构类似但更精简。Cycle 内团队只做一件 Shaped Work（已定义范围的项目），Cool-Down 用于修复 Bug、探索新想法、不做新 Feature 承诺。RA-06 Variant A 中的"IP Sprint / Buffer 列"与 Cool-Down 直接对应。Shape Up 强调"Appetite（时间盒）决定交付范围"（而非需求决定时间），这与 PI 的固定迭代工期哲学一致。

---

## 10. Production QA Checklist

- [ ] 时间轴列标题清晰（Sprint 编号或月份）
- [ ] 每个 Feature 卡片包含：Feature 名 + Owner + 状态
- [ ] 所有发布里程碑有版本号 + 计划日期
- [ ] 跨团队依赖用颜色区分（绿/橙/红），阻塞线有简短原因标注
- [ ] 团队泳道数 ≤ 6（超过则分页）
- [ ] Feature 总数 ≤ 30（超过则按 Release 分页）
- [ ] IP Sprint / Buffer 列已标注（如适用）
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：Q1 发什么、谁负责、依赖在哪里
