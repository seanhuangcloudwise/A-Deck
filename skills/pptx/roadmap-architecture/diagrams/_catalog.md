# Roadmap Architecture Diagram Catalog

Domain: Product Planning Roadmap Architecture (独立能力域，与 TOGAF 四层并列)
Total Specs: 10
Cloudwise Palette: #00CCD7 / #53E3EB / #2F2F2F / #A5A7AA / #44546A
Audience: CPO, Product Manager, Strategy, PMO, Executive, Business Analyst

---

## Diagram Index

| ID | File | Chinese Name | Primary Audience | Best For |
|----|------|-------------|-----------------|---------|
| RA-01 | [ra-01-strategic-timeline.md](ra-01-strategic-timeline.md) | 战略路线图时间轴 | CPO, Executive | 年度/多年战略展示、主题-举措对齐 |
| RA-02 | [ra-02-portfolio-heat-matrix.md](ra-02-portfolio-heat-matrix.md) | 举措组合热力矩阵 | CPO, PM, Strategy | 举措优先级决策、投资组合平衡 |
| RA-03 | [ra-03-kpi-milestone-ladder.md](ra-03-kpi-milestone-ladder.md) | KPI里程碑阶梯 | Executive, PMO | OKR/KPI 目标拆解、结果追踪 |
| RA-04 | [ra-04-capability-evolution.md](ra-04-capability-evolution.md) | 能力演进路线图 | CPO, Architect, Strategy | 能力成熟度规划、技术/组织演进 |
| RA-05 | [ra-05-dependency-critical-path.md](ra-05-dependency-critical-path.md) | 依赖与关键路径图 | PM, Delivery Lead | 交付依赖管理、关键路径分析 |
| RA-06 | [ra-06-release-train-quarterly.md](ra-06-release-train-quarterly.md) | 发布列车/季度计划 | PM, Engineering, PMO | PI 规划、季度迭代节奏、发布协调 |
| RA-07 | [ra-07-resource-priority-matrix.md](ra-07-resource-priority-matrix.md) | 资源-优先级矩阵 | CPO, PMO, Finance | 资源分配决策、投入-产出可视化 |
| RA-08 | [ra-08-risk-mitigation-kanban.md](ra-08-risk-mitigation-kanban.md) | 风险与缓解看板 | PM, PMO, Risk Owner | 规划期风险识别与缓解状态跟踪 |
| RA-09 | [ra-09-governance-gate.md](ra-09-governance-gate.md) | 治理关口图 | Executive, PMO, Sponsor | 阶段评审、投资决策关口、Go/No-Go |
| RA-10 | [ra-10-scenario-investment.md](ra-10-scenario-investment.md) | 场景化投资视图 | CPO, CFO, Strategy | 多情景对比、不确定性下的投资决策 |

---

## Selection Guide

```
Input intent → Recommended diagram

战略展示、年度主题、多年蓝图                → RA-01 战略路线图时间轴
举措数量 > 5，需要决策优先序               → RA-02 举措组合热力矩阵
OKR 分解、KPI 目标梯级展示               → RA-03 KPI里程碑阶梯
能力规划、成熟度演进路径                   → RA-04 能力演进路线图
交付依赖、阻塞分析、关键路径              → RA-05 依赖与关键路径图
季度计划、PI 规划、发布节奏              → RA-06 发布列车/季度计划
资源分配、团队投入、优先级 vs 成本         → RA-07 资源-优先级矩阵
规划期风险登记与缓解进度                  → RA-08 风险与缓解看板
阶段评审、阶段关口、投资决策流程          → RA-09 治理关口图
多方案对比、情景规划、预算路径            → RA-10 场景化投资视图
```

---

## Planning Layer Routing

```
P1 Strategy Intent       → RA-01, RA-04
P2 Opportunity & Portfolio → RA-02, RA-07, RA-10
P3 Delivery Planning     → RA-05, RA-06, RA-09
P4 Validation & Learning → RA-03, RA-08
```

---

## Shared Constraints (All RA Diagrams)

1. 标题和副标题 **必须** 使用幻灯片版式占位符（idx=0 标题，idx=1 副标题）
2. 所有圆角框 corner radius ≤ 6pt；禁止使用 PowerPoint 默认大圆角
3. 每个连接线必须承载语义（流向/依赖/阻塞），禁止纯装饰性线条
4. Cloudwise 色板强制：`#00CCD7`（主色）/ `#53E3EB`（次色）/ `#2F2F2F`（文字）/ `#A5A7AA`（辅助）/ `#44546A`（区域头）
5. 时间轴类图表（RA-01/RA-04/RA-06）必须标注时间范围
6. 评分/优先级图表（RA-02/RA-07）必须注明评分口径
7. 任何里程碑节点必须包含 Owner + 目标日期
8. 每张图必须有图例（Legend），解释颜色/大小/形状的语义
