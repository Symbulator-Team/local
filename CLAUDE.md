# Symbulator — how the whole thing fits together

Orientation for anyone (human or assistant) picking this up cold. It covers
all three site variants, not just this repo.

**This file is the canonical reference.** It is version-controlled, so it can be
corrected in the same commit as whatever it describes. A rendered copy of this
material exists as a shareable web page for people who would rather not clone
anything — if the two ever disagree, this file wins.

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
   the sympy, mpmath and numpy wheels, the Python stdlib and MathJax — about
   22 MB — are deliberately not in git. A release needs an extracted copy of a
   *recent* ZIP to draw them from, passed as `--assets`. See the note under
   "Making a release" about numpy, which older ZIPs do not have.

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

---

## Making a release

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

   > **numpy joined the bundle in Aug 2026.** An `--assets` folder taken from
   > a ZIP older than that will not contain it, and the build fails its own
   > check (`sw.js` caches a file the ZIP has not got). Use a current ZIP, or
   > copy the numpy wheel across. It is required because
   > `symbulator.plotting` imports numpy lazily: without it the Plot card
   > fails at the point of use with a bare `No module named 'numpy'` — which
   > is how the offline build shipped until it was caught.
3. **A `symbulator-local/` top-level folder** so unzipping is tidy.

`build_zip.py` verifies what it built — every manifest icon, every file the
service worker caches, every `<link>` in the page head, and the icon sizes
Chrome requires. It refuses to produce a ZIP that fails those checks.

### Deploying each variant

| Variant | How |
|---|---|
| **server** | Push to GitHub, then in a **PythonAnywhere Bash console**: `cd ~/symbulator_web`, `git pull`, `touch /var/www/symbulator_pythonanywhere_com_wsgi.py`. Then load the site and **run a real solve** — a clean pull does not catch a version-mismatch crash, which only appears on an actual request. |
| **install** | Upload the local build's files to the `install` directory on the web host. |
| **local** | Build the ZIP, upload as `symbulator.com/9/local.zip`. |

Deploying the local build is **two jobs**, not one: the hosted copy at
`install.symbulator.com` *and* the ZIP. Doing one and forgetting the other
leaves them silently out of step.

---

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

**Shared modules.** `symbulator_ui.py` and `circuitbook.py` are byte-identical
in the server and local repos, deliberately, so the two front ends cannot
drift. Change one, copy it to the other.

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
