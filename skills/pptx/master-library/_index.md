# Master Library Index

Master library stores reusable PPT masters extracted from uploaded presentations.

## Registered Masters

| master-id | Display Name | Scene slug | Source file | Layout count | Added | Status |
|-----------|--------------|------------|-------------|--------------|-------|--------|
| `light-cloudwise-cyan` | cloudwise 2025 (Light Cyan) | `product-brochure` | projects/ppt-maker-intro-cloudwise-2025/ppt-maker-agent-self-intro-cloudwise.pptx | 12 | 2026-03-22 | active |
| `dark-cloudwise-green` | cloudwise dark green | `roadmap-architecture` | /Volumes/work/04 产品体系/宣发资料/EAI/市场胶片/0123/dark-cloudwise-green1.pptx | 12 | 2026-03-26 | active |
| `light-cloudwise-purple` | cloudwise purple light | `overall-intro` | /Volumes/work/04 产品体系/宣发资料/整体介绍/模版/颜色0326.pptx | 11 | 2026-03-26 | active |

## Naming Rules

- `Display Name`: user-defined (supports Chinese)
- `master-id`: lowercase kebab-case English slug used as folder name
- If conflict, suggest `-v2`, `-v3` and require user confirmation before write

## Directory Structure

Each master is stored at:

```
skills/pptx/master-library/{master-id}/
├── manifest.json      # metadata and mapping
├── preview.md         # preview notes and layout summary
└── assets/
    ├── slideMasters/  # copied slideMaster*.xml
    ├── slideLayouts/  # copied slideLayout*.xml
    └── theme/         # copied theme1.xml if available
```

## Write Gate (Mandatory)

Before writing any master:
1. Show candidate extraction summary
2. Ask: "检测到可沉淀母版，是否沉淀到母版库？（确认/跳过）"
3. Ask for user-defined `Display Name`
4. Generate and confirm `master-id`
5. Only then write files and append index row
