#!/usr/bin/env python3
"""Publish only the images the site uses, downscaled, from images/ (originals).

`images/` holds the full-resolution originals (up to 5.9 MB each, 2752 px
wide) and is never served. This script scans the Markdown pages under docs/
for references to `assets/images/<name>`, and for each referenced name:

  * finds the original `images/<name>` (byte-exact, case-sensitive - macOS
    file systems are case-insensitive, so existence is checked against the
    directory listing, not the file system);
  * downscales it with Pillow so the width is at most MAX_WIDTH (LANCZOS,
    aspect ratio kept, never upscaled) and saves it as an optimized PNG,
    keeping alpha (RGBA) when present;
  * copies .svg and .gif files verbatim (never resized).

A manifest `docs/assets/images/.manifest.json` maps each published name to
{source_sha256, width, height, bytes}. A destination whose recorded source
hash is unchanged is skipped, so reruns are idempotent and fast. Files in
docs/assets/images that are no longer referenced are deleted (unless
--keep-unreferenced) so the served set is exactly the referenced set.

Usage:
  python scripts/optimize_images.py                 # sync docs/assets/images
  python scripts/optimize_images.py --report        # + missing/unreferenced report
  python scripts/optimize_images.py --dry-run       # show actions, write nothing
  python scripts/optimize_images.py --keep-unreferenced

Exit status is non-zero when a referenced original is missing or an image
cannot be processed. Requires Pillow (see requirements-dev.txt).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("error: Pillow is required (pip install -r requirements-dev.txt)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMAGES_DIR = ROOT / "images"
OUT_DIR = DOCS / "assets" / "images"
MANIFEST_NAME = ".manifest.json"

MAX_WIDTH = 1600
SKIP_TOP_DIRS = {"assets", "materials"}      # docs/ subtrees that are not pages
COPY_AS_IS = {".svg", ".gif"}                # never resized or re-encoded
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}

# ![alt](../assets/images/X.png){ width="900" }   and   ![alt](path "title")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(\s*<?(?P<path>[^)\s>]*?assets/images/[^)\s>]+)")
# <img src="../assets/images/X.png" width=600>  (single or double quotes)
HTML_SRC_RE = re.compile(r"""src\s*=\s*(?P<q>["'])(?P<path>[^"']*?assets/images/[^"']+)(?P=q)""")


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #

def basename_from_ref(path: str) -> str:
    """'../../assets/images/X.png#frag' -> 'X.png' (URL-decoded)."""
    tail = path.rsplit("assets/images/", 1)[1]
    tail = tail.split("#", 1)[0].split("?", 1)[0]
    return urllib.parse.unquote(tail)


def find_references(docs: Path) -> dict[str, set[str]]:
    """Map image basename -> set of referencing pages (docs-relative)."""
    refs: dict[str, set[str]] = {}
    for md in sorted(docs.rglob("*.md")):
        rel = md.relative_to(docs)
        if rel.parts[0] in SKIP_TOP_DIRS:
            continue
        text = md.read_text(encoding="utf-8")
        for regex in (MD_IMG_RE, HTML_SRC_RE):
            for m in regex.finditer(text):
                name = basename_from_ref(m.group("path"))
                if name:
                    refs.setdefault(name, set()).add(rel.as_posix())
    return refs


def listdir_files(d: Path) -> set[str]:
    """Byte-exact names of the regular files in `d` (empty set if absent)."""
    if not d.is_dir():
        return set()
    return {e.name for e in os.scandir(d) if e.is_file()}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# manifest
# --------------------------------------------------------------------------- #

def load_manifest(out_dir: Path) -> dict:
    p = out_dir / MANIFEST_NAME
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def dump_manifest(manifest: dict) -> str:
    ordered = {k: manifest[k] for k in sorted(manifest)}
    return json.dumps(ordered, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


# --------------------------------------------------------------------------- #
# processing
# --------------------------------------------------------------------------- #

def raster_dimensions(path: Path):
    try:
        with Image.open(path) as im:
            return im.width, im.height
    except Exception:  # SVG or unreadable
        return None, None


def publish_raster(src: Path, dest: Path, max_width: int) -> tuple[int, int]:
    """Downscale (never upscale) and save as an optimized PNG; return (w, h)."""
    with Image.open(src) as im:
        im.load()
        if im.mode in ("P", "1"):  # palette/bilevel cannot be resampled well
            im = im.convert("RGBA" if "transparency" in im.info else "RGB")
        if im.width > max_width:
            new_h = max(1, round(im.height * max_width / im.width))
            im = im.resize((max_width, new_h), Image.Resampling.LANCZOS)
        save_kwargs = {"optimize": True}
        icc = im.info.get("icc_profile")
        if icc:
            save_kwargs["icc_profile"] = icc  # keep colour fidelity, drop EXIF/XMP
        fmt = "PNG" if dest.suffix.lower() == ".png" else None
        tmp = dest.with_name(dest.name + ".tmp")
        im.save(tmp, format=fmt, **save_kwargs)
        os.replace(tmp, dest)
        return im.width, im.height


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.1f} GB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--docs", type=Path, default=DOCS, help="docs directory to scan")
    ap.add_argument("--images", type=Path, default=IMAGES_DIR, help="directory of originals")
    ap.add_argument("--out", type=Path, default=OUT_DIR, help="published image directory")
    ap.add_argument("--max-width", type=int, default=MAX_WIDTH)
    ap.add_argument("--keep-unreferenced", action="store_true",
                    help="do not delete published images that no page references")
    ap.add_argument("--report", action="store_true",
                    help="list missing originals, unreferenced originals, and sizes")
    ap.add_argument("--dry-run", action="store_true", help="print actions; write nothing")
    args = ap.parse_args()

    docs, images, out = args.docs.resolve(), args.images.resolve(), args.out.resolve()
    if not docs.is_dir():
        print(f"error: docs directory not found: {docs}", file=sys.stderr)
        return 2
    if not images.is_dir():
        print(f"error: originals directory not found: {images}", file=sys.stderr)
        return 2

    refs = find_references(docs)
    originals = listdir_files(images)
    published = listdir_files(out)
    manifest = load_manifest(out)
    new_manifest: dict = {}

    written = skipped = copied = removed = kept = 0
    missing: list[str] = []
    failed: list[str] = []
    before_bytes = after_bytes = 0

    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)

    for name in sorted(refs):
        if name not in originals:
            missing.append(name)
            continue
        src = images / name
        before_bytes += src.stat().st_size
        dest = out / name
        digest = sha256_of(src)
        entry = manifest.get(name)
        unchanged = (
            isinstance(entry, dict)
            and entry.get("source_sha256") == digest
            and name in published
            and dest.stat().st_size == entry.get("bytes")
        )
        if unchanged:
            new_manifest[name] = entry
            after_bytes += entry["bytes"]
            skipped += 1
            continue
        if args.dry_run:
            print(f"  would write {name}")
            written += 1
            continue
        try:
            if src.suffix.lower() in COPY_AS_IS:
                shutil.copyfile(src, dest)
                w, h = raster_dimensions(dest)
                copied += 1
            else:
                w, h = publish_raster(src, dest, args.max_width)
                written += 1
        except Exception as exc:  # unreadable/corrupt image
            failed.append(f"{name}: {exc}")
            continue
        size = dest.stat().st_size
        after_bytes += size
        new_manifest[name] = {"source_sha256": digest, "width": w, "height": h, "bytes": size}
        dims = f"{w}x{h}" if w and h else "vector"
        print(f"  {'copied ' if src.suffix.lower() in COPY_AS_IS else 'wrote  '}{name}"
              f"  {dims}  {human(src.stat().st_size)} -> {human(size)}")

    # Prune published files nobody references (never the manifest itself).
    stale = sorted(f for f in published if f not in refs and f != MANIFEST_NAME)
    if stale and not refs:
        print(f"warning: no page under {docs} references any image; leaving "
              f"{len(stale)} published file(s) in place (nothing to sync against)")
        kept = len(stale)
        for f in stale:
            if f in manifest:
                new_manifest[f] = manifest[f]
    else:
        for f in stale:
            if args.keep_unreferenced:
                kept += 1
                if f in manifest:
                    new_manifest[f] = manifest[f]
                continue
            if args.dry_run:
                print(f"  would remove {f}")
            else:
                (out / f).unlink()
                print(f"  removed {f}")
            removed += 1

    if not args.dry_run and (refs or manifest):
        text = dump_manifest(new_manifest)
        mpath = out / MANIFEST_NAME
        if not mpath.is_file() or mpath.read_text(encoding="utf-8") != text:
            mpath.write_text(text, encoding="utf-8")

    if args.report:
        print("\n== report ==")
        if missing:
            print("referenced originals missing from images/ (byte-exact names):")
            lower = {o.casefold(): o for o in originals}
            for name in missing:
                hint = lower.get(name.casefold())
                hint = f"  (did you mean {hint}?)" if hint and hint != name else ""
                print(f"  {name}{hint}  <- {', '.join(sorted(refs[name]))}")
        else:
            print("referenced originals missing from images/: none")
        unreferenced = sorted(o for o in originals
                              if o not in refs and Path(o).suffix.lower() in IMAGE_EXTS)
        unref_bytes = sum((images / o).stat().st_size for o in unreferenced)
        print(f"unreferenced originals in images/: {len(unreferenced)} ({human(unref_bytes)})")
        for o in unreferenced:
            print(f"  {o}")
        print(f"referenced originals: {len(refs) - len(missing)} files, {human(before_bytes)}")
        print(f"published copies:     {len(new_manifest)} files, {human(after_bytes)} "
              f"(max width {args.max_width} px)")

    if failed:
        print("errors:", file=sys.stderr)
        for f in failed:
            print(f"  {f}", file=sys.stderr)
    if missing and not args.report:
        print("error: referenced images missing from images/: " + ", ".join(missing),
              file=sys.stderr)

    verb = "would sync" if args.dry_run else "synced"
    print(f"optimize_images: {verb} {len(refs)} referenced image(s): {written} written, "
          f"{copied} copied as-is, {skipped} unchanged, {removed} removed, {kept} unreferenced kept, "
          f"{len(missing)} missing; originals {human(before_bytes)} -> published {human(after_bytes)}")
    return 1 if (missing or failed) else 0


if __name__ == "__main__":
    sys.exit(main())
