# Knowledge Base — Scene Index

This file is the single source of truth for all registered scenes.
To add a new scene: append a row to the table, then create the directory following `_schema.md`.

## Registered Scenes

| slug | 显示名 | 关键词（用于自动识别） |
|------|--------|----------------------|
| `product-roadmap` | 产品蓝图规划 | 路线图, roadmap, 蓝图, 产品规划, OKR, 里程碑, milestone, Q1/Q2/Q3/Q4, 年度计划, 战略时间轴, 举措组合, KPI阶梯, 能力演进, 依赖路径, 发布列车, 资源矩阵, 风险看板, 治理关口, 场景投资, RICE, WSJF, Now/Next/Later, Stage-Gate, RA-01, RA-02, RA-03, RA-04, RA-05, RA-06, RA-07, RA-08, RA-09, RA-10 |
| `product-architecture` | 产品架构设计 | 架构, architecture, 系统设计, 技术方案, API, 微服务, 数据流, 模块, 组件, 技术栈 |
| `product-feature` | 产品功能说明 | 功能, feature, 使用说明, how-to, 操作指南, 用户手册, demo演示, 功能介绍, 产品演示 |
| `product-marketing` | 产品市场宣传 | 市场, marketing, 宣传, 推广, GTM, 增长, 品牌, 竞争分析, 用户价值, 市场定位 |
| `project-roadmap` | 项目蓝图规划 | 项目计划, 项目蓝图, 甘特, Gantt, 交付, 进度, sprint, 资源, 风险, 项目管理 |
| `product-brochure` | 产品表皮书 | 表皮书, brochure, 宣发资料, 产品手册, 解决方案, capability, 产品体系 |

## Scene Directory Structure

Each scene slug maps to:
```
skills/pptx/knowledge/{slug}/
├── style-profile.md      # 色板、排版、设计风格、受众偏好权重
├── slide-structures.md   # 幻灯片大纲模版库（带使用计数）
└── session-log.md        # 历史会话记录（时序日志）
```

## Global PPT Rules

These rules apply to every scene knowledge base:

1. 标题、副标题必须优先写入母版/版式预留的标题类占位符，不得用自绘文本框替代；仅在版式确实不存在对应占位符时才允许降级处理。
2. 所有圆角框默认使用较小圆角，禁止使用 PowerPoint 默认的大圆角观感。
3. 不要添加没有业务语义的装饰性形状；线条、连接线、分隔线同样必须承担结构表达作用，不能只为装饰存在。

## How to Add a New Scene

1. Choose a slug (lowercase, hyphen-separated English)
2. Add a row to the table above with: slug + 显示名 + keyword list
3. Run:
   ```bash
   mkdir skills/pptx/knowledge/{your-slug}
   # Then create the three files following _schema.md template
   ```
4. No changes needed to the Agent file — it reads this index dynamically at session start
