# Next build — accepted but not yet done

> **The offline pair is behind the server, as of 22 Aug 2026.**
> PythonAnywhere runs build `11:53 UTC`; install.symbulator.com and
> `local.zip` are still on `09:39 UTC`. The build for them is made and
> pushed -- `repos/local/local.zip`, sha256 `4c766674...`, cache `v26` --
> it simply has not been uploaded yet. Two jobs remain: the four changed
> files (`index.html`, `sw.js`, `circuitbook.py`, `examples.cir`) to the
> install host, and the ZIP to `symbulator.com/9/local.zip`. Rebuild
> rather than trusting that hash if anything else lands first; every build
> re-stamps.
>
> Everything below is already live on the server.

---

## #73 — Stale "several solutions" picker (**deployed to the server only**)

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

## #72 — Clear-all button press nudge (**deployed to the server only**)

**Done in the repos on 22 Aug 2026; the three live sites do not have it.**
Where: `server/templates/index.html`, commit `e4b95d7`; regenerated in
`local/index.html`, commit `2560acd`.

The button beside the Inputs heading is centred with a transform, and every
button on the site gets a 1px press nudge that is also a transform. A second
transform replaces the first rather than adding to it, and `:active` is the
more specific selector, so pressing the button discarded its centring and it
fell 20px -- half its own 37px height, plus the nudge -- gliding down and back
because `transform` is transitioned. Fixed by carrying both offsets together
as `translateY(calc(-50% + 1px))`, with the narrow-screen branch reset to the
plain nudge since the button is not centred there.

Deliberately not deployed: it is cosmetic, and shipping it costs a full
three-site round. **Fold it into the next deploy**, most likely the one that
carries #71. Until then the live sites run build `2026-08-22 09:39 UTC` while
the repos are ahead of them -- which the footer stamp will show honestly, and
is exactly what it is for.

Note for whoever does that deploy: rebuild rather than reusing any ZIP hash
quoted in this session. Every build re-stamps, so the artefact and its hash
change each time.

---

## #59 — Bracket typos quote the rewritten value, not what was typed

**Noted, not accepted.** Where: `solver/symbulator/si_prefix.py`, around
`expand_shorthand` and `check_expression_syntax`.

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

Roberto's view (22 Aug): not a problem worth a release of its own.
