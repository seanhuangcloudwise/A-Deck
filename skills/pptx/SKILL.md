# PPTX Skill

Quick reference for A-Deck PPT Maker operations.

Canonical product requirement and full functional descriptions:
- [docs/ppt-maker-agent-spec.md](../../docs/ppt-maker-agent-spec.md)

运行时主源（全局）：
- `~/Library/Application Support/Code/User/prompts/ppt-maker.agent.md`

This file is intentionally concise. It contains command-level operations and QA commands.
本文件保持精简，仅保留命令级操作与 QA 入口。

## Quick Reference

| Task | Command |
|------|---------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | See [Editing Workflow](#editing-workflow) |
| Create from scratch | Use PptxGenJS (see agent instructions) |

## Workflow Contract Summary / 工作流契约摘要

- W1 Create: requirements -> outline -> design -> generation -> QA
- W2 Edit: analyze -> unpack -> edit -> clean/pack -> QA
- W3 Analyze: text + visuals + structural checks
- W4 Template: layout inventory -> content mapping -> replacement -> QA
- W5 Learn: extract style -> confirm -> persist
- W6 Master Extract: candidate summary -> gated confirmation -> deposit

Full bilingual details are maintained in [docs/ppt-maker-agent-spec.md](../../docs/ppt-maker-agent-spec.md).

## Dependencies

Install before using Edit/Analyze workflows:

```bash
# Python dependencies
pip install "markitdown[pptx]" Pillow defusedxml

# Node.js dependencies
npm install -g pptxgenjs

# Icon support (for Create workflow)
npm install react react-dom react-icons @resvg/resvg-js

# System tools (macOS)
brew install libreoffice poppler
```

## Reading Content

```bash
# Full text extraction (ordered by slide)
python -m markitdown presentation.pptx

# Visual overview thumbnail grid
python skills/pptx/scripts/thumbnail.py presentation.pptx

# Raw XML (for debugging)
python skills/pptx/scripts/office/unpack.py presentation.pptx unpacked_view/
```

## Editing Workflow

1. Analyze template:
   ```bash
   python skills/pptx/scripts/thumbnail.py template.pptx
   python -m markitdown template.pptx
   ```

2. Unpack:
   ```bash
   python skills/pptx/scripts/office/unpack.py template.pptx unpacked/
   ```

3. Plan slide mapping — review `unpacked/ppt/presentation.xml` for `<p:sldIdLst>`

4. Structural changes (do all BEFORE content edits):
   ```bash
   # Duplicate a slide
   python skills/pptx/scripts/add_slide.py unpacked/ slide2.xml

   # Create from layout
   python skills/pptx/scripts/add_slide.py unpacked/ slideLayout2.xml

   # Delete: remove <p:sldId> from presentation.xml
   # Reorder: rearrange <p:sldId> elements in presentation.xml
   ```

5. Edit slide content in `unpacked/ppt/slides/slide{N}.xml`
   - Use subagents to edit multiple slides in parallel if available
   - Bold headers: `b="1"` on `<a:rPr>`
   - Multi-item: separate `<a:p>` per item (never concatenate)
   - Smart quotes: `&#x201C;` `&#x201D;` `&#x2018;` `&#x2019;`

6. Clean:
   ```bash
   python skills/pptx/scripts/clean.py unpacked/
   ```

7. Pack:
   ```bash
   python skills/pptx/scripts/office/pack.py unpacked/ output.pptx --original template.pptx
   ```

## Creating from Scratch

See `pptxgenjs.md` for detailed PptxGenJS code patterns, or refer to the PPT Maker agent instructions.

```bash
# After writing generate.js:
mkdir -p output
node generate.js
```

## QA (Required)

```bash
# Content QA: check for placeholder/unfinished text
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"

# Visual QA: convert to high-resolution JPEG
python skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
# Creates: slide-01.jpg, slide-02.jpg, ...

# Re-render specific slides after fix:
pdftoppm -jpeg -r 150 -f 2 -l 4 output.pdf slide-fixed
```

**Verification loop:**
1. Generate → Convert → Inspect (use subagent for fresh eyes)
2. List issues, even minor ones
3. Fix → Re-verify affected slides only
4. Repeat until zero new issues

## Scripts Reference

| Script | Usage |
|--------|-------|
| `scripts/office/unpack.py` | `python scripts/office/unpack.py input.pptx unpacked/` |
| `scripts/office/pack.py` | `python scripts/office/pack.py unpacked/ output.pptx --original input.pptx` |
| `scripts/office/soffice.py` | `python scripts/office/soffice.py --headless --convert-to pdf file.pptx` |
| `scripts/clean.py` | `python scripts/clean.py unpacked/` |
| `scripts/add_slide.py` | `python scripts/add_slide.py unpacked/ slide2.xml` |
| `scripts/thumbnail.py` | `python scripts/thumbnail.py input.pptx [prefix] [--cols N]` |

## Knowledge Base

Personal style knowledge is stored in `skills/pptx/knowledge/` and organized by scene.

### Scene Management

```bash
# View registered scenes
cat skills/pptx/knowledge/_index.md

# View style preferences for a scene
cat skills/pptx/knowledge/product-roadmap/style-profile.md

# View saved slide structure templates for a scene
cat skills/pptx/knowledge/product-roadmap/slide-structures.md

# View session history for a scene
cat skills/pptx/knowledge/product-roadmap/session-log.md
```

### Add a New Scene

```bash
# 1. Register in index
#    Edit skills/pptx/knowledge/_index.md — add a row to the Registered Scenes table

# 2. Create scene directory and files
mkdir skills/pptx/knowledge/{your-slug}
# Copy the three file templates from skills/pptx/knowledge/_schema.md
```

### Trigger Knowledge Learning (Workflow 5)

```
# In the PPT Maker agent chat, attach a .pptx file and say:
"学习这个" / "从这个PPT提取风格" / "learn from this"

# Agent will:
# 1. Ask you which scene this belongs to
# 2. Extract 6 dimensions (palette, typography, structure, style, density, audience)
# 3. Show a summary table for your confirmation
# 4. On confirmation: write to the scene's knowledge files
```

### Trigger Session Save (after PPT generation)

```
# After PPT Maker finishes and passes QA, it will show a Session Summary.
# Reply "保存" to persist this session's style choices to the knowledge base.
# The agent updates: style-profile.md (palette/font counts), 
#   slide-structures.md (template usage), session-log.md (new row)
```

### Knowledge File Schema

See `skills/pptx/knowledge/_schema.md` for the exact format specification
used when Agent reads or writes knowledge files.

## Master Library

Reusable masters are stored in `skills/pptx/master-library/`.

### Extract Master from Uploaded PPT (Workflow 6)

```
# In the PPT Maker agent chat, attach a .pptx file and say:
"提取母版" / "加入母版库" / "extract masters"

# Agent flow:
# 1. Unpack and analyze slideMasters/slideLayouts/theme
# 2. Show candidate summary (count/colors/fonts/layouts)
# 3. Ask mandatory gate: 是否沉淀到母版库？（确认/跳过）
# 4. Ask user-defined display name
# 5. Ask and confirm master-id (kebab-case)
# 6. Item-level confirmation (M1-M5)
# 7. Write to master-library only after confirmation
```

### Master Deposit Gate (Mandatory)

- No write before explicit user confirmation
- If user chooses `跳过`, do not write any master files
- Display name must be provided by user
- `master-id` conflicts must be resolved and reconfirmed (`-v2`, `-v3`, ...)

### Master Library Files

```
skills/pptx/master-library/
├── _index.md
├── _schema.md
└── {master-id}/
   ├── manifest.json
   ├── preview.md
   └── assets/
```

### Use a Master While Creating PPT

During Create/Template workflow, user can explicitly select a master from `_index.md`.
If selected, agent should prefer that master's layout style before applying default design templates.

## Master + Loader Implementation Mechanism (Extension Guide)

This section defines the required mechanism to safely extend both master templates and new diagram loader skills.

### 1. Runtime Contract (Must Follow)

1. Always generate through `build_pptx(template, output, my_slides, template_spec_path)`.
2. Always pass both master PPTX and matching `cloudwise-spec.yaml` from the same master folder.
3. Loader rendering input must be `ctx` + external data only; no business data hardcoding in loaders.
4. Placeholder-first rule remains mandatory for title/subtitle.

### 2. Color Source of Truth (Must Follow)

Color resolution chain is:

1. Base theme from master PPTX theme XML via `extract_theme_colors(prs)`.
2. Optional alias/compatibility overrides from `template_spec.infrastructure_colors.palette`.
3. Loader usage through `ctx.colors` and `ctx.palette`.

Rules:

1. Brand/style colors must come from active master (`ctx.colors` / `ctx.palette`).
2. Do not hardcode brand RGB in loaders.
3. Semantic reserved colors are allowed only when diagram spec explicitly requires them (for example RACI semantics), and should still prefer theme-derived mapping when possible.
4. If a master's visual color differs from expected style, check PPTX `ppt/theme/theme*.xml` first, not only YAML comments.

### 3. Loader Skill Protocol (Must Follow)

1. File placement:
   1. Reusable loaders under `skills/pptx/{domain}/loaders/`.
   2. Project orchestrator under `projects/{project-name}/generate.py`.
2. Entry signature: `def load_slide(ctx, data): ...` (or domain-equivalent loader function with same contract).
3. Data-driven only: all text/items/metrics come from config YAML.
4. Shared primitives should come from shared renderer helpers (`renderer_utils`, `pptx_lib`) where possible.

### 4. Layout Selection Mechanism

1. Prefer `layout_by_names(prs, names, fallback_index)` with explicit, precise name arrays.
2. Names and fallback indices should be read from `template_spec.layout.names` and `template_spec.layout.indices` when available.
3. Avoid ambiguous short substrings that can match the wrong layout.

### 5. Scaling Mechanism Across Masters

1. If a skill uses legacy fixed canvas coordinates, implement internal scale mapping in loader/common helpers.
2. Avoid double scaling:
   1. If loaders already scale internally, neutralize global horizontal scaling (`ctx.scale_x = 1.0`) in orchestrator.
   2. Otherwise rely on framework scaling only.
3. Validate with right-edge overflow check on all target masters.

### 6. New Master Onboarding Checklist

When adding a new master to `skills/pptx/master-library/{master-id}/`:

1. Prepare files: `cloudwise-master.pptx`, `cloudwise-spec.yaml`, `preview.md`, `manifest.json`, extracted assets.
2. Ensure `cloudwise-spec.yaml` layout names/indices map to real layouts in the PPTX.
3. Ensure theme XML colors in PPTX match intended palette.
4. Register master in `skills/pptx/master-library/_index.md`.
5. Run at least one full generation test for each representative skill family (for example GTM, Roadmap, TOGAF).

### 7. New Diagram Skill Onboarding Checklist

When adding a new diagram skill or loader set:

1. Define loader protocol and data schema first.
2. Keep render logic in skill loader modules; keep orchestration in project `generate.py`.
3. Use placeholder-first title/subtitle handling.
4. Use theme-derived colors only (except documented semantic reserved colors).
5. Add explicit loader registration and deterministic load order.
6. Validate on all supported masters and report:
   1. slides count,
   2. theme hash match,
   3. right overflow count,
   4. obvious placeholder/layout mismatches.

### 8. Regression Test Matrix (Recommended)

For every significant master or loader change, run matrix tests:

1. Skill families: GTM + Roadmap + TOGAF (or project-relevant set).
2. Masters: `dark-cloudwise-green`, `light-cloudwise-cyan`, `light-cloudwise-purple`.
3. Output files must be isolated per (skill, master) pair for easy QA comparison.

## TOGAF 4-Layer Skills

Architecture diagram capability is split into four reusable skills:

- `skills/pptx/togaf-architecture/business-architecture/SKILL.md`
- `skills/pptx/togaf-architecture/application-architecture/SKILL.md`
- `skills/pptx/togaf-architecture/data-architecture/SKILL.md`
- `skills/pptx/togaf-architecture/technology-architecture/SKILL.md`

Routing priority:

1. If request is strategy/process/role/value oriented, route to Business Architecture first.
2. If request is app interaction/API/integration oriented, route to Application Architecture.
3. If request is data domain/lineage/lifecycle oriented, route to Data Architecture.
4. If request is deployment/platform/network/security-zone oriented, route to Technology Architecture.

Global architecture constraints (mandatory across all 4 skills):

1. Title/subtitle must use layout placeholders first.
2. Rounded rectangle corner radius must be small by default.
3. No decorative-only shapes or lines; every connector must carry semantics.
