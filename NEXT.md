# Next build — accepted but not yet done

## #312 — the app's half of one sun-and-moon in the split view — **done 7 Sep 2026, live on the offline pair at cache v151 and on the server since Roberto's pull the same night**

Written up in `Documentation/NEXT_DOCS.md` #312, whose shell half is
live. Here: `html.embedded .theme-toggle { display: none }` beside #311's
rule, the click handler refactored into `setDarkTheme()`, and a
`message` listener that applies `{from:'symbulator-split', type:'theme',
dark}` only when framed and only from `learn.symbulator.com` or the
page's own origin. Never framed, the offline builds are untouched by it.

## #311 — no wordmark band inside the split view — **done 7 Sep 2026, live on the offline pair at cache v150; the server current since Roberto's pull the same night**

Roberto, 7 Sep 2026: *"in split view, you do not show the banner of the
documentation. That's great. Would it be possible to hide also the
banner of the app in split?"* The app pane is another origin, so the
shell cannot style it; the app detects being framed itself, the way the
docs page does (#224, `window.self !== window.top`, never a flag a
reload would lose), adds `embedded` to its root before first paint, and
one rule hides `.topbar`. The ribbon stays: inside the split view its
controls -- Clear, Collapse, the language, the theme -- are the ones a
reader reaches for, and the wordmark band is what the shell's own bar
already provides. The rule sits outside the shared `banner.css` block
on purpose: that block is the lockup five sites share, and this is one
host's decision about one frame.

Verified on the dev server by framing the page inside itself (the
frame-ancestors policy allows `'self'`): the framed copy carries the
class, its topbar is `display: none` and its ribbon sits at 0px; the
top-level page is untouched. The offline builds are never framed, so
nothing changes there.

## #309 — the theme swatch hidden on a phone — **done 7 Sep 2026, live on the offline pair at cache v149; the server current since Roberto's pull the same night**

Roberto, 7 Sep 2026, on #308's cost: *"Feel free to hide the theme button
in mobile."* One rule below 480px on `.palette-wrap`, the colour-theme
swatch beside the sun and moon; the sun and moon stay, since dark mode
matters on a phone, and the theme still applies from the stored
preference or a wider screen. Its width is what the nav needed: measured
at 375px on the dev server, both nav links are back in twelve of the
thirteen languages -- *App+Doku*, *Appli+Docs*, *Aplikasi+Dok*, ローカル+文書,
অ্যাপ+ডক্স … -- and Ukrainian was the one left showing *Застосунок* without *Док*.
Roberto asked how a Ukrainian reader would get back to the docs, and the
answer was that they could not: the ribbon's one-line rule had clipped
the link and the footer names no documentation. Fixed by wording, at
cache v149: the Ukrainian short labels became *Додаток* (app), *Скласти*
(collapse) and *Стерти* (clear), which is the 17px the nav was short by,
measured -- both links show in all thirteen languages at 375px. The
ribbon is one row (53px) in every language.

## #308 — *Collapse all cards* in the ribbon — **done 7 Sep 2026, live on the offline pair at cache v148; the server current since Roberto's pull the same night**

Roberto, 7 Sep 2026: *"add a link, next to 'Clear all inputs', reading
'Collapse all cards' (shortened to 'Collapse') that, when clicked,
collapses all the cards in the interface."*

A second `.subbar-action` button before *Clear inputs*, with its own dot
after it, so the two read as one group of page actions at the ribbon's
right-hand end. Two spellings through the pair `banner.css` already
switches at 480px -- *Collapse all cards* above, *Collapse* at or below
-- and translated in the twelve other languages in the same shape as
*Clear inputs* (`Alle Karten zuklappen` / `Zuklappen`, `Replier les
cartes` / `Replier`, 收起所有卡片 / 收起 …), plus the hover title. The click
closes every `<details>` inside a `.card`, the nested boxes included
(Settings, Expert Mode, the SymPy help), which is the one gesture that
gives back a page of headings.

Measured on the dev server at 375px: the ribbon stays one row in every
language tried, both new items showing, and a click took the open cards
from two to none. **One cost, flagged to Roberto**: the nav's one-line
rule hides a link that would wrap, and the new button's width is what
the second link needed in six languages -- at 375px German, French,
Portuguese, Indonesian, Japanese and Ukrainian now show *App* but not
*Docs* (English, Spanish and the rest keep both). Measured by hiding the
button and re-reading the nav: `Doku` comes back the moment it goes.
Resolved the same night by #309, at Roberto's word, by hiding the theme
swatch on a phone instead.

## #307 — the Walnut theme removed — **done 7 Sep 2026, live on the offline pair at cache v146; the server current since Roberto's pull the same night**

Roberto, 7 Sep 2026: *"kill the Walnut theme. It's too close to Earth."*
One row out of `tools/palettes.py`'s TABLE, `palettes.py write` to
regenerate both templates' theme blocks, the key out of both
`PALETTES` lists and `paletteNames()`, and `js.palette.walnut` out of
all thirteen dictionaries. Twelve themes remain. A reader who had
Walnut stored gets the default: `currentPalette()` already falls back to
`navy` for a name the list no longer has, so nothing else was needed.
`palettes check`, `i18n check` and the hidden-guard check clean; the
served page carries no `walnut` at all.

## #305 — one infinity sign in every result field — **done 7 Sep 2026, live on the offline pair at cache v145 and on the server since Roberto's pull the same night**

Roberto, 7 Sep 2026, on an ∞ with a tilde over it in a result: *"If
that's the mathematically correct symbol, we can leave it. But if you
are changing it in the results, then let's have it displayed consistently
in all other result fields in evaluate and solve as well."*

The tilde is SymPy's `zoo`, complex infinity -- an infinity of undefined
direction, which is what a nonzero quantity over zero becomes -- and
SymPy prints it `zoo` in text and `	ilde{\infty}` in LaTeX. The Results
card had always folded oo, -oo and zoo into a plain ∞ (`fmt`/`fmt0`);
Evaluate and Solve handed the value to SymPy's printers, so Bo2's 3.11's
`req` came out with the tilde in Evaluate and would have read `zoo` in
plain text. `_infinity_pair()` now does what the card does, in both
closures (`shown_pair`, `once`), sign kept for -oo. And an infinite
answer that had been *stored* (`values` holds `str(expr)`, so `zoo`)
read back as a symbol called zoo, because the restricted namespace
knows `oo` but not `zoo`; `_parse_answer` maps that one word first.

Verified: `1/x` at `x = 0` evaluates to ∞ and `req` stored as `zoo` to ∞
(both had printed the tilde, the second `zoo` in plain text). Solve's
`once` calls the same helper; an equation whose stored answer is
infinite has no finite root to report, so that path shows nothing rather
than a tilde.

## #300 — the Load-equivalent button moves under the Thévenin answers — **done 7 Sep 2026, live on the offline pair at cache v144; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 7 Sep 2026: *"Move the 'Load circuit equivalent?' button to
appear under the results of the Thevenin equivalent at the end of the
card."* The button and its warning left the Analysis card -- the tick
stays there, under the port nodes -- for a box at the foot of the Results
card, after the answers. `syncLoadEquivBox()` shows the box when the tick
is on and the answers on screen are a Thévenin run (`last`, not
`lastSolve`: an edited input stales the solve without taking the answers
off the screen, and the button should then go dead per #299 rather than
vanish); `syncLoadEquivBtn()` still governs the button itself. Clear all
hides both. The markup moved as a unit, so its four dictionary keys are
unchanged; `i18n check` and the hidden-guard check clean.

Verified on the dev server: the box is inside the Results card after the
answers; hidden before a run; shown with the seven rows after a Thévenin
run with the tick on; hidden when the tick comes off (the rows drop to
four) and back when it returns; the button dead after one edit, with a
click showing no warning; the box gone after Clear all.

## #299 — the Load-equivalent button follows the solve's freshness — **done 7 Sep 2026, live on the offline pair at cache v143; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 7 Sep 2026, on #292: *"the 'Load circuit equivalent?' should
not be active until the Thevenin simulation has been run. Until then,
deactivate it. Also, if any modifications are made to the input, the
button becomes inactive until run again."*

The page already tracks exactly that for the Run button -- `freshness.solve`,
set by `markFresh` after a run and cleared by `markStale` from every input
listener -- so the button reads the same state: `syncLoadEquivBtn()` runs
from `paintFreshness('solve')` on every transition and from
`activatePostSolve` once `last` holds the new run (markFresh fires before
`last` is replaced, which is why both are needed), and enables the button
only while the solve is fresh *and* is a Thévenin run with an `ino`. An
open warning closes when the button goes dead. The tick itself is not an
input that stales the solve, so ticking after a run leaves the button
live. The first version's inline *find it first* notice is gone, and its
key with it, from all thirteen dictionaries.

Verified on the dev server by driving the page: disabled before a run
and a click shows nothing; enabled after a Thévenin run; still enabled
after unticking and re-ticking; disabled after one character typed into
the description; enabled again after re-running; disabled on switching
the equivalent to resistance.

## #295 — three theme names: *Default*, *Warm Pink*, *Gray & Gold* — **done 7 Sep 2026, live on the offline pair at cache v141; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 7 Sep 2026, mid-train: *"In the theme list, please capitalise
'Pink' and 'Gold', and change 'Navy' with 'Default'."* The names live in
three places that must agree -- `tools/palettes.py`'s TABLE, and the
`paletteNames()` fallbacks in both templates (the Numerical Solver page
has its own copy, which is what `i18n check` caught: *two different
English texts for 'js.palette.navy'*). All three say *Default*, *Warm
Pink* and *Gray & Gold* now; `palettes.py write` rewrote the two theme
blocks. The twelve translations of *Navy* became each language's
*Default* (*Standard*, *Predeterminado*, *Par défaut*, *Padrão*,
*Defaŭlta*, 默认, デフォルト, 기본, *Bawaan*, डिफ़ॉल्ट, ডিফল্ট, *Типова*); the
pink and gold names keep their own languages' casing, which was already
what each language does with a colour name. The palette key stays `navy`
-- it is the stylesheet's attribute value and a stored preference, not a
word anyone reads.

Shipped with #291/#292 at cache **v141** (v140 had gone out minutes
earlier without it; ZIP 31,802,167 bytes, hash-verified on both sites).

## #292 — the th tool's load features, ported at last from version 8 — **done 7 Sep 2026, live on the offline pair at cache v141; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 7 Sep 2026: *"The features of the th() tool of Symbulator were
not properly ported from v8 to v9."* Version 8's `th`, once it had the
equivalent, asked *"If you are planning to analyze a load connected to
this equivalent, we can give you the description of the equivalent
circuit and some key equations that will help. Interested? [y/n]"* and on
yes defined `irl`, `vrl` and `prl` in the variable `load` and wrote the
equivalent circuit into `eqcir`. None of that had crossed to version 9;
the tutorial had been made to work around the gap with hand-typed
`vth/(req+2)` expressions -- the *"nonsense added by the AI"* that #293
removes on the docs side.

What the app does now, to his brief:

* **A question under the two node boxes**, shown only when the
  equivalent asked for is *Thévenin / Norton*: *Are you running a problem
  with a load connected to this equivalent circuit?* Unticked, the app
  behaves exactly as before.
* **Ticked, Results shows three more answers under the four**, each a
  function of `load`, in the calculator's words: `irl` *current in load*,
  `vrl` *voltage drop in load*, `prl` *power consumed in load*. The
  formulas are v8's, decoded from `calculator/decoded/v8_programs.txt`
  and not re-derived: `ino*req/(load+req)`, `load*ino*req/(load+req)`,
  `load*ino^2*req^2/(load+req)^2` in DC; the same with `zeq` in AC and
  FD, the power as the real part of S = V I* -- `prl` for RMS phasors,
  `aprl` (*average power consumed in load*) with the extra half for peak
  ones, as v8 named them. They are computed in `symbulator_ui.py`
  (`_load_answers`) on every th run and returned apart from the four, in
  `load_extras`, so the page decides whether to show them and ticking or
  unticking after a solve redraws Results without solving again. They are
  in `values` either way, so **Evaluate** takes `irl` with `load = 2` in
  **Conditions** whether or not the tick is on -- B11's 9.6 gives 3/2,
  and 0.0588 at 100, the book's .059. A source with nothing in series
  (the op-amp case, `ino` unbounded) has no load formulas through `ino`,
  so the list is empty rather than three infinities. No solver release:
  the solver's `th()` is untouched, so the server variant needs its pull
  and nothing from PyPI.
* **Beneath the tick, a button: *Load circuit equivalent?*** It asks
  first, inline rather than in a browser dialog so it translates and the
  circuit stays visible: the equivalent will overwrite the Circuit
  Description, Define and Expert Mode fields and switch the analysis to
  *Solve circuit* -- cancel and save first if the circuit is unsaved.
  Cancel hides the warning and nothing moves. Proceed clears the
  description, Define and the three Expert Mode fields (and the Enable
  tick), sets the analysis to *Solve circuit*, and writes v8's `eqcir` in
  version 9's fields --

      jN,0,n,iNo
      rE,n,0,rEq
      rL,n,0,load

  with **Define** holding `iNo=` and `rEq=` at their **exact** values
  from `values`, not the rounded display (RM3's 9-8 gets `iNo=-9/25`,
  `rEq=84`), and `load=` too if a `load = …` line was standing in Define
  or in Evaluate's Conditions -- the calculator's `load` variable
  surviving into its eqcir. In AC and FD the second line is `zEq`, a
  complex resistor value being legal there. The answers on screen are
  cleared, as they are whenever a circuit is loaded over another; the
  Define box opens; the inputs count as edited, so *Update* offers itself.
  **The button is disabled until a Thévenin run has been made, and
  disabled again the moment any input changes** (Roberto, later the same
  evening, #299): it writes `ino` and `req`, so it lives only while a
  fresh Thévenin result is on screen, following the same freshness the
  Run button reads. The inline *find it first* notice of the first
  version went with that.

Element names are lower-cased by the parser, so `rE` becomes `re`, which
is not a collision -- the parse and a DC solve of the loaded equivalent
were run first. `irl`/`vrl`/`prl` are typeset `i_{rl}`, `v_{rl}`,
`p_{rl}` (`TEXNAME`), and their four labels joined the engine vocabulary
(`srv.*`), translated in the twelve other languages along with the
question, the button, the warning, *Proceed*, *Cancel* and the two new
Evaluate placeholders (#291); `i18n check` clean, 650 keys.

**The tick is saved with the entry** (Roberto, the same day: *"Save the
tick to input files, and update built in examples"*): a `with_load`
key, yes/no, written beside the port nodes only when on, read back as a
boolean like `si` and `units`, restored by the loader and cleared by
Clear all; `check_export_fields.py` sees it in `inputsSnapshot()` and
round-trips it. The format reference names it after `kind`, in all
thirteen languages. The eleven built-in entries whose problem connects a
load -- B11's 9.6 and RM3's 9-8, Bo2's 3.10, 3.5, 3.7 and Drill 3.7,
RM3's 9-7, 9-13 and Practice Problem 9.5, B11's 9.15, AS2's 4.8, and
Lesson 5's TR5 Figure 4-32 -- carry `with_load: yes`, so they open with
the question ticked and the load answers on screen.

Guards: `check_hidden_guards.py` clean (the new `[hidden]` boxes have no
author `display`); `build_local.py --check` runs its JavaScript check
clean and then reports STALE, as it must until the build; the bridge
passes the response through whole, but `app.py` lists its fields by hand
(its own comment warns of this) and needed `load_extras` added -- found
because the first browser run showed four rows, not seven. The
`evaluate fetch` rewrite rule in `build_local.py` was updated for #291's
change to the request body.

Verified on the Flask dev server by driving the page: the question is
`display: none` for *Solve circuit* and for the other two equivalents and
`block` for Thévenin; ticked, B11's 9.6 shows seven rows with the seven
labels, unticked four, re-ticked seven; `irl` at `load = 2` evaluates to
3/2; the button before a run shows the *find it first* notice; after a
run, Cancel leaves the description as it was, Proceed leaves
`jN,0,n,iNo / rE,n,0,rEq / rL,n,0,load`, Define `iNo=3 / rEq=2 / load=2`
(the 2 carried from Conditions), Expert Mode empty and off, the analysis
*Solve circuit*, the results cleared.

The example books follow the chapter (#293): B11's 9.6, Bo2's 3.10, 3.5,
3.7 and Drill 3.7, RM3's 9-7, 9-13 and Practice Problem 9.5, B11's 9.15,
AS2's 4.8 and Lesson 5's TR5 Figure 4-32 now carry `evaluate: irl` (or
`vrl`, `prl`) with an `evaluate_conditions: load = …`, and RM3's 9-8
follow-up entry is the circuit the button writes, with its two
`defines:`. `verify_lesson.py --quiet`: Lesson_04a 7 entries, 0
problems; Lesson_04b 46 entries, the one standing deliberate failure
(Bo2's 3.11) and nothing else.

**To ship**: bump `sw.js` `CACHE_VERSION` to v140, `build_local.py`,
`build_zip.py --assets ../../local`, `stage_install_site.py`, the two
cPanel deploys; the server needs its pull (`symbulator_ui.py`, `app.py`,
the template, thirteen dictionaries, the examples), no `pip`. X will
take it on its next merge.

## #291 — the Evaluate card is active before any solve — **done 7 Sep 2026, live on the offline pair at cache v141 with #292**

Roberto, 7 Sep 2026: *"We need to make the Evaluate card active even
without a circuit solved, because people may need to use the pr function
to reduce resistors. So please make it active always."*

`evaluate_ui` never needed a solve -- `pr(100, 220)` with an empty
answer set already came back 275/4 -- only the page held the card back:
`activatePostSolve` enabled it and `clearResults` disabled it, and
`evaluate()` returned early with no `last`. Now the field, the button and
the Conditions box start live with their working placeholders, the card
is never `inactive`, and with nothing solved the request carries an
empty `values` and no domain, so the evaluator works on the expression
and Define alone. The label's hint says so: *Works with no circuit
solved, too: `pr(100, 220)` is the parallel of two resistors.* The
Solve-equations card still waits for a solve, and the *solve a circuit
first…* wording stays for it. Two `js.eval.*` keys became markup
placeholders; the twelve translations moved with them.

Verified in the browser with nothing solved: `pr(100,220)` evaluates to
275/4.

## #289 — the tool answers' labels in lower case, like every other label — **done 6 Sep 2026, live on the offline pair at cache v139; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 6 Sep 2026, reading an equivalent-resistance result: *"the label
says 'Equivalent resistance' ... the other labels use lower case ... make
all labels be lower case, unless they refer to a proper name like
Thevenin or Norton."*

The engine's element and port labels were already lower case (*current
through*, *voltage drop*, *open-circuit input impedance*); the one table
that was not is `_TOOL_LABELS` in `symbulator_ui.py`, the th/er tool's
five named answers. Three change -- *equivalent resistance*, *equivalent
impedance*, *maximum deliverable power* -- and *Thevenin voltage* and
*Norton current* keep their capitals for the names. A sweep of every
`srv.` word in `en.json` found no other capital.

The engine's words are the dictionary keys, so the three moved to new
keys and the twelve translations moved with them, first letter lowered
where the language has case; **German keeps its capitals**, since
*Ersatzwiderstand* is a noun. `i18n check` clean. `symbulator_ui.py` is
shared into the offline build by `build_local.py`; shipped at cache
**v139** (ZIP 31,793,970 bytes, hash-verified; build `2026-09-05 06:35
UTC`), both offline sites. The server's own `symbulator_ui.py` and
dictionaries change with the next pull.

## #286 — Lesson 3's four `is1` entries say `is`, as the book now does — **done 6 Sep 2026, live on the offline pair at cache v138; the server current since Roberto's pull of 7 Sep 2026**

From the docs session, 6 Sep 2026: four entries in
`repos/server/examples/Lesson_03.cir` used `is1` as the symbolic value of
a current source where the chapter now prints `is` -- which the app
accepts, since the Python-keyword guard bans an *element* named `s`, not
a value symbol called `is`. Renamed in every field that carried it,
word-bounded so nothing else moved: B11's Example 6.21 (the circuit line
and `unknowns:`), TR5's Figure 4-4, Bo2's Example 1.11 (Symbolic), and
TR5's Example 4.5 (Symbolic), whose `jd,b,a,β*is1` became `β*is`. Eight
lines in the book; `tools/Lesson_03.expected.json` moved with it, six
occurrences in three answers, since the chapter and the JSON move
together.

Verified: `verify_lesson.py Lesson_03 --quiet` -- 48 entries, 0 problems
(the two "book names not found" entries, 6.22 and RM3's 9-12, are the
standing ones and untouched); `check_example_plots.py Lesson_03` -- its
one plot runs. `build_local.py` regenerated `repos/local/examples/`;
cache **v138**, both offline sites, hash-verified. The server serves the
examples from its own checkout, so the four entries reach
`symbulator.pythonanywhere.com` with Roberto's next pull.

## #285 — the app's footer, two lines, no copyright sign — **done 6 Sep 2026, live on the offline pair at cache v137; the server current since Roberto's pull of 7 Sep 2026**

Roberto, 6 Sep 2026, after ruling that every repository is open source:
*"Let's remove the copyright, then. Let's use this footer for the app in
all its forms"* --

    Symbulator by Roberto Perez-Franco (1999–2026) · Release 2026-09-05 04:22 UTC
    symbulator.com · Free and open-source under the MIT licence · Runs on Python+SymPy

His words exactly. Gone with it: the © sign, the Facebook, GitHub and
PyPI links, *results are symbolic*, and the version numeral -- the foot
names no version now, only the release stamp. `symbulator.com` stays a
link. The first line and the link are `notranslate`; the licence phrase
is the one translation unit, re-keyed by `i18n.py tag`
(`free-and-open-source.d231`) and translated in all twelve languages.

**The stamp moved, and two readers with it.** `build_local.py`'s
`STAMP_RE` and `app.py`'s `_BUILD_RE` both keyed on *Symbulator 9
version*; both now key on *Release*, and both were proved to find the
stamp exactly once in the new template before anything else was run.
`/healthz` therefore keeps reporting the build. `branding.py`'s note on
the footer (the ruling of 4 Sep 2026 that a fork's foot reads the same)
was reworded to the new line; the ruling stands.

**A third reader turned up on the deploy.** `Deploy/deploy_targets.ini`
verifies the install page by the marker *Symbulator 9 version*, and the
first deploy uploaded every file correctly and then reported FAIL on that
line -- the right outcome, since the marker names the footer. It now
reads *Symbulator by Roberto Perez-Franco*, and the re-run verified
clean. Shipped with #282 at cache **v137** (ZIP 31,794,098 bytes,
hash-verified; build `2026-09-05 05:40 UTC`).

## #283 — every repository carries the MIT licence — **done 6 Sep 2026, nothing to deploy**

Roberto asked whether *Symbulator © 1999–2026 Roberto Perez-Franco* still
made sense now that the code is open source, and ruled: *"All repositories
are open source, for everything."* The line stays -- MIT works by
copyright and asks that the notice be kept -- and the footer's next line
already says *Free and open-source software under the MIT licence*, so
the page needed nothing. What was missing was the file: `server` and the
docs repository were public with no `LICENSE`, which reads as all rights
reserved. Both now carry the same MIT text as `solver` and `local`,
byte-identical, committed and pushed. Not a build, not a deploy.

## #282 — two theme names: *Gray & gold*, *Contrast* — **done 6 Sep 2026, live on the offline pair at cache v137; the server current since Roberto's pull of 6 Sep 2026**

Roberto, 6 Sep 2026: *"Change 'Gray and gold' to 'Gray & gold', and 'High
contrast' to 'Contrast'."* The table in `tools/palettes.py`, the two
templates' picker calls and the dictionaries. The twelve *Contrast*
translations shortened to match (*Contraste*, *Kontrast*, *대비* ...);
*Gray & gold*'s keep each language's own conjunction. `palettes check`
and `i18n check` clean. The keys (`graygold`, `highcontrast`) and the
stored values are unchanged, so a reader's saved choice survives.

Asked the same day whether the theme could be *"a setting that is
remembered across sessions, like the mode"*: it already is -- stored as
`symbulator-palette` beside `symbulator-theme` and applied by the head
script before first paint (#278). Proved on the live install site by
choosing Burgundy, reloading, and reading the root attribute and the band
colour back: `burgundy`, `#4f1424`. If it does not persist somewhere, that
is the server before its pull (no picker there yet), or a browser that
blocks storage -- the mode would fail there the same way.

Shipped with #285 at cache **v137**.

## #280 — answers set at full size: display-style maths in the results — **done 6 Sep 2026, live on the offline pair at cache v136; the server current since Roberto's pull of 6 Sep 2026**

Roberto, 6 Sep 2026: *"when there are mathematical expressions that have
nominator and denominator, the font is shrunk to make it fit in the fix
height. But there's no need for that. I'd rather enlarge the space ...
making the spaces taller, but also making the blocks longer, fitting one
per line instead of two per line when needed."*

**Measured first.** Nothing in the stylesheet scales a result, and no
height is fixed: a `.result-row` and an `.elcard` are both sized by their
content, and the cards are `flex: 0 0 auto` with a 250px minimum, so a
wide card already widens and wraps to a line of its own. What shrinks a
fraction is TeX itself: every result was typeset as inline maths,
`\( ... \)`, and inline (text-style) TeX sets a numerator and a
denominator at script size so the fraction fits one text line. That is
the "shrunk font", and it is the only shrink there is.

**The fix is one word in four places**: `\displaystyle` at the head of
every result the app typesets -- the Results card and the element cards
(one helper), the Equations card, Evaluate, and the Mini-Tools. The plain
text fallback is untouched, and the Numerical Solver typesets nothing.

Measured on the Flask server with a symbolic divider (`e1,1,0,vs`,
`r1,1,2,ra`, `r2,2,0,rb`, `r3,2,0,rc`), same page width, before and after:

| | before | after |
|---|---|---|
| node 2's fraction, rendered | 143 × 24 px | 199 × 40 px |
| its row | 52 px | 66 px |
| the widest element card | 250 × 279 px | 261 × 322 px |
| cards per line at 798 px | 3 then 1 | 3 then 1 (each wider) |

So the rows are taller and the cards wider, and nothing had to be told to
wrap: the layout was already the reader's, only the type was not. On a
phone (≤ 520 px) an `.el-item` keeps its horizontal scroll for a fraction
wider than the screen, as before.

Shipped with #279 at cache **v136** (ZIP 31,794,299 bytes, hash-verified; build
`2026-09-05 04:22 UTC`), both offline sites the same evening; the server
pull is Roberto's, and it is a real pull (the template changed).

## #279 — Expert Mode's three labels say *equation(s)*, *unknown(s)*, *condition(s)* — **done 6 Sep 2026, live on the offline pair at cache v136; the server current since Roberto's pull of 6 Sep 2026**

Roberto, 6 Sep 2026: *"In the interface, in the Expert Mode, add
parentheses around the s in 'Add equation(s)', 'Add unknown(s)' and 'Add
condition(s)'."* Then: *"apply this only to the English one."*

Three words in `templates/index.html`. The English text is the key, so
`i18n.py tag` gave the three labels new keys (`add-equation-s-one.e3a4`,
`add-unknown-s-one.7f55`, `add-condition-s-one.7e29`) and the twelve
translations moved under them unchanged -- *Agregar ecuaciones*, *Ajouter
des équations* and the rest keep their plain plurals, per the ruling.
`i18n check` clean. Shipped with #280 at cache **v136**.

## #278 — thirteen colour themes, each with light and dark, and the scorpion on a transparent ground — **done 6 Sep 2026, live on the four cPanel sites at cache v135; the server current since Roberto's pull of 6 Sep 2026**

Roberto's brief, 6 Sep 2026: *"I would like to allow the user to select
a theme. Each theme would have a dark and a light versions, switchable
using the toggle. The default theme would be the light and dark navy
blue currently in place."* He listed seven alternatives, asked for three
more (burgundy, forest, pastels), accepted a fourth proposed here (high
contrast), named all twelve, and then added Walnut (the palette of Leonardo's
notebooks), thirteen. Settled over a rendered sheet of
twenty-six miniatures of the app, one per theme and mode; the sheet and
the script that generates it are kept in
`C:\Users\perez\Claude Symbulator\Notes\themes_2026-09-06\` — edit
`make_themes.py`'s table, run it, and the sheet is regenerated. **The
palettes below are the spec**; the sheet is what Roberto approved.

### The decisions

- **The sun-and-moon toggle keeps its job.** It switches light and dark
  *within* the chosen theme. A second control picks the theme.
- **The control is a round swatch beside the toggle in the ribbon**, the
  toggle's size and ring, whose dot is the theme's band colour and numeral
  colour split diagonally. Behind it, a native `<select>` built the way
  the language menu is (#201): thirteen entries are too many for a custom
  menu and a phone renders a select as a proper picker.
- **Stored as `symbulator-palette` in `localStorage`**, beside
  `symbulator-theme` and `symbulator-lang`, applied by the head script
  before first paint like dark mode is. A root attribute `data-palette`;
  Navy is the absence of the attribute, so today's page is byte-for-byte
  the default.
- **The banner keeps its theme colour in both modes**, as it does now.
  `banner.css` is **not edited**: it already reads `--navy`, `--navy-2`
  and `--sky` with fallbacks, so a theme paints the bands by setting three
  variables on the root. The guarded copies stay identical. Two banner
  colours are literals in `banner.css` today and stay so for Navy but need
  variables with fallbacks for the others: the subtitle `#b7c3d6` and the
  ribbon link `#dbe6f5`. That is a two-line change to the shared file
  (`var(--banner-sub, #b7c3d6)`, `var(--banner-link, #dbe6f5)`),
  propagated to all three consumers as the banner section of the root
  `CLAUDE.md` describes.
- **The results panel takes the theme's tint.** Today `.lcd` and
  `.elcard` are hard-wired blue in both modes. Each theme supplies seven
  panel values.
- **Both pages**: `index.html` and `eqsheet.html` share the banner and
  the store, so the Numerical Solver follows the theme too.
- **Names are translated, Firefly included** (Roberto: *"I'd suggest
  translating the word 'firefly' unless it doesn't exist in the
  language"* — luciérnaga, luciole, Glühwürmchen, vagalume, and the
  English word where a language has none). Thirteen names plus the picker's
  label in all thirteen dictionaries.
- **Firefly** was retuned at Roberto's ask from a Matrix-green terminal to
  *a firefly in a dark forest*: night-wood bands, the insect's yellow-green
  glow for the numeral, keyline and readout, a moss-lit light side.
- **The scorpion loses its navy ground** (Roberto, 6 Sep 2026: *"convert the
  navy background into an alpha channel, so that only the white drawing
  remains, and the background appears as the colour of the banner"*).
  `Notes/themes_2026-09-06/logo_alpha.png` is the converted file: each
  pixel unmixed as a blend of white and the corner navy, white kept and the
  blend kept as alpha, so the anti-aliased edges survive; recomposited on
  navy it reproduces the original to within one level per channel. **It
  replaces every copy of the logo in the build**: `repos/server/static/logo.png`
  (which `build_local.py` carries into the offline pages), the landing's and
  learn's copies in the docs tree, and the icons if they carry the same
  ground. On Navy nothing changes to the eye.
- **Walnut**: the palette of Leonardo's notebooks. Parchment page,
  iron-gall-ink bands, red-chalk accent; the one theme whose light ground is
  a colour rather than an off-white. Named Leonardo for an hour.
- **The menu is in chromatic order** (Roberto, 6 Sep 2026: *"sort the
  themes chromatically"*): Navy first as the default, then round the wheel
  — Violet, Pastels, Warm pink, Burgundy, Brick, Walnut, Earth, Gray and
  gold, Firefly, Forest, Turquoise — and High contrast, the achromatic one,
  last. The tables below and the sheet are in that order.
- **Gray and gold** is the one theme with a gradient: a brushed sheen on
  the top band (`#4a5059` to the band colour over 70%), and the ribbon
  the reverse. **High contrast** drops the panel's gradient and both
  inset glows and the card shadow.
- **Pastels bends the lockup on purpose**: its bands are a dusty lavender,
  the only bands that are not dark, just deep enough for white text; and
  its Solve button is the only one with dark lettering. Roberto saw it and
  kept it.

### The palettes

Twenty-two values each. Banner (five): top band, ribbon, numeral and
keyline, subtitle, ribbon link. Panel (seven): gradient top, ground,
border, row line, readout ink, dim text, element name. Page (ten, per
mode): ground, card, ink, muted, accent, accent ink, rule, field, field
border, button hover. The app's other variables (notices, warnings, code
and callout backgrounds, placeholder, focus ring) derive from these at
build time and are not specified here.

| Theme | Banner | Panel |
|---|---|---|
| Navy (default) | `#203864 #2a4576 #8ec7f5 #b7c3d6 #dbe6f5` | `#102338 #0d1e30 #081525 #173352 #8ecbff #4a7098 #6fb8f0` |
| Violet | `#363a80 #42478f #b9bdff #bfc1e6 #e0e1f8` | `#1b1d44 #14163a #0a0b22 #2b2e60 #c6c5ff #6b6ca8 #a3a1ff` |
| Pastels | `#7f74ad #8d83b8 #ffe9a8 #ece7f7 #f6f3fc` | `#47406c #3e3860 #2e2a48 #565080 #c8f5dc #9a93bf #f7c7d9` |
| Warm pink | `#5c1a45 #6c2654 #f3a6d3 #d9b3cb #f3dbe9` | `#2b0f22 #21091a #12050e #43203a #ffb6de #8a5a78 #f08cc4` |
| Burgundy | `#4f1424 #5f1d30 #f0a9b8 #d4aab4 #f3dae0` | `#2a0c14 #200810 #100408 #44182a #ffb8c6 #8c5868 #f28aa0` |
| Brick | `#6a2c20 #7b392c #f4b79e #d8b3a6 #f5e1da` | `#2d1611 #23100c #120705 #4a2820 #ffbfa6 #8f5c4c #f39678` |
| Walnut | `#3a2718 #4a3323 #e6cf9a #cdb992 #eadcbd` | `#33251a #281c13 #140d08 #4a3826 #efd9a6 #8a7455 #d9a56b` |
| Earth | `#4a3a2a #594736 #dcbb87 #cdbca4 #ecdfcc` | `#2a2016 #201810 #100b07 #43352a #eacd9e #8a7250 #d7b078` |
| Gray and gold | `#3b4048 #484e57 #d9aa4c #b8bec6 #e2e6ea` | `#23282e #1a1e22 #0d0f11 #343a41 #f0c070 #7d7466 #d9aa4c` |
| Firefly | `#0a1810 #122419 #e3f56b #8fb09a #d2e8c8` | `#0e2418 #081a10 #030d07 #1a3a26 #e8ff7a #4e7a56 #b9ec5c` |
| Forest | `#1e3d2b #294a36 #a8d8a0 #b3c9b8 #dcebdf` | `#14301f #0f2418 #061209 #1f4430 #b8ecb8 #5a8a66 #8fd49a` |
| Turquoise | `#0f4a58 #175a69 #7fe3d6 #a9d3cf #d6f1ec` | `#0b2f36 #08252b #041418 #164048 #8ef0e2 #3f8a84 #5fd6c8` |
| High contrast | `#000000 #111111 #ffd400 #dddddd #ffffff` | `#000000 #000000 #ffffff #444444 #ffffff #bbbbbb #ffd400` |

| Theme | Light page | Dark page |
|---|---|---|
| Navy | `#f4f6fa #ffffff #1c2330 #5b6472 #2f5fa8 #ffffff #e2e5ea #fbfcfd #cfd6df #1f4a86` | `#12161d #1b212c #e4e8ee #97a3b6 #5b96e0 #0d1420 #2b3341 #11161e #38424f #4a86d0` |
| Violet | `#f5f5fc #ffffff #1f1f38 #5f6180 #5652c8 #ffffff #e0e1f0 #fbfbff #cbcde6 #4340a8` | `#13142a #1c1d38 #e7e7f6 #9c9ec4 #9d9bff #12132a #2d2f52 #0f1024 #3b3d66 #b4b2ff` |
| Pastels | `#f8f6fb #ffffff #3a3550 #7a7494 #e79ab0 #3a3550 #e8e3f2 #fcfbfe #d8d1e8 #f0b0c2` | `#221f30 #2c2840 #ece8f5 #aaa3c4 #f2b8c8 #221f30 #3f3a56 #1d1a2a #4c4666 #f8cbd8` |
| Warm pink | `#fbf5f8 #ffffff #2a1a24 #6f5866 #b02a72 #ffffff #ecdde5 #fdfafc #dcc6d3 #8f1f5b` | `#1a1015 #24161f #f2e6ed #ad93a3 #ea6fb4 #1a1015 #3a2833 #160d12 #4a3341 #f08cc4` |
| Burgundy | `#faf4f5 #ffffff #2c1a1f #6f5860 #8c1d38 #ffffff #ebdde0 #fdfafb #dcc6cb #6e1329` | `#1a1114 #251a1e #f2e6e9 #ad949b #e3708c #1a1114 #3c2a30 #150e11 #4c373e #ee92a8` |
| Brick | `#faf4f1 #fffdfc #2e1c17 #715a53 #a53f2b #ffffff #ecdcd6 #fdfaf8 #dcc6bf #86311f` | `#1b1210 #261915 #f1e4df #b0958c #e27a5e #1b1210 #3d2a25 #160e0c #4e3730 #ee9a82` |
| Walnut | `#ece0c4 #f4ead3 #3a2a1c #7a6549 #9c4a2c #ffffff #d8c7a3 #f7efdc #c9b58c #7d3a20` | `#1e160f #2a1f16 #e8dcc0 #a89474 #d18a5a #1e160f #3f3225 #17110c #4d3e2d #e0a070` |
| Earth | `#f8f4ee #fffdf9 #2d2419 #6f6152 #8a5a2b #ffffff #e6dccf #fdfaf5 #d5c8b6 #6e4620` | `#1a1512 #241d18 #ede4d8 #ab9c8a #d3a262 #1a1512 #3a3028 #15100d #4a3e33 #e2b87d` |
| Gray and gold | `#f2f3f4 #ffffff #1e2125 #5f666e #b3781e #ffffff #dde0e3 #fafbfb #c8cdd3 #8f5e14` | `#141618 #1d2023 #e6e8ea #9aa1a8 #e0a83c #141618 #2d3135 #101214 #3d4247 #f0bd5e` |
| Firefly | `#f1f5ee #fbfdf8 #16261b #52685a #4f7f21 #ffffff #d5e1d3 #f7faf4 #bdd0bf #3d6418` | `#070f0a #0d1a12 #d9ecd2 #7fa088 #d6f253 #0a1a10 #1c3324 #050b07 #23402c #e8ff7a` |
| Forest | `#f3f7f3 #fffefc #172519 #566b5a #2c6e42 #ffffff #dbe6dc #fbfdfb #c6d8c9 #215532` | `#0f1712 #16221a #e4eee5 #92ab97 #6cc488 #0f1712 #26362b #0c130e #33473a #8ad8a1` |
| Turquoise | `#f4f8f5 #fffefb #14302e #56706c #0f8a82 #ffffff #dbe8e3 #fbfdfb #c4d9d3 #0b6d67` | `#0e1b1c #142628 #e3f0ec #8fb2ac #45d0c2 #0a1a1a #23393a #0b1617 #2f4a4b #6ee0d4` |
| High contrast | `#ffffff #ffffff #000000 #333333 #0000c8 #ffffff #000000 #ffffff #000000 #000080` | `#000000 #000000 #ffffff #dddddd #ffd400 #000000 #ffffff #000000 #ffffff #ffe866` |

### How it was built

Everything the list below planned, and these facts from doing it:

- **`repos/server/tools/palettes.py` is the table.** Thirteen rows of
  twenty-two values; everything else the two stylesheets need (the soft
  rule, the code and note tints, the placeholder, the focus ring, the
  scrollbar, the panel's glow) is derived there, the same way for every
  theme, and written into both templates between `BEGIN/END palettes`
  markers. `write` regenerates, `check` fails on drift, and
  `build_local.py` runs the check on every build. A new theme is a row.
  Navy has no block: it is the templates' own `:root` and dark block,
  and `data-palette` is absent for it, so the default page is the page
  before this item but for the dark hover fix and the new variables.
- **Fourteen literals became variables** in `index.html` (the panel's
  gradient top, border, row line, name colour, scrollbar and glow; the
  button and link hover; the focus line; the disabled button; the Solve
  button's shadow as an rgb triple; the language face's colour), and the
  two toggle icons take `currentColor` from `--sky` instead of a fixed
  `#8ec7f5`. The Solver page's mode buttons lost two literals the same
  way. The `<select>` arrow's grey stroke was left alone: it reads on
  every ground.
- **`banner.css` changed by two variables with fallbacks**, `--banner-sub`
  and `--banner-link`, and its header comment says why. Propagated to
  both templates (`check_banner` passes) and to the landing copy
  (`stamp_assets.py` re-stamped it, `build.py --check` clean).
- **The picker is the language menu's construction**: a native `<select>`
  stretched invisibly over a face, here a dot split between `--navy` and
  `--sky`, so it follows the theme with no script. Option labels are
  `t()` calls, so `i18n.py tag` collected them and `check` demanded
  the twelve translations; Firefly is luciérnaga, luciole, Glühwürmchen,
  vaga-lume, lampiro, 萤火虫, ホタル, 반딧불이, kunang-kunang, जुगनू,
  জোনাকি, світлячок. `syncPaletteMenu()` runs from `refreshDynamic()`
  in the app and from the language handler in the Solver, and
  `build_local.py`'s Solver anchor (the language handler it extends
  with the boot bar) had to learn the new line -- the build said so.
- **Measured live on the Flask server before deploying**, both pages: 13
  options, the choice stored and applied, `--navy` and `--bg` following
  it, the toggle switching dark within the theme, the icon colour
  following `--sky`, the Solver arriving in the app's theme and mode.
  The ribbon stays one row: 59px at 1280 wide, the swatch and toggle
  40px each; at 375 the swatch and toggle are 34px, the row 50px, App ·
  Docs on the left, Clear · EN and the pair on the right, nothing
  clipped. Spanish names read back from the live menu. The offline
  build measured the same on a static server, both pages.
- **The scorpion**: `logo.png` replaced in five places -- the server's
  static copy, `repos/local`, the `--assets` source folder, and the
  landing's and learn's copies -- all one file, 40,586 bytes. The icons
  keep their navy ground: a home-screen icon wants one.
- **Deployed**: install and the ZIP at cache **v135** (ZIP 31,794,040
  bytes, hash-verified; build `2026-09-05 03:56 UTC`), the landing page
  (four files) and learn (`assets/logo.png` and `assets/banner.css`
  only -- no `build.py --web` ran, on purpose: the docs tree had three
  chapter sources with someone else's uncommitted edits, and a rebuild
  would have shipped them; the two assets were copied straight into
  `build/web/assets/` instead). **`symbulator.pythonanywhere.com` needs
  its pull and reload** -- the template and the dictionaries changed, so
  this is a real pull, no `pip`.
- **Not done, deliberately**: X has not been merged (`git fetch v9 &&
  git merge v9/main` in its three repos, keeping `branding.py`, then a
  rebuild -- the root `CLAUDE.md` describes it), and the mockup sheet
  stays in `Notes/`, not in a repo.

### What the build touched (the plan, kept for the record)

- `templates/index.html` and `templates/eqsheet.html`: the token blocks
  become one `:root` (Navy light), one `html[data-theme="dark"]` (Navy
  dark), and then a `html[data-palette="…"]` and
  `html[data-palette="…"][data-theme="dark"]` pair per theme. Fifteen
  colours are literal hex in the template today and become variables
  first: the panel gradient top `#102338`, border `#081525`, row line
  `#173352`, result name `#6fb8f0`, scrollbar thumb `#25517a`, the
  button hover `#1f4a86`, link hover `#1f4a86`, focus outline `#2f6fc0`,
  disabled button `#9fb0c8`, the Solve button's shadow `rgba(32,56,100)`,
  the select arrow's stroke in its data URI (two copies), the
  `a.toplinks:hover` `#b8ddff`, and the toggle's `fill="#8ec7f5"` in the
  markup, which should be `var(--sky)`.
- **A bug to fix on the way**: `button:hover` is `#1f4a86` in dark mode
  too, the light theme's dark blue on a `#5b96e0` button. Dark Navy gets
  `#4a86d0`.
- The head script: read `symbulator-palette`, set `data-palette`.
- The ribbon: the swatch and its select, after the language menu and
  before the toggle; `applyLang` must reach the option labels the way
  #240 taught it to reach the entry picker's.
- Thirteen dictionaries: thirteen names and the picker's label.
- `build_local.py` regenerates both offline pages; **cache bump**; the
  three-command chain and both offline deploys; the server pull is
  Roberto's. No solver release.
- `banner.css`: the two-line variable change above, then the propagation
  and both checks (`build_local.py`'s `check_banner()` and the docs
  `build.py --check`). The landing page and learn are unaffected in
  appearance — Navy's literals are the fallbacks.
- `tools/check_hidden_guards.py` and the heading audit of #248 both run
  again: a new control in the ribbon at 375px is exactly what #245–#248
  measured.

## #255 - every built-in entry that can be plotted carries its plot - **done 3 Sep 2026, live on all five sites**

> **Numbered #251 when it was written, and renumbered on 4 Sep 2026.** A
> documentation session running the same evening claimed #251-#254 for the
> version 9 wording pass, the `::: web` / `::: pdf` tags and the legibility
> pass -- its #253 is the tutorial's account of #250 here. The two trees
> share one running sequence, so the collision made #251 two different
> things. Their block is committed, deployed and named by a revert tag, and
> is four items to this one, so this is the side that moved. **Two pushed
> commits still say #251 in their subject lines** (`fd64b36` in `server`,
> `6f4ce8f` in `local`); the number in the notes is the one to believe.
> Working in two trees at once is how this happens: claim the number in
> both `NEXT.md` and `NEXT_DOCS.md` before starting, not when writing up.

Roberto, after #250: *"update all the built-in .cir input files for the
tutorial and other built-in examples, so that the entries carry the
values for the fields in the plot tool."* Then *"After that, commit,
upload, update."* and *"Do not wait for me. I'm going to bed."* -- so
this ran through to the deploys unattended; PyAn is his.

### What was there

Five entries carried a full plot already (Bo2's 6.5 and 6.6 in Lesson
6d, the low-pass in Lesson 11, two in the Showcase). **Two of them said
`plottool: time`**, which is the API's name for the tool and not the
menu's (`plot_time`), and a `<select>` handed a value it has no option
for selects *nothing*: both entries loaded with the Plot type blank,
`selectedIndex -1`, and Run would have posted an empty tool. Measured in
the browser before anything was changed. Both books now say `plot_time`,
and `applyCircuit()` maps `time` to `plot_time` on the way in, so a file
written by hand or downloaded from the old build still loads.

### How the 62 new plots were chosen

Not by hand. A script solved every entry with the real engine and sized
its plot from the answer, then ran the proposal through the same ui
function the Plot card calls and kept it only if it drew something:

| analysis | tool | key | range |
|---|---|---|---|
| tr | `plot_time` | the entry's `variables:` name if it is an answer; else the capacitor voltage, else the inductor current, else the output node | 0 to five times the slowest time constant, or three periods of the slowest oscillation, or twice the latest step -- rounded up to 1/2/5 x 10^k |
| fd, ac | `bode` | as above | a decade below the lowest corner to a decade above the highest, on decade marks, at least three decades; the AC entry's own omega counts as a corner |
| fd, no numeric source | `bode_tf` | H(s) itself, simplified | 1 Hz to 100 kHz |
| dc, one free symbol that is a source's whole value | `sweep` | the output node | 0 to 10 V |

**62 proposals survived, 261 entries were left alone**, each for a
reason the script printed: 46 Thévenin and 15 other tool entries; 107 DC
circuits with nothing to sweep; 37 with several free symbols (the
symbolic derivations); every AC power and three-phase problem of lessons
7-10, whose impedances are written in jΩ and so cannot be swept in
frequency (the engine says so: *still depends on j*); the transient
figures that are symbolic in V, r and c; the impulse response
(`DiracDelta` does not sample); and three current-source sweeps I
dropped by hand, having no natural range for the current. The
two-stage amplifier in the monograph has a symbolic source and a
four-capacitor H(s) too long to type into the Bode-of-H(s) field, so it
has none.

The one editorial addition: NR11's Example 13.7 is *about* a transfer
function, so it carries `plottool: bode_tf` with `1000/(s + 1000)`, the
H(s) the engine derives -- the reader sees the plot the chapter is
about without a source value.

### The check

`repos/server/tools/check_example_plots.py` runs every entry's plot the
way the card would -- Define lines expanded, Expert Mode extras passed --
and fails on a tool the menu lacks, an engine refusal, non-finite
samples, a flat trace, or an inverted range. **67 plots in 330 entries,
0 failures.** Proved red by sabotage three ways on Lesson 11 (a wrong
key, `time`, an inverted range), each naming the entry and the reason.
Not in the build: it solves 67 circuits and takes a minute or two. Run
it after touching a book or the plot tools.

### Verified on the artefact

NR11's entry opened from `?lesson=12&entry=6` in the local server, the
Plot card filled, Run pressed: *Plotted!* and an SVG in the card. Bo2's
6.5 opened with `plot_time` selected where the morning's build had
nothing selected. Both legacy spellings (`plottool: time`, and the older
`tool: time`) applied through `applyCircuit()` select `plot_time`.

Build `2026-09-03 12:22 UTC`, cache **v134**, ZIP **31,802,999 bytes**.
Deployed and hash-verified: `install.symbulator.com` (14 files uploaded,
48 identical) and `symbulator.com/9/local.zip`. **The server followed on
4 Sep 2026**, Roberto's pull and reload; no `pip`, no solver release.

Verified on the live host rather than by the stamp: `/api/examples` for
Lesson 11 serves four entries, all four with a plot, and Lesson 6d
sixteen -- Bo2's 6.5 among them, now reading `plot_time` where it read
`time`. Then the plot itself, driven on
`symbulator.pythonanywhere.com/?lesson=11&entry=1`: Run returns
*Plotted!* and the card holds a 640x260 SVG titled *v_2 - magnitude*,
its axis starting at 10 Hz and its trace carrying **300 points** -- the
entry's own `plotpoints`. The pane was hidden, so every pixel
measurement read 0; the point count is the measurement that survives
that, and the viewport was printed to prove the zero rather than
believed. The monograph's exemplar circuits gained plot keys
but their drawings did not change, so Appendix B is not stale.

---

## #250 - the Plot card's inputs travel with the entry - **done 3 Sep 2026 at cache v133; live on all five sites**

Roberto: *"I want to add the inputs in the fields for the Plot tools to
the entry that is saved in input files. So, if there are values for a
Bode plot inputs at the time the entry is saved, save those and restore
them when the entry is loaded."*

The keys already existed - `plottool`, `plotkey`, `plotx`, `plotmin`,
`plotmax`, `plotpoints`, written by `inputsSnapshot()`, read by
`applyCircuit()`, known to `parse_book` and `format_book`, listed in the
format reference. And they worked, for the case they were tested on. Two
things lost the values anyway, and both were found by trying the round
trip rather than by reading the code that claimed to do it.

### What was losing them

**The gate.** `inputsSnapshot()` saved the Plot card only when the
*variable* field was non-empty. A Bode plot's frequencies typed before
its variable, or a sweep's range typed first, were dropped from the entry
and came back blank. The card now counts as in use when any of its four
text fields holds something, or when the point count has been changed
from the 300 a fresh page shows - so a fresh page still claims no plot,
which the "have the inputs changed?" comparison depends on.

**Two field lists that were supposed to be one.** The browser's entries
go to a file through `/api/export` on the server or `export_book` in the
offline bridge, and each kept its own hand-written list of the fields to
carry across. `app.py` even had a comment saying this was the trap
CLAUDE.md warns about. It was. Measured before the fix, by posting one
entry with every field set:

| lost by | fields |
|---|---|
| the server's export | `defines`, `evaluate_conditions`, `polar`, `show_equations` |
| the offline bridge's export | `plotx`, `defines`, `polar`, `show_equations` |

So the sweep's x-axis variable - the one plot field no other plot type
has - was silently dropped from every file the offline builds wrote, and
an AC entry saved with polar phasors came back rectangular from any
downloaded file. Nothing showed inside a session: the entries live in
the browser and are restored from there, so the values were lost only
between **Download** and opening the file again - the one place a
reader expects them to be safe.

### The fix

One function, `circuitbook.clean_circuits()`, behind both exports, and
its field lists **derived from the parser's own tables** rather than
written a third time: `SCALAR_FIELDS`, `BOOL_FIELDS` and `LIST_FIELDS`
come out of `_KEYS`, `_BOOL_FIELDS` and `_MULTI`, so whatever
`parse_book` can read, an export can write. The server passes its
request caps; the offline build passes none, as before. `app.py` and
`bridge.py` each shrank by thirty lines.

### The guard

`repos/server/tools/check_export_fields.py`, run by every
`build_local.py`, hard. Three directions:

1. a circuit with every field set is written, parsed, cleaned and
   written again - every field must come back with its value, and the
   second file must equal the first byte for byte;
2. every key `inputsSnapshot()` returns must be one the format knows,
   read straight out of the template;
3. both exports must still call the shared function.

Proved red by sabotage four ways before being trusted: `plotx` deleted
from the parser (caught by 2), a `bogus:` key added to the snapshot
(2), the bridge's call replaced by `[]` (3), and the writer told to skip
`plotmin` (1, naming the field). Green again on restore:

    check_export_fields: ok -- 31 fields round-trip, 28 snapshot keys all known, both exports share clean_circuits

### Verified on the artefact

Driven in the local server's page, not read off the code: a Bode plot
with `10` and `1e5` typed and the variable blank, saved to a new entry,
exported (`plottool: bode / plotmin: 10 / plotmax: 1e5 / plotpoints:
300` in the file text), the card wiped with *Clear all*, the entry
re-applied - all four back, card open. A fresh page's snapshot has no
`plottool`. Both exports were then posted the same full entry and both
wrote all 21 lines, `defines:` and `plotx: rx` and `polar: yes` among
them; the bridge was tested against the server's `circuitbook.py`, since
the copy in `repos/local` is generated and was stale until the build
copied it.

### The format reference, in thirteen languages

The paragraph in the Input File card described the plot keys as
*`plottool` (time/bode) / plotkey / plotmin / plotmax / plotpoints* - no
`plotx`, and two plot types short. It is one translation unit, so the
fix was a translation round, done the same day at Roberto's ask: the
English now reads *`plottool` (sweep/bode/bode_tf/plot_time) / plotkey /
plotx (the variable on the x-axis) / plotmin / plotmax / plotpoints*,
`i18n.py tag` minted the new key (`everything-after-the-element.afbf`,
retiring `.4f05`), and the twelve dictionaries got the same two edits
each - the parenthetical borrowed from each language's own label for the
x-axis field, so the reference and the field agree. Japanese and Chinese
keep their full-width parentheses, as their `plottool` already did.
`i18n.py check` is clean, no orphans.

Build `2026-09-03 11:54 UTC`, cache **v133**, ZIP **31,802,120 bytes**.
Both repositories pushed, then **deployed on Roberto's go the same
day**: `install.symbulator.com` (17 files uploaded, 45 already identical,
`index.html`, `sw.js`, `bridge.py`, `circuitbook.py` and the dictionaries
hash-verified live) and `symbulator.com/9/local.zip` (31,802,120 bytes,
hash-verified). **The server followed on 4 Sep 2026** -- Roberto's pull
and reload on both PythonAnywhere accounts -- so this is live on all five
sites; no `pip`, no solver release. Verified by fetching, not by the
stamp: the live page's reference paragraph reads *plottool
(sweep/bode/bode_tf/plot_time) / plotkey / plotx (the variable on the
x-axis) / plotmin / plotmax / plotpoints*, and the new translation key
`everything-after-the-element.afbf` is in the served markup with the old
`.4f05` gone.

`verify_bridge.py` was not run: it solves all 330 entries through both
front ends and times out at five minutes, and it exercises the solve
path, which this item did not touch.

---

## #249 - a `display` rule had been overriding `hidden` - **done 3 Sep 2026; live on all five sites since the 4 Sep pull**

Roberto, on his phone: the monograph's second entry still showed the
**Show image** tick with nothing under it. #242 was meant to hide that
tick on the 31 entries with no picture, and my audit had reported that
it did.

The audit was wrong, and wrong in the way that is hardest to see.

### Why the DOM lies about this

An author `display` beats the browser's own `[hidden] { display: none }`
whatever the specificity - the two rules are in different cascade
origins, and the author origin always wins. `label.checkline` sets
`display: flex`, so #242's `line.hidden = true` set the attribute, the
property read back `true`, and the tick went on rendering at 34x229.

Any check that asks the DOM `is this hidden?` therefore agrees with the
code and disagrees with the screen. Only `getBoundingClientRect()` or
`getComputedStyle()` tells the truth.

The template already said all of this, in a comment on `.solution-pick`
ending *"Anything here that sets display has to say this too."* #242 was
the third time. So this closes with a check rather than a fourth
comment.

### The check

`repos/server/tools/check_hidden_guards.py`: every element the page ever
hides - `hidden` in the markup, or `.hidden =` in the script - must have
a `[hidden]` rule for every `display` rule that targets it.

The one design decision that makes it usable is keying on the
**rightmost compound** of a selector. `.setnote .hint:last-child` targets
`.hint`, not `.setnote`; without that it blames the parent for the
child's rule and reports a guard that is already there. That was its only
false positive, and it went away.

Proved by sabotage, per the standing rule: deleting
`label.checkline[hidden]` turns it red and names the right element,
restoring it turns it green.

It found a **second instance, older and never reported**:

    #vtab,#rtab { display: block }          eqsheet.html
    <table id="rtab" hidden>

so a blank Numerical Solver has been drawing an empty
`EQUATION / VARIABLES` header at 33x261 for as long as that page has
existed. Nobody had mentioned it; it looks like a heading, not a fault.

Wired into `build_local.py` beside `check_example_images()`, and **hard**
where that one is soft - it needs nothing outside the repository, so
there is no absent-tree case.

### Verified on the artefact

On the live offline build, not in the DOM:

| | |
|---|---|
| monograph entry 2 (no picture) | `display: none`, 0px, not rendered |
| lesson 1 entry 2 (has one) | tick shown and checked, image loaded 229x136 from 887x501 |
| eqsheet on a blank sheet | header 0px, not rendered |

One aside worth keeping: the first attempt to verify measured the **old
build**. `install.symbulator.com` had installed the v132 worker but v123
was still controlling, so the page under measurement was 3 hours stale
and reported `hasHiddenAttr: false`. That is the same thing Roberto's
phone was doing, and it is why the diagnostic below matters more than
the fix.

Cache **v132**; install and the ZIP deployed and verified.

### Also: `install` needs three commands, not one

`deploy_symbulator.py install` reads `Application/v9/install_site`, which is
unpacked from `repos/local/local.zip` by `stage_install_site.py`. Running
the deploy straight after `build_local.py` uploads **the previous
build** and verifies it as a hash match, honestly and uselessly - stale
against stale. The order is:

    py build_local.py
    py build_zip.py --assets ../../local
    py stage_install_site.py

then `install` and `zip`. It cost two clean-looking no-op deploys here
before the local and live byte counts were compared.

---

## #246, #247, #248 — nothing in the interface wraps on a phone any more — **done 3 Sep 2026; live on all five sites since the 4 Sep pull**

#245 fitted the Input File buttons for English. These three finish the
job: the remaining three languages, the summary under the buttons, and
then every other heading in the app.

### #246 — the last three languages fit the button row

German, Japanese and Ukrainian still wrapped. Both Upload and Download
now carry the same two-span pair *Create new* got:

    de  Hochladen / Herunterladen  ->  Hoch / Runter
    ja  アップロード / ダウンロード  ->  アップ / ダウン
    uk  Вивантажити / Завантажити  ->  Вивант. / Завант.

Ukrainian could not take the Up/Down shorthand Roberto suggested: its
two words differ by one prefix, so directional wording would have made
them the same word. The standard clipping is used instead.

The other ten repeat their own word in both spans, and their measured
widths after the change are **identical** to before — which is the
evidence that nothing moved for them. de 285→186, ja 290→194,
uk 325→233, in a 293px row.

A tier at 360px (tighter gap and padding) was added because a 320px
phone leaves the card 238px, where even English was 4px over. At 320px
eleven of thirteen now fit; French and Bengali still wrap, and that is
left as a known limit — 320px is a 2016 screen and wrapping there is
graceful.

### #247 — the `.cir` format link

From a German screenshot. Measured first: that one summary wrapped in
**eight of thirteen** languages, English among the five it fits, which
is why nobody had seen it. The other two summaries in that card fit
everywhere and were left alone.

`.lbl-full` / `.lbl-short` stopped being the button row's private
property here and became general, switching at the same 480px as the
ribbon, the property mark and the subtitle.

### #248 — the rest of the interface

An audit of **30 headings × 13 languages**, plus the Numerical Solver's
own page, every `details` forced open and every `inactive` card
un-dimmed. Nine languages were already clean; six instances turned up
across three headings, plus one Roberto rewrote:

    Run Symbulator 9 locally -> Run locally     (his wording; pt, id)
    Circuit syntax reference -> Circuit syntax  (eo, fr)
    Plotting Tools           -> Plotting        (uk)
    What you can do with it  -> What it does    (id)

*Run locally* is a real rewording in every language, not a phone
spelling — the card's heading and the two places the page names it in
prose, so it goes on being called one thing. Each language's
host-notice sentence had the old name swapped for the new inside its
existing wording rather than being re-translated. Note that card is
inside a `server-only` block, so it does not exist in the offline
builds at all: 4 mentions in the template, 0 in the generated page.

Re-audited after: **all thirteen languages clean, every heading, both
pages.**

### Three ways to measure a wrap, two of them wrong

Worth keeping, because the first two were convincing:

| measure | what it does |
|---|---|
| `height / line-height` | counts padding as a line — claimed *List of Equations* wraps in English; that box is one 19.2px line plus 19.2px of padding |
| counting line boxes | breaks when a line mixes font sizes — *Input File (optional)* has two distinct rect tops because the hint is smaller |
| **`nowrap` + overflow** | the actual question: force one line, ask whether it overflows its own box |

The first two would each have had six already-fine headings "fixed".
Measure the thing, not a model of it.

Cache **v131**; install and the ZIP deployed and verified.

---

## #245 — the Input File buttons fit a phone — **done 3 Sep 2026; live on all five sites since the 4 Sep pull**

*Upload*, *Download* and *Create new* each carried `min-width: 8.6rem`
so the trio would read as a set. Three of those plus two gaps is
**438px**, and the card is **294px** wide at 375px — so the row wrapped,
in every language.

Two changes, and the order matters. **The equal-width rule goes first**:
reading as a set is a desktop luxury, not something worth a wrapped row.
Below 480px each button hugs its own label instead, with a tighter gap
and padding. **The short spelling is second**, and only for *Create
new*, which becomes *New* — the same two-span idea `banner.css` uses in
the ribbon, kept local because that rule is scoped to `.subbar`. Upload
and Download are short enough in English to stand as they are.

480px because that is where everything else on this page abbreviates:
the ribbon, the property mark and the subtitle all switch there.

Each language keeps whatever it already said for the full spelling, so
this cost no re-translation — only the twelve short forms are new.

### Measured, and three that still wrap

At 375px in all thirteen languages. English fits at **228px of buttons
in a 294px row**, where before the change every language needed 438px.
**Ten of thirteen fit.**

**German (285px), Japanese (290) and Ukrainian (325)** are still over
the row once the gaps count. Their *Upload* and *Download* are simply
long words — *Herunterladen*, アップロード, *Завантажити*. Fixing them
means a second short spelling on those two buttons: two more keys and
twenty-four more translations. Roberto asked for English (*"at least for
the English version"*), so that is what this does. The other three are a
strict improvement on wrapping at every width, and the rest is one
decision away.

Cache **v128**; install and the ZIP deployed and verified.

---

> **X is deliberately a version behind, from 3 Sep 2026.** Roberto:
> *"Will hold on X for now."* The merges are done and pushed — X's
> repositories carry #241–#244 — but `symbulatorx.pythonanywhere.com`
> was left on the earlier build rather than reloaded. So X's *source* is
> current and X's *site* is not, which is the one combination that looks
> like an oversight from either end. Reload it whenever he says.

## #244 — the checkbox just says *Show image* — **done and live on version 9, 3 Sep 2026**

The *"(if available)"* was a caveat about entries that have no picture,
and since #242 the control does not appear for those at all — so it was
describing a case that can no longer be on screen. One item creating the
next: the qualifier was honest right up until the moment the behaviour
made it unnecessary.

Twelve translations updated to match — the #225 strings with the
parenthetical dropped, same wording and register otherwise, so this cost
no new translation work beyond the trimming. `i18n check` clean.

Cache **v127**; install and the ZIP deployed and verified. X merged.

---

## #241, #242, #243 — the entry picture framed, its checkbox conditional, and Export Output demoted — **done and live on version 9, 3 Sep 2026**

### #241 — centred, in a white mat

It matters more since #239: a capped picture no longer fills the card,
so a small scan sat hard left against the card's own background with
nothing separating the two — and in dark mode a white-backed scan
against a dark card had no edge at all. `margin-inline: auto` and 7px of
padding over the white background it already had, which turns that
background into a mat instead of something hidden behind the picture.

**The arithmetic is the part worth reading.** `box-sizing` is
`border-box` throughout this page, so `max-width` would have included
the mat and every capped picture would have rendered ~16px narrower than
the width #239 computed for its lettering. `showEntryImage` therefore
adds the frame to the cap — and *reads* it off the element rather than
repeating the number, so the stylesheet stays the single source.
`--entry-frame` is declared once in the rule; `frameAllowance()`
measures padding plus borders from the computed style.

Measured: with a `[278px]` cap the element is 294px and the picture
inside it is exactly 278px, gaps equal at 124px. An uncapped picture is
unchanged — 541px in a 541px box, no overflow of box or card, no
horizontal scroll.

### #242 — the checkbox appears only when there is a picture

Roberto's idea. *Show image (if available)* is shown for an entry that
names one and hidden for one that does not; most entries in a reader's
own file will not have a picture, and a control that governs nothing on
screen is furniture. **The preference is untouched by the hiding** —
global, in `localStorage`, and it survives every entry that hides the
control.

**It keys off whether the entry *names* a usable image, not whether the
image loads, and it has to.** When the box is unticked nothing is
fetched, so "does it load" is a question this code cannot answer without
making the request the reader declined. Naming is also the stable
answer: it cannot flicker on a slow network the way a load test would.

That reordered `showEntryImage` — the src is parsed and validated
*before* the unticked early return, because the control's visibility has
to be decided even when no picture will be drawn. The markup starts
hidden: nothing is loaded at boot, so there is nothing to govern yet.

Verified through the awkward path: untick on an entry with a picture,
move to one without (control vanishes, preference still "no"), come back
(still unticked), re-tick (picture returns, stored "yes").

### #243 — Export Output is a subheading

Its summary drops `results-h section-toggle` and takes the plain
`summary` styling, which is what *Input File* uses. The app already had
two tiers of card heading — the big ones for Results, Solve, Plotting
Tools, and the quiet one for Input File — and this moves Export Output
into the quiet tier beside the other utility card. Measured after:
16.8px and weight 600 on both. Their colours differ only because
`dlCard` still carries `inactive` before a solve.

Cache **v126**; install and the ZIP deployed and verified. No solver
release. X has all three merged and keeps its own `branding.py`.

---

## #240 — the entry picker follows the language — **done and everywhere, 3 Sep 2026**

Switching language with a book open left the picker's label and
placeholder in the previous one — *"Entradas en …"* alone on an
otherwise English page. Spotted in passing while verifying #239 on the
live install build, and numbered on Roberto's say-so.

**Why `applyLang` could not reach them.** Those two strings are written
by the app, not carried on a `data-i18n` element: `populatePicker` built
that markup at the moment the file was opened, so it froze whatever
language was current then. `applyLang` repaints tagged markup and has no
idea the picker exists.

`refreshDynamic()` is the right home — its own comment says
*"everything on screen that the app itself wrote, redrawn in the new
language"* — and the picker had simply been left out of the list.
`pickerStrings()` factors the label and placeholder out of `showFile` so
both callers build them identically; `syncPicker()` rebuilds them on a
language change.

**Two details.** The selection is captured and restored around it,
because `populatePicker` rebuilds every `<option>` and would otherwise
drop the reader back to the placeholder. And `lastPickerValue` is
deliberately *not* touched: nothing has actually been picked, so the
change handler's idea of what is current must not move.

The file's own title stays English inside the label, as it should — the
built-in books' titles and `note:` lines are English in every language
by Roberto's ruling of 31 Aug 2026.

Verified in the running app across es, ja, uk and back to en: both
strings follow, the selected entry survives every switch, and picking a
*different* entry still works afterwards with the circuit intact.

Cache **v124**; install and the ZIP deployed. No solver release.

---

## #232, #235–#239 — the fine-tuning batch — **done and everywhere, 3 Sep 2026**

One listen-first round on 3 Sep 2026, nine items, six of them app-side.
The docs-side three (#231, #233, #234) are in `NEXT_DOCS.md`.

### #232 — the ribbon says Documentation / Docs

`templates/index.html` and `templates/eqsheet.html`. The landing page had
said *Documentation* all along; the app said *Tutorial*, and was the only
thing out of step. **`banner.css` had already specified this** in its
29 Aug comment — *"The app says App / Docs / Clear inputs there"* — so
this was finishing a decision, not making one.

Two new keys, twelve languages each, and then the check that is not
optional: all thirteen languages measured at 375/481/520/768/1100px for
clipping or wrap. **All clean, so no wording had to be shortened.** The
first measurement pass was wrong and said even English clipped — it set
`document.documentElement.style.width` instead of emulating a viewport,
so the media query never fired and the *full* labels were being squeezed
into 375px. Emulate the viewport; a CSS width is not a screen.

### #235 — `image: <url> [200px]`

A cap on how wide an entry's picture is drawn. One spelling only,
case-insensitive on the `px`, whitespace required before the bracket so
a URL containing brackets cannot be misread. A cap that does not parse
leaves the picture at **full width and warns at parse time**: #219's
rule is that an image *problem* produces silence, but a malformed
instruction is a typo, and a silent typo is the thing this project keeps
paying for.

**It forced a fix to a guard.** `check_example_images.py` anchored its
pattern straight after the URL, so a line carrying a cap would have
stopped matching *entirely* and that picture would have dropped out of
the check unnoticed — the same shape as #230. It now reads the cap,
ignores it, and **reports any `image:` line it cannot parse** instead of
skipping it. Proved by sabotage: valid cap passes, broken cap and
missing file both exit 1, restored file clean.

No parser change was needed for the value itself: `circuitbook.py` keeps
`image` as one opaque string and writes it back verbatim, so the cap
round-trips through a download for free.

### #236 — the entry note is not shy any more

It was `.84rem` in `--muted` — two separate ways of saying "this matters
less" on the one thing carrying the instructions. Body size, body ink,
its own class. The same `.booknote` also carries the transient chatter
("reading file…", "Could not upload that file."), which stays small;
the box and left rule are kept on both, because that is what marks the
text as the entry's rather than the page's.

### #237 — `note:` is repeatable

One paragraph per line, rendered as separate `<p>` elements. It was
scalar, so a second `note:` **silently replaced the first** — a whole
paragraph lost without a word. `textContent` throughout, never
`innerHTML`: a `.cir` can arrive from a stranger.

**It needed the same fix in two places.** `note` sat in hand-written
scalar field lists in *both* `app.py` and `bridge.py`, where `str()`
would have written the literal `"['a', 'b']"` into a downloaded file.
That is the by-hand-field trap `CLAUDE.md` names, and it bites once per
front end.

### #238 — a repeated scalar key warns

`omega`, `image`, `rounding` and the rest kept the last value silently.
Only the `_MULTI` keys may repeat.

### #239 — 186 image caps, computed rather than judged

    cap = natural_width x 16px / text_px

The width that puts the lettering *inside the scan* at the app's body
text size. **That is the documentation's own rule since #153** — the app
was the one surface that never had it, so a two-element divider and a
dense op-amp network were both stretched to the full 620px card.
Roberto's brief was *"examine the image, find the size of text and
symbols, and extrapolate"*, which is the same rule arrived at
independently; the measurements were already sitting in the docs tree's
`figure_sizes.json`.

**Measuring first killed the obvious theory.** The assumption was that
small pictures were being blown up. They were not: only **6 of 299** are
narrower than the card, and **200 were already being shrunk**. The
complaint was never about scaling — it was that every picture got the
full card regardless of how much was in it. `hk5s-figure-1-26-1.jpg` is
887px wide with **51px lettering**, so at 620px its letters landed at
36px against 16px body text; capped at 278px they land at 16px.

186 of 299 gain a cap; the other 111 are already right and get nothing,
so those lines stay clean. Reviewed as a **59-page PDF contact sheet**
before a single file was touched — each picture as the app draws it
today beside the proposal, pictures embedded from the docs tree so it
reads on a machine with no network. `tools/image_caps.py` computes and
writes; `tools/image_caps_pdf.py` builds the sheet. Both re-runnable.

`BODY_PX = 16` in `image_caps.py` is the one tunable: move it and all
186 caps move together.

### Shipped

Cache **v123**; `install.symbulator.com` and the ZIP deployed and
verified. Live check on the install build found the old page first —
the service worker had not yet handed over — which is the trap
`CLAUDE.md` names; after the reload the cache read `symbulator-v123` and
everything was right: note at 16px in `booknote entry`, HK5's picture at
exactly 278px, ribbon *Documentation / Docs*.

**No solver release**, so no `pip` upgrade anywhere. The server wants a
`git pull` and a **Reload**. X has the batch merged and keeps its own
`branding.py`.

---

## #229 — The beta mark at 80% of the numeral's height — **done and everywhere, 3 Sep 2026**

Roberto, 3 Sep 2026, and **everywhere it appears**: the app's wordmark
and the landing page's, which are the two consumers that draw a beta.
`learn.symbulator.com` never did.

Georgia's beta has a long descender *and* an ascender taller than the
digits, so at the numeral's own size it was the tallest thing in the
lockup — the wrong emphasis for a mark that is temporary by design.
`.brand-name .tm .beta { font-size: 0.8em; }` in `banner.css`, and the
beta gets its own span so it can be sized without taking the numeral
with it. Measured after: font ratio exactly 0.800, rendered ink 26.4px
against the numeral's 33.6.

**`BRAND_BETA` joins `branding.py`** rather than staying inside
`BRAND_TM`. It is a separate glyph with its own styling, and #137
removes it when 9 leaves beta — at which point it becomes `""` and the
markup disappears with it, with no template edit. A fork that is not in
beta leaves it empty, which is what version X does.

**This is a `banner.css` change, so it went to all four cPanel sites.**
Canonical edited, copied to the landing folder, `stamp_assets.py` run
(the stamp moved `15076a3e` → `00850b21`, without which a returning
visitor keeps the old stylesheet for a week), re-inlined into both app
templates, and both guards run. `check_banner` caught the drift the
instant the canonical changed and refused to build — which is exactly
what it is for, and the first time this session it has been seen doing
it.

Verified live afterwards rather than assumed: the three copies of
`banner.css` — canonical, `symbulator.com`, `learn.symbulator.com` —
are byte-identical at sha `00850b2108`, and the beta span is on the
landing page and the install build. Cache **v122**; install and the ZIP
deployed together.

**The server still wants a `git pull` and a Reload** to serve it. No
`pip` upgrade — no solver release.

### Version X, the same day

X took Roberto's variant C from a rendered mockup: the mark in gold
(`#d9a521`) and a subtitle that says outright what X is — *an
experimental fork of Symbulator 9 — testing the limits of symbolic
simulation*. `BRAND_TM_COLOR` is a third branding value, rendered as an
inline style on the mark alone and absent entirely when empty, so
version 9 keeps the sky blue `banner.css` gives every property. Inline,
and declared in `branding.py`, precisely so that a fork never has cause
to edit the shared stylesheet — which would be #228's problem again, one
file further down.

---

## #228 — The banner's forkable strings move to `branding.py` — **done 3 Sep 2026; needs a server pull when convenient**

Roberto asked how a separate banner for X was going to be *maintained*,
which was the right question: X1 had made X look different by editing
X's copy of `templates/index.html`, and that collides with version 9
every time version 9 touches the banner's neighbourhood in a 5,000-line
file. Resolved by hand, every time, with a silent failure mode — take
version 9's side by reflex and X quietly becomes a byte-identical clone
again, which is what got its PythonAnywhere account disabled.

**Two constants now carry the difference.** `repos/server/branding.py`:

    BRAND_TM  = "9β"   # X sets "X"
    BRAND_SUB = ""     # empty = use the translated subtitle in the
                       # template; a fork sets its own tagline

Version 9 changes that file about once a year — #137's beta removal is
the next time — so the trees now collide almost never, and when they do
the conflict is two lines and obviously about branding.

**The subtitle keeps both spellings in the markup and picks with Jinja**,
rather than becoming a variable outright. Version 9's subtitle is a
translated UI string with twelve translations; turning it into a
constant would have thrown them away. The i18n tagger still reads the
English literal out of the markup and keys it exactly as before —
`en.json` is unchanged and `i18n.py check` is clean.

**`build_local.py` resolves both at build time**, from the same file, because
the offline page has no Jinja. `sub()` insists each replacement matched,
so a template edit that moves the banner fails the build loudly instead
of shipping a raw `{{ brand_tm }}` to a reader.

### The guard that caught its own author

The offline build's sanity check banned `"{{ "` and nothing else. A Jinja
**comment** is neither an expression nor caught by that rule, and the
first draft of this item leaked one straight into the offline page as
visible text. The check now bans `{%` and `{#` as well — and immediately
failed the very next build, because the explanatory comment written to
document the leak quoted the syntax verbatim. Hence the wording in the
template, which describes the braces instead of spelling them.

This is the same family as the 30 Aug 2026 incident already in
`CLAUDE.md`: `{#` in an HTML comment stopped the template parsing and
returned 500 on every page while `/healthz` stayed green. Jinja syntax
does not look like syntax to a reader, and neither of the two checks
that existed could see it.

### Verified both ways round

Version 9 renders `9β` and the translated subtitle, on the server and in
both offline pages; the generated pages are byte-identical to v121's but
for the build stamp and one added HTML comment. A fork's values render
`X` and its own untranslated tagline on all four surfaces, with no trace
of the canonical subtitle anywhere in the page. `/`, `/eqsheet/` and
`/healthz` all 200 — a template edit is not verified until Flask has
rendered it.

**Nothing needs deploying urgently.** No cache bump (the offline pages
are unchanged in substance), no solver release, and the server's rendered
output is identical to what it already serves. The server repo has the
commit whenever the next `git pull` happens.

---

## #227 — Say who may frame the app — **done and live, 2 Sep 2026**

    Content-Security-Policy: frame-ancestors 'self' https://learn.symbulator.com

Server variant only (`repos/server/app.py`, one `after_request`). The
offline builds are static files on cPanel and send no headers; nothing
frames them.

**Why now.** #224's split view legitimately frames this host from
`learn.symbulator.com`, and until now nothing said so -- the app sent no
framing header at all, so *every* origin on the internet was allowed to
embed it. On 2 Sep 2026 PythonAnywhere disabled the separate
`symbulatorx` account for content that "might be related to phishing
activities" (X was then byte-identical to this site under a hostname one
letter away). Nothing about *this* site was in that notice, but a page
anybody may frame is what an automated scanner reads as a phishing
surface, and naming the one origin that may is the honest answer as well
as a real defence against clickjacking.

**`frame-ancestors` only.** A full CSP would have to account for the
inline styles and scripts the template is built from, the KaTeX and
MathJax CDNs and Google Fonts; getting one wrong breaks the page for
everyone. This directive touches nothing but framing.

**And no `X-Frame-Options` beside it** -- the obvious instinct, and
wrong. There is no safe value: it has no syntax for "me and one other
origin", `ALLOW-FROM` was removed from every current browser, and
`SAMEORIGIN` would forbid the split view, which is the one framing this
exists to permit. A browser too old for `frame-ancestors` cannot run
this front end anyway.

**Proved by making it fail on purpose**, not by reading the header back:
a page served from a second local origin framing the app is refused, and
the console names the directive --

    Framing 'http://127.0.0.1:5000/' violates the following Content
    Security Policy directive: "frame-ancestors 'self'
    https://learn.symbulator.com". The request has been blocked.

The header is on every route, the eqsheet Blueprint included. No cache
bump: `app.py` is not part of the offline build, so this was a server
`git pull` and **Reload** and nothing else, done by Roberto the same
evening.

**Verified live afterwards, including the thing that could have broken.**
The header is served on `/` and on `/eqsheet/`, with no `X-Frame-Options`
beside it — and `learn.symbulator.com/split/` still renders both panes
with an entry loaded on each and **no console errors**. A wrong origin in
that header would have blanked the right pane in production, so checking
the header alone would not have been checking the right thing.

---

## #225 — "Show image (if available)" — **done and everywhere, 2 Sep 2026**

Roberto, 2 Sep 2026: a checkbox in the Input File card governing #219's
entry picture. **Checked by default**, and **remembered across entries
and across sessions** — his ruling, asked and answered before any of it
was written: "checked by default in the app, but then it should remember
across entries and sessions. Not per entry."

So it is a standing preference in its own `localStorage` key,
`symbulator-show-image`, beside `symbulator-theme` and
`symbulator-lang`, and deliberately **not** part of the saved workspace
and **not** a `.cir` field. It says how this reader likes to work, not
what this circuit is; the input file format is unchanged.

**Unticked, the picture is not merely hidden — the `<img>` is given no
`src`, so nothing is requested.** That is the point of the feature for
anyone on a metered connection, and it is why it could not be a CSS
rule. Measured rather than assumed: with the box off, a fresh load of
`?lesson=1&entry=1` — an entry that has a picture — requests `logo.png`
and nothing else.

Two details worth keeping:

* **The src is remembered** (`entryImageSrc`), so ticking the box puts
  the picture back at once instead of at the next pick. The entry itself
  is not always to hand — a reader can be looking at inputs they have
  edited away from it — so the value is kept rather than looked up.
* **The control sits outside `entryImageBox`**, which is hidden whenever
  there is no picture. A checkbox that vanished along with the image
  could never be used to bring one back.

Translated into all twelve languages, `i18n check: ok`. Verified in the
offline build as well as the server one, and in four languages on the
page: `Mostrar imagen (si está disponible)`, `画像を表示（ある場合）`,
`Показувати зображення (якщо є)`, `Bild anzeigen (falls vorhanden)`.

**Shipped, all three surfaces:** cache **v121**;
`install.symbulator.com` and `symbulator.com/9/local.zip` deployed and
verified byte-identical to each other (`index.html`, `sw.js` and all
twelve dictionaries); and `symbulator.pythonanywhere.com` on Roberto's
pull-and-reload the same day — `/healthz` build `2026-09-02 12:57 UTC`
running *and* on disk, `needs_reload: false`, solver 0.5.26. The
checkbox was hit-tested on the live server rather than found in the
markup: default on with the picture loaded, and unticking it drops the
`src` and stores `no`. **No solver release** — 0.5.26 is untouched, so
the bundled wheel and the three pins that name it did not move, and no
`pip install --upgrade` was needed anywhere.

**X has this merged**, and **X's site came back on 3 Sep 2026**:
PythonAnywhere disabled the account on 2 Sep for content that "might be
related to phishing activities" -- X was then byte-identical to version 9
under a hostname one letter away -- and restored it on appeal. So #225
does reach X, once its own PythonAnywhere pull-and-reload happens. X now
differs from v9 by its orientation `CLAUDE.md` files, its `branding.py`
(#228, #229) and the pages generated from it.

---

**#212 is done and everywhere, 1 Sep 2026**, at solver **0.5.24** and cache **v115** — PyPI, `install.symbulator.com`, the ZIP and `symbulator.pythonanywhere.com` (Roberto's pass the same night; `/healthz` clean, a DC divider, an AC complex solve and a live schematic all verified by fetching). The wheel is byte-identical in four places: PyPI, the install host, the ZIP and the local build. Only the typed prune of the 0.5.23 wheel on the install host is left, and that is his to run. — **the schematics are drawn the way a textbook draws them.** Element names are set as a kind letter with a capitalised subscript — `rin` is Rₓₙ, `r1` is R₁ — inductors are coils of *loops* rather than rows of humps, and a controlled source is a diamond. Roberto's brief, with two textbook PDFs to work from; the grounding is written into the code, not just into this entry.

**The naming.** One `<text>` per label, one `<tspan>` per run, the subscript carrying `class="sub"` and a baseline shift relative to the run before it — which is what lets a caption come back up to full size after `R₁ = `. An underscore is a separator, not a character to print (`r_a` is Rₐ), so the display is many-to-one: `rab`, `rAB` and `r_a_b` all read Rₐᵇ. That was already true of case, and it is confined to the drawing — the answers, the exports and the description keep the name as typed. Written up under LIMITATIONS.

**The inductor.** The old body was `a r r 0 0 1 2r 0` four times: an exact semicircle over a chord of exactly 2r, which is a row of humps — a cursive `m`. A loop needs the arc to be *more* than a semicircle, so the chord has to be shorter than the diameter and the large-arc flag set: `a 7 7 0 1 1 11.5 0`, four times across the same 46px the zigzag spans. `2*IND_R > IND_STEP` is not a nicety but the condition for the arc to exist at all — at a chord of exactly 2r the two arcs coincide and the flag stops meaning anything. There is a test on that inequality.

**The diamond.** *"Dependent sources are usually designated by diamond-shaped symbols"* — Sadiku & Alexander, Fig. 1.13. A source is controlled when its value refers to another quantity in the circuit, and the test is built from the circuit's own names and folded the way `spice._fold` folds them, because `i_r1`, `ir1` and `IR1` are one name to the solver since 0.5.19 — searching for an underscore would have missed two spellings out of three. A consequence worth knowing: `e1,1,0,vs` in a circuit that has a node `s` draws as a diamond, correctly, because that is what it solves as.

**Also:** the resistor's peaks are mitred (the page's global `stroke-linejoin` is round, which turned each peak into a blob), and label placement now comes from each symbol's actual reach rather than one offset for every kind. The old fixed −11px cleared a resistor's 9px zigzag and ran *through* a capacitor's 13px plates; it would have run through the new coil too.

### What it found

**The review harness had never reviewed the working tree.** `review_schematics.py` computed its solver path with one `os.path.dirname` too many — `Symbulator/solver`, a directory that has never existed — so it silently fell back to the installed package. Every "clean run" since it was written was a clean run against whatever `pip` had. Fixed, and it now says so on stderr instead of falling back quietly. This is the schematic drawer's counterpart of the lesson #210 taught about `bridge.py`: **a guard nobody has watched fail is not yet a guard.**

With the path fixed, the harness immediately reported 306 of 330 circuits with findings — from the two new checks, both of which were real:

* **labels touching each other.** A vertical element's name and value were 15px apart, which the subscript's descent closed to nothing.
* **labels touching symbols.** This one needed the canvas to record where each body actually draws (`_Canvas.ink` — deliberately *narrower* than the `obstacle` a wire must clear, since every value label sits 3px above its own body by design). The first pass recorded the whole segment as ink and produced 485 findings that were all a node name sitting over a *lead*; recording only the body's extent, leads excluded, took it to zero.

Both are fixed, and the check is proved non-vacuous: forcing `GAP` to −14 makes it report the two labels it should.

### Round two: the labels were still touching

Roberto looked at the drawings and said labels were touching symbols. The harness said `with_issues=0`. **He was right and the harness was wrong**, and the gap between those two sentences is the most useful thing in this item.

The check compared label boxes against `_Canvas.ink`, and every `REACH` entry was a **path centreline** figure. A stroke puts another half-width outside its path — and a *mitred* one puts far more: the peak of the zigzag runs past its own vertex by half the stroke over the sine of half the vertex angle, **2.2px** at these proportions. So `REACH["r"] = 9.0` understated the resistor's ink by a quarter, and the mitre that made the peaks sharp (this same item, an hour earlier) is what widened the error. Labels the geometry called 3px clear were **1px clear on screen**.

Geometry could not catch this, so the fix was to stop asking geometry. **`tools/pixel_clearance.py`** renders each drawing with the labels forced to pure red and every stroke to pure blue, then grows the blue mask a ring at a time until it meets the red one. Real font, real glyphs, real stroke widths, no estimate anywhere. It put numbers on it immediately: 1.00px on the divider, the series RLC, the dependent-source circuit and the op-amp stage.

Every `REACH` is an ink figure now — half a stroke wider than its path, the resistor `ZIG_AMP + _ZIG_MITRE` — `GAP` is 4px, and the vertical labels' two magic offsets (17 and 20) are `reach + GAP + 1.5`. Re-measured: the tightest of the samples is 4.00px, which is the 4px it was asked for.

Two things the tool cost, worth writing down because both are easy to repeat:

* **Read a pixel's ink from the channel it removes from white.** Red ink takes the blue channel down; blue ink takes the red channel down. Classifying by "are R and B close?" reads a faint antialiased red — `(255,243,243)`, 12/255 of red and no blue at all — as carrying *both* inks, and the first version duly reported all eight sample drawings as collisions, uniformly 0.00px. A checker that reports everything is as useless as one that reports nothing, and looks more convincing.
* **Prove it can fail.** Forcing `GAP` to −14 must make it report the two labels it should. Both checks were run that way before either was believed.

The fast harness keeps its estimate-based check — it is a second, not twenty minutes — but `tools/README.md` now says plainly that it estimates, and what it cannot see.

### Round three: the sample was not the population

Round two fixed the four-pixel gap on eight hand-picked circuits and I said so. Running the pixel checker over **all 330** said something else: **21 of them below 3px, the tightest at 1.00px.** The eight I had chosen were not representative, and "I measured it" is not the same claim as "I measured all of it".

The offenders named themselves once the tool was made to report *which* label: `-2j`, `-4j`, `-5j`, `30j`, `1/gx`, `1/g4`, and the node names `ag`, `bg`, `cg` that the three-phase chapters use. Every one of them **hangs below its baseline**. Placement was computing "the label's baseline sits GAP above the symbol's ink" — but a baseline is not an edge. A `j`, a `g` or a `µ` descends past it and eats the whole gap.

So the font's real extents were measured the same way everything else in this item was, by rendering them: **ascent 9.75, descent 3.12** at 13px `ui-sans-serif` — and capitals alone still descend **1.25**, which is Q's tail, so even a name and its capitalised subscript are not flush with their baseline. Those are `LABEL_ASCENT`, `LABEL_DESCENT` and `CAP_DESCENT` now, and every offset in `_draw_element`, the node names and the op-amp's label are expressed as *ink clears ink by GAP* rather than as a baseline distance. `review_schematics.py` and the unit tests read the same three constants, so the fast check no longer has the blind spot that hid this.

Re-measured, the ten worst are 4.00-4.50px, which is the GAP they were asked for.

**Two process notes, both paid for.** The tool crashed while printing its own findings — a value carrying `µ` through a console on a legacy code page — and took thirty-five minutes of results with it; it reconfigures its streams now. And it originally reported only a number per drawing, which is enough to know something is wrong and useless for fixing it: naming the label turned a guess into a five-minute diagnosis.

**Where it stands.** 330 circuits, `failed=0 with_issues=0`, against the working tree this time. 317 solver tests pass, including six new ones for the naming, the loop condition, the diamond, the folding rule, and a unit-level version of the clearance check. **Nothing is deployed**: `schematic.py` is in the solver package, so this needs a PyPI release (0.5.24) before the hosted app sees it, and a rebuilt wheel for the two offline builds. No app-side file changed — `symbulator_ui.py` passes the SVG through untouched.

**#199 is done, 31 Aug 2026**, at solver **0.5.23** and cache **v114**: the solver package speaks in codes too — **thirty-six of them, 2xx–6xx**, one range per module — and with it the batch Roberto ruled on that morning is complete. `CircuitError` carries a code and its arguments; a plain string still works, which is what let the two halves deploy in either order. It found two bugs on the way, both by tooling: `app.py` flattened the code in its own parse step, and **`verify_bridge.py` — one day old — found the mirror image in `bridge.py`**, which is exactly what #210 was built for.

**#207 is done, 31 Aug 2026**, at cache **v113**: the thirteen dictionaries are downloadable files at `/i18n/<lang>.json`, with a `/translate` page explaining what may be edited and what is machinery, and a Languages section in the About card linking out to it. Server-only by design. Corrections go to **translate@symbulator.com** or a GitHub pull request. **No native speaker has reviewed any of the twelve**, and today alone added about 1,200 unreviewed strings — this is the only route to fixing that.

**#210 is done, 31 Aug 2026**, at cache **v112**: the offline path has a harness. `verify_bridge.py` runs every input through **both** front ends and compares them — 340 cases, **0 disagreements**. It exists because the day's shipped bug lived in `bridge.py`, which no check touched, and it found a second drift on its first run: `app.py` takes `variables` as a list or a string, `bridge.py` only a string. It needed one calibration, recorded in the entry — 201 of its first 201 findings were a benign shape, and a harness that cries wolf is one people stop running.

**#200 is done, 31 Aug 2026**, at cache **v110**: `symbulator_ui.py` speaks in codes too — **forty-one of them, 801–877**, across the validators, plotting, Evaluate, the mini-tools, SPICE and the notes, in twelve languages. The trap its own entry predicted was real and one function higher than expected: `_run_in_process` flattened every failure to a string before any route could name its code. Only **#199** — the package, with the release train — is left of the three.

**#198 is done, 31 Aug 2026**, at cache **v109**: **the Numerical Solver's engine speaks in codes** — seventeen of them, 901–924, with the page putting them into words. The status line that was four concatenated pieces (three of them untranslated English) is now one code and one `tv()` call: 已求解（最小二乘：3 个方程，2 个未知量） — 3 次求值. Roberto's design of that morning survived contact unchanged, which is what it was ordered first to find out; **#199** (the package, with the release train) and **#200** (`symbulator_ui.py`) can now follow it. The item's own costing had gone stale inside the day — #208 had put `eqsheet.py` into the offline builds, so 'server-only, no cache bump' was no longer true.

**#209 is done, 31 Aug 2026**, at cache **v108**: **twenty-four reader-facing strings that never reached the dictionary** are in it, twenty-two new keys across twelve languages — the line under every set of answers among them, now *DC 分析 · 12 个结果*. The lasting part is the guard in `tools/i18n.py check`, which finds literals reaching a reader outside `t()`; it caught two more on its first run that three manual sweeps had missed. Its blind spot — strings thrown as exceptions — is written down rather than chased. `time (s)` follows Roberto's ruling: the word translates, the unit symbol does not, in Ukrainian too, which brings it back into line with the `Ω` its own answers print.

**#208 is done, 31 Aug 2026**, at cache **v107**: the **Numerical Solver ships in the offline builds** — its own page, its own Pyodide, SciPy bundled, solving with no network at all. The ZIP is **31,682,389 bytes (30.2 MB)**, up from 17.8 MB, which Roberto agreed to against the measured figure; the app's one published "about 17 MB" string now reads **about 30 MB** in English and in all twelve translations. Along the way: `vendor/`'s provenance was recovered and written down (Pyodide **v314.0.5** — the version scheme changed, which is why every earlier probe 404'd) as `vendor_pyodide.py`, and a **live server bug** was found and fixed — a NaN residual travelled as bare `NaN`, which no JSON parser accepts, and hung the hosted Solver on *solving…* for ever.

**#204 is done, 31 Aug 2026**, at cache **v106**: the dictionaries are files now, fetched only when a language is actually used. The app page dropped from **941,815 to 271,905 bytes** while the ZIP grew 19 KB, and an English reader now makes no i18n request at all. Boot uses a parser-blocking script and a later switch uses an injected one — see the entry for why those cannot be the same mechanism.

**#203 and #206 are done and deployed, 31 Aug 2026**, at cache **v105**: the app speaks **thirteen** languages — **Hindi** and **Bengali** (terms of art transliterated into the reader's own script, per Roberto's ruling), and **Ukrainian**, which he asked for on political rather than reach grounds and which should not be tidied out of the list by speaker count. Ukrainian also exposed a real bug: a ribbon label long enough to wrap was being **clipped away silently**, and the test meant to catch that had been checking the wrong axis since #197. **#205 (Arabic and Urdu) is deferred at Roberto's instruction**; #204 is no longer a prerequisite for anything.

**#202 is done and deployed, 31 Aug 2026**, at cache **v104** — `install.symbulator.com` and the ZIP verified by fetching (the install page hash-matches the local build; ZIP sha256 `69280ce33b2dafd0b8139729398bcb027dc0d277f27e8d399f0ee15da1dac344`, 17,758,663 bytes). **`symbulator.pythonanywhere.com` awaits one pull carrying #201 and #202 together.**  **Indonesian** is the tenth language — the cheapest of the five candidates and the one whose readers most plausibly need it, since Indonesian engineering is taught in Indonesian. #203–#205 open the rest of that plan: Hindi and Bengali, the dictionary split, then the right-to-left pass for Arabic and Urdu.

**#201 is done and deployed, 31 Aug 2026**, at cache **v103**: the
ribbon's language control shows the chosen language as two letters, a
dot separates it from the Clear button, the Clear button abbreviates at
phone widths, and Esperanto is third in the list. See its entry below.

`install.symbulator.com` and `symbulator.com/9/local.zip` are live and
verified by fetching — the install page hash-matches the local build, the
ZIP is
`d1da9ad3e7372c0d2417073f8a6f434d226be078d1e1d6aea44ba44b923c630a`
(17,743,655 bytes), and the live host was checked in Spanish: face **ES**,
*Limpiar entradas* / *Limpiar*, the dot present, Esperanto third, build
stamp `2026-08-31 00:26 UTC`. **`symbulator.pythonanywhere.com` awaits
Roberto's pull** — `templates/index.html`, `templates/eqsheet.html` and
`i18n/es.json`, no solver release.

**#197 is done and deployed, 31 Aug 2026**: the app speaks nine
languages. `install.symbulator.com` and `symbulator.com/9/local.zip` are
live at cache **v102**, both verified by fetching and hashing — the
install page matches the local build byte for byte, and the ZIP is
`de42e5ca3b919f67f1bdf459688b8659caeb398551c6631f8133f3e9571e8e4b`
(17,743,392 bytes). Checked live in Portuguese and Esperanto, build stamp
`2026-08-30 15:52 UTC`.

**`symbulator.pythonanywhere.com` is done too** — Roberto's pull, same
day, carrying #183, #196 and #197. Verified by fetching, not by report:
`/healthz` gives build `2026-08-30 15:52 UTC` running *and* on disk,
`needs_reload: false`, solver 0.5.22 (no release was involved). A real
solve through `/api/solve` returns the expected answers with no notes,
and in the browser the same circuit solved in English, Spanish and
Japanese gives byte-identical mathematics with the interface in each.
`/eqsheet/` checked in Korean: headings, variable-sheet columns and the
DC/AC pair all translated, ribbon one line, no console errors.

**All five sites are current.**

**#184–#191 deployed 30 Aug 2026** to `learn.symbulator.com`,
`install.symbulator.com` and the ZIP, at cache **v99**, and verified by
fetching: the settings box, the *approx (full precision)* label, the Solve
card's waiting text, the centred SPICE row, the solver's Clear button and
its blank sheet, the renamed showcase, `sw.js` at v99 and the ZIP matching
by hash.

Version X has the same code: merged with `git fetch v9 && git merge
v9/main` — clean, no conflicts — pushed to `Symbulator-Team`, and live on
`symbulatorx.pythonanywhere.com`, verified the same way.

---

## #223 — the solver README calls `ap_` apparent power, and it is not — **done and pushed, 2 Sep 2026**

`repos/solver/README.md`, under *DC / AC / s-domain results*:

    - `res["p_<name>"]` / `res["ap_<name>"]` -- real/apparent power (DC / AC only)

`ap_` is **average real power**, the same quantity as `p_`. From
`symbulator/analysis.py:211`:

    out[f"p_{e.name}" if use_rms else f"ap_{e.name}"] = sp.re(s)

One value, `sp.re(V·conj(I))`; the name it lands under depends only on
the RMS setting — `ap` under peak-amplitude phasors (the default, with
the divide-by-two), `p` under RMS. Apparent power is the *magnitude* of
the complex power `s_<name>`, which the README documents correctly on
the next line. `_ELEMENT_KEYS` in `repos/server/symbulator_ui.py` has it
right too, labelling `ap_{n}` "average power" in W, and so does Lesson 8:
*"stores the average real power consumed in r, e, j and o elements in a
variable called **ap** plus the element name."*

**This line has already cost a wrong bug report.** A documentation review
on 2 Sep 2026 cited it to argue that Lesson 7's AS7 Example 9.9 had the
two swapped and should be rewritten. The chapter was correct; the change
would have introduced the error. See #220 in
`Documentation/NEXT_DOCS.md`.

Suggested wording: `real (average) power -- ap_ under peak-amplitude
phasors, p_ under RMS`, with a pointer to the `use_rms` paragraph
already three lines below.

### Done, 2 Sep 2026 — and it was in three places, not one

The grep found the same misconception twice more, both of which would
have kept regenerating the first:

* **`symbulator/analysis.py`**, `_derived`'s docstring, called `s_<name>`
  "apparent/complex power". `s_` is the complex power; the apparent
  power is its *magnitude*. Reworded to say what each name holds and
  which one the RMS setting selects.
* **`symbulator/tests/test_circuits.py`**, the AC power test, commented
  its assertion as "apparent power (peak convention) = |V|^2/(2R)". The
  number is right and the label is wrong — and **on a resistor the two
  quantities are equal**, so that test could never have caught the
  mislabel. That is why this survived: the only test touching `ap_` was
  one that cannot tell average from apparent power.

**So a test that can was added.** `test_ap_is_average_power_not_apparent_power`
uses a series R-L at the source, where S = −0.6 − 0.8j VA: the average
power is −0.6 W and the apparent power |S| is 1.0 VA. It asserts `ap_`
equals `re(s_)`, equals −0.6, and is *not* equal to `abs(s_)`.

Proved non-vacuous the way this tree requires: forcing
`p = sp.simplify(abs(s))` in `analysis.py` makes it fail with
`approx_eq(1.0, -0.6)` while the old resistor test still passes — which
is the whole point, and the sabotage was reverted immediately after.
337 tests pass.

No release: nothing shipped changed behaviour. GitHub carries the README
now; the PyPI page re-renders on the next real release.

## #219 — an `image:` field on an input-file entry — **done, cache v120**

Roberto's brief, 1 Sep 2026. An optional `image:` line on a `.cir` entry
names a picture of its circuit; when the entry is picked, the picture
appears at the **foot of the Input File card**, below the format
reference and under a hairline rule, with **no heading**. An entry without
one reserves nothing — the card simply ends at its ordinary bottom padding.

It first shipped (cache v118) in a headingless card of its own between the
input file and the circuit description; Roberto changed his mind the same
day and it moved into the Input File card at **cache v119**. It sits
*inside* that card's disclosure, so it folds away with the rest of the
panel — which means a picture could load into a closed box and never be
seen, so the image's `load` handler opens the panel, exactly as
`showNote()` already does for an entry's note.

The field is in `circuitbook.py` beside `note:`, in `_KEYS` and in
`format_book`'s key order, so it round-trips: an entry saved from the app
comes back with its picture. Like `note:`, it is deliberately **not** in
`inputsSnapshot()` — the picture is content of the entry, not a field on
screen, so *Update inputs in this entry* keeps it rather than wiping it.

### Local paths cannot work, and not only in the hosted build

The brief asked for a path to an image on the reader's own device "if that
can be made to work", and expected the answer to be that the hosted build
could not manage it. Measured, the answer is stronger and simpler: **no
build can**, and the reason is one both offline builds already live with.

All three builds are served over http(s). The hosted app obviously is; but
so are `install.symbulator.com` and the downloaded ZIP, because Pyodide
will not load WebAssembly from a `file://` URL — which is why the ZIP
ships `start.bat`/`start.sh`/`start.command` to run `python -m
http.server` rather than telling anyone to double-click `index.html`.
And an http origin cannot fetch a `file://` subresource at all.

Measured rather than reasoned, in a page served from `http://127.0.0.1`,
which *is* the ZIP's own case:

| written in the file | result |
|---|---|
| `file:///C:/…/circuit.jpg` (same folder as the page) | blocked |
| `file:///C:/…/circuit.jpg` (any other folder) | blocked |
| a bare `C:\Users\me\circuit.png` | blocked |
| `sibling.jpg`, `sub/nested.jpg` (relative) | **loads** |
| `https://learn.symbulator.com/…` | **loads** |
| an https URL that 404s | `onerror` fires |

So the field takes a URL or a path relative to the page, and the format
panel says plainly that a picture on your own computer cannot be linked
to. The third option the brief floated — resolving a sibling of an
uploaded `.cir` through the file picker — is not available either: an
`<input type=file>` hands over that one File and nothing around it.

### A dead link degrades to silence

The card starts hidden and is revealed by the image's own `load` event;
its `error` event hides it again. An entry with no picture, a link that
404s, a host that cannot be reached and an offline reader all therefore
produce exactly the same thing: no card, no gap, no broken-image box.

**`loading="lazy"` cannot be used here**, which is worth writing down
because the brief suggested it. A browser does not fetch a lazy image that
is not being displayed — and this one starts inside a `hidden` card, so
the `load` event that reveals the card would never fire and the picture
would never appear at all. It cost nothing to drop: there is only ever one
of these on the page, fetched only when an entry that has one is picked.
The value is also held to `http:`, `https:`, `data:image/` or no scheme at
all, since a `.cir` is reader-supplied content.

### The mapping was derived from the netlists, not from the names

The brief supplied a slug rule that resolved 255 of the 330 entries and
warned, correctly, that a rule resolving 255 is *a hypothesis about 255
entries*. It did not have to stay a hypothesis. Every chapter in the docs
tree writes each problem as `::: problem <name>` containing both the
figure **and** the `field 9 Circuit Description` netlist — so an entry can
be matched to a figure by the circuit itself, and the entry's name used
only to corroborate.

Netlist identity resolved **295** entries, not 255, and where the name
agreed it never disagreed: 163 entries matched on both signals, **163
agreements, 0 conflicts**.

Three structural facts had to be measured, each of which the naive reading
gets wrong:

* a figure inside the problem's `::: answer` is a *solution* step, not the
  circuit (`b11e0507b.jpg` is Example 5.7 "with the node names pencilled
  in"). Excluding those cut the ambiguous entries from 47 to 28;
* a figure *after* the netlist is a screenshot of the answer or the
  textbook's printed answer, not the circuit. Excluding those took 28 to 6;
* the last 6 were looked at — actually looked at, as pictures — and in
  half of them the first figure is a **scan of the problem's prose** and the
  second is the circuit. Aspect ratio does not separate the two: the
  flattest image in the whole set (`a-more-complex-problem-44.png`, 5.34:1)
  is a real circuit, and a 6.3:1 one is prose.

Four more entries were added by name where the netlist is a *notation*
variant of the same physical circuit — `re,1,0,[10'k,22'k]` is the
chapter's R2 and R3 in parallel — each checked against its figure by eye.
**299 image lines across 248 distinct pictures**, and every pair was
either matched by netlist identity or looked at.

**Two entries in `The_Monograph.cir` legitimately have one**, against the
brief's expectation that it would have none: their own notes say "Lesson 9
solves it too" and "Lesson 10 has it too", and the netlist match found the
tutorial figure the slug rule could not.

### What was deliberately left without a picture

31 entries. `Showcase.cir` (12) and six of the monograph's eight are drawn
by the schematic engine and never were scanned figures. The other 13 are
entries whose chapter prints no circuit for them because they *modify*
another problem's circuit — Bo2's Drill Exercise 5.11 reads "for the
circuit of Bo2's Example 5.7, change the value of the capacitor to ¼ F".
Reusing 5.7's figure there would put a picture with the wrong capacitor
and the wrong source over a netlist that has neither, and **a confidently
wrong picture is worse than none**: nothing on the page would look broken.

### Online links, and what stops them drifting

Roberto's decision, 1 Sep 2026, given the measured numbers: the 248
pictures total 23.4 MB raw against a 30.3 MB ZIP, or 8.3 MB re-encoded to
900px wide at quality 82. **Online links** — so the ZIP does not grow, no
second copy of the images exists, and the offline reader simply sees no
card.

That leaves the app depending on the docs tree, which nothing else joins.
A figure renamed on the docs side would leave a dead link here, and a dead
link is *invisible by design* — the card hides itself. So
**`repos/server/tools/check_example_images.py`** exists: every `image:`
URL must name a file that is really in `Documentation/assets/`,
and `--live` fetches all 248 from the real site. `build_local.py` runs the
plain form on every build — soft when `Documentation` is not beside the tree,
since the offline build does not use these pictures, and hard on a link it
can check and finds broken. Both the tool and the build hook were **watched
going red** on a deliberately broken link before either was believed.

`--live` earned its own lesson. The first version fetched eight at a time
and reported 23 dead links; every one served 200 when asked again on its
own. It now retries, runs three at a time, and separates an HTTP status —
which it believes — from a transport failure, which it reports as "could
not reach" rather than as a broken link. All 248 verified live.

### Shipped

**Two placement rounds after the first live look**, both cheap because the
feature was one block of markup. v118 put the picture in a headingless card
of its own between the input file and the description; v119 moved it to the
foot of the **Input File** card; v120 moved the *"About input file (.cir)
format"* reference **above** *Built-in Examples*, so that card now reads
Upload/Download/Create new → the format reference → Built-in Examples →
the entries picker → its note → the picture. The last two were pure
markup reorders: no wording changed, so no i18n key was regenerated and
all thirteen dictionaries stand untouched.

Version 9's PythonAnywhere pass for v120 is **done** (1 Sep 2026): `/healthz` build `2026-09-01 12:03 UTC` running *and* on disk, `needs_reload: false`, solver 0.5.26 — the served card ordering checked (upload row → format reference → Built-in Examples → entries → note → picture) and the picture hit-tested live at 798×540. X's account followed the same day: `symbulatorx.pythonanywhere.com` reports the same build `2026-09-01 12:03 UTC` running and on disk, with the card ordering, the picture (798×540, hit-tested) and a real DC solve all verified live — so the merge carried #219 across without breaking X's engine.

**#219 crossed to version X on 1 Sep 2026.** `git fetch v9 && git merge
v9/main` ran clean on `Application/vX/repos/server` and `repos/local` (the
solver needed nothing), and both are pushed to `Symbulator-Team`. X now
differs from v9 by its own orientation `CLAUDE.md` files **and nothing
else**, which is the state that keeps future merges clean.

Worth knowing for the next crossing: X's `build_local.py --check` reports
`i18n/zh.js` STALE straight after a merge, and it is **not** stale. The
dist dictionaries are near-single-line JS; git checks them out with LF
while `build_local.py` writes CRLF, so the four line endings make a 4-byte
difference and a byte-for-byte check calls it stale. The content is
identical. **Do not "fix" it by running `build_local.py` in X** — that
re-stamps the build time into `templates/index.html`, which diverges X
from v9 on a line every future merge would then conflict on. Leave it.


**A zero measurement means the viewport, not the bug.** Verifying the moved
picture on the live install site, the image measured **2px tall** with
`max-height` computed to `0px`. That looked like a real fault in the new
placement. It was not: `innerWidth`/`innerHeight` were **0** and
`document.visibilityState` was `hidden` — the browser pane was collapsed, so
`60vh` is `0`, a `width:100%` box is `0` wide, and everything under it
measures nothing. It also explains a session's worth of "stale" screenshots
that contradicted the DOM. Forcing a viewport (1280×900) gave the real
numbers immediately: `max-height` 540px, the image painted at 798×540 with
`elementFromPoint` returning `IMG#entryImage`, 23px from the picture's
bottom to the card's. This is the trap the shared `CLAUDE.md` already names
— it is written down because it keeps working.


Deployed 1 Sep 2026 on Roberto's go, and **all five sites are current at v119** — his PythonAnywhere pass for the move landed the same day (`/healthz` build `2026-09-01 09:41 UTC` running and on disk, `needs_reload: false`, solver 0.5.26; the picture verified on the live app by hit-testing it at the foot of the Input File card). `install.symbulator.com` and
`symbulator.com/9/local.zip` are live at cache **v119** (the picture in the
Input File card; v118 was the same feature in a card of its own), hash-verified by the deploy script and then by fetching: the card
appears, the picture loads, and two entries from different lesson books
were driven on the live site. Both repos are pushed.

Roberto's PythonAnywhere pass followed the same day: `/healthz` reports
build `2026-09-01 08:52 UTC` running *and* on disk, `needs_reload: false`,
solver **0.5.26** — no `pip` upgrade, since #219 shipped no solver release,
though the *pull* mattered (`templates/index.html`, `circuitbook.py` and
`i18n/` all changed). Verified on the live app rather than from the
console's exit status: an entry loads its picture, switching entries swaps
it, a real solve is right (36 V over 1k+3k+2k gives v2 = 30 V, v3 = 12 V,
ie = −6 mA), and a Showcase entry leaves **no card and no gap** — the space
between the input-file and description cards measures 21px, which is the
ordinary card margin and not a reserved hole.

Two things worth remembering from the deploy itself:

* **`build_zip.py --assets` only supplies `vendor/` and `static/`**, and
  the repo wins every overlap, so a stale extracted copy at
  `Application/v9/local/` cannot put old examples in the ZIP. `install_site/`
  is the one staging folder that *does* have to be refreshed by hand from
  the built ZIP, and it is deliberately five files short of it — the
  launchers and README belong to the download, not to the hosted site.
* **The stale service worker did exactly what it always does.** The first
  live check found no card at all, and a `fetch(..., {cache:'reload'})`
  agreed — because the SW is cache-first, so that fetch never reached the
  network either. `curl` settled it in one request: the server's
  `index.html` was hash-identical to the local one and had the card all
  along. Unregistering the worker and clearing the caches showed the real
  page. Do not diagnose this one from inside the page.

---

## #218 — the three passive symbols, redrawn — **done, solver 0.5.26**

Roberto's brief, 1 Sep 2026, from reference images rather than words:
the resistor's peaks rounded, the inductor a single line that loops, the
capacitor with one bowed plate. Settled one parameter at a time against
rendered strips — the working method his conventions already ask for,
and the only one that would have worked here, because every one of these
was a shape nobody could describe accurately enough to build blind.

**The resistor.** Each corner is a quadratic whose control point is the
old vertex, leaving the straight run `ZIG_ROUND` back along one arm and
rejoining it the same distance along the next. A quadratic leaves its
first control point along the line to the second, so the curve is
tangent to both arms and there is no join to see. `stroke-linejoin
="round"` was the free alternative and is a different thing: its radius
is fixed at half a stroke, 0.85px, which is the blob #212 rejected.

**Rounding a corner cuts it off**, so the drawn peak is 6.51px against
the 7.20 amplitude, and *that* is the number a label has to clear. REACH
is built from the drawn peak, not the amplitude, and the resistor's
labels moved 2px closer (9.37 → 7.36). A 10% size reduction was also
tried, measured clean across all 330, and then withdrawn — the size is
unchanged.

**The inductor took three shapes to get right, and the first two were
wrong in ways only measurement showed.**

* *Arcs between two points on a line cannot cross their own chord.* The
  large-arc flag takes the major arc, over the top; the far side of the
  circle lies on the minor arc. I built it, lifted it above the leads to
  make the loops dip, and the sampler came back **0.00 below the leads**
  on every variant. On eye alone I would have shipped it.
* *A row of whole ellipses* does cross the line, but reads as separate
  rings rather than one wire, which is what Roberto said when he saw it.
* What it is now: a **projected helix**, the prolate trochoid
  `x = A·t − B·sin t`, `y = −H·cos t`, emitted as cubic Béziers fitted
  to the analytic derivative. It loops exactly when `B > A` — that is
  when `dx/dt` changes sign and the line doubles back. At `B == A` it is
  a sine wave with no crossings. `IND_RATIO` is that ratio and the only
  number that decides it; the test walks the emitted curve counting
  reversals rather than trusting the constant.

The span carries an **extra half turn**, so one end dives into a loop
and the other rises out of an arch. `IND_PHASE` decides which end, and
it took two goes — the first put the arch at the near end. Worth
knowing: flipping the phase changes the advance, because the endpoints
must stay `BODY` apart and the B term moves them relative to each other
in opposite directions at the two phases. A went 2.501 → 1.692 across
the flip and the retune to `IND_RATIO 2.6`.

**The capacitor.** The bowed plate's ends stay on the old chord and its
middle comes in by `CAP_BOW`, so the plates are 7.5px apart at the
middle against 11 at the corners. The lead runs in to the **apex**: the
arc's chord is no longer on the axis, so a lead stopping there leaves a
visible gap between the wire and the curve it is supposed to meet —
which is exactly what Roberto spotted in the first mockup. The radius
comes from the sagitta, so the bow is the depth asked for.

**The capacitor keeps its straight plates.** A bowed one was built and
drawn for a few hours, and Roberto withdrew it on the reason rather than
the look: a curved plate conventionally marks a **polarised** capacitor,
and Symbulator's are not — `c1,2,0,1'u` has no + end and the engine never
treats one terminal differently from the other. There is a test on the
plates being straight so it cannot drift back.

**A reversed transformer says it once.** `t,2,3,1,-2` draws as `1 : 2`
with the dots opposed — the dots carry the polarity and the printed ratio
shows magnitudes. It shipped for a few hours saying it *twice*, sign and
dots both, until Roberto asked whether the inversion was deliberate or a
double count. It was a double count: the engine sets `v(n1)/turns1 =
v(n2)/turns2`, so a reader applying both reversals reads AS7's Example
13.8 as `+2`. There is a test, and it covers `-1,-2` — two negatives are
the *same* polarity — and the symbolic `1 : n`, which has no sign to read
and so keeps its dots level.

**The two-port stopped being an element in a branch.** It was a labelled
box in line between its two nodes, which implied a single series current
the element does not carry — its two port currents differ, the difference
going to ground. It is a square block now, four terminals, upper pair on
the node row and lower pair on the rail, with its four parameters written
inside it. Nothing else on the drawing said what a `z` or an `h` block
does; the reader had to go back to the description for `[40,20j,30j,50]`
and remember that the order is 11, 12, 21, 22.

Its height is written `ROW_H + 2*PORT_BOX_OVER` rather than the literal
174, because that is the only value that lands the lower terminals on the
rail and lets their leads run out unbent — a literal would have quietly
brought the bend back the first time anyone touched the band.

**One ground symbol per run of rail**, which is a rule rather than a
special case: a block that grounds itself says so mid-gap and the rail's
own far-left symbol is dropped, and a two-port ends up with two symbols
not by exception but because it *cuts* the rail and each half is a run.
The node's name moved from beside the bars to under them, which retired
the `side` argument that existed only because a symbol set left of a
block had the box hard against it.

### How this one was actually done

Nine rounds of rendered strips, and the reason it took nine is worth
keeping: **every one of these was a shape nobody could describe
accurately enough to build blind.** "Less tall" turned out to mean less
tall *relative to the width* and then, two rounds later, genuinely
shorter than the band. The measurements settled it each time —
Roberto's reference at w/h 1.10 against a drawing at 0.72 is a fact; "it
looks too tall" is not something either of us could have acted on.

Two mistakes are worth naming because measurement caught both and eyes
would not have. The lifted-arc coil measured **0.00 below the leads** on
every variant, which is what proved that construction cannot cross its
own chord. And when the two-port's grounds were moved to the midpoints
of their gaps they came out at 56 and 323 instead of 86 and 294 — the
*legs* had moved and the symbols were still offset thirty pixels from
where the legs used to be.

---

## #217 — an SI prefix is a decimal shift, so it is done in decimal — **done, shipped in 0.5.25**

Roberto, 1 Sep 2026: `js,0,d,397.3'm` translated to SPICE as
`Is 0 d 0.39730000000000004`, where `js,0,d,.3973` gave `Is 0 d 0.3973`.
Same current, two spellings, one of them showing the reader a binary
artefact.

**The noise was born nowhere near the netlist.** `397.3'm` expanded to
the *expression* `397.3*10**-3`, and multiplying those out in binary
lands one unit in the last place from the decimal that was typed.
Nothing downstream can undo that — it is a different double, and `repr`
is right to print all seventeen digits of it. The exporter's `_exact`
was doing exactly its job. So the fix is upstream: the prefix is folded
into the number in **base ten**, with `decimal`, before anything binary
sees it. Quoted form and bare suffix, every prefix, every element.

**What was deliberately *not* changed.** A whole-numbered mantissa keeps
the `n*10**e` form, because SymPy reads that as an exact Rational —
`100'p` is 1/10000000000, not a float, and a circuit of whole-numbered
values still solves exactly, which is what "Rounding: exact" is for.
Folding those too would have quietly turned every `4.7'k` circuit's
exact-mode answers into fractions. Only a mantissa that already has a
decimal point — a Float either way — is folded.

**The same bug ran the other way, in the two number formatters.**
`2.2e-9 / 10**-9` is 2.1999999999999997 in binary, so `2.2'n` went out
as `2.1999999999999997N`. That one only became visible *after* the
first fix, because the input noise had been masking it. Both formatters
now take the mantissa out in base ten and verify it by reading the
decimal back rather than by multiplying floats. `100'p` gained from it
too: it used to come back as `100.00000000000001P`, and is now `100P`.

**The blast radius was measured, not assumed.** Of the 330 example
circuits, seven use a decimal mantissa with a prefix — the only ones
whose stored value can move at all — and all seven print byte-identical
answers before and after, checked by running each one twice with the
old expansion monkeypatched back in. The stored double moves toward the
value the reader typed; nothing the reader sees moves.

Five tests, in `test_suffix.py` (the fold, and the Rational that must
survive it) and `test_spice.py` (Roberto's case, every prefix through
the round trip, and the SPICE suffix read back).

---

## #215 — the monograph showcase, restated — **done, in the working tree**

Roberto's own rewrite of the entry, 1 Sep 2026, in
`Application/v9/repos/server/examples/The_Monograph.cir`, in two passes. The
circuit is the same circuit; what changed is how it is *written*, and it
now reads the way #213 draws it — implied multiplication and no
underscores in the controls: `jd1,a,b,0.2vr7`, `ed2,c,b,0.1ir5`,
`jd3,n,c,2ir1`, `ed4,0,n,0.7vr6`. The expert equations follow the same
hand: `pjd1 = -80` and `ped2 = 0`. Rounding moved from 5 digits to **4**,
and the entry now carries `units: yes` and `show_equations: yes`, so it
opens with units on and the equation system on screen.

**The second pass renamed the two unknowns after their own elements**:
`es,e,0,es` and `js,0,d,js`, with `unknowns: es, js` and the conditions
to match. An element whose value is its own name is not a special case
to the solver — `es` is an ordinary free symbol, and `v_es` / `i_es` are
its answers — and it is not one to #214 either: the unknown is still the
whole of an element's value, so it still inherits that element's unit.
The note's names moved with it (`Find positive values of Es and Js`);
the numbers in it did not need to.

Verified in the running app: it solves, the answers are unchanged, and
the Expert Mode block reads `is = 0.3973 A` / `vs = 17.61 V` (which is
#214's fix, found on this very entry).

`repos/local/examples/The_Monograph.cir` is now behind the server copy,
as it should be -- it is generated by `build_local.py`, which runs at
deploy time. Nothing to do by hand; just do not edit it.

**One thing left for Roberto.** The entry's `note:` still quotes the
answers to five digits — *"Vs = 17.614 V and Is = 0.39727 A"* — because
that is what the monograph's §5.2 prints, and the note is tied line by
line to it. At rounding 4 the app now shows 17.61 and 0.3973. The note
was left exactly as it was: a documented value is authoritative until he
says otherwise. Say the word and it becomes 17.61 / 0.3973, or the
rounding goes back to 5.

---

## #214 — Expert Mode's own answers get their units — **done, in the working tree**

Roberto, 1 Sep 2026: *"in the Results area, the Expert Mode results are
not given units of measure (e.g. V, A, W) like the rest of the answers
above do."* He was right, and the reason is worth writing down.

Every other answer in the Results carries a **prefix** the formatter can
read a unit off: `v_e` is volts, `i_r7` is amps, `p_jd1` is watts. An
Expert Mode unknown carries nothing — `vs` in `es,e,0,vs` is an ordinary
free symbol with no underscore, so `key.split("_")[0]` came back empty
and the whole Expert Mode block was the one part of the Results that
ignored the "Show units" checkbox.

**The circuit says what they measure, so the circuit is what is read.**
`_value_units()` walks the elements and maps every free symbol that *is*
an element's value to that element's unit: a voltage source's value is
volts whatever the reader called it. That covers every shape in the 330
examples — `vs`, `is`, `rx`, `r_b`, `ix`, `is1`, and the bare `e`, `r2`,
`r3` of B11's Example 6.19.

**The unknown has to be the whole of the value, up to things that carry
no dimension.** `e,1,0,a*u(t)` still makes `a` a voltage — the unit step
has no dimension — but `j,2,0,gm*vrg` does *not* make `gm` a current:
that is a transconductance times a voltage, and the second dimensional
name in the expression is exactly what says so. Guessing from the
leading letter instead would have got `vs` and `is` right and `gm`,
`zeta` and `sigma` wrong; guessing from the circuit gets all of them
right and knows when to say nothing. A symbol that is the value of two
elements of different kinds also gets nothing — there is no answer that
is right for both.

`H` and `F` joined `_UNIT_LATEX` on the way past: an unknown standing for
an inductance or a capacitance can now carry one, and they would have
come out as italic maths otherwise.

Verified in the running app: the showcase reads **is = 0.3973 A** and
**vs = 17.61 V** where it read bare numbers before. Front end untouched
— it renders `plain`/`latex` as they arrive.

---

## #213 — a dependent source shows what it is reading — **built, unreleased**

Roberto's brief, 1 Sep 2026. A schematic that prints `4*ir1` inside a
diamond and nothing else has told the reader that *some* current
controls the source and left them to work out from the netlist text
which r1 and which way round — which is the one thing a schematic
exists to save them. So the control is now drawn on the element it
reads, and the value inside the diamond is typeset to match.

**A voltage control marks its drop.** `ed,3,0,2*v_r1` puts a **+** at
r1's first node and a **−** at its second, just outside the body on the
leads, where Sadiku and Boylestad both put them. The direction is not a
choice: `v_r1` is v(n1) − v(n2) (`engine.stamp_all`), so the + is at n1
every time, whichever way round the layout happened to draw the element.

**A current control marks its direction.** `ed,3,0,4*i_r1` draws an
arrow beside r1 running first node to second, head at the second, and
labels it *i* with `R1` as its subscript — a sloped lower-case i, the
way every book sets a current. Again not a choice: the solver's positive
`i_r1` flows n1 → n2 through the element (`engine._stamp_r`).

**And the value is typeset the same way.** Whatever the reader typed,
the drawing sets multiplication as implied rather than starred, a
voltage or a current as its own lower-case sloped letter, and what it
names as a capitalised subscript. `2*v_r1`, `2vr1` and `2*VR1` all read
*v*_R1 in the diamond, exactly as the resistor beside it reads R₁. Two
things the star rule has to get right: `2*3` keeps its star (`23` is a
different number), and the *names come out of the string before the
stars do* — dropping them first fuses `2*x*ir2` into the single word
`xir2` and the current inside it is never seen again, which is what the
first cut of this did.

**`pi` became the letter on the way past**, and for the same reason the
star went: spelled out and run together, `100+24*pi*j` draws as the
unreadable word `24pij`, where `24πj` reads at a glance. Seven values
in the example books are affected. The degrees rewrite (`30*pi/180`
→ `30°`) runs first, so what is left is a real π.

**What is not marked.** A node voltage (`2*v_2`) is a real control and
makes a real diamond, but there is no element to put a sign on; it is
typeset in the value and left at that. Nor are the non-two-terminal
kinds — an op-amp or a two-port block has no single pair of terminals a
sign could sit at. And precedence follows `engine._alias_map` exactly:
node voltages are claimed first, so in a circuit with a node called `x`
the token `vx` is *that node's* voltage and not the drop across an
element called `x`, and nothing is marked. The drawing has to say what
the solver will actually solve.

48 of the 330 example circuits carry marks.

### What it found

**`STACK_H` had never been measured.** A lifted source hangs its value
*below* its circle and the element on the row beneath stacks a value and
a name *above* its own: 34.75px down against 45.35px up, so the gap
needed 84 and had 78. The two had been overlapping by 0.4px ever since
#212 gave every name a subscript — under `review_schematics.py`'s 2px
tolerance, and so invisible until the *values* gained subscripts too and
it grew to 2.1 on three circuits. Now 88. The same lesson as #212's
three rounds, one layer up: the number that had never been computed was
the one that was wrong.

**The guard was made to go red on purpose** before its green was
believed — `_reference_marks` called with the symbol's reach forced
negative puts the new arrows and signs through the bodies, and the
harness reports 29 circuits with label clearances, naming the new `iR1`
labels among them. With the marks where they belong: `total=330 failed=0
with_issues=0`, and the exhaustive check clean too — `pixel_clearance.py
--all --min 3` over all 330 drawings, **tightest 4.00px, nothing below**.
4.00 is `GAP` exactly, so nothing is even marginal, and the tightest ten
are all pre-existing descender cases (`ag`, `1/gx`, `1/g4`) rather than
anything the marks brought.

### Where it stands

Built, tested (328 solver tests, up from 323) and clean on both
schematic harnesses, **in the working tree and unreleased**. It ships in
the next solver release train — PyPI, the bundled wheel, the two offline
deploys at a new cache version, `requirements.txt`, and the
PythonAnywhere pass — which is Roberto's go.

---

## #197 — the app speaks nine languages — **done, deployed everywhere, cache v102**

Roberto, 30 Aug 2026, briefed as an overnight run: a language menu, and
the interface translated into **Spanish, French, German, Portuguese,
Chinese, Japanese, Korean** and **Esperanto**. Nine with English.

**All nine are done**, both pages, all three builds. What follows is why
the scheme is the shape it is, and the four things that nearly went
wrong.

### It had to be a dictionary in the page

There are three builds and only one of them has a server. `install` and
the ZIP are static files with Pyodide in the tab; a Flask-Babel or
`gettext` scheme would have translated the hosted app and left the
downloaded one in English, and per-language templates would have forked
the one-template property `CLAUDE.md` guards. So: **one client-side
dictionary, applied in the page**, on the model of the theme switch —
stored in `localStorage` under `symbulator-lang`, read by the same
head script that applies Dark Mode before first paint.

Roberto's note offering the server alone was not needed. It cost nothing
to do all three: the dictionary that works on the server is the same file
the offline page carries, and *excluding* the offline build would have
been the extra work.

**English is not in the dictionary.** The page's own markup is the
English, so `applyLang` snapshots what it finds before writing anything
and restores the snapshot for English. That halves the payload and, more
usefully, makes it impossible for the English to drift from what the
template says.

### What is translated, and what is deliberately not

**474 keys**: 265 units of markup, 169 strings the page's JavaScript
writes at runtime, and 42 terms the maths engine names (element kinds,
the quantities in the Results card, the twenty-odd two-port parameter
descriptions), looked up on the way in through `tSrv()`.

Never translated, and the reasons are not stylistic:

* **The mathematics.** No decimal comma, no localised number formatting
  — `toLocaleString` stays pinned to `'en-US'` where it appears, with a
  comment saying why. `v_1 = 8` reads `v_1 = 8` in all nine, and it was
  measured, not assumed (below).
* **The syntax.** The Fields column of the elements table
  (`name,n1,n2,value`), the two SI cells that spell alternatives
  (`'k or 'K`), and the sample `.cir` file in the format card. Those are
  what a reader types, and the tutorial spells them this way in every
  language.
* **The wordmark and the build stamp.** `notranslate`, both of them. The
  stamp especially: `build_local.py` rewrites it with `STAMP_RE` and
  expects exactly one in the file, so a copy inside a dictionary would
  fail the build — which is the good outcome — or freeze the version a
  reader is told they have.
* **The tutorial, the landing page, the PDFs, and the 330 example
  entries.** Out of scope by the brief — and **confirmed as a standing
  decision by Roberto on 31 Aug 2026**: *"I'm fine leaving the notes in
  the input files in English. At least for now."* So the examples' titles
  and their `note:` lines stay English, in every language, until he says
  otherwise. They are tied line by line to the printed chapters and were
  verified entry by entry against them; translating them is not a
  translation job but a second edition of the tutorial.

### The menu

A native `<select>` in the ribbon, beside the theme toggle — the one
control a phone renders as a proper picker, and this one has nine
entries. Its options are the languages' own names for themselves, so it
is `notranslate`; its accessible name comes from the dictionary instead.

Roberto asked (31 Aug) that the ribbon never wrap, offering abbreviations
if needed, and that *Clear all inputs* become **Clear inputs** to make
room. Both done. The abbreviation is **decided by measurement, not by a
breakpoint**: a breakpoint measured against English wording is wrong in
eight other languages, so `syncLangMenu()` writes the names, looks at
whether the row wrapped, and falls back to ISO codes if it did.

Two things that taught: a `<select>` sized `width: auto` is as wide as
its **widest** option, not the selected one, so all nine option texts
have to change together for the control to shrink at all. And wrapping is
not the only way the ribbon runs out of room — `banner.css` caps `<nav>`
at one line-box and *clips* what wraps inside it, so a wide control next
door does not push the row onto two lines, it silently takes the Tutorial
link off the screen. German found that: *Eingaben löschen* is 36px wider
than *Clear inputs*, enough at 375px to cost the reader the only link out
of the app. The crowding test now asks the nav whether it had to clip, as
well as counting rows.

`banner.css` itself is untouched. The menu's styling is app-local, in the
page's own `<style>`, because only these two pages speak nine languages.

### The machinery

`repos/server/tools/i18n.py`, documented in `tools/README.md`. It finds
the translation units, tags them, packs the dictionaries into the
templates between markers, and — the part that matters six months from
now — **checks**. A translation is written into the page as innerHTML, so
one that drops an `id`, an `href` or a `%{slot}` breaks the page
silently; `check` fails on all three, on stale keys, on orphans, on a
`t(key, …)` whose key is a variable (invisible to the extractor, so it
would fall back to English in all eight languages with nothing to say
so), and on a new element kind in `symbulator_ui.py` that no language has
a word for yet.

`pack` escapes `<`, `>`, `&` and `{` inside every string. That is not
tidiness: `{#` inside an HTML comment took every server page down on
30 Aug, and eight languages of prose none of us can proofread as code is
a lot of new opportunity to do it again.

The keys are a readable slug plus four hex of the English's SHA-1, so
editing an English string mints a new key and the stale translation shows
up as an orphan rather than staying on screen.

### Verified

* **A real solve in each of the nine**, twice — a DC ladder and an AC
  circuit with polar phasors — comparing the rendered mathematics.
  Byte-identical across all nine, both times.
* **All 48 entries of Lesson 3 run through the real page** in English,
  then Korean, then Spanish — each entry three times in a row, comparing
  the rendered mathematics. Zero mismatches. (The first attempt at this
  reported thirteen; every one was the harness racing a slow symbolic
  solve, because it waited for a result row to appear rather than for the
  Run button to go fresh. A measurement that can be wrong in only one
  direction is not a measurement.)
* `tools/verify_lesson.py` clean on Lesson 1, Lesson 3, Lesson 13 and the
  Showcase — the API path is language-blind by construction, but the
  templates changed and this is what says the answers did not.
* **Loading an entry raises no phantom unsaved edit** in Korean. The
  language is in `localStorage`, never in `inputsSnapshot()` or the
  `.cir` file: it is a reader's preference like the theme, and #182's
  warning compares that snapshot.
* **The ribbon is one line in all nine at 375px and at 1280px**, with the
  nav unclipped; screenshots in both themes.
* **The offline build**, served and solved: Spanish applied before first
  paint, all eight dictionaries present, Pyodide solving with translated
  labels, and the server-only blocks correctly absent — the host notice
  and the *Run Symbulator 9 locally* card are gone from the markup, and
  no dictionary entry paints them back, because a unit spanning a
  `server-only` marker is never a unit.
* Flask renders `/`, `/eqsheet/` and `/healthz`; no console errors on
  either page.

### Found along the way

`PROMPT_i18n_overnight.md`, the brief for this item, had been committed
into `repos/local`, and `build_zip.py` swept it into the ZIP and from
there would have put it on `install.symbulator.com`. Its exclusion list
was by exact name; it now drops **every top-level `.md`** — users get
`README.txt`, and the next working note will not need remembering. The
brief itself was deleted from the repo at Roberto's ask once the item
was done (31 Aug 2026); it survives in this repo's history at `34084c8`
and the rule in `build_zip.py` outlives it.

Three things worth knowing but not fixed tonight:

* **The maths engine still speaks English.** The solver package's 31
  `CircuitError` messages, `symbulator_ui.py`'s notes and warnings, and
  the Numerical Solver's status line all reach the reader in English in
  every language. Its closed vocabularies are translated (that is what
  `tSrv` is for); its sentences are not. Written up as **#198**.
* The `.cir` sample in the input-file card stays English. It is a file
  listing whose keys (`title:`, `analysis`) are English keywords.
* The app page is 660 KB now, 213 KB gzipped, against 270/85 before. Each
  page carries only the keys it asks for — that took the Numerical Solver
  from 475 KB to 90 KB — but the app really does use nearly all of them.

### Lines a native speaker should check

The Spanish is the one Roberto will read, and one decision in it is worth
his eye more than the rest:

* **`voltage` is rendered `voltaje`, not `tensión`**, throughout — chosen
  for a Panamanian student audience over the more formal term. It is one
  find-and-replace in `i18n/es.json` if he or Antony García prefers
  `tensión`; the words that would move with it are *voltaje*, *fuente de
  voltaje*, *caída de voltaje* and *Voltajes de nodo*.
* **`two-port` is `cuadripolo`** (es), *quadripôle* (fr), *Zweitor* (de),
  *quadripolo* (pt), *二端口* (zh), *二端子対* (ja), *2포트* (ko),
  *duopordo* (eo). The Esperanto one is a coinage; the other eight are
  the settled term.
* **`Expert Mode`** is *Modo experto* (es) but *Modo avançado* (pt) and
  *전문가 모드* (ko) — the Portuguese reads better as "advanced" and I
  took that liberty.
* The three group headings are spaced capitals —
  `[ E N T R A D A S ]`, `[ H E R R A M I E N T A S ]` — and the longest
  of them is the Spanish one. It fits at 375px; it is the first thing to
  shorten if any wording grows.
* Esperanto's *tensifonto* / *kurentfonto* are compounds rather than
  *tensia fonto*; both are used.

---

## #201 — the ribbon's language control, reworked — **done, cache v103**

Roberto, 31 Aug 2026, in four passes over the course of the morning:
Esperanto third; the chosen language shown as two letters rather than its
full name; a separator between *Clear inputs* and the language; and then
the better idea that made the rest fit — abbreviate the Clear button
itself when the screen narrows.

### The chosen language is two letters; the list keeps the names

A native `<select>` displays the **selected option's own text** when
closed, so the closed control and the list cannot differ. That is the
whole constraint. The construction:

* the two-letter face is a `<span>` in normal flow and **defines the
  width**;
* the real `<select>` is stretched over it, `opacity: 0`, still taking
  every click, key and mobile picker.

The obvious version — make the select's own text transparent and leave it
in flow — looks identical and **saves nothing**: a `<select>` sized
`width: auto` is as wide as its *widest* option whatever colour its text
is. Measured on the live ribbon: full name **79px**, transparent text
**79px**, this construction **35px**. It is a good trap, and the sort
that ships because the screenshot looks right.

### Why not flags

Mocked up and rejected, in this order of severity. **Windows does not
render flag emoji at all** — on Roberto's own machine 🇪🇸 comes out as the
letters ES in a box, so the flag variant silently becomes a worse version
of the letters for every Windows reader. **Languages are not countries**:
Spanish would fly Spain's flag at a Panamanian audience, our Portuguese
is Brazilian, English has two candidates and Chinese three. And
**Esperanto has no country by design** — its green star is not an emoji.

### The dot

`·`, at every width, between the Clear button and the language. Not a new
mark: it is already this design's separator, used 38 times in the app —
the footer's four links, `DC · real` and `AC · phasor` on the Numerical
Solver's own ribbon. Sky at 55% so it sits under the labels it separates.

### The Clear button abbreviates, and that is what made room

The measurement that decided it. At 375px the usable row is **335px**,
and with the full language name it was **completely full — zero slack**.
Two letters gave 44px back, but not evenly: English, Spanish, Esperanto
and the three CJK languages had 44px, while **French, German and
Portuguese had none** — *Eingaben löschen* is half again the width of
*Clear inputs* and ate the entire saving.

So the button regained the `.subbar-lbl` / `.subbar-lbl-short` pair that
banner.css already switches at 480px (#144), and three of the wide forms
were shortened as well:

| | wide (>480px) | narrow (≤480px) |
|---|---|---|
| en | Clear inputs | Clear |
| es | Limpiar entradas | Limpiar |
| eo | Vakigi enigojn | Vakigi |
| fr | Tout effacer *(was "Effacer les entrées")* | Effacer |
| de | Alles leeren *(was "Eingaben löschen")* | Leeren |
| pt | Limpar tudo *(was "Limpar entradas")* | Limpar |
| zh | 清空输入 | 清空 |
| ja | 入力を消去 | 消去 |
| ko | 입력 비우기 | 비우기 |

Two wording notes. German moved from *löschen* to *leeren*: the button
empties fields, it does not delete data, and *löschen* was the wrong
promise as well as the wider word. Spanish is **Limpiar**, not *Borrar*,
at Roberto's instruction — same distinction — and the confirm dialog and
the tooltip that name the same action moved with it, since a button
saying *Limpiar* that raises a dialog saying *¿Borrar…?* is two verbs for
one act.

### It deleted more code than it added

`ribbonRows()`, `ribbonCrowded()`, `setLangOptionText()` and the resize
listener are gone — about 45 lines, in both templates. All of it existed
only because the closed control showed the full name and had to be
measured and shrunk when the ribbon got crowded. With the face always two
letters there is nothing to measure, and the Clear button abbreviates
through a rule banner.css already had. The pixels were the ask; the
simplification was the return.

### Verified

* **One row, and the Tutorial link unclipped, in all nine languages** at
  375px, 481px, 520px and 1100px. The 481–520 band was the one to watch —
  full two-word labels at the smallest viewport that shows them — and
  Spanish's *Limpiar entradas* is the widest thing in it.
* Answers **byte-identical** across English, Korean and Esperanto,
  switched through the real menu; `<html lang>` follows; the choice
  persists in `localStorage`.
* Esperanto third in the list, native names throughout.
* Both pages render through Flask; no console errors on either; the
  offline build regenerates clean with no dead references.

### A correction worth keeping

Roberto read a 375px panel of the mockup as *dropping the Tutorial link
to hold one line*, and praised the call. It was the opposite: banner.css
caps `<nav>` at one line-box and **clips** what overflows, so a crowded
ribbon does not grow — it takes the Tutorial link off the screen without
a trace. That is the failure this whole item exists to prevent, and the
static mockups showed it because they carry none of the page's logic. If
a future reader sees the link missing at a narrow width, that is a bug,
not a design.

---

## #202 — Indonesian, the tenth language — **done, cache v104**

Roberto, 31 Aug 2026, after asking which languages lead the world by
total speakers and what each would cost: *"Proceed as you advise."* The
advice was Indonesian first, and this is it.

**Why it was first, of the five candidates.** It is the cheapest — Latin
script, left to right, no font question at all, no new machinery — and it
is the one whose readers most plausibly need it. Indonesian engineering
*is* taught in Indonesian, with settled vocabulary of its own: *tegangan*,
*arus*, *daya*, *kapasitor*, *induktor*, *dua-port*. That is not true of
every large language on the list, and it is the argument that ranked
Indonesian above three languages with more speakers.

485 keys, ~5,100 English words, one new `i18n/id.json` and one line in
`LANGS` in each template and in `tools/i18n.py`. No machinery changed:
this is exactly what #197's scheme was built to make routine, and it was.

### Choices a native speaker should check

* **berkas**, not *file*, for the input file — the formal Indonesian term,
  as GNOME and other localisations use. If Roberto or a reader prefers
  *file*, it is a find-and-replace in one file.
* **Bersihkan masukan** / **Bersihkan** for Clear, following the #201
  pair. At 123px the wide form is now the **widest of the ten** — Spanish
  is 105px — so it is the label to watch if the ribbon ever tightens
  again. Measured at 481px, the narrowest width that shows wide labels:
  one row, nav unclipped.
* **Perkakas** for Tools, **Pemecah numerik** for the Numerical Solver,
  **Mode Pakar** for Expert Mode, **simpul** for node.
* Headings are `[ M A S U K A N ]`, `[ K E L U A R A N ]`,
  `[ P E R K A K A S ]`.

### Verified

One row and the Tutorial link unclipped in **all ten** at 375px and
481px; a real solve in Indonesian returning mathematics byte-identical to
English; `<html lang="id">`; the face reading **ID**; no console errors;
`i18n.py check` clean, including the structural comparison of ids, links
and slots against the English.

Bahasa Indonesia is a long name for a menu, and it costs nothing: since
#201 the closed control shows two letters, so the list can carry names of
any length.

---

## #203 — Hindi and Bengali — **done, cache v105**

Roberto, 31 Aug 2026: *"#203 I follow your advise."* The advice was
option (2) of the three below — translate the chrome and the prose, leave
the terms of art recognisable — so that question is settled and the item
is built.

**What (2) turned out to mean in practice.** Not Latin script dropped
into Devanagari mid-sentence, which reads as broken typesetting rather
than as a technical term. It means **transliterating the term of art into
the reader's own script**: रेज़िस्टर, not प्रतिरोधक; ক্যাপাসিটর, not
ধারক. The reader meets the word they learned in English, and the sentence
still reads as Hindi or Bengali. The rule applied throughout:

* **components and circuit-theory terms are transliterated** — रेज़िस्टर
  / রেজিস্টর, कैपेसिटर / ক্যাপাসিটর, इंडक्टर / ইন্ডাক্টর, इम्पीडेंस /
  ইম্পিড্যান্স, टू-पोर्ट / টু-পোর্ট, ऑप-ऐम्प / অপ-অ্যাম্প;
* **ordinary physics quantities keep their standard native word**, because
  every reader met those at school — वोल्टेज, धारा, शक्ति, प्रतिरोध;
  ভোল্টেজ, কারেন্ট, পাওয়ার, রোধ.

That split is the whole of the judgement, and it is the thing a native
speaker should check first.

### Digits are Western in both

Bengali was drafted with Bengali-script digits (নোড ১, ৫ অঙ্ক) and then
converted: **58 of them, all to ASCII.** Hindi never had any. The reason
is not typographic. `নোড ১` is a label for a node the reader *types* as
`1`, and the rounding menu's `৫ অঙ্ক` names a digit count the app prints
in Western figures — a label that disagrees with its own field is worse
than a label in the wrong script. It also keeps the standing rule intact:
the mathematics is never localised, and these labels are part of it.

### The failure this found, which was real

**Ukrainian lost the Tutorial link at 481px**, and would have shipped that
way. `banner.css` caps `<nav>` at one line-box with `overflow: clip`, so a
crowded ribbon does not grow or scroll — the overflow is simply gone.
*Локальний застосунок* measures **149px** against English's 62px, which
pushed *Підручник* onto a second line that was then clipped away.

**And the check that was supposed to catch it did not**, because it tested
the wrong axis: it asked whether the Tutorial link's right edge had passed
the nav's right edge. A wrapped element is not to the right, it is
*below*. The test now compares each child's bottom against
`nav.clientHeight` and reads `scrollHeight - clientHeight`, which is what
the failure actually looks like. The old test would have passed a clipped
ribbon in any of the thirteen languages; it is worth assuming it did not
catch things in #197 and #201 either, and the widths were re-swept for all
thirteen on that basis.

The fix was the wording, not the CSS: **Локальна версія** (124px) for the
wide form, **Застосунок** for the narrow one.

### Verified

Thirteen languages at **375, 481, 520, 768 and 1100px**: one row, nothing
clipped horizontally or vertically, in every one. The mathematics compared
as the *glyph sequence MathJax actually draws*, not as text near it —
identical in English, Hindi, Bengali, Ukrainian and Spanish, on the server
build and again on the offline build. Both pages render through Flask;
every inline script re-parses; `i18n.py check` clean, including the
structural comparison of ids, links and `%{slots}` against the English.

---

## #204 — the dictionaries are files, fetched on demand — **done, cache v106**

Roberto, 31 Aug 2026: *"Let's split the dictionary out of the page (#204)
and have the app download it the moment the user tries to use a
non-default language."*

**The page went from 941,815 to 271,905 bytes** — 670 KB out of every
load, for every reader, in every language. That is more than the ~505 KB
this item estimated when it was only a payload argument; the estimate
counted the JSON and not what escaping it into a script had cost.

The ZIP barely moved: 17,814,560 → 17,833,540 bytes, **+19 KB**. The
dictionaries left the page and became twelve files inside the same
archive, so the download is the same size and the app is lighter.

### One file per language, whole

Not per-page subsets, which is what the inlined version did. Two reasons:
the file is then byte-identical to what a translator would be handed
(#207), and the Numerical Solver's saving — it uses about sixty of the
keys — is not worth a second set of files to keep in step. The Solver
fetches ~50 KB it mostly does not need, once, from cache thereafter.

They are **.js, not .json**, because the file is loaded two ways and one
format has to serve both. JSON would mean shipping every dictionary
twice.

### Two load paths, and why they are not the same

**Boot** — a parser-blocking `<script>`, written into the head by the
generated block. This is not a style choice. `applyLang()` runs at boot
*before the page takes any element reference*, because it replaces
`innerHTML` and would otherwise leave those references pointing at
detached nodes. A `fetch` defers it past that line, and the app breaks in
ways that would not show up in a screenshot.

**A language chosen later** — an injected `<script>`, resolved through a
promise, exactly as Roberto asked. Safe here precisely because the
references are long taken by then.

English does neither: it is the page's own markup and is never fetched at
all, so an English reader's boot now makes **zero** i18n requests and is
strictly faster than before this item.

### Failure is English, never a hidden page

A dictionary that 404s resolves to an empty one. The page paints, in
English, and stays usable; `i18n-pending` is lifted either by the apply
or by the 2s failsafe that has guarded it since #197. Tested by hiding
`eo.js` and booting into Esperanto: visible immediately, English, app
working.

That test found a real flaw, now fixed: `<html lang>` went on claiming
`eo` while the text was English, which would put a screen reader in the
wrong voice. `applyLang` now sets the attribute to the language it could
actually apply.

### Where the files live

`i18n/dist/<lang>.js`, generated by `python tools/i18n.py pack` from the
`.json` sources — never edited by hand. The server serves them at
`/i18n/<lang>.js` from a route with a year-long immutable cache; the
offline builds carry them beside the page. The URL is root-absolute on
the server (the app is at `/`, the Solver at `/eqsheet/`, so a relative
path would resolve differently on the two) and rewritten to relative by
`build_local.py`, where there is one page at the root of its folder.

The `?v=` on the URL is a hash of every dictionary, so it changes exactly
when a translation does. It does nothing offline — the service worker
matches with `ignoreSearch: true` — where `CACHE_VERSION` governs as it
does for everything else.

### The service worker had to be taught about them

`sw.js` gained a generated `BEGIN/END i18n` block beside the examples
one, written by `build_local.py`. A dictionary that ships but is never
precached is a dictionary that vanishes offline, which would silently
drop a Ukrainian reader back to English the first time they opened the
app without a network. `build_local.py --check` now fails on a stale or
missing one, and `sw_i18n_lines()` refuses to build at all if the `dist`
folder is empty rather than quietly shipping an English-only app.

### Verified

Server build: English boots with **zero** i18n requests; Hindi boots with
exactly one and the page is Hindi before first paint; three switches
fetch two files and returning to the first refetches nothing; `/eqsheet/`
correctly resolves the root-absolute path; `/i18n/xx.js`, `/i18n/zzz.js`
and `/i18n/en.js` all 404. Offline build: relative base, all **twelve**
precached under `symbulator-v106`, a versioned request for a
never-loaded language served from cache, a runtime switch to Korean
working from the cache, and a real Pyodide solve byte-identical to
English. Every inline script re-parses on both pages; `i18n.py check` and
`build_local.py --check` clean; `build_zip.py`'s cache-list check passes
with 63 files.

**A note for whoever tests this next.** The first offline run appeared to
work and did not: the service worker served the *previous* build from
cache `symbulator-v105`, so the page was Bengali with no i18n request and
none of the new globals. That combination — translated, but with nothing
loaded — is the signature. Unregister the worker and delete the caches
before believing anything the offline build tells you.

### What this leaves for #207

Most of it. The dictionaries are now files a translator can be pointed
at. What is still missing is `en.json` among the served files, since the
`js.*` English lives as literal fallbacks in `t()` calls and cannot be
harvested in the browser.

---

## #205 — Arabic and Urdu, and the first right-to-left pass — **deferred
at Roberto's instruction, 31 Aug 2026**

Roberto, 31 Aug 2026: *"Let's leave the right to left languages out for
now."* Not descoped and not rejected — **deferred**, with the measurement
below kept intact so that whoever picks it up does not have to re-derive
it. Nothing else waits on this.

Not another dictionary: the first RTL layout the app has ever had. What
the measurement found:

* **22 physical-direction CSS declarations** to convert to logical ones —
  16 in `templates/index.html`, 4 in `eqsheet.html`, 2 in `banner.css`.
  All mechanical (`margin-left` → `margin-inline-start`, `border-left` →
  `border-inline-start`, `text-align: left` → `start`); the stylesheets
  are already part-way there.
* **`dir="rtl"`** in `applyLang`, beside the `lang` it already sets.
* **Pinning the mathematics to LTR** — the real work. 37 places render
  answers, the LCD panels, MathJax output and the circuit textarea, and
  every one must stay left-to-right inside a right-to-left page. So must
  every `<code>` inside translated prose, or bidi reordering visually
  scrambles `4.7'k` and flips parentheses.
* **The digits stay Western.** `٠١٢٣` would break the rule that the
  mathematics is never localised. Browsers do not substitute by default,
  but it needs a test rather than an assumption.

**And a coordination cost worth knowing before starting:** `banner.css`
is the lockup shared by all five sites, so converting its two physical
rules trips `build_local.py`'s `check_banner()` and `build.py --check`.
An RTL pass therefore turns a two-site deploy into a five-site one, for a
change that alters nothing visible on the landing page or on learn.

**Urdu rides with Arabic and never alone**: same script, same direction,
so it is nearly free afterwards and expensive before. It prefers
Nastaliq, and where Noto Nastaliq Urdu is absent it falls back to Naskh —
legible to an Urdu reader, but wrong-looking.

---

---

## #206 — Ukrainian — **done, cache v105**

Roberto, 31 Aug 2026: *"For political reasons, I'd like to add
Ukrainian."*

**That reason is the entry.** Every language before this one was chosen by
reach — the ranking of world languages by total speakers that produced
Indonesian, Hindi and Bengali. Ukrainian is not on that list and is not
close to it: roughly 40 million speakers, well outside the top ten, and
its readers overwhelmingly have another language they could use. It is
here because Roberto wants it here. **A later session tidying the roster
by speaker count would remove it, and would be wrong to** — this
paragraph exists so that does not happen.

The cheapest language added so far, and the only one needing no vocabulary
judgement at all: Ukrainian has a complete native technical vocabulary
that Ukrainian engineering actually uses, so there was no
translate-or-transliterate question of the kind #203 had to settle.
напруга, струм, потужність, опір, конденсатор, котушка індуктивності,
вузол, коротке замикання, **чотириполюсник** for two-port — the standard
Slavic four-terminal-network term — and холостий хід / коротке замикання
for the open- and short-circuit parameter families.

Cyrillic, left to right, no new machinery, no font question.

**It is also the language that found the clipped-ribbon bug**, because it
is the first one whose *Local App* label was long enough to overflow. See
#203 for that; the fix was the Ukrainian wording, and the corrected test
now guards all thirteen.

---

## #207 — the dictionary as a file a translator can take away — **done, cache v113**

Roberto, 31 Aug 2026: *"Could the dictionary be offered as a downloadable
thing?"* Opened at his instruction as a write-up only; nothing is built.

**Why this is worth doing, stated plainly: no native speaker has reviewed
any of the twelve.** Claude wrote all of them. #203's terminology split —
components transliterated, physics quantities in the native word — was
flagged in that entry as the thing a native speaker should check first,
and there is currently no way for one to. A dictionary someone can take
away, correct and send back is the only route to that correction, and it
is the difference between twelve translations and twelve *reviewed*
translations.

### As built, 31 Aug 2026

**Version (1), and it needed less than the entry expected**, because
#204 had already done half of it: the dictionaries were files by then,
just the packed `.js` form the page loads rather than the JSON a person
edits.

* **`/i18n/<lang>.json`** serves all thirteen source dictionaries.
  `en.json` is among them, for the reason this entry gives: half its keys
  are markup the page could hand back at runtime, but the `js.*` half
  lives as literal fallbacks inside `t()` calls and cannot be harvested
  in a browser at all. A translator needs both halves or the template
  looks broken. Not the same file as `/i18n/<lang>.js`, which is escaped,
  stamped and machine-shaped.
* **`/translate`** explains what to do with them.
* **A Languages section in the About card** links out to it, the same
  outward-link pattern as Acknowledgements.

**Server-only, deliberately.** A translator has to send a file back,
which needs a network anyway, so there is nothing for the offline builds
to carry. 817 KB of source JSON in a 30 MB download whose readers cannot
finish the job would be paying for it twice, and it would put install and
local out of step, which this project does not do. Checked after the
build: no `.json` reached `install_site`.

### The page, and why it is the way it is

**Not translated.** It is addressed to somebody about to translate, who
reads English by definition — and a version in their own language
would be a page written by the very machine whose work they came to
check.

**No dependencies.** No `banner.css`, no i18n runtime, no Pyodide, no
Jinja beyond being rendered. It is the one page that must keep working
while everything else is mid-deploy, and a translator arriving from an
email should not meet a broken layout.

It says four things the checker cannot say for itself:

* **What is machinery, not words** — `%{slot}`, tags, `id=`, `href=`
  — and that a checker refuses a file that has lost one, so a
  translator can be aware rather than careful.
* **What never translates** — the mathematics. Variable names,
  element letters, the decimal point, unit symbols.
* **Roberto's rule for a label carrying a unit**, stated as a rule:
  *translate the word, keep the symbol*. `time (s)` becomes *Zeit (s)*,
  *时间（s）*, *समय (s)*.
* **That the terminology calls are open to being overruled.** #203's
  transliteration split is named on the page as exactly the kind of
  decision a native speaker should reverse. That is the point of the
  whole item: it is the difference between twelve translations and
  twelve *reviewed* ones.

### One decision that was not mine

The first draft put Roberto's personal email on the page as the route
back. It came out again before anything shipped. This page invites
strangers, a published address cannot be unpublished, and whose inbox
takes that traffic is the decision of the person who owns the inbox.

Asked, and answered: **translate@symbulator.com**, a role address on his
own domain. It lives in `templates/translate.html` and nowhere else.
GitHub pull requests are offered beside it for anyone who would rather
work in the open.

### Version (3) is still not built, and its warning still stands

Upload-to-preview — a translator loading their edited file and seeing
their own words in the live app — remains worth doing and remains
unbuilt. **If it is ever built it must escape on load.** Dictionaries are
written into the page as `innerHTML`, and `pack` escapes `<`, `>`, `&`
and `{` at *build* time; a file loaded from a reader's own disk bypasses
that entirely, and the wrapper that would have prevented stored XSS is a
great deal harder to add once the loader exists.

### Three versions, increasing in value

**1. Serve the dictionaries as static files.** `i18n/*.json` stop being
inlined text and become files the page fetches. Every URL is then a
download — `install.symbulator.com/i18n/uk.json` — with no interface at
all. **This is #204 doing double duty:** the payload split and the
download feature are the same piece of work, which is why these two
should be done together rather than in sequence.

**2. A *Help translate* button** that builds a translator's working file
in the browser: one row per key, carrying the English and the current
translation, so a new language starts from a filled-in template instead
of a blank file.

**3. Download *and* upload-to-preview.** The translator loads their
edited file and sees their own words in the live app before sending
anything back. The app already has the upload pattern, for `.cir` files.

**Recommendation: (1) with #204, (3) eventually, skip (2).** Once the
files are served and `en.json` is among them, a button that merely links
to them earns little.

### The English is the one part that is not free

Half of it is already in the page at runtime. `applyLang()` stores every
translated element's original English `innerHTML` in the `i18nBase` map,
keyed beside its `data-i18n` — see `templates/index.html`, `applyLang`.
That is `en.json`'s markup half, available in the browser at no payload
cost and with no drift risk, which is exactly why English is not shipped
as a dictionary in the first place.

**The other half is not reachable that way.** The runtime strings — the
`js.*` keys, a large share of the 485 — live as literal fallback
arguments inside `t('js.solved', 'Solved!')` calls, not in any map. A
purely client-side harvest would hand a translator a half-empty template
and look like a bug.

So **ship the generated `en.json` as one of the static files** in (1).
`i18n.py scan` already produces it; this costs a build step, not a
decision.

### One thing to build in at the start, not retrofit

Dictionaries are written into the page as `innerHTML`, and `pack` escapes
`<`, `>`, `&` and `{` inside every string **at build time**. A dictionary
loaded from a reader's own file at runtime bypasses that entirely. If (3)
is ever built, it must escape on load — otherwise a hostile dictionary
file is stored XSS in the reader's tab, and the wrapper that would have
prevented it is a great deal harder to add once the loader exists.

### What already gates a contribution

`i18n.py check` validates a returned file structurally: stale keys,
orphans, a translation that dropped an `id`, an `href` or a `%{slot}`,
and the `<script>`/`<style>` comparison against the English. So a file
that comes back can be verified before it is trusted, and the reviewer's
job is the words, not the markup.

**Not gated by any of that:** whether the words are *right*. That still
needs a speaker, which is the entire point of the item.

---

## #210 — the offline path gets a harness — **done, cache v112**

Roberto, 31 Aug 2026, after the day's bug: *"Close that gap."*

The gap: `tools/verify_lesson.py` checks that the app's answers still
match the tutorial's printed ones, and it drives `app.py`. **Nothing
drove `bridge.py`**, which is the other half of the same job — the
offline builds call it instead of the Flask routes. On 31 Aug that cost
a shipped bug: four sites in `bridge.py` rendering `[object Object]`
where a definition failed, live on `install.symbulator.com` and in the
ZIP for hours, while every check the project had stayed green. The sweep
could not see it. It exercises the server.

### `repos/local/verify_bridge.py`

Every input through **both** front ends, compared field by field —
`app.py` through the Flask test client, `bridge.py` called directly.

    python3 verify_bridge.py                # every example book
    python3 verify_bridge.py Lesson_03      # one book
    python3 verify_bridge.py --errors       # the refusal paths only

**No Pyodide, and none needed.** `bridge.py` imports `symbulator_ui` and
`circuitbook` and nothing else, so it runs under ordinary CPython. That
is what makes this cheap enough to run often, and it is the code that
actually ships offline rather than a stand-in for it.

Ten refusal cases lead the run, because that is where the two files are
most likely to drift: each writes its own guards, and the 31 Aug bug was
exactly there.

### What "the same" means, and the calibration it needed

`app.py` **lists its response fields by hand**, so it cannot be a byte
comparison. Three rules:

* every field the **server** returns must match the bridge's;
* a field the **bridge** has and the server lacks is a **NOTICE** —
  that is the hand-enumeration trap `CLAUDE.md` warns about, where a key
  added in `symbulator_ui` reaches the offline build automatically and
  is dropped by the server until someone names it;
* a field the server sends as an **empty default** and the bridge omits
  is also a notice, not a failure.

That third rule was learned on the first full run, where it was **201 of
201 findings**. `app.py` emits `eqsheet`, `system` and `solutions` on
every solve, filled with `None` or `[]` when `symbulator_ui` produced
nothing; the bridge has no such key. The page sees `null` on one build
and `undefined` on the other, and every read of the three is guarded —
`(data.solutions || []).length`. Checked, not assumed: the unguarded
`data.solutions.length` reads are in the **solveq** handler, where
`solveq_ui` always supplies the field.

A harness that cries about a known-benign shape is a harness people stop
running, so the reasoning is in the constant beside the rule.

### It found a real one immediately

`app.py` accepts `variables` as a list **or** a comma-separated string.
`bridge.py` accepted only a string, and `str(["v 2"])` is `"['v 2']"`,
which split into `["['v", "2']"]` — so the offline build answered
``Invalid variable name: "['v"`` where the server said
`Invalid variable name: 'v 2'`.

Not reachable from the page, which sends the Variables field's text. But
**the drift is the bug**: these two files exist so that the two front
ends cannot differ, and the next caller to pass a list would have found
it the hard way. Fixed.

### Result

**340 cases — 330 example entries and 10 refusal paths — 0
disagreements, 201 notices**, all of them the one benign shape (67 each
for `eqsheet`, `system`, `solutions`).

### What it still does not cover

The browser around `bridge.py`: the Pyodide boot, the fetch of the `.py`
files, the service worker, the page's own rendering. That needs a real
offline load, which is a different check and is still done by hand. The
docstring says so, so nobody mistakes a green run for more than it is.

---

## #209 — the strings that never reach the dictionary — **done, cache v108**

Roberto asked, 31 Aug 2026, what the app looks like for a reader who
wants it in Chinese. Answering it properly meant running it, and running
it turned up a hole: **the line under every set of answers is English in
all twelve languages.**

    DC analysis · 12 result(s) · 0.06s

`templates/index.html:4435` builds it as a bare template literal. No
`t()`, so no dictionary, so no translation — and it is arguably the
most-read line in the app after the answers themselves.

### Why nothing caught it

`tools/i18n.py check` catches an untagged **markup** unit, a key whose
English no longer hashes to it, an orphan, a translation that dropped an
`id` or a `%{slot}`, and a `t()` call whose key is a variable. Every one
of those is about a string that is *already* in the scheme.

A string that never calls `t()` at all is **invisible to it**. There is
no rule that can see it, because there is nothing to compare. That is
the actual defect; the nineteen strings below are its symptoms.

### The twenty-four

Found by sweeping every literal reaching a reader — assigned to
`.textContent`, `.innerHTML`, `.placeholder`, `.title` or `.value`,
passed to `confirm` / `prompt` / `alert`, or passed to the app's own
`showNote()` — and subtracting everything inside a `t()` / `tv()` /
`tSrv()` call.

It took three passes to get here, and the reason is worth recording. The
first pass wanted two adjacent English words, which walked past
`'solving…'`. The second wanted three-letter words, which walked past
`` `${data.key} vs. ${data.xname}` ``. The third missed `showNote()`
entirely, because it is not a DOM sink — and three of its nineteen call
sites turned out to be untranslated. **Every widening found more.** That
is the argument for the guard, not for a fourth pass.

**`templates/index.html` — sixteen**

| line | string | where a reader meets it |
|---|---|---|
| 3337 | `'reading ' + file.name + '…'` | opening an input file |
| 3826 | `` `Updated '${name}' in ${file}.` `` | after Update entry |
| 3858 | `` `Renamed '${was}' to '${now}'.` `` | after Rename |
| 3867 | `` `Delete '${name}' from ${file}?` `` | a confirm dialog — the **only** one of eleven that skips `t()` |
| 4126 | `'Solution #' + (i+1)` | the multi-solution picker's options |
| 4223 | `'Unknowns: '` | the Equations card |
| 4397 | `'Copy'` | the copy button on the two-port parameter term (#166) |
| 4435 | `` `${DOMAIN} analysis · ${n} result(s) · ${s}s` `` | **after every solve** |
| 4776 | `` `${data.key} vs. ${data.xname}` `` | the sweep chart's title |
| 4779 | `xLabel: 'time (s)'` | the time plot's x-axis |
| 4789 | `` `${toolLabel} · ${n} point(s) · ${s}s` `` | after every plot |
| 4791 | `'Plotted!'` | the Plot button's own status |
| 4993 | `` `solution ${i} of ${n}` `` | the caption above each solution |
| 5208, 5229 | `'drawing…'`, `'Drawn.'` | the Schematic button's own status |
| 5223 | `'Could not draw it.'` | when the drawing fails |

**`templates/eqsheet.html` — eight, of which three are #198's**

| line | string | |
|---|---|---|
| 1192 | `` `line ${e.line}: ${e.error}` `` | the `line N:` prefix is #209's; `e.error` is the engine's |
| 1301 | `'solving…'` | #209 |
| 1305 | `` ` (least-squares: ${n} equations, ${m} unknowns)` `` | **#198** |
| 1306 | `' (restricted)'` | **#198** |
| 1307 | `` ` — ${d.nfev} evaluations` `` | **#198** |
| 1450 | `'system file: '` | #209 |
| 1503, 1504 | `'import: '`, `'import link: '` | #209 |

So **twenty-one for #209**, three already spoken for.

**The shape of the mistake is visible in the button statuses.** #125
gave Solve, Plot and Schematic each its own status. #197 translated
**all three of Solve's** and none of the other two's, because it was
working from the markup and these live in script. Same feature, same
day, three buttons, one done.

Roberto asked on 31 Aug whether *Solving* and *Solved* would be
translated. Most of that family already is — measured, not assumed:

| | at rest | while busy | when done | on failure |
|---|---|---|---|---|
| **Solve** (app) | ✅ `run-symbulator.e67f` 运行 Symbulator | ✅ `js.busy.solving` 正在求解… | ✅ `js.solved` 已求解！ | ✅ `js.res.noVars` etc. |
| **Plot** (app) | ✅ `run.b1b3` (markup) | — no busy label | ❌ `'Plotted!'` | ✅ via `t()` |
| **Schematic** (app) | ✅ `draw-the-circuit-above.4fac` | ❌ `'drawing…'` | ❌ `'Drawn.'` | ❌ `'Could not draw it.'` |
| **Solver** (eqsheet) | — | ❌ `'solving…'` | **#198** — `d.message` is the engine's | **#198** |

So: the app's *Solving…* and *Solved!* have been translated since #197
and were on screen in Chinese during the 31 Aug walkthrough (已求解！).
What #209 adds is their four missing counterparts on the Plot and
Schematic buttons, plus the Solver's `solving…`. The Solver's *solved*
and *did not converge* stay English until **#198**, because they are the
engine's words, not the page's.

### Two questions asked, both already answered in the tree

Both were raised for Roberto on 31 Aug and both were withdrawn the same
day, because the answers were already written down. Recorded because a
question that looks open and is not costs somebody a reply.

**`time (s)` — Roberto's ruling, 31 Aug 2026:**

> That should be translated. Use the corresponding word for "time" in the
> target language and the unit of measure (s) which stands for second.

So: the **word** translates, the **symbol** does not. Which is what
eleven of the twelve dictionaries already do — see the Ukrainian note
below for the twelfth.

It was never really a judgement call to begin with. It sits in a
four-branch `if/else` where every sibling is already decided, twelve
lines of code:

```js
xLabel: t('js.plot.freqAxis', 'frequency (Hz, log scale)'),   // Bode x
yLabel: 'dB',                                                 // bare unit
yLabel: t('js.plot.degrees', 'degrees'),                      // Bode phase y
xLabel: data.xname,  yLabel: data.key,                        // sweep: names
xLabel: 'time (s)',                                           // <- the miss
```

The rule is already applied and already shipped: a **unit symbol alone**
stays (`dB`), and a **label containing one** goes to the translator
whole, who decides per language. They have — Chinese kept the Latin
symbol and used full-width brackets, 频率（Hz，对数刻度）; Ukrainian
localised it, Частота (Гц, логарифмічна шкала).

And the same phrase is *already translated on the same card*: the End
time field above the plot is `end-time-s.801d`, zh 终止时间（s）, de
Endzeit (s). The form says it in Chinese and the axis below says it in
English.

#### The Ukrainian consequence, which needs Roberto's nod

Measured across all twelve dictionaries, on the three shipped strings
that carry a unit symbol (`end-time-s.801d`, `js.plot.endFreq`,
`js.plot.freqAxis`):

**Eleven of twelve keep the Latin symbol** — `(s)`, `(Hz)` — including
Hindi and Bengali, which set every word in their own script and still
write `s` and `Hz`. That is Roberto's rule, already in force, without
anyone having stated it before now.

**Ukrainian is the exception**, and consistently so: `Кінцевий час (с)`
with a Cyrillic *es*, `Кінцева частота (Гц)`, `Частота (Гц,
логарифмічна шкала)`. That is ordinary Ukrainian practice and not a
mistake — but it is not the rule just given.

**And the app cannot follow Ukrainian all the way.** The unit symbols in
the *answers* are not in the dictionary and cannot be: they come from
`symbulator_ui._UNIT_SUFFIXES` — `VA, ohm, Ω, Hz, V, A, W, S, F, H` —
under the rule that the mathematics is never translated. Measured live
on 31 Aug: a Ukrainian reader solving a divider gets `Vin = 12 V`,
`R1 = 2 kΩ`, `r_e1 = 3000 Ω`. So Ukrainian already shows Latin unit
symbols on every screen that has an answer on it, and the Cyrillic
`(Гц)` in the chrome contradicts the `Ω` two inches above it. That is
not a style preference; it is the one language where the app disagrees
with itself today.

There are only two coherent endings, because the worst outcome is
Ukrainian disagreeing **with itself** — the form reading `час (с)` and
the axis beneath it `час (s)`:

* **(a) Apply the ruling everywhere.** The new string is `час (s)`, and
  the three shipped Ukrainian strings change from `(с)`/`(Гц)` to
  `(s)`/`(Hz)`. Consistent with the other eleven and with the ruling.
  Three values, one line each. **Recommended — and chosen by Roberto,
  31 Aug 2026.**
* **(b) Let Ukrainian keep its own convention.** The new string is
  `час (с)`, nothing shipped changes, and Ukrainian is deliberately
  the one language that localises unit symbols — written down here so a
  later tidy-up does not "fix" it, exactly as #206 had to be protected
  from a tidy-up by speaker count.

Either is defensible; **(a)** is what the ruling says and what the
other eleven do. It meant editing translations that are already live,
which is why it was put to Roberto rather than assumed. He chose (a).

**The Solver's status line is #198's, and #198 already says so.** Its
entry carries a section headed *Known, and resolved by #198* naming
these exact fragments, and the reasoning: translating them alone leaves
a half-English line, because `d.message` is English from the engine
regardless. Once the message is a code the whole line renders in one
`tv()` call. So #209 does not touch 1305–1307, and the ordering already
in the file stands.

### The part that outlives the twenty-four

A scanner, in `tools/i18n.py check`: every literal reaching a reader-
facing sink, minus everything inside a `t()`-family call, minus an
explicit allowlist of the deliberate exceptions (mode values compared
against, CSS, selectors, filenames, the mathematics). It is about forty
lines and it is the only thing here that stops the class coming back —
the twenty-one are a day's work, the guard is why there is not a
twenty-fifth next month.

Seed the allowlist from the triage, and keep it **explicit**: an
exception that has to be written down is an exception somebody has
looked at.

### What it came to

**Twenty-four strings wrapped, twenty-two new keys, twelve languages.**
Two of the twenty-four reuse a key the app already had: `js.copy`, and
`js.busy.solvingLower` — the Solver page had been showing `solving…` in
English beside an app that had translated that exact word twelve times.
`en.json` went 485 → 507.

Two of them were found **by the guard, on its first run**, after the
three manual sweeps had finished: `$('evalConds').placeholder` and
`$('solveqEqs').placeholder`, both sitting directly under
`$('evalExpr').placeholder = t('js.eval.hint', …)`. Same function, same
six lines, one wrapped and two not — the button-status mistake again, in
a second place, and neither eye nor regex had caught it.

One more was found by **reading the page in Chinese** after the guard
was green: `throw new Error('missing "equations" list')`, which the
reader meets two functions away as the tail of an already-translated
prefix — 方程组文件：missing "equations" list. See the blind spot below.

**A collision worth recording.** `js.draw.fail` already existed, with
*"Could not draw that circuit."*, on the error panel. The status line
beside the button wanted *"Could not draw it."* — a second English under
one key, which is precisely what `check` catches and what it caught. The
short one became `js.draw.failShort`. Two messages that differ only in
length still differ.

### The guard, and what it cannot see

`untranslated()` in `tools/i18n.py`, wired into `check`. Every literal
reaching a reader — `.textContent`, `.innerHTML`, `.placeholder`,
`.title`, `.alt`, `.value`, `confirm`, `alert`, `prompt`, and the app's
own `showNote()` — minus everything inside a `t()`/`tv()`/`tSrv()` call,
minus an explicit `NOT_FOR_READERS` allowlist.

The allowlist is **short and reasoned on purpose**: state values compared
against, the mathematics, markup fragments, and the three Solver status
fragments that belong to **#198**, which carry a comment saying to delete
them when #198 lands.

**Its blind spot, stated so nobody assumes otherwise: it watches sinks,
not values that travel to a sink.** A string thrown as an exception and
displayed by a `catch` three functions away is invisible to it — which is
how `missing "equations" list` survived a green run. Widening it to
follow `throw new Error(...)` was considered and not done: nearly
everything arriving that way is the browser's own English (`atob`,
`JSON.parse`), which is not ours to translate, and a guard that cries
about strings nobody can fix is a guard people switch off.

### Verified in Chinese, offline, on the shipped build

* the line that started it: **DC 分析 · 12 个结果 · 0.09 s**
* the time plot: x-axis **时间（s）** — Roberto's ruling exactly, the word
  translated and the unit symbol kept — with **时域图 · 300 个点 · 1.54 s**
  under it and **已绘图！** beside the button
* the Schematic button: **已绘制。**
* the Solver: **正在求解…**, **第 1 行：…**, and a dropped bad file giving
  **方程组文件：缺少 "equations" 列表**
* the two placeholders: **例如 t = to**, **例如 p_r2 = 0.05**
* mathematics unmoved throughout — `v_2`, `12 V`, `2 kΩ`
* zero off-origin requests

The one line still half-English is the Solver's `solved — 13
evaluations`, which is #198's by design and by its own entry.

### Ukrainian

Ruling (a) applied: `Кінцевий час (s)`, `Кінцева частота (Hz)`,
`Частота (Hz, логарифмічна шкала)`, and the new `час (s)`. Ukrainian no
longer contradicts the `Ω` and `V` that the answers print beside it.

---

## #208 — the Numerical Solver in the offline builds — **done, cache v107**

Roberto, 31 Aug 2026: *"EqSheet is supposed to be also in the local
versions. Can you fix that? The Numerical Solver (EqSheet) should be
available in the locals, with the packages needed for it to run."*

It is. `eqsheet.html` now ships beside `index.html` in both offline
builds, boots its own Pyodide with SciPy on board, and solves with no
network at all — verified with the static server stopped.

### The number, and where the distribution actually came from

**scipy's Pyodide wheel is 14,029,768 bytes (13.4 MiB)**, and the ZIP
went from 17,833,540 to **31,682,389 bytes (30.2 MiB)**. Roberto was
given the figure before anything was bundled and chose to bundle it:
*"with the packages needed for it to run"* was never going to be served
by a lazy CDN fetch, which would break the no-internet promise for the
one feature that most needs it.

The entry that stood here said the wheel could not be found, that every
probe of `cdn.jsdelivr.net/pyodide/v0.28…v0.31/full/` returned 404, and
that the provenance of `vendor/` was unrecorded and unrecoverable.

**It was recoverable, and the answer was inside `vendor/` the whole
time.** `pyodide.js` carries its own version string, `var ee="314.0.5"`:
Pyodide now tracks the CPython it ships (3.14) instead of counting up
from 0.x, so the version scheme had changed underneath, not the URL.
`https://cdn.jsdelivr.net/pyodide/v314.0.5/full/` serves every filename
in `vendor/pyodide-lock.json`, and the scipy wheel fetched from it
hash-matches the lockfile exactly. So do the sympy, mpmath and numpy
wheels already on disk — checked, so the whole folder's provenance is
now established rather than assumed.

**`vendor_pyodide.py` is the answer written down where it can be
re-run.** It fetches what is missing and hash-checks everything against
the lockfile; `--check` verifies without downloading. #208 was the
second time somebody needed this and the first time anyone recorded it.
It is a dev script and is excluded from the ZIP.

### What the port is

* **`eqsheet.py` no longer imports Flask.** It was a Blueprint; the two
  entry points are now `api_parse(data)` and `api_solve(data)`, plain
  dict in, plain dict out. `eqsheet_web.py` is the Blueprint the server
  mounts (three routes, no opinions), and `app.py` imports from there.
  The module joined `SHARED` in `build_local.py`, so it is copied into
  the offline build verbatim, exactly like `symbulator_ui.py`.
* **`eqbridge.py`** is the offline glue, deliberately separate from
  `bridge.py`: that one imports `symbulator_ui` at module level and
  pulls the whole solver in with it. Apart, the Solver page never
  fetches the symbulator wheel and the app page never fetches SciPy,
  and the shared service-worker cache means a reader who opens both
  downloads each file once.
* **`build_local.py` generates `eqsheet.html`** the way it generates
  `index.html`. It is a much smaller job: everything the Solver asks the
  server is `post('api/parse')` and `post('api/solve')`, so replacing
  the body of `post()` ports the entire page and every call site is left
  as the server's. The page sits at the **root** as `eqsheet.html`, not
  in an `eqsheet/` folder, so #204's `i18n/` base rewrite is the same
  string for both pages.
* **The Google Fonts pair is stripped** from the offline page. A
  downloaded copy has no network to fetch IBM Plex from, and a
  stylesheet link that cannot resolve is a render-blocking wait for a
  timeout before the fallback stack takes over — which is where the page
  lands either way. Measured after the port: the offline Solver makes
  **zero off-origin requests**.
* **The handover is re-pointed.** `EQSHEET_URL` is
  `'eqsheet.html'` in the offline build. The `?import=` payload, the
  6 KB URL ceiling and the `numerical_system.json` drop-file fallback
  all work unchanged — all three were exercised offline.
* **`sw.js` is at v107** and caches `eqsheet.html`, `eqsheet.py`,
  `eqbridge.py` and the scipy wheel. `build_zip.py` now checks both
  pages' heads (`src` as well as `href`) and checks those three by name,
  since none of them is reachable from any tag.

### It found a bug, and the bug was the server's

A NaN residual travelled as a bare `NaN`, which `json.dumps` writes
happily and **no JSON parser accepts**. Give the Solver every variable
Unknown at a guess of zero — which is exactly what a fresh sheet starts
with — and a divider equation evaluates 0/0 at the start point. The
reply could not be read at all: the page sat on *solving…* for ever,
with a `SyntaxError` in the console and nothing on screen.

**This was live on `symbulator.pythonanywhere.com`, and had been since
the Solver shipped.** The port only made it impossible to miss, because
the offline page fails in the same tab you are looking at.
`eqsheet.py` now sends `null` for any non-finite residual or answer (a
phasor all-or-nothing, since "3 + j —" is not a partial answer), and the
page draws an em dash. A failed solve is a normal thing to say; saying
it in unparseable JSON is not.

### Verified, not assumed

* **24 payloads through both engines, 0 differing** — exact, bounded,
  range-bounded, least-squares, AC complex, AC real-only, a Python
  keyword as a variable name, the unit step, the non-converging case and
  both error paths. Recorded from the live Flask routes, then replayed
  through `eqbridge` in the tab and compared field by field.
* **With the server stopped**: boot, parse, solve, `Vout = 4 V`.
* **The handover**, offline: a 2k/1k divider solved in the app, its
  system carried across in the link, `v1` flipped to Known and set to
  24 V, and the sheet followed to `v2 = 8 V`, 8 mA.
* **The drop-file fallback**, offline.
* **Ukrainian**, offline, from the cache: the whole page translated, the
  boot bar with it (`syncBootBar()` is hooked into the language-change
  handler), and the mathematics byte-identical to English.
* Both server pages re-rendered through Jinja after every template
  change, and `tools/i18n.py check: ok`.

### The published size string — one, not three

The brief said three strings say "about 17 MB". Measured: **one**, and
it is narrower than that even sounds. It is in the app's *Installing
from a file* card, which sits inside a **`server-only` block** — so it
is on `symbulator.pythonanywhere.com` and on **neither offline build**,
which strip it. That is right, and it is the point of the card: it
tells a reader of the hosted app how big the download would be, and
someone already running the download does not need telling. The
landing page and `README.txt` state no size at all.

It now reads **about 30 MB** — the same MiB convention the old number
used, and what a browser's download dialog will show. Verified live on
the server after the pull; the two offline builds correctly do not
carry the sentence.

Changing that English mints a new content-hash key, so the twelve
translations were **migrated in place** rather than orphaned:
`works-on-windows-macos.f74e` → `.b9b9`, with `17` → `30` inside each
value. Every language writes the number in Western digits (Bengali's
were converted in #203), so nothing else moved. One line changed per
dictionary.

---

## #198–#200 — the engine speaks in codes, the interface in words
## — **all three done: #198 (v109), #200 (v110), #199 (v114)**

Roberto's ruling, 31 Aug 2026, replacing the proposal that stood here
overnight. I had recommended translating `symbulator_ui.py` and
`eqsheet.py` and leaving the solver package alone. He asked for the
opposite and for something better:

> Let's standardise the error format. Let's modify the package this one
> time, so that all messages, warnings, errors, etc, are returned in a
> structured manner, with a message code and arguments. When I think
> about the package, I do not worry about readability by humans. I do not
> expect any human to use the package directly. The package is meant to
> be under the hood. So, create a running list of all the messages shared
> by the package, give each a number and a format for it to pass the
> arguments (variables, numbers) needed to communicate this message to
> the human, and let the interface do the work of putting the message
> into words.

He is right, and for a reason beyond translation: it gives the package,
`symbulator_ui.py` and `eqsheet.py` **one** mechanism where they have
three, and the app **one** renderer where it would have had three.

**And the pattern is already in the tree.** `eqsheet.py` does exactly
this for its success line: Python returns `mode`, `n_eq`, `n_un` and
`nfev` as fields, and `templates/eqsheet.html` composes "solved
(least-squares: 1 equations, 4 unknowns) — 29 evaluations" from them.
Only its *failures* come back as prose. This is finishing a job somebody
already started at the one place they needed it.

### The measured inventory

| emitter | messages | carry a value | ships how |
|---|---|---|---|
| solver package `CircuitError` | 27 distinct, 33 raise sites (elements 19, engine 8, equiv 2, laplace 2, spice 2) | 22 | PyPI release |
| solver package SPICE warnings | 17 sites — `spice()` returns `(netlist, warnings)` | most | same release |
| `symbulator_ui.py` notes and errors | ~40 (35 `_err`, 4 note sites) | most | copied file, no release |
| `eqsheet.py` | 12, plus the composed status line | 4 | server only |

About 85 messages end to end. The SPICE warnings are the surface the
first write-up missed, and they are the clearest case for the change:
they are already prose assembled in the engine purely for the interface
to display.

**A risk that turned out not to exist:** no tutorial chapter quotes a
solver message. Checked across `Documentation/src`. So the
English wording is not pinned by the printed answers and may be reworded
as well as restructured — unlike every answer in the app.

### The shape

```python
# symbulator/messages.py -- the one place the package's words live.
E_TWOPORT_LIST_LEN = 214

CATALOGUE = {
    214: ("error",
          "The parameter list of two-port '{name}' has {n} entries. "
          "Exactly four are expected: [p11,p12,p21,p22]."),
}
```

```python
raise CircuitError(E_TWOPORT_LIST_LEN, name=el.name, n=len(items))
```

A named constant at the raise site so the code still reads; the **number**
on the wire. `exc.code`, `exc.args_map` and `str(exc)` all available.
Warnings become `{"code": …, "args": {…}}` in the list `spice()` already
returns.

**Severity is a field, not a number range**, so a warning and an error
about the same thing need one code, not two.

**Ranges by origin**, matching how the modules already divide:
1xx parsing · 2xx elements · 3xx engine · 4xx Laplace and transient ·
5xx equivalents and two-ports · 6xx SPICE · 8xx `symbulator_ui.py` ·
9xx `eqsheet.py`. One renderer in the page serves all of them.

**A code is permanent once published.** Never reused, never renumbered;
retired codes stay retired. The same rule as the item numbers in this
file, for the same reason: a reader quoting "E214" in a bug report should
mean one thing forever.

### The English stays in the package

Roberto's premise — nobody should need to read the package — stands, and
this does not contradict it. `str(exc)` keeps rendering the English from
the catalogue for three reasons that have nothing to do with reading the
package for pleasure:

1. **It is the generation source.** `tools/i18n.py` generates `en.json`
   from the English in the app rather than letting anyone hand-keep a
   second copy, and `check` fails when the two drift. A catalogue in the
   package generates the same way and gets the same guard. English living
   only in `en.json`, against a numbered list in another repo, is exactly
   the drift the scheme exists to prevent.
2. **15 of the solver's tests assert on message wording** (of 36
   `pytest.raises`, out of 272). They pass untouched. Migrating them to
   assert on `.code` is better testing and worth doing later; it should
   not gate the release.
3. The `.txt` export, `review_schematics.py`, `verify_lesson.py` and a
   traceback in a bug report all need something to write — and the About
   card invites "circuits that break it".

Cost of keeping it: one dict in the package.

### Three items, in this order

Ordered by cost, cheapest first, so the design is proved on the surface
that cannot break anything before it reaches the one that can.

**#198 — `eqsheet.py` speaks in codes (9xx). Done, 31 Aug 2026, cache
v109.** See the section below for what it came to.

> **This paragraph's costing went stale within the day, and the way it
> went stale is the point.** It said: server-only, no wheel, no
> `vendor/` copy, no three pins, no cache bump, no offline build to
> think about. That was true when it was written at 09:25. At 14:08
> **#208 put `eqsheet.py` and `eqsheet.html` into both offline builds**,
> so #198 needed a cache bump and both offline deploys after all. Still
> no wheel and no PyPI release. A cost written down beside an item is
> only true until another item moves under it.

The original estimate follows. Twelve messages and the status line, twelve
languages (the entry said eight when it was written, before #202, #203
and #206 — the count moved under it). This is the end-to-end proof of the whole scheme for the price
of an afternoon, and if the design is wrong we find out here.

**#199 — the solver package speaks in codes (2xx–6xx). Done,
31 Aug 2026, solver 0.5.23, cache v114.** See the section below. The
original plan follows.

The release
train: PyPI publish → the same wheel into `repos/local/vendor/` → three
pins (`build_local.py`'s `WHEEL`, `sw.js`'s cache list,
`requirements.txt`) → cache bump → both offline deploys → the PyAn pull
with `pip install --upgrade`. The interface reads `.code` and falls back
to `str(exc)`, so nothing breaks in the window between the publish and
the pull.

**#200 — `symbulator_ui.py` joins (8xx). Done, 31 Aug 2026, cache
v110.** See the section below. The trap this paragraph predicted was
real and was worse than predicted: see *The field nobody would have
named*.

**Each item carries its own twelve translations**, so none of them can
land half-done and the app is never in a state where a code renders as a
bare number.

### Known, and resolved by #198

The Numerical Solver's status line is assembled in the page from
`d.message` plus English fragments — `(least-squares: N equations, M
unknowns)`, `— N evaluations`. Those fragments are untranslated English
that #197 shipped: the leftovers sweep missed them because the prose is
split across `${}` boundaries, which its two-adjacent-words filter cannot
see. Translating the fragments alone would give a half-English line,
since `d.message` is English from the server regardless. Once the message
is a code, the whole line renders in one `tv()` call and the gap closes
by construction.

### #198, as built

**Seventeen codes, 901–924.** `eqsheet.py` carries a `CATALOGUE` mapping
each to `(severity, English template)`, named constants at the call
sites (`M_UNCLASSIFIED`, `M_SOLVED_LSQ`), and `msg(code, **args)`
returning `{code, args, severity, text}`. The wire keeps **both**: `msg`
for the page and `message` — the rendered English — for a traceback, a
bug report, or a page older than the server.

**The status line is one code now, not four pieces.** It was
`d.message` + `(least-squares: …)` + `(restricted)` + `— N evaluations`,
three of which #209 found untranslated and deliberately left here.
`_status()` picks one of five codes and the page renders it in one
`tv()` call:

| | Chinese, measured |
|---|---|
| 920 | 已求解 — 13 次求值 |
| 921 | 已求解（最小二乘：3 个方程，2 个未知量） — 3 次求值 |
| 922 | 已求解（受限） — 6 次求值 |
| 923 | 未收敛 — 请换一组初值（21 次求值） |
| 924 | *no solution under the restrictions*, same shape |

**The page's table is verbose on purpose.** `EQ_MESSAGES` is seventeen
literal `t()`/`tv()` calls keyed by code, not a lookup built from the
number, because `tools/i18n.py` harvests the English from the call
itself and `check` refuses a variable key. A computed key would have
been shorter and invisible to every guard in the file.

**The deploy window is covered.** `eqMsg()` falls back to the message's
own `text` when it meets a code it does not know — which is what a
server ahead of its page sends. Tested: an unknown code renders the
server's English, a payload with no code at all renders its prose, and
`null` renders nothing rather than throwing.

**SymPy's words stay English, as an argument.** Code 912 is *could not
read that equation: %{error}*, and `%{error}` is the parser's own
sentence. The frame translates and the library's text does not, which is
honest: those words are not ours. Same for 907 and 910.

**#209's three exceptions are deleted.** They were allowlisted in
`NOT_FOR_READERS` with a comment saying to remove them when #198 landed.
It landed; they are gone; the guard now watches that line again.

Verified in Chinese on the offline build: the five status shapes above,
every refusal code with its arguments substituted (未归类的变量：c,
x 的范围为空 — “从”必须小于“到”), and the per-line parse errors, which
used to be raw engine English and now read 第 1 行：每个方程需要且只需要
一个 '='.

**What it proves for #199 and #200.** The shape survived contact: named
constant at the raise site, number on the wire, severity as a field,
English kept in the catalogue as the generation source, arguments by
name. Nothing about it wanted changing. #199 can take the same pattern
into the package with the release train, and #200 into
`symbulator_ui.py`.

### #200, as built

**Fifty-five codes, 801–877**, across six surfaces: the description
and analysis validators (801–810), added equations, conditions,
unknowns and definitions (811–816), plotting (820–824),
Evaluate and conditions (830–833), the schematic drawer
(840–841), the mini-tools (850–854), SPICE (860) and the
**notes** (870–877). Same `CATALOGUE` / `msg(code, **args)` shape
as #198's, deliberately, so the page has one renderer for both engines
rather than two.

**Severity earned its keep here.** #198 had errors and one success line;
this range has eight **notes** sitting in the same catalogue as
thirty-three errors, told apart by a field. Two number ranges would have
meant two of everything.

### The seam that makes a half-done state safe

`_err()` takes a coded message **or** a bare string, and `error` is the
English either way:

```python
if isinstance(message, dict) and "code" in message:
    return {"ok": False, "error": message["text"], "err": message}
return {"ok": False, "error": message}
```

A string is what this file *forwards* rather than writes — a
sentence out of the solver package, which has no codes until #199. So
#199 and #200 could have landed in either order, and an uncoded message
renders its English exactly as it did before. The page's `uiMsg()`
mirrors it: a coded message is looked up, a plain string is its own
answer, and an unknown code falls back to the `text` the engine sent
— which is the deploy window, when the server is ahead of the page.

### The field nobody would have named

`app.py` lists its response fields by hand, and the entry above predicted
that as the trap. It was sharper than that: `_run_in_process` **flattened
the failure to a string** before any route saw it —

```python
return False, result.get("error", "Unknown error.")
```

— so the code was destroyed one function above the six places that
would have had to name it. Naming a field in six routes is a field
forgotten in the seventh. It returns the failure dict now, and one
`_refusal(payload, **extra)` names `err` **once**.

The same shape was needed in `bridge.py` and at five validator call
sites in `app.py`, where `{"ok": False, "error": err}` was built by hand
around what is no longer a string.

### What is deliberately not coded

* **Everything this file forwards from the solver package** —
  `_err(_exc_text(exc))` and friends. Those words are the package's and
  get 1xx–6xx numbers in **#199**. Inventing 8xx numbers for
  sentences about to acquire their own would have been work done twice.
* **`app.py`'s own messages** — about twenty of them. They are
  server-only (the offline build validates in `bridge.py` instead), they
  are not in this item's brief, and one of them is visible in the
  measurements below: a bad SPICE direction is refused by `app.py`
  before `symbulator_ui` sees it, so code 860 never fires on the server.
  Worth an item if anyone wants it; not worth folding in silently.

### The inventory grew four times, and the fourth found the rest

**34, then 5, then 8, then 6 — fifty-five codes in all.** Each pass was
sure it was the last, and each of the first three was wrong:

* **34** from the first hand sweep: `_err()`, the validators, three notes.
* **5** more found by running the app in Chinese and reading what was
  still English — the TR step-source explanations and the "switched
  Rounding to approximate" line, which live in helpers returning lists of
  sentences and are reached by no `_err` and no validator.
* **8** more found by grepping for a shape the sweep had not looked for:
  `return {}, "..."`, a message in the second half of a tuple. All five of
  `parse_defines`' refusals were there, plus the TR "cannot limit the
  results" error and the mini-tools' one-number reader.
* **6** more found by the guard below, after those three had finished:
  two notes that refuse a name outright, the "did you mean" warning, the
  complex-value refusal and the two no-solution notes.

### The guard, which is the part worth keeping

`uncoded_messages()` in `tools/i18n.py`, wired into `check` beside
#209's `untranslated()`. It parses `symbulator_ui.py` and `eqsheet.py`,
finds every string literal that reads like a sentence and is returned or
appended where a message goes, and subtracts everything inside `msg()`,
`_exc_text()` or `tSrv()`.

Two exceptions are allowlisted with reasons: a comment line inside the
SymPy export (a `.py` file the reader opens in an editor — its comments
are code) and the port phrase `tSrv()` handles by regex (#168).

**Three careful hand sweeps missed six messages; the guard found them in
one run.** That is the whole argument for it, and it is #209's argument
about the page in the other language. Grep finds what you thought to look
for.

It also caught something it was not aiming at. `srv_vocabulary()` reads
its tables by finding a name and scanning to the next line beginning
`}`, so the new `_QUANTITY_WORDS` — written with its brace tucked after
the last entry — made it swallow the SI prefix table as engine
vocabulary, and `check` started demanding translations for `k`, `M` and
`p`. The brace sits at column 0 now, with a comment saying why.

### One argument was engine vocabulary, and is now translated

Message 837 says "`%{name}` is its %{what}", where `%{what}` is *voltage*,
*reactive power*, *equivalent impedance* and six others. Those are the
engine's words rather than that sentence's, so leaving them a plain
argument would have put an English noun inside a translated sentence —
which is not the SymPy case, where the words genuinely are not ours.

They are `_QUANTITY_WORDS` now, module-level and listed in `SRV_SOURCES`,
so `check` harvests them like the element kinds and demands their
translations. The page's 837 entry passes that one argument through
`tSrv()` before substituting it.

### Verified in Chinese, offline, on the shipped build

* the line that started it: **DC 分析 · 12 个结果 · 0.09 s**
* the time plot: x-axis **时间（s）** — Roberto's ruling exactly, the word
  translated and the unit symbol kept — with **时域图 · 300 个点 · 1.54 s**
  under it and **已绘图！** beside the button
* the Schematic button: **已绘制。**
* the Solver: **正在求解…**, **第 1 行：…**, and a dropped bad file giving
  **方程组文件：缺少 "equations" 列表**
* the two placeholders: **例如 t = to**, **例如 p_r2 = 0.05**
* mathematics unmoved throughout — `v_2`, `12 V`, `2 kΩ`
* zero off-origin requests

The one line still half-English is the Solver's `solved — 13
evaluations`, which is #198's by design and by its own entry.

### Ukrainian

Ruling (a) applied: `Кінцевий час (s)`, `Кінцева частота (Hz)`,
`Частота (Hz, логарифмічна шкала)`, and the new `час (s)`. Ukrainian no
longer contradicts the `Ω` and `V` that the answers print beside it.

---

### #199, as built

**Thirty-six codes** in a new `symbulator/messages.py`, numbered by the
module that raises them: 2xx `elements`, 3xx `engine`, 4xx `laplace`,
5xx `equiv`, 6xx `spice`. `CircuitError` carries `code`, `args_map` and
`severity`; `str(exc)` renders the English from the catalogue, which is
why the nine tests that assert on wording pass untouched. Solver
**0.5.23**, cache **v114**.

**A plain string still works, and that is not a shim.**
`CircuitError("a sentence")` sets `code` to None and behaves as before.
It is how an exception re-raised from elsewhere keeps flowing through,
and it is what let the package and the app deploy in either order
instead of in lockstep — the same seam `_err()` has on the interface
side.

**Four messages became two codes apiece** rather than one code with a
clause glued on, because the clause is prose a translator has to see
whole: both `_diagnose_unsolvable` diagnoses with and without their
*"and inductors, which are shorts in dc"* / *"and capacitors, which are
open in dc"*, and "could not solve" with and without its extra-equation
hint.

**`laplace._check_transform` takes `fn`, not `origin`.** It used to be
handed a ready-made English phrase — *"between brackets"*, *"as an
argument to t2s()"* — and a phrase cannot be translated from inside
an argument. It takes a function's name now, or None for the `{...}`
shorthand, and the two forms are two codes apiece.

### Two bugs, both found by tooling rather than by reading

**`app.py` flattened the code in its own parse step.** It forwarded the
worker's code correctly, so solve-time errors carried theirs while every
*parse* error — bad name, duplicate, floating node, two-port list
— silently lost it.

**`bridge.py` had the mirror image, and `verify_bridge.py` found it** —
one day after that harness was built for exactly this, reporting
`1 disagreement: [unparseable circuit] .err: only the server has it`.
Two of the day's items paying for each other: **#210** exists because
#200's bug shipped, and it caught #199's before it could.

### Verified

* **311 solver tests pass**, the nine wording assertions among them.
* Every path carries its code end to end — 204, 205, 211, 217, 304,
  309 — with arguments, through both front ends.
* `verify_bridge.py`: **340 cases, 0 disagreements**.
* `i18n check: ok`; thirty-six codes times twelve languages.
* The wheel `install.symbulator.com` serves is byte-identical to PyPI's:
  152,782 b, sha256 `51c1714c...`.
* Offline, in Chinese, with 0.5.23 in the tab: **二端口 'zz1' 的参数列表有
  3 个条目** (211), **节点 2, 3 没有通向参考节点 0 的路径** (217),
  **元件名 'r-x' 含有不能用于名称的字符** (204). The engine's own words,
  in the reader's language, with no server — which is the point of
  the whole batch.

### What is not in it: #211

**`spice.py`'s warnings.** Seventeen `append` sites are not seventeen
messages: seven are `f"{el.name}: {why}"` with `why` built elsewhere,
`skip()` alone has eight call sites with their own reasons, and the
`described` map names eleven element kinds. Thirty-odd more codes.

It is separate for a reason that is not size. **The SPICE translator is
labelled beta in the app**, so its wording is the likeliest prose in the
package to change, and **a code is permanent once published**. Rework
the wording first, then code it.

There is a handoff brief at
`C:\Users\perez\Claude Symbulator\Notes\PROMPT_211_spice_warnings.md`, written
31 Aug 2026 at Roberto's ask: the measured chain from `to_spice()` to
`note(w)` in the page, the four consequences of that shape, the design
these three items proved, and the precondition above stated first.

`si_prefix.py`'s `AmbiguousValueError` and `UnsafeExpressionError` are
their own classes with their own contract, not `CircuitError`. The 1xx
range is held for them.

## #191 — a box for the settings notes — **done, cache v99; PyAn pending**

Roberto, 30 Aug 2026: put the notes about the settings inside a rounded
rectangle with a tag reading **A word about your settings**.

Three treatments were mocked up in both themes against the app's own
tokens — a legend straddling the border, a pill on a tinted panel, and a
header strip. Roberto chose the **legend**, and was right to: I had argued
for the tinted one because it makes a live message land, but the box is
inert most of the time, and a permanent tint gives permanent weight to
something usually saying nothing. That is the same argument that hid the
RMS row rather than greying it (#183's precedent).

What compensates for the missing tint: the dynamic line is set **bold**
inside the box. It already carried `--note-warn`; bold is what makes it
read as an event rather than more explanation. If that turns out not to
catch the eye in use, tinting the box only *while* a message is present is
a two-line change.

**In the box:** `#siNote` (the live message) and `#settingsNote` (the
standing explanation about SI prefixes and exact).

**Not in the box:** the Rounding control's own note. There is a comment
beside it saying a message about one control belongs under that control,
not in a shared box at the foot of the card — a decision already taken,
and folding it in would have undone it. Worth knowing that the SI-versus-
exact conflict raises *either* note depending on which control you touched:
ticking SI writes the Rounding one, choosing exact writes the one in here.

The tag paints `var(--card)` over the border to make its notch, **not a
fixed white** — in dark mode the card is `#1b212c` and a white notch would
be a bright bar across the border. Verified in both themes: the notch
matches the card exactly, the tag takes the accent (#2f5fa8 light,
#5b96e0 dark), and a real message raised through the app's own handler
sits bold and crimson above the standing text.

---

## #189 — the showcase book is renamed — **done, cache v99; PyAn pending**

Roberto, 30 Aug 2026: in **Built-in Examples**, *A sample of what
Symbulator can do* becomes **Claude's sampler for Symbulator 9**.

One line, the `title:` in `examples/Showcase.cir`, which is what the menu
lists the book by. `repos/local/examples/Showcase.cir` is generated from
it by `build_local.py`, so the server copy is the one to edit.

Checked afterwards that the apostrophe rides through `circuitbook.parse_book`
intact and the book still reports its 12 entries.

---

## #190 — the *approx* option names its precision — **done, cache v99; PyAn pending**

The menu's **approx** becomes **approx (full precision)**. Roberto asked
what the option actually does, having guessed "without rounding" or "12
digits"; measured, it is neither. It converts to a decimal and shows the
shortest form that is still exactly the same number at double precision,
so `15/2` prints `7.5` and `1/3` prints `0.3333333333333333`. No fixed
count — the number decides the width, where *approx to n digits* makes the
setting decide.

The write-up with the measurements is in `Documentation`'s `NEXT_DOCS.md`,
since the tutorial line that names the option moved with it.

---

## #184 — the Solve card says it is waiting — **done, cache v99; PyAn pending**

Roberto, 30 Aug 2026: make the fields in the **Solve** card inactive until
a simulation has been run, the way Evaluate's are.

Measured first, and they already were. All five controls carry `disabled`
in the markup, and `clearResults()` and `activatePostSolve()` handle them
in step with Evaluate's. What was missing was the *signal*:

| field | placeholder while disabled |
|---|---|
| `evalExpr`, `evalConds` | *solve a circuit first…* |
| `solveqEqs` | **(empty)** — `clearResults()` blanked it |
| `solveqUnks` | **`x`** — its live hint, never swapped out |
| `solveqConds` | **(empty)** — never had one |

So a card that could not be used read as one that could, and one of its
fields advertised a value you could not type. Evaluate looked right for
one reason only: it says so on both of its fields.

All three now carry Evaluate's wording while they wait, and
`activatePostSolve()` puts the live hints back (`e.g. p_r2 = 0.05`, `x`,
and nothing for Conditions). The text is a single constant,
`WAITING_FOR_SOLVE`, because this item *was* the two cards drifting apart.

Verified in a browser: before a solve, all five controls disabled and all
three fields reading *solve a circuit first…*; after one, the live hints
back.

Not changed, and worth knowing: a disabled field on this page does not
*look* disabled — `opacity: .55; cursor: not-allowed` is scoped to
`#expertBox` alone, so everywhere else a disabled input keeps the same
background and ink as a live one. Widening that rule would grey the Solve
and Evaluate fields, and also `omega`, `vars`, `n1`, `n2` and `kind`
whenever the analysis does not use them. That is a bigger visual change
than was asked for; say if it is wanted.

---

## #185 — the Numerical Solver opens blank — **done, cache v99; PyAn pending**

Roberto, 30 Aug 2026: after **Clear all inputs**, opening the Numerical
Solver still showed a set of equations. Why?

Not a leak from the app. `templates/eqsheet.html` shipped a worked example
hard-coded in its `#rules` textarea — a voltage divider and a thermal
equation — so the page would not be empty for someone arriving at
`/eqsheet/` cold. The app opens it with no payload whenever nothing has
been solved (#136), and that sample was simply sitting there.

It also contradicted the page's own tagline three lines above it: *"Arrives
preloaded with the solved circuit's equation system and results."* What
arrived was a system no Symbulator circuit would ever produce.

Gone. The box is empty, with a placeholder naming the format instead:
*one equation per line, e.g. Vout = Vin \* R2 / (R1 + R2)*.

---

## #186 — Clear all inputs, in the Numerical Solver — **done, cache v99; PyAn pending**

Roberto, same day: the solver should be able to clean its slate in one
click, as the app can.

Same control, same place, same class — `.subbar-action` in the ribbon,
right of the spacer beside the theme toggle, with the two spellings the
shared banner switches between at phone widths. That class was already
styled in `eqsheet.html` and had no button using it.

It empties everything derived from the equations, not just the text: the
parsed rules, which of them are ticked, every variable's Known/Unknown
status and value, the stored solution, the residuals and both status
lines. Done locally rather than by re-parsing an empty box, so it needs no
round trip and works with the server unreachable.

**Deliberately kept:** the DC/AC mode and the rounding menu. Those are
preferences about how the sheet works rather than inputs typed into it,
and the rounding one is remembered in `localStorage` between visits.

Verified: two equations and five variable rows in, one click, everything
back to zero with both tables hidden.

---

## #187 — the SPICE card's buttons, centred — **done, cache v99; PyAn pending**

Roberto, same day: centre the two buttons in the **SPICE Translator**
card, on one line, rather than aligning them left.

`justify-content: center` on that one row, inline, **not** on `.actions` —
four cards share that class and the other three are meant to line up with
the text above them. Confirmed after the change that `inputsCard`,
`miniCard` and `plotCard` still read `normal`.

At 1200px the two sit on one line with 180px clear on each side. The row
keeps `flex-wrap: wrap`, so at phone widths they stack — and each line is
then centred in turn, which is the sensible reading of the request.

---

## #196 — the SI note appears only when SI prefixes are on — **done, cache v101; PyAn pending**

Roberto, 30 Aug 2026: the note reading *"SI prefixes apply to numeric
answers only; a symbolic answer such as `x·vin/(r1 + x)` is left as it is.
A prefixed value is a decimal, so SI prefixes and exact can't both
apply."* is shown even when the SI prefixes box is unchecked, *"which does
not make sense"*.

It doesn't. The line is the standing explanation of what that tick does to
an answer, and `si` is **off by default**, so the commonest state of the
app was a paragraph explaining a setting nobody had asked for.

### It is two changes, not one

Hiding the line alone leaves a bordered box with *A word about your
settings* on its border and nothing inside it — which reads as a bug. So
the box (#191) hides too, whenever both of the lines it can hold are
hidden. It holds exactly two: `#siNote`, the dynamic one, and
`#settingsNote`, the standing one.

The three ways in are covered by one function, because those two lines
move independently:

    function syncSetnote() {
      $('settingsNote').hidden = !$('siUnits').checked;
      $('setnoteBox').hidden = $('settingsNote').hidden && $('siNote').hidden;
    }

called from `syncSettings()` (an entry loading, a rounding change), from
the `siUnits` handler (the tick itself, on **both** branches — the else
branch never called `syncSettings`), and from the tail of
`settingsNote()` (the dynamic line being raised or retired).

### The CSS rule that would have silently defeated it

`hidden` is only a UA-stylesheet `display: none`, and **any** author rule
that sets `display` out-ranks it. The box already had one:

    .setnote .hint:last-child { display: block; }

`#settingsNote` matches that whenever the dynamic line is hidden — which
is nearly always — so marking it `hidden` would have done nothing at all,
and the markup would have looked right while the page ignored it. Fixed
with an equal-specificity rule placed after it:

    .setnote .hint[hidden] { display: none; }

The note also carries `hidden` **in the markup**, not just from script, so
it never flashes on screen before `syncSettings()` runs — with SI off by
default that flash would be the common case.

### Verified

Through the real Flask render, seven states:

| | box | standing line | dynamic line |
|---|---|---|---|
| load, SI off | **hidden** | — | — |
| SI ticked | shown | shown | — |
| SI unticked | **hidden** | — | — |
| exact, SI off | **hidden** | — | — |
| SI on while exact | shown | shown | — (the rounding note lives under Rounding) |
| exact chosen while SI on | shown | — | shown |
| SI back on | shown | shown | — |

Lesson 1's *B11's Example 5.7* (`si: yes`) loads with the box and the
standing line on screen, and loads **clean** — this is display only,
touching no saved value, so no unsaved edit is raised.

Live and hash-verified on install and the ZIP.

---

## #183 — hide the polar phasors tick outside AC — **done, cache v100; PyAn pending**

Roberto, 30 Aug 2026, as a note for the to-do list: **Show AC answers as
polar phasors** should be *hidden* when the analysis is not AC, not merely
disabled as it is now.

This finishes a decision already taken. On 28 Aug 2026 the **AC power
convention** row faced the same question — grey it out, or hide it — and
Roberto chose hiding, on the argument that a permanently greyed control is
clutter that never becomes useful where it sits. `syncSettings()` already
does that for RMS:

    $('rmsRow').style.display = isAc ? '' : 'none';
    $('useRms').disabled = !isAc;

Polar was left on the older treatment three lines below, so the two
settings that are AC-only behave differently on the same card:

    $('polarPhasors').disabled = !isAc;
    $('polarLine').style.opacity = isAc ? '1' : '.5';
    $('polarLine').title = isAc ? '' : 'Applies to AC analysis only';

### What makes this different from the RMS one

**RMS has a row of its own; polar does not.** `#rmsRow` is a whole `.row`
and can be hidden outright. `#polarLine` is one `.checkline` among several
inside the Display block — *Show units*, *Use SI prefixes*, *Show AC
answers as polar phasors*, *Show equations* — so what gets hidden is that
one label, and the remaining ticks have to close up cleanly behind it.
Worth a look at the card at phone width as well as desktop.

The `opacity` and `title` lines go with it: both exist only to explain a
greyed-out control, and neither means anything once it is gone.

**Leave the value alone while it is hidden.** The RMS comment records why:
nothing clears it, so an AC entry's choice comes back when the analysis
returns to AC. The same must hold here — `polar` is saved in the `.cir`
(and in `inputsSnapshot()`), so clearing it on a domain change would edit
the reader's entry behind their back and, since #182, would rightly be
reported as an unsaved edit.

Check afterwards that loading an AC entry with `polar: yes` still shows
the tick, and that switching that entry to DC and back leaves it ticked.

### Done, 30 Aug 2026

Three lines became two:

    $('polarLine').style.display = isAc ? '' : 'none';
    $('polarPhasors').disabled = !isAc;

`disabled` stays, mirroring the RMS pair. A hidden control is out of the
accessibility tree anyway, so it guards nothing a reader can reach — it
guards the code: anything that reads the tick without asking the domain
first still gets the right answer.

**Measured, not eyeballed**, driving the real Flask render:

| domain | tick shown | still ticked |
|---|---|---|
| ac | yes | yes |
| dc | **no** | yes |
| fd | **no** | yes |
| tr | **no** | yes |
| back to ac | yes | yes |

The Display block closes up behind it: in DC the remaining three — *Show
units*, *Use SI prefixes*, *Show equations* — keep their rhythm, and at
375px the block loses exactly the 84px the two-line polar label occupied,
with no gap left where it was.

The value survives, as required. Loading Lesson 7's *AS7's Example 9.9*
(`polar: yes`), switching to DC and back leaves `inputsSnapshot().polar`
`true` throughout, and the entry loads and returns **clean** — no phantom
unsaved edit. It does report an unsaved change *while* the domain is DC,
which is right: the reader really did change the analysis type. That is
#182's warning working, not misfiring.

Live on both offline sites and hash-verified: the deployed page carries
the `style.display` line and **zero** occurrences of `Applies to AC
analysis only`, the string that only ever existed to apologise for a
greyed control.

---

## #182 — two things that went wrong around loading an entry — **done, cache v98**

Roberto, 30 Aug 2026, describing both from use. Both reproduced in the
browser before anything was changed, and both fixed at the source.

### A. Warned about unsaved changes nobody made

Loading an entry asked *"Discard your unsaved changes to '...'?"* over a
form the reader had not touched.

The culprit was the **solver's own correction**. When a circuit carries a
decimal value, "exact" rounding cannot be honoured, so the server returns
`approx_forced` and the page moves the **Rounding** control to
*approximate* and says so — a deliberate, self-explaining UI change. But
`loadedSnapshot`, the baseline "what the inputs looked like when this was
loaded", was left behind. From that moment `inputsDifferFromLoaded()` was
true, and every guard built on it fired: the next load warned about an
edit the app had made to itself.

Reproduced exactly: load an entry, set Rounding to *exact*, solve
`e1,1,0,12.5 / r1,1,0,2.2`, and the control flips to *approximate* while
`differs` goes from false to true. Load the next entry and the warning
appears.

Fixed by absorbing that one key into the baseline where the switch
happens — `loadedSnapshot.rounding = roundingLabel()` — not by
re-snapshotting the lot, so a reader who **does** have unsaved edits is
still told about them. Verified both ways: no warning after the
auto-switch, and a warning still raised after genuinely typing into the
circuit box.

The SI-versus-exact auto-switches in the settings listeners are left
alone deliberately. Those fire as a consequence of the reader ticking a
box, so the resulting state really is their edit.

### B. A solve out of the blue, and stale answers underneath it

After loading an entry and before solving it, touching any setting ran a
solve. Worse than reported, and found while reproducing it: **the
previous circuit's answers stayed on screen**, under the newly loaded
circuit, as though they were its own. Load B11's Example 5.7, solve it,
load the next entry — and `v_1 = 36 V` from the first was still sitting
in **Results**.

One cause for both. `applyCircuit()` put a new circuit in the form
without clearing the old results, so `last` — the record of the last
solve — survived, and the settings listeners' `if (last) solve()` read
it as "there is a result to refresh" and solved.

`clearResults()` now runs at the top of `applyCircuit()`, which covers the
picker, the `?lesson=&entry=` deep link and the session restore alike, and
any caller added later. After a load: the card reads *no analysis run
yet*, `last` is null, and touching a setting runs **zero** solves. Once
the reader does solve, settings changes re-solve as before.

Verified afterwards: the deep link still lands on the right entry with
the form clean, and `/`, `/eqsheet/` and `/healthz` render through Flask.

---

## #181 — exact-and-approx folds when there is no exact — **done, cache v97**

Roberto, 30 Aug 2026, with a screenshot of **AS7's Example 19.2** in
Lesson 13: every polar answer printed the same number twice —
`i_e = 2.0∠180.0° A  (≈ 2.0∠180.0° A)`. His rule: *the exact + approx
should fold into simply approx when there is no exact.*

Measured on that entry, the two halves of one phasor were

    exact    plain '2.00000000000000∠180.000000000000°'   latex '2.0 \angle 180.0^\circ'
    approx   plain '2.00∠180°'                            latex '2.0 \angle 180.0^\circ'

— the **plain** strings differ, which is all `_join_dual` compared, while
the **LaTeX**, the thing the reader actually sees, is identical.
Underneath that is the real point: `_polar_format` numericises, so a
phasor's "exact" half is not an exact form at all, only a longer decimal.

Two tests now decide it, and they answer different questions:

- **`_has_exact_form`** — is there an exact rendering worth showing?
  No when the display is polar, and no when the value already carries a
  `Float` (an approximate input like `2E3` was never exact). Folds to the
  **approximation**, which is Roberto's rule exactly.
- **`_is_whole`** — is there anything to round to? No for a whole number,
  real or complex. Folds to the **exact** half, which is the better of
  the two here: `1j`, not `1.0j`.

`_join_dual` now compares LaTeX as well as plain, as a backstop for any
other formatter whose two spellings render alike.

The whole-number case was not in the report. It is the same defect in a
milder guise — `i_r = 1j A  (≈ 1.0j A)` in rectangular display, a bracket
that tells the reader nothing — and it is fixed with it. Say if that was
wanted left alone.

Verified on the reported entry: AS7's Example 19.2 in polar at 4 digits
now prints **byte-identical to plain "approx to n digits"**, zero `≈`
markers on the page. Rectangular gives `1j A`, `10j V`, `-1j A`, no
brackets. And the bracket still earns its place where it should:
`i_r1 = 3/500 A (≈ 6 mA)`, `p_r1 = 9/250 W (≈ 36 mW)`.

Lessons 7, 8, 9 and 13 — the AC and two-port books — re-swept, all at 0
entries with a problem. `/`, `/eqsheet/` and `/healthz` rendered through
Flask, per the rule #180 wrote down.

---

## #180 — the knowns are equations too — **done, cache v96**

Roberto, 30 Aug 2026, on the Equations card (#176): the listing split into
**Equations** and **Known**, and the second group should not exist. A row
like `i_c1 = s*v_2/1000000` is an equation like any other, and heading it
"Known" asked the reader to care about a distinction the solver makes for
its own bookkeeping.

They now join the main list, in the order the stamp produced them:
stamped equations first, knowns after. **Added in expert mode** and
**Conditions** stay apart — those are the reader's own and worth finding
at a glance, which Roberto left to my judgement.

The merge is in the renderer, not the payload: `system.known` is still
sent separately, so anything else reading it keeps the detail. The card's
own visibility test counts the merged list too, or a system that produced
only knowns would hide a card with something in it.

### The #178 template break, and what it changed about verifying

This item was built immediately after the fix for it, so the note belongs
here. The `#178` comment quoted the credits heading's anchor in its source
form, braces included — and **`{#` is Jinja's comment-opener**. With no
closing `#}`, `templates/index.html` stopped parsing and the server
returned **500 on every page**, while `/healthz`, which renders no
template, stayed green and correctly reported a healthy build.

Every check run after #178 had been against `install.symbulator.com` and
the ZIP. Those are static HTML generated by `build_local.py` and **never
pass through Jinja**, so they were green on builds that structurally could
not catch it.

**An offline check cannot clear a template change.** Anything touching
`repos/server/templates/` has to be rendered through Flask — `/`,
`/eqsheet/` and `/healthz` — before it counts as verified. Done for this
item, along with a real `/api/solve` post.

---

## #179 — the Rounding menu, reordered and reworded — **done, cache v95; PyAn pending**

Roberto, 30 Aug 2026, giving the order and the wording verbatim:

    exact
    exact and approx to n digits
    approx to n digits
    approx

Most exact first, and the two modes that use the **n** box now sit
together instead of at opposite ends.

**The `value` of each option is deliberately unchanged** — `exact`,
`both`, `n`, `approx`. Those are what `roundingLabel()` writes into a
`.cir` and what `applyCircuit()` reads back, so every input file ever
saved still loads and only what the reader sees has moved.

### It made 22 lines of the tutorial wrong, which are fixed with it

The chapters name these options by their labels, and two of the four
labels changed. *approximate to n significant digits* → *approx to n
digits* in 21 places (Lesson 1's own instruction, and the twenty copies
of the `approx`/**Rounding** boilerplate across Lessons 1, 3 and 4), and
*approximate* → *approx* once, in Lesson 5. Left alone: three references
to *exact*, whose label did not change, and two `note:` lines in the
example books that say "five significant digits" — prose about the
setting's effect, not the name of a menu entry.

`examples/Showcase.cir` documents the `.cir` keys at its head and was
two releases stale: its `rounding:` line predated `exact+n` (#175) and
`show_equations` (#176) was missing entirely. Both added.

Docs guards after the pass: `check_against_originals` unchanged at 73
verified / 11 not found, `check_control_chars` clean, `check_white_text`
clean, three PDFs rebuilt at 240 / 205 / 195 pages.

---

## #178 — an Acknowledgements link in the About card — **done, cache v94; PyAn pending**

Roberto, 30 Aug 2026: at the end of the first paragraph of the **About
Symbulator** card, the word **Acknowledgements**, linking to that part of
the credits in the documentation.

Added to the "What is Symbulator" paragraph, pointing at
`https://learn.symbulator.com/9/credits#acknowledgements` — version 9's
credits, this being version 9. The anchor is the
`## Acknowledgements {#acknowledgements}` heading in `src/99-credits.md`,
and it is a real `<h2 id="acknowledgements">` in the built page.

An outward link, like the Tutorial one in the ribbon: it needs the
internet, and the offline build keeps it rather than stripping it. A
reader who is offline is better served by a link that waits than by no
link at all.

**On verifying it.** The fragment could not be confirmed by driving the
browser pane — that pane would not scroll the credits page at all, not by
`location.hash`, not by `scrollTo`, not by `scrollIntoView`, with
`scrollY` pinned at 27 throughout. That is the pane, not the page: the
built credits page contains **no scripts whatsoever**, `web/index.php`
has nothing touching scroll or hashes, and the only relevant CSS is
`html { scroll-behavior: smooth; scroll-padding-top: 1.25rem }`. So the
anchor is an ordinary working fragment in a real browser. Worth a glance
on a phone next time someone is in there, since it was not seen to jump.

---

## #175 — rounding: "exact and approx to n digits" — **done, cache v93; PyAn pending**

Antony García's suggestion, brought by Roberto on 30 Aug 2026: solve the
circuit exactly, but show, for every answer that is a pure number, both the
exact value and a numerical approximation.

A fourth entry on the **Rounding** menu, using the same **n** box as
*approximate to n significant digits*. Roberto chose the layout from three
mock-ups: exact first, the approximation after it in brackets.

    i_r1 = 3/500 A  (≈ 6 mA)
    v_r1 = 6 V
    v_o  = v·r2/(r1 + r2)

The second and third lines are the rule that makes it readable. **An answer
that is already a whole number gains no bracket** — "6 V (≈ 6 V)" is noise —
and **a symbolic answer gets none either**, there being nothing to
approximate. `_join_dual` drops the bracket whenever the two halves would
print the same.

Both formatters are *wrapped*, not rewritten: `fmt`/`fmt0` in `solve_ui`
grew keyword parameters defaulting to the call's own flags, so `_dualise`
runs each answer through the very same code twice — once with the rounding
off, once with it on. The two halves therefore cannot drift apart in units,
polar form, SI prefixes or the infinity spelling. SI prefixes land on the
approximation only, which is what makes `3/500 A (≈ 6 mA)` read as it does.

It applies in **Evaluate** and the **Solve** card too, not only Results: a
setting that visibly did nothing in two of the three places answers arrive
would read as a bug. Both took the same treatment; `evaluate_ui`'s two
identical formatting tails became one `shown()` on the way past.

Carried in the input file as `rounding: exact+4`. An older Symbulator
reading that file falls through to plain n digits — wrong in the display,
right in the arithmetic.

Wired through `app.py` **and** `repos/local/bridge.py`: the offline build
calls `symbulator_ui` directly, so a flag added to one and not the other
works online and silently does nothing offline.

---

## #176 — a Show equations tick, and an Equations card — **done, cache v93; PyAn pending**

Antony García's second suggestion, same day. A tick in **Settings**, and
when it is on, a card under Results headed **Equations** listing the system
the solver assembled, set as mathematics with MathJax.

Most of it was already there: `symbulator_ui` has built the equation list
for the Export Output card's download all along. What is new is `system`, a
grouped version of the same content carrying a LaTeX rendering per line —
the stamped equations, the known values, expert-mode extras marked
**Added in expert mode**, **Conditions**, and the unknowns at the foot.
Roberto's call: the whole system, not equations and conditions alone.

Three things worth knowing:

- **The card needs both the tick and a system.** An empty card headed
  "Equations" is worse than no card, so it stays hidden without both.
  Ticking the box after a solve re-renders from `last.system` rather than
  solving again.
- **The unit step is shown `u(t)`, not `θ(t)`.** SymPy's LaTeX for
  Heaviside is theta, which is not what the app's input language or the
  tutorial calls it. The EqSheet export already rewrote it; the card does
  the same now.
- **`app.py` lists the payload keys by hand**, as its own comment warns, so
  `system` had to be named there or the server variant would have dropped
  it silently while the offline build worked. `bridge.py` returns the
  payload whole and needed nothing.

### The TR system was a chimera — fixed, and it predates the card

Roberto, reading the first TR listing: a source appearing in the time
domain. He wondered whether it was the calculator's **Impala mode** — the
version 4 trick that stamps a placeholder for a time-varying source, solves,
then substitutes the s-domain value and re-evaluates.

It is not: **there is no Impala in version 9**, and the port never needed
one. `laplace.tr()` moves the sources into s *before* stamping
(`_sources_to_s`), solves that in FD, and inverts the answers — the same
destination by the opposite route.

The real cause was this code stamping the description **as typed** while
`tr()` stamps the transformed one. Exactly one line differed, and it was
the source's own defining equation — "the drop across it is its value" —
which is precisely the line that shows which domain the value is in:

    what was listed          what tr() actually solves
      v_1 = 12*u(t)            v_1 = 12/s
      v_1 - v_2 = 1000*i_r1    v_1 - v_2 = 1000*i_r1
      i_e + i_r1 = 0           i_e + i_r1 = 0
      -i_r1 + s*v_2/1e6 = 0    -i_r1 + s*v_2/1e6 = 0

A system with the capacitor in s and the source in t is one nobody solves.
The stamp now uses `_sources_to_s(desc)` for TR, and `_relations_to_s` for
the expert extras, which `tr()` also transforms.

**This is older than the card.** The flat `equations` list the Export Output
card downloads was built from the same Circuit and has carried the same
hybrid for every TR solve since it existed. Both are fixed, because both
come off the one stamp.

Verified afterwards: every one of the 18 example books through
`tools/verify_lesson.py`, all reporting **0 entries with a problem** — the
sole exception being Lesson 4's Bo2 Example 3.11, the failure that lesson
teaches on purpose. The TR books (06a–d) and the FD book (12) were the ones
Roberto asked for by name.

**Deployed 30 Aug 2026 to the two offline sites**, at cache **v93**, and
verified by fetching: the Rounding menu on `install.symbulator.com` reads
exact / approximate / approximate to n significant digits / **exact and
approx to n digits**; `showEquations` and `equationsCard` are both in the
page; `sw.js` reports `symbulator-v93`; the served `symbulator_ui.py`
carries both `_dualise` and the `_sources_to_s(desc)` TR fix; and
`symbulator.com/9/local.zip` matches the local build by hash.

**`symbulator.pythonanywhere.com` still runs the old build** until Roberto
pulls. `symbulator_ui.py`, `app.py`, `circuitbook.py` and
`templates/index.html` all changed, so the pull matters beyond pip; no
solver release is involved, so `pip install --upgrade symbulator` is not
needed and 0.5.22 stays correct.

---

## #174 — ribbon and card wording — **done, deployed everywhere**

Roberto, 30 Aug 2026, in four separate notes while the PDF work ran.

In the ribbon under the banner:

- **Download App** → **Local App**. The short spelling stays `App`.
- **Documentation** → **Tutorial**. Both spellings now read `Tutorial`:
  the word is already short enough that a separate phone spelling would
  only be a second thing to keep in step, and `Docs` no longer matches
  the full label anyway.

On the cards:

- the **Explore Numerically** card is headed **Numerical Solver**
- the **Plot** card is headed **Plotting Tools**

The Tutorial rename was applied to `templates/eqsheet.html` as well as
`templates/index.html`, so the Numerical Solver's own ribbon says the same
word as the app's. Say if you would rather it stayed *Documentation* there.

The two comments in `index.html` that quoted "Download App" by name were
updated with it, so a search for the label still finds the code that
depends on it — the anchor into the collapsed *Run Symbulator 9 locally*
card, which is server-only and which `build_local.py` strips.

**Deployed 30 Aug 2026 to the two offline sites**, at cache **v92**:
`build_local.py`, `build_zip.py --assets ../../local`, `install_site`
refreshed from the new ZIP, then `install` and `zip`. Verified by fetching:
`install.symbulator.com` serves *Tutorial* in the ribbon, *Plotting Tools*
and *Numerical Solver* on the cards, and `sw.js` reports `symbulator-v92`;
`symbulator.com/9/local.zip` matches by hash.

**PythonAnywhere done the same day.** `/healthz` reports build
`2026-08-30 04:36 UTC` running and on disk, `needs_reload: false`, solver
0.5.22 — no release was involved, so 0.5.22 is correct rather than stale.
Verified by fetching: the app's ribbon links are exactly *Local App* (to
`#runLocallyCard`) and *Tutorial* (to learn), the cards read *Plotting Tools*
and *Numerical Solver*, `Download App` appears nowhere, and `/eqsheet/` says
*Tutorial* too.

One thing a grep will trip over: `subbar-lbl">Documentation` still appears in
both pages. It is inside the CSS comment that documents the two-spelling
convention (#144), not a link — the illustration was left as it was rather
than restamping every build to reword an example.

---

## #169 + #170 — the reader-quiet examples pass — done overnight, cache v91

Roberto, 29 Aug 2026, late: having caught two bugs by running library
examples as a reader, he asked for all of them run and every Results
notice justified — then accepted the recommendations and went to
sleep ("work autonomously... so that when I wake up I do PyAn"). The
sweep: all 330 entries of the 20 books through the real app, four
parallel batches. 121 findings, four classes.

**#169, the code half** (`symbulator_ui.py`): the AC imaginary
normaliser now touches a value only when it genuinely respells
`i`/`I`/`J` — a value already in j-form is left exactly as typed,
which removes the "normalised '8-6j' to '8 - 6j'" yellow box from
roughly ninety AC/power/three-phase entries (a note per spacing
change), and it never reprints through sympify, which had collapsed
Problem 9.39's typed `4+20j+pr(16,-14j+25j)` into an opaque
fraction. The SymPy-shadow note skips names the circuit owns (`rf`
is the feedback resistor, not the rising factorial), and the
answer-name-as-value note skips an element valued by its own name —
the idiom Lesson 2 documents ("it is not a problem that the symbolic
value is the same as the name"), which the transistor bias model's
`re1,e,0,re1` uses. Genuine cases all still fire: `10+5*i` still
normalises with its note, `gamma` still gets the shadow note, a
resistor valued by *another* element's answer still warns.

**#170, the entry half**: eleven TR sources written as explicit
steps (`u(t)`-form) — **Drill 5.7 alone keeps the bare constant**,
because its own note and the chapter teach exactly that shorthand
("a plain 12 is enough, no u(t) needed"), so its step note is the
lesson confirmed; everywhere else the constant was incidental and
the chapter's own house style is explicit `V*u(t)` anyway. Fifteen
entries with decimal inputs now carry `rounding: approx` themselves
instead of being auto-switched with a note. Example 6.6 keeps its
Float source (`12.0*u(t)`): dropping the trailing dot made the
answers come back in exact `sqrt(3999991)` form instead of the
chapter's decimals — caught by the display-equality check, restored.
Ten `field 9` blocks in `Documentation`'s transient chapter updated to
match (the DC-interval twins verified untouched), plus the chapter
date.

**Verification, twice over**: the displayed answers of all 185
entries in the affected books captured before and after —
byte-identical (the one drift, 6.6's exact-form slip, was caught and
fixed by exactly this check). Then the full 330-entry sweep re-run:
**exactly four notices remain, each deliberate** — Bo2 3.11's taught
failure, the Thévenin unbounded-current lesson, Drill 5.7's step
note, and the Bode showcase's impulse note. Shipped at cache **v91**
on both offline sites; the server takes it with Roberto's morning
pull + Reload (no pip — `symbulator_ui.py` and the examples).


## #168 — the two-port's Results card, and two Tools-group touches — done, cache v90

Roberto, 29 Aug 2026, on seeing where Example 19.2's port currents
landed: showing them under "Expert mode unknowns" was "ridiculous" —
they have nothing to do with expert mode. Now the two-port gets a
proper card in **Results by Element**: its name, the kind label
*two-port*, and the two port currents, each labelled **"current into
port at node <n>"** — *into* the two-port (measured: the engine
stamps each as leaving its node into the block; 19.2's i_z1 = +2∠0°
with the source driving port 1 confirms the direction), matching the
chapter's "current entering each port" and the 2023 originals. Card
rows gained an optional per-row subscript (`sub`) so the two
currents print as i_z1 and i_z2 rather than both claiming i_z; the
catch-all section keeps its role for genuine expert-mode unknowns
and is empty on 19.2. `verify_lesson.py` reads the new spelling and
Lesson_13 still ends 0 problems.

Two more of Roberto's touches rode along: the **SPICE Translator
moved to last of the four Tools cards** (Mini-Tools, Plot, Explore
Numerically, SPICE Translator), and its **buttons swapped** so
*Symbulator to SPICE* sits on the left. All three verified in the
running app before deploying. Cache **v90** on both offline sites;
the server needs Roberto's pull + Reload (no pip — the shared
`symbulator_ui.py` and the template).


## #167 — a called name is not an answer reference — done, cache v89

Roberto, 29 Aug 2026 late evening, running Lesson 13's Example 19.2:
a note asked about a `pr` he never wrote. Confirmed: the
answer-name-as-value heuristic (`ambiguous_answer_names`, 24 Aug)
scans value *text* after the bracket shorthand has encoded `[...]`
as `pr(...)`, so any circuit with an element literally named `r`
warned about `pr` ≡ `p_r`. 19.2 has a bare `r` — which is also why
the tests missed it (they used `r1`, `rl`). Three shapes tripped it:
an encoded parameter term, an encoded resistor bracket, and a typed
`pr(6,3)` call. The fix covers all three at once: a name immediately
followed by `(` is a function call, never an answer reference, and
is skipped. The true positives stand — a *bare* `pr` or `re` used
as a value still warns exactly as designed. Verified on all five
shapes. #165 itself was checked and is correct — the encoding is
text-level and universal by design; only this reader of the encoded
text was naïve. Shipped at cache v89 on both offline sites; the
server needs Roberto's pull + Reload (no pip — `symbulator_ui.py`
only).


## #166 — the port tool's parameters, ready to paste — done, cache v87

Roberto, 29 Aug 2026 evening, closing the loop #163 opened: after
*Find equivalent → Two-port parameters*, the reader should be able to
carry the four found values into a following simulation without
transcribing them. Below the four named answers the app now shows
**"As a two-port element's parameter term: `[60,40,40,70]`"** with a
**Copy** button — the term only, per Roberto ("not sure if the whole
element, but at least the parameters"). Built from the *exact*
solved expressions in `values`, not the rounded display strings, so
an FD run copies `[1/(s+1),...]` intact; whitespace is stripped so
the term pastes cleanly. Clipboard via `navigator.clipboard` with a
legacy fallback; when neither works the button says "Select and copy
by hand" (the term is plain text either way). Verified in the real
app: the z-parameter T-network run shows the term and the button.
Shipped at cache **v87** on both offline sites, hash-verified; the
server variant gets it with Roberto's pending pull + Reload (one
pull now carries #164's fix, the lesson-13 examples, and this).

## #165 — brackets mean pr only in a resistor's value — done, shipped in 0.5.22

Roberto, 29 Aug 2026 evening, on hearing how #164's AC bug was fixed:
he remembered the calculator restricting the `[...]` shorthand, and
measurement proved the port looser — `e1,1,0,[4,4]` silently became
a meaningless "2 V" source (pr applied to a source value), and a
capacitor value would have computed the *series* combination
(parallel capacitances add; pr is the resistor rule). His ruling: in
two-ports `[...]` is the parameter term, in a resistor's value it is
the pr shorthand, and **anywhere else it stops the simulation** with
a message. Implemented in `parse_circuit` on the *typed* text (a
`pr(...)` the user typed remains a function call, legal anywhere);
nested brackets in a resistor value still work. Swept first: none of
the 330 built-in examples nor the docs use brackets outside the two
legitimate places. 311 solver tests pass. In the repo — ships with
the next solver release; live sites stay 0.5.21 (which still accepts
the loose forms) until then.

## #163 — two-port parameters in the description — done, shipped in 0.5.21

Roberto, 29 Aug 2026, on discovering that the v9 port had left
two-port parameters reachable only through expert mode (a Sonnet
porting decision he had not reviewed): a design of his own, three
cases. **Case A** — `z,1,2` alone keeps the tacit parameter term
`[z11,z12,z21,z22]` and the parameters stay symbolic (today's
behaviour, so old descriptions are untouched). **Case B** — Define
supplies values for any of the four names, and they land: the app's
`expand_defines_in_desc` (shared `symbulator_ui.py`, both repos)
materialises the tacit term when a define names one of its entries,
and the values substitute; partial definitions leave the rest
symbolic. **Case C** — the term written explicitly:
`z,1,2,[100,10,20,50]`, entries numeric, SI-prefixed or symbolic
expressions. Implementation: each entry binds its
correspondingly-named variable through the same substitution
machinery as expert conditions (the TI's `|` operator — the
calculator's "store the values first"), placed so an explicit user
condition on the same name still wins. The values are substituted
into the system *before* solving, so they ride into the Numerical
Solver handover already baked in. No clash with the `[a,b]` parallel
shorthand: two-ports have no value field, and the internal `pr(...)`
encoding disambiguates by element kind. Verified: term ≡ conditions
(same answers), all six kinds, override, partial defines, malformed
lists refused, the schematic drawer unaffected — and Roberto's
v7/v8-era guards were confirmed still live and stopping the solve
(a port node of 0, or both ports on one node, each a clear
`CircuitError`). The naming rule (`z` → `z11`, `z1` → `z111`) is
deliberate and documented rather than warned about, per Roberto.
Solver README rewritten accordingly; every code block run verbatim.

## #162 — every element type exports to SPICE — done, shipped in 0.5.21

Roberto, 29 Aug 2026: ideally any Symbulator element translates to
SPICE, even where the reverse is not feasible. Now true. The ideal
**op-amp** exports as a gain-1e9 VCVS (`Eo1 3 0 0 2 1G`) — the
universal SPICE idiom, parts-per-billion finite-gain error, and the
warning says "finite-gain stand-in" honestly. The ideal
**transformer** exports *exactly*: a VCVS at the turns ratio, a 0 V
current sense, and a CCCS reflecting the secondary current into the
primary — correct at DC, where the coupled-inductor approximation
(k=1 inductors) shorts out; the measured port relations
(`v/t` equal, `t·i` conserved, both checked against the solver)
round-trip symbolically equal. A **two-port block** with a numeric
parameter term (#163) exports as up to four grounded VCCS elements
via the engine's own admittance reduction — the i1/i2 formulas
transcribed verbatim from `engine._stamp_two_port`, so exporter and
solver cannot disagree; sets singular in admittance form warn, as
the solver itself cannot substitute them either. Also fixed while
verifying: computed netlist numbers (gains, ratios, coupling
factors) now print with round-trip precision — six significant
digits measurably shifted every solved voltage at the 1e-6 level,
caught by the ground-truth harness. All of it verified per node
voltage against the independent simulator: op-amp, transformer, and
each of the six two-port kinds, alongside the #161 cases. 310
solver tests pass.

## #161 — dependent sources translate to SPICE — done, shipped in 0.5.21

Roberto, 29 Aug 2026, after testing the SPICE Translator online:
solve the Symbulator→SPICE direction for dependent sources ("think
deep and hard about it"). Built the same day as solver **0.5.21**
(committed and pushed, wheel built and twine-checked, **not yet on
PyPI** — the release train awaits Roberto's go).

The mechanism: `to_spice()` decomposes a dependent value as an
*affine* expression over node voltages (`v_2`), two-terminal element
drops (`v_r1`) and element currents (`i_r1`) — spelling equivalence
included — via SymPy's `linear_coeffs`, then emits one plain linear
SPICE element per term: E/G for voltage controls (a `+k`/`−k` node
pair folds into one textbook difference-controlled element, oriented
so the gain is positive), H/F for current controls, an independent
V/I for any constant. Terms chain in **series** for a voltage source
and in **parallel** for a current source, through generated internal
nodes (`e2_x1`…). A current control on anything that is not already
a voltage source gets a **0 V sensing source** spliced into that
branch (`Vi_r1` — SPICE's own ammeter idiom), shared by all
referencing sources, and dependent sources can sense each other. The
current of an independent current source is its own value and folds
into the constant. Nonlinear controls and symbolic gains warn as
before; a reference to an untranslatable current cascades its
warning to the referencing source, naming the culprit.

Sign conventions were **measured, not assumed**: Symbulator's
`i_el` is positive n1→n2, its `e`/`j` node order and SPICE's
`V`/`I`/`I(V)`/E-control conventions align in all four cases with no
flips anywhere. Verified two independent ways: round trips re-solved
through `from_spice()`, and — because a symmetric sign flip cancels
in a round trip — every emitted netlist also runs through **ahkab**,
an independently implemented pure-Python MNA simulator, compared
node voltage by node voltage (11 parametrized cases in the new
`test_spice_groundtruth.py`, self-skipping where ahkab is absent;
reviving ahkab 0.18 on Python 3.14 took three shims, documented in
the file). The harness caught a real quirk worth remembering:
**ahkab's H (CCVS) senses with the opposite sign to its own F and to
the ngspice manual** — the manual defines F and H identically, and
ngspice/LTspice/PSpice follow it, so the exporter targets the
manual and the test harness flips H gains into ahkab's dialect.
288 solver tests pass.

**The train ran on Roberto's "Punch it!", 29 Aug 2026 evening**,
carrying #161, #162 and #163 together: 0.5.21 on PyPI (wheel
sha256 3a45f825…, hash-verified identical to the bundled copy),
cache **v85**, both offline sites deployed and hash-verified, the
SPICE card's beta note live, `requirements.txt` at `>=0.5.21`. The
offline build was smoke-tested through real Pyodide before deploying
(a two-port parameter solve and an op-amp export) — after first
falling for the documented stale-service-worker trap in the test
browser itself, which is the trap doing its job.

**Remaining:** Roberto's PythonAnywhere pass — the pull matters
beyond `pip install --upgrade symbulator` this time, since the
shared `symbulator_ui.py` changed (#163's Define materialisation) —
then verify with a solve, a translation, and a two-port parameter
circuit. And the wheel prune on the install host (typed DELETE):
0.5.19 **and** 0.5.20 now sit beside 0.5.21 there. Queued next:
**#164**, the Lesson 13 two-port documentation revision in the docs
tree (`Documentation`) — Roberto: "in addition to, and independent from,
the SPICE stuff" — documenting the three cases, the naming rule, and
the guards.

## #160 — the SPICE Translator card — done, live on all three app surfaces

Roberto, 29 Aug 2026: a Tools card named **SPICE Translator** — a
Symbulator Notation field and a SPICE Notation field, a button for
each direction, and warnings whenever the origin holds element types
or symbolic values the destination cannot express. A prototype, to
be tested online and refined.

Built and shipped the same day to both offline sites (cache **v84**,
wheel **0.5.20** bundled, hash-verified). The translation lives in
the solver as `symbulator.spice.to_spice/from_spice` (18 tests,
round trips verified by solving both circuits, not comparing text);
`symbulator_ui.spice_ui` wraps it; the server has `/api/spice`; the
offline build calls `bridge.spice()`. What translates: r/l/c with
initial conditions (`IC=`), independent sources, shorts (a 0 V
source, SPICE's own idiom), mutual inductance ↔ `K` (numeric
inductances only), and SPICE's E/G/F/H controlled sources
(`E1` → `ee1`, so it can never collide with `V1` → `e1`). Everything
else warns instead of mistranslating: op-amps, ideal transformers,
two-ports, symbolic values, waveform sources (a `SIN(...)` keeps its
DC value if it has one), diodes and transistors, subcircuits,
directives. The mega/milli trap is closed by construction: `1'M`
exports as `1MEG`, and the exporter never writes a bare `M` at all —
milli becomes a plain decimal.

**0.5.20 reached PyPI on 29 Aug 2026** (uploaded from Roberto's
machine at his instruction after the permission layer blocked the
assistant's first attempt; PyPI's recorded sha256 5d856850… matches
the bundled `vendor/` wheel exactly). This release also carries
#158's README section and #159's name check to the PyPI page.

**Roberto's PythonAnywhere pass completed 29 Aug** ("PyAn done"),
verified by fetching: `/healthz` reports build `2026-08-29 07:05
UTC` running and on disk, `needs_reload: false`, solver **0.5.20**;
a real solve through the live `/api/solve` returned the Lesson 1
answers exactly, and a live `/api/spice` translation spelled `2.2'M`
as `2.2MEG` with no warnings. The card is a prototype by design —
Roberto will test online and refinements become new numbered items.

The one loose end is routine: the wheel prune on the install host
(`py deploy_symbulator.py install --prune "symbulator-*.whl"`, typed
DELETE — Roberto's) still has 0.5.19 sitting beside 0.5.20.

## #137 — remove the β from the banner wordmark

Roberto, 28 Aug 2026: the wordmark reads **Symbulator 9β** while
version 9 is in beta — banner titles only, on all five properties
(learn shows it only on the version-9 pages), shipped the same day.
This item is the standing reminder to take it out "when it's no
longer betta": the five spots are `web/index.php` +
`tools/static_preview.py` (a label == '9' conditional),
`landing/index.html`, and the two `templates/*.html` in the server
repo — each marked with a "temporary" comment. A cache bump ships
the removal to the offline builds.

---

Everything below is closed: #140–#150, #158 and #159 landed on
29 Aug 2026 and #132–#136, #138 and #139 on 28 Aug 2026, each the
same day it was accepted. (#151–#157, the docs-side visual pass over
the PDFs, are written up in `Documentation/NEXT_DOCS.md` on
the same running sequence.) The write-ups follow, newest first; the
next new item is **#160**.

## #159 — names that cannot appear in an expression are refused — done

Roberto, 29 Aug 2026, asked whether any resistor names were
forbidden. Measured against 0.5.19: none were — the old
`RESERVED_NAMES` set in `symbulator/elements.py` was declared and
referenced by nothing, dead since the fixes that removed
reserved-name handling (Roberto remembered this correctly). The only
enforced rules were the element-kind prefix and uniqueness after
case folding.

The measurement also showed why that was one rule short: a resistor
named `r-x` parsed and solved fine alone, but a dependent source
written `2*i_r-x` silently read as the subtraction `2*i_r - x` and
returned an answer containing phantom symbols — no error, wrong
result. Dots and spaces failed the same way.

Roberto: names should not have hyphens; put in a warning — and, he
clarified when the implementation was reported back, by "warning" he
meant the ambiguous-suffix treatment: the user is asked to resolve
it and the simulation does not proceed. That is exactly what the
parse-time `CircuitError` gives through the app: the pre-flight
parse in `repos/server/app.py` (the same stage as the ambiguity
check) catches it before any solve and returns the message to the
browser. The one difference from the suffix flow is deliberate —
`1k` gets a picker because both readings are valid and the app can
proceed with either; a hyphenated name has no valid reading, so the
resolution is the message itself: rename the element. `parse_circuit` now requires the folded name to be
identifier-safe (letters, digits, underscores — `name.isidentifier()`),
on the solve and echo (`expand_si=False`) paths alike, with a message
that quotes the name as typed and says why: the element's answers
(`i_...`, `v_...`, `p_...`) must stay typable inside a value or an
added equation. `RESERVED_NAMES` deleted in the same commit.

Checked before committing: all 246 solver tests pass (two new — the
rejection for `r-x`/`r.1`/`r x`, and a guard that `r`, `r0`, `r_1`,
`ris`, `rlongname99` still solve); every one of the 1,637 element
lines across the 330 built-in examples already satisfies the rule.
One residual quirk left alone, recorded here: `r1` and `r_1` may
coexist as distinct elements, and a spelled reference like `ir1`
binds to one of them without an ambiguity error — legal under the
spelling-equivalence rules, confusing to write, not worth a rule
until someone actually does it.

In the repo, not yet released: ships with the next solver release
(the same one that takes #158's README section to PyPI). Until then
PyPI, the bundled wheel and the server all stay 0.5.19, which still
*accepts* such names — the app's behaviour changes only when that
release is cut and deployed.

## #158 — the solver README teaches the SymPy side — done

Roberto, 29 Aug 2026: asked whether the `symbulator` package deserved
a manual on being used from Python/SymPy. The README already *was*
the manual for the API; what no package user could learn from it was
what to do with an answer once they had one — every answer is a SymPy
expression — and the two traps recorded only in
`Documentation/VERIFIED-v9-api.md`, which no PyPI reader
ever sees.

New README section, **Working with the answers (SymPy)**, between the
`fd()`/`tr()` section and expert mode: answers are exact SymPy
expressions (`5/2`, not `2.5`); `simplify` on a symbolic solve; the
time-symbol trap — answers use `Symbol("t", nonnegative=True)`, so a
bare `Symbol("t")` substitutes as a silent no-op — with its two
escapes, `res.at(t=...)` (substitutes by name) and
`from symbulator import t, s`; initial/final values by `subs`/`limit`
plus the final-value theorem on an `fd()` answer; `sympy.plot` with
the imported `t`; `lambdify` for NumPy; `bode_samples()`/
`time_samples()` and why an `ac()` result cannot be swept by
`plot()`; and the `pf()` sign at a source (negate the current for
leading/lagging).

Alongside it: `llms.txt`'s easy-to-get-wrong list grew from two
entries to three with the `t` trap, and the one stale
`positive=True` in `Result.at()`'s docstring
(`symbulator/analysis.py`) was corrected to `nonnegative=True` — the
assumption changed to `nonnegative` on 26 Aug 2026 so impulses at
t = 0 survive, and the docstring had not followed.

Verified before committing: every code block in the section was
executed verbatim, in published order, against the installed 0.5.19,
with each printed claim asserted (17 checks, all passing). GitHub is
the deploy for a README change; the PyPI page renders the README of
the *last uploaded release*, so it picks this up with the next real
release — no version was cut for prose alone, to keep the
0.5.19-everywhere parity across PyPI, the bundled wheel and the
server pin.

## #150 — the app footer wraps between the copyright and the links — done

Roberto, 29 Aug 2026: if the "Symbulator © 1999–2026 Roberto
Perez-Franco · symbulator.com · Facebook · GitHub · PyPI" line has to
wrap, it should break where the links start, the separator dot leading
the second line. Two nowrap spans now; measured breaking exactly there
at 375px, one line on desktop. Shipped at cache v83.

## #149 — Mini-Tools works before a solve — done

The card sat dim until a circuit was solved, but aa, pf and gain are
standalone calculators on typed arguments. Now active from the start,
like Explore Numerically (#136); Clear all inputs empties its output
but no longer deactivates it. The real coupling turned out to be two
lines of code, not the tools: `runMiniTool` returned silently without
a solve, and `callMiniTool` read `last.values` off the null `last` —
both now tolerate no-solve (an empty values dict; a solve only adds
its answer names to what arguments may reference). The offline build's
`build_local.py` substitution moved in step, and `aa(3+4j)` was run
pre-solve in the rebuilt offline app: 5.00000∠53.1301°.

## #148 — one phrasing for how entries are separated — done

Seven hint spans (Expert Mode's equations/unknowns/conditions, the
Solve card's three, Evaluate's Conditions) now all read canonically:
"one per line or separated by `and`" for equations and conditions,
"one per line or separated by commas" for unknowns, each with an
e.g. Wording only — measured first that every one of the seven
fields already splits on both (the #96/v76 machinery).

## #147 — the Built-in Examples picker no longer overflows on mobile — done

Roberto's screenshot, 29 Aug 2026: the entry picker ran off the right
edge of the phone. A native select's default width is its widest
option's text, and entry names are wider than a phone. `max-width:
100%` on `.examples select` (and on the solution picker, whose labels
quote roots); the closed select clips its label, the opened list is
the OS's own and loses nothing. Measured at 375px: 294px wide, inside
the viewport.

## #146 — the Plot menu reordered, H(s) label shortened — done

New order: the DC sweep first (and the menu's rest state, including
after Clear all inputs), Bode of a variable, "Bode plot of transfer
function H(s)" (the "(FD)" dropped so the label holds one line on a
phone — the H(s) gives the analysis away), the TR plot last. The
sweep's label also shortened to "Plot a variable against another
(DC)". Values unchanged, so nothing downstream moved.

## #145 — the Numerical Solver's name moved into the property mark — done

The property mark reads **Numerical Solver** (both spellings), the
ribbon dropped the sheet-id and the "Symbulator App" link, and
Documentation — the one link left — shortens to "Docs" at phone
widths via the shared vocabulary of #144. Measured at 375, 560 and
1280: the mark fits in the slot form, never overlaps the brand, and
the ribbon holds one line with the DC/AC toggle in view.

## #144 — the app ribbon's labels shorten on narrow screens — done

Download App → App, Documentation → Docs, Clear all inputs → Clear
inputs, at ≤480px — the width where the banner already hides the
subtitle. Mechanics in the shared `banner.css`: a control carries two
spans, `.subbar-lbl` and `.subbar-lbl-short`, and exactly one shows —
the same two-spellings idea as the property mark. Measured at 375px
on both variants: short labels, one-line ribbon.

## #143 — the ribbon is one line at every width — done

The one-line clip of 28 Aug capped the *link row*, but the ribbon
row itself (`.subbar-inner`) still flex-wrapped — and flexbox wraps
on content sizes before it shrinks anything, so learn's version
picker dropped to a second line while all three links showed. Now
`.subbar nav` is `flex: 999 1 0`: the nav claims no width of its
own, grows into what the row can spare, and a link that does not fit
clips away (on learn, "How it works" hides first, exactly as asked).
Grow 999 and not 1 because the spacer grows too and at equal factors
starved the nav into clipping links it had room for — caught by
measurement at 375px, not by eye. Verified live on learn at 375
(How it works hidden, one line) and 700 (all three shown).

## #142 — "How it works" points at the landing section — done

learn's ribbon link goes to `https://symbulator.com/#logic` — the
landing page's new "The logic and its history" section (#140), where
the monograph is offered with its context — instead of at the PDF
directly.

## #141 — the landing footer's line reworded — done

"Born free and shared openly for the greater good." — "freely"
became "openly" and the comma went. One spot; verified live.

## #140 — the landing page reordered — done

New order: Hero · What it does (with its limits block) · Start here
(the Learn It cluster keeps only the Documentation card) · For
developers · On a calculator · **The logic and its history** — a new
final section (`#logic`) holding the Internal Logic and Symbulator
Book cards, under the headline "Two books: how it works inside, and
where it began." The tinted bands reassigned to keep alternating down
the new order (what/build/logic tinted). Verified live: order,
anchor, and a one-line ribbon at phone width.

## #139 — the Built-in Examples dropdown closes on an outside click — done

Roberto, 28 Aug 2026: "it doesn't want to go away unless you click on
'Built-in Examples' again. It's annoying, hehe." The `<details>` menu
now closes on any click outside itself (a document-level listener that
checks `menu.contains(ev.target)`) and on Escape, which also returns
focus to the summary. Clicks inside the panel still work as before —
picking an entry already closed it. Shipped at cache v82.

## #138 — URL parameters open a built-in example — done

Roberto, 28 Aug 2026: a link like
`https://symbulator.pythonanywhere.com/?lesson=4b&entry=17` opens the
app with the 17th entry of Lesson_04b loaded — for linking straight
from the documentation to a worked example. `?input=` is an alias for
`?lesson=` (both of Roberto's spellings work), `entry` is 1-based and
defaults to 1, and `lesson=showcase` / `lesson=monograph` reach the
Showcase and The_Monograph books. Lesson values accept `4b`, `04b`,
`7` and so on (a leading zero is optional). A bad lesson or an
out-of-range entry shows the app's own note ("no lesson 99…") and
falls through to normal startup. **The link wins over the restored
workspace**: `openFromUrl()` runs before `restoreState()` in
`loadExamples`, and a successful open persists, so a reload without
the query keeps what the link loaded. Works identically in the
offline builds — the query is read client-side, so
`install.symbulator.com/?lesson=4b&entry=17` works too. Verified live
on the Flask build: `?lesson=4b&entry=17` → Bo2's Drill Exercise 3.12
with picker synced and note shown; `?input=7&entry=3` → AS7's
Example 9.10.

## #136 — Explore Numerically, capitalised and always active — done

The card heading "Explore numerically" became "Explore Numerically",
and the card is active before anything has been solved: after a solve
the button carries that solve's system to the Numerical Solver via
the `?import=` payload exactly as before, and before one it opens a
blank solver (a plain link to `/eqsheet/`, no payload). The
`inactive` gating in `activatePostSolve`/`clearResults` is gone.
Shipped at cache v82.

## #135 — the property mark — done

Roberto's brief, 28 Aug 2026: an elegant designation of which
property the reader is on — Documentation (learn), Welcome (landing),
Application (the hosted app and PythonAnywhere, *not* the downloaded
local build), Numerical (the Numerical Solver). Chosen from a
rendered mockup: spaced capitals in the sky at 55% opacity, no
brackets — the app's [ T O O L S ] motif moved into the banner — at
the right of the top band, on the wordmark's centre line, ending on
the band's own right edge (a negative margin swallows the trailing
letter-space). Treatment 2 for mobile, Roberto's pick: shrunk below
640px, and at ≤480px it moves into the slot the hidden subtitle
leaves under the wordmark. The styling is shared vocabulary in
`banner.css` (`.property-mark`, `-top`, `-slot`: one word, two
spellings in the markup, exactly one ever shown); each property
supplies its word, the app's wrapped in the markers the offline
build strips — which is what keeps the local build unmarked for
free. Verified by computed style at 1280/500/360 on the docs
preview, and by grep that the built local page carries no mark.

## #134 — rounding in the Numerical Solver — done

A Rounding menu in the sheet's status bar — full (the original
behaviour), or 3/4/5/6 significant digits. Display-only, the same
doctrine as the noise chop: the solver's numbers and the residuals
line stay raw; Result cells re-format, in the row's SI prefix, and
in AC the angle follows the same choice (it keeps its two decimals
until a rounding is chosen). Persists in localStorage like the
theme. √2 shows 1.41421 on full and 1.41 at 3 digits, measured.

## #133 — Expert answers in the two exports — done

The Numerical Solver side was overtaken by the export fixes (v79):
expert unknowns cross as unknowns with their solved values as
guesses. The Export to SymPy side had a real hole: an expert unknown
named `is` produced `is = sp.S(...)` — a script dead on arrival,
since `is` is a Python keyword, and the same name broke the
sp.symbols declaration line. Keyword names now export with a
trailing underscore (`is_`), PEP 8's own convention, while the
SymPy Symbol keeps the true name; a comment in the script says which
names were renamed. The generated script for the showcase circuit
executes clean under real Python, `is_` = 0.39727 included.

## #132 — the Restriction menu's first option reads "None" — done

Label only; the stored value and the API are unchanged.

> **Deployed and verified, 28 Aug 2026 (four releases).** Cache
> **v71**–**v74**; solver **0.5.16** through **0.5.19**. 0.5.16 is
> the schematic rework — the drawer reviewed against all 322 tutorial
> circuits (wires never cross element bodies, real crossings drawn as
> hops, junctions on node corners, values shown as typed, long values
> captioned below the drawing; see the solver CHANGELOG); 0.5.17 has
> the op-amp feedback wire leave the tip the way the triangle points;
> 0.5.18 closes #130 below; **0.5.19** (cache v74) adds expert-mode
> inequality conditions, Python keywords (`is`) as names, and full
> spelling equivalence of underscored and flat answer names —
> universal, in values, expert equations, unknowns and conditions.
> Between them, `banner.css` moved into this repository (#75's
> inversion — see the write-up below) and the review harness landed
> in `server/tools/review_schematics.py`. install + ZIP + learn +
> landing deployed and hash-verified with 0.5.19 bundled. **PyPI and
> PythonAnywhere still at 0.5.18**: the autonomous session could not
> run `twine upload` (permission-gated), so the upload is Roberto's
> (`py -m twine upload dist/*` in `repos/solver` — the dist there is
> byte-identical to the bundled wheel), followed by the usual
> PythonAnywhere console pass. The other leftover: the prune of
> superseded wheels (0.5.15–0.5.18) on the install host —
> interactive, Roberto's to type.

---

## #131 — the Numerical Solver restricts where it looks — done, deployed

**Done 28 Aug 2026, server repo only (eqsheet.py + eqsheet.html);
the cPanel sites deployed the same morning, PythonAnywhere on
Roberto's next console pass (pull + Reload, no pip).** Roberto:
for each unknown, an option to restrict the search space —
Unrestricted, Positive, Negative, or a Range from/to. Each unknown's
row now carries a **Restriction** menu; the range's two ends read in
the row's SI prefix, like the guess. A restricted solve goes through
SciPy's `least_squares` with bounds (MINPACK's hybr takes none;
unrestricted solves keep it, untouched), and a square restricted
system is judged by its residual, so a root outside the restriction
reports "no solution found under the restrictions" instead of a
boundary minimum posing as one. A guess outside its restriction is
moved to a genuinely *interior* start — reflected across the bound,
or 10% inside a range — never onto the boundary itself, where trf
nudges ~1e-10 inward and reports convergence without moving
(measured). In AC the menu applies to Real only / Imag only unknowns
and greys out on Complex ones: a restriction is a statement about one
real scalar, and a complex value has no sign. Verified through the
API (both x² = 4 roots selectable by sign, a range picking one root
of a two-unknown system, the no-solution and empty-range messages)
and through the page itself. The same session made the sheet accept
Python keywords (`is`) as variable names — the 0.5.19 shielding,
ported to the sheet's own parser.

---

## #130 — the op-amp's + and − match the source's polarity marks — done, deployed

**Done 28 Aug 2026, solver 0.5.18.** Roberto: the signs at the
op-amp's input pins should match the voltage source's polarity marks
in line thickness and size. They were 13px *text* glyphs (filled from
the label font); the source's marks are stroked 3.5px arms at the
page's 1.7px stroke. Both now draw through one helper
(`_sign_mark` in `repos/solver/symbulator/schematic.py`), so they are
identical by construction and cannot drift apart. Verified across all
322 tutorial circuits with `server/tools/review_schematics.py`.

---

## #129 — the [ T O O L S ] group heading — done and deployed

Same `.group-h` style as INPUTS and OUTPUTS, brackets and spaced
letters included, above the Mini-Tools card — so Mini-Tools, Plot and
Explore numerically read as the tools group. Measured identical in
computed style to the other two headings.

## #128 — Circuit Description and Analysis & Settings split — done and deployed

The one card that held both is two cards now, each its own
collapsible, both open by default. Nothing in the JS referenced the
old container; verified with a live solve after the split, and
build_local's coupling checks pass.

## #127 — mathematics set as mathematics — done and deployed

Roberto asked that math given as text be pretty-printed, centered, in
a distinctive font. KaTeX was wired into learn all along; what changed:
`{{o:...}}` values that parse to symbolic SymPy expressions render as
mathematics (19 sites, source text untouched so the originals checker
and harness still read answers as printed; `\ansmath` joins
symbulator.cls for print); 52 bare-text answer paragraphs in lesson 6
— the calculator's `{ 6e^-4t , ... }` lists — became `$$` display
blocks, typography only, with the two longest split across aligned
lines after they overflowed the PDF margin by 180pt (worst overfull is
now a pre-existing 32pt chapter title). Verified on the live page (52
of 52 blocks and 18 of 18 inline answers KaTeX-rendered, zero raw) and
by opening the PDF (page 238: Figure 5.38's centered answers and
in-sentence fractions in the answer colour). Deliberately not
converted, awaiting Roberto's ruling: bold set-answers inside
sentences ("The answer, **{12,4,3}**, is correct").

## #126 — the mobile pass — done and deployed

All three properties audited at 375×812 by measurement. Fixed: the
Numerical Solver's variable table was clipped by overflow:hidden (the
Value/guess and SI Prefix columns unreachable on a phone — it scrolls
sideways now); every input on both app pages is 16px at ≤520px, the
size below which iOS Safari zooms the page on focus; the Built-in
Examples panel ran 13px off screen (clamped, scrolls inside); learn's
version menu opened 128px off a phone's screen (it hangs from the
right edge below 40rem now, measured 74..314 after). The landing page
and the app's results area passed as they stood.

---

> **Deployed and verified, 27 Aug 2026 (fourth release that day — the
> evening batch).** Build `2026-08-27 11:15 UTC`, solver **0.5.15**
> (the impulse fix, published to PyPI that evening, hashes verified),
> cache **v69**. It carries **#119–#125**: the v9 documentation
> review's A–H fixes, the solver's second and third feedback rounds
> (#120, #122), β/γ in the whitelist (#121), the two new plot types
> (#123), the TR/FD handovers to the Numerical Solver (#124) and the
> Run button carrying its own status (#125).
>
> Measured, not eyeballed:
>
> 1. `https://symbulator.pythonanywhere.com/healthz` -- `build` and
>    `build_on_disk` both `2026-08-27 11:15 UTC`, `needs_reload:
>    false`, `solver: 0.5.15`. Pulled, pip-upgraded and reloaded by
>    Roberto. A live `/api/solve` of `e,1,0,10*delta(t):r1,1,0,1` in TR
>    answered `v_1 = 10*DiracDelta(t)` with no eqsheet payload — the
>    impulse fix and the delta gate, on the real server.
> 2. `https://install.symbulator.com/` -- 12 files uploaded (45 staged
>    from the new ZIP; 33 identical), all five verify_files
>    hash-matched. Loaded in a browser: footer `2026-08-27 11:15 UTC`,
>    four Plot types in the menu, and a real Pyodide solve of the
>    impulse circuit on the bundled 0.5.15 wheel answered `10 δ(t)`
>    with the button cycling Run → Solving… → Solved!.
> 3. `https://symbulator.com/9/local.zip` -- 17,533,902 bytes,
>    hash-verified against `repos/local/local.zip` after upload.
> 4. `https://learn.symbulator.com` -- 22 files uploaded including the
>    three rebuilt PDFs (320/303/355 pages), 914 identical, all
>    verify checks passed; the v9 lesson-bode page serves the new
>    "When you have H(s) itself" section and the lesson-fd page the
>    restored curly-bracket shorthand.
> 5. `symbulator.com` (landing) untouched and still current.
>    **All five sites are current.** The stale `symbulator-0.5.14`
>    wheel on the install host awaits Roberto's `--prune`.
>
> Every build re-stamps, so these figures hold only until the next one.

---

## #118 — Roberto's feedback round on #117 and the app — done and deployed

**27 Aug 2026, twenty-eight numbered items of feedback taken live in one
sitting; built as one release.** The user-facing name is now the
**Numerical Solver** — `/eqsheet/`, `eqsheet.py` and the other file
names stay as internal handles, the way a numbered item keeps its
number.

**On the solver page:** dark mode (same toggle, icons, `data-theme`
attribute and `symbulator-theme` storage key as the app — the pages
share an origin, so one choice carries to both); "Rule Sheet" →
"List of Equations" and "rule" → "equation" everywhere, including the
API messages; the new tagline; "×" → "SI Prefix", with a blank
dropdown entry replacing the dash; **every variable now defaults to
Unknown** — imported results arrive as guesses, so a sheet lands square
and re-solves as it stands; the Result column moved next to Variable;
Result text raised to the Value/guess size (the AC polar subline stays
smaller); a Known's Result shows its given value immediately; and the
**numerical-noise chop**: within each variable-type group (leading
letters of the name), a result more than 1e8 times smaller than the
group's largest magnitude displays as 0, plus an absolute 1e-18 floor
for groups that are all noise — display only, residuals stay raw.

**The system handover is now hybrid:** the paste box is gone; the URL
carries the payload as before, but past ~6 KB the button saves
`numerical_system.json` and opens the page empty, and the page's new
"Open a system file…" control reads it back — which also makes a system
keepable and re-openable, which the URL never was. Tested for real with
a 62-element ladder: the file saves, the page opens, the file loads,
the sheet solves.

**In the app:** the button is now **Numerical Solver** and lives in a
new **Explore numerically** card under Plot, active only when the solve
carried a payload (DC, or AC with numeric ω — fd/tr leave it inactive
rather than offering a dead button); the Input File card's three
buttons are equal-width on one line; the loaded-file note renders under
the "Entries in" dropdown, whose file title is now bold (appended as a
text node — titles are user-supplied); the Built-in Examples popup
always opens downward, above the banner (z-index 60) and scrolls —
flip-up, which hid it behind the bands, is gone; Circuit Description is
collapsible, open by default; the "Insert δ(t)" link is gone and the
syntax reference notes `delta(t)` = `δ(t)` instead (**`mu(t)` is NOT
noted: the parser does not accept it** — an alias was offered and
Roberto declined; he had been thinking of `u(t)`, which already
works); the Evaluate
label points at the "Useful SymPy functions" fold; the Conditions field
starts at the Evaluate field's height; "About this checkbox" → "About
'real solutions'"; "Download Output" → "Export Output", split into
"Export to .txt file" and "Export to SymPy" subheadings with the new
copy, and output files download as `.txt` instead of `.sym`.

Verified in the browser against the running app, item by item — button
widths and band heights measured, the popup's z-index and direction
checked, the dark preference confirmed to carry between the two pages,
the fd gate confirmed inactive, the file round trip run end to end.
Cache **v68**, build `2026-08-27 05:36 UTC`.

---

## #125 — The Run button carries its own status — done and deployed

**27 Aug 2026, Roberto's idea, shaped together.** "Run Symbulator" →
"Solving…" (disabled) while busy → "Solved!" until any input
invalidates the answers, at which point the freshness tracker reverts
the label — the button honestly reflects whether there is something
new to run. Error text stays in the line beside it ("No solution
found." and the error card), because a button cannot hold a sentence
and stay a button; the redundant "Solving…"/"Solved!" in that line are
gone. Verified in the browser: all four states, including the revert
on an edited description and the error path.

---

## #124 — TR and FD reach the Numerical Solver — done and deployed

**27 Aug 2026, Roberto's two ideas.** The Explore numerically card now
comes on for all four domains; each crosses in the shape that survives:

- **FD** hands over its stamped system — it is algebraic in s — in
  complex mode, with `s` arriving as a **Known** complex variable
  (j by default). Move `s` around the plane and re-solve: verified in
  the page, s = j·1000 on the 1 kΩ / 1 µF divider gives
  500 − j500 mV, the corner exactly.
- **TR**'s system is differential and cannot cross, so its *answers*
  cross instead — one equation per solved expression, `t` arriving
  **Known** at 0. Set `t` and read every waveform at that instant
  (verified: 503.415 mV at t = 0.7 for 1 − e^−t), or flip an answer
  Known and `t` Unknown and the sheet finds when the waveform gets
  there (verified: t = ln 2 for v2 = 0.5). Answers containing
  delta(t) are left out by name in a `#` comment the sheet shows but
  does not parse.

Under the hood: the payload contract grew an optional `known` field
({"t": 0.0} real, {"s": [0.0, 1.0]} complex) the page applies after
the arrive-Unknown results; the sheet's DC parser learned `u(...)`,
the unit step with u(0) = 1, joined to the namespace only when the
text actually calls it, so a plain variable named `u` still works;
and a bare `s` no longer gets a guessed VA unit — a lone `s` is the
Laplace variable, never an apparent power.

Two findings along the way, both fixed or flagged:

- **MINPACK's hybr reports "did not converge" on systems it solved
  exactly** — a linear or explicit system lands in one Newton step and
  the trust-region bookkeeping sees ten iterations of no improvement
  on a residual that is already zero. TR handovers are all explicit
  assignments and hit this every time. The sheet now judges success by
  the residual itself when the flag disagrees.
- **Solver-level finding, fixed the same day as 0.5.15:** with
  symbulator 0.5.14 a TR answer whose true value was an impulse came
  back as its s-domain constant (`tr("e,1,0,delta(t):r1,1,0,1")`
  reported `v_1 = 1`, not `delta(t)`) — a 10 V·s impulse printed
  identically to a 10 V step. Roberto asked for the fix; 0.5.15
  (published 27 Aug 2026, hashes verified against PyPI) transforms
  s-free circuit answers to `expr*DiracDelta(t)` while expert-mode
  scalars and dependent-source echoes still pass through, judged by
  provenance instead of shape. 223 solver tests pass; all 60 tutorial
  TR entries re-swept — only the two impulse problems' unprinted
  answers changed. The payload's delta skip now fires for real:
  impulse-bearing answers are named in the `#` comment, and a circuit
  whose every answer is an impulse produces no payload at all. The
  wheel pins (build_local.py, sw.js, vendor/, requirements.txt) all
  moved to 0.5.15 and ride the pending batch.

Server-hosted page plus shared payload builder; the offline builds
pick the payload up through `symbulator_ui` and hand it to the same
hosted page, so nothing offline-specific changed beyond the template.

---

## #123 — Two new plot types — done and deployed

**27 Aug 2026, Roberto's request, resolving the documentation review's
A7.** The Plot card's type menu grows from two entries to four:

- **Bode plot of a transfer function H(s).** Type H(s) directly —
  `100/(s^2 + 10*s + 100)` — no circuit involved; the Circuit
  Description is ignored for this type. The expression takes the same
  shorthand a circuit value does (`^`, implied multiplication, `1'k`)
  and must be numeric apart from `s`; a stray symbol is refused by
  name. This is what makes Lesson 11's five practice problems (which
  hand the reader an H(s) with no circuit) followable in version 9 —
  their v9 notes should now be rewritten to use it.
- **Plot a variable against another variable (DC).** `v2` against
  `rx`, when `rx` is a symbolic value in the circuit: solved once in
  DC with the sweep variable left symbolic, then sampled linearly
  across the range. Leftover symbols beyond the sweep variable are
  refused by name (pin them with a condition, or sweep them instead);
  an answer that doesn't involve the sweep variable plots flat with a
  note saying so. A pole inside the range becomes a gap in the line,
  not a broken response — non-finite samples cross as null and the
  chart skips them.

New `sweep_ui` and `bode_tf_ui` in `symbulator_ui.py`; `/api/plot` in
`app.py` and `plot()` in `bridge.py` grew the two tools and a
`xname` field; the template's Plot card gained the two menu entries, a
sweep-variable field, and per-type labels. The sweep variable is saved
and loaded with the circuit (`plotx:` in the file format,
`circuitbook.py`).

Found and fixed in passing: the offline `bridge.plot` never expanded
the Define box, so an offline plot of a circuit leaning on Defines
failed on symbols the solve had accepted — it now mirrors the server
route.

Verified through both front ends by measurement: 24 route-level checks
(values against hand-computed answers, error wording, the pole-gap
null, the old tools unregressed) plus the bridge path with and without
defines. Not yet built or deployed — rides the pending batch with
#120–#122.

---

## #122 — Numerical Solver: guessed units and Interactive Mode — done and deployed

**27 Aug 2026, Roberto's third solver round, two features.** Results
now carry a unit guessed from the variable's first letter, run
together with the SI prefix the way it is read — `-4 mA`, `12 V`,
`51.46 Ω`. Only the electrically confident letters guess (v e → V,
i j → A, p → W, r z → Ω, s → VA, c → F, l → H, g → S); ambiguous ones
guess nothing, so the default sheet's `T = T0 + P2*Rth` does not come
back in seconds.

And an **Interactive Mode** checkbox beside Solve. Unchecked, nothing
changes. Checked, the sheet *tries* to solve half a second after any
change settles — a value typed, a Known/Unknown flip, a prefix change,
an equation ticked or edited (edits re-parse first, on a slightly
longer settle, so half-typed lines don't thrash) — with a busy guard
so solves never overlap. Verified in the browser: flip `v1` to Known,
type 24, and `v2` reads 8 V with no button pressed; type a new
equation `q = v1*3` into the box and `q = 72` appears on its own.

Server-hosted page only — no offline rebuild involved.

---

## #121 — β and γ join the description whitelist — done and deployed

Found by the documentation's C/E pass on 27 Aug 2026: the 2023 pages
write symbolic circuits with Greek values (`β*irb`, `vγ`), the engine
reads the glyphs fine, and µ and δ were already allowed through
`symbulator_ui._ALLOWED` for exactly this reason — but β and γ were
not, so the restored panels failed validation with "characters that
aren't used in Symbulator syntax". Both are now in the whitelist (and
`_ALLOWED_EQ`). The lesson example files also moved to the
calculator's own notation — `u(t)`, `δ(t)`, `2e^(-4t)`, SI shorthand
in expert equations — all verified equivalent by measurement, and the
touched lessons re-swept clean.

---

## #120 — Numerical Solver, Roberto's second feedback round — done and deployed

**27 Aug 2026, five items.** The solver now speaks sans-underscore:
the payload built in `symbulator_ui.solve_ui` strips underscores from
every Symbulator-defined name — `v_1` arrives as `v1`, `i_r1` as
`ir1` — in the equations, the result keys, and the expert extras
(renamed longest-first so `i_r12` cannot be half-eaten by `i_r1`).
`tools/eqsheet_export.py` matches. The noise chop groups by first
letter accordingly, which is also what Roberto's original per-type
spec said ("names that start with v… with i").

On the page: every new variable — imported or hand-typed — starts
Unknown with a guess prepopulated to **0**, and an empty guess field
is read as 0 when Solve is pressed (a Known still insists on a
value). A solved row's result now survives an SI-prefix change — the
solution is kept per variable in base units, chopped, and re-scaled
into whatever prefix the menu says, cleared only when the equations
change under it. And a solved variable whose prefix menu is blank
gets the most suitable prefix picked *in the menu itself*, matching
the app's own SI style — 0.004 arrives as 4 m with the dropdown on m.
(Roberto's threshold sentence read "smaller than 1E-3 or
equal-or-larger than 1E-4"; the built rule is the app's always-pick
autoPre, under which 0.5 shows 500 m and 1200 shows 1.2 k. If he
meant a window that leaves those plain, it is a three-line change.)

Verified in the browser against the running app: import lands
`ie, ir1, ir2, v1, v2` all Unknown with the solved values as guesses;
blanking a guess and solving assumes 0; flipping `v1` Known echoes 12;
currents solve to **4 m** with the dropdown set; switching that row to
µ re-displays **4000 µ**, back to blank **0.004**; a hand-typed
`q = v1*2` arrives Unknown with guess 0; re-parsing clears stale
results. Lesson 1 sweep re-run as a smoke test: 0 problems.

**Deploy state:** committed and built (cache **v69**); the server
needs Roberto's step — `git pull`, **Reload**, no pip — and the
offline pair deploys after it.

---

## #117 — EqSheet, the what-if solver, integrated — done and deployed

**Built standalone in a separate session; integrated 27 Aug 2026.**
EqSheet is a TK!Solver/SolveSys-style numerical solver: a Rule Sheet of
equations, a Variable Sheet where each variable is Known or Unknown, and
SciPy root-finding on the residuals (DC real / AC phasor modes). It is
mounted on the Flask app at
`https://symbulator.pythonanywhere.com/eqsheet/` — `repos/server/eqsheet.py`
(a Blueprint; its `/api/solve` must not collide with the app's own),
`repos/server/templates/eqsheet.html` (the page), `EQSHEET.md` (user
docs), `tools/eqsheet_export.py` (the reference implementation of the
import contract).

**The interface side.** After a DC solve, or an AC solve with numeric ω,
the Download Output card offers **What if…** beside Export to SymPy: it
opens EqSheet in a new tab with the solved circuit's stamped equation
system in the Rule Sheet and every numeric answer as a Known, via a
`?import=` base64url payload. The payload is built at solve time in
`symbulator_ui.solve_ui` (both front ends get it; app.py names the
`eqsheet` key in its hand-enumerated response, the bridge passes it
through). fd and tr carry no payload and the button stays disabled —
their answers are expressions, and EqSheet is a numerical tool. The
handover's claim that expert-mode extras "come along for free" was wrong
for this code path — `solve_ui` re-stamps a Circuit without them — so
extras and conditions are appended to the payload explicitly, through
`expand_shorthand` (a reader may have typed `2'k`; EqSheet reads plain
SymPy).

**Decisions taken** (the handover delegated them): mounted as a path on
the existing app rather than a subdomain, so deploying stays `git pull`
+ Reload with no new PythonAnywhere config; the button ships in the
offline builds too, as an outward link like Documentation — EqSheet
needs SciPy and is server-hosted only, and its URL is pinned absolute in
the shared script. The page carries the shared two-band banner with
`banner.css` inlined verbatim between the same guarded markers as
index.html, and `build_local.py`'s `check_banner` now validates **both**
templates (verified by deliberately drifting one: the build refuses).
The subbar's DC/AC toggle is pinned to the ribbon's standard 2.5rem
control height, so the bands measure the same as the app's — topbar
148.8, subbar 61.6, measured side by side, not eyeballed. No dark mode
yet; if someone asks, follow the tokens' three-part pattern and keep the
navy band navy.

**Verified by running** (test client + the real page in a browser):
DC divider `e1,1,0,12:r1,1,2,2'k:r2,2,0,1'k` → button → sheet arrives
with 5 rules ticked and every value Known; untick the source rule, flip
`v_1` to Unknown → 12.0 comes back. The RL divider at ω=1000 arrives
with `v_2 = [5, 5]` and re-solves to 5+j5 with every variable flipped to
Unknown. An expert-mode solve (`v_2 = 2`, unknown `vs`) carries the
extra equation and the solved `vs = 6` as a Known. fd, tr and
symbolic-ω AC all return `eqsheet: null`. The payload survives the
base64url round-trip (371 chars for the divider).

**Deploy state:** live on all five sites, 27 Aug 2026 — server first
(Roberto: `git pull`, `pip install -r requirements.txt` for the new
numpy and scipy, **Reload**), then the offline pair, in that order
because their What if… button points at the server-hosted page. The
header banner above carries the measurements.

---


## Found building the tutorial's example input files, 26 Aug 2026

Written up from the documentation side; the documentation findings from the
same pass are in `Documentation/NEXT_DOCS.md`.

---

## #116 — #59's fix does not reach the Flask server's `/api/solve` — fixed

**Found 27 Aug 2026 while verifying 0.5.14 on the live server; fixed the
same day.** Where: the `desc` re-emission in `repos/server/app.py`'s
`/api/solve` — **and, it turned out, the identical re-emission in
`repos/local/bridge.py`**, see the closing note below.

#59 made an error quote what the reader typed instead of the machine's
rewrite of it, and that works — in the solver, and in the offline builds.
It does **not** work through `symbulator.pythonanywhere.com`:

    typed  rx,1,0,rx[1'k]
    local  Could not read the value 'rx[1'k]': a name is being used ...
    live   Could not read the value 'rxpr(1'k)': a name is being used ...

`rxpr(1'k)` is half-rewritten: the brackets have become `pr(`, the SI
prefix has not. It comes from `/api/solve` rebuilding the description
before solving it:

    desc = ":".join(e.name + "," + ",".join(e.fields) for e in elements)

`elements` there was parsed with `expand_si=False`, which is deliberate --
it keeps `4.7'M` as typed for the copy the reader is shown. But the
**bracket rewrite is unconditional** (it has to be: `_split_fields` cannot
tell the shortcut's inner commas from an element's own field commas), so
`e.fields` already reads `rxpr(1'k)`. The original `[...]` form is gone
one layer above the solver, and #59's machinery can only quote what it is
handed.

**Why the offline builds are fine.** `bridge.py` calls `symbulator_ui`
directly with the description as typed; there is no re-emission step.
Verified: the same input through `solve_ui` locally gives `rx[1'k]`.

**Not all of #59 is affected.** The missing-bracket case is correct on the
server too, because it raises inside `expand_shorthand` during that very
parse, before anything is re-emitted. Only the paths that survive to the
solve are wrong, and only in which string they quote -- nothing is
mis-solved.

**Two ways to fix it.** Rebuild `desc_used` from `Element.raw_fields`
(added in 0.5.14 for exactly this kind of recovery) rather than from
`fields`; or pass the untouched posted description alongside, and let
`solve_ui` hand it to the solver as the `original`. The second is smaller
and does not depend on the two field lists lining up -- which, as #59
found, they do not when a bracket is unbalanced.

**How it was actually fixed, 27 Aug 2026.** The first way, because the
second is not smaller after all: `solve_ui` has no channel to hand an
`original` to the solver -- `ex`/`dc`/`ac`/`fd`/`tr` take only the
description string, so that route means a solver API change and a PyPI
release for a message-wording bug. And the first way's stated weakness
is moot at the point of the fix: an unbalanced bracket raises inside
`parse_circuit`, *before* the re-emission line, so it can never reach
it. Two edits, made identically in `app.py` and `bridge.py`:

- the re-emission prefers each element's `raw_fields` (the fields as
  typed, which at that point already carry `normalise_imaginary` and
  the Define expansion) and falls back to `fields` where `raw_fields`
  is empty -- which by then can only mean "nothing was rewritten"
  (identical) or the multi-comma `[a,b]` case, where the typed text
  splits into a different number of fields and cannot be lined up
  (unchanged behaviour, same as the solver's own recovery);
- the ambiguous-suffix rewrite mirrors its explicit spelling into
  `raw_fields` too, so resolving `2k` to `2'k` is not lost when the
  description is rebuilt from the typed copy.

A side effect worth having: `desc_used` now echoes rewritten-but-
alignable fields as typed, so a reader who wrote `[2'k]` gets `[2'k]`
back, not `pr(2'k)`. The multi-comma `[1'k,2'k]` still echoes as
`pr(1'k,2'k)` -- that is the unrecoverable case above.

**The closing surprise: the offline builds had the same bug.** This
entry originally said `bridge.py` "calls symbulator_ui directly with the
description as typed; there is no re-emission step". That was verified
by calling `solve_ui` directly -- which bypasses `bridge.solve`, where
the same always-echo re-emission had been sitting since 21 Aug 2026
(`a1dc288`, the same change that added it to `app.py`). Measured before
the fix, `bridge.solve` gave the identical wrong `rxpr(1'k)`. So the
deployed offline builds (v65) were wrong too, and the fix ships to all
five sites, not just the server.

Measured after the fix, through both `bridge.solve` and a test client on
`/api/solve`, identically:

| typed | now |
|---|---|
| `r1,1,0,[1'k,2'k` | names the missing bracket, as typed |
| `rx,1,0,rx[1'k]` | quotes `rx[1'k]` |
| `r1,1,0,1'Q` | names the value, as typed |
| `r1,1,0,[1'k,2'k]` | solves; echoes `pr(1'k,2'k)` as before |
| `r1,1,0,[2'k]` | solves; echoes `[2'k]` as typed |
| `2k` + choice si / var | solves as 2'k / 2*k -- the choice survives |
| `e1,1,0,5*i` in AC | normalised to `5j` with the note, as before |

Solver untouched: 216 tests pass unchanged, and the server needs no
`pip install --upgrade` -- a `git pull` and **Reload** is the whole
server deploy.

---

## #105 — A symbolic value sharing a name with a SymPy function broke Evaluate — fixed

`rf` is a natural name for a feedback resistor and Lesson 5 uses it four
times. It is also `sympy.rf`, the rising factorial. Solving was never
affected -- the answers were right and displayed correctly, `vo =
-rf*vi/r1` as the book has it -- but asking **Evaluate** for anything then
failed:

    vo  ->  bad operand type for unary -: 'FunctionClass'

One line did it. `_alias_mapping` re-parsed each solved answer with bare
`sp.sympify`, which reads against the whole of SymPy, so any answer
carrying such a name came back as the function rather than the symbol.
`im`, `beta`, `gamma`, `zeta`, `N`, `S`, `O` and `E` were all in the same
trap -- `beta` and `re1` appear together in Lesson 4's TR5 Exercise 4-7.

**Fixed the same way `re = 12000` was**, one layer further in: a new
`_parse_answer()` reads answers through `safe_sympify`, which uses the
small allowed namespace, so every other identifier stays an ordinary
symbol. That fix rewrote *the names a reader types*; this one covers *the
values already solved*.

The imaginary unit is handled by hand rather than by `safe_sympify`'s
domain flag, and that detail matters. These strings are SymPy's own output,
not anything a reader typed, and SymPy always prints the unit as a capital
`I` -- so a lowercase `i` here is a circuit symbol and nothing else. Lesson
6's impulse problem, whose source amplitude is called `i`, is exactly the
case the domain flag would have got wrong: it would have turned the
amplitude into the square root of minus one.

Measured after the change:

| | |
|---|---|
| `vo` on the rf circuit | `-rf*vi/r1` |
| `vo/vi` | `-rf/r1` |
| `rji` with `beta` and `re1` | `re1*(beta + 1)` |
| `rei` with Greek mu and `rf` | `rf*(mu + 1)` |
| AC complex power, `-pe` | `7650/61` |
| TR with an amplitude called `i` | `i*exp(-t/(c*r))/c`, still a symbol |
| FD `s2t(vo)` round trip | unchanged |

All eighteen lesson files re-verified against the answers their chapters
print, with nothing outstanding.

`expand(vo)` still fails on these circuits, but for the unrelated reason in
#104: there is no `expand` in the evaluator's namespace at all.

---

## #107 — Thevenin of an op-amp output failed outright where the calculator gave half — fixed

Lesson 5, Bo2's Drill Exercise 3.11. The chapter describes a partial
success: the script "found the Thévenin voltage, but could not find the
Norton current", leaving you holding `vth`. Version 9 refuses the whole
run:

    Could not solve the system of equations. If you used exact numeric
    values, try again using symbolic values only.

The reason is sound -- an ideal op amp has zero output resistance, so the
short-circuit round divides by zero -- but version 9 gives up on both
rounds where the calculator kept the first.

A plain solve gets there: the Thevenin voltage of an unloaded output is the
open-circuit node voltage, and `v3` comes back as `vs*(r1 + r2)/r1`, the
book's answer exactly. The example entry does that.

**Settled by measuring the short rather than assuming it** (solver 0.5.13,
27 Aug 2026). Roberto's proposal was to report `vth` and say the second
round failed, guessing that the Norton current runs away. It does — and it
can be shown rather than guessed, which gives the whole answer instead of
half.

A short is a resistance of zero. So when the short-circuit round will not
solve, `th()` now puts a resistance `x_test` across the terminals instead
and takes the current's limit as `x_test` falls to zero:

    open circuit  ->  v_3 = vs*(r1 + r2)/r1
    short         ->  no solution
    resistance x  ->  i = vs*(r1 + r2)/(r1*x),  |i| -> oo as x -> 0+

Unbounded means `ino` is infinite and `req` is 0, reported as results. The
same routine returns 17.6 on an ordinary divider whose short happens to be
awkward, so it is a generalisation of the old path rather than a special
case bolted beside it. `TheveninResult.note` says which happened and is
empty on an ordinary run.

Two things worth remembering about it:

The infinity test is `has(oo, zoo)`, not `is_infinite`. With a symbolic
source the limit comes back as `oo*sign(Abs(vs*(r1 + r2)/r1))`, whose
`is_infinite` is `None` — and that symbolic case is the one the whole
change exists for.

The probe's symbol is matched **by name** out of the expression's
`free_symbols`. A SymPy symbol carries its assumptions in its identity, so
`Symbol("x_test", positive=True)` is a different symbol from the plain one
the parser builds, and a limit taken in the wrong one silently finds
nothing to do.

Only if the limit cannot settle it either does the call still fail, and the
message now carries the open-circuit voltage, so the half that was found is
never thrown away.

**What this does not touch.** Bo2's Example 3.11 and Drill Exercise 3.13 in
Lesson 4, the two "tricky" problems the chapter *teaches* as failures, fail
in the **first** round, before any of this. Both still print exactly the
refusal the chapter quotes, and `req = (9x-35)/(4(x-3))` is unchanged. The
one caveat is in `th()`'s docstring: an expert equation that pins an element
value from a measurement no longer even accidentally trips the refusal it
used to, since a raise now falls through to the probe.

Lesson 5's example entry runs the Thévenin tool now instead of working
around it with a plain solve, and version 9's half of the chapter passage
was rewritten to show `req = 0` as an answer rather than assert it.

**Versions 7 and 8 keep their wording, by Roberto's decision on 27 Aug
2026.** The rat he smelled — the chapter asserting a Thévenin resistance of
0Ω without ever evaluating it — is real, but it is a fair account of what
the calculator did: it reported the Thevenin voltage and could not find the
Norton current. Only version 9 goes further, and only version 9 says so.
Closed.

---

## #110 — "Limit the results to save time" emptied the results — fixed

Lesson 6 tells a version 9 reader to tick it and list `vc`. Doing that gave
a completely empty **Results** -- no error, no note, for a circuit that
solves fine without the tick.

**Two faults, and the silent one did the damage.**

`tr()` inverse-Laplaces only the keys it is handed and skips anything it
does not recognise without a word (`laplace.py:346`). So a name it could
not provide produced a blank page rather than a complaint.

And one of the names the documentation asks for it can *never* provide. A
transient solve answers in element currents and node voltages only:

    tr(desc)  ->  i_c, i_r, v_1

An element's voltage drop is derived afterwards, in the front end, from the
two node voltages it spans -- so `v_c` is not a solver key at all, and no
spelling of it could have worked.

**Both fixed in `symbulator_ui.py`,** which is where the knowledge lives,
rather than in the solver -- that would have meant a release to PyPI for
something the front end can settle on its own. `_wanted_solver_keys()`
translates the casual spelling the way Evaluate and Solve already do, turns
a request for an element's voltage drop into the node voltages it is built
from (inverse Laplace is linear, so transforming those and subtracting
gives the same answer for the same work), and hands back anything left
over. `solve_ui` refuses those by name instead of asking for them, so the
solver's silent skip is now unreachable from the interface.

Measured after the change, on Lesson 6's Drill Exercise 5.11 circuit:

| asked for | got |
|---|---|
| `vc` | `v_c` — the exact expression the unlimited solve gives |
| `v_c` | the same |
| `il` | `i_l` |
| `v_1` | `v_1`, and `v_r3`/`v_r6` derived from it |
| `p_r3` | refused: there are no powers in TR |
| a typo | refused, naming it |

**The feature earns its keep.** On Professor Boulet's problem, the heaviest
in the tutorial: 14.5 s for all fourteen answers, 10.2 s for the two the
question asks about. The two Lesson 6 entries that had to give it up use it
again.

**One correction to the original write-up.** It said the field does nothing
in DC. That is true of the API -- `dc()` has no `variables` argument -- but
not something a reader can reach: `index.html:1775` already shows the field
only when the analysis is TR *and* the tool is Solve circuit, which is
exactly where Roberto intended it. The interface was right; the write-up
was not.

---

## #112 — The polar-phasor setting was not saved with a circuit — fixed

The front end saved it (`polar: $('polarPhasors').checked`) and restored it,
but `circuitbook.py` had no `polar` key, so it was dropped on the way into
the file and every reload came back rectangular with nothing to say why.
`rms`, the other AC-only display setting beside it, was handled correctly.

**Fixed**, mirroring `rms`: the key in `_KEYS`, `polar` in `_BOOL_FIELDS`,
and the value written whenever the analysis is AC.

Lessons 7, 9 and 10 depend on it -- their chapters quote nearly every
answer as an amplitude and an angle.

---

## #114 — The equivalent tools refused FD — fixed

Lesson 13's AS7 Example 19.7 and Practice Problem 19.7 both say to choose
*g — inverse hybrid* in **FD**, and both were refused:

    Thevenin / impedance / two-port tools work in DC or AC only.

**The solver never had that restriction.** `er()` answers plainly when asked
for a domain it does not know -- *"domain must be 'dc', 'ac', or 'fd'"* --
and `port()` in FD returns exactly the four parameters the chapter prints.
All three tools take all three domains, as they were designed to. The
front end was simply stricter than the design, in three places:

  - `app.py`, the domain check before the tool runs
  - `bridge.py`, the same check for the offline build
  - `index.html`, which disabled *fd* and *tr* in the analysis menu
    whenever an equivalent was chosen

All three now allow DC, AC and FD, and refuse only the time domain -- which
the solver refuses too, and rightly: an equivalent is a statement about a
circuit at a frequency, and TR is the one analysis with no such thing.

Lesson 13's two entries use FD as the chapter says, and both give the
printed answers. The s-domain-impedance workaround they carried is gone.

---

## #115 — The Plot and Bode cards could not plot an element's voltage drop — fixed

Found while checking the two Lesson 6 plot entries, which did not work.

`time_samples()` and `bode_samples()` each ask the solver for one key and
read it straight back, so they could plot what the solver answers in --
element currents and node voltages -- and nothing else. An element's
voltage drop is derived afterwards, in the front end, from the two nodes it
spans. So neither `vc` nor `v_c` could be plotted, and Lesson 6 asks for
both: Bo2's Example 6.5 says to plot `vc`, and Bo2's Example 6.6 is a plot
of `vl` -- the inductor swinging to nearly four thousand volts, which is
the whole point of that problem.

It also left the app inconsistent with itself, once #110 was fixed:
**Settings** accepted `vc` and the **Plot** card did not.

**Fixed the same way #110 was:** the request is expanded into the node
voltages it is built from and the subtraction done afterwards. Sound
because both transforms are linear -- the difference of the transforms is
the transform of the difference -- so the curve is identical to what a
direct transform would give, for the same work. It lives in
`symbulator_ui.py` rather than the solver, since the derived name is this
layer's invention and the solver has no reason to know it.

Measured after the change:

| | |
|---|---|
| `vc`, `v_c`, `v_3` on Example 6.5 | all plot, all peak 0.4379 -- the same curve by three names |
| `vl` on Example 6.6 | **3990.6 V at t = 1.57 ms** |
| `vc1` vs `v_2` on the Bode RC | identical, -0.02 dB to -55.96 dB |
| a misspelling | still refused, naming it |

The chapter's own words for Example 6.6 are *"around t = 1.57 ms, the
voltage drop across the inductor is 3991 volts"* -- an answer that was
unreachable in version 9 until now. Both Lesson 6 entries plot what the
chapter plots.

---

## #97 — The two shared modules are copied by the build now, not by hand — shipped

**Done 26 Aug 2026, and in every release since 27 Aug.** `symbulator_ui.py` and
`circuitbook.py` are one file each, shared verbatim between the server and
the offline build. Nothing copied them and nothing compared them: the copy
happened when somebody remembered.

The history says so plainly -- a run of server commits each followed by a
separate "Carry the ... into the offline build" -- and
`stage_install_site.py` exists because those files once
"sat a full day out of date while every deploy reported success". Checked
for a mechanism before adding one: no git hooks, no CI, no workflows, no
scheduled task, and the only two mentions of the filenames anywhere are a
docstring and a line inside the *generated* JavaScript listing what the
offline page fetches at boot.

Same shape as the banner, and the same answer -- except that here the copy
can be *made* rather than checked, because `build_local.py` already
generates `index.html` into this repository from the server's template and
these are no different. So:

* `build_local.py` copies them on every build and reports which moved.
* `build_local.py --check` fails and names the file if either has drifted.
* `build_zip.py` already gated on that check, so the ZIP is covered for
  free; only its message needed widening, since the cause may now be a
  module rather than the page.

Verified both directions: drift introduced deliberately makes `--check`
exit 1 naming `circuitbook.py`, and the sync restores it byte-identical to
both the server's copy and its own previous state.

`bridge.py` is deliberately not among them -- it is the offline build's own
glue, with no server counterpart.


## #96 — A Conditions field on the Evaluate card (**done, deployed**)

**Accepted and built 26 Aug 2026.** Roberto's request: give **Evaluate** a
*Conditions* field, like **Solve** already has. It does the two things he
chose:

* `t = to` is a **substitution**, applied before the expression is
  evaluated -- the calculator's `vc|t=to`, which is what the box is mostly
  for. Verified in the browser against a real solve: `vc` with `t = to`
  reads `V - V*exp(-to/(c*r))`.
* `pr1 > 0` is an **assumption**, translated into the predicate `refine()`
  wants. That translation is the whole trick: `refine(sqrt(x**2), x > 0)`
  hands the expression straight back, while `refine(sqrt(x**2),
  Q.positive(x))` gives `x`. Verified both ways round -- `x > 0` gives `x`,
  `x < 0` gives `-x`, neither gives `sqrt(x**2)`.

An equality with anything but a single name on the left is refused, with a
message pointing at the Solve card, rather than quietly ignored: Evaluate
substitutes and formats, it does not solve.

Where it went, beyond the field itself:

* **The input file.** `evaluate_conditions`, one per line, in
  `circuitbook.py`'s `_MULTI` and in the writer beside `evaluate:`; the
  `inputsSnapshot()` / `applyCircuit()` pair; and the key list in the page's
  own Input File help. Named for its card, like `solve_conditions`, so it
  cannot collide with a circuit's Expert Mode `conditions` -- round-tripped
  through `format_book`/`parse_book` and confirmed the three stay apart.
* **The domain-sensitive inputs.** It posts `domain` with the rest, as
  Evaluate and Solve equations already did, so `{...}` keeps meaning what it
  means in FD and nothing else.
* `STALE_ON_CHANGE`, so editing it retires a fresh Evaluate result --
  checked in the browser, the button drops out of `is-current` on the first
  keystroke. The post-solve enable pass. "Clear all inputs". And the
  downloaded report, which now prints the conditions under the expression
  and only while both fields still hold what produced the result.

Guarded like the Solve card's box, not like an expression: `_ALLOWED` has no
`=`, `<` or `>` in it, so it was the wrong guard and rejected every
condition on the first try. `_ALLOWED_COND`, `_MAX_SOLVE_EQS`,
`MAX_EXTRA_LEN` and `_expand_and` are what the Solve card uses, and now what
this uses.

The offline build has it too: `bridge.py` reads the box, `build_local.py`
rewrites the new fetch, and `index.html` is regenerated and `--check` clean.

**Not deployed.** The chain when it goes: `build_local.py` →
`build_zip.py --assets ../../local` → `stage_install_site.py` →
`deploy_symbulator.py install` and `zip`, plus a `CACHE_VERSION` bump in
`sw.js`. PythonAnywhere is Roberto's to reload. The documentation's #89
becomes writable once it is live, and not before.


## #95 — There is no version 9 way to say `vc|t=to` (**done, deployed**)

**Fixed 26 Aug 2026.** `t = to` now works in the Solve card as well as in
Evaluate's new Conditions box.

**The first diagnosis was backwards and is worth recording as such.** The
note said a typed `t` was a plain `Symbol("t")` while the answers carried
the nonnegative one. The opposite is true: `_allowed_namespace` has bound
`t` to `symbulator.laplace.t` all along, so every box on the page has always
parsed `t` correctly. It is the **answers** that lose it. A solved answer
crosses to the browser as a string and is read back by `_alias_mapping` with
bare `sp.sympify`, which knows nothing of that namespace and makes a plain
`Symbol("t")`. Different symbol, `subs()` does nothing, nothing says so.

Two lines, once it was aimed at the right side:

* `_alias_mapping` canonicalises `t` as it re-reads each answer.
* `solveq_ui` built its unknowns as `sp.Symbol(u)`, so an unknown named `t`
  was a third, plain `t` that appeared in none of the equations and left the
  system unsolved. It canonicalises them too.

And `real_only` no longer re-declares a symbol that already carries an
assumption implying real -- doing so threw the nonnegative away and put the
mismatch back for exactly the circuits that needed it.

Measured after: `t = to` gives `x = V - V*exp(-to/(c*r))`, `t = 0` gives 0,
both with and without "real solutions only"; leaving `t` free is unchanged;
and the Solve card's own conditions still filter roots, `w**2 = 4` with
`w > 0` still coming back as just `2`.

The docs' `README.md` says this trap is about `Symbol("t", positive=True)`.
It is `nonnegative` -- laplace changed it deliberately, because DiracDelta
of a strictly positive argument evaluates to 0 and every impulse vanished.
Worth correcting there.


## #94 — A number glued to an answer name silently unbinds it (**done, deployed**)

**Fixed 26 Aug 2026.** `.2v1` and `3ir1` now bind, with no `*` and no
underscore, which is how both 2023 pages are written.

Implied multiplication was never the problem: `3t`, `2(a+b)`, `2e^(-2t)` and
`2ir1` were all read as products already. The problem was that
`_alias_pattern` refused to rewrite `v1` into `v_1` with a digit against it,
and ran before `si_prefix` made the multiplication explicit -- so by the time
the `*` arrived, `v1` was an ordinary symbol. The circuit then solved, in
terms of a variable the reader thought was a node voltage, and nothing
anywhere said so. With a current-controlled source it was worse:
`e,2,3,3ir1` in a two-port answered
`a11 = -30.0*x_test1/(3.0*ir1 - 20.0*x_test1)`, leaking the tool's own
internal probe names onto the page.

The pattern now consumes an optional number in front of the name and emits
the multiplication itself. Consumed rather than merely allowed, so the guard
still holds inside a name: in `x2v1` neither the number nor the name can
start, and nothing matches, which is right. Scientific notation is safe for
a different reason -- an alias is a quantity letter plus an element name,
and `e3` is not one.

Measured after: `.2v1`, `0.2v1`, `2v1`, `.2*v1` and `0.2v_1` all resolve;
HK5's Drill Problem 1-13 gives -2, 3, -8 and -0.5 from the panel as the
2023 page writes it. `.2 v1`, with a space, is still refused, unchanged.

**Still worth having:** nothing catches this class automatically. The docs'
`tools/check_v9_panels.py` asks only whether a panel is *read*, and these
were read perfectly. A check that a solved panel's answers carry no
unexpected free symbols would sit well beside it.


## #77 — TR read its sources in the s-domain (**done, deployed**)

**Settled 25 Aug 2026, in solver 0.5.5.** It was a port omission, not a
design choice, and the primary source proves it.

`tr()` called `fd()` and inverse-transformed the answers, but passed the
source values through untouched -- so they were read as s-domain
expressions. Every transient answer was one integration short: a plain
`12` gave the impulse response where the step response was meant,
plausible enough to pass a glance.

The evidence, in the order it got firmer:

1. Version 7's `.tig` is a plain zip; raw ASCII showed `s	2s` beside a
   `tool="tr"` test. Suggestive, and the technique is low-confidence.
2. Version 8's documentation agreed -- but Roberto pointed out it is an
   unfinished clone of version 7's and not evidence of intent.
3. `PROJECT_HISTORY.md`, bundled in `symbulator-project.skill`, recorded
   the omission at the time: the port skipped the forward transform
   "rather than auto-detecting and transforming time-domain expressions
   **the way the original did**", because the `lf\laplace` library was
   not in the source dump.
4. Version 8's actual source, decoded with `tnstools` (3DES in counter
   mode -- which is why the payload is not block-aligned, the detail that
   made it look like something other than encryption). `symbv8s5`:

       If betatool="tr" and inString("ej",kind) Then
         value depends on t     -> t2s(value)
         value is a constant    -> value/s
         refers to another answer -> left alone

0.5.5 restores exactly that. A controlled source is left alone because
its value is a relation, not a waveform; a value already written in `s`
is left alone too, which is what keeps every existing version 9
description working.

Verified before shipping: all twelve bundled examples answered
byte-identically under published 0.5.4 and the new build, and six
transient circuits now match answers derived by hand -- including AS7's
Example 16.1, whose answer is in print in both calculator versions.

Two things fell out of it. 0.5.3 had bound `t` in the parsing namespace to
`Symbol("t", positive=True)`, and SymPy evaluates `DiracDelta` of a
strictly positive argument to **zero** -- so impulse sources had been
silently erased. And 0.5.6 added the `{...}` shorthand, `symbv8si`'s
FD-only marker for a source written in time.

The decoded version 8 source is worth keeping: it turns "what did the
original do?" from inference into a grep.

---

## #75 — The lockup exists once, not once per tree (**done, deployed everywhere**)

**Done 23 Aug 2026.** Where: `server/templates/index.html` (commit `8585e70`),
`local/build_local.py` (`check_banner`).

`Documentation\design\banner.css` is now the only place the lockup is
stated. The app's header was renamed to the shared class names -- `.topbar`
wrapping `.topbar-inner`, `.header-flex` to `.header-brand`, `header h1` to
`.brand-name`, `header p` to `.brand-sub` -- and the file is inlined verbatim
into the template between `BEGIN/END banner.css` markers. Inlined rather than
linked because the offline ZIP cannot fetch a stylesheet from another tree.

The guard is the part that works. `check_banner()` in `build_local.py` compares
the inlined block against the source and stops the build if they differ, naming
the fix; it warns and carries on when `Documentation` is absent, so `repos/` alone
still produces a release. The app's own controls stay in the app, layered on top
exactly as the version picker is on `learn` and the nav links on the landing
page.

Left open, deliberately: the app's build now reads a file from a tree that is
**not under version control**. Moving `banner.css` into `repos/local` and having
the docs' `build.py` read it from there would invert that dependency. Worth
doing when `Documentation` becomes a repo; nothing breaks meanwhile.

> **Closed 28 Aug 2026** by doing exactly the inversion above (`Documentation`
> had become a repo on the 26th, which removed half the reason, but the
> commit-pinning half stood): the canonical is `banner.css` in this
> repository, `check_banner()` reads its own tree and fails hard instead of
> warning, and the docs' `build.py` copies the canonical for `learn` and
> checks the landing copy against it. Byte-identical move, so nothing needed
> redeploying; the current arrangement is described in the top-level
> `CLAUDE.md`.

## #74 — The app and the two websites are different shapes (**done, deployed**)

**Settled 23 Aug 2026, by the app adopting two bands.** The websites had been
changed to a two-band header -- `.topbar` carrying the lockup alone with no
keyline, `.subbar` beneath it carrying every control in a lighter navy
(`#2a4576`) and the 3px sky keyline closing the pair -- hours after the app had
been brought into line with the older single-band design. The app followed the
websites, which were the reference it had been asked to match, rather than the
websites reverting.

**Reopened 23 Aug 2026: the app took the file, not the shape.** Measured in a
browser at 1280 wide, the same viewport for all three properties:

| | symbulator.com | learn.symbulator.com | the app |
|---|---|---|---|
| `.topbar` | 149 | 149 | 149 |
| `.subbar` | 62 | 62 | **absent** |
| where the controls sit | subbar, left edge | subbar, left edge | **inside the lockup band, right** |
| keyline | on `.subbar` | on `.subbar` | on `.topbar`, via `:last-child` |

The lockup band itself matches to the pixel, which is what `check_banner()`
guards and why this passed unnoticed: the shared file styles `.subbar`, and the
app has no element with that class. `banner.css` even anticipates it -- the
`.topbar:last-child` rule that gives the app its keyline exists for a header
with no ribbon.

What was left to do was markup, not CSS: wrap the app's theme toggle in
`<div class="subbar"><div class="subbar-inner">`, in
`repos/server/templates/index.html`. The keyline then moves to the subbar on its
own, because `:last-child` stops matching.

**Closed 26 Aug 2026.** The markup is in and live, and this time measured
rather than read -- the item's own point being that a file check is not a
shape check. Both at 1280 wide, in a browser, against the deployed sites:

| | install.symbulator.com | learn.symbulator.com |
|---|---|---|
| `.topbar` height | 149 | 149 |
| `.topbar` bottom border | none | none |
| `.subbar` height | 62 | 62 |
| `.subbar` keyline | 3px `rgb(142,199,245)` | 3px `rgb(142,199,245)` |
| controls in the subbar | yes | yes |

Which is the table above with the "absent" filled in.

The drift itself is the lesson, and #75 is the answer to it -- but only for the
part a byte comparison can see. This happened twice in one day, in both
directions, while every session involved was being careful, because three files
each stated the lockup and nothing compared them. A file check is not a shape
check.

## #73 — Stale "several solutions" picker (**done, deployed everywhere**)

**Found by Roberto, 22 Aug 2026.** Where: `server/templates/index.html`,
`markStale()`.

Solve a circuit with two roots, then pick a different entry from the circuit
menu: the "2 solutions fit the circuit as described" line and its picker
stayed on screen, now describing a circuit no longer in the form.

The cause was where the reset lived, not what it did. `buildSolutionPicker({})`
was called from exactly two places -- the start of a solve, and
`clearResults()` -- so every *other* way of invalidating a solve left the
picker behind. It now happens inside `markStale('solve')`, which every such
path already goes through, including `applyCircuit()`, whose own comment
states the rule: *loading a circuit rewrites every field and fires no events
doing it, so nothing on screen describes these inputs any more*. The line and
the menu are part of "nothing on screen".

Verified: picker clears on loading another entry and on editing a field, and
survives switching between solutions, which marks the solve fresh rather than
stale.

## #72 — Clear-all button press nudge (**done, deployed everywhere**)

**Done 22 Aug 2026, deployed 23 Aug in the `09:25 UTC` build.** Where:
`server/templates/index.html`, commit `e4b95d7`; regenerated in
`local/index.html`, commit `2560acd`.

The button beside the Inputs heading is centred with a transform, and every
button on the site gets a 1px press nudge that is also a transform. A second
transform replaces the first rather than adding to it, and `:active` is the
more specific selector, so pressing the button discarded its centring and it
fell 20px -- half its own 37px height, plus the nudge -- gliding down and back
because `transform` is transitioned. Fixed by carrying both offsets together
as `translateY(calc(-50% + 1px))`, with the narrow-screen branch reset to the
plain nudge since the button is not centred there.

It was held back at the time as cosmetic, on the grounds that shipping it alone
costs a full three-site round, and folded into the next deploy that had a reason
to happen. Verified live: `translateY(calc(-50% + 1px))` is present in the page
served by `https://install.symbulator.com/` as well as in
`C:\Users\perez\Claude Symbulator\Application\v9\repos\local\index.html`.

---

## #59 — Bracket typos quoted the rewritten value, not what was typed — fixed

**Fixed in solver 0.5.14, 27 Aug 2026.** Accepted 23 Aug and carried until
there was a reason to cut a release.

Every value is rewritten before it is parsed: `expand_shorthand` turns
`[a,b]` into `pr(a,b)`, `expand_value` turns `1'k` into `1*10**3`, and only
then does `safe_sympify` call `check_expression_syntax`. That function
quoted the string it was handed, which by then was the machine's rewrite.

Three symptoms, three fixes:

**The rewrite was quoted back.** `safe_sympify` and
`check_expression_syntax` now take an `original` alongside the rewritten
text and quote the original. `Element` gained `raw_fields`, the fields as
typed, and the engine builds a rewritten-to-typed lookup in its constructor
so `_value` -- which receives a field's text and nothing else -- can
recover it.

**An unbalanced bracket is caught before the rewrite**, not after, because
after is too late: `_split_fields` does not respect `[...]`, which is
exactly why the bracket rewrite has to run on the whole element line first.
With one bracket missing, the typed text and the rewrite split into
*different numbers of fields*, so no field-by-field lookup can line them
up. The balance check is now the first thing `expand_shorthand` does:

    'r1,1,0,[1'k,2'k' is missing a closing bracket. A parallel
    combination is written [a,b], as in [1'k,2'k].

**A name used as a function says so.** `rx[1'k]` has balanced brackets, so
it rewrites into a call shape, passes the syntax gate -- calls of named
functions are legitimate -- and died in SymPy as `'Symbol' object is not
callable`, which named nothing at all. It now names the value.

It deliberately does **not** name the symbol in that case. The rewrite makes
`rx[1'k]` into `rxpr(...)`, so the culprit SymPy reports is `rxpr`, a name
the reader never typed; naming it is worse than naming nothing. The message
only names a symbol when the text was not rewritten.

Thrown in while there: an unrecognised unit prefix now names the value and
lists the prefixes that exist, rather than "Circuit description uses
shorthand that Symbulator does not recognize" with nothing to go on.

**What to watch.** The balance check runs on the echo path too
(`expand_si=False`, which the schematic and the ambiguity check use), so an
unbalanced bracket now raises where it used to be quietly rewritten. Both
surfaces were checked: each reports the message rather than crashing. Four
tests cover it in `test_suffix.py`, including one asserting that correct
shorthand still solves -- a guard must not cost the feature it guards.

