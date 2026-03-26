# Roadmap Architecture Skill

产品规划路线图体系 — 产品规划类方法论驱动的路线图 PPT 能力域。
与 TOGAF 四层能力域并列，专注于"从战略意图到执行交付"的产品规划可视化。

---

## Scope

Use this skill when users ask for:
- 战略路线图、年度规划、多年期蓝图
- 产品 roadmap、发布计划、里程碑拆解
- 举措/需求优先级排序（RICE/WSJF/价值-投入分析）
- KPI 目标阶梯、结果追踪
- 资源分配、投资视图
- 依赖管理、关键路径、治理关口
- 风险识别与缓解管理（规划视角）
- 场景化投资分析（保守/基准/激进）

Do **not** use this skill for:
- 系统/能力架构图（→ TOGAF Business Architecture）
- 技术部署图（→ Technology Architecture）
- 数据流/数据域图（→ Data Architecture）
- 流程 SOP / 泳道图（→ Business Architecture BA-03）

---

## Method Stack

本能力域采用以下主流产品规划方法论：

| 方法 | 应用场景 |
|------|---------|
| OST (Opportunity Solution Tree) | 机会识别与方案挂载 |
| RICE (Reach/Impact/Confidence/Effort) | 功能/需求级优先级 |
| WSJF (Weighted Shortest Job First) | 组合/史诗级优先级 |
| Now/Next/Later | 执行沟通格式 |
| Stage-Gate® | 阶段治理检查点 |
| KPI Driver Tree | 结果可追溯量化框架 |
| Scenario Planning | 不确定性下的投资决策 |

---

## Planning Architecture (4 Layers)

```
P1 Strategy Intent    → RA-01 战略路线图时间轴 | RA-04 能力演进路线图
P2 Opportunity & Portfolio → RA-02 举措组合热力矩阵 | RA-07 资源-优先级矩阵 | RA-10 场景化投资视图
P3 Delivery Planning  → RA-05 依赖与关键路径图 | RA-06 发布列车/季度计划 | RA-09 治理关口图
P4 Validation & Learning → RA-03 KPI里程碑阶梯 | RA-08 风险与缓解看板
```

---

## Diagram Catalog (Must Support)

1. **RA-01 战略路线图时间轴** — 多泳道横向时间轴，战略主题 × 季度/半年
2. **RA-02 举措组合热力矩阵** — 价值 vs 投入/风险的二维热力图，气泡= 举措规模
3. **RA-03 KPI里程碑阶梯** — 阶梯式 KPI 进展，基准→目标→拉伸目标
4. **RA-04 能力演进路线图** — 能力成熟度跨时段演进，二维热图+时间轴
5. **RA-05 依赖与关键路径图** — 有向无环图（DAG），关键路径红线高亮
6. **RA-06 发布列车/季度计划** — PI 规划甘特+迭代泳道，发布里程碑标注
7. **RA-07 资源-优先级矩阵** — 优先级 × 资源消耗 2×2 象限，举措气泡定位
8. **RA-08 风险与缓解看板** — 看板列（已识别/评估中/缓解中/已关闭）+ P×I 热力
9. **RA-09 治理关口图** — 阶段块 + 关口菱形 + RACI 迷你表，Go/No-Go 标记
10. **RA-10 场景化投资视图** — 场景列（保守/基准/激进）× 举措行，投资气泡

---

## Mandatory Rules

1. 标题/副标题必须使用版式占位符（idx=0 标题，idx=1 副标题）
2. 圆角框半径 ≤ 6pt，禁止 PowerPoint 大圆角默认值
3. 每个连接线必须承载语义（流向/依赖/阻塞），禁止纯装饰性线条
4. 色彩从母版 theme 动态读取（`ctx.colors`），禁止在 loader 中硬编码品牌色。仅语义专用色（如关键路径红、状态指示色）可硬编码。
5. 时间轴类图表必须标注时间范围（季度/年份）
6. 优先级类图表必须注明评分方法（RICE/WSJF/手工排序）
7. 任何里程碑必须标注 Owner + 目标日期

---

## Diagram Specifications

所有图类详见 `diagrams/` 子目录：

- [RA-01: 战略路线图时间轴](diagrams/ra-01-strategic-timeline.md)
- [RA-02: 举措组合热力矩阵](diagrams/ra-02-portfolio-heat-matrix.md)
- [RA-03: KPI里程碑阶梯](diagrams/ra-03-kpi-milestone-ladder.md)
- [RA-04: 能力演进路线图](diagrams/ra-04-capability-evolution.md)
- [RA-05: 依赖与关键路径图](diagrams/ra-05-dependency-critical-path.md)
- [RA-06: 发布列车/季度计划](diagrams/ra-06-release-train-quarterly.md)
- [RA-07: 资源-优先级矩阵](diagrams/ra-07-resource-priority-matrix.md)
- [RA-08: 风险与缓解看板](diagrams/ra-08-risk-mitigation-kanban.md)
- [RA-09: 治理关口图](diagrams/ra-09-governance-gate.md)
- [RA-10: 场景化投资视图](diagrams/ra-10-scenario-investment.md)

See [diagrams/_catalog.md](diagrams/_catalog.md) for selection guide.

---

## Loader Mechanism (Data-Driven)

Roadmap Architecture skill now supports dynamic loader expansion, aligned with GTM mechanism:

1. Loader files live in [skills/pptx/roadmap-architecture/loaders](skills/pptx/roadmap-architecture/loaders)
2. Each loader implements a standard entry:
	- `load_slide(ctx, data)`
3. Orchestrator auto-discovers `ra_*.py` and registers them dynamically.
4. Business data is externalized in YAML config; no hardcoded business text in orchestrator.

Reference demo project:

- Generator: [projects/roadmap-architecture-full-demo/generate.py](projects/roadmap-architecture-full-demo/generate.py)
- Data config: [projects/roadmap-architecture-full-demo/data/config_template.yaml](projects/roadmap-architecture-full-demo/data/config_template.yaml)

To add a new roadmap diagram loader:

1. Add `ra_xx_*.py` under loaders directory.
2. Implement `load_slide(ctx, data)` with placeholder-based title/subtitle.
3. Register data entry in demo config under the target section.
4. Re-run generator; loader will be picked up automatically.

---

## Selection Logic

```
战略全景、年度主题展示          → RA-01
举措竞争优先级排序决策          → RA-02 + RA-07
KPI 目标拆解、结果追踪         → RA-03
能力成熟度规划、演进路径        → RA-04
交付依赖管理、关键路径分析      → RA-05
季度执行计划、发布节奏          → RA-06
风险可见度、缓解状态跟踪        → RA-08
阶段评审、投资决策关口          → RA-09
预算分配、多情景对比决策        → RA-10
```

---

## QA Checklist

- [ ] 时间轴图表是否标注了季度/年份？
- [ ] 优先级图表是否注明了评分口径（RICE/WSJF）？
- [ ] 所有里程碑是否有 Owner + 目标日期？
- [ ] 颜色是否从 `ctx.colors` 动态获取（禁止硬编码品牌色）？
- [ ] 关口图的每个关口是否有明确的 Go/No-Go 判断标准？
- [ ] 风险看板是否标注了 P×I 分值？
- [ ] 场景投资视图是否包含≥2 个对比情景？

---

## Failure Fallbacks

- 举措数量 > 20 条：优先 RA-02 热力矩阵先筛选，再用 RA-06/RA-07 做局部展开
- 时间轴跨度 > 2 年：按年拆分为独立幻灯片，共用同一图例
- 依赖关系 > 15 条边：去除非关键路径连接，剩余高亮关键链路
- 数据不完整：按现有数据渲染，缺失字段用明确占位符标出（如 "Owner: TBD"）
