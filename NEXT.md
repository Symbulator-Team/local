# Next build — accepted but not yet done

> **Deployed and verified, 28 Aug 2026 (three releases).** Cache
> **v71**, **v72**, then **v73**; solver **0.5.16**, **0.5.17**, then
> **0.5.18**. 0.5.16 is the schematic rework — the drawer reviewed
> against all 322 tutorial circuits (wires never cross element bodies,
> real crossings drawn as hops, junctions on node corners, values
> shown as typed, long values captioned below the drawing; see the
> solver CHANGELOG); 0.5.17 has the op-amp feedback wire leave the tip
> the way the triangle points; 0.5.18 closes #130 below. Between
> them, `banner.css` moved into this repository (#75's inversion — see
> the write-up below) and the review harness landed in
> `server/tools/review_schematics.py`. install + ZIP + learn + landing
> deployed and hash-verified; **PythonAnywhere pull + pip + Reload
> pending** (one console pass lands 0.5.18 directly). The prune of
> superseded wheels (0.5.15, 0.5.16, 0.5.17) on the install host is
> also pending — interactive, Roberto's to type.

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
same pass are in `Sym Docum/Documentation/NEXT_DOCS.md`.

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

`Sym Docum\Documentation\design\banner.css` is now the only place the lockup is
stated. The app's header was renamed to the shared class names -- `.topbar`
wrapping `.topbar-inner`, `.header-flex` to `.header-brand`, `header h1` to
`.brand-name`, `header p` to `.brand-sub` -- and the file is inlined verbatim
into the template between `BEGIN/END banner.css` markers. Inlined rather than
linked because the offline ZIP cannot fetch a stylesheet from another tree.

The guard is the part that works. `check_banner()` in `build_local.py` compares
the inlined block against the source and stops the build if they differ, naming
the fix; it warns and carries on when `Sym Docum` is absent, so `repos/` alone
still produces a release. The app's own controls stay in the app, layered on top
exactly as the version picker is on `learn` and the nav links on the landing
page.

Left open, deliberately: the app's build now reads a file from a tree that is
**not under version control**. Moving `banner.css` into `repos/local` and having
the docs' `build.py` read it from there would invert that dependency. Worth
doing when `Sym Docum` becomes a repo; nothing breaks meanwhile.

> **Closed 28 Aug 2026** by doing exactly the inversion above (`Sym Docum`
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
`C:\Users\perez\Claude Code\Symbulator\repos\local\index.html`.

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

