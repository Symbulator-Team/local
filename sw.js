/*
 * Service worker: makes Symbulator work offline and installable.
 *
 * Everything the app needs is cached on first visit -- the Python
 * runtime, SymPy, SciPy, the symbulator wheel, MathJax and both pages
 * (the app and the Numerical Solver) -- so afterwards it runs with no
 * network at all. That is what turns this
 * from "a website" into "an app you can install", and it is why the
 * download is worth paying once.
 *
 * Bump CACHE_VERSION whenever the app files change, so returning users
 * get the new build instead of the cached one.
 */
const CACHE_VERSION = 'symbulator-v151';

const ASSETS = [
  './',
  'index.html',
  'eqsheet.html',
  'manifest.webmanifest',
  'favicon.ico',
  'favicon-16x16.png',
  'favicon-32x32.png',
  'apple-touch-icon.png',
  'icon-192.png',
  'icon-512.png',
  'icon-maskable-512.png',
  'logo.png',
  // ==== BEGIN examples ==== written by build_local.py; do not edit
  'examples/examples.json',
  'examples/Lesson_01.cir',
  'examples/Lesson_02.cir',
  'examples/Lesson_03.cir',
  'examples/Lesson_04a.cir',
  'examples/Lesson_04b.cir',
  'examples/Lesson_05a.cir',
  'examples/Lesson_05b.cir',
  'examples/Lesson_06a.cir',
  'examples/Lesson_06b.cir',
  'examples/Lesson_06c.cir',
  'examples/Lesson_06d.cir',
  'examples/Lesson_07.cir',
  'examples/Lesson_08.cir',
  'examples/Lesson_09.cir',
  'examples/Lesson_10.cir',
  'examples/Lesson_11.cir',
  'examples/Lesson_12.cir',
  'examples/Lesson_13.cir',
  'examples/Showcase.cir',
  'examples/The_Monograph.cir',
  // ==== END examples ====
  // ==== BEGIN i18n ==== written by build_local.py; do not edit
  'i18n/bn.js',
  'i18n/de.js',
  'i18n/eo.js',
  'i18n/es.js',
  'i18n/fr.js',
  'i18n/hi.js',
  'i18n/id.js',
  'i18n/ja.js',
  'i18n/ko.js',
  'i18n/pt.js',
  'i18n/uk.js',
  'i18n/zh.js',
  // ==== END i18n ====
  'bridge.py',
  'symbulator_ui.py',
  'circuitbook.py',
  'eqsheet.py',
  'eqbridge.py',
  'static/mathjax/tex-svg.js',
  'vendor/pyodide.js',
  'vendor/pyodide.asm.mjs',
  'vendor/pyodide.asm.wasm',
  'vendor/python_stdlib.zip',
  'vendor/pyodide-lock.json',
  'vendor/sympy-1.14.0-py3-none-any.whl',
  'vendor/numpy-2.4.6-cp314-cp314-pyemscripten_2026_0_wasm32.whl',
  'vendor/mpmath-1.4.1-py3-none-any.whl',
  // The Numerical Solver's own dependency (#208), and by a long way the
  // largest file here: 13.4 MB. It is cached with everything else on
  // purpose. Fetching it on demand would be cheaper for a reader who
  // never opens the Solver, and would also mean the Solver did not work
  // offline -- which is the one thing this file exists to guarantee.
  'vendor/scipy-1.18.0-cp314-cp314-pyemscripten_2026_0_wasm32.whl',
  'vendor/symbulator-0.5.26-py3-none-any.whl',
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_VERSION);
    // addAll fails the whole install if any single file 404s, which
    // would leave the app half-cached; take them one at a time and let
    // the page still work if something optional is missing.
    await Promise.all(ASSETS.map(async url => {
      try { await cache.add(new Request(url, { cache: 'reload' })); }
      catch (e) { console.warn('[sw] could not cache', url, e); }
    }));
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

// Cache-first: the app is a fixed set of files, and serving them from
// disk is both faster and what makes offline use work. Anything not in
// the cache falls through to the network.
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith((async () => {
    const hit = await caches.match(event.request, { ignoreSearch: true });
    if (hit) return hit;
    try {
      const res = await fetch(event.request);
      if (res && res.ok && new URL(event.request.url).origin === location.origin) {
        const cache = await caches.open(CACHE_VERSION);
        cache.put(event.request, res.clone());
      }
      return res;
    } catch (e) {
      // Offline and not cached: let the caller handle the failure.
      return new Response('Offline and not cached.', { status: 504 });
    }
  })());
});
