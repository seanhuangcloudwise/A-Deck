#!/usr/bin/env python3
"""
Swap master/theme from a source PPTX into a target PPTX while preserving
ALL slide content (text, shapes, images).  Slide XML and slide .rels files
are never modified.

Three modes
-----------
  Mode 1 (default)   ppt/theme/theme1.xml only
  Mode 2             theme + specified slideLayout(s)  [--replace-layout]
  Mode 3             theme + slideMaster + every slideLayout  [--with-master]

Source is either an uploaded PPTX (--from-pptx) or a repo preset
(--from-preset) from skills/pptx/master-library/.

Usage examples
--------------
  # List available presets
  python swap_theme.py --list-presets

  # List layouts in a file or preset
  python swap_theme.py --list-layouts input.pptx
  python swap_theme.py --list-layouts --from-preset light-cloudwise-purple

  # Mode 1: theme colors only
  python swap_theme.py input.pptx --from-preset light-cloudwise-purple -o out.pptx

  # Mode 2: theme + specific layouts (repeatable, TARGET=SOURCE)
  #   Each SPEC = filename (slideLayout3.xml) | name (封面) | 1-based index
  python swap_theme.py input.pptx --from-preset light-cloudwise-purple -o out.pptx \\
      --replace-layout "slideLayout6.xml=封面" \\
      --replace-layout "3=内容"

  # Mode 3: theme + full master + all layouts
  python swap_theme.py input.pptx --from-preset light-cloudwise-purple -o out.pptx \\
      --with-master

  # Add --verify to any mode for SHA-256 validation
  python swap_theme.py input.pptx --from-preset light-cloudwise-purple -o out.pptx --verify
"""
from __future__ import annotations

import argparse
import hashlib
import io
import re
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# File lives at: skills/pptx/scripts/office/swap_theme.py
# master-library: skills/pptx/master-library/
_SCRIPT_DIR = Path(__file__).resolve().parent
MASTER_LIBRARY: Path = _SCRIPT_DIR.parent.parent / "master-library"

# ---------------------------------------------------------------------------
# Preset helpers
# ---------------------------------------------------------------------------


def list_presets() -> list[str]:
    """Return sorted list of preset names from master-library/."""
    if not MASTER_LIBRARY.exists():
        return []
    return sorted(
        d.name
        for d in MASTER_LIBRARY.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def resolve_preset(name: str) -> Path:
    """Resolve preset name → cloudwise-master.pptx path.  Exits on failure."""
    path = MASTER_LIBRARY / name / "cloudwise-master.pptx"
    if not path.exists():
        candidates = list_presets()
        names = ", ".join(candidates) if candidates else "(none found)"
        print(
            f"Error: preset '{name}' not found in {MASTER_LIBRARY}.\n"
            f"Available presets: {names}",
            file=sys.stderr,
        )
        sys.exit(1)
    return path


# ---------------------------------------------------------------------------
# Low-level ZIP helpers
# ---------------------------------------------------------------------------


def read_zentry(pptx_path: str | Path, entry: str) -> bytes | None:
    """Read a single ZIP entry.  Returns None if not present."""
    with zipfile.ZipFile(pptx_path, "r") as zf:
        if entry in zf.namelist():
            return zf.read(entry)
    return None


# ---------------------------------------------------------------------------
# Layout discovery
# ---------------------------------------------------------------------------

_CSLD_NAME_RE = re.compile(rb'<p:cSld[^>]*\sname="([^"]*)"', re.DOTALL)
_LAYOUT_PATH_RE = re.compile(r"ppt/slideLayouts/slideLayout\d+\.xml$")
_LAYOUT_RELS_PATH_RE = re.compile(
    r"ppt/slideLayouts/_rels/slideLayout\d+\.xml\.rels$"
)


def list_layouts(pptx_path: str | Path) -> list[dict]:
    """
    Return layout metadata list from a PPTX.
    Each item: {"idx": int, "filename": str, "name": str}
    """
    results: list[dict] = []
    with zipfile.ZipFile(pptx_path, "r") as zf:
        entries = sorted(e for e in zf.namelist() if _LAYOUT_PATH_RE.match(e))
        for i, entry in enumerate(entries, start=1):
            xml_bytes = zf.read(entry)
            m = _CSLD_NAME_RE.search(xml_bytes)
            layout_name = m.group(1).decode("utf-8", errors="replace") if m else ""
            results.append(
                {"idx": i, "filename": Path(entry).name, "name": layout_name}
            )
    return results


def resolve_layout_spec(pptx_path: str | Path, spec: str) -> str:
    """
    Resolve a layout spec (filename / name / 1-based index) to a canonical
    filename like "slideLayout6.xml".
    """
    layouts = list_layouts(pptx_path)

    # 1) exact filename
    for lay in layouts:
        if lay["filename"] == spec:
            return lay["filename"]

    # 2) 1-based integer index
    try:
        idx = int(spec)
        for lay in layouts:
            if lay["idx"] == idx:
                return lay["filename"]
    except ValueError:
        pass

    # 3) name (exact, then case-insensitive)
    for lay in layouts:
        if lay["name"] == spec:
            return lay["filename"]
    for lay in layouts:
        if lay["name"].lower() == spec.lower():
            return lay["filename"]

    available = "\n  ".join(
        f"[{l['idx']:2d}] {l['filename']}  \"{l['name']}\"" for l in layouts
    )
    print(
        f"Error: layout spec '{spec}' not found in {pptx_path}.\n"
        f"Available:\n  {available}",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Bundle extraction  (layout XML + .rels + referenced media)
# ---------------------------------------------------------------------------

_MEDIA_TARGET_RE = re.compile(rb'Target="\.\./media/([^"]+)"')


def extract_layout_bundle(pptx_path: str | Path, layout_filename: str) -> dict:
    """
    Extract a layout and all files it references.

    Returns:
        {
            "layout_xml":  bytes,
            "layout_rels": bytes | None,
            "media":       {basename: bytes},
        }
    """
    entry_xml = f"ppt/slideLayouts/{layout_filename}"
    entry_rels = f"ppt/slideLayouts/_rels/{layout_filename}.rels"
    with zipfile.ZipFile(pptx_path, "r") as zf:
        all_entries = set(zf.namelist())
        if entry_xml not in all_entries:
            print(f"Error: {entry_xml} not found in {pptx_path}", file=sys.stderr)
            sys.exit(1)

        layout_xml = zf.read(entry_xml)
        layout_rels = zf.read(entry_rels) if entry_rels in all_entries else None

        media: dict[str, bytes] = {}
        if layout_rels:
            for m in _MEDIA_TARGET_RE.finditer(layout_rels):
                name = m.group(1).decode()
                media_entry = f"ppt/media/{name}"
                if media_entry in all_entries:
                    media[name] = zf.read(media_entry)

    return {"layout_xml": layout_xml, "layout_rels": layout_rels, "media": media}


# ---------------------------------------------------------------------------
# [Content_Types].xml patching (for injected media files)
# ---------------------------------------------------------------------------

_CT_DEFAULT_RE = re.compile(r'<Default\s+Extension="([^"]+)"', re.IGNORECASE)

_EXT_MIME: dict[str, str] = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "svg": "image/svg+xml",
    "wmf": "image/x-wmf",
    "emf": "image/x-emf",
    "tiff": "image/tiff",
    "bmp": "image/bmp",
}


def _patch_content_types(ct_bytes: bytes, new_media_names: list[str]) -> bytes:
    """Add <Default Extension="..."> entries for any new media file extensions."""
    text = ct_bytes.decode("utf-8")
    existing_exts = {m.group(1).lower() for m in _CT_DEFAULT_RE.finditer(text)}

    additions: list[str] = []
    for name in new_media_names:
        ext = Path(name).suffix.lstrip(".").lower()
        if ext and ext not in existing_exts:
            mime = _EXT_MIME.get(ext, "application/octet-stream")
            additions.append(f'  <Default Extension="{ext}" ContentType="{mime}"/>')
            existing_exts.add(ext)

    if not additions:
        return ct_bytes

    new_text = text.replace(
        "</Types>", "\n".join(additions) + "\n</Types>", 1
    )
    return new_text.encode("utf-8")


# ---------------------------------------------------------------------------
# Mode 1 — theme only
# ---------------------------------------------------------------------------


def swap_theme_only(
    target_path: str | Path,
    theme_bytes: bytes,
    output_path: str | Path,
) -> None:
    """Replace only ppt/theme/theme1.xml."""
    target_path = Path(target_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    THEME_ENTRY = "ppt/theme/theme1.xml"
    buf = io.BytesIO()
    with (
        zipfile.ZipFile(target_path, "r") as zin,
        zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout,
    ):
        for entry in zin.namelist():
            zout.writestr(entry, theme_bytes if entry == THEME_ENTRY else zin.read(entry))

    output_path.write_bytes(buf.getvalue())
    print(f"✓ Mode 1 (theme-only) → {output_path}")


# ---------------------------------------------------------------------------
# Mode 2 — theme + specified layouts
# ---------------------------------------------------------------------------


def replace_layouts(
    target_path: str | Path,
    bundles: dict[str, dict],   # {target_layout_filename: bundle}
    theme_bytes: bytes,
    output_path: str | Path,
) -> None:
    """Replace theme + specified slideLayouts (with media collision handling)."""
    target_path = Path(target_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    THEME_ENTRY = "ppt/theme/theme1.xml"
    CT_ENTRY = "[Content_Types].xml"

    with zipfile.ZipFile(target_path, "r") as zin:
        existing_entries = set(zin.namelist())

    # Build replacements map and extra media map
    replacements: dict[str, bytes] = {THEME_ENTRY: theme_bytes}
    extra_media: dict[str, bytes] = {}  # zip entry → bytes

    for layout_file, bundle in bundles.items():
        xml_entry = f"ppt/slideLayouts/{layout_file}"
        rels_entry = f"ppt/slideLayouts/_rels/{layout_file}.rels"

        replacements[xml_entry] = bundle["layout_xml"]

        rels_bytes: bytes | None = bundle["layout_rels"]
        if rels_bytes is not None:
            for orig_name, media_bytes in bundle["media"].items():
                media_entry = f"ppt/media/{orig_name}"
                if media_entry in existing_entries:
                    # collision: prefix with _src_
                    new_name = f"_src_{orig_name}"
                    new_entry = f"ppt/media/{new_name}"
                    extra_media[new_entry] = media_bytes
                    rels_bytes = rels_bytes.replace(
                        f'Target="../media/{orig_name}"'.encode(),
                        f'Target="../media/{new_name}"'.encode(),
                    )
                else:
                    extra_media[media_entry] = media_bytes
            replacements[rels_entry] = rels_bytes

    new_media_basenames = [Path(k).name for k in extra_media]

    buf = io.BytesIO()
    with (
        zipfile.ZipFile(target_path, "r") as zin,
        zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout,
    ):
        for entry in zin.namelist():
            if entry == CT_ENTRY and new_media_basenames:
                zout.writestr(
                    entry,
                    _patch_content_types(zin.read(entry), new_media_basenames),
                )
            elif entry in replacements:
                zout.writestr(entry, replacements[entry])
            else:
                zout.writestr(entry, zin.read(entry))
        # Inject new media files (they don't exist in target)
        for media_entry, media_bytes in extra_media.items():
            zout.writestr(media_entry, media_bytes)

    output_path.write_bytes(buf.getvalue())
    print(f"✓ Mode 2 (layout swap, {len(bundles)} layout(s)) → {output_path}")


# ---------------------------------------------------------------------------
# Mode 3 — full master swap
# ---------------------------------------------------------------------------


def swap_master_full(
    target_path: str | Path,
    source_path: str | Path,
    output_path: str | Path,
) -> None:
    """Replace theme + slideMaster1 + all slideLayouts + related media."""
    target_path = Path(target_path)
    source_path = Path(source_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    CT_ENTRY = "[Content_Types].xml"

    # --- Collect everything to take from source ---
    MASTER_PARTS = {
        "ppt/theme/theme1.xml",
        "ppt/slideMasters/slideMaster1.xml",
        "ppt/slideMasters/_rels/slideMaster1.xml.rels",
    }

    src_data: dict[str, bytes] = {}
    with zipfile.ZipFile(source_path, "r") as src_zf:
        src_entries = set(src_zf.namelist())

        for entry in MASTER_PARTS:
            if entry in src_entries:
                src_data[entry] = src_zf.read(entry)

        for entry in src_entries:
            if _LAYOUT_PATH_RE.match(entry) or _LAYOUT_RELS_PATH_RE.match(entry):
                src_data[entry] = src_zf.read(entry)

        # Collect media referenced by master / layouts
        media_refs: set[str] = set()
        for data in src_data.values():
            for m in _MEDIA_TARGET_RE.finditer(data):
                media_refs.add(f"ppt/media/{m.group(1).decode()}")
        for ref in media_refs:
            if ref in src_entries:
                src_data[ref] = src_zf.read(ref)

    with zipfile.ZipFile(target_path, "r") as zin:
        existing_entries = set(zin.namelist())

    # --- Handle media collisions ---
    media_renames: dict[str, str] = {}  # orig_basename → new_basename

    for entry in list(src_data.keys()):
        if not entry.startswith("ppt/media/"):
            continue
        if entry in existing_entries:
            orig_name = Path(entry).name
            new_name = f"_src_{orig_name}"
            new_entry = f"ppt/media/{new_name}"
            src_data[new_entry] = src_data.pop(entry)
            media_renames[orig_name] = new_name

    # Rewrite references in source .xml/.rels for renamed media
    if media_renames:
        for entry in list(src_data.keys()):
            if not (entry.endswith(".xml") or entry.endswith(".rels")):
                continue
            data = src_data[entry]
            for orig, new in media_renames.items():
                data = data.replace(
                    f'Target="../media/{orig}"'.encode(),
                    f'Target="../media/{new}"'.encode(),
                )
            src_data[entry] = data

    # Entries in target that will be replaced by source versions
    skip_from_target = set(src_data.keys())

    new_media_basenames = [
        Path(e).name
        for e in src_data
        if e.startswith("ppt/media/") and e not in existing_entries
    ]

    buf = io.BytesIO()
    with (
        zipfile.ZipFile(target_path, "r") as zin,
        zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout,
    ):
        for entry in zin.namelist():
            if entry in skip_from_target:
                continue  # will be overwritten by source version
            if entry == CT_ENTRY and new_media_basenames:
                zout.writestr(
                    entry,
                    _patch_content_types(zin.read(entry), new_media_basenames),
                )
            else:
                zout.writestr(entry, zin.read(entry))

        # Write source master parts (replacing whatever was skipped)
        for entry, data in src_data.items():
            zout.writestr(entry, data)

    output_path.write_bytes(buf.getvalue())
    n_layouts = sum(1 for e in src_data if _LAYOUT_PATH_RE.match(e))
    print(f"✓ Mode 3 (full-master swap, {n_layouts} layout(s)) → {output_path}")


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _check_entry(
    output_path: str | Path,
    expected_bytes: bytes,
    entry: str,
) -> bool:
    out = read_zentry(output_path, entry)
    if out is None:
        print(f"  ✗ {entry}  (missing from output)")
        return False
    if _sha256(out) == _sha256(expected_bytes):
        print(f"  ✓ {entry}")
        return True
    print(f"  ✗ {entry}  (hash mismatch)")
    return False


def verify_mode1(output_path: str | Path, theme_bytes: bytes) -> bool:
    print("Verifying theme:")
    return _check_entry(output_path, theme_bytes, "ppt/theme/theme1.xml")


def verify_mode2(
    output_path: str | Path,
    theme_bytes: bytes,
    bundles: dict[str, dict],
) -> bool:
    print("Verifying replaced parts:")
    ok = _check_entry(output_path, theme_bytes, "ppt/theme/theme1.xml")
    for target_file, bundle in bundles.items():
        entry = f"ppt/slideLayouts/{target_file}"
        ok = _check_entry(output_path, bundle["layout_xml"], entry) and ok
    return ok


def verify_mode3(
    output_path: str | Path,
    source_path: str | Path,
) -> bool:
    print("Verifying master parts:")
    ok = True
    with zipfile.ZipFile(source_path, "r") as src_zf:
        src_entries = src_zf.namelist()
        check_entries = [
            e
            for e in src_entries
            if e in {
                "ppt/theme/theme1.xml",
                "ppt/slideMasters/slideMaster1.xml",
            }
            or _LAYOUT_PATH_RE.match(e)
        ]
        for entry in check_entries:
            src_bytes = src_zf.read(entry)
            ok = _check_entry(output_path, src_bytes, entry) and ok
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _resolve_source(args: argparse.Namespace) -> Path:
    if getattr(args, "from_pptx", None):
        p = Path(args.from_pptx)
        if not p.exists():
            print(f"Error: --from-pptx not found: {p}", file=sys.stderr)
            sys.exit(1)
        return p
    return resolve_preset(args.from_preset)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Swap master/theme into a PPTX while preserving all slide content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("target", nargs="?", help="Target PPTX (content to preserve)")

    src_group = parser.add_mutually_exclusive_group()
    src_group.add_argument("--from-pptx", metavar="PPTX", help="Source PPTX for master/theme")
    src_group.add_argument("--from-preset", metavar="NAME", help="Preset from master-library")

    parser.add_argument("--output", "-o", metavar="PPTX", help="Output PPTX path")
    parser.add_argument(
        "--verify", action="store_true",
        help="SHA-256 verify replaced parts after writing",
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--replace-layout", metavar="TARGET=SOURCE", action="append",
        dest="replace_layouts",
        help=(
            "Replace a layout: TARGET_SPEC=SOURCE_SPEC (repeatable). "
            "SPEC = filename | name | 1-based index"
        ),
    )
    mode_group.add_argument(
        "--with-master", action="store_true",
        help="Replace theme + slideMaster + all layouts",
    )

    # Query modes
    parser.add_argument(
        "--list-presets", action="store_true",
        help="List available master-library presets and exit",
    )
    parser.add_argument(
        "--list-layouts", action="store_true",
        help="List layouts in target or --from-preset/--from-pptx and exit",
    )

    args = parser.parse_args()

    # ---- Query: list presets ------------------------------------------------
    if args.list_presets:
        presets = list_presets()
        if not presets:
            print("No presets found in master-library/")
        else:
            print(f"Available presets ({len(presets)}):")
            for p in presets:
                print(f"  {p}")
        return

    # ---- Query: list layouts ------------------------------------------------
    if args.list_layouts:
        if args.target:
            pptx_path: str | Path = args.target
        elif args.from_pptx or args.from_preset:
            pptx_path = _resolve_source(args)
        else:
            parser.error("--list-layouts requires a target PPTX or --from-pptx/--from-preset")
        layouts = list_layouts(pptx_path)
        print(f"Layouts in {pptx_path} ({len(layouts)}):")
        for lay in layouts:
            print(f"  [{lay['idx']:2d}] {lay['filename']}  \"{lay['name']}\"")
        return

    # ---- Validate required swap args ----------------------------------------
    if not args.target:
        parser.error("target PPTX is required")
    if not args.from_pptx and not args.from_preset:
        parser.error("one of --from-pptx or --from-preset is required")
    if not args.output:
        parser.error("--output / -o is required")

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: target not found: {target_path}", file=sys.stderr)
        sys.exit(1)

    source_path = _resolve_source(args)
    output_path = Path(args.output)

    theme_bytes = read_zentry(source_path, "ppt/theme/theme1.xml")
    if theme_bytes is None:
        print("Error: ppt/theme/theme1.xml not found in source", file=sys.stderr)
        sys.exit(1)

    # ---- Mode 3: full master ------------------------------------------------
    if args.with_master:
        swap_master_full(target_path, source_path, output_path)
        if args.verify:
            ok = verify_mode3(output_path, source_path)
            print("\n" + ("All checks passed ✓" if ok else "Some checks FAILED ✗"))
        return

    # ---- Mode 2: specific layouts -------------------------------------------
    if args.replace_layouts:
        bundles: dict[str, dict] = {}
        for spec_pair in args.replace_layouts:
            if "=" not in spec_pair:
                print(
                    f"Error: --replace-layout must be TARGET=SOURCE, got: {spec_pair!r}",
                    file=sys.stderr,
                )
                sys.exit(1)
            target_spec, source_spec = spec_pair.split("=", 1)
            target_file = resolve_layout_spec(target_path, target_spec.strip())
            source_file = resolve_layout_spec(source_path, source_spec.strip())
            print(f"  mapping: {target_file} ← {source_file} ({source_spec.strip()!r})")
            bundles[target_file] = extract_layout_bundle(source_path, source_file)

        replace_layouts(target_path, bundles, theme_bytes, output_path)
        if args.verify:
            ok = verify_mode2(output_path, theme_bytes, bundles)
            print("\n" + ("All checks passed ✓" if ok else "Some checks FAILED ✗"))
        return

    # ---- Mode 1 (default): theme only ---------------------------------------
    swap_theme_only(target_path, theme_bytes, output_path)
    if args.verify:
        ok = verify_mode1(output_path, theme_bytes)
        print("\n" + ("All checks passed ✓" if ok else "Some checks FAILED ✗"))


if __name__ == "__main__":
    main()
