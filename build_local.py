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

Building also stamps the current UTC time into the footer of both the
template and the generated page, so every release says when it was cut.
--check does not stamp: it only compares.

    python3 build_local.py            # stamps, then writes ./index.html
    python3 build_local.py --check    # exit 1 if ./index.html is stale
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "server" / "templates" / "index.html"
OUTPUT = HERE / "index.html"

WHEEL = "symbulator-0.5.2-py3-none-any.whl"

# The build stamp in the page footer, the last line of the interface.
# It lives in the template, so the server page and the offline build cut
# from it at the same moment carry the same one -- which is the whole
# point of it: it is what tells you which build a site is actually
# running, when three of them are deployed separately and any one of
# them can silently be a version behind.
STAMP_RE = re.compile(r"(Symbulator 9 version )\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")


def stamp_template() -> str:
    """Write the current UTC time into the template's footer; return it.

    This is the one place the build writes back to its own source, and it
    is deliberate: the stamp describes the release, not the interface, and
    the template is what both variants are cut from. --check must never
    call this -- it compares the generated file against the template byte
    for byte, and a stamp read off the clock would make every check fail
    with nothing actually wrong."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = TEMPLATE.read_text(encoding="utf-8")
    text, found = STAMP_RE.subn(lambda m: m.group(1) + now, text)
    if found != 1:
        raise SystemExit(f"build_local.py: expected exactly one build stamp "
                         f"in {TEMPLATE.name}, found {found}. The footer line "
                         f"changed shape -- fix STAMP_RE to match it.")
    TEMPLATE.write_text(text, encoding="utf-8", newline="")
    return now


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
    """Removes every span from `start` up to and including `end` -- there
    can be more than one such marked block in the template (e.g. the
    "download the offline version" card, and separately the "no backend
    here" notice), so this loops rather than assuming a single pair.
    Insists at least one block was found, and that every start has a
    matching end. Used to drop content that is nonsensical inside the
    offline build itself, where there is always a working engine."""
    out = []
    pos = 0
    count = 0
    while True:
        i = text.find(start, pos)
        if i == -1:
            out.append(text[pos:])
            break
        j = text.find(end, i + len(start))
        if j == -1:
            raise SystemExit(
                f"build_local.py: {label or 'strip_between'} found a start "
                f"marker with no matching end marker. The template has "
                f"changed; fix this script."
            )
        out.append(text[pos:i])
        pos = j + len(end)
        count += 1
    if count == 0:
        raise SystemExit(
            f"build_local.py: {label or 'strip_between'} markers not found. "
            f"The template has changed; fix this script."
        )
    return "".join(out)


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
    // numpy comes with the runtime and is loaded up front alongside
    // sympy: symbulator.plotting imports it lazily, so without it the
    // Plot card fails at the point of use with a raw "No module named
    // 'numpy'" -- the two plot examples in examples.cir among them.
    await pyodide.loadPackage(['sympy', 'numpy']);
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
  // Whichever caller happens to be the first to invoke py() before boot
  // finishes sets this message -- which might not be solve() (the
  // examples list loads itself in the background as soon as the page
  // opens, well before anyone has clicked Run). Only solve() clears it
  // afterward, so if some other caller set it, it would otherwise sit
  // there forever. py() is the one thing every caller shares, so it is
  // the one place that can reliably clean up after itself once boot is
  // done, no matter who triggered it.
  const setBooting = !bridge && !pyFailed;
  if (setBooting) status.textContent = 'starting the maths engine…';
  await pyReady;
  if (setBooting && status.textContent === 'starting the maths engine…') {
    status.textContent = '';
  }
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
<script>
// Offering installation from inside the page, because the browser's own
// affordance is easy to miss and impossible to describe in one sentence:
// desktop puts an icon in the address bar, Android hides it in a menu
// whose wording changes between Chrome versions ("Install app",
// "Install and create shortcut", "Add to Home Screen"), and iOS has no
// install prompt at all. Where the browser lets us drive it, we show a
// button and skip the explaining entirely.
(function () {
  var bar = document.getElementById('installbar');
  var btn = document.getElementById('installbtn');
  var txt = document.getElementById('installtext');
  if (!bar) return;

  function installed() {
    return window.matchMedia('(display-mode: standalone)').matches ||
           window.navigator.standalone === true;
  }
  var dismissed = false;
  try {
    dismissed = localStorage.getItem('symbulator-install-dismissed') === '1';
  } catch (e) {}
  if (installed() || dismissed) return;

  var deferred = null;
  // Chromium fires this only once its own install criteria are met, so
  // the bar cannot appear on a page that could not actually be installed.
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    bar.classList.add('show');
  });

  btn.addEventListener('click', function () {
    if (!deferred) return;
    deferred.prompt();
    deferred.userChoice.then(function () {
      deferred = null;
      bar.classList.remove('show');
    });
  });

  document.getElementById('installno').addEventListener('click', function () {
    bar.classList.remove('show');
    try { localStorage.setItem('symbulator-install-dismissed', '1'); } catch (e) {}
  });

  window.addEventListener('appinstalled', function () {
    bar.classList.remove('show');
    try { localStorage.removeItem('symbulator-install-dismissed'); } catch (e) {}
  });

  // iOS/iPadOS Safari never fires beforeinstallprompt and exposes no way
  // to trigger installation, so describing the Share menu is the only
  // option left there.
  var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
              (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (isIOS) {
    txt.textContent = 'Install Symbulator as an app: tap Share, then "Add to Home Screen". ' +
                      'It then works offline, in its own window.';
    btn.hidden = true;
    bar.classList.add('show');
  }
})();
</script>
</body>"""

BOOTBAR_CSS = """  .bootbar { background: #fff9ec; border: 1px solid #eadfc0; color: #6b5b34;
             border-radius: 8px; padding: .5rem .9rem; margin: 1rem 0 -.4rem;
             font-size: .88rem; }
  .bootbar.ready { display: none; }
  .bootbar.failed { background: var(--err-bg); border-color: #ecc8c8; color: var(--err-ink); }
"""

# Deliberately built from the page's own colour tokens rather than fixed
# hex values, so the bar follows Dark Mode like everything else.
INSTALLBAR_CSS = """  .installbar { background: var(--card); border: 1px solid var(--line);
                color: var(--ink); border-radius: 8px; padding: .5rem .9rem;
                margin: 1rem 0 -.4rem; font-size: .88rem; display: none;
                align-items: center; gap: .6rem; flex-wrap: wrap; }
  .installbar.show { display: flex; }
  .installbar button { font: inherit; padding: .3rem .8rem; border-radius: 6px;
                border: 1px solid var(--accent); background: var(--accent);
                color: var(--accent-ink); cursor: pointer; }
  .installbar button.dismiss { background: none; color: var(--muted);
                border-color: transparent; text-decoration: underline; padding: .3rem .4rem; }
"""


# The banner lockup is shared with symbulator.com and
# learn.symbulator.com, whose tree holds the single source. The template
# carries a verbatim copy between markers, because a build has to be
# self-contained -- the offline ZIP cannot fetch a stylesheet from another
# repository. A copy nothing compares is a copy that drifts: it drifted
# twice in one day while three files each stated the lockup, so the copy
# is checked here instead.
#
# The docs tree is not required to build. When it is absent this warns and
# carries on, so `repos/` alone still produces a release; when it is present
# and disagrees, the build stops.
BANNER_SRC = (HERE.parent.parent.parent / "Sym Docum" / "Documentation"
              / "design" / "banner.css")
BANNER_BEGIN = "/* ==== BEGIN banner.css ===="
BANNER_END = "/* ==== END banner.css ====================================== */"


def _trim(text: str) -> str:
    """Both sides compared without leading or trailing blank lines: the
    inlined copy inevitably picks up the indentation sitting before its
    closing marker, which is not a difference in the CSS."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def check_banner(template_text: str) -> None:
    """Stop the build if the inlined banner has drifted from its source."""
    if not BANNER_SRC.is_file():
        print(f"build_local.py: note -- {BANNER_SRC.name} not found at "
              f"{BANNER_SRC}; the banner copy could not be checked.")
        return
    start = template_text.find(BANNER_BEGIN)
    end = template_text.find(BANNER_END)
    if start == -1 or end == -1:
        raise SystemExit("build_local.py: the banner markers are missing from "
                         "the template. Restore them, or the shared lockup "
                         "stops being checked.")
    inlined = template_text[template_text.index("*/", start) + 2:end]
    want = "\n".join(("  " + ln).rstrip() for ln in
                     BANNER_SRC.read_text(encoding="utf-8").splitlines())
    if _trim(inlined) != _trim(want):
        raise SystemExit(
            "build_local.py: the banner block in templates/index.html no "
            f"longer matches {BANNER_SRC}.\n"
            "  The lockup is shared with symbulator.com and "
            "learn.symbulator.com; edit the source, then paste it back "
            "between the markers.")


def build() -> str:
    """Read the server template and return the transformed local-version
    HTML as a string (the caller decides whether to write it to disk or
    just compare it against the existing file -- see `main`'s --check
    mode). Each step below does one focused substitution: drop the
    server-only card, swap in the PWA/offline asset tags, add the
    "starting up" boot notice, rewire every fetch('/api/...') call to a
    direct Pyodide call, and register the service worker."""
    # encoding is explicit: the template contains curly quotes and em
    # dashes, and Windows would otherwise decode it as cp1252 and crash.
    s = TEMPLATE.read_text(encoding="utf-8")
    check_banner(s)

    # --- drop every server-only block: the "download the offline
    #     version" card, and the "no backend here" notice -- both are
    #     nonsensical inside the offline build itself, which always has
    #     a working engine on board ---------------------------------------
    s = strip_between(
        s, "  <!-- server-only:", "  <!-- /server-only -->\n",
        label="server-only blocks",
    )

    # --- title/description: the server version's say "online", which is
    #     wrong for this offline build -- match the wording already used
    #     in manifest.webmanifest's own "name" field instead, so an
    #     installed window's title bar (which some browsers/OSes
    #     concatenate manifest name + document title for) doesn't show
    #     two different, contradictory descriptions of the same app. ----
    s = sub(
        s,
        "<title>Symbulator — symbolic circuit analysis online</title>",
        "<title>Symbulator — symbolic circuit simulation</title>",
        label="local title",
    )
    s = sub(
        s,
        'content="Symbulator: symbolic simulation of linear electrical '
        'circuits (DC, AC, Laplace, transient) online, created by Roberto '
        'Perez-Franco. Powered by Python and SymPy.">',
        'content="Symbulator: symbolic simulation of linear electrical '
        'circuits (DC, AC, Laplace, transient), created by Roberto '
        'Perez-Franco. Powered by Python and SymPy.">',
        label="local meta description",
    )

    # --- head: PWA tags, local asset paths, the Pyodide runtime --------
    s = sub(
        s,
        '<link rel="icon" href="/static/favicon.ico" sizes="any">\n'
        '<link rel="icon" href="/static/favicon-32x32.png" type="image/png" sizes="32x32">\n'
        '<link rel="icon" href="/static/favicon-16x16.png" type="image/png" sizes="16x16">\n'
        '<link rel="apple-touch-icon" href="/static/apple-touch-icon.png" sizes="180x180">\n'
        '<script defer src="/static/mathjax/tex-svg.js"></script>',
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<meta name="theme-color" content="#203864">\n'
        '<link rel="icon" href="favicon.ico" sizes="any">\n'
        '<link rel="icon" href="favicon-32x32.png" type="image/png" sizes="32x32">\n'
        '<link rel="icon" href="favicon-16x16.png" type="image/png" sizes="16x16">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180">\n'
        '<script defer src="static/mathjax/tex-svg.js"></script>\n'
        '<script src="vendor/pyodide.js"></script>',
        label="head assets",
    )

    # --- header logo: server serves it from /static/, local keeps it at
    #     the folder root (same convention as the favicon above). The logo
    #     image (banner) and the icon image (favicon/app icon) are two
    #     different files -- see logo.png vs icon.png in ASSETS. ---------
    s = sub(
        s,
        '<img src="/static/logo.png" alt="Symbulator logo" class="header-logo">',
        '<img src="logo.png" alt="Symbulator logo" class="header-logo">',
        label="header logo path",
    )

    # --- the "starting up" notice --------------------------------------
    marker = "  .wrap { "
    if marker not in s:
        raise SystemExit("build_local.py: could not find the .wrap CSS rule.")
    s = s.replace(marker, BOOTBAR_CSS + INSTALLBAR_CSS + marker, 1)

    # Both bars go BELOW the banner, not inside it.
    #
    # They used to be injected ahead of <div class="topbar-inner">, which put
    # them inside <header class="topbar"> -- so the offline build's lockup
    # band measured 198px while symbulator.com and learn.symbulator.com
    # measured 149. Same CSS, same markup, different height, because this
    # build alone had two extra elements in the band. Below <main> they sit
    # in the content column, aligned with the cards, and the identity band is
    # identical on all three properties again.
    s = sub(
        s,
        '<main class="wrap">',
        '<div class="wrap"><div id="boot" class="bootbar">Starting the maths engine…\n'
        '  <span class="hint">you can start typing a circuit now</span></div></div>\n\n'
        '<div class="wrap"><div id="installbar" class="installbar">\n'
        '  <span id="installtext">Install Symbulator as an app — it then works offline,\n'
        '  in its own window, with no need to visit this page.</span>\n'
        '  <button type="button" id="installbtn">Install</button>\n'
        '  <button type="button" class="dismiss" id="installno">Not now</button>\n'
        '</div></div>\n\n'
        '<main class="wrap">',
        count=1,
        label="the boot and install bars, above <main>",
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
        """    const text = await (await fetch('examples.cir')).text();
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
      body: JSON.stringify({ circuits: openFile.entries })
    });
    const data = await r.json();""",
        """    const data = await py('export_book', { circuits: openFile.entries });""",
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
        """    const r = await fetch('/api/schematic', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ desc: desc })
    });
    const data = await r.json();""",
        """    const data = await py('schematic', { desc: desc });""",
        label="schematic fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/plot', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    const data = await r.json();""",
        """    const data = await py('plot', body);""",
        label="plot fetch",
    )

    s = sub(
        s,
        """  const r = await fetch('/api/minitool', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ tool: tool, args: args, values: last.values,
                           ...roundingState() })
  });
  return await r.json();""",
        """  return await py('mini_tool', { tool: tool, args: args,
    values: last.values, ...roundingState() });""",
        label="mini-tool fetch",
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
        conditions: $('solveqConds').value,
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
      conditions: $('solveqConds').value,
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

    if args.check:
        built = build()
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != built:
            print("index.html is STALE -- run build_local.py", file=sys.stderr)
            return 1
        print("index.html is up to date.")
        return 0

    # Stamp first, then build, so the generated page carries the same
    # build time as the template it came from.
    stamp = stamp_template()
    built = build()
    OUTPUT.write_text(built, encoding="utf-8", newline="")
    print(f"index.html written, {built.count(chr(10)) + 1} lines, build {stamp}")
    for probe in ("fetch('/api", "loadPyodide", "py('solve'", "sw.js",
                  "roundingState", "Symbulator <span", "solveqReal",
                  "py('export_book'", "addToFileBtn", "downloadFileBtn",
                  "server-only", "Run it offline", "id=\"hostNotice\"",
                  "showHostNotice"):
        print(f"  {probe:<20} {built.count(probe)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
