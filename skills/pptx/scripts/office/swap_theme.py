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

  # Mode 1 + remap hardcoded colors (srgbClr hex + schemeClr slots in slides)
  python swap_theme.py input.pptx --from-preset light-cloudwise-cyan -o out.pptx \\
      --remap-colors

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
import colorsys
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
# Color remap helpers  (used by Mode 1 --remap-colors)
# ---------------------------------------------------------------------------

_COLOR_SLOTS = [
    "dk1", "lt1", "dk2", "lt2",
    "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
    "hlink", "folHlink",
]
_BRAND_SLOTS = ["accent1", "accent2", "accent3", "accent4", "accent5", "accent6"]

# Neutral hex values that are never remapped
_ALWAYS_SKIP: set[str] = {
    "FFFFFF", "000000", "FEFEFE", "010101",
    "404040", "333333", "666666", "595959", "262626",
    "A5A7AA", "AAAAAA", "999999", "CCCCCC", "DDDDDD",
    "D9D9D9", "F2F2F2", "BFBFBF", "7F7F7F", "E7E6E6",
}


def _h2rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#").upper()
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb2h(r: float, g: float, b: float) -> str:
    return "{:02X}{:02X}{:02X}".format(int(round(r)), int(round(g)), int(round(b)))


def _lum(hex_str: str) -> float:
    r, g, b = _h2rgb(hex_str)
    return (max(r, g, b) + min(r, g, b)) / 2


def _tint(base_hex: str, factor: float) -> str:
    """Blend base_hex toward white by factor (0 = base, 1 = white)."""
    r, g, b = _h2rgb(base_hex)
    return _rgb2h(r + factor * (255 - r), g + factor * (255 - g), b + factor * (255 - b))


def _tint_factor(base_hex: str, light_hex: str) -> float:
    """Estimate how much light_hex is a tint of base_hex."""
    br, bg, bb = _h2rgb(base_hex)
    lr, lg, lb = _h2rgb(light_hex)
    fs = [max(0.0, (lc - bc) / (255 - bc))
          for bc, lc in [(br, lr), (bg, lg), (bb, lb)] if 255 - bc > 5]
    return sum(fs) / len(fs) if fs else 0.5


def _is_neutral(hex_str: str) -> bool:
    """True if the color is near-white, near-black, or achromatic gray."""
    h = hex_str.upper().lstrip("#")
    if h in _ALWAYS_SKIP:
        return True
    r, g, b = _h2rgb(h)
    mx = max(r, g, b)
    sat = (mx - min(r, g, b)) / mx if mx > 0 else 0
    lum = (mx + min(r, g, b)) / 2
    # Near-black or fully achromatic → always neutral
    if lum < 25 or sat < 0.07:
        return True
    # Near-white: only neutral if it's truly achromatic (sat very low)
    # Light-tinted pastels (e.g. FDE9E8 = light pink) are NOT neutral
    if lum > 238:
        return sat < 0.05   # allow through if it has any visible hue tint
    return False


def _extract_theme_colors(z: zipfile.ZipFile) -> dict[str, str]:
    """Return {slot: uppercase_hex} from theme1.xml inside a PPTX zip."""
    ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    tp = sorted(n for n in z.namelist() if re.match(r"ppt/theme/theme\d+\.xml", n))
    if not tp:
        return {}
    root = _parse_xml(z.read(tp[0]))
    cs = root.find(f".//{{{ns}}}clrScheme")
    if cs is None:
        return {}
    colors: dict[str, str] = {}
    for slot in _COLOR_SLOTS:
        el = cs.find(f"{{{ns}}}{slot}")
        if el is None:
            continue
        sg = el.find(f"{{{ns}}}srgbClr")
        if sg is not None:
            colors[slot] = sg.get("val", "").upper()
        else:
            sc = el.find(f"{{{ns}}}sysClr")
            if sc is not None:
                colors[slot] = sc.get("lastClr", "").upper()
    return colors


def _parse_xml(data: bytes):  # type: ignore[return]
    try:
        from lxml import etree
        return etree.fromstring(data)
    except Exception:
        import xml.etree.ElementTree as ET
        return ET.fromstring(data)


def build_slot_color_map(
    old_colors: dict[str, str],
    new_colors: dict[str, str],
) -> dict[str, str]:
    """Map old theme-slot hex values → new theme-slot hex values (skip neutrals)."""
    m: dict[str, str] = {}
    for slot in _COLOR_SLOTS:
        o = old_colors.get(slot, "").upper()
        n = new_colors.get(slot, "").upper()
        if o and n and o != n and not _is_neutral(o):
            m[o] = n
    return m


def build_family_color_map(
    slides_bytes: list[bytes],
    slot_map: dict[str, str],
    target_bases: list[str],
) -> dict[str, str]:
    """
    Detect non-neutral custom hardcoded srgbClr colors not covered by slot_map.
    Group into hue families (±50°).  Map darkest per family to a distinct
    target base, then compute proportional tints for lighter variants.
    """
    custom: set[str] = set()
    for xml in slides_bytes:
        for h in re.findall(rb'srgbClr val="([A-Fa-f0-9]{6})"', xml, re.I):
            hx = h.decode().upper()
            if not _is_neutral(hx) and hx not in slot_map:
                custom.add(hx)

    if not custom:
        return {}

    # Group by hue family
    families: list[list[tuple[str, float, float]]] = []
    for hx in sorted(custom):
        r, g, b = _h2rgb(hx)
        hv, sat, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        hue = hv * 360
        placed = False
        for fam in families:
            avg_hue = sum(c[1] for c in fam) / len(fam)
            if min(abs(hue - avg_hue), 360 - abs(hue - avg_hue)) < 50:
                fam.append((hx, hue, sat))
                placed = True
                break
        if not placed:
            families.append([(hx, hue, sat)])

    # Sort families: most saturated first
    families.sort(key=lambda f: -sum(c[2] for c in f) / len(f))

    vivid = [t for t in target_bases if not _is_neutral(t)]
    remap: dict[str, str] = {}
    used: set[str] = set()

    for i, fam in enumerate(families):
        unused = [t for t in vivid if t not in used]
        chosen = unused[i % len(unused)] if unused else vivid[i % len(vivid)]
        used.add(chosen)

        by_lum = sorted(fam, key=lambda c: _lum(c[0]))
        base_src = by_lum[0][0]
        remap[base_src] = chosen

        for src_hx, _, _ in by_lum[1:]:
            f = min(0.97, max(0.0, _tint_factor(base_src, src_hx)))
            remap[src_hx] = _tint(chosen, f)

    return remap


def build_scheme_slot_remap(
    slides_bytes: list[bytes],
    new_colors: dict[str, str],
) -> dict[str, str]:
    """
    Redirect schemeClr slot references that would resolve to off-brand colors
    after the theme swap (e.g., accent6=green in a cyan theme → accent3=cyan).
    """
    brand_entries = [(s, new_colors[s]) for s in _BRAND_SLOTS if s in new_colors]
    brand_hexes = [h for _, h in brand_entries if not _is_neutral(h)]

    if len(brand_hexes) < 2:
        return {}

    # Find dominant hue bucket
    buckets: list[list[tuple[float, str]]] = []
    for hx in brand_hexes:
        r, g, b = _h2rgb(hx)
        hv, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        hue = hv * 360
        placed = False
        for bucket in buckets:
            avg = sum(x[0] for x in bucket) / len(bucket)
            if min(abs(hue - avg), 360 - abs(hue - avg)) < 50:
                bucket.append((hue, hx))
                placed = True
                break
        if not placed:
            buckets.append([(hue, hx)])

    dominant = max(buckets, key=len)
    dominant_set = {hx for _, hx in dominant}
    on_brand = [s for s, h in brand_entries if h in dominant_set]
    off_brand = [s for s, h in brand_entries if h not in dominant_set and not _is_neutral(h)]

    if not off_brand or not on_brand:
        return {}

    used_slots: set[str] = set()
    for xml in slides_bytes:
        for slot in re.findall(rb'schemeClr val="([^"]+)"', xml):
            used_slots.add(slot.decode())

    slot_remap: dict[str, str] = {}
    for bad_slot in off_brand:
        if bad_slot not in used_slots:
            continue
        bad_lum = _lum(new_colors[bad_slot])
        best = min(on_brand, key=lambda s: abs(_lum(new_colors.get(s, "000000")) - bad_lum))
        slot_remap[bad_slot] = best

    return slot_remap


def apply_color_remap(
    xml_bytes: bytes,
    srgb_map: dict[str, str],
    scheme_map: dict[str, str],
) -> bytes:
    """Apply srgbClr + schemeClr slot remaps to a slide/layout XML."""
    s = xml_bytes.decode("utf-8")
    for old, new in srgb_map.items():
        s = re.sub(rf'val="{re.escape(old)}"', f'val="{new}"', s, flags=re.I)
    for old_slot, new_slot in scheme_map.items():
        s = s.replace(f'schemeClr val="{old_slot}"', f'schemeClr val="{new_slot}"')
    return s.encode("utf-8")


# ---------------------------------------------------------------------------
# Mode 1 — theme only
# ---------------------------------------------------------------------------


def swap_theme_only(
    target_path: str | Path,
    theme_bytes: bytes,
    output_path: str | Path,
    srgb_map: dict[str, str] | None = None,
    scheme_map: dict[str, str] | None = None,
) -> None:
    """Replace ppt/theme/theme*.xml and optionally remap hardcoded colors in slides."""
    target_path = Path(target_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    _srgb = srgb_map or {}
    _scheme = scheme_map or {}
    remap_active = bool(_srgb or _scheme)

    buf = io.BytesIO()
    with (
        zipfile.ZipFile(target_path, "r") as zin,
        zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zout,
    ):
        for entry in zin.namelist():
            data = zin.read(entry)
            if re.match(r"ppt/theme/theme\d+\.xml", entry):
                data = theme_bytes
            elif remap_active and (
                re.match(r"ppt/slides/slide\d+\.xml$", entry)
                or entry.startswith("ppt/slideLayouts/")
                or entry.startswith("ppt/slideMasters/")
                or entry.startswith("ppt/charts/")
            ) and entry.endswith(".xml"):
                data = apply_color_remap(data, _srgb, _scheme)
            zout.writestr(entry, data)

    output_path.write_bytes(buf.getvalue())
    label = " + color remap" if remap_active else ""
    print(f"✓ Mode 1 (theme-only{label}) → {output_path}")


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
    parser.add_argument(
        "--remap-colors", action="store_true", default=False,
        help=(
            "Mode 1 only: remap hardcoded srgbClr hex values and schemeClr slot "
            "references in slides to match the new theme palette. Handles three "
            "layers: (1) theme-slot hex map, (2) hue-family custom color map, "
            "(3) off-brand schemeClr slot redirect."
        ),
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
    srgb_map: dict[str, str] = {}
    scheme_map: dict[str, str] = {}

    if args.remap_colors:
        with (
            zipfile.ZipFile(target_path, "r") as t_zip,
            zipfile.ZipFile(source_path, "r") as s_zip,
        ):
            old_colors = _extract_theme_colors(t_zip)
            new_colors = _extract_theme_colors(s_zip)
            slot_map = build_slot_color_map(old_colors, new_colors)
            print(f"  srgbClr slot map   ({len(slot_map)}): {slot_map}")

            slides_bytes = [
                t_zip.read(n)
                for n in sorted(t_zip.namelist())
                if re.match(r"ppt/slides/slide\d+\.xml$", n)
                or re.match(r"ppt/charts/chart\w+\.xml$", n)
            ]
            n_charts = sum(
                1 for n in t_zip.namelist()
                if re.match(r"ppt/charts/chart\w+\.xml$", n)
            )
            if n_charts:
                print(f"  charts scanned:    {n_charts}")
            brand_vivid = [
                h for s in _BRAND_SLOTS
                for h in [new_colors.get(s, "")] if h and not _is_neutral(h)
            ]
            fam_map = build_family_color_map(slides_bytes, slot_map, brand_vivid)
            fam_map = {k: v for k, v in fam_map.items() if k not in slot_map}
            print(f"  srgbClr family map ({len(fam_map)}): {fam_map}")

            srgb_map = {**fam_map, **slot_map}
            scheme_map = build_scheme_slot_remap(slides_bytes, new_colors)
            print(f"  schemeClr remap    ({len(scheme_map)}): {scheme_map}")

    swap_theme_only(target_path, theme_bytes, output_path, srgb_map, scheme_map)
    if args.verify:
        ok = verify_mode1(output_path, theme_bytes)
        print("\n" + ("All checks passed ✓" if ok else "Some checks FAILED ✗"))


if __name__ == "__main__":
    main()
