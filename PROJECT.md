# A-Deck — Project Overview

This repository hosts A-Deck implementation assets, scripts, and architecture knowledge packs. A-Deck is an enterprise-grade PPTX generation agent that delivers 90-point presentation quality.

本仓库用于承载 A-Deck 的实现资产、脚本与架构知识库。A-Deck 定位"做90分的PPT"。

## Canonical Specification / 主规范

- Repository mirror (versioned): [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md)
- Runtime source (global): `~/Library/Application Support/Code/User/prompts/ppt-maker.agent.md`

Policy:
- The global agent file is runtime source.
- 本仓库中的 [docs/ppt-maker-agent-spec.md](docs/ppt-maker-agent-spec.md) 是可版本化镜像，用于协作与评审。

## Core Structure / 核心结构

```text
A-Deck/
├── docs/
│   └── ppt-maker-agent-spec.md
├── skills/
│   └── pptx/
│       ├── SKILL.md
│       ├── scripts/
│       ├── knowledge/
│       ├── master-library/
│       └── togaf-architecture/
├── projects/
│   ├── capability-map-test/
│   ├── service-interaction-test/
│   ├── function-capability-mapping-test/
│   ├── business-process-test/
│   └── business-process-full-deck/
└── output/
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
- Use [skills/pptx/knowledge/_index.md](skills/pptx/knowledge/_index.md) as the naming reference for knowledge scenes.

## QA Baseline / QA基线

- Content extraction check (markitdown)
- Visual rendering check (PDF/JPEG)
- Structure integrity check (XML relation/slide reference)

QA commands remain in [skills/pptx/SKILL.md](skills/pptx/SKILL.md).
