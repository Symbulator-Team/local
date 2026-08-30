# Overnight brief — #197, the app speaks nine languages

*Written 30 Aug 2026 by the session that closed #196, for a session running
while Roberto sleeps. Paste the whole of this file as your first message.*

---

## What Roberto asked for

Two things, in the **app interface** (not the tutorial, not the landing
page — see Scope below):

1. **A language selection menu**, where the reader picks a language.
2. **Translations of the English interface text** into **Spanish, French,
   German, Portuguese, Chinese, Japanese, Korean** and **Esperanto**.

Nine languages including English. Esperanto was added a moment after the
other eight and is not a joke — treat it as seriously as the rest.

This is item **#197** in the running sequence (`repos/local/NEXT.md`). It
is large enough that it may want to be several numbered items; if you split
it, take **#197, #198, …** in order and say in each what it covers.

## Read these first

- `C:\Users\perez\Claude Code\CLAUDE.md` — the index across both trees.
- `C:\Users\perez\Claude Code\Symbulator\repos\local\CLAUDE.md` — canonical
  on the three builds, the release order and the deploy. **Read its
  "Things that will bite you" section in full**; two of the traps in it were
  paid for in production this week.
- `repos/local/NEXT.md`, the last ten or so entries, for the house style of
  a write-up and for what the settings card has just been through
  (#179–#196 all touched it).

## Scope — what is and is not in this job

**In:** every string a reader sees in the app itself. `templates/index.html`
(the app), `templates/eqsheet.html` (the Numerical Solver at `/eqsheet/`),
and the reader-facing notes and errors emitted by `symbulator_ui.py`.

**Out, and do not drift into these:**

- **The tutorial** (`learn.symbulator.com`, `Sym Docum/`), the **landing
  page** and the **three PDFs**. That is version 9's documentation — a far
  larger job with its own tree, its own build and its own printed answers.
  If the app links to a documentation page, the link stays as it is.
- **The 330 built-in example entries** in `repos/server/examples/`. Their
  titles and `note:` lines are tutorial content, tied line by line to the
  printed chapters, and every one has been verified against its chapter.
  Leave them in English. (Say so in the language menu's own note if you
  think a reader needs telling.)
- **The solver package.** 31 `CircuitError` messages and ~55 raises live in
  `repos/solver`, which is on PyPI and which the server installs by pin.
  Translating those means a release and a deploy-order dance. Out of scope
  tonight; note it as a follow-up item if you think it is worth doing.
- **Version X.** Merge nothing into it. Roberto or a later session will
  decide whether X wants this.

## The measurements, so you can plan rather than discover

Taken 30 Aug 2026 against the current template:

| | |
|---|---|
| `templates/index.html` | 4,972 lines; **530 visible strings, ~3,255 words**; 12 translatable text attributes |
| `templates/eqsheet.html` | 1,177 lines; **25 visible strings, ~88 words**; 7 text attributes |
| the page's own JavaScript | **~50 sentence-like literals** it writes into the DOM at runtime |
| `symbulator_ui.py` | 3,143 lines; 8 note/error emission sites that reach the reader |

So: roughly **600 strings and 3,400 words**, times eight target languages.
That is the real size of the night. Plan for it — if you cannot finish all
eight to a standard you would defend, **finish fewer languages properly**
and say plainly which ones are done. A half-translated interface that
silently falls back is much worse than six good languages and a note.

## The architecture constraint that decides everything

**There are three builds and one of them has no server.**

| build | what it is |
|---|---|
| server | Flask, at `symbulator.pythonanywhere.com` |
| install | the same page as static files, at `install.symbulator.com` |
| local | the same page again, in a downloadable ZIP, opened from disk |

The offline pair renders no Jinja and runs no Python except Pyodide in the
browser. **So the translation must be a client-side JavaScript dictionary
applied in the page — not Flask-Babel, not `gettext`, not a server-rendered
per-language template, and not one HTML file per language.** A scheme that
works beautifully on the server and cannot work offline is a wasted night;
this is the single most important sentence in this brief.

The theme switch is your model: it already persists a reader preference in
`localStorage` (`symbulator-theme`) and applies it before first paint. Do
the same for language, with the same care about the flash — an interface
that renders in English and then repaints in Korean will be noticed.

`<html lang="en">` at line 2 must become whatever is selected, for
screen readers and for CJK line-breaking.

## Roberto's own note: the server alone is enough, if that helps

He added, after reading the first draft of this brief: he had been thinking
of the languages for **the server version only**, and said that if it makes
the job simpler you may do the server alone.

Take the permission, but understand what it is worth before spending it,
because the honest answer is **it probably does not make anything simpler**:

- The app is **one template**. `build_local.py` generates the offline page
  from `repos/server/templates/index.html`; it is not a second codebase.
- The scheme this brief calls for is a **client-side dictionary**, and the
  server page is as static as the offline one once it has been rendered.
  A dictionary that works on the server therefore works offline **at no
  extra cost** — nothing needs porting.
- Excluding the offline build is *work*: you would have to strip the menu
  and the dictionary out of the generated page (there are markers for
  server-only content — see how the property mark is handled), and keep
  the two versions from drifting afterwards.

So the sensible reading of his note is as a **relief valve, not a design
choice**:

- **Do** use it if the offline build fights back late in the night — a
  failing `build_local.py` check, the ZIP, a Pyodide interaction. Ship the
  server, leave the offline pair in English, say plainly that you did and
  why. That is a good outcome and he has explicitly allowed it.
- **Do not** use it as a reason to pick a **server-side** scheme
  (Flask-Babel, `gettext`, per-language templates). That is the one path
  that genuinely makes the job harder: it forks the app into two divergent
  code paths, breaks the one-template property that
  `repos/local/CLAUDE.md` guards, and throws away the offline languages
  that the client-side design gives you free. If you find yourself
  reaching for it, re-read the section above.

If you do ship all three builds, the offline pair is the deploy you can do
yourself; the server is Roberto's pull. Which is a second small argument
for doing all three.

## Rules that are not negotiable

**Never localise the mathematics.** No decimal comma, no thousands
separator, no translated variable names, no translated element names, no
translated syntax. `v_1 = 8` reads `v_1 = 8` in every language. The answers
must keep matching the tutorial's printed answers exactly — that agreement
has been verified entry by entry across all 330 examples and it is not to
be broken by a locale-aware number formatter arriving through the side
door. The SI prefixes, the `∠` for phasors, `j` for the imaginary unit and
the unit symbols (V, A, W, VA, Ω) stay as they are.

**The language must not enter the `.cir` file or `inputsSnapshot()`.** It
is a reader preference, like the theme, not a property of a circuit. #182
made the app warn about unsaved edits by comparing a snapshot; anything you
add to that snapshot which the reader did not type produces a phantom
warning on every entry load. `localStorage` only.

**A template change is not verified until Flask has rendered it.** A `{#`
inside an HTML comment is Jinja's comment-opener and took every server page
down for real this week, while the offline builds — which never touch Jinja
— stayed green. After every template edit: start the dev server and load
the page. Non-ASCII text in a Jinja template is fine; `{#`, `{%` and `{{`
inside your new strings are not, and eight languages of new text is a lot
of new opportunity.

**Do not touch `banner.css`.** It is the one source of the lockup shared by
all five sites and it is guarded by `build_local.py`'s `check_banner()` in
this repo and by `build.py --check` in the docs tree. The ribbon's *text*
lives in the app markup and is yours to translate; the stylesheet is not.
Consider carefully whether the wordmark, the property mark and the ribbon
labels should translate at all — Roberto set that wording deliberately in
#174, and four other sites show it in English.

**`build_local.py` re-stamps the footer into the server template.** Every
local build leaves a change in `repos/server` as well. Commit both.

**Bump `CACHE_VERSION` in `repos/local/sw.js`.** It is at **v101**; go to
v102. Without it, returning visitors keep the old build indefinitely and
your night is invisible.

## Translation quality

Roberto is Panamanian. **He will read the Spanish himself**, so it must be
the best of the nine — natural, not translated-sounding, and using the
circuit vocabulary an engineer actually uses in Spanish.

For all languages, the terms of art matter more than the prose:

- **Thévenin** and **Norton** are names and stay, with the accent.
- *Phasor, mesh, node, branch, drop, source, impedance, admittance,
  two-port, transient, steady state, sweep, transfer function, unit step,
  op-amp, transformer* — each has a settled term in each of these
  languages. Use the settled term, not a literal rendering of the English.
- The **Numerical Solver**, **Plotting Tools**, **SPICE Translator**,
  **Expert Mode**, **Define**, **Evaluate** cards are the app's own
  furniture; translate the label, keep the concept.
- Mark anything you are unsure of. A short list at the end of your write-up
  of "lines a native speaker should check" is worth more than false
  confidence, and Roberto has a friend in Panama (Antony García, credited
  in #177) who might read the Spanish too.

Chinese: pick **Simplified** unless you have a reason, and say which.
Portuguese: pick **Brazilian** unless you have a reason, and say which.
Esperanto: use the standard technical vocabulary; the language has one for
electrical engineering.

## Verification — the app must still work, in every language

The house rule is *verify by measurement, not by eye*. Specifically:

1. **Solve in every language.** Load a circuit and solve it with each of
   the nine selected. The answers must be byte-identical across all nine.
   Automate this; nine manual passes will not happen at 3 a.m.
2. **Load an entry and check it comes back clean** — no phantom unsaved
   edit, in any language (this is the `inputsSnapshot()` rule above).
3. **The example harness.** `repos/server/tools/verify_lesson.py` posts
   entries through the real app and compares against the chapters' printed
   answers; `tools/README.md` explains it. A language change must not move
   a single answer. Run it on at least a few books, in a non-English
   language, and say which.
4. **Layout.** German and Spanish run long; Chinese, Japanese and Korean
   run short and break differently. Check the settings card, the ribbon and
   the cards at **375px** as well as desktop — the subtitle hides below
   480px and the property mark moves, and those thresholds were measured
   against *English* wording. Re-measure rather than trusting the numbers.
5. **Both themes**, since you will be adding UI.
6. **The offline build too**, unless you have taken the server-only
   fallback above: `build_local.py`, then open the built page and switch
   languages there. The offline page has no Flask, and a scheme that
   quietly depended on one fails exactly here — which is also the check
   that tells you *whether* you need the fallback, so run it early rather
   than at the end.

## When you are done

**Deploy the four cPanel sites yourself if — and only if — every check
above passes.** That is Roberto's standing arrangement: the cPanel deploy
script is the assistant's to run, and he has explicitly wanted overnight
work deployed before. The sequence, from `C:\Users\perez\Claude Code`:

```bash
py deploy_symbulator.py install
```

then rebuild the ZIP and `py deploy_symbulator.py zip`. `repos/local/CLAUDE.md`
has the full order, including refreshing `Symbulator\install_site` from the
new ZIP first — the two offline deployments drift if you skip that.

**PythonAnywhere is Roberto's**, always. Never log into it. Leave the
server pull for him and say clearly in your report that it is pending and
what it carries.

If anything fails and you cannot fix it soundly, **do not deploy**. Leave
the work committed on a branch, and say what is wrong. Roberto would rather
read a clear account of a problem in the morning than find a broken app.

## Your report in the morning

Write it as a `NEXT.md` entry in the house style (read the last few), and
say in your closing message:

- which languages are **done**, and which are not, without softening it;
- the lines you want a native speaker to check;
- what is deployed, what is pending his PythonAnywhere pull;
- anything you found along the way that should become its own numbered
  item — including whether the solver's 31 error messages are worth
  translating, and whether version X should take this.

One last thing. This is Roberto's project of twenty-seven years, public as
a beta for two days. Nine languages is a generous thing to want for it.
Make the Spanish good.
