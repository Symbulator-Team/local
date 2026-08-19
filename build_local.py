#!/usr/bin/env python3
"""
Regenerate the local version's index.html from the server version's
template.

There is exactly one interface, written once, in
../server/templates/index.html. The local version is that same
page with the network taken out: every `fetch('/api/...')` becomes a
direct call into Python running in the tab, plus the boot code, the PWA
tags and the service-worker registration.

Doing this by hand is how the two front ends drift apart, so it is a
script. Every substitution asserts that it matched -- a silent no-op is
what once shipped a build with no service worker.

    python3 build_local.py            # writes ./index.html
    python3 build_local.py --check    # exit 1 if ./index.html is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "server" / "templates" / "index.html"
OUTPUT = HERE / "index.html"

WHEEL = "symbulator-0.4.0-py3-none-any.whl"


def sub(text: str, old: str, new: str, *, count: int = 1, label: str = "") -> str:
    """Replace and insist it happened."""
    found = text.count(old)
    if found != count:
        raise SystemExit(
            f"build_local.py: {label or old[:60]!r} matched {found} time(s), "
            f"expected {count}. The template has changed; fix this script."
        )
    return text.replace(old, new)


def strip_between(text: str, start: str, end: str, *, label: str = "") -> str:
    """Removes everything from `start` up to and including `end`, and
    insists both markers were found exactly once, in order. Used to
    drop the server-only "download the offline version" card, which
    would be nonsensical inside the offline build itself."""
    i = text.find(start)
    j = text.find(end, i + len(start) if i != -1 else 0)
    if i == -1 or j == -1:
        raise SystemExit(
            f"build_local.py: {label or 'strip_between'} markers not found. "
            f"The template has changed; fix this script."
        )
    return text[:i] + text[j + len(end):]


BOOT_JS = """
// ---------------------------------------------------------------------
// The engine. Everything below runs Python in this tab -- there is no
// server. Boot happens in the background so the page is usable while
// CPython and SymPy load (about eight seconds on a first visit); by the
// time anyone has typed a circuit it is normally ready.
// ---------------------------------------------------------------------
let pyodide = null, bridge = null, pyFailed = false;

const pyReady = (async () => {
  try {
    pyodide = await loadPyodide({ indexURL: 'vendor/' });
    await pyodide.loadPackage(['sympy']);
    await pyodide.loadPackage('vendor/WHEEL_NAME');
    // symbulator_ui.py and circuitbook.py are shared verbatim with the
    // server build; bridge.py is this build's own glue module.
    for (const f of ['symbulator_ui.py', 'circuitbook.py', 'bridge.py']) {
      const src = await (await fetch(f)).text();
      pyodide.FS.writeFile('/home/pyodide/' + f, src);
    }
    await pyodide.runPythonAsync('import sys\\nsys.path.insert(0, "/home/pyodide")');
    bridge = pyodide.pyimport('bridge');
    // symbulator_ui imports sympy lazily inside its functions, so the
    // expensive import would otherwise land on the user's first click.
    // Do it here, while they are still typing.
    await pyodide.runPythonAsync('import sympy, symbulator');
    // And run one throwaway solve: sympy builds a lot of internal
    // caches on first use, which is why solve #1 costs far more than #2.
    await pyodide.runPythonAsync(`
import symbulator_ui as _u
_u.solve_ui("e1,1,0,1:r1,1,0,1", "dc", "", None, "solve", "", "", "z",
            [], [], [], 0, False, False, False, False)
`);
    document.getElementById('boot').classList.add('ready');
    return true;
  } catch (e) {
    pyFailed = true;
    const b = document.getElementById('boot');
    b.classList.add('failed');
    b.textContent = 'The maths engine could not start: ' + e;
    return false;
  }
})();

// Call into Python. Mirrors what fetch() did in the server version, so
// the rendering code below is unchanged.
async function py(fnName, payload) {
  const status = document.getElementById('status');
  if (!bridge && !pyFailed) status.textContent = 'starting the maths engine…';
  await pyReady;
  if (pyFailed) return { ok: false, error: 'The maths engine is not available.' };
  const arg = (fnName === 'parse_book') ? payload : JSON.stringify(payload);
  const t0 = performance.now();
  const out = JSON.parse(bridge[fnName](arg));
  if (out && out.elapsed === undefined) {
    out.elapsed = +((performance.now() - t0) / 1000).toFixed(2);
  }
  return out;
}
""".replace("WHEEL_NAME", WHEEL)

SW_JS = """<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('sw.js').catch(function (err) {
      console.warn('Service worker registration failed:', err);
    });
  });
}
</script>
</body>"""

BOOTBAR_CSS = """  .bootbar { background: #fff9ec; border: 1px solid #eadfc0; color: #6b5b34;
             border-radius: 8px; padding: .5rem .9rem; margin: 1rem 0 -.4rem;
             font-size: .88rem; }
  .bootbar.ready { display: none; }
  .bootbar.failed { background: var(--err-bg); border-color: #ecc8c8; color: var(--err-ink); }
"""


def build() -> str:
    """Read the server template and return the transformed local-version
    HTML as a string (the caller decides whether to write it to disk or
    just compare it against the existing file -- see `main`'s --check
    mode). Each step below does one focused substitution: drop the
    server-only card, swap in the PWA/offline asset tags, add the
    "starting up" boot notice, rewire every fetch('/api/...') call to a
    direct Pyodide call, and register the service worker."""
    s = TEMPLATE.read_text()

    # --- drop the server-only "download the offline version" card -----
    s = strip_between(
        s, "  <!-- server-only:", "  <!-- /server-only -->\n",
        label="offline-download card",
    )

    # --- head: PWA tags, local asset paths, the Pyodide runtime --------
    s = sub(
        s,
        '<link rel="icon" href="/static/icon.svg" type="image/svg+xml">\n'
        '<script defer src="/static/mathjax/tex-svg.js"></script>',
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<meta name="theme-color" content="#123c33">\n'
        '<link rel="icon" href="icon.svg" type="image/svg+xml">\n'
        '<script defer src="static/mathjax/tex-svg.js"></script>\n'
        '<script src="vendor/pyodide.js"></script>',
        label="head assets",
    )

    # --- the "starting up" notice --------------------------------------
    marker = "  .wrap { "
    if marker not in s:
        raise SystemExit("build_local.py: could not find the .wrap CSS rule.")
    s = s.replace(marker, BOOTBAR_CSS + marker, 1)

    s = sub(
        s,
        '<div class="wrap">',
        '<div class="wrap"><div id="boot" class="bootbar">Starting the maths engine…\n'
        '  <span class="hint">you can start typing a circuit now</span></div></div>\n\n'
        '<div class="wrap">',
        count=1,
        label="first .wrap div",
    )

    # --- the boot code, injected ahead of the app's own script ---------
    anchor = "// ---- Circuit picker"
    if anchor not in s:
        raise SystemExit("build_local.py: could not find the circuit-picker section.")
    s = s.replace(anchor, BOOT_JS.strip() + "\n\n\n" + anchor, 1)

    # --- every network call becomes a Python call ----------------------
    s = sub(
        s,
        """    const r = await fetch('/api/examples');
    const data = await r.json();""",
        """    const text = await (await fetch('examples.sym')).text();
    const data = await py('parse_book', text);""",
        label="examples fetch",
    )

    s = sub(
        s,
        """  const fd = new FormData();
  fd.append('file', file);
""",
        "",
        label="upload FormData",
    )
    s = sub(
        s,
        """    const r = await fetch('/api/upload', { method: 'POST', body: fd });
    const data = await r.json();""",
        """    const text = await file.text();
    const data = await py('parse_book', text);
    data.filename = file.name;""",
        label="upload fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/export', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ circuits: picker })
    });
    const data = await r.json();""",
        """    const data = await py('export_book', { circuits: picker });""",
        label="export fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/solve', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    const data = await r.json();""",
        """    const data = await py('solve', body);""",
        label="solve fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/evaluate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ expr: $('evalExpr').value, values: last.values,
                             ...roundingState(), si: $('siUnits').checked })
    });
    const data = await r.json();""",
        """    const data = await py('evaluate', {
      expr: $('evalExpr').value, values: last.values,
      ...roundingState(), si: $('siUnits').checked });""",
        label="evaluate fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/solveq', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        equations: $('solveqEqs').value,
        unknowns: $('solveqUnks').value,
        values: last.values,
        ...roundingState(),
        si: $('siUnits').checked,
        units: $('showUnits').checked,
        real_only: $('solveqReal').checked
      })
    });
    const data = await r.json();""",
        """    const data = await py('solve_equations', {
      equations: $('solveqEqs').value,
      unknowns: $('solveqUnks').value,
      values: last.values,
      ...roundingState(),
      si: $('siUnits').checked,
      units: $('showUnits').checked,
      real_only: $('solveqReal').checked });""",
        label="solveq fetch",
    )

    # --- "could not reach the server" is the wrong words here ----------
    s = s.replace("Could not reach the server.", "The maths engine failed.")

    # --- service worker -------------------------------------------------
    s = sub(s, "</script>\n</body>", "</script>\n" + SW_JS, label="service worker")

    # --- sanity: no server left behind ---------------------------------
    for banned in ("/api/", "{{ ", "url_for("):
        if banned in s:
            raise SystemExit(
                f"build_local.py: {banned!r} survived into the local build."
            )
    return s


def main() -> int:
    """CLI entry point (see the module docstring for the two invocation
    forms): build the transformed HTML once, then either write it to
    ./index.html, or -- under --check -- compare it against what's
    already on disk and fail with a nonzero exit code if they differ,
    without touching the file. --check is what a CI/pre-commit step
    would run to catch a server-template edit that nobody re-ran the
    generator for."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify index.html is up to date instead of writing it")
    args = ap.parse_args()

    built = build()
    if args.check:
        current = OUTPUT.read_text() if OUTPUT.exists() else ""
        if current != built:
            print("index.html is STALE -- run build_local.py", file=sys.stderr)
            return 1
        print("index.html is up to date.")
        return 0

    OUTPUT.write_text(built)
    print(f"index.html written, {built.count(chr(10)) + 1} lines")
    for probe in ("fetch('/api", "loadPyodide", "py('solve'", "sw.js",
                  "roundingState", "Symbulator <span", "solveqReal",
                  "py('export_book'", "addToFileBtn", "downloadFileBtn",
                  "server-only", "Run it offline"):
        print(f"  {probe:<20} {built.count(probe)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
