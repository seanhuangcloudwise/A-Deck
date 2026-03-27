#!/usr/bin/env python3
"""Generate compact BPMN deck (10 business slides only) using light-cloudwise-cyan master."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
PROJ = Path(__file__).resolve().parent

sys.path.insert(0, str(PROJ))

import generate as g  # noqa: E402
from pptx_lib import build_pptx, verify_pptx  # noqa: E402
from renderer_utils import configure_theme  # noqa: E402


g.TEMPLATE = ROOT / "skills" / "pptx" / "master-library" / "light-cloudwise-cyan" / "cloudwise-master.pptx"
g.TEMPLATE_SPEC = ROOT / "skills" / "pptx" / "master-library" / "light-cloudwise-cyan" / "cloudwise-spec.yaml"
g.OUTPUT = PROJ / "bpmn-cyan-demo-compact-10slides.pptx"


def my_slides_compact(ctx):
    configure_theme(ctx.colors, ctx.template_spec)
    cfg = g.load_config(g.CONFIG_FILE)

    # Compact mode: only BP-01..BP-10 business slides, no cover/chapter/back slides.
    for section in cfg.get("sections", []):
        for loader_name in g.sort_loader_names(list(section.get("slides", {}).keys())):
            loader_fn = g.LOADER_REGISTRY.get(loader_name)
            if not loader_fn:
                print(f"  [skip] {loader_name} not registered")
                continue
            print(f"  [slide] {loader_name}")
            loader_fn(ctx, section["slides"][loader_name])
            print("         OK")


def main():
    print("=" * 60)
    print("BPMN Compact Cyan 生成器")
    print("母版: light-cloudwise-cyan")
    print("模式: 仅10张业务页（无封面/章节/结束页）")
    print("=" * 60)

    print("\n[1] 加载装载器...")
    g.load_all_loaders()
    print(f"    已注册 {len(g.LOADER_REGISTRY)} 个装载器\n")

    print("[2] 生成 PPT...")
    build_pptx(g.TEMPLATE, g.OUTPUT, my_slides_compact, g.TEMPLATE_SPEC)
    print(f"\n    输出: {g.OUTPUT}")

    print("\n[3] 移除阴影特效...")
    g._strip_shadows_from_pptx(g.OUTPUT)

    print("\n[4] 验证...")
    verify_pptx(g.OUTPUT, g.TEMPLATE)
    print("    验证通过")


if __name__ == "__main__":
    main()
