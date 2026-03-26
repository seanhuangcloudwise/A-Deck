#!/usr/bin/env python3
"""
Remove orphaned slides (not referenced in presentation.xml) and their
associated media/relationship files from an unpacked PPTX directory.

Usage: python scripts/clean.py unpacked/
"""
import sys
import re
from pathlib import Path


def parse_rels(rels_file: Path) -> dict:
    """Parse a .rels file and return {rId: target} mapping."""
    if not rels_file.exists():
        return {}

    try:
        import defusedxml.ElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    try:
        tree = ET.parse(str(rels_file))
        root = tree.getroot()
        ns = "http://schemas.openxmlformats.org/package/2006/relationships"
        result = {}
        for rel in root.findall(f"{{{ns}}}Relationship"):
            rid = rel.get("Id", "")
            target = rel.get("Target", "")
            rel_type = rel.get("Type", "")
            result[rid] = {"target": target, "type": rel_type}
        return result
    except Exception as e:
        print(f"  ⚠ Could not parse {rels_file}: {e}", file=sys.stderr)
        return {}


def get_referenced_slides(unpacked_dir: Path) -> set:
    """Get set of slide filenames referenced in presentation.xml.rels."""
    prs_rels = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
    rels = parse_rels(prs_rels)

    referenced = set()
    slide_type = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
    for rid, info in rels.items():
        if info["type"] == slide_type:
            # Target is relative to ppt/, e.g. "slides/slide1.xml"
            target = info["target"].replace("../", "")
            referenced.add(target.split("/")[-1])  # just filename

    return referenced


def clean(unpacked_dir: str) -> None:
    unpacked_dir = Path(unpacked_dir)

    if not unpacked_dir.exists():
        print(f"Error: {unpacked_dir} not found", file=sys.stderr)
        sys.exit(1)

    slides_dir = unpacked_dir / "ppt" / "slides"
    if not slides_dir.exists():
        print("No slides directory found — nothing to clean.")
        return

    referenced = get_referenced_slides(unpacked_dir)
    removed = 0

    for slide_file in sorted(slides_dir.glob("slide[0-9]*.xml")):
        if slide_file.name not in referenced:
            print(f"  Removing orphaned slide: {slide_file.name}")
            slide_file.unlink(missing_ok=True)

            # Remove corresponding .rels file
            rels_file = slides_dir / "_rels" / (slide_file.name + ".rels")
            if rels_file.exists():
                rels_file.unlink()
                print(f"  Removing orphaned rels:  {rels_file.name}")

            removed += 1

    if removed == 0:
        print("✓ No orphaned slides found — directory is clean.")
    else:
        print(f"\n✓ Removed {removed} orphaned slide(s).")

    print("\nNext step: Pack the directory:")
    print("  python scripts/office/pack.py unpacked/ output.pptx --original input.pptx")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean.py unpacked/")
        sys.exit(1)
    clean(sys.argv[1])
