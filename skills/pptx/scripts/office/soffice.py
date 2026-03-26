#!/usr/bin/env python3
"""
LibreOffice (soffice) wrapper for PPTX conversion.
Finds the soffice binary automatically on macOS and Linux.

Usage: python scripts/office/soffice.py --headless --convert-to pdf file.pptx
       python scripts/office/soffice.py --headless --convert-to pdf file.pptx --outdir output/
"""
import sys
import os
import subprocess
import shutil
from pathlib import Path


def find_soffice() -> str:
    """Find LibreOffice soffice binary across common macOS and Linux locations."""
    candidates = [
        # macOS
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        os.path.expanduser("~/Applications/LibreOffice.app/Contents/MacOS/soffice"),
        # Linux
        "/usr/bin/soffice",
        "/usr/local/bin/soffice",
        "/snap/bin/libreoffice",
        # PATH lookup
        shutil.which("soffice"),
        shutil.which("libreoffice"),
    ]

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate

    raise FileNotFoundError(
        "LibreOffice not found.\n"
        "Install on macOS:  brew install libreoffice\n"
        "Install on Ubuntu: sudo apt install libreoffice\n"
        "Install on Fedora: sudo dnf install libreoffice"
    )


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: python scripts/office/soffice.py [soffice flags] file.pptx")
        print("Example: python scripts/office/soffice.py --headless --convert-to pdf file.pptx")
        sys.exit(1)

    try:
        soffice = find_soffice()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cmd = [soffice] + args
    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
