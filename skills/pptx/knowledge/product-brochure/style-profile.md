# Style Profile — 产品表皮书

_Last updated: 2026-03-22 | Sessions recorded: 2_

## Palette Preferences

| Palette slug | 显示名 | Uses | Last used | Notes |
|-------------|--------|------|-----------|-------|
| custom-cloudwise-cmdb-light | Cloudwise CMDB Light | 1 | 2026-03-22 | 白底主导，青色 `00CCD7` 为第一强调色，黑灰正文，少量语义辅色 |
| custom-cloudwise-neutral | Cloudwise Neutral + Accent | 1 | 2026-03-22 | 早期总结，适合作为次级参考 |
| ocean-gradient | Ocean Gradient | 0 | — | 可作为后续同类材料的候选 |
| teal-trust | Teal Trust | 0 | — | 可作为后续同类材料的候选 |
| midnight-executive | Midnight Executive | 0 | — | |
| charcoal-minimal | Charcoal Minimal | 0 | — | |

## Typography Preferences

| Header Font | Body Font | Uses | Notes |
|-------------|-----------|------|-------|
| 微软雅黑 | 微软雅黑 | 2 | 中文主字体绝对主导，CMDB 样本中出现最频繁 |
| Arial | Arial | 1 | 英文标签与辅助文本常用 |
| 思源黑体 CN | 思源黑体 CN / Source Han Sans CN | 1 | 部分标题与信息块补充字体 |
| Calibri | Calibri | 1 | 数字与英文兼容补充字体 |

## Global Generation Rules

- 标题、副标题必须优先写入母版/版式预留的标题类占位符，不得用自绘文本框替代；仅在版式确实不存在对应占位符时才允许降级处理。
- 所有圆角框默认使用较小圆角，禁止使用 PowerPoint 默认的大圆角观感。
- 不要添加没有业务语义的装饰性形状；线条、连接线、分隔线同样必须承担结构表达作用，不能只为装饰存在。

## Design Style Tags

- dark-background: very-low
- icon-heavy: low
- minimal-text: low
- data-rich: medium-high
- full-bleed-images: low
- decorative-shapes: medium
- semantic-shapes: high
- full-width-content: high
- section-banding: high

## Audience Preferences

| Audience type | Frequency | Preferred style adjustments |
|---------------|-----------|----------------------------|
| 管理层 | 1 | 强调价值主张、市场定位、业务成果 |
| 客户/外部 | 1 | 视觉清晰、结构化、可讲解 |
| 售前沟通 | 1 | 挑战-方案-价值链路完整，页面要满版展开 |
| 技术团队 | 0 | |

## Visual Element Density (Averages)

- avg-shapes-per-slide: 27.17
- avg-text-elements-per-slide: 32.89
- avg-images-per-slide: low-to-medium
- slides-with-connectors: 20/35 (57%)
- slides-with-tables: low
- decoration-shapes-style: 细分隔线、宽色块、关系连线、分组图形
- layout-style: 白底满版横向展开、标题区固定、内容区大跨度铺满
- wide-blocks-detected: 49
- full-width-blocks-detected: 31

## Layout & Composition Patterns

| Pattern | Frequency | Examples |
|---------|-----------|----------|
| Section title + wide content field | very-high | 标题在上，主体横向铺满 |
| Multi-column info grid | high | 产品矩阵、挑战拆解、能力分层 |
| Flowchart/connector-based | high | 架构图、关系图、解决路径 |
| Wide semantic blocks | high | 挑战块、价值块、能力块 |
| Data visualization (shapes) | medium | 层级、关系、自定义图表 |

## Design Directives

**形状应用规则**：
1. 形状优先承担结构表达，不为装饰而装饰。
2. 页面主内容宽度应覆盖幻灯片的 85%–95%，避免内容只落在左半边。
3. 标题区保持稳定位置，主体区用宽色块、分栏、连接线横向铺开。
4. 优先使用满版分区、宽矩形、连线、分组图，而不是小卡片堆叠。
5. 深蓝大底不是主风格，最多用于极少数品牌强调页，不应常态化。

## Learning Source & Design Baseline

此知识库当前以 `Cloudwise CMDB解决方案-售前版.pptx` 为主样式基线，并吸收此前 Cloudwise AI 宣发稿的通用结构指引：
- 参考页数：35 页
- 形状密度：平均 27.17/页
- 连接符/流程图频率：57% 页面包含关系连接
- 字体：微软雅黑主导，少量 Arial / 思源黑体 CN
- 调色板：白底 + 青色主强调 + 黑灰正文 + 少量语义辅色
- 布局密度：宽内容区、横向铺满、弱留白、强分区

## CMDB 样式结论

- 主背景：白色或极浅底色，不依赖深蓝通栏或深蓝整页。
- 主品牌色：`00CCD7`，为最高频强调色。
- 正文字色：黑/深灰（`000000` / `404040`）。
- 标题策略：顶部固定标题区，标题偏左但主体内容整体横向铺满，不是左窄右空。
- 正文字号：以 10–14 pt 为主，信息量较高但分组清楚。
- 标题字号：常见 20–36 pt，强调词可用青色或加粗。
- 图形语言：大量组图、关系线、宽矩形、层级块；语义强于装饰。
- 页面观感：适合售前讲解，像“讲结构化方案”，不是“做视觉海报”。

## 页面占位规则

- 内容起始 `x` 建议落在 0.4–1.0 in 之间。
- 主内容最右应尽量延伸到 9.0–9.5 in。
- 单页至少包含一个宽内容带、横向关系图或多列满版布局。
- 避免 6 in 以下的小内容岛孤立在画面中央或左侧。
- 标题和内容之间留稳定呼吸区，但页面整体必须“撑满”。

## 图形表达规范

**重要**：避免纯文字列表，应根据内容逻辑灵活应用图形模式。

详见 `diagram-patterns.md`，优先使用：
- 并列、列表、总分、关系、流程、组织架构

每页内容应至少包含一种图形模式以增强视觉表达。
