#!/usr/bin/env python3
"""
Unpack a PPTX file to a directory, pretty-printing XML files.
Smart quotes (", ", ', ') are left as-is for editing; pack.py will re-encode them.

Usage: python scripts/office/unpack.py input.pptx unpacked/
"""
import sys
import os
import zipfile
import shutil
from pathlib import Path


def pretty_print_xml(data: bytes) -> str:
    """Pretty-print XML using defusedxml (preferred) or fallback to minidom."""
    text = data.decode("utf-8", errors="replace")
    try:
        import defusedxml.minidom as dxml
        dom = dxml.parseString(data)
        pretty = dom.toprettyxml(indent="  ", encoding=None)
        # Remove the XML declaration added by toprettyxml if original didn't have it
        if not text.lstrip().startswith("<?xml"):
            lines = pretty.split("\n")
            # Drop declaration line only if it was added
            if lines[0].startswith("<?xml"):
                pretty = "\n".join(lines[1:])
        return pretty
    except ImportError:
        pass

    try:
        from xml.dom import minidom
        dom = minidom.parseString(data)
        pretty = dom.toprettyxml(indent="  ", encoding=None)
        if not text.lstrip().startswith("<?xml"):
            lines = pretty.split("\n")
            if lines[0].startswith("<?xml"):
                pretty = "\n".join(lines[1:])
        return pretty
    except Exception:
        return text


def unpack(pptx_path: str, output_dir: str) -> None:
    pptx_path = Path(pptx_path)
    output_dir = Path(output_dir)

    if not pptx_path.exists():
        print(f"Error: {pptx_path} not found", file=sys.stderr)
        sys.exit(1)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    xml_extensions = {".xml", ".rels"}
    extracted = 0

    with zipfile.ZipFile(pptx_path, "r") as zf:
        for item in zf.infolist():
            target = output_dir / item.filename
            if item.filename.endswith("/"):
                target.mkdir(parents=True, exist_ok=True)
                continue

            target.parent.mkdir(parents=True, exist_ok=True)
            data = zf.read(item.filename)
            suffix = Path(item.filename).suffix.lower()

            if suffix in xml_extensions:
                try:
                    content = pretty_print_xml(data)
                    target.write_text(content, encoding="utf-8")
                except Exception:
                    target.write_bytes(data)
            else:
                target.write_bytes(data)

            extracted += 1

    print(f"✓ Unpacked {pptx_path.name} → {output_dir}/")
    print(f"  {extracted} files extracted")
    print()
    print("Next steps:")
    print("  1. Review ppt/presentation.xml for slide list")
    print("  2. Edit ppt/slides/slide{N}.xml for each slide")
    print("  3. Run: python scripts/clean.py unpacked/")
    print("  4. Run: python scripts/office/pack.py unpacked/ output.pptx --original input.pptx")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/office/unpack.py input.pptx unpacked/")
        sys.exit(1)
    unpack(sys.argv[1], sys.argv[2])
