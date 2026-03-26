#!/usr/bin/env python3
"""
Repack a directory of unpacked PPTX XML back into a .pptx file.
Re-encodes smart quotes as XML entities. Validates XML before packing.

Usage: python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
"""
import sys
import zipfile
import argparse
import re
from pathlib import Path

# Smart quote → XML entity mapping
SMART_QUOTE_MAP = [
    ("\u201c", "&#x201C;"),  # " left double quotation mark
    ("\u201d", "&#x201D;"),  # " right double quotation mark
    ("\u2018", "&#x2018;"),  # ' left single quotation mark
    ("\u2019", "&#x2019;"),  # ' right single quotation mark
    ("\u2013", "&#x2013;"),  # – en dash
    ("\u2014", "&#x2014;"),  # — em dash
    ("\u2026", "&#x2026;"),  # … ellipsis
]

# Correct MIME types for PPTX parts
CONTENT_TYPES = {
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xml": "application/xml",
    ".rels": "application/vnd.openxmlformats-package.relationships+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".wmf": "image/x-wmf",
    ".emf": "image/x-emf",
}


def validate_xml(content: str, filename: str) -> bool:
    """Validate XML content. Returns True if valid."""
    try:
        try:
            import defusedxml.ElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        ET.fromstring(content.encode("utf-8"))
        return True
    except Exception as e:
        print(f"  ⚠ XML validation warning in {filename}: {e}", file=sys.stderr)
        return False


def re_encode_smart_quotes(text: str) -> str:
    """Re-encode smart quotes back to XML entities."""
    for char, entity in SMART_QUOTE_MAP:
        text = text.replace(char, entity)
    return text


def pack(input_dir: str, output_pptx: str, original_pptx: str = None) -> None:
    input_dir = Path(input_dir)
    output_pptx = Path(output_pptx)
    output_pptx.parent.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        print(f"Error: {input_dir} not found", file=sys.stderr)
        sys.exit(1)

    xml_extensions = {".xml", ".rels"}
    files_packed = 0
    errors = 0

    # Collect all files preserving directory order
    # [Content_Types].xml must be first in the ZIP
    all_files = []
    content_types = input_dir / "[Content_Types].xml"
    if content_types.exists():
        all_files.append(content_types)

    for f in sorted(input_dir.rglob("*")):
        if f.is_file() and f != content_types:
            all_files.append(f)

    with zipfile.ZipFile(output_pptx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in all_files:
            rel_path = str(f.relative_to(input_dir))
            # Normalize path separators to forward slash (ZIP standard)
            rel_path = rel_path.replace("\\", "/")

            suffix = f.suffix.lower()
            if suffix in xml_extensions:
                try:
                    text = f.read_text(encoding="utf-8", errors="replace")
                    # Re-encode smart quotes
                    text = re_encode_smart_quotes(text)
                    # Validate
                    if not validate_xml(text, rel_path):
                        errors += 1
                    data = text.encode("utf-8")
                except Exception as e:
                    print(f"  ⚠ Error processing {rel_path}: {e}", file=sys.stderr)
                    data = f.read_bytes()
                    errors += 1
            else:
                data = f.read_bytes()

            zf.writestr(rel_path, data)
            files_packed += 1

    status = "✓" if errors == 0 else f"⚠ ({errors} warnings)"
    print(f"{status} Packed {files_packed} files → {output_pptx}")

    if errors > 0:
        print(f"\n  {errors} XML validation warning(s) above may indicate content issues.")
        print("  Run visual QA to verify the output is correct.")
    else:
        print("\nNext step: Run QA to verify the presentation:")
        print("  python scripts/office/soffice.py --headless --convert-to pdf output.pptx")
        print("  pdftoppm -jpeg -r 150 output.pdf slide")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Repack unpacked PPTX directory into a .pptx file"
    )
    parser.add_argument("input_dir", help="Unpacked directory path")
    parser.add_argument("output_pptx", help="Output .pptx file path")
    parser.add_argument("--original", help="Original .pptx (for reference, currently unused)")
    args = parser.parse_args()
    pack(args.input_dir, args.output_pptx, args.original)
