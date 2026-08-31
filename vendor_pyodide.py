#!/usr/bin/env python3
"""
Fetch the Pyodide runtime and the wheels the offline build bundles, and
hash-check every one of them against the distribution's own lockfile.

**Why this file exists.** It did not, until 31 Aug 2026. `vendor/` is
gitignored -- 23 MB of upstream artefacts, rightly outside the repo --
and nothing recorded where those bytes had come from, so the provenance
lived only in whichever session had done it. #208 needed one more wheel
from that same distribution and could not find it: the version scheme
had changed underneath, every probe of
`cdn.jsdelivr.net/pyodide/v0.28…v0.31/full/` returned 404, and the
conclusion written down was that the source was unrecoverable.

It was recoverable, from the runtime itself. `pyodide.js` carries its
own version string, and it reads **314.0.5** -- Pyodide now tracks the
CPython it ships (3.14) instead of counting up from 0.x. With the right
number the CDN serves every filename in `vendor/pyodide-lock.json`, and
the scipy wheel fetched that way hash-matches the lockfile exactly.

So: the answer is written down here, in a script that can be re-run,
rather than in a paragraph that cannot.

    python3 vendor_pyodide.py            # fetch what is missing, check it all
    python3 vendor_pyodide.py --check    # verify what is there, fetch nothing
    python3 vendor_pyodide.py --all      # re-fetch even what is present

The lockfile is the authority on filenames and hashes and is *not*
re-fetched by default: it is the thing every other check is made
against, and replacing it silently would replace the standard along
with the measurement. `--relock` does it deliberately, and then
everything else is checked against the new one.

The Symbulator wheel in vendor/ is not upstream and is not touched here
-- it comes from a PyPI release, by the recipe in CLAUDE.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"

# Read off ee in vendor/pyodide.js -- `var ee="314.0.5"`, the value the
# runtime itself substitutes into its own CDN URL. If the runtime is
# ever upgraded, this and the lockfile move together.
PYODIDE_VERSION = "314.0.5"
BASE = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/"

LOCK = "pyodide-lock.json"

# The runtime's own files. They are not in the lockfile's package list
# and carry no hash there, so they are fetched by name and checked only
# for being non-empty and unchanged against what is already on disk.
RUNTIME = (
    "pyodide.js",
    "pyodide.asm.mjs",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
)

# The packages the two pages load by name: index.html asks Pyodide for
# sympy and numpy, eqsheet.html for sympy, numpy and scipy. mpmath is
# sympy's dependency and Pyodide resolves it out of the lockfile, so it
# has to be here even though nothing names it.
PACKAGES = ("sympy", "mpmath", "numpy", "scipy")


def fetch(name: str) -> bytes:
    url = BASE + name
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(
            f"vendor_pyodide.py: {url} returned {exc.code}.\n"
            f"  If this is a 404, the Pyodide version pinned at the top of "
            f"this file no longer matches vendor/pyodide-lock.json. Read the "
            f"version string out of vendor/pyodide.js (search it for a bare "
            f'"NNN.N.N" literal) and correct PYODIDE_VERSION.') from None


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify what is on disk; download nothing")
    ap.add_argument("--all", action="store_true",
                    help="re-fetch every file, present or not")
    ap.add_argument("--relock", action="store_true",
                    help="re-fetch pyodide-lock.json as well")
    args = ap.parse_args()

    VENDOR.mkdir(exist_ok=True)
    lockfile = VENDOR / LOCK

    if args.relock and not args.check:
        print(f"fetching {LOCK}")
        lockfile.write_bytes(fetch(LOCK))
    if not lockfile.is_file():
        if args.check:
            print(f"vendor_pyodide.py: {lockfile} is missing", file=sys.stderr)
            return 1
        print(f"fetching {LOCK}")
        lockfile.write_bytes(fetch(LOCK))

    lock = json.loads(lockfile.read_text(encoding="utf-8"))
    info = lock.get("info", {})
    print(f"Pyodide v{PYODIDE_VERSION} - Python {info.get('python')}, "
          f"abi {info.get('abi_version')}, {info.get('platform')}")

    wanted: dict[str, str | None] = {name: None for name in RUNTIME}
    for pkg in PACKAGES:
        entry = lock["packages"].get(pkg)
        if entry is None:
            print(f"vendor_pyodide.py: {LOCK} has no package {pkg!r}",
                  file=sys.stderr)
            return 1
        wanted[entry["file_name"]] = entry["sha256"]

    problems, fetched, total = [], 0, 0
    for name, want in sorted(wanted.items()):
        path = VENDOR / name
        if args.all and not args.check:
            path.unlink(missing_ok=True)
        if not path.is_file():
            if args.check:
                problems.append(f"{name} is missing")
                continue
            print(f"fetching {name}")
            path.write_bytes(fetch(name))
            fetched += 1
        data = path.read_bytes()
        total += len(data)
        got = sha256(data)
        if want is None:
            print(f"  {len(data):>10,} b  {name}  (runtime, unhashed)")
            continue
        if got != want:
            problems.append(f"{name}: sha256 {got}, lockfile says {want}")
        else:
            print(f"  {len(data):>10,} b  {name}  sha256 ok")

    print(f"{total:,} bytes in vendor/ from this distribution"
          + (f"; {fetched} fetched" if fetched else "; nothing to fetch"))

    # The Symbulator wheel is a PyPI release, not part of this
    # distribution, and is pinned in build_local.py rather than here.
    extra = sorted(p.name for p in VENDOR.glob("*")
                   if p.name not in wanted and p.name != LOCK)
    if extra:
        print("also in vendor/, from elsewhere: " + ", ".join(extra))

    for line in problems:
        print("  " + line, file=sys.stderr)
    if problems:
        print("vendor_pyodide.py: vendor/ does not match the lockfile",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
