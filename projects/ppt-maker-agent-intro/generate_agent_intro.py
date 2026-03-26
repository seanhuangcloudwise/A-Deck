#!/usr/bin/env python3
"""Skill-driven PPT workflow entrypoint for the PPT Maker Agent intro project.

This script intentionally reuses the local Anthropic-style pptx skill already
present in the workspace under skills/pptx instead of generating slides with a
custom python-pptx implementation.

Supported workflow:
1. Analyze template with thumbnail.py + markitdown
2. Unpack template with office/unpack.py
3. Add slides via add_slide.py and register them in presentation.xml
4. Clean orphaned files with clean.py
5. Pack output with office/pack.py

The actual slide text/layout editing should happen in the unpacked XML files,
which matches the template-editing workflow documented in skills/pptx/editing.md.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


WORKSPACE_ROOT = Path("/Volumes/work/Workspace/A-Deck")
PROJECT_DIR = WORKSPACE_ROOT / "projects" / "ppt-maker-agent-intro"
SKILL_DIR = WORKSPACE_ROOT / "skills" / "pptx"

TEMPLATE_PATH = Path("/Volumes/work/04 产品体系/宣发资料/AI/Cloudwise AI 创新产品体系-方案.pptx")
UNPACKED_DIR = PROJECT_DIR / "work" / "unpacked"
ANALYSIS_DIR = PROJECT_DIR / "work" / "analysis"
OUTPUT_PATH = PROJECT_DIR / "ppt-maker-agent-intro-skill-driven.pptx"

THUMBNAIL_SCRIPT = SKILL_DIR / "scripts" / "thumbnail.py"
UNPACK_SCRIPT = SKILL_DIR / "scripts" / "office" / "unpack.py"
ADD_SLIDE_SCRIPT = SKILL_DIR / "scripts" / "add_slide.py"
CLEAN_SCRIPT = SKILL_DIR / "scripts" / "clean.py"
PACK_SCRIPT = SKILL_DIR / "scripts" / "office" / "pack.py"


def run_python(script: Path, *args: str, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    """Run one of the local skill scripts with the current Python interpreter."""
    command = [sys.executable, str(script), *[str(arg) for arg in args]]
    return subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=capture_output,
    )


def ensure_directories() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    UNPACKED_DIR.parent.mkdir(parents=True, exist_ok=True)


def analyze_template() -> None:
    """Generate reusable analysis artifacts using the existing pptx skill tools."""
    ensure_directories()

    thumbnail_prefix = ANALYSIS_DIR / "template-thumbnails"
    run_python(THUMBNAIL_SCRIPT, TEMPLATE_PATH, thumbnail_prefix, "--cols", "4")

    markitdown_output = subprocess.run(
        [sys.executable, "-m", "markitdown", str(TEMPLATE_PATH)],
        check=True,
        text=True,
        capture_output=True,
    )
    (ANALYSIS_DIR / "template.md").write_text(markitdown_output.stdout, encoding="utf-8")

    print(f"Analysis written to {ANALYSIS_DIR}")
    print(f"- Thumbnails prefix: {thumbnail_prefix}")
    print(f"- Markitdown text: {ANALYSIS_DIR / 'template.md'}")


def unpack_template() -> None:
    """Unpack the template using the skill implementation, not custom XML code."""
    ensure_directories()
    run_python(UNPACK_SCRIPT, TEMPLATE_PATH, UNPACKED_DIR)
    print(f"Unpacked template at {UNPACKED_DIR}")


def insert_slide_id(presentation_xml: Path, slide_id_xml: str) -> None:
    """Insert the suggested <p:sldId> emitted by add_slide.py into presentation.xml."""
    content = presentation_xml.read_text(encoding="utf-8")
    if slide_id_xml in content:
        return

    replacement = f"  {slide_id_xml}\n    </p:sldIdLst>"
    updated = content.replace("</p:sldIdLst>", replacement, 1)
    if updated == content:
        raise RuntimeError("Could not find </p:sldIdLst> in presentation.xml")
    presentation_xml.write_text(updated, encoding="utf-8")


def add_slide(source: str) -> None:
    """Reuse add_slide.py, then register the produced slide in presentation.xml."""
    if not UNPACKED_DIR.exists():
        raise FileNotFoundError(
            f"{UNPACKED_DIR} does not exist. Run the 'unpack' command first."
        )

    result = run_python(ADD_SLIDE_SCRIPT, UNPACKED_DIR, source, capture_output=True)
    stdout = result.stdout

    match = re.search(r'(<p:sldId id="\d+" r:id="rId\d+"/>)', stdout)
    if match is None:
        raise RuntimeError(
            "add_slide.py did not emit a slide id snippet. Output was:\n" + stdout
        )

    presentation_xml = UNPACKED_DIR / "ppt" / "presentation.xml"
    insert_slide_id(presentation_xml, match.group(1))

    print(stdout.strip())
    print("Registered new slide in ppt/presentation.xml")


def clean_unpacked() -> None:
    """Run the skill cleanup pass."""
    if not UNPACKED_DIR.exists():
        raise FileNotFoundError(
            f"{UNPACKED_DIR} does not exist. Run the 'unpack' command first."
        )
    run_python(CLEAN_SCRIPT, UNPACKED_DIR)


def pack_output(output_path: Path = OUTPUT_PATH) -> None:
    """Pack the current unpacked directory back into a PPTX via the skill script."""
    if not UNPACKED_DIR.exists():
        raise FileNotFoundError(
            f"{UNPACKED_DIR} does not exist. Run the 'unpack' command first."
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_python(PACK_SCRIPT, UNPACKED_DIR, output_path, "--original", TEMPLATE_PATH)
    print(f"Packed PPTX to {output_path}")


def run_qa(pptx_path: Path = OUTPUT_PATH) -> None:
    """Run the minimum QA pass recommended by the skill."""
    if not pptx_path.exists():
        raise FileNotFoundError(f"{pptx_path} does not exist.")

    markitdown_output = subprocess.run(
        [sys.executable, "-m", "markitdown", str(pptx_path)],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    qa_path = ANALYSIS_DIR / "output-qa.md"
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(markitdown_output, encoding="utf-8")

    placeholder_hits = re.findall(
        r"xxxx|lorem|ipsum|this.*(?:page|slide).*layout",
        markitdown_output,
        flags=re.IGNORECASE,
    )

    print(f"QA text written to {qa_path}")
    if placeholder_hits:
        print("Placeholder-like content detected. Review the QA text before shipping.")
    else:
        print("No obvious placeholder text detected in markitdown output.")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reuse the local skills/pptx workflow instead of generating slides from scratch.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("analyze", help="Run thumbnail + markitdown analysis on the template")
    subparsers.add_parser("unpack", help="Unpack the template into the local work directory")
    subparsers.add_parser("prepare", help="Run analyze, then unpack")

    add_slide_parser = subparsers.add_parser(
        "add-slide",
        help="Add a slide by duplicating a slide XML or creating from a slideLayout XML",
    )
    add_slide_parser.add_argument(
        "source",
        help="Example: slide2.xml or slideLayout3.xml",
    )

    subparsers.add_parser("clean", help="Clean orphaned slide files in the unpacked directory")

    pack_parser = subparsers.add_parser("pack", help="Pack the unpacked directory into a PPTX")
    pack_parser.add_argument(
        "--output",
        default=str(OUTPUT_PATH),
        help="Output PPTX path",
    )

    qa_parser = subparsers.add_parser("qa", help="Run markitdown QA on an output PPTX")
    qa_parser.add_argument(
        "--pptx",
        default=str(OUTPUT_PATH),
        help="PPTX file to validate",
    )

    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        analyze_template()
    elif args.command == "unpack":
        unpack_template()
    elif args.command == "prepare":
        analyze_template()
        unpack_template()
    elif args.command == "add-slide":
        add_slide(args.source)
    elif args.command == "clean":
        clean_unpacked()
    elif args.command == "pack":
        pack_output(Path(args.output))
    elif args.command == "qa":
        run_qa(Path(args.pptx))


if __name__ == "__main__":
    main()
