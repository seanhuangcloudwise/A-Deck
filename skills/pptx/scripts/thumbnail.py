#!/usr/bin/env python3
"""
Generate a thumbnail grid from a PPTX file.
Converts slides to JPEG images and arranges them in a grid.

Usage: python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]

Output: thumbnails.jpg (or {output_prefix}.jpg)
"""
import sys
import os
import subprocess
import shutil
import tempfile
import argparse
from pathlib import Path


def find_soffice() -> str:
    """Find LibreOffice soffice binary."""
    candidates = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        os.path.expanduser("~/Applications/LibreOffice.app/Contents/MacOS/soffice"),
        "/usr/bin/soffice",
        "/usr/local/bin/soffice",
        shutil.which("soffice"),
        shutil.which("libreoffice"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise FileNotFoundError(
        "LibreOffice not found. Install with: brew install libreoffice"
    )


def find_pdftoppm() -> str:
    """Find pdftoppm binary."""
    path = shutil.which("pdftoppm")
    if path:
        return path
    raise FileNotFoundError(
        "pdftoppm not found. Install with: brew install poppler"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate slide thumbnail grid")
    parser.add_argument("pptx_path", help="Input .pptx file")
    parser.add_argument("output_prefix", nargs="?", default="thumbnails",
                        help="Output file prefix (default: thumbnails)")
    parser.add_argument("--cols", type=int, default=3,
                        help="Number of columns in grid (default: 3)")
    args = parser.parse_args()

    pptx_path = Path(args.pptx_path)
    if not pptx_path.exists():
        print(f"Error: {pptx_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("PIL not found. Install with: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    try:
        soffice = find_soffice()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        pdftoppm = find_pdftoppm()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Step 1: Convert PPTX to PDF
        print(f"Converting {pptx_path.name} to PDF...")
        result = subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             str(pptx_path.resolve()), "--outdir", str(tmpdir)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"LibreOffice error:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        pdf_file = tmpdir / pptx_path.with_suffix(".pdf").name
        if not pdf_file.exists():
            # LibreOffice sometimes doesn't preserve the name
            pdfs = list(tmpdir.glob("*.pdf"))
            if not pdfs:
                print("Error: PDF conversion failed", file=sys.stderr)
                sys.exit(1)
            pdf_file = pdfs[0]

        # Step 2: Convert PDF pages to JPEG (72dpi for thumbnails)
        print("Generating slide images...")
        slide_prefix = str(tmpdir / "slide")
        subprocess.run(
            [pdftoppm, "-jpeg", "-r", "72", str(pdf_file), slide_prefix],
            check=True, capture_output=True
        )

        # Collect generated images
        slides = sorted(tmpdir.glob("slide-*.jpg"))
        if not slides:
            slides = sorted(tmpdir.glob("slide*.jpg"))

        if not slides:
            print("Error: No slide images generated", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(slides)} slides. Building thumbnail grid...")

        # Step 3: Build thumbnail grid
        cols = min(args.cols, len(slides))
        rows = (len(slides) + cols - 1) // cols

        sample = Image.open(slides[0])
        thumb_w = 320
        thumb_h = int(thumb_w * sample.height / sample.width)
        label_h = 22
        padding = 4

        grid_w = cols * (thumb_w + padding) + padding
        grid_h = rows * (thumb_h + label_h + padding) + padding

        grid = Image.new("RGB", (grid_w, grid_h), (230, 230, 230))
        draw = ImageDraw.Draw(grid)

        for idx, slide_path in enumerate(slides):
            row, col = divmod(idx, cols)
            x = padding + col * (thumb_w + padding)
            y = padding + row * (thumb_h + label_h + padding)

            # Paste thumbnail
            img = Image.open(slide_path).resize((thumb_w, thumb_h), Image.LANCZOS)
            grid.paste(img, (x, y))

            # Draw slide label
            label = slide_path.stem  # e.g., "slide-01"
            draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h],
                           fill=(50, 50, 50))
            draw.text((x + 4, y + thumb_h + 4), label, fill=(200, 200, 200))

        output = f"{args.output_prefix}.jpg"
        grid.save(output, quality=85)
        print(f"✓ Saved: {output}  ({len(slides)} slides, {cols} columns)")
        print(f"\nTip: For high-res QA images, use:")
        print(f"  python scripts/office/soffice.py --headless --convert-to pdf {pptx_path}")
        print(f"  pdftoppm -jpeg -r 150 {pptx_path.stem}.pdf slide")


if __name__ == "__main__":
    main()
