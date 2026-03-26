# GTM A-Deck 完整演示PPT - 装载器架构

## 📋 架构概述

本项目采用**数据驱动、高内聚低耦合**的设计模式，每个GTM图表（GM-01~GM-35）通过独立的**装载器模块**来实现。

### 核心原则

```
业务数据（外部输入）
    ↓
config_template.yaml (统一数据源)
    ↓
generate.py (编排器 - 逐页分发数据)
    ↓
loaders/ (35个装载器 - 纯渲染引擎)
    ↓ 每个装载器: load_slide(ctx, data)
    ↓
输出PPT
```

**关键约束：**
- ✅ **装载器是无状态的、完全参数化的**：所有数据都通过`data`参数传入
- ✅ **数据与渲染逻辑分离**：业务数据在config_template.yaml中管理
- ✅ **高内聚**：每个装载器自包含一张图的完整样式和布局
- ✅ **低耦合**：装载器间无依赖，只依赖shared工具集

---

## 📁 项目结构

```
skills/pptx/
├── gtm-architecture/
│   ├── loaders/                   # 35个装载器模块 (可复用技能库)
│   │   ├── __init__.py           # 装载器注册表
│   │   ├── gm_01_positioning_statement.py
│   │   ├── gm_02_buyer_journey.py
│   │   ├── gm_03_competitor_matrix.py
│   │   ├── ...
│   │   └── gm_35_assumption_sensitivity.py
│   │
│   └── SKILL.md                  # GTM技能文档
│
├── shared/                        # 共用工具包 (可复用)
│   ├── __init__.py
│   └── renderer_utils.py          # 通用render函数
│       ├── textbox()
│       ├── shape_rect()
│       ├── render_two_col_list()
│       ├── render_three_col_list()
│       ├── render_horizontal_flow()
│       ├── render_table_grid()
│       └── render_matrix_2d()
│
projects/gtm-a-deck-demo-full/
├── generate.py                    # 项目编排脚本
│   ├── 读取config_template.yaml
│   ├── 动态加载 skills/pptx/gtm-architecture/loaders/*
│   └── 逐页调用：add_cover() → add_chapter() → loader(ctx, data) → add_back()
│
├── data/                          # 项目数据配置
│   └── config_template.yaml       # 所有业务数据（项目特定输入）
│       ├── g1_positioning:        # G1市场定位
│       │   ├── gm_01_positioning_statement: {...}
│       │   ├── gm_02_buyer_journey: {...}
│       │   ...
│       ├── g2_buyer_value:        # G2买方价值
│       ├── ...
│       └── g8_risk_management:    # G8风险管理
│
└── README.md                      # 项目说明
```

**关键区别：**
- `skills/` 下的 **loaders** 和 **shared** = 可复用技能库
- `projects/` 下的 **generate.py** + **data/** = 项目实例

---

## 🔧 装载器设计规范

### 装载器接口（Loader Protocol）

每个装载器都遵循统一的接口规范：

```python
def load_slide(ctx, data):
    """
    装载一张图表
    
    Args:
        ctx: BuildContext (由pptx_lib提供)
            - ctx.prs: Presentation对象
            - ctx.add_slide(): 添加幻灯片
        
        data: dict (来自config_template.yaml)
            {
                "title": "图表标题",
                "subtitle": "副标题",
                "content": {
                    # 图表特定的内容结构
                    # 完全由装载器定义和解析
                }
            }
    
    Returns:
        slide: 生成的Slide对象
    """
    
    # 1. 获取布局
    slide = add_content_slide(ctx)
    
    # 2. 设置标题和副标题
    header(slide, data["title"])
    set_subtitle(slide, data["subtitle"])
    
    # 3. 基于data["content"]进行渲染
    render_core_content(slide, data["content"])
    
    return slide
```

### 装载器实现示例

**GM-01 Positioning Statement**

```python
# loaders/gm_01_positioning_statement.py

def load_slide(ctx, data):
    slide = add_content_slide(ctx)
    header(slide, data["title"])
    set_subtitle(slide, data["subtitle"])
    
    # 从data中获取内容（数据驱动）
    items = [
        ("Target", data["content"]["target"], COLOR_CYAN),
        ("Problem", data["content"]["problem"], COLOR_LIGHT),
        ("Product", data["content"]["product"], COLOR_CYAN),
        ("Differentiator", data["content"]["differentiator"], COLOR_BRAND),
        ("Category", data["content"]["category"], COLOR_DARK),
    ]
    
    # 基于items列表进行布局
    x = MARGIN_LEFT
    for label, description, bg_color in items:
        shape_rect(slide, x, TOP_Y, BOX_W, BOX_H, bg_color)
        textbox(slide, x, TOP_Y, BOX_W, BOX_H/2, label, ...)
        textbox(slide, x, TOP_Y + BOX_H/2, BOX_W, BOX_H/2, description, ...)
        x += BOX_W + SPACING
    
    return slide
```

### 装载器分类

35个装载器分为8大组：

| 分组 | 代码范围 | 用途 | 装载器数 |
|------|---------|------|---------|
| G1 | GM-01~04 | 市场定位 | 4 |
| G2 | GM-05~08 | 买方价值 | 4 |
| G3 | GM-09~12 | 解决方案 | 4 |
| G4 | GM-13~17 | 实施执行 | 5 |
| G5 | GM-18~22 | GTM策略 | 5 |
| G6 | GM-23~25 | 产品特性 | 3 |
| G7 | GM-26~30 | 价值实现 | 5 |
| G8 | GM-31~35 | 风险管理 | 5 |

---

## 📊 数据配置格式

**config_template.yaml** 包含所有业务数据：

```yaml
g1_positioning:
  gm_01_positioning_statement:
    title: "GM-01 Positioning Statement | A-Deck 市场定位"
    subtitle: "..."
    content:
      target: "目标客户描述"
      problem: "问题描述"
      product: "产品描述"
      differentiator: "差异化"
      category: "类别"

  gm_02_buyer_journey:
    title: "GM-02 Buyer Journey | 采购方决策路径"
    content:
      stages:
        - label: "Stage 1"
          desc: "..."
          triggers: [...]
        - label: "Stage 2"
          ...

# 后续其他分组...
```

**关键优势：**
- 📝 所有数据集中管理，易于维护
- 🔄 修改数据不需要改动装载器代码
- 📚 可以快速生成不同内容的PPT（只需换config）
- 🧪 便于数据验证和测试

---

## 🚀 快速启动

### 1. 安装依赖

```bash
cd /Volumes/work/Workspace/A-Deck
source .venv/bin/activate

# 确保安装了必要的包
pip install pptx pyyaml
```

### 2. 创建/更新装载器

在 `skills/pptx/gtm-architecture/loaders/` 中新建装载器文件 `gm_XX_*.py`，遵循Loader Protocol：

```python
# skills/pptx/gtm-architecture/loaders/gm_XX_chart_name.py
def load_slide(ctx, data):
    # 实现该装载器的渲染逻辑
    pass
```

### 3. 配置数据

编辑 `data/config_template.yaml`，为该装载器添加数据：

```yaml
gX_group_name:
  gm_XX_loader_name:
    title: "..."
    content: {...}
```

### 4. 运行生成

```bash
cd projects/gtm-a-deck-demo-full
python3 generate.py
```

输出：`a-deck-gtm-full-demo.pptx`

---

## ✅ 装载器检查清单

每个装载器创建时，确保：

- [ ] 位置：`skills/pptx/gtm-architecture/loaders/gm_<序号>_<描述>.py`
- [ ] 包含 `load_slide(ctx, data)` 函数
- [ ] 从 `data` 获取所有业务数据，不硬编码
- [ ] 使用 `shared/renderer_utils.py` 中的渲染函数（导入：`from renderer_utils import ...`）
- [ ] 添加对应的config entry到 `projects/gtm-a-deck-demo-full/data/config_template.yaml`
- [ ] 在 `projects/gtm-a-deck-demo-full/generate.py` 的groups列表中注册

---

## 🔍 调试和扩展

### 添加新装载器

1. 创建 `skills/pptx/gtm-architecture/loaders/gm_NN_chart_name.py`
2. 实现 `load_slide(ctx, data)` 函数
3. 在 `projects/gtm-a-deck-demo-full/data/config_template.yaml` 中添加对应数据设置
4. 在 `projects/gtm-a-deck-demo-full/generate.py` 的 groups 列表中添加条目
5. 运行 `python3 projects/gtm-a-deck-demo-full/generate.py` 测试

### 添加新的render函数

如果需要新的渲染模式（如流程图、热力图等）：

1. 在 `skills/pptx/shared/renderer_utils.py` 中实现函数
2. 在 `skills/pptx/shared/__init__.py` 中导出
3. 在相关装载器中导入使用：`from renderer_utils import render_new_chart`

### 测试单张幻灯片

```python
# test_loader.py
from loaders import gm_01_positioning_statement
from pptx import Presentation

template = "..."
prs = Presentation(template)

data = {
    "title": "Test Title",
    "content": {...}
}

# Mock ctx object for testing
class MockCtx:
    def __init__(self, prs):
        self.prs = prs

ctx = MockCtx(prs)
slide = gm_01_positioning_statement.load_slide(ctx, data)
```

---

## 📌 最佳实践

1. **数据参数化**：永远不要在装载器中硬编码业务数据
2. **统一布局**：使用 `shared/renderer_utils.py` 中的render函数保持一致性
3. **清晰注释**：每个装载器的 `load_slide()` 必须有清晰的docstring
4. **颜色管理**：使用集中定义的颜色常量
5. **尺寸单位**：统一使用 `Inches()` 和 `Pt()`，避免混乱

---

## 🎯 后续工作

- [ ] 实现所有35个装载器 (当前仅GM-01作为示例)
- [ ] 补充完整的config_template.yaml数据
- [ ] 为每个render函数编写使用示例
- [ ] 创建单元测试套件
- [ ] 性能优化（特别是大型表格渲染）
