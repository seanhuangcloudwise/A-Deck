# A-Deck

**企业级 PPTX 自动生成工具集** — 让 AI 像售前顾问一样做 PPT。

A-Deck 不是"文字转 PPT"工具。它是一个知识驱动、母版继承、提纲优先的演示文稿生成平台，目标是输出**可交付**的品牌化演示文稿，而不仅仅是可预览的草稿。

## 核心能力

| 能力 | 说明 |
|------|------|
| **学习** | 从现有 PPT 提取配色、字体、布局规律，沉淀到母版库 |
| **生成** | 基于品牌母版 + template spec + 知识库 + 内容逻辑，一次性组装完整 PPT |
| **质检** | 校验主题继承、内容完整性、版式一致性，避免空页和样式漂移 |
| **编辑** | 解包 PPTX 为 XML，精确编辑后重新打包 |
| **多母版回归** | 同一套图形 skill 在多母版下批量生成并对比（Theme/Overflow/页数） |

## 架构

```
用户输入（主题 / 受众 / 风格）
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  Master Library              Skill Loaders             │
│  品牌母版（3 色系）           TOGAF / GTM / RA / XSean  │
│  dark-cloudwise-green        图形模板 · 布局规则         │
│  light-cloudwise-cyan        共享渲染库 pptx_lib.py     │
│  light-cloudwise-purple                               │
└────────────────────────┬──────────────────────────────┘
                         │
                         ▼
                  Generation Engine
                  generate_*.py 编排
                  组装页面 · 应用母版 · 缩放适配
                         │
                         ▼
                  输出 PPTX + QA 验证
                  （Slides / Theme match / Overflow）
```

## 目录结构

```
A-Deck/
├── docs/                               # 产品规范与功能契约
│   └── ppt-maker-agent-spec.md
├── skills/pptx/                        # 核心技能包
│   ├── SKILL.md                        #   操作速查
│   ├── scripts/                        #   共享渲染库与工具
│   │   ├── pptx_lib.py                 #     绘图原语 · BuildContext
│   │   └── office/                     #     unpack / pack / soffice
│   ├── shared/                         #   跨 loader 公共工具
│   │   └── renderer_utils.py
│   ├── master-library/                 #   品牌母版资产库
│   │   ├── dark-cloudwise-green/
│   │   ├── light-cloudwise-cyan/
│   │   └── light-cloudwise-purple/
│   ├── togaf-architecture/             #   TOGAF 图形 Skill（BA/AA/TA）
│   │   └── loaders/
│   ├── gtm-architecture/               #   GTM 图形 Skill
│   │   └── loaders/
│   ├── roadmap-architecture/           #   路线图图形 Skill
│   │   └── loaders/
│   └── XSean/                          #   XSean 专属图形域
│       ├── diagrams/                   #     图形规格文档
│       └── loaders/                    #     渲染器实现
├── projects/                           # 生成项目
│   ├── ppt-maker-intro-cloudwise-2025/ #   Cloudwise 自我介绍（多母版）
│   ├── business-process-full-deck/     #   业务流程泳道图
│   ├── togaf-architecture-full-demo/   #   TOGAF 全架构演示
│   ├── gtm-a-deck-demo-full/           #   GTM 全流程演示
│   ├── roadmap-architecture-full-demo/ #   路线图架构演示
│   └── ...                             #   其他测试 & 验证项目
└── output/                             # 学习产物 & QA 中间产物
```

## 技术栈

| 层 | 技术 |
|----|------|
| 模板生成（Python） | python-pptx · pptx_lib.py 共享库 |
| 从零生成（Node.js） | PptxGenJS v4 |
| XML 编辑 | defusedxml · lxml |
| 文本提取 | markitdown |
| 视觉校验 | LibreOffice headless → PDF → pdftoppm → PIL 网格 |

## 快速开始

### 模板生成（推荐）

```bash
cd projects/ppt-maker-intro-cloudwise-2025
python3 generate_from_template.py
# → ppt-maker-agent-self-intro-cloudwise.pptx
```

### 多母版一键回归（GTM + Roadmap）

```bash
source .venv/bin/activate
python output/_test_all_masters.py
# 输出到 projects/test-masters/
# 包含 6 份回归产物：
#   gtm-{dark-cloudwise-green|light-cloudwise-cyan|light-cloudwise-purple}.pptx
#   roadmap-{dark-cloudwise-green|light-cloudwise-cyan|light-cloudwise-purple}.pptx
```

### 多母版一键回归（TOGAF）

```bash
source .venv/bin/activate
python projects/togaf-architecture-full-demo/_test_all_masters.py
# 输出到 projects/togaf-architecture-full-demo/
# 包含 2 份回归产物：
#   togaf-dark-green.pptx
#   togaf-light-cyan.pptx
# 另可使用 generate.py 生成当前默认母版文件：
#   togaf-architecture-full-demo.pptx
```

### 共享库用法

```python
from pptx_lib import *

def my_slides(ctx):
    slide = ctx.add_content_slide()
    header(slide, "标题", subtitle="副标题", num=1)
    render_flow(slide, [
        {"title": "输入", "desc": "需求与目标"},
        {"title": "处理", "desc": "知识匹配"},
        {"title": "输出", "desc": "品牌化 PPT"},
    ])

build_pptx("template.pptx", "output.pptx", my_slides, "cloudwise-spec.yaml")
```

说明：

1. `build_pptx` 推荐总是传入与母版同目录的 spec 文件。
2. 主题色以 PPTX 的 theme XML 为准（`extract_theme_colors`），spec 中的 `infrastructure_colors.palette` 主要用于兼容别名补充。
3. loader 中品牌色应来自 `ctx.colors` / `ctx.palette`，避免硬编码品牌 RGB。

### 图形模式

| 渲染器 | 用途 | 调用 |
|--------|------|------|
| `render_flow()` | 横向流程图 | 步骤 + 箭头连接 |
| `render_three_cols()` | 三列并列 | 标题栏 + 要点列表 |
| `render_wide_list()` | 全宽堆叠条 | 颜色交替信息条 |
| `render_relationship()` | 总分关系 | 根节点 → 三子列 |
| `render_capability_map()` | 能力矩阵 | 领域行 × 能力列 + 成熟度着色 |

### XML 编辑工作流

```bash
python3 skills/pptx/scripts/office/unpack.py input.pptx unpacked/
# 手动编辑 unpacked/ppt/slides/*.xml
python3 skills/pptx/scripts/clean.py unpacked/
python3 skills/pptx/scripts/office/pack.py unpacked/ output.pptx
```

## 工作流覆盖

| 编号 | 工作流 | 状态 |
|------|--------|------|
| W1 | 从零创建 | ✅ |
| W2 | 编辑现有 PPT | ✅ |
| W3 | 分析 PPT | ✅ |
| W4 | 模板化生成 | ✅ |
| W5 | 从 PPT 学习 | ✅ |
| W6 | 母版提取 | ✅ |

## 母版与图形 Skill 扩展机制

面向“新增母版”和“新增图形 loader”扩展，当前版本遵循以下机制：

1. 运行时契约：统一走 `build_pptx(template, output, my_slides, template_spec)`。
2. 版式选择：优先使用 layout 名称 + fallback index（来自 spec）。
3. 数据驱动：loader 只做渲染，业务内容来自外部 YAML。
4. 颜色机制：母版 theme XML -> `ctx.colors` / `ctx.palette`；仅图形规范明确要求的语义保留色可例外。
5. 缩放机制：若 loader 已做内部缩放映射，需避免与全局缩放叠加（防止双重缩放导致溢出）。
6. 回归必测：Theme match、页数、Right overflow、占位符渲染。

详细规范见：

1. `skills/pptx/SKILL.md`
2. `skills/pptx/master-library/_schema.md`

## QA 基线

每份生成的 PPT 都经过三重校验：

1. **内容校验** — markitdown 提取文本，检查无占位符残留（xxxx / lorem / TODO）
2. **视觉校验** — LibreOffice 转 PDF → JPEG 缩略图网格，目视确认版面
3. **结构校验** — 主题 hash 匹配、XML 关系完整性、坐标值为整数（无 float EMU）

## 设计原则

- **提纲优先** — 先确认逐页内容提纲，再生成页面
- **母版继承** — 沿用品牌的 theme / layout / master，保证视觉一致性
- **EMU 整数化** — 所有坐标计算结果 `int()` 转型，防止 XML 中出现 `"2647188.0"` 导致文件损坏
- **知识沉淀** — 每次学习的风格规则和结构模式保存为 knowledge，支持跨项目复用
- **安全 XML** — 优先使用 defusedxml，防止 XXE 等注入风险

## 许可

ISC
