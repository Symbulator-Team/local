# Symbulator — how the whole thing fits together

Orientation for anyone (human or assistant) picking this up cold. It covers
all three site variants, not just this repo.

**This file is the canonical reference.** It is version-controlled, so it can be
corrected in the same commit as whatever it describes. A rendered copy of this
material exists as a shareable web page for people who would rather not clone
anything — if the two ever disagree, this file wins.

Accepted-but-deferred work is in [NEXT.md](NEXT.md) -- fold it into the next
release that has a reason to happen, rather than deploying three sites for it
on its own.

---

## Start here

Five things that are true, load-bearing, and **not discoverable by reading the
code**. Everything below is detail hanging off these.

1. **install and local are the same build.** `install.symbulator.com` and the
   downloadable ZIP are the same files. There is no separate "install" source
   tree and no `install` repository. Change the local build and you have changed
   both — and both need deploying, separately.

2. **The interface is generated, not written.** It exists once, in the *server*
   repo. `local/index.html` is produced from it by `build_local.py`. Editing it
   by hand works right up until the next build silently discards your change.

3. **Some text exists in only one variant.** Blocks wrapped in `server-only`
   markers are deleted from the local build. This is why searching the local
   build for copy that is plainly on the site can come up empty — and why the
   install instructions were once invisible on the one build whose entire
   purpose was installing.

4. **You cannot build a release from the repos alone.** The Pyodide runtime,
   the sympy, mpmath, numpy and scipy wheels, the Python stdlib and MathJax —
   about 36 MB — are deliberately not in git. A release needs an extracted copy
   of a *recent* ZIP to draw them from, passed as `--assets`, **or** a run of
   `vendor_pyodide.py`, which fetches the lot from the CDN and hash-checks every
   file against `vendor/pyodide-lock.json`. See the note under "Making a
   release" about numpy and scipy, which older ZIPs do not have.

5. **A stale service worker hides everything you deploy.** `sw.js` is
   cache-first. Without a `CACHE_VERSION` bump, returning visitors keep the old
   build indefinitely, including the old manifest. Any fix that "didn't work" on
   a device you have visited before is this, until proven otherwise.

## The three variants

Symbulator ships as **three separate builds of one interface**. They look
identical to a user and are built from the same source, but they run in
completely different ways.

| Variant | What it is | Where it lives | Repo |
|---|---|---|---|
| **server** | Flask app; solving happens on the server | `symbulator.pythonanywhere.com` | `Symbulator/server` |
| **install** | The offline build, hosted, installable as an app | `install.symbulator.com` | *(no repo — it is the local build, uploaded)* |
| **local** | The same offline build, downloaded as a ZIP | `symbulator.com/9/local.zip` | `Symbulator/local` |

A fourth repo, `Symbulator/solver`, is the `symbulator` PyPI package — the
maths engine. Both front ends depend on it; neither contains it.

> The GitHub repo was renamed `web` → `server` in Aug 2026. `build_local.py`
> expects the server checkout to sit beside this one **as a directory named
> `server`**. Clone them as siblings or the build cannot find its template.

### install and local are the same build

This is the point people miss. `install.symbulator.com` and the ZIP are the
*same files*. One is uploaded to a web host, the other is zipped and
downloaded. There is no separate "install" source tree — if you change the
local build, you have changed both, and both need redeploying.

---

## One interface, one source of truth

The interface is written **once**, in the server repo:

```
server/templates/index.html
```

The local build is generated from it by `build_local.py`, which takes the
network out: every `fetch('/api/...')` becomes a direct call into Python
running in the browser tab, plus the Pyodide boot code, the PWA tags and the
service-worker registration.

```
python3 build_local.py            # regenerate index.html
python3 build_local.py --check    # exit 1 if index.html is stale
```

**Never hand-edit `local/index.html`.** It is generated. Edit the server
template and re-run the script.

### There are two pages, not one

Since **#208** (31 Aug 2026) the offline build carries the **Numerical
Solver** as well: `templates/eqsheet.html` becomes `eqsheet.html`, beside
`index.html`, by the same script and the same rules. Everything above about
generation applies to it identically.

Three things about it are worth knowing before touching either page:

* **It is at the root, as `eqsheet.html`, not `eqsheet/index.html`.** That
  is what makes #204's `i18n/` base rewrite one string instead of two. The
  server serves the app at `/` and the Solver at `/eqsheet/`, which is why
  the template's own path has to be root-absolute.
* **It boots its own Pyodide, and a different set of packages.** The Solver
  loads sympy, numpy and **scipy**; the app loads sympy, numpy and the
  **symbulator wheel**. Neither loads the other's, because they are separate
  documents that share only the service worker's cache — so a reader who
  opens both downloads each file exactly once, and one who never opens the
  Solver never pays SciPy's import cost.
* **`eqsheet.py` must never import Flask.** It is a shared module now
  (`SHARED` in `build_local.py`, alongside `symbulator_ui.py` and
  `circuitbook.py`), copied verbatim and imported by Pyodide inside the tab.
  `eqsheet_web.py` in the server repo is the Blueprint; keep it thin, because
  a check added there alone guards the hosted Solver and leaves the
  downloaded one without it.

### The build stamp

The last line of the interface reads `Symbulator 9 version 2026-08-22 09:25
UTC`. `build_local.py` writes the current UTC time there on every real build --
into the **template**, not just the generated page, so the server variant and
the offline build cut from it at the same moment agree. That is what it is for:
three sites are deployed separately, any one of them can silently be a version
behind, and the footer is how you tell without guessing.

`--check` never stamps. It compares the generated file against the template
byte for byte, and a stamp read off the clock would make every check fail with
nothing actually wrong.

**A server-only deploy will not re-stamp.** If you change the template and push
it without running `build_local.py`, the live server page keeps the previous
build time. Run the build anyway -- it costs a second, and it is also what
tells you the template and the offline build still agree.

**And the reverse: a local build dirties the *server* repo.** The stamp is
written into the template, which lives in `server/`, so `build_local.py` always
leaves a one-line change there. Commit and push **both** repos after a build.
Forgetting caught us on 22 Aug: the offline pair was built and pushed, the
server repo kept the change uncommitted, and PythonAnywhere pulled a commit
whose stamp was a build behind -- with nothing wrong at either end, which is
the confusing part. If a pull gives you an older stamp than you expect, check
`git status` in `server/` before looking anywhere else.

### Server-only blocks

Chunks of the template that make no sense offline — the "download the offline
version" card, the missing-backend notice — are wrapped in markers:

```html
<!-- server-only: ... -->
   ...
<!-- /server-only -->
```

`build_local.py` deletes everything between them. **This is why some text
exists only in the server version.** The install instructions are the classic
example: they live in a server-only card, so users of the install build never
see them.

### Local-only additions

The reverse also happens: things that exist **only** in the local build.
There are no markers for these — `build_local.py` injects them from
constants, so the server template stays clean. Currently: the Pyodide boot
code and boot bar (`BOOT_JS`, `BOOTBAR_CSS`), the service-worker
registration (`SW_JS`), and the install bar (`INSTALLBAR_CSS` plus the
markup in the "first .wrap div" substitution).

The Numerical Solver's page has its own smaller set of the same kind:
`EQ_BOOT_JS`, `EQ_POST_JS`, `EQ_BOOTBAR_CSS` and `EQ_SW_JS`. Its boot bar
carries the app's own wording through the app's own `t()` keys, so the two
pages say the same sentence in thirteen languages without a second string
to translate.

The **install bar** is worth knowing about. It offers an Install button in
the page, because the browser's own affordance is close to undescribable:
desktop puts an icon in the address bar, Android hides it in a menu whose
wording changes between Chrome versions, and iOS has no install prompt at
all. Where the browser lets us drive it we show a button; only on iOS do we
fall back to describing the Share menu. It listens for
`beforeinstallprompt`, so it cannot appear on a page that could not really
be installed, and it stays hidden once the app is installed or the user has
dismissed it.

Because install and local are the same build, the bar appears in the
downloaded ZIP too, when it is served from `localhost`. That is intended —
it makes installing from the ZIP one click instead of a hunt.

### The template and the build script are coupled

`build_local.py` matches exact strings from the template and **asserts every
substitution matched**. Change the template's `<head>` and the build fails
loudly rather than silently dropping the icons or the service worker. That is
deliberate — an earlier silent no-op once shipped a build with no service
worker at all. If a build fails with "matched 0 times, expected 1", the
template changed and the script needs the same change.

### The interface speaks thirteen languages, from a dictionary in the page

Since #197 (31 Aug 2026) the app is available in English, Spanish,
Esperanto, French, German, Portuguese, Chinese, Japanese, Korean,
Indonesian (#202), Hindi and Bengali (#203) and Ukrainian (#206), chosen
from a `<select>` in the ribbon and remembered in `localStorage` under
`symbulator-lang` — the same shape as the theme, and applied by the same
head script before first paint.

**It is a client-side dictionary, and it has to be.** Two of the three
builds are static files with Pyodide in the tab and no Python outside it.
Flask-Babel, `gettext` or a per-language template would translate the
hosted app and leave the downloaded one in English, and would fork the
one-template property this file exists to protect. If you find yourself
reaching for a server-side scheme, you are about to break the offline
builds.

* The dictionaries are `repos/server/i18n/<lang>.json`. Since **#204**
  they are **not** inlined into the page: `tools/i18n.py pack` generates
  one file per language into `repos/server/i18n/dist/<lang>.js`, and the
  page loads only the language actually in use. The block between the
  `BEGIN/END i18n dictionaries` markers in each template's `<head>` is
  now a *loader and a version stamp*, still generated — **do not edit
  between the markers.**
* **The boot path and the switch path are deliberately different.** Boot
  uses a parser-blocking `<script>`; a language chosen later is fetched.
  That is because `applyLang()` must run before the page takes any
  element reference — it replaces `innerHTML`, and a deferred apply
  leaves those references on detached nodes. If you ever "tidy" the boot
  path into a fetch, that is the breakage, and it will not show up in a
  screenshot.
* The files must be in `sw.js`'s generated `BEGIN/END i18n` block, which
  `build_local.py` writes. A dictionary that ships but is not precached
  vanishes offline, dropping the reader back to English.
* The server serves them at `/i18n/<lang>.js` (root-absolute: the app is
  at `/`, the Numerical Solver at `/eqsheet/`); `build_local.py` rewrites
  the base to a relative path for the offline builds.
* **`en.json` is generated.** The English lives in the template markup and
  in the fallback argument of every `t()` / `tv()` call. At runtime the
  page snapshots its own markup and restores that for English, so English
  is not in the shipped dictionary at all and cannot drift.
* Every markup unit carries a `data-i18n` key; every runtime string goes
  through `t('key', 'English')`, `tv(...)` for one with slots, or `tSrv()`
  for a term the maths engine names.
* `py tools/i18n.py check` is the guard, and it is not optional after
  touching either template: it catches untagged units, stale keys,
  orphans, a translation that dropped an `id` or a `%{slot}`, and a `t()`
  call whose key is a variable. See `tools/README.md` for the full list.
* **`check` knows nothing about pixels, and the ribbon is where a
  translation actually breaks.** `banner.css` caps `.subbar nav` at one
  line-box with `overflow: clip`: a label too wide for the row does not
  wrap visibly and does not scroll — the overflow is silently gone, and it
  usually takes the Tutorial link with it. Ukrainian shipped past the
  first check this way (#203/#206). Measure `scrollHeight - clientHeight`
  on the nav, per language, at 375/481/520/768/1100px; 481 is the band to
  watch, being the narrowest that still shows the wide labels. The fix is
  nearly always the wording.

**The mathematics is never translated** — not the variable names, not the
element letters, not the decimal point, not the unit symbols. The answers
have to keep matching the tutorial's printed answers, and that agreement
was verified entry by entry across all 330 examples. `toLocaleString` is
pinned to `'en-US'` wherever it appears.

**The language must never enter `inputsSnapshot()` or a `.cir` file.** It
is a reader's preference, like the theme. #182 warns about unsaved edits
by comparing that snapshot, so anything in it the reader did not type
raises a phantom warning on every entry load.

### An answer may be several answers

From solver 0.4.6 a circuit can come back with **more than one solution**. An
expert-mode equation on a power is quadratic in its unknown, so `p_r1 = 0.025`
on a symbolic source is satisfied by `e = 5` and by `e = -5` alike. The solver
returns every root (`Result.solutions`, ranked so the physically likely one
leads); `symbulator_ui.solve_ui` formats each one and ships them as a
`solutions` array, with the top-level `nodes`/`elements`/`extras`/`values`
mirroring the first; the page renders `solutions[0]`, announces the choice
under the Run button and offers a picker under the Outputs heading.

Two consequences worth knowing:

- **Switching solutions never re-solves.** Every root is formatted once, when
  the circuit is run, and the picker only redraws. That is deliberate: a solve
  costs seconds in the Pyodide builds, and a menu that stalls is not a menu.
- **The Flask route enumerates its response fields by hand** (`app.py`), so a
  new key added in `symbulator_ui` reaches the local build automatically -- the
  Pyodide bridge serialises the whole dict -- but is silently dropped by the
  server variant until it is listed there too.

---

## Making a release

### When the solver version moves, the order is fixed

`repos/server/requirements.txt` pins `symbulator` from PyPI, so the server
variant cannot use a new API until it is *published*. The offline builds bundle
the wheel instead and are not subject to that — but the wheel's filename is
pinned in three places that have to move together.

1. Bump `symbulator/__init__.py`, write the CHANGELOG entry, run the tests.
2. `python -m build`, then `python -m twine check dist/...`.
3. **Publish to PyPI** — `python -m twine upload`. This is irreversible; a
   version number cannot be reused.
4. Copy the *same wheel file* into `repos/local/vendor/` and delete the old
   one. Use the artefact you uploaded, so the bytes PyPI serves and the bytes
   the offline build bundles are identical — and verify that by hash.
   (`vendor_pyodide.py` does **not** touch this one: it is a PyPI release, not
   part of the Pyodide distribution, and the script says so when it lists what
   else it found in `vendor/`.)
5. Update the three pins: `WHEEL` in `build_local.py`, the cache list in
   `sw.js`, and `symbulator>=` in `repos/server/requirements.txt`.
6. **Bump `CACHE_VERSION` in `sw.js`.** Without it, returning visitors keep
   the old build indefinitely.
7. `python build_local.py`, then `python build_zip.py --assets ../../local`.
8. Refresh `Symbulator/install_site` from the new ZIP.
9. Deploy `install` and `zip`, then prune the superseded wheel (above).
10. Server last: push, pull on PythonAnywhere, `pip install --upgrade
    symbulator`, Reload, and run a real solve.

PyPI's *simple index* lags the upload by a few minutes, so `pip` may briefly
insist the new version does not exist while the release page already serves it.
`--no-cache-dir` or a short wait fixes it; the release itself is fine, and its
recorded SHA256 can be checked at
`https://pypi.org/pypi/symbulator/<version>/json` without waiting.

### The ZIP

```
python3 build_zip.py --assets ../../local
```

The ZIP is three things glued together:

1. **This repo** — the app, the launchers, `README.txt`.
2. **Upstream artefacts** — Pyodide runtime, sympy/mpmath/**numpy** wheels,
   Python stdlib, MathJax. ~22 MB, too big for git, so they are **not in
   version control**. `--assets` points at any extracted copy of a previous
   ZIP; these files only change when Pyodide, MathJax or numpy is upgraded.

   > **numpy joined the bundle in Aug 2026, scipy in #208.** An `--assets`
   > folder taken from an older ZIP will not contain them, and the build fails
   > its own check (`sw.js` caches a file the ZIP has not got). Use a current
   > ZIP, run `vendor_pyodide.py`, or copy the wheels across. numpy is
   > required because `symbulator.plotting` imports it lazily: without it the
   > Plot card fails at the point of use with a bare `No module named
   > 'numpy'` — which is how the offline build shipped until it was caught.
   > scipy is required because `eqsheet.py` solves with
   > `scipy.optimize.root` and `least_squares`, and nothing in SymPy stands
   > in for the second: `nsolve` takes square systems only and no bounds, so
   > every one of #131's per-unknown restrictions would go.
   >
   > **`vendor_pyodide.py` is where these files come from**, and the one
   > record of it. The distribution is **Pyodide v314.0.5** — it tracks the
   > CPython it ships (3.14), which is why probing for a `0.2x` version
   > returns 404 on every filename and why #208 nearly concluded the source
   > was lost. Every wheel in `vendor/` hash-matches
   > `vendor/pyodide-lock.json`; `python vendor_pyodide.py --check` says so
   > without downloading anything.
3. **A `symbulator-local/` top-level folder** so unzipping is tidy.

`build_zip.py` verifies what it built — every manifest icon, every file the
service worker caches, every `<link>` **and `<script src>` in both pages'
heads**, `eqsheet.py`, `eqbridge.py` and the scipy wheel by name (nothing
links to those three), and the icon sizes Chrome requires. It refuses to
produce a ZIP that fails those checks.

**The ZIP is about 30 MB since #208**, up from 17.8. Exactly one published
string states that size, and it is easy to look for in the wrong places:
the app's *Installing from a file* card, which lives inside a
**`server-only` block**, so the sentence is on the server build alone and
both offline builds strip it. The landing page and `README.txt` state no
size at all. If the ZIP's size changes again, that one card is the whole
job.

### Deploying each variant

| Variant | How |
|---|---|
| **server** | Push to GitHub, then in a **PythonAnywhere Bash console**: `cd ~/symbulator_web`, `source ~/.virtualenvs/symbulator-venv/bin/activate`, `git pull`, and — whenever the solver version moved — `pip install --upgrade symbulator`. Then **Reload** on the Web tab, and load the site and **run a real solve**: a clean pull does not catch a version-mismatch crash, which only appears on an actual request. `/healthz` reports the running build, the build on disk and the solver version, so a pull without a reload is visible in one request. |
| **install** | `py deploy_symbulator.py install`, from `C:\Users\perez\Claude Code`. |
| **local** | Build the ZIP, then `py deploy_symbulator.py zip`. |

Both upload only what changed and verify over HTTPS afterwards. The `install`
target's local folder is `Symbulator\install_site`, which is **the ZIP's
contents minus the launchers** (`LICENSE`, `README.txt`, `start.bat`,
`start.command`, `start.sh` — a hosted copy is reached by URL and never uses
them). Refresh it from the ZIP you just built, or the two deployments of the
same build drift.

### One step that recurs every release

The deploy never deletes, so each release leaves its predecessor's wheel in
`vendor/` on the install host. Clear it, in a **PowerShell window** — the
confirmation is typed, deliberately, and cannot be answered from a script:

    cd "C:\Users\perez\Claude Code"
    py deploy_symbulator.py install --prune "symbulator-*.whl"

It deletes only files that match the glob **and** have no local counterpart,
shows both lists first, and asks you to type DELETE. Read the KEPT list before
you do: `.htaccess` and `.user.ini` are server config that lives only on the
host, and they appear there precisely because the two-condition rule is what
protects them.

Deploying the local build is **two jobs**, not one: the hosted copy at
`install.symbulator.com` *and* the ZIP. Doing one and forgetting the other
leaves them silently out of step.

---

## The two harnesses

`repos/server/tools/verify_lesson.py` checks the **answers** against the
tutorial's printed ones, over all 330 examples. It drives `app.py`.

`repos/local/verify_bridge.py` checks that the **two front ends agree**,
over the same examples plus ten refusal paths. It drives `app.py` and
`bridge.py` side by side.

They cover different failures, and #210 exists because the second one
did not. A bug in `bridge.py` shipped on 31 Aug 2026 — four sites
rendering `[object Object]` where a definition failed — while
`verify_lesson` stayed green, because `verify_lesson` never calls the
file the offline builds use. Run both after touching `symbulator_ui.py`,
`bridge.py` or `app.py`.

`verify_bridge.py` needs no Pyodide: `bridge.py` runs under ordinary
CPython. What it therefore does **not** cover is the browser around it —
the boot, the fetch of the `.py` files, the service worker. A green run
is not an offline test; it is a drift test.

## Verifying a deploy

"The command didn't error" is not verification. What actually catches problems:

- **Server:** load the site and run a real solve. A version mismatch between the
  app and the `symbulator` package only surfaces on an actual request — a clean
  `git pull` and reload will not reveal it. `DEPLOY.md` says the same thing.
- **ZIP:** compare the SHA256 of the published file against the local build.
  Sizes can coincide; hashes do not.
- **Install host:** compare each served file against the repo byte for byte. A
  partial upload looks completely healthy from a browser.
- **Installability:** only a real device settles it. Clear the site data first,
  or the old service worker serves a cached page and you have tested nothing.

Service workers and localhost: some embedded and sandboxed browsers refuse to
register a service worker over plain `http://localhost`, failing with an
unhelpful "unknown error when fetching the script" even though the file serves
correctly. Before chasing that as a bug, serve a known-good build the same way —
if it fails identically, the browser is the cause, not the build.

## Things that will bite you

**The preview tab caches `localhost` too, and it will lie to you about
your own edit.** On #183 the first probe of a freshly started dev server
reported the *old* JavaScript running, while `curl` against the same port
returned the new file: the tab had come up on a copy of the page cached from
an earlier session, no service worker involved (there was none registered,
and the cache storage was empty). Two minutes went into suspecting the edit.
The cheap settlement, in this order: `curl` the route and grep for the line
you added — that separates "Flask is not serving it" from "the tab is not
showing it" — then reload with a throwaway query (`/?cb=183`) and read the
running function back with `(''+fn)` before believing anything the page says.

And read that function back by matching the **exact** text you wrote. A
loose test lies in the other direction: `(''+syncSettings).includes(
"style.display")` came back true on the *old* code, because the RMS line
three rows up has always used `style.display`. It reported the fix present
when it was not.

**A template change is not verified until Flask has rendered it.**
`repos/server/templates/index.html` is a **Jinja** template; the offline
builds are static HTML generated from it and never pass through Jinja. On
30 Aug 2026 an HTML comment in it contained `{#`, which is Jinja's
comment-opener, with no closing `#}`. The template stopped parsing and the
server returned **500 on every page** — while `install.symbulator.com` and
the ZIP were fine, verified clean by hash, and `/healthz` stayed green
because it renders no template. Every check that had been run was
structurally incapable of catching it.

So: after touching anything under `templates/`, start the app and fetch
`/`, `/eqsheet/` and `/healthz` before calling it done. `py app.py` and
three requests take a minute. Watch for `{#`, `{%` and `{{` in comments
and in JavaScript especially, since none of them look like template
syntax to a reader.


**A translation is innerHTML, so it can break the page silently.** The
dictionary values are written straight into the elements they belong to.
A translation that loses an `id="plotKeyLabel"` takes the element the app
looks up with it; one that loses a `%{n}` slot loses the number the
sentence was about. Neither throws. `tools/i18n.py check` compares the
ids, links and slots of every translation against its English and fails on
a mismatch — run it, and do not hand-edit inside the `BEGIN/END i18n`
markers, which `pack` overwrites.

**The ribbon must stay one line, and a breakpoint cannot know when it
does.** What fits depends on the language: German's *Eingaben löschen* is
36px wider than *Clear inputs*. Worse, `banner.css` caps `<nav>` at one
line-box and *clips* what wraps inside it, so a crowded ribbon does not
grow — it drops the Tutorial link off the screen without a trace.
`syncLangMenu()` therefore measures: it writes the language names, asks
whether the row wrapped **or the nav had to clip**, and falls back to ISO
codes if either. A `<select>` sized `width: auto` is as wide as its widest
option, not the selected one, so all nine option texts change together.

**`CACHE_VERSION` in `sw.js`.** The service worker is cache-first. If you
change app files without bumping it, returning visitors keep the old build
forever — including the old manifest. Any fix you cannot see on a device you
have visited before is probably this. Bump it on every change to the local
build.

**PWA installability.** Chrome will only offer to install if the manifest
declares a **192px and a 512px icon**, plus HTTPS, a service worker, and
`display: standalone`. Desktop Chrome is lenient about the icons and falls
back to the favicon; **Android is not**, because it must build a launcher
icon and splash screen. This asymmetry — installable on Windows, no option on
Android — was a real bug, caused by a lone 335x335 icon. `build_zip.py` now
refuses to build a ZIP that would reproduce it.

Also: on Android there is **no install icon in the address bar**. That is
desktop-only. Mobile installs happen through the browser menu, and Chrome
will not offer it until the user has interacted with the page and spent a
little time on it. A phone showing no install option is very often either
that, a stale service worker, or the app already being installed.

**Maskable icons.** Android crops icons to arbitrary shapes and guarantees
only the middle 80%. `icon-maskable-512.png` scales the artwork to 60% of the
canvas so the crop cannot bite into it. Do not declare edge-to-edge artwork
as `maskable`.

**Icons are generated.** `icon.png` is the master. The `favicon*`,
`apple-touch-icon.png` and `icon-*.png` files are derived from it. If the
master changes, regenerate the set — and remember the server variant keeps its
own copies under `server/static/`.

**The server variant has no manifest, on purpose.** It needs the network, so
it must not advertise itself as installable. Offline installation is what the
install and local builds are for.

**Encoding and line endings.** The template contains curly quotes and em
dashes; every file read/write in the build scripts passes
`encoding="utf-8"` explicitly, because Windows would otherwise decode as
cp1252 and crash. `.gitattributes` forces LF, because `start.sh` and
`start.command` are run by `/bin/sh` — a CRLF checkout ships launchers that
fail with `bad interpreter: /bin/sh^M`.

**Shared modules.** `symbulator_ui.py`, `circuitbook.py` and (since #208)
`eqsheet.py` are byte-identical in the server and local repos, deliberately,
so the two front ends cannot drift. `build_local.py` copies them and fails
`--check` when they differ, so the copying is not a thing to remember.

**A number that is not a number cannot travel as JSON.** `json.dumps` writes
a bare `NaN` or `Infinity` for a non-finite float; it is legal Python and
**invalid JSON**, so `JSON.parse` and `Response.json()` both throw and the
page hangs with nothing on screen. `eqsheet.py` hit this on the live server
for as long as the Solver existed — a fresh sheet starts every variable
Unknown at zero, and a divider equation is 0/0 there. It sends `null` now.
Anything else that formats a float for the page wants the same guard.

---

## Layout on Roberto's machine

```
Claude Code/Symbulator/
  local/          extracted copy of the ZIP — also the --assets source
  local.zip       built artefact
  repos/
    server/       github.com/Symbulator/server
    local/        github.com/Symbulator/local   (this repo)
    solver/       github.com/Symbulator/solver
```

`build_local.py` needs `repos/server` and `repos/local` as siblings.
