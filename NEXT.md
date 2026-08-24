# Next build — accepted but not yet done

> **Deployed and verified, 23 Aug 2026.** Build `2026-08-23 09:25 UTC`, solver
> 0.5.0, cache **v30**. The Schematic card is gone; drawing is now a link
> under the circuit box, where the thing it draws is. All five sites are on
> this build; nothing here is waiting to go out.
>
> Commits live: `repos/server` `bb0659d`, `repos/local` `2402041`,
> `repos/solver` `13c42aa`. All three clean and level with origin.
>
> Measured, not eyeballed:
>
> 1. `https://symbulator.pythonanywhere.com/healthz` -- `build` and
>    `build_on_disk` both `2026-08-23 09:25 UTC`, `needs_reload: false`,
>    `solver: 0.5.0`.
> 2. `https://install.symbulator.com/` -- footer reads
>    `Symbulator 9 version 2026-08-23 09:25 UTC`, and the page shows the
>    Schematic link under the circuit box rather than the old card.
> 3. `https://symbulator.com/9/local.zip` -- downloaded: 17,443,084 bytes,
>    sha256 `63731f0a36c5909e87a33fa4098f548bb1e7f67d1553df9b0b82e9c085fb1e27`,
>    byte-identical to
>    `C:\Users\perez\Claude Code\Symbulator\repos\local\local.zip`.
> 4. `banner.css` served by `learn.symbulator.com` and by `symbulator.com`
>    both hash to the same 5,991 bytes as
>    `C:\Users\perez\Claude Code\Sym Docum\Documentation\design\banner.css`;
>    `py build_local.py --check` passes, which is the app's copy checked
>    against that same file.
>
> Every build re-stamps, so these figures hold only until the next one.

---


## #77 — TR reads its sources in the s-domain; the calculators read time

**Open, and it makes transient answers silently wrong.**

The 2023 site states the rule plainly, in the frequency-domain lesson:

> The value of sources E and J, when used as input for an FD simulation, are
> assumed to be in the s-domain. In contrast, when they are given as input for
> a TR simulation, they are assumed to be in the domain of time.

Symbulator 9's `tr()` does not do the second half. It calls `fd()` and inverse-
transforms the *answers*; the source value is passed through untouched, so it
is read as an s-domain expression. Measured:

| Circuit | Version 9 | By hand |
|---|---|---|
| `j,0,1,1:c,1,0,2,0` | `1/2` | `t/2` |
| `j,0,1,t:c,1,0,2,0` | `t/2` | `t**2/4` |
| `e1,1,0,12:r,1,2,2:c,2,0,1,0` | `6*exp(-t/2)` | `12 - 12*exp(-t/2)` |

Every one of those is the impulse response where a step response was wanted --
one integration short, and plausible enough to pass a glance.

Wrapping the value in `t2s(...)` fixes each of them, and gives the textbook
answer exactly. `j,0,1,t2s(t)` is `t**2/4`. So the machinery is all there; what
is missing is `tr()` doing it.

**Two ways out, and it is a judgement call rather than an obvious fix.**

*Transform in `tr()`.* Matches the calculators, matches the 2023 documentation,
and makes a version 7 circuit description work unchanged in version 9 -- which
was the whole point of teaching the parser `u(t)` in 0.5.1. It changes the
meaning of every existing version 9 TR call, including the app's own bundled
example (`e1,1,0,5/s`, which would then be wrong), and anything anyone has
written against the current behaviour.

*Leave it and document `t2s(...)`.* Nothing existing breaks, `fd()` and `tr()`
stay consistent with each other, and the conversion is explicit where a reader
can see it. But a version 7 description then reads unchanged and answers
differently, which is the worst of the three outcomes for someone working from
the older book -- and 0.5.1's `u(t)` shorthand makes that trap easier to fall
into, not harder.

Chapter 12 documents the rule as it stands. Chapter 6 does not yet, and its
transient panels still carry time-domain values, so **its answers are wrong
until this is settled**. That is the reason chapter 6 is not finished.

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

## #74 — The app and the two websites are different shapes (**reopened**)

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

What is left to do is markup, not CSS: wrap the app's theme toggle in
`<div class="subbar"><div class="subbar-inner">`, in
`repos/server/templates/index.html`. The keyline then moves to the subbar on its
own, because `:last-child` stops matching.

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
