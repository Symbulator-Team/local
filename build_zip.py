#!/usr/bin/env python3
"""
Assemble the offline distributable, the ZIP published as
https://symbulator.com/9/local.zip

The ZIP is three things glued together:

  1. **This repository** -- the app itself: index.html, the Python
     modules, the icons, the manifest, the service worker, the
     launchers and README.txt.
  2. **Upstream build artefacts** -- the Pyodide runtime, the sympy and
     mpmath wheels, the Python stdlib, and MathJax. About 19 MB, far too
     big for git, so they live outside the repo and are pointed at with
     `--assets`.
  3. **A `symbulator-local/` top-level folder**, so unzipping produces
     one tidy directory instead of scattering thirty files into
     whatever the user had open.

Where the assets come from: any previously-extracted copy of the ZIP
works, since these files change only when Pyodide or MathJax is
upgraded. `--assets ../../local` points at the extracted copy on
Roberto's machine.

Why this script exists: the recipe used to live only in an assistant's
head, and the ZIP shipped for some time with a manifest that Chrome on
Android refused to install -- a single 335x335 icon where Chrome wants
a 192 and a 512. So this does not just zip a folder, it *checks what it
built*: every icon the manifest names, every file the service worker
promises to cache, and the 192/512 pair, all have to be present and the
right size, or the build fails loudly.

    python3 build_zip.py --assets ../../local
    python3 build_zip.py --assets ../../local --out dist/local.zip
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_IN_ZIP = "symbulator-local"

# Dev-only files: they belong in the repo, not in a user's download.
EXCLUDE_NAMES = {
    "README.md",          # developer readme; users get README.txt
    "build_local.py",
    "build_zip.py",
    "CLAUDE.md",
    ".gitignore",
    ".gitattributes",
    "local.zip",
}
EXCLUDE_DIRS = {".git", "__pycache__", "dist"}

# Subtrees the repo cannot hold (too big) and must get from --assets.
ASSET_SUBTREES = ("vendor", "static")


def png_size(data: bytes) -> tuple[int, int] | None:
    """Width/height straight out of a PNG's IHDR, so this needs no Pillow."""
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return (int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big"))


def collect(src: Path, skip_top_level_excludes: bool) -> dict[str, Path]:
    """Map archive-relative path -> file on disk."""
    found: dict[str, Path] = {}
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS)
        for name in sorted(filenames):
            full = Path(dirpath) / name
            rel = full.relative_to(src).as_posix()
            if skip_top_level_excludes and rel in EXCLUDE_NAMES:
                continue
            if name.endswith(".pyc"):
                continue
            found[rel] = full
    return found


def verify(staged: dict[str, Path]) -> list[str]:
    """Everything the app promises must actually be in the archive."""
    problems: list[str] = []

    def read(rel: str) -> bytes | None:
        p = staged.get(rel)
        return p.read_bytes() if p else None

    # --- the manifest's icons -----------------------------------------
    raw = read("manifest.webmanifest")
    if raw is None:
        problems.append("manifest.webmanifest is missing")
    else:
        manifest = json.loads(raw.decode("utf-8"))
        icons = manifest.get("icons", [])
        if not icons:
            problems.append("manifest declares no icons")
        biggest = 0
        sizes_seen = []
        for icon in icons:
            src = icon.get("src", "")
            blob = read(src)
            if blob is None:
                problems.append(f"manifest names {src}, which is not in the ZIP")
                continue
            dims = png_size(blob)
            if dims is None:
                continue          # .ico and friends carry no IHDR
            width, height = dims
            sizes_seen.append((src, width))
            biggest = max(biggest, width)
            declared = icon.get("sizes", "")
            if declared and declared != f"{width}x{height}":
                problems.append(
                    f"{src} is really {width}x{height} but the manifest says {declared}"
                )
        # Chrome's install criteria; getting this wrong is what broke
        # installation on Android and is invisible until someone tries.
        if not any(w >= 192 for _, w in sizes_seen):
            problems.append("no icon >= 192px: Chrome will not offer to install")
        if not any(w >= 512 for _, w in sizes_seen):
            problems.append("no icon >= 512px: Chrome will not offer to install")
        if not any("maskable" in (i.get("purpose") or "") for i in icons):
            problems.append("no maskable icon: Android will crop the artwork badly")

    # --- everything the service worker promises to cache ---------------
    sw = read("sw.js")
    if sw is None:
        problems.append("sw.js is missing")
    else:
        text = sw.decode("utf-8")
        block = re.search(r"const ASSETS = \[(.*?)\];", text, re.S)
        if not block:
            problems.append("could not find the ASSETS list in sw.js")
        else:
            for asset in re.findall(r"'([^']+)'", block.group(1)):
                if asset == "./":
                    continue
                if asset not in staged:
                    problems.append(f"sw.js caches {asset}, which is not in the ZIP")

    # --- every local href in the page head -----------------------------
    html = read("index.html")
    if html is None:
        problems.append("index.html is missing")
    else:
        head = html.decode("utf-8").split("</head>")[0]
        for href in re.findall(r'<link[^>]+href="([^"]+)"', head):
            if href.startswith(("http://", "https://", "data:")):
                continue
            if href not in staged:
                problems.append(f"index.html links {href}, which is not in the ZIP")

    # --- the worked example of the input-file format --------------------
    # The "About input file (.cir) format" panel shows a sample file. It is
    # hand-written prose, so nothing makes it follow the writer -- and it
    # silently went stale once already, when the blank-line spacing changed
    # and rms stopped being written outside AC. Rebuild it from format_book
    # and compare: what the panel teaches has to be what the app produces.
    if html is not None:
        try:
            sys.path.insert(0, str(HERE))
            import circuitbook
        except ImportError:
            circuitbook = None
        if circuitbook is None:
            problems.append("could not import circuitbook to check the format example")
        else:
            page = html.decode("utf-8")
            start = page.find('<pre style="background:var(--code-bg)')
            if start == -1:
                problems.append("could not find the file-format example in index.html")
            else:
                shown = page[page.index(">", start) + 1:page.index("</pre>", start)]
                book = [
                    {"name": "Problem 1 — divider",
                     "desc": "e1,1,0,20\nr1,1,2,5'k\nr2,2,0,15'k",
                     "domain": "dc", "rounding": "exact", "si": False,
                     "units": True, "rms": False},
                    {"name": "Problem 2 — RC transient",
                     "desc": "e1,1,0,10/s\nr1,1,2,2200\nc1,2,0,4.7e-6",
                     "domain": "tr", "vars": "v_2", "rounding": "exact",
                     "si": False, "units": True, "rms": False},
                ]
                # drop format_book's own file header; the panel opens with a
                # line teaching the comment syntax instead
                body = circuitbook.format_book(book).split("\n", 2)[2]
                want = "# comments start with a hash\n\n" + body
                if shown.strip() != want.strip():
                    problems.append(
                        "the file-format example in index.html no longer matches what "
                        "format_book writes -- regenerate it")

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets", required=True, type=Path,
                    help="folder holding vendor/ and static/ (an extracted copy "
                         "of a previous ZIP will do)")
    ap.add_argument("--out", type=Path, default=HERE / "local.zip",
                    help="where to write the ZIP (default: ./local.zip)")
    ap.add_argument("--skip-check", action="store_true",
                    help="do not verify index.html is up to date first")
    args = ap.parse_args()

    assets = args.assets.resolve()
    if not assets.is_dir():
        print(f"build_zip.py: --assets {assets} is not a directory", file=sys.stderr)
        return 1
    missing = [d for d in ASSET_SUBTREES if not (assets / d).is_dir()]
    if missing:
        print(f"build_zip.py: {assets} has no {', '.join(missing)} subfolder(s). "
              f"Point --assets at an extracted copy of a previous ZIP.", file=sys.stderr)
        return 1

    # index.html is generated; shipping a stale one silently ships a
    # different interface from the one in the server template.
    if not args.skip_check:
        result = subprocess.run([sys.executable, str(HERE / "build_local.py"), "--check"])
        if result.returncode != 0:
            print("build_zip.py: index.html is stale -- run build_local.py first.",
                  file=sys.stderr)
            return 1

    # Assets first, repo second: the repo wins any overlap, so a wheel
    # tracked here overrides an older copy sitting in the assets folder.
    staged: dict[str, Path] = {}
    for subtree in ASSET_SUBTREES:
        staged.update({f"{subtree}/{rel}": path
                       for rel, path in collect(assets / subtree, False).items()})
    staged.update(collect(HERE, True))

    problems = verify(staged)
    if problems:
        print("build_zip.py: refusing to build --", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp()) / "out.zip"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(staged):
            z.write(staged[rel], f"{ROOT_IN_ZIP}/{rel}")
    shutil.move(str(tmp), str(args.out))

    size = args.out.stat().st_size
    print(f"{args.out}: {len(staged)} files, {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
    print("checks passed: manifest icons, service-worker cache list, page head links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
