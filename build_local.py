#!/usr/bin/env python3
"""
Regenerate the local version from the server version.

Two things come across. **index.html**: there is exactly one interface,
written once, in ../server/templates/index.html, and the local version is
that same page with the network taken out -- every `fetch('/api/...')`
becomes a direct call into Python running in the tab, plus the boot code,
the PWA tags and the service-worker registration. And **the shared
modules**, symbulator_ui.py and circuitbook.py, which are one file each and
are simply copied.

Doing either by hand is how the two front ends drift apart, so it is a
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
SERVER = HERE.parent / "server"
TEMPLATE = SERVER / "templates" / "index.html"
OUTPUT = HERE / "index.html"

# The two modules that are one file each, shared verbatim with the server.
#
# They used to be copied across by hand, which is to say they were copied
# across when somebody remembered: the git history is a run of server
# commits each followed by a separate "Carry the ... into the offline build",
# and stage_install_site.py exists because the three support files
# "sat a full day out of date while every deploy reported success".
#
# Nothing compared them, so nothing could say when they had drifted -- the
# same shape as the banner two functions down, and the same answer, except
# that here the copy can simply be made rather than checked: this script
# already generates index.html into this repository from the server's
# template, and these are no different. bridge.py is not among them; it is
# this build's own glue, with no server counterpart.
SHARED = ("symbulator_ui.py", "circuitbook.py")

# The built-in examples: a folder of input files, each carrying its own
# title. Same story as the modules above -- one source, in the server tree,
# copied here by the build.
#
# The manifest is the part that is not just a copy. On the server the folder
# is listed live, so a file can be dropped in without a rebuild. The offline
# build has no server and a fetch cannot enumerate a directory, so it reads
# examples.json instead. Both ends answer the same shape and the interface
# cannot tell them apart -- but only as long as the manifest matches the
# folder, which is what --check is for.
EXAMPLES_SRC = SERVER / "examples"
EXAMPLES_OUT = HERE / "examples"
MANIFEST = "examples.json"
SW = HERE / "sw.js"
SW_BEGIN = "  // ==== BEGIN examples ==== written by build_local.py; do not edit"
SW_END = "  // ==== END examples ===="

WHEEL = "symbulator-0.5.20-py3-none-any.whl"

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
    // 'numpy'" -- the two plot examples in the supplied set among them.
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
# learn.symbulator.com. banner.css in THIS repository is the single
# source (moved here from the docs tree, closing #75's open question:
# now the commit that changes the lockup and the commit the app build
# was checked against are the same commit). The template carries a
# verbatim copy between markers, because a build has to be
# self-contained -- the offline ZIP cannot fetch a stylesheet at all.
# A copy nothing compares is a copy that drifts: it drifted twice in
# one day while three files each stated the lockup, so the copy is
# checked here. The docs build reads the same file for the two
# websites, and its --check guards the landing page's hand copy.
BANNER_SRC = HERE / "banner.css"
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


def example_manifest() -> str:
    """The manifest the offline build reads, as it should be right now."""
    import json
    import sys

    # circuitbook from the *server*, deliberately: it is the source of the
    # format, and the copy in this repository may be the one this run is
    # about to replace.
    sys.path.insert(0, str(SERVER))
    import circuitbook                                        # noqa: E402

    files = []
    for path in sorted(EXAMPLES_SRC.glob("*.cir")):
        _circuits, _warnings, title = circuitbook.parse_book(
            path.read_text(encoding="utf-8"))
        files.append({"name": path.name, "title": title or path.name})
    return json.dumps({"ok": True, "files": files}, indent=1) + "\n"


def sw_example_lines() -> str:
    """The examples, as the service worker's cache list wants them.

    The offline build caches by name -- it cannot discover a folder any
    more than a fetch can -- so this block is generated. Adding a lesson
    should not mean remembering to edit a service worker, and a file that
    is shipped but never cached is a file that vanishes offline."""
    names = [MANIFEST] + [p.name for p in sorted(EXAMPLES_SRC.glob("*.cir"))]
    return "\n".join(f"  'examples/{n}'," for n in names)


def sw_text() -> str:
    """sw.js as it should be, with the generated block filled in."""
    current = SW.read_text(encoding="utf-8")
    start = current.find(SW_BEGIN)
    end = current.find(SW_END)
    if start == -1 or end == -1:
        raise SystemExit("build_local.py: the examples markers are missing "
                         "from sw.js. Restore them, or the offline build "
                         "stops caching the examples and loses them.")
    head = current[:start + len(SW_BEGIN)]
    tail = current[end:]
    return head + "\n" + sw_example_lines() + "\n" + tail


def stale_examples() -> list:
    """What in the examples folder is out of date: file names, and the
    manifest if it has drifted."""
    out = []
    if not EXAMPLES_SRC.is_dir():
        raise SystemExit(f"build_local.py: {EXAMPLES_SRC} is missing. The "
                         f"built-in examples live there.")
    for src in sorted(EXAMPLES_SRC.glob("*.cir")):
        here = EXAMPLES_OUT / src.name
        if not here.is_file() or here.read_bytes() != src.read_bytes():
            out.append(src.name)
    # A file deleted from the source has to go from here too, or the
    # manifest and the folder disagree about what exists.
    wanted = {p.name for p in EXAMPLES_SRC.glob("*.cir")}
    if EXAMPLES_OUT.is_dir():
        for here in sorted(EXAMPLES_OUT.glob("*.cir")):
            if here.name not in wanted:
                out.append(here.name + " (no longer in the source)")
    manifest = EXAMPLES_OUT / MANIFEST
    if not manifest.is_file() or manifest.read_text(
            encoding="utf-8") != example_manifest():
        out.append(MANIFEST)
    if SW.read_text(encoding="utf-8") != sw_text():
        out.append("sw.js cache list")
    return out


def sync_examples() -> list:
    """Copy the examples across and write the manifest. Returns what moved."""
    moved = []
    EXAMPLES_OUT.mkdir(exist_ok=True)
    wanted = {p.name for p in EXAMPLES_SRC.glob("*.cir")}
    for here in sorted(EXAMPLES_OUT.glob("*.cir")):
        if here.name not in wanted:
            here.unlink()
            moved.append("removed " + here.name)
    for src in sorted(EXAMPLES_SRC.glob("*.cir")):
        here = EXAMPLES_OUT / src.name
        data = src.read_bytes()
        if not here.is_file() or here.read_bytes() != data:
            here.write_bytes(data)
            moved.append(src.name)
    manifest = EXAMPLES_OUT / MANIFEST
    text = example_manifest()
    if not manifest.is_file() or manifest.read_text(encoding="utf-8") != text:
        manifest.write_text(text, encoding="utf-8", newline="")
        moved.append(MANIFEST)
    want = sw_text()
    if SW.read_text(encoding="utf-8") != want:
        SW.write_text(want, encoding="utf-8", newline="")
        moved.append("sw.js cache list")
    return moved


def stale_shared() -> list:
    """(name, wanted bytes) for each shared module that is out of date.

    Compared as bytes, since that is what has to match: these files are
    fetched verbatim by the offline build at boot, and served verbatim from
    install.symbulator.com."""
    out = []
    for name in SHARED:
        src = SERVER / name
        if not src.is_file():
            raise SystemExit(f"build_local.py: {src} is missing. The offline "
                             f"build shares that file with the server and "
                             f"cannot be cut without it.")
        want = src.read_bytes()
        here = HERE / name
        if not here.is_file() or here.read_bytes() != want:
            out.append((name, want))
    return out


def sync_shared() -> list:
    """Copy the shared modules across. Returns the names that moved."""
    moved = []
    for name, want in stale_shared():
        (HERE / name).write_bytes(want)
        moved.append(name)
    return moved


_SCRIPT_OPEN = re.compile(r"<script(?![^>]*\bsrc=)[^>]*>")


def _inline_scripts(text: str):
    """(first line number, body) for each inline <script> in `text`."""
    out = []
    for m in _SCRIPT_OPEN.finditer(text):
        end = text.find("</script>", m.end())
        if end == -1:
            continue
        out.append((text.count("\n", 0, m.end()) + 1, text[m.end():end]))
    return out


def check_js(text: str, where: str) -> None:
    """Stop the build on a string literal left open at end of line.

    Not a parser -- a scanner for one specific, and specifically nasty,
    mistake: a newline inside '...' or "...". JavaScript does not allow it,
    the whole script then fails to parse, and every listener after it is
    never attached. The page still renders, so it looks fine until you
    click something.

    Template literals may legitimately span lines and are tracked so they
    do not raise a false alarm.
    """
    for first_line, body in _inline_scripts(text):
        quote = None          # "'", '"' or "`" when inside one
        block = False         # inside a /* ... */
        for offset, line in enumerate(body.split("\n")):
            i = 0
            while i < len(line):
                ch = line[i]
                nxt = line[i + 1] if i + 1 < len(line) else ""
                if block:
                    if ch == "*" and nxt == "/":
                        block = False
                        i += 1
                elif quote:
                    if ch == "\\":
                        i += 1
                    elif ch == quote:
                        quote = None
                elif ch == "/" and nxt == "/":
                    break                       # rest of the line is comment
                elif ch == "/" and nxt == "*":
                    block = True
                    i += 1
                elif ch in "'\"`":
                    quote = ch
                i += 1
            if quote in ("'", '"'):
                n = first_line + offset
                raise SystemExit(
                    f"build_local.py: unterminated {quote} string at "
                    f"{where}:{n}\n"
                    f"  {line.strip()[:78]}\n"
                    "  A newline inside a string literal is a SyntaxError, "
                    "and the browser then parses none of the script -- the "
                    "page renders and nothing works. Usually an escaping "
                    "slip in a script that edited this file: write a "
                    "backslash-n, not a real line break.")


def check_banner(template_text: str, where: str = "templates/index.html") -> None:
    """Stop the build if the inlined banner has drifted from its source.

    Checked in two templates: index.html (the app, whose copy this build
    inlines into the offline page) and eqsheet.html (the what-if solver
    at /eqsheet/, server-hosted but carrying the same lockup). Neither
    page can link the source file -- the offline page cannot fetch one
    at all -- so each carries a verbatim copy between the same markers,
    and this one check guards them both."""
    if not BANNER_SRC.is_file():
        raise SystemExit(
            f"build_local.py: {BANNER_SRC} is missing. It is the one "
            "source of the shared banner lockup and lives in this "
            "repository; a checkout without it is broken.")
    start = template_text.find(BANNER_BEGIN)
    end = template_text.find(BANNER_END)
    if start == -1 or end == -1:
        raise SystemExit(f"build_local.py: the banner markers are missing from "
                         f"{where}. Restore them, or the shared lockup "
                         "stops being checked.")
    inlined = template_text[template_text.index("*/", start) + 2:end]
    want = "\n".join(("  " + ln).rstrip() for ln in
                     BANNER_SRC.read_text(encoding="utf-8").splitlines())
    if _trim(inlined) != _trim(want):
        raise SystemExit(
            f"build_local.py: the banner block in {where} no "
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

    # EqSheet's page is not part of this build -- it is server-hosted --
    # but its banner copy has no other guard, and this is the one check
    # that runs on the app tree. A server checkout old enough to lack
    # the page is not an error.
    eqsheet_template = TEMPLATE.parent / "eqsheet.html"
    if eqsheet_template.is_file():
        check_banner(eqsheet_template.read_text(encoding="utf-8"),
                     where="templates/eqsheet.html")

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
        """    const data = await (await fetch('examples/examples.json')).json();""",
        label="examples list fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/examples?file=' + encodeURIComponent(name));
    const data = await r.json();""",
        """    const text = await (await fetch('examples/' + name)).text();
    const data = await py('parse_book', text);""",
        label="one example fetch",
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
      body: JSON.stringify({ circuits: openFile.entries,
                             title: openFile.title || '' })
    });
    const data = await r.json();""",
        """    const data = await py('export_book', { circuits: openFile.entries,
                                          title: openFile.title || '' });""",
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
    body: JSON.stringify({ tool: tool, args: args,
                           values: last ? last.values : {},
                           ...roundingState() })
  });
  return await r.json();""",
        """  return await py('mini_tool', { tool: tool, args: args,
    values: last ? last.values : {}, ...roundingState() });""",
        label="mini-tool fetch",
    )

    s = sub(
        s,
        """  const r = await fetch('/api/spice', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ direction: direction, text: text })
  });
  return await r.json();""",
        """  return await py('spice', { direction: direction, text: text });""",
        label="spice fetch",
    )

    s = sub(
        s,
        """    const r = await fetch('/api/evaluate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      // The domain rides with the values: `{...}` converts from time into
      // s, so it means something only when the answers are in s.
      body: JSON.stringify({ expr: $('evalExpr').value, values: last.values,
                             conditions: $('evalConds').value,
                             defines: linesOf($('defines').value),
                             domain: last.domain || '',
                             ...roundingState(), si: $('siUnits').checked })
    });
    const data = await r.json();""",
        """    const data = await py('evaluate', {
      expr: $('evalExpr').value, values: last.values,
      conditions: $('evalConds').value,
      defines: linesOf($('defines').value),
      domain: last.domain || '',
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
        defines: linesOf($('defines').value),
        values: last.values,
        domain: last.domain || '',
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
      defines: linesOf($('defines').value),
      values: last.values,
      domain: last.domain || '',
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
        check_js(TEMPLATE.read_text(encoding="utf-8"), TEMPLATE.name)
        built = build()
        check_js(built, OUTPUT.name)
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        stale = [name for name, _ in stale_shared()]
        examples = stale_examples()
        if current != built or stale or examples:
            for name in stale:
                print(f"{name} is STALE -- it differs from "
                      f"{SERVER / name}", file=sys.stderr)
            for name in examples:
                print(f"examples/{name} is STALE -- run build_local.py",
                      file=sys.stderr)
            if current != built:
                print("index.html is STALE", file=sys.stderr)
            print("run build_local.py", file=sys.stderr)
            return 1
        print("index.html is up to date, and so are "
              + " and ".join(SHARED) + " and the examples folder.")
        return 0

    # Stamp first, then build, so the generated page carries the same
    # build time as the template it came from.
    stamp = stamp_template()
    built = build()
    check_js(built, OUTPUT.name)
    OUTPUT.write_text(built, encoding="utf-8", newline="")
    print(f"index.html written, {built.count(chr(10)) + 1} lines, build {stamp}")
    moved = [f"copied {n} from ../server" for n in sync_shared()]
    moved += [f"examples: {n}" for n in sync_examples()]
    for line in moved:
        print("  " + line)
    if not moved:
        print("  the shared modules and the examples are already current")
    for probe in ("fetch('/api", "loadPyodide", "py('solve'", "sw.js",
                  "roundingState", "Symbulator <span", "solveqReal",
                  "py('export_book'", "addToFileBtn", "downloadFileBtn",
                  "server-only", "Run it offline", "id=\"hostNotice\"",
                  "showHostNotice"):
        print(f"  {probe:<20} {built.count(probe)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
