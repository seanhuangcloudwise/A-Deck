# Knowledge Base — File Schema

This document defines the exact structure each scene's three files must follow.
When the Agent writes knowledge to disk, it must use these exact formats.

---

## style-profile.md template

```markdown
# Style Profile — {场景显示名}

_Last updated: YYYY-MM-DD | Sessions recorded: N_

## Palette Preferences

<!-- 按使用次数降序排列。Uses=0 表示未使用过但可作为候选 -->
| Palette slug | 显示名 | Uses | Last used | Notes |
|-------------|--------|------|-----------|-------|
| teal-trust | Teal Trust | 0 | — | |

## Typography Preferences

| Header Font | Body Font | Uses | Notes |
|-------------|-----------|------|-------|
| Georgia | Calibri | 0 | |

## Global Generation Rules

- 标题、副标题必须优先写入母版/版式预留的标题类占位符，不得用自绘文本框替代；仅在版式确实不存在对应占位符时才允许降级处理。
- 所有圆角框默认使用较小圆角，禁止使用 PowerPoint 默认的大圆角观感。
- 不要添加没有业务语义的装饰性形状；线条、连接线、分隔线同样必须承担结构表达作用，不能只为装饰存在。

## Design Style Tags

<!-- 强度: none / low / medium / high -->
- dark-background: none        # 深色背景幻灯片占比偏好
- icon-heavy: none             # 图标密度偏好
- minimal-text: none           # 文字简洁倾向（少文字大图形）
- data-rich: none              # 图表/数据出现频率
- full-bleed-images: none      # 全出血图片使用倾向
- decorative-shapes: none      # 装饰性形状（色块、线条）密度

## Audience Preferences

| Audience type | Frequency | Preferred style adjustments |
|---------------|-----------|----------------------------|
| 技术团队 | 0 | |
| 管理层 | 0 | |
| 客户/外部 | 0 | |

## Visual Element Density (Averages)

- avg-icons-per-slide: 0
- avg-shapes-per-slide: 0
- avg-images-per-slide: 0
- charts-frequency: none       # none / occasional / frequent

## Learned from Files

<!-- 通过 Workflow 5 (Learn from PPTX) 导入的参考文件记录 -->
| Date | File | Scene match | Key insights extracted |
|------|------|-------------|----------------------|
```

All generated or updated style profiles must preserve the `Global Generation Rules` section verbatim.

---

## slide-structures.md template

```markdown
# Slide Structures — {场景显示名}

_Last updated: YYYY-MM-DD | Templates recorded: N_

## Templates

### Template: {模版名称}

- **Source**: manual | learned-from-file | session-generated
- **Uses**: 0
- **Audience**: 通用 / 技术团队 / 管理层 / 客户
- **Slide count**: N
- **Added**: YYYY-MM-DD
- **Last used**: —

**Structure**:
1. Cover — {标题} | {副标题}
2. Agenda — {本次内容导航}
3. {幻灯片名} — {内容类型: text/chart/icon-grid/stats/timeline/...}
...
N. Close — {结尾类型: CTA/summary/contact}

**Notes**: {任何关于此模版适用场景的说明}

---
```

---

## session-log.md template

```markdown
# Session Log — {场景显示名}

_Total sessions: 0_

## Log

<!-- 每次用户确认保存后追加一行 -->
| Date | Topic snippet | Palette | Slides | Structure | QA issues | Saved by |
|------|---------------|---------|--------|-----------|-----------|----------|
```
