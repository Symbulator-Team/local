#!/usr/bin/env python3
"""
Run every input through **both** front ends and compare what they say.

`tools/verify_lesson.py` in the server repo checks that the app's answers
still match the tutorial's printed ones. It drives `app.py`. Nothing
drove `bridge.py`, which is the other half of the same job -- the offline
builds call it instead of the Flask routes -- and on 31 Aug 2026 that
gap cost a shipped bug: four sites in bridge.py were rendering
`[object Object]` where a definition failed, for hours, on
install.symbulator.com and in the ZIP, while every check the project had
stayed green. The sweep could not see it; it exercises the server.

So this script exists to compare the two, entry by entry.

    python3 verify_bridge.py                # every example book
    python3 verify_bridge.py Lesson_03      # one book
    python3 verify_bridge.py --errors       # the refusal paths only
    python3 verify_bridge.py --quiet        # only what disagrees

**No Pyodide is involved, and none is needed.** `bridge.py` imports
`symbulator_ui` and `circuitbook` and nothing else; it runs under
ordinary CPython, which is what makes this cheap enough to run often.
What it cannot test is the browser around it -- the boot, the fetch of
the .py files, the service worker. That is what a real offline load in a
browser is for, and it is a different check.

### What "the same" means here

Not byte equality of the whole response. `app.py` **lists its response
fields by hand** (see the comment on its /api/solve return), so it
legitimately carries fewer keys than the bridge, which serialises the
whole dict. So:

* every field the **server** returns must match the bridge's, and
* a field the **bridge** has and the server does not is reported as a
  NOTICE, not a failure -- because that is exactly the hand-enumeration
  trap `repos/local/CLAUDE.md` warns about, where a key added in
  symbulator_ui reaches the offline build automatically and is silently
  dropped by the server until someone lists it.

`elapsed` is excluded: it is a stopwatch, not an answer.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = HERE.parent / "server"
sys.path.insert(0, str(HERE))          # bridge.py, symbulator_ui.py
sys.path.insert(0, str(SERVER))        # app.py

import bridge                                                  # noqa: E402
import circuitbook                                             # noqa: E402
import app as flask_app                                        # noqa: E402

#: Never compared: a stopwatch reading, and the two files' own idea of
#: how long they took.
IGNORE = {"elapsed"}

#: Number equality, loosely enough that a float repr cannot fail a run.
TOL = 1e-12


def rounding_args(c):
    """Same reading of a circuit's `rounding:` line as verify_lesson.py."""
    r = str(c.get("rounding") or "exact")
    if r == "exact":
        return {"digits": 0, "approx": False}
    if r == "approx":
        return {"digits": 0, "approx": True}
    try:
        return {"digits": int(r), "approx": True}
    except ValueError:
        return {"digits": 0, "approx": False}


def payload_for(e):
    """One example entry, as both front ends want to be given it."""
    p = {
        "desc": e["desc"],
        "domain": e.get("domain", "dc"),
        "omega": e.get("omega", ""),
        "tool": e.get("tool") or "solve",
        "n1": e.get("n1", ""), "n2": e.get("n2", ""),
        "kind": e.get("kind", "z"),
        "si": bool(e.get("si")), "units": bool(e.get("units", True)),
        "use_rms": bool(e.get("rms")), "polar": bool(e.get("polar")),
        "equations": e.get("equations", []),
        "unknowns": e.get("unknowns", ""),
        "conditions": e.get("conditions", []),
        "variables": ([v.strip() for v in str(e.get("vars", "")).split(",")
                       if v.strip()] or None),
    }
    p.update(rounding_args(e))
    if e.get("defines"):
        p["defines"] = e["defines"]
    return p


def diff(a, b, path=""):
    """Where two responses disagree. Numbers to a tolerance, else exact."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k in IGNORE:
                continue
            if k not in a:
                out.append(f"{path}.{k}: only the bridge has it")
            elif k not in b:
                out.append(f"{path}.{k}: only the server has it")
            else:
                out += diff(a[k], b[k], f"{path}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: {len(a)} vs {len(b)} items"]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f"{path}[{i}]")
        return out
    if isinstance(a, bool) or isinstance(b, bool):
        return [] if a is b else [f"{path}: {a!r} vs {b!r}"]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == b or math.isclose(a, b, rel_tol=TOL, abs_tol=TOL):
            return []
        return [f"{path}: {a!r} vs {b!r}"]
    return [] if a == b else [f"{path}: {a!r} vs {b!r}"]


#: An absent key and one of these are the same thing to the page.
#: app.py names its response fields by hand, so it emits `eqsheet`,
#: `system` and `solutions` on every solve, filled with a default when
#: symbulator_ui produced nothing. The bridge serialises the dict it was
#: given and simply has no such key. `data.eqsheet` is then null on one
#: build and undefined on the other, and every read of the three is
#: guarded -- `(data.solutions || []).length`. Calibrated on the
#: harness's first full run, where this shape was 201 of 201 findings.
EMPTYISH = (None, [], {}, "")


def compare(label, server, brdg):
    """(failures, notices) for one pair of responses."""
    fails, notices = [], []
    extra = sorted(set(brdg) - set(server) - IGNORE)
    shared_server, defaulted = {}, []
    for k, v in server.items():
        if k in IGNORE:
            continue
        if k not in brdg and any(v is e or v == e for e in EMPTYISH):
            defaulted.append(k)      # a hand-filled default, not drift
            continue
        shared_server[k] = v
    shared_bridge = {k: v for k, v in brdg.items()
                     if k in shared_server and k not in IGNORE}
    for d in diff(shared_server, shared_bridge):
        fails.append(f"{label}{d}")
    for k in extra:
        notices.append(f"{label}the bridge returns {k!r} and the server "
                       f"does not -- app.py lists its fields by hand, so "
                       f"check whether it should name this one")
    for k in defaulted:
        notices.append(f"{label}the server sends {k!r} as an empty default "
                       f"and the bridge omits it (benign; every read of "
                       f"these is guarded)")
    return fails, notices


# ---------------------------------------------------------------------
# The refusal paths -- where the 31 Aug bug lived, and where the two
# files are most likely to drift, because each writes its own guards.
# ---------------------------------------------------------------------
ERROR_CASES = [
    ("empty description", {"desc": "", "domain": "dc"}),
    ("bad domain", {"desc": "e1,1,0,12:r1,1,0,1", "domain": "sideways"}),
    ("ac without omega", {"desc": "e1,1,0,12:r1,1,0,1", "domain": "ac"}),
    ("braces outside fd", {"desc": "e1,1,0,{5}:r1,1,0,1", "domain": "dc"}),
    ("bad variable name", {"desc": "e1,1,0,12:r1,1,0,1", "domain": "dc",
                           "variables": ["v 2"]}),
    ("circular define", {"desc": "e1,1,0,a:r1,1,0,1", "domain": "dc",
                         "defines": "a = b\nb = a"}),
    ("define twice", {"desc": "e1,1,0,a:r1,1,0,1", "domain": "dc",
                      "defines": "a = 1\na = 2"}),
    ("define bad form", {"desc": "e1,1,0,a:r1,1,0,1", "domain": "dc",
                         "defines": "just some words"}),
    ("bad added equation", {"desc": "e1,1,0,12:r1,1,0,1", "domain": "dc",
                            "equations": ["v_1 == "], "unknowns": "x"}),
    ("unparseable circuit", {"desc": "this is not a circuit", "domain": "dc"}),
]


def run_errors(quiet):
    fails, notices, n = [], [], 0
    client = flask_app.app.test_client()
    for label, payload in ERROR_CASES:
        n += 1
        srv = client.post("/api/solve", json=payload).get_json()
        brg = json.loads(bridge.solve(json.dumps(payload)))
        f, no = compare(f"  [{label}] ", srv, brg)
        fails += f
        notices += no
        if not quiet:
            code = (brg.get("err") or {}).get("code", "-")
            print(f"  {label:22} code={code:<5} {str(brg.get('error'))[:56]}")
    return n, fails, notices


def run_book(path, quiet):
    text = path.read_text(encoding="utf-8")
    circuits, _warnings, title = circuitbook.parse_book(text)
    client = flask_app.app.test_client()
    fails, notices = [], []
    for i, e in enumerate(circuits, 1):
        payload = payload_for(e)
        srv = client.post("/api/solve", json=payload).get_json()
        brg = json.loads(bridge.solve(json.dumps(payload)))
        f, no = compare(f"  [{i}] {e['name']}: ", srv, brg)
        fails += f
        notices += no
    if not quiet:
        print(f"{path.stem}: {title!r}, {len(circuits)} entries, "
              f"{len(fails)} disagreement(s)")
    return len(circuits), fails, notices


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("book", nargs="?", help="one book, e.g. Lesson_03")
    ap.add_argument("--errors", action="store_true",
                    help="only the refusal paths")
    ap.add_argument("--quiet", action="store_true",
                    help="print only what disagrees")
    args = ap.parse_args()

    total, fails, notices = 0, [], []

    if not args.book:
        n, f, no = run_errors(args.quiet)
        total += n
        fails += f
        notices += no
        print(f"refusal paths: {n} case(s), {len(f)} disagreement(s)")
    if args.errors:
        pass
    else:
        books = ([SERVER / "examples" / f"{args.book}.cir"] if args.book
                 else sorted((SERVER / "examples").glob("*.cir")))
        for path in books:
            if not path.is_file():
                print(f"verify_bridge.py: {path} not found", file=sys.stderr)
                return 1
            n, f, no = run_book(path, args.quiet)
            total += n
            fails += f
            notices += no

    print()
    for line in notices:
        print("NOTICE " + line)
    for line in fails:
        print("DIFFER " + line)
    print(f"\n{total} case(s) through both front ends; "
          f"{len(fails)} disagreement(s), {len(notices)} notice(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
