# Symbulator — browser build

The whole simulator, running as static files. There is **no server**:
Python, SymPy and the `symbulator` package all run inside the visitor's
browser via [Pyodide](https://pyodide.org) (CPython compiled to
WebAssembly). Solving happens in their tab, not on your host.

Two consequences worth having:

* **It uploads anywhere.** No "Setup Python App", no subprocess
  permissions, no memory limits, no PHP-versus-Python question — any
  host that serves files will do, cPanel included.
* **It works offline and installs.** A service worker caches everything
  on the first visit, so afterwards it runs with no internet, and the
  page offers an Install bar to give it a desktop or home-screen icon
  (see the install bar notes in CLAUDE.md).

## Putting it online

Upload the whole folder to your web root (or a subfolder) and visit
`index.html`. That's the entire deployment.

Two server details matter:

1. **Serve `.wasm` as `application/wasm`.** Most hosts already do. If
   the page reports that the maths engine could not start, this is the
   usual reason — add to `.htaccess`:

   ```apache
   AddType application/wasm .wasm
   AddType application/json .webmanifest
   ```

2. **HTTPS is required for offline mode.** Service workers only run on
   `https://` (or `localhost`). Without it the site still works, it just
   won't cache or install. Both of your domains have certificates, so
   this is automatic.

Enabling gzip/deflate is worth it: the first visit transfers about
12 MB compressed rather than 18 MB raw.

## Running it locally

You cannot just double-click `index.html` — browsers block WebAssembly
loading from `file://` URLs ("Cross origin requests are only supported
for http, https"). Serve the folder over HTTP instead:

```
python -m http.server 8000
```

then open `http://localhost:8000`. For everyday offline use, though,
prefer installing the hosted version as an app: visit the site once and
use the browser's Install option. That needs no Python at all.

## What the visitor experiences

| moment | what happens |
|---|---|
| page appears | instantly — the form is usable straight away |
| first ~8 s | Python, SymPy and symbulator load **in the background**, with a small notice; typing a circuit takes about this long anyway |
| every solve after that | 20–50 ms for DC, a few hundred ms for AC or transient — faster than the server version, since nothing crosses the network |
| second visit | no download (cached); the ~8 s warm-up runs again, still in the background |
| offline | identical, once it has been visited once |

## Files

| file | purpose |
|---|---|
| `index.html` | the entire interface, and the code that boots Python — **generated**, do not hand-edit |
| `build_local.py` | regenerates `index.html` from the server version's template |
| `build_zip.py` | assembles the downloadable ZIP, and verifies the icons, cache list and head links before writing it |
| `CLAUDE.md` | how all three site variants fit together — read this first |
| `README.txt` | the readme that ships **inside the ZIP**, for end users (this file is for developers) |
| `start.bat`, `start.sh`, `start.command` | launchers shipped in the ZIP; they start `python -m http.server` and open a browser |
| `bridge.py` | thin adapter: JSON in, JSON out |
| `symbulator_ui.py` | **shared with the Flask build** — all solving, formatting, units, ordering |
| `circuitbook.py` | the `[Name]` circuit-file format, also shared |
| `examples.sym` | the examples dropdown; edit freely, no restart needed |
| `sw.js` | service worker: offline caching. Bump `CACHE_VERSION` when you change app files, or returning visitors keep the old build |
| `manifest.webmanifest` | what makes it installable. Its `icons` must include a 192px **and** a 512px entry, or Chrome on Android will not offer to install |
| `icon.png` | master artwork; the `favicon*`, `apple-touch-icon.png` and `icon-*.png` files are generated from it. Regenerate them if it changes |
| `LICENSE` | MIT |
| `vendor/` | Pyodide runtime plus the sympy, mpmath and symbulator wheels |
| `static/mathjax/` | typeset maths, served locally |

`symbulator_ui.py` and `circuitbook.py` are byte-identical to the ones in
the server project — deliberately, so the two front ends can never drift
apart. If you change one, copy it to the other.

## Changing the interface

There is only one interface, and it lives in the *server* project, at
`../server/templates/index.html`. This build's `index.html` is
produced from it:

```
python3 build_local.py            # regenerate index.html
python3 build_local.py --check    # exit 1 if it is stale
```

Every substitution the script makes asserts that it matched, so a change
to the template that breaks the transformation fails loudly instead of
quietly dropping a feature — which is exactly how an earlier build
shipped with no service worker registered. Edit the template, re-run the
script, bump `CACHE_VERSION` in `sw.js`.

## Updating the symbulator package

The wheel in `vendor/` is pinned. To move to a newer release:

```
pip download symbulator==X.Y.Z --no-deps -d vendor/
```

then update the filename in `index.html` (the `loadPackage` line) and in
`sw.js` (the `ASSETS` list), and bump `CACHE_VERSION`.
