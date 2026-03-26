#!/usr/bin/env python3
"""
Duplicate a slide or create a new slide from a layout in an unpacked PPTX directory.
Prints the <p:sldId> element to add to presentation.xml manually.

Usage:
  Duplicate slide:       python scripts/add_slide.py unpacked/ slide2.xml
  Create from layout:    python scripts/add_slide.py unpacked/ slideLayout3.xml
"""
import sys
import re
import shutil
import uuid
from pathlib import Path


def get_max_slide_id(unpacked_dir: Path) -> int:
    """Find the maximum existing slide ID in presentation.xml."""
    prs_xml = unpacked_dir / "ppt" / "presentation.xml"
    if not prs_xml.exists():
        return 256

    content = prs_xml.read_text(encoding="utf-8")
    ids = [int(m) for m in re.findall(r'<p:sldId\b[^>]*\bid="(\d+)"', content)]
    return max(ids, default=255)


def get_next_rid(unpacked_dir: Path) -> str:
    """Find the next available rId for presentation.xml.rels."""
    rels_file = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
    if not rels_file.exists():
        return "rId10"

    content = rels_file.read_text(encoding="utf-8")
    ids = [int(m) for m in re.findall(r'Id="rId(\d+)"', content)]
    next_num = max(ids, default=9) + 1
    return f"rId{next_num}"


def add_relationship(rels_file: Path, rid: str, slide_name: str) -> None:
    """Append a new slide relationship to presentation.xml.rels."""
    content = rels_file.read_text(encoding="utf-8")
    slide_type = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
    new_rel = f'  <Relationship Id="{rid}" Type="{slide_type}" Target="slides/{slide_name}"/>'

    # Insert before </Relationships>
    content = content.replace("</Relationships>", f"{new_rel}\n</Relationships>")
    rels_file.write_text(content, encoding="utf-8")


def add_slide(unpacked_dir: str, template_arg: str) -> None:
    unpacked_dir = Path(unpacked_dir)
    slides_dir = unpacked_dir / "ppt" / "slides"
    layouts_dir = unpacked_dir / "ppt" / "slideLayouts"

    if not slides_dir.exists():
        print(f"Error: {slides_dir} not found", file=sys.stderr)
        sys.exit(1)

    template_name = Path(template_arg).name
    is_layout = template_name.startswith("slideLayout")

    if is_layout:
        # Create from layout: use the first existing slide as a structural template
        existing_slides = sorted(slides_dir.glob("slide[0-9]*.xml"))
        if not existing_slides:
            print("Error: No existing slides to use as template base.", file=sys.stderr)
            sys.exit(1)
        src_slide = existing_slides[0]
        print(f"Creating new slide based on layout {template_name} (using {src_slide.name} as structural base)")
    else:
        # Duplicate a specific slide
        src_slide = slides_dir / template_name
        if not src_slide.exists():
            print(f"Error: Slide {src_slide} not found", file=sys.stderr)
            sys.exit(1)
        print(f"Duplicating slide: {template_name}")

    # Determine next slide number
    existing_nums = [
        int(re.search(r"\d+", f.name).group())
        for f in slides_dir.glob("slide[0-9]*.xml")
        if re.search(r"\d+", f.name)
    ]
    next_num = max(existing_nums, default=0) + 1
    new_name = f"slide{next_num}.xml"

    # Copy slide file
    new_slide = slides_dir / new_name
    shutil.copy2(src_slide, new_slide)
    print(f"  Created: ppt/slides/{new_name}")

    # Copy .rels file
    rels_dir = slides_dir / "_rels"
    rels_dir.mkdir(exist_ok=True)
    src_rels = rels_dir / (src_slide.name + ".rels")
    if src_rels.exists():
        shutil.copy2(src_rels, rels_dir / (new_name + ".rels"))
        print(f"  Created: ppt/slides/_rels/{new_name}.rels")

    # Add relationship to presentation.xml.rels
    prs_rels = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"
    rid = get_next_rid(unpacked_dir)
    if prs_rels.exists():
        add_relationship(prs_rels, rid, new_name)
        print(f"  Added relationship {rid} → slides/{new_name}")

    # Compute next slide ID
    next_id = get_max_slide_id(unpacked_dir) + 1

    # Print instruction for presentation.xml
    print()
    print("─" * 60)
    print("Add this element to ppt/presentation.xml inside <p:sldIdLst>")
    print("at the position where you want the slide to appear:")
    print()
    print(f'  <p:sldId id="{next_id}" r:id="{rid}"/>')
    print()
    print("─" * 60)
    print(f"New slide: ppt/slides/{new_name}")
    print(f"Edit its content, then run: python scripts/clean.py {unpacked_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/add_slide.py unpacked/ slide2.xml")
        print("       python scripts/add_slide.py unpacked/ slideLayout3.xml")
        sys.exit(1)
    add_slide(sys.argv[1], sys.argv[2])
