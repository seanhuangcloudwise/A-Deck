# Master Library Schema

## manifest.json

```json
{
  "masterId": "cloudwise-ai-brochure-v1",
  "displayName": "Cloudwise AI 产品表皮书母版",
  "sceneSlug": "product-brochure",
  "sourceFile": "Cloudwise AI 创新产品体系-方案.pptx",
  "addedAt": "2026-03-22",
  "layoutCount": 12,
  "masterCount": 1,
  "fonts": ["微软雅黑", "Arial", "Calibri"],
  "topColors": ["A5A7AA", "FFFFFF", "000000", "FFC000", "FF0000", "00CCD7"],
  "layoutNames": ["Title Slide", "Section Divider", "Two Column", "Comparison"],
  "notes": "Extracted from uploaded PPT and confirmed by user"
}
```

## preview.md

```markdown
# {Display Name}

- master-id: `{master-id}`
- scene: `{scene-slug}`
- source: `{source-file}`
- layout count: {n}

## Key Layouts

1. {layout name} — {usage suggestion}
2. {layout name} — {usage suggestion}

## Visual Signature

- Main colors: {hex list}
- Fonts: {font list}
- Style tags: {tags}
```

## Asset Copy Rules

- Copy all `ppt/slideMasters/slideMaster*.xml` -> `assets/slideMasters/`
- Copy all `ppt/slideLayouts/slideLayout*.xml` -> `assets/slideLayouts/`
- Copy `ppt/theme/theme1.xml` if exists -> `assets/theme/`
- Never write if user selected "跳过"
- Never write until display name and master-id are confirmed

## Runtime Integration Rules (Master + Loader)

Use this checklist when onboarding a new master or extending diagram loader skills.

### 1. Master Runtime Contract

- Generation must call `build_pptx(template, output, my_slides, template_spec_path)`.
- `template` and `template_spec_path` must come from the same master folder.
- `layout.names` and `layout.indices` in spec must map to real layouts in master PPTX.

### 2. Color Source of Truth

- Effective theme colors are read from PPTX `ppt/theme/theme*.xml` via `extract_theme_colors()`.
- `infrastructure_colors.palette` only provides aliases/compatibility keys on top of theme.
- Loader brand/style colors must use `ctx.colors` / `ctx.palette`.
- Do not hardcode brand RGB values in loaders.

### 3. Loader Protocol

- Loader input contract: `loader(ctx, data)`.
- All business content comes from external YAML config.
- Titles/subtitles should use placeholders first.
- Keep orchestration in project `generate.py`, reusable rendering in `skills/pptx/.../loaders/`.

### 4. Cross-Master Scaling

- If loaders do internal coordinate scaling, set `ctx.scale_x = 1.0` to avoid double-scaling.
- Validate right-edge overflow after generation.

### 5. Mandatory Verification Matrix

For each important master/loader change, verify at least:

- Slides count expected.
- Theme hash match (`verify_pptx` theme match true).
- Right overflow count is zero (or explicitly accepted).
- Layout/title placeholders render as expected.

### 6. Recommended Test Scope

- Skill families: GTM + Roadmap + TOGAF.
- Masters: dark-cloudwise-green, light-cloudwise-cyan, light-cloudwise-purple.
- Save outputs by (skill, master) pair for visual comparison.
