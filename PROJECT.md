# A-Deck — Project Overview

This repository hosts A-Deck implementation assets, scripts, and architecture knowledge packs. A-Deck is an enterprise-grade PPTX generation agent that delivers 90-point presentation quality.

本仓库用于承载 A-Deck 的实现资产、脚本与架构知识库。A-Deck 定位"做90分的PPT"。

## Canonical Specification / 主规范

- **Workspace agent (primary)**: [.github/prompts/ppt-maker.agent.md](.github/prompts/ppt-maker.agent.md) — Copilot Agent，随仓库版本化，可直接在 VS Code 中调用
- Repository spec mirror: [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md)
- Global fallback: `~/Library/Application Support/Code/User/prompts/ppt-maker.agent.md`

Policy:
- `.github/prompts/ppt-maker.agent.md` 是工作区级主源，随仓库版本化管理。
- 全局文件保留作为跨工作区后备，与工作区文件保持同步。
- 修改 agent 规范时，同步更新工作区文件和全局文件。

## Core Structure / 核心结构

```text
A-Deck/
├── docs/
│   └── ppt-maker-agent-spec.md
├── skills/
│   └── pptx/
│       ├── SKILL.md
│       ├── scripts/              # 共享渲染库 pptx_lib.py + office 工具
│       ├── shared/               # 跨 loader 公共工具 renderer_utils.py
│       ├── master-library/       # 品牌母版资产（3 色系）
│       ├── togaf-architecture/   # TOGAF 图形 Skill（BA/AA/TA loaders）
│       ├── gtm-architecture/     # GTM 图形 Skill
│       ├── roadmap-architecture/ # 路线图图形 Skill
│       └── XSean/                # XSean 专属图形域（diagrams + loaders）
├── projects/
│   ├── ppt-maker-intro-cloudwise-2025/  # Cloudwise 自我介绍（主力项目，多母版）
│   ├── business-process-full-deck/      # 业务流程泳道图全量演示
│   ├── togaf-architecture-full-demo/    # TOGAF 全架构演示
│   ├── gtm-a-deck-demo-full/            # GTM 全流程演示
│   ├── roadmap-architecture-full-demo/  # 路线图架构全量演示
│   └── ...                              # 其他测试 & 验证项目
└── output/                       # 学习产物 & QA 中间产物
```

## Workflow Coverage / 工作流覆盖

- W1 Create from Scratch / 从零创建
- W2 Edit Existing PPTX / 编辑现有PPT
- W3 Analyze PPTX / 分析PPT
- W4 Template-based Generation / 模板化生成
- W5 Learn from PPTX / 从PPT学习
- W6 Master Extraction / 母版提取

Detailed functional contracts are maintained in [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md).

详细功能契约以 [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md) 为准。

## Collaboration Rules / 协作规则

- Keep [skills/pptx/SKILL.md](skills/pptx/SKILL.md) concise as an operational quick reference.
- Maintain full product requirement and functional descriptions in [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md).
- Style conventions and diagram specs live in `skills/pptx/XSean/` (XSean domain) and loader directories.

## QA Baseline / QA基线

- Content extraction check (markitdown)
- Visual rendering check (PDF/JPEG)
- Structure integrity check (XML relation/slide reference)

QA commands remain in [skills/pptx/SKILL.md](skills/pptx/SKILL.md).
