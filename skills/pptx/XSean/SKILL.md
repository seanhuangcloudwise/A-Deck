# XSean Diagram Skill

面向私有绘图资产的可扩展技能域，和 gtm-architecture / roadmap-architecture 同级。
目标是沉淀“可复用、可参数化、可回归”的图形装载器（loader）与规范。

---

## Scope

Use this skill when users ask for:
- 私有方法论图（流程、机制、规则、能力映射）
- 需要跨母版复用的结构化图形模板
- 从文本数据快速生成“可交付级”图页
- 需要通过 loader 扩展新图类（Xxx）

Do not use this skill for:
- TOGAF 标准业务/应用/数据/技术分层图（-> togaf-architecture）
- GTM 营销定位与价值表达图（-> gtm-architecture）
- 路线图与优先级治理图（-> roadmap-architecture）

---

## Architecture

```
XSean/
  SKILL.md
  _index.md
  diagrams/
    _catalog.md
    x01-founction-architecture.md
  loaders/
    __init__.py
    common.py
    _template.py
    x01_function_architecture.py
```

---

## Naming Convention

- Diagram ID: `X01`, `X02` ...
- Loader file: `x01_*.py`
- Loader entry: `load_slide(ctx, data)`
- Content payload path: `data["content"]`

Note:
- `X01` 已提供专属 loader：`loaders/x01_function_architecture.py`。

---

## Mandatory Rules

1. 标题/副标题优先使用 placeholder（idx=0/1）。
2. 所有坐标和尺寸必须使用整数 EMU（避免浮点写入 XML）。
3. 颜色优先来自 `ctx.colors`，禁止硬编码品牌色。
4. 连接线必须有语义（流向/依赖/异常），不能只做装饰。
5. 新图类必须先补 `diagrams/` 规格，再写 loader。

---

## Expansion Workflow

1. 在 `diagrams/` 新增 `xxx-*.md` 规格文档（目标、数据结构、布局规则）。
2. 在 `loaders/` 新增 `xxx_*.py`，实现 `load_slide(ctx, data)`。
3. 在项目侧配置中增加 `slide_id -> loader_id -> content` 映射。
4. 用三母版回归脚本验证：页数、theme match、overflow。

---

## QA Checklist

- [ ] 标题/副标题来自版式占位符
- [ ] 无右侧越界（overflow）
- [ ] 连接关系完整且语义可读
- [ ] 不依赖硬编码品牌色
- [ ] 图中关键标签 30 秒内可理解
