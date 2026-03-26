# GTM Architecture Skill

产品走向市场（GTM）图表体系，覆盖产品白皮书、解决方案、销售一指禅、市场宣传、产品特性表达与价值透出材料。

---

## Scope

Use this skill when users ask for:
- 产品白皮书中的架构与价值表达图
- 解决方案 brief 的场景架构、特性表达与 ROI 图
- 销售 battle card、竞品对比、ICP 定位图
- 市场宣传 deck、品类占领、分析师 briefing 材料
- 产品特性透出图（特性深度、机制、采用率、发布节奏）
- 商务价值透出图（价值驱动、KPI 对照、TTV、不行动成本、敏感性）

Do not use this skill for:
- 技术系统架构图 -> `togaf-architecture`
- 产品路线图、优先级规划 -> `roadmap-architecture`
- 产品功能操作演示 -> `knowledge/product-feature`
- 项目交付计划 -> `knowledge/project-roadmap`

---

## Method Stack

| 方法论 | 来源 | 适用图类 |
|---|---|---|
| Crossing the Chasm Positioning | Geoffrey Moore | GM-01 |
| Elements of Value | Bain x HBR 2016 | GM-02, GM-26 |
| Jobs-to-be-Done (JTBD) | Clayton Christensen | GM-08, GM-20 |
| Gartner Magic Quadrant | Gartner Research | GM-04 |
| Forrester TEI Framework | Forrester Research | GM-10, GM-28, GM-29, GM-30 |
| Service Blueprint | Nielsen Norman Group | GM-08 |
| PLG / SLG / CLG Motion | Openview Partners / a16z | GM-13, GM-23 |
| Command of the Message | Force Management | GM-15, GM-25 |
| Category Creation | Play Bigger (2016) | GM-16 |
| MEDDIC / ICP Framework | Miller Heiman / SiriusDecisions | GM-14 |
| Product Discovery and Kano | Kano model | GM-18, GM-21, GM-32 |
| Value Realization Framework | Gainsight / CS Ops practices | GM-31, GM-33, GM-34 |

---

## Diagram Catalog (Must Support)

### G1 - Value Proposition
1. GM-01 Positioning Statement Diagram
2. GM-02 Value Pyramid
3. GM-03 Before/After Comparison

### G2 - Market and Competition
4. GM-04 Market Positioning Matrix
5. GM-05 Competitive Comparison Matrix
6. GM-06 Market Ecosystem Map

### G3 - Solution Architecture
7. GM-07 Solution Reference Architecture
8. GM-08 Customer Journey with Touchpoints
9. GM-09 Use Case Scenario Diagram

### G4 - Proof and ROI
10. GM-10 ROI / Business Case Frame
11. GM-11 KPI Dashboard Mockup
12. GM-12 Customer Success Metrics Card

### G5 - GTM Strategy
13. GM-13 GTM Motion Diagram
14. GM-14 ICP Segmentation Map
15. GM-15 Sales Playbook Flow

### G6 - Category and Analyst
16. GM-16 Category Creation Diagram
17. GM-17 Analyst Briefing Framework

### G7 - Product Feature Expression
18. GM-18 Feature Capability Matrix
19. GM-19 Feature Differentiation Radar
20. GM-20 Feature to Use Case Mapping
21. GM-21 Feature Depth Ladder
22. GM-22 Unique Mechanism Diagram
23. GM-23 Feature Adoption Funnel
24. GM-24 Feature Release Timeline
25. GM-25 Feature Proof Card

### G8 - Value Realization
26. GM-26 Value Driver Tree
27. GM-27 Capability to Outcome Trace Matrix
28. GM-28 Time to Value Curve
29. GM-29 Baseline vs Target KPI Table
30. GM-30 Cost of Inaction Table
31. GM-31 Benefit Realization Roadmap
32. GM-32 Persona Value Map
33. GM-33 Risk Reduction Heatmap
34. GM-34 Proof Evidence Ladder
35. GM-35 Assumption Sensitivity Table

---

## Diagram Specifications

See `diagrams/` subdirectory and [diagrams/_catalog.md](diagrams/_catalog.md) for full mapping.

---

## Selection Logic

- 用户提到“定位”“价值主张”“我们做什么” -> GM-01, GM-02
- 用户提到“痛点”“现状 vs 未来”“before/after” -> GM-03
- 用户提到“竞争”“差异化”“为什么选我们” -> GM-04, GM-05, GM-19
- 用户提到“市场格局”“生态” -> GM-06
- 用户提到“方案架构”“集成” -> GM-07
- 用户提到“客户旅程”“场景路径”“触点” -> GM-08, GM-09, GM-20
- 用户提到“ROI”“商业价值”“TCO”“不行动成本” -> GM-10, GM-26, GM-29, GM-30
- 用户提到“指标”“效果数据”“dashboard” -> GM-11, GM-27
- 用户提到“GTM策略”“打法” -> GM-13
- 用户提到“ICP”“客户分层” -> GM-14
- 用户提到“销售剧本”“battle card” -> GM-05, GM-15, GM-25
- 用户提到“品类”“占领认知” -> GM-16
- 用户提到“分析师 briefing” -> GM-17, GM-34
- 用户提到“产品特性”“功能深度”“机制壁垒” -> GM-18 to GM-25
- 用户提到“价值透出”“价值实现”“敏感性分析” -> GM-26 to GM-35

---

## Mandatory Rules

1. 标题和副标题优先使用版式占位符（idx=0/1）。
2. 圆角框半径 <= 6pt，避免默认大圆角。
3. 每条连接线必须承载语义，避免纯装饰。
4. Cloudwise 色板强制：`#00CCD7` / `#53E3EB` / `#2F2F2F` / `#A5A7AA` / `#44546A`。
5. 所有价值声明需有可验证数据或来源。
6. 竞争和能力声明避免绝对化措辞，需可辩护。

## QA Checklist

- [ ] 标题和副标题使用 placeholder（idx=0/1）
- [ ] 价值声明有数据或来源支撑
- [ ] 特性类图表包含场景或证据，不是纯功能堆砌
- [ ] 价值类图表包含基线和目标口径
- [ ] 颜色语义符合 Cloudwise 色板
- [ ] 页面可在 30 秒内被目标受众理解