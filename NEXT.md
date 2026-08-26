# Next build — accepted but not yet done

> **Deployed and verified, 26 Aug 2026.** Build `2026-08-26 07:37 UTC`, solver
> 0.5.11, cache **v59**. It carries #94, #95 and #96 -- the Conditions box on
> Evaluate, and the two silent binding bugs behind it. **All five sites are on
> this build.**
>
> Commits live: `repos/server` `b487416`, `repos/local` `afbb6aa`,
> `repos/solver` `13c42aa` (untouched). All three clean and level with origin.
>
> Measured, not eyeballed:
>
> 1. `https://install.symbulator.com/` -- footer reads
>    `Symbulator 9 version 2026-08-26 07:37 UTC`, `sw.js` reads
>    `symbulator-v59`, and the page carries `id="evalConds"`.
> 2. `https://symbulator.com/9/local.zip` -- 17,484,844 bytes, sha256
>    `abe82885dec8ea58f6d024eb32977fa8aa5e1cd1d54592cd5fff59708737111b`,
>    byte-identical to `repos/local/local.zip`, and the copy inside carries
>    the same stamp, the same cache version and the same field.
> 3. `https://symbulator.pythonanywhere.com/healthz` -- `build` and
>    `build_on_disk` both `2026-08-26 07:37 UTC`, `needs_reload: false`,
>    `solver: 0.5.11`. Pulled and reloaded by Roberto. Behaviour checked
>    rather than the stamp alone: the Conditions box is on the page,
>    `.2v1` gives -2, 3, -8 and -0.5 -- the answers HK5's Drill Problem
>    1-13 prints -- and `vc` with `t = to` gives `V - V*exp(-to/(c*r))`,
>    which is the calculator's `vc|t=to` working in version 9 for the
>    first time.
> 4. `banner.css` served by `symbulator.com` and by `learn.symbulator.com`
>    both hash to the same 11,149 bytes as the one source,
>    `C:\Users\perez\Claude Code\Sym Docum\Documentation\design\banner.css`.
>    symbulator.com had been serving an older copy until this deploy.
> 5. The banner measured in a browser at 1280 wide on the app and on learn:
>    `.topbar` 149, `.subbar` 62, same keyline, controls in the subbar.
>    That is #74, finally closed.
>
> Every build re-stamps, so these figures hold only until the next one.

---


## Found building the tutorial's example input files, 26 Aug 2026

Written up from the documentation side; the documentation findings from the
same pass are in `Sym Docum/Documentation/NEXT_DOCS.md`.

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

## #97 — The two shared modules are copied by the build now, not by hand

**Done 26 Aug 2026, not yet in a release.** `symbulator_ui.py` and
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

## #59 — Bracket typos quote the rewritten value, not what was typed

**Accepted 23 Aug 2026, for the next solver release.** Where:
`solver/symbulator/si_prefix.py`, around `expand_shorthand` and
`check_expression_syntax`.

`[a,b]` (parallel impedance) is rewritten to `pr(a,b)` and SI prefixes are
expanded *before* the value is parsed, so an error message quotes the
rewritten string. Type `[1'k,2'k` and you are told about
`pr(1*10**3,2*10**3`; type `rx[1'k]` and you get a bare
`'Symbol' object is not callable`.

Nothing is mis-solved -- every case is refused, never answered wrongly -- and
it is not a security gap: the syntax gate is intact, and `x(0)` is legitimate
input that SymPy then rejects on its own. It is a papercut on a feature
students are meant to use: the error is about internals rather than about
their circuit. The fix is to carry the original text alongside the rewritten
one and quote the original.

Not worth a release of its own -- fold it into whatever next takes the
solver to a new version, which means a version bump, a PyPI publish and
a rebundled wheel in the offline builds.
