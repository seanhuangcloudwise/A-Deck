# cloudwise 2025

- master-id: light-cloudwise-cyan
- scene: product-brochure
- source: skills/pptx/master-library/light-cloudwise-cyan/cloudwise-master.pptx
- style-spec-source: skills/pptx/master-library/light-cloudwise-cyan/cloudwise-master.pptx (layout: 内容)
- layout count: 12
- master count: 1

## Key Layouts

1. slideLayout1 — Cover / Title-like structure
2. slideLayout2 — 内容（章节标题 + 副标题）
3. slideLayout3 — Dense content block
4. slideLayout4 — Multi-card capability comparison
5. slideLayout5 — Two-column description
6. slideLayout6 — List-heavy explanatory page
7. slideLayout7 — Diagram-oriented content
8. slideLayout8 — Summary / closing style
9. slideLayout9 — Visual emphasis block
10. slideLayout10 — Variant content grid
11. slideLayout11 — Variant two-column
12. slideLayout12 — Variant diagram/text mix

## Visual Signature

- Main colors: A5A7AA, 00CCD7, 2F2F2F, 53E3EB
- Fonts: Source Han Sans CN Normal, 微软雅黑
- Style tags: low dark background, medium icon density, high decorative shape density

## Content Layout Conventions

### Slide dimensions

- Width: 13.33" (12192000 EMU)
- Height: 7.50" (6858000 EMU)
- Aspect ratio: 16:9

### Safe margins (内容安全区)

| Zone | Top (Y) | Bottom (Y) | Height |
|------|---------|------------|--------|
| Header zone (顶部母版区) | 0" – 0.75" (10%) | — | 0.75" |
| Content safe zone (内容区) | 0.75" (10%) | 6.75" (90%) | 6.00" |
| Footer zone (底部母版区) | — | 6.75" – 7.50" (10%) | 0.75" |

- **规则**: 内容页的正文、图表、泳道等主体内容必须放在 Content safe zone (0.75" – 6.75") 内，上下居中排布。
- **Header**: 标题 placeholder 由母版控制位置（约 0.29"），属于 Header zone，不受此约束。
- **Footer**: 页脚分隔线和元数据属于 Footer zone，不受此约束。
- **左右安全边距**: SAFE_LEFT=0.3"  SAFE_RIGHT=9.68"（基于 10" 设计基线，运行时按 scale_x 缩放）

### 版式「内容」(slideLayout2) — 章节标题 / 副标题规范

#### 章节标题（占位符）

| 属性 | 值 | 来源 |
|------|----|------|
| shape name | 标题 1 | layout |
| type | title (idx=0) | placeholder |
| 位置 | left=2.385" / top=0.150" | layout spPr |
| 尺寸 | width=10.616" / height=0.463" | layout spPr |
| 字号 | 24pt | layout lstStyle lvl1pPr `sz="2400"` |
| 粗体 | Yes | layout lstStyle `b="1"` |
| 颜色 | accent1 -> #00CCD7 | layout lstStyle `schemeClr val="accent1"` |
| 字体 | +mj-ea -> 微软雅黑 | theme majorFont |
| CS 字体 | 微软雅黑 | layout lstStyle explicit |
| bodyPr | wrap=square, spAutoFit | layout |
| 语言 | kumimoji=1, zh-CN / en-US | layout |

#### 副标题（占位符）

| 属性 | 值 | 来源 |
|------|----|------|
| shape name | 标题 1 | layout |
| type | subTitle (idx=1) | placeholder |
| 位置 | left=2.397" / top=0.499" | layout spPr |
| 尺寸 | width=10.616" / height=0.301" | layout spPr |
| 字号 | 12pt | layout lstStyle lvl1pPr `sz="1200"` |
| 颜色 | bg1 + lumMod 65000 | `a:schemeClr val="bg1"` |
| 粗体 | No | layout lstStyle `b="0"` |
| 字体 | 跟随主题字体（微软雅黑） | 主题继承 |
| bodyPr | wrap=square, spAutoFit | layout |

**代码约定**:
- `header()` 写入章节标题时不覆盖 font 属性，保持 title placeholder 的母版继承样式。
- `subtitle` 必须写入 subtitle placeholder（idx=1, top=0.499"），不新建任意位置文本框。

### 主题色方案（"云智慧"）

| 标识 | 色值 | 用途 |
|------|------|------|
| dk1 | #000000 | 深色文本1 |
| lt1 | #FFFFFF | 浅色背景1 |
| dk2 | #44546A | 深色文本2 / domain_bg |
| lt2 | #E7E6E6 | 浅色背景2 |
| accent1 | #00CCD7 | 品牌主色（标题、强调） |
| accent2 | #67E0E6 | 辅助青色 |
| accent3 | #23C1E0 | 辅助蓝青 |
| accent4 | #55CED4 | 辅助青绿 |
| accent5 | #5B9BD5 | 蓝色 |
| accent6 | #70AD47 | 绿色 |

### 主题字体

| 引用 | 字体 |
|------|------|
| majorFont (+mj-lt / +mj-ea) | 微软雅黑 |
| minorFont (+mn-lt / +mn-ea) | 微软雅黑 |
| Slide Master titleStyle | Source Han Sans CN Normal (被 layout 覆盖) |
| Slide Master bodyStyle | Source Han Sans CN Normal |
