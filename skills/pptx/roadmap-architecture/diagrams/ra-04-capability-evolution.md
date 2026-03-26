# RA-04: 能力演进路线图 — Capability Evolution Roadmap

_Ref: TOGAF Capability-Based Planning | Gartner Capability Maturity Model | Microsoft Azure Capability Roadmap | SAFe Evolving Architecture | Wardley Mapping_

---

## 1. Purpose & When to Use

**Definition**: 以时间轴（X 轴）× 能力维度（Y 轴/泳道）构建二维图，展示每项业务/技术能力从当前成熟度跨多个时间段演进到目标状态的路径，揭示"何时哪项能力需要被建立、加强或替换"。

**Use When**:
- 制定 3-5 年数字化转型能力建设计划
- 技术架构升级规划，展示"从 As-Is 到 To-Be"的能力跃升时序
- 组织能力规划（人才技能栈、组织敏捷度演进）
- 平台/产品中台能力路线图，说明"什么时候具备什么能力"
- 与 BA-01 Capability Map × 时间轴结合，从静态视图到动态演进视图

**Questions Answered**:
- 当前哪些能力已经成熟，哪些仍处于建设初期？
- 每项能力何时会达到下一个成熟度等级？
- 多项能力的演进是否有合理的先后依赖顺序？
- 在某个时间节点，我们的整体能力栈处于什么水平？

**Primary Audience**: CPO、CTO、企业架构师、Strategy Lead、组织发展 Lead

---

## 2. Visual Layout Specification

**Structure**: 横向时间轴 × 纵向能力泳道，每条泳道显示能力成熟度随时间的"台阶跃升"

### Variant A: 成熟度台阶型（适合能力建设规划）
- 泳道 = 每项核心能力（3-8 项）
- 每条泳道内，色块从左到右增宽，代表成熟度提升
- 5 级成熟度用颜色深度标注：L1（浅灰）→ L5（Cloudwise 深蓝/青）
- 成熟度跃升处用竖向虚线+标签标注触发事件（如 "引入 AI 能力后"）
- Best for: 数字化转型规划、能力成熟度评估后的路线图

### Variant B: Wardley Map 演进横轴（适合战略技术选型）
- X 轴：Genesis（探索）→ Custom（定制）→ Product（产品化）→ Commodity（商品化）
- Y 轴：价值链位置（从用户可见性高→低）
- 举措/技术用圆点标注当前位置，箭头指向目标位置
- Best for: 技术策略讨论、Build vs Buy vs Partner 决策

### Variant C: 二维热图 × 时间矩阵（适合多能力快照对比）
- 行 = 能力项，列 = 时间节点（当前/12M/24M/36M）
- 每个单元格用成熟度颜色填充（热图格式）
- Best for: 董事会快速概览、能力建设里程碑墙

**Slide Proportions**:
- Title placeholder: 顶部 12%
- 左侧能力名称列: 16% 宽度，`#44546A` 填充，白字
- 时间轴刻度行: 固定 28px 高度（顶部）
- 泳道区域: 等分剩余空间（3-8 道）
- 底部图例: 固定 48px 高度，说明成熟度级别颜色

---

## 3. Color Semantics

成熟度分级颜色（与 BA-01 能力地图保持一致）：

| 成熟度 | 级别 | 填充色 | 说明 |
|--------|------|--------|------|
| L1 未建设 | 初始 | `#FFFFFF` + 虚线框 | 尚未投入建设 |
| L2 初级 | Ad-hoc | `#E5E5E5` 浅灰 | 有探索但不稳定 |
| L3 发展中 | Developing | `#53E3EB` 浅青 | 有系统投入，能力在建 |
| L4 受管理 | Managed | `#00CCD7` 主青 | 稳定运行，可量化 |
| L5 优化级 | Optimized | `#44546A` 深蓝灰 | 行业领先，持续优化 |
| 需投资 | Target Focus | Bold border `#00CCD7` 3pt | 本周期重点建设 |
| 建设触发事件 | Trigger | 竖向虚线 `#A5A7AA` | 能力跃升依赖的前置条件 |

---

## 4. Typography Hierarchy

| Level | Usage | Size | Weight | Color |
|-------|-------|------|--------|-------|
| Slide Title | Placeholder idx=0 | 28pt | Bold | `#2F2F2F` |
| Slide Subtitle | Placeholder idx=1 | 14pt | Regular | `#44546A` |
| 能力名称 | 左侧列 | 10pt | SemiBold | White |
| 时间轴刻度 | Q1/Q2 等 | 9pt | Regular | `#2F2F2F` |
| 成熟度级别 | 色块内 | 8pt | Regular | White 或 `#2F2F2F` |
| 触发事件标签 | 虚线旁 | 7pt | Regular | `#A5A7AA` |
| 图例标签 | 底部 | 8pt | Regular | `#A5A7AA` |

---

## 5. Shape & Connector Vocabulary

| Shape | Meaning |
|-------|---------|
| 填充色矩形（泳道内） | 能力成熟度色块（颜色=级别，宽度=持续时段） |
| 阶梯边缘 | 成熟度等级跃升点 |
| 竖向虚线 | 关键触发事件（前置依赖/里程碑） |
| 圆形节点 | 能力关键建设完成点 |
| 向右箭头 | 能力演进方向（Wardley 变体时使用） |
| 加粗边框矩形 | 本周期重点投资能力 |

**Connector Rule**: 不同泳道间的依赖用细实线箭头连接（从一个泳道的节点到另一个泳道的触发点），仅标注关键依赖（≤ 5 条）。

---

## 6. Annotation Rules

- **触发事件**: 竖向虚线上方标注触发条件，如 "完成数据平台建设后" / "2026 Q3 引入 AI 引擎"
- **里程碑节点**: 圆形节点内标注 ID，图旁标注里程碑名称
- **能力当前状态**: 用"★ 已在建"或"○ 计划中"区分已启动和未启动
- **差距高亮**: 当前成熟度与目标成熟度之间的"颜色落差区域"用浅色虚线框圈出
- **脚注**: "能力分级标准参考：[TOGAF/CMM/内部标准] | 评估日期: YYYY-MM"

---

## 7. Content Density Rules

| Mode | 能力项数 | 时间跨度 | Max per Slide |
|------|---------|---------|---------|
| Minimum | 3 | 4 个季度 | — |
| Optimal | 5-8 | 4-8 个季度 | — |
| Maximum | 10 | 8 个季度 | → split by domain |

**Overflow Strategy**: 超过 10 项能力按业务域分拆为 2 页。第一页：核心差异化能力。第二页：支撑/通用能力。两页共用相同时间轴刻度和成熟度图例，便于对比。

---

## 8. Anti-Patterns

1. **Vague capability names（能力命名模糊）**: 使用"AI 能力"/"数字化能力"等泛指词 — 无法作为建设目标展开行动，应精确到"实时个性化推荐引擎"/"低代码配置平台"等。
2. **All L3 to L5 in Q1（虚假跃升）**: 所有能力在当前季度都标注为"即将升到 L5" — 失去优先级信息，破坏可信度。
3. **Missing triggers（无触发条件）**: 能力在某个季度突然跃升一级，但没有说明是什么条件/事件触发的 — 路线图变成"愿望时间表"。
4. **Mixing capability and feature（能力与功能混淆）**: 将具体功能（"支持 SSO 登录"）与能力（"身份与访问管理"）放在同一层级 — 能力是持续的组织能力，特性是一次性的交付产物。
5. **Too many swimlanes（泳道过密）**: 超过 12 条泳道在同一页，每条高度不足 12px，无法书写文字，失去可读性。

---

## 9. Industry Reference Patterns

**TOGAF Capability-Based Planning（能力驱动规划）**:
TOGAF ADM Phase B 的能力驱动规划方法要求：先评估当前能力成熟度（As-Is），定义目标能力状态（To-Be），再识别差距并制定分阶段过渡计划（Migration Plan）。能力演进路线图是将 TOGAF Migration Plan 可视化的最佳格式，将抽象的"能力差距分析"转化为管理层能理解的"建设时间表"。实践中每个季度的能力成熟度评估结果作为数据源定期刷新路线图。

**Gartner Maturity Model Roadmap**:
Gartner 的多个能力成熟度评估模型（Data Governance/Analytics/AI 成熟度等）均采用 5 级标准（Initial → Repeatable → Defined → Managed → Optimizing），与能力演进路线图的 L1-L5 等级直接对应。Gartner 的典型汇报格式是一张"当前级别热图"加上一张"目标级别热图"，而能力演进路线图将两者合并为时间维度连续视图，信息密度更高。

**Microsoft Azure Adoption Framework — Capability Roadmap**:
微软 Cloud Adoption Framework 的"Ready"阶段包含一张"Cloud Capability Readiness Roadmap"，按基础设施/安全/治理/运维/人才 5 个能力维度，展示组织从 On-Premises 到 Cloud-Native 的逐阶段能力建设计划。其可视化特征：以 Horizon（时间段）为列，能力域为行，成熟度用颜色填充，"下一步建设"用黑色边框高亮——完全契合 RA-04 Variant A 格式。

**Wardley Mapping（价值链演进分析）**:
Simon Wardley 提出的 Wardley Map 将业务组件按"用户可见性"（Y 轴）和"演进阶段"（X 轴：Genesis→Custom→Product→Commodity）二维定位，通过箭头显示每个组件的演进方向和速度。RA-04 Variant B 直接借鉴此格式，用于技术选型决策（什么时候从"自研"迁移到"采购商品化服务"）。Wardley Map 的核心洞察：不同演进阶段的组件需要不同的管理策略（探索/建设/产品化/外包），路线图应体现这种差异性投资逻辑。

---

## 10. Production QA Checklist

- [ ] 时间轴跨度与规划周期匹配（季度/半年）
- [ ] 每项能力的当前成熟度（As-Is）已标注
- [ ] 每项能力的目标成熟度（To-Be）已标注
- [ ] 能力名称精确到可操作的业务/技术能力（非泛指）
- [ ] 成熟度跃升处有触发事件标注
- [ ] 颜色图例存在且成熟度等级定义清晰
- [ ] 能力数量 ≤ 10（超过则按域拆分）
- [ ] 标题 / 副标题使用版式占位符（idx=0 / idx=1）
- [ ] Presenter 能用此图说明：今天哪些能力最弱，计划何时解决，解决依赖什么
