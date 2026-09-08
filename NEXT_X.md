# Version X — its own items

Version X numbers its work **X1, X2, X3…** and writes it up here, in a
file version 9 never has, so a `git merge v9/main` can never conflict on
it. `NEXT.md` beside this file is version 9's running list and arrives
by merge; read it as upstream history, not as a record of X.

## X18 — version 9's #330–#332 merged: rounding in the equations, both methods on one press, and the augmented method; label `0.6.1+x18` — **done 8 Sep 2026, pushed; the site wants a pull of both clones**

Three of version 9's items in one merge, all of them descended from work
that started here:

* **#330** the Rounding setting reaches the card's equations, not only
  its answers -- and only the *floats*, so a DC equation keeps
  `6*I1 - 4*I2 + 20 = 0` rather than gaining a `.0` on every coefficient;
* **#331** both methods are solved on one press and the picker chooses
  which is *shown*, hidden until there is a choice to make, defaulting to
  the shorter route and to mesh on a tie;
* **#332** the augmented method: transformers and two-ports go to nodal,
  coupled coils to mesh, carrying the element's own relation as an extra
  equation and its own current as an extra unknown. **No circuit in the
  book is left without a by-hand method** -- 16 before, 0 now. Solver
  **0.6.1**, which also carries an `engine.py` fix: a four-terminal
  two-port had been registering the bracketed pair `pr(1,0)` as a node.

Three conflicts, all of them expected and none of them interesting: the
solver's version label, the server template's build stamp and the
generated `local/index.html`. Version 9's side everywhere, then the label
set to `0.6.1+x18` and `build_local.py` re-run -- checked by hashing, X
`6ff9e89c...` against version 9's `8ece0552...`, with the gold X and the
fork's subtitle in place. `branding.py` did not conflict, as it never
does.

X's suite **484 passed, 1 skipped**; the sweep **204 nodal and 149 mesh,
all agreeing** -- the same numbers version 9 reports. `i18n check: ok`.

**Open:** a pull of both clones and a reload. **No `pip`** -- the solver
is an editable checkout there, so `git pull` in `/home/symbulatorx/solver`
is what moves it to `0.6.1+x18`.

## X17 — version 9's #329 merged: the by-hand feature comes home, coded and translated; label `0.6.0+x17` — **done 8 Sep 2026, pushed; the site wants a pull of both clones**

The round trip closed. X14–X16 built the by-hand systems here; version 9
took them on 8 Sep 2026 as **#329** after the sweep came back with no
disagreements, and #329 is what comes back — better than what left.

Two things version 9 added that X did not need and now has anyway:

* **The package speaks in codes.** Every sentence a by-hand run produces
  is the *solver's*, so under #199 all of it moved into `messages.py`'s
  new **7xx range** rather than being English in `byhand.py`. X had plain
  strings; it has codes now.
* **Thirteen languages.** 67 new keys. X's standing rule is that nobody
  does language work *for* X — and this is exactly the case that rule
  anticipates: the dictionaries live in files the two trees share, so the
  merge carried them across on its own. Let it. `tools/i18n.py check` is
  **ok** here too.

Also arriving: `branches.py` as its own module (X15's extraction, which
version 9 took as part of #329 rather than as the standalone pull request
— that branch, `proposal/branch-relations`, is superseded and can be
closed), the *shorter route* line answering which method to reach for,
and solver **0.6.0**.

### The merge

`git fetch v9 && git merge v9/main` in all three repos. Ten conflicts,
every one of them X's older English version against version 9's coded
one — and since 9's descends from X's, **v9's side won everywhere**:

    solver   __init__.py, branches.py, byhand.py, tests/test_byhand.py
    server   app.py, symbulator_ui.py, templates/index.html,
             tools/check_byhand.py
    local    index.html, symbulator_ui.py

`branding.py` did not conflict at all — version 9 never touches it — and
was verified afterwards rather than assumed: `BRAND_TM = 'X'`,
`BRAND_TM_COLOR = '#d9a521'`, the fork's subtitle intact.

Then the step the rules insist on: **`build_local.py`, so X's pages stop
being byte-identical to version 9's.** Taking v9's side on the generated
`index.html` is correct *and* is exactly the shape that got this account
disabled in September, for one commit until the rebuild undoes it.
Checked by hashing rather than by looking — X `8331a2ea…`, version 9
`5dcedf8e…`, and X's page carries the gold `X` and the fork's subtitle.

The one thing that is only X's is the version label: version 9 is
**0.6.0**, so this checkout is **`0.6.0+x17`**, and a label bump needs
`pip install -e repos/solver --no-deps` in `Application\vX\.venv` before
the packaging test agrees.

### Verified after the merge

X's suite **480 passed, 1 skipped**. The whole-book sweep: **194 nodal
and 143 mesh systems, all agreeing, none differing** — the same numbers
version 9 reports, which is what a clean merge should look like.
`tools/i18n.py check` ok. Branding verified by reading `branding.py` and
by hashing the built page against version 9's.

**Open:** the site needs Roberto's pull of both clones —
`/home/symbulatorx/solver` and `/home/symbulatorx/symbulator_web` — and a
reload. **No `pip`**: X's solver is an editable checkout there, so `git
pull` in the solver clone is what moves it to `0.6.0+x17`.

## X16 — every by-hand run draws its own working on the circuit; and a branch that lies on no mesh carries no current — **done 8 Sep 2026, label `0.5.33+x16`; needs a pull of both clones**

Roberto, 8 Sep 2026: *"I would like a schematic in each run of the
by-hands equations. For the nodal, mark the nodes... For the supernodes,
either colour them separately or circle them or something. For the
supermesh, the same."*

So the card now draws a picture on **every** run, not only a mesh one,
and the picture is that run's own working:

| | |
|---|---|
| every node whose KCL is written | ringed |
| each supernode | a dashed enclosure round its nodes *and the source between them*, captioned |
| each mesh | the circulating arrow, `I1`, `I2`, `I3` |
| each supermesh | a dashed enclosure over the loops it merged, captioned |

All of it in `var(--accent, currentColor)`, so the overlay reads as one
layer distinct from the circuit, follows whichever of the fifteen themes
is on (verified live: the enclosure computes to the theme's gold), and
still renders standalone where that variable does not exist.

Two placement rules that are not obvious:

* **A supernode's box must not swallow a node that is not in it.** Where
  another node sits on the row between two members, the box is dropped
  in favour of a ring round each member and a dashed tie between them.
  A box that quietly includes a stranger is worse than no box.
* **The box reaches up to the source.** A voltage source between two
  non-reference nodes is drawn above the node row, so the enclosure is
  grown over every element whose *both* ends are inside the group --
  otherwise it encloses two nodes and not the thing that ties them.

`to_svg` now takes one `marks=` dict rather than `loops=`, and
`byhand.nodal()/mesh()` expose `.marks` in exactly that shape, so the
caller does not branch on which method it has. With no `marks` the
drawing is byte-identical to what it always produced;
`review_schematics.py` still reports `failed=0 with_issues=0`.

Measured over the book: **543 drawings, 537 node rings, 38 supernode
boxes, 523 mesh arrows, 64 supermesh boxes, and nothing — no caption,
no mesh label — landing on a symbol's ink.**

### The sweep, and the bug it found

Roberto also asked for every example to be run both ways and compared.
`tools/check_byhand.py` gained **`--cover`**, which asks the wider
question: not *is every entry checked* but *is every circuit in the book
checked somewhere*. A transient's circuit is run in FD (the domain its
own system is built in anyway) and a tool entry's circuit as a plain
solve. Neither is that entry's own answer, and the default run does not
pretend otherwise.

That wider net found a real bug in mesh analysis, on two circuits the
ordinary sweep never reaches because both are tool entries:

    Lesson_04b / HK5's Figure 2-29        (er)   i_e:  classic 0 / by hand -0.3*i_s1
    Lesson_13  / AS7's Example 19.4       (port) i_j:  classic 0 / by hand 2*i_r1

**A branch that lies on no mesh carries no current, and `mesh()` never
said so.** In both circuits one element hangs off a node nothing else
touches -- which is what an open port looks like -- so it is a bridge in
the graph, on no loop, with zero current. Both circuits then have a
dependent source that *reads* that current (`e,3,0,1.5*is1`), and with
no mesh-current expression to substitute, the symbol stayed free and
nothing in the system ever bound it. The classic solve answers 0.

Now every such branch is bound to 0 and gets its own bridge line -- *no
mesh runs through it, so none flows*. The one case that cannot be
rescued is a **current source** on such a branch: it is driving an open
circuit, there is no mesh current for it to set, and a sentence beats a
contradiction dressed as an equation, so that is a refusal. It is
reachable only on a connected circuit (a source into a genuinely
floating piece is refused by the parser first), and there is a test for
each.

### The sweep's results

| | nodal | mesh |
|---|---|---|
| **default** (each entry in its own domain) | 194 built, **194 agree** | 143 built, **143 agree** |
| **`--cover`** (every circuit, TR in FD, tools as plain solves) | 319 built, **319 agree** | 247 built, **247 agree** |
| differ / unsure / unsolved | 0 | 0 |

Six entries are skipped under `--cover`, all because **the classic solve
itself refuses them**, so there is nothing to compare against: Lesson 4's
*Bo2's Example 3.11 (Tricky, as it comes)*, which the tutorial teaches
as a failure, and five of Lesson 13's *AS7's Problem 19.x*, which are
two-port circuits that only mean anything through the `port` tool.

**So every circuit in the book that the classic solve can solve at all
has been compared, both ways where both apply, and every one agrees.**

X's suite is **477 passed, 1 skipped**. Solver label `0.5.33+x16`.

**Open:** the site needs Roberto's pull of both clones —
`/home/symbulatorx/solver` and `/home/symbulatorx/symbulator_web` — and
a reload. No `pip`.

## X15 — the branch reader extracted into `symbulator/branches.py`, and proposed to version 9 on its own — **done 8 Sep 2026; the pull request is open and Roberto's to review**

X14's front half answers a question that has nothing to do with by-hand
equations: *for each two-terminal branch of this circuit, what is its
impedance in this domain, and what source term rides in series with it?*
That is the form a hand-written nodal or mesh system needs, and also what
a better netlist export or a "show me what the engine thinks this element
is" panel would want. So it is now its own module rather than a private
half of `byhand.py`.

A **pure move**: `byhand.py` imports what it used to define, every
behaviour is unchanged, and the whole-book harness still reports 194
nodal and 143 mesh systems, all agreeing. X's suite is **475 passed, 1
skipped** — 17 of those are the new `tests/test_branches.py`.

Public names: `branches_of(elements, domain, ...)` for the one call most
callers want, with `stamped()` and `read_branches()` underneath for a
caller that needs the `Circuit` too, and `BranchError` for a circuit that
cannot be read in this form. `byhand.ByHandError` is now an alias of
`BranchError`, so every `raise`/`except` in that file still reads as it
did.

### Proposed to version 9

Branch **`proposal/branch-relations`** on `Symbulator-Team/solver`, cut
straight off `v9/main` so its diff is exactly the two new files and no
existing file is touched. Open the pull request here:

https://github.com/Symbulator/solver/compare/main...Symbulator-Team:solver:proposal/branch-relations

Verified on that branch — which is version 9's tree plus the module, with
none of X14 — as **442 passed, 1 skipped, nothing failing**, after
matching the editable install to the branch (the packaging test compares
`__version__` against the installed distribution's metadata, so a stale
`+x14` install fails it and that failure means nothing).

This is the shape the fork was made for: an idea is tried in X, and the
generally useful part of it crosses to 9 on its own, as a pull request
Roberto reviews — not the whole experiment.

**Proved red**: scaling `Z` by two in `branches.py` fails five of the
seventeen tests, including the one that asserts the derived relation and
the engine's own equation are the same equation up to a factor free of
the branch's own unknowns.

## X14 — by-hand equations: a second system, written the way it is taught, and always checked against the classic solve — **built 8 Sep 2026, label `0.5.33+x14`; not yet on `symbulatorx.pythonanywhere.com`, which needs a pull of both clones**

Roberto's brief, 8 Sep 2026, in his words: *"the classic Symbulator solve
is always done. It has 27 years of history and it is as close to tried and
tested as it gets. The by-hand equations and solve is optional, done
afterwards, and always compared to the classic Symbulator solution."* And:
*"Offer it in a card above the Numerical Explorer. It would run only when
asked, on the same circuit description, and whenever it is run, the answers
are checked against the classic."*

So the classic solve is the authority and this is subordinate to it in
every direction. The by-hand system reaches no results card, no export, no
plot and no Numerical Solver payload; it cannot change an answer; and a
failure inside it is a sentence in its own card, never an exception into
the page. When the two disagree the card says the by-hand side is the one
at fault, in those words.

### What it writes

**Nodal**, with supernodes. One KCL per node in the node voltages alone,
every branch current replaced by its own v-i relation solved for the
current. A voltage source between two non-reference nodes has no such
relation, so its two nodes are enclosed in a supernode — one KCL for the
enclosure, and the source's own equation as the constraint that replaces
the one given up. A source to a reference node needs no KCL at all. An
op-amp's output node carries whatever the op-amp supplies, so that node
gets no KCL and the input equality takes its place.

**Mesh**, with supermeshes. One KVL per mesh in `I1`, `I2`, `I3`…, with
every branch current written as the signed sum of the meshes running
through it. A current source's drop is unknown, and getting rid of it is
the method: shared between two loops, the two are added and the drop
cancels — the supermesh; on one loop only, that loop's KVL is dropped
whole and the source's own constraint fixes the mesh current.

The meshes themselves come from a **minimum-weight cycle basis** (Horton's
construction, over GF(2)). For a planar graph that basis *is* the set of
bounded faces, which is what makes it the right one to hand a student
rather than the fundamental cycles of a spanning tree — those are correct
and need not look like anything anyone would draw.

Both methods then write the **bridge** — `i_r3 = I1 - I2`, or `i_r1 =
(v_1 - v_2)/r1` — which is the last step of the method, the thing that
lets a reader see their own working turn into Symbulator's answers, and
the route the comparison itself runs through.

### It does not restate a single circuit rule

The obvious implementation writes out "a resistor's drop is `R*i`, a
capacitor's is `i/(jwC)`, an inductor in FD is `s*L*i - L*i0`…" a second
time. That is the engine's knowledge, it is domain-dependent, and a second
copy drifts from the first the moment either moves — the failure this
tree already knows from the header lockup.

So `repos/solver/symbulator/byhand.py` states no component rule at all. It
runs the real `Circuit.stamp_all()` and reads each branch's v-i relation
back **out** of the equations the engine produced, by differentiation:

    f(u, i) = lhs - rhs = 0        linear in the drop u and the current i
    Z = -(df/di) / (df/du)         E = -(f at u=0, i=0) / (df/du)

giving `v(n1) - v(n2) = Z*i + E` for whatever the domain happens to be. A
capacitor and a current source have no equation of their own — the engine
records their current in `Circuit.known` — so those are read the same way
from the admittance side. Add a domain rule to the engine and it appears
here for free.

Which element produced which equation is recorded by wrapping the
`_stamp_<kind>` methods as *instance* attributes before `stamp_all()`
runs: `stamp_all` dispatches through `getattr(self, "_stamp_" + kind)`, so
the instance attribute shadows the class method and the engine never
learns this module exists. **Zero lines of `engine.py` changed.**

### Three states, never two

A symbolic circuit can leave `simplify` unable to show a difference is
zero. Rendering that as *differs* would accuse a correct by-hand system of
being wrong, which would poison the card. So the verdict is **agrees /
differs / unsure**, and a numeric spot-check at random values is the
tie-breaker before *differs* is ever shown.

### Checked over the whole example book

`repos/server/tools/check_byhand.py` runs both methods over every built-in
entry and compares each with the classic solve:

| | nodal | mesh |
|---|---|---|
| systems built | **194** | **143** |
| agree | **194** | **143** |
| differ | 0 | 0 |
| unsure / unsolved | 0 | 0 |
| not offered | 16 | 67 |

The refusals are honest ones: transformers, two-port blocks and mutual
inductance for both methods (a first course does not teach either method
on them, and their coupled multi-terminal constraints are not a branch
relation at all), plus op-amps for mesh, whose output current is supplied
by the op-amp rather than flowing round a loop — the card says so and
points at nodal. TR is out of scope: a transient is solved in the s-domain
and inverted, so its by-hand system would be the s-domain one and could
not be compared without an inverse transform on every line. The card says
that too, and points at FD.

**Proved red**, as this tree requires. Flip one traversal sign in `_walk`
and the mesh run goes from 143 agreeing to **129 differing**, exit code 1;
the clean run exits 0.

### Five bugs the harness and the tests caught, worth keeping

1. **The harness was green against the wrong reading.** `analysis:` in a
   `.cir` file is stored under the key `domain` (circuitbook's alias
   table), so `entry.get("analysis")` was always `None` and **every entry
   ran as DC**. The first clean sweep tested a third of what it claimed.
   Reading a field by the name the file spells it is not the same as
   reading the field.
2. **`Circuit.node_sum` is not closed; `Circuit.equations` is.**
   `stamp_all` substitutes the quantities a dependent source names — a
   capacitor's current, another element's drop — into the *equations*
   only. Summing `node_sum` gave KCLs still carrying `i_co` and `v_rx`,
   which are not node voltages. The KCLs are taken from the equations now
   (they are the last one-per-node, in `node_sum` order).
3. **A VCCS reading one terminal's voltage looks exactly like an
   impedance.** `j2,1,2,.2*vrx` has a current depending on `v_1` and not
   on `v_2`, so the admittance test saw a coefficient and made it a 5 ohm
   resistor. A two-terminal component depends on its terminals **as their
   difference**; the check is `y1 + y2 == 0`, and only where neither
   terminal is a reference (a reference's voltage is the literal 0 and
   carries no coefficient).
4. **Eliminating one unknown must cost one equation.** A current source
   shared by three loops was eliminated pairwise, which spent two — the
   system stayed solvable and returned every answer in terms of `I3`. One
   pivot row, subtracted from each of the others, then dropped.
5. **A supernode's current cancels — unless something names it.** Asking
   whether `i_e1` appears in some *other* node's KCL sounds equivalent to
   asking whether it cancels, and is not: a source reading it can sit on
   one of that source's own two nodes. Now the sum is formed and looked
   at. No built-in example has that shape, so only a written test caught
   it (`test_a_source_whose_current_is_named_keeps_both_kcls`).

### The mesh currents are drawn

`schematic.py` gained an **opt-in** pass: `to_svg(desc, loops=...)` draws a
labelled circulating arrow in each mesh, taking the loops from
`byhand.mesh(...).loops`. The layout already kept an oriented segment per
element with the n1 end first, so the walk lays straight over the picture.
Which way an arrow turns is a property of the *drawing*, not of the
equations, so it is read off the drawing — the shoelace sum over the
loop's midpoints in traversal order, positive being clockwise because
SVG's y axis points down.

A mesh's centroid lands on a symbol when the loop is thin, so a label that
clashes walks a widening ring until it is clear of every ink box: measured
over the book, **24 of 251 labels clashed before, 0 after**.
`to_svg(desc)` with no `loops` is byte-identical to what it always
produced, and `review_schematics.py` reports `failed=0 with_issues=0`.

### Where it lives

| | |
|---|---|
| `repos/solver/symbulator/byhand.py` | new — both methods, the comparison, the three-state verdict |
| `repos/solver/symbulator/tests/test_byhand.py` | new — 33 tests |
| `repos/solver/symbulator/schematic.py` | the opt-in `loops` pass; `runs()` gains an optional class |
| `repos/server/tools/check_byhand.py` | new — the whole-book harness |
| `repos/server/symbulator_ui.py` | `byhand_ui`, appended |
| `repos/server/app.py` | `/api/byhand`, in its own killable child process |
| `repos/server/templates/index.html` | the card, above the Numerical Solver |
| `repos/local/bridge.py` | `byhand`, so the offline build runs it in Pyodide |
| `repos/local/build_local.py` | the fetch rewritten to `py('byhand', ...)` |

The card runs on **`last.desc_used`** — the description the classic solve
actually used, Define expanded and any ambiguous suffix resolved — not on
the textarea, so it cannot compare two different circuits. `last` gained
that field. Editing anything clears the card and disables its button, the
way #299 disabled the load-equivalent button.

The card is **not** wrapped in the offline-strip markers. It was, briefly:
`build_local.py` refuses to let `/api/` reach a local build, and stripping
the markup left the script behind with the URL in it. Everything the card
needs is in the bundled wheel, so it goes through the Pyodide bridge like
every other endpoint instead of shipping dead.

X's suite is **458 passed, 1 skipped**. Solver label `0.5.33+x14` — and a
label bump needs `pip install -e . --no-deps` in `Application\vX\.venv`
before the packaging test agrees, since it compares the module's
`__version__` against the installed distribution's metadata. X's pages were
rebuilt, so `repos/local/index.html` carries the card and still the gold X.
`sw.js`'s `CACHE_VERSION` is **not** bumped: X has no offline site to serve
a stale copy from.

**Open:** the site needs Roberto's pull of both clones —
`/home/symbulatorx/solver` and `/home/symbulatorx/symbulator_web` — and a
reload. No `pip`: the solver is an editable checkout there since X1.

## X13 — version 9's #327 merged: the two macaws, *Ara macao* and *Ara ararauna*, and the `--accent-text` token; label stays `0.5.33+x10` — **done and live 8 Sep 2026 after Roberto's pull: `/healthz` reports build `2026-09-08 01:57 UTC` running *and* on disk with solver `0.5.33+x10`, and the served page carries both binomials, both band colours and all thirteen `--accent-text` sites — and still the gold X and the fork's subtitle**

Roberto's ask, 8 Sep 2026: *"Yes, do X this time around."* One app item,
no solver change, so X's local label is untouched.

* **Ara macao** is #326's Macaw redrawn from his photographs of the bird:
  scarlet bands, the gold numeral kept as the wing band, an ultramarine
  results panel and Solve button, and a warm near-white page.
* **Ara ararauna** is new -- deep teal bands, gold numeral and button, and
  the subtle baby blue of the wing coverts kept for the subtitle and the
  ribbon links.
* **`--accent-text`** lets a theme's button colour and its link colour
  differ, which both macaws need: gold measures 1.97:1 as text. Nine text
  uses in `index.html` and one in `eqsheet.html` read it with `--accent`
  as the fallback, so the other thirteen themes are untouched.

Fifteen themes in X as in 9.

**The merge.** One conflict in each of `server` and `local`, both the build
stamp, both taken from v9 -- and asserted to *be* the stamp before
resolving, rather than resolved on faith. `branding.py` auto-merged with X's
four values intact, and `build_local.py` was re-run afterwards. Verified:
X's `index.html` hashes differently from version 9's, carries the gold
`#d9a521` X and the fork's subtitle, has **no** beta mark, and carries both
macaws, both band colours and all thirteen `--accent-text` sites.

**The theme names are Linnaean binomials and are not translated** -- all
twelve dictionaries carry them verbatim. That arrives here by merge like any
shared file, and is right for X too: a species name does not change with the
reader's language, so X's English-only rule has nothing to say about it.

## X12 — version 9's #324, #325 and #326 merged: *Clear all inputs*, Aqua, and the Bayerische and Macaw themes; label stays `0.5.33+x10` — **done and live 7 Sep 2026 after Roberto's pull: `/healthz` reports build `2026-09-07 10:48 UTC` running *and* on disk with solver `0.5.33+x10`, and the served page carries both theme blocks, `'Aqua'`, *Clear all inputs* — and still the gold X and the fork's subtitle**

Roberto's ask, 7 Sep 2026: *"Please publish the new themes to X as
well."* Three app items, no solver change, so X's local label is
untouched.

* **#324** — the ribbon reads *Clear all inputs* above 640px and falls
  back to *Clear* below it, through an app-local media query scoped by
  the button's id. X inherits the wording and the breakpoint.
* **#325** — the *Turquoise* theme is called **Aqua**; the palette key
  stays `turquoise`, so nobody's stored choice resets.
* **#326** — two themes join the picker: **Bayerische** (the BMW M
  stripe — `#16588e` bands, `#81c4ff` numeral, red accent) and
  **Macaw** (cobalt bands, gold numeral, gold button on a warm page).
  Fourteen themes now.

**The merge.** One conflict in each of `server` and `local`, both the
build stamp, both taken from v9. `branding.py` auto-merged with X's four
values intact, and `build_local.py` was re-run afterwards -- the step
that matters here, because taking v9's side on the *generated* pages
leaves X byte-identical to version 9, which is the shape that got the
account disabled in September. Verified after the rebuild: X's
`index.html` hashes differently from version 9's, carries the gold
`#d9a521` X and the fork's subtitle, has **no** beta mark, and carries
all three items (`bayerische` and `macaw` blocks, `'Aqua'`, and thirteen
*Clear all inputs*).

**X is English-only by decision (31 Aug 2026), and this changed nothing
about that.** The twelve dictionaries carry the new theme names because
they live in files X shares with 9 and the merge brings them across on
its own. That is the documented outcome, not a mistake: let it happen,
do not strip them back out.

## X11 — version 9's three 12th-edition Nilsson & Riedel entries merged; label stays `0.5.33+x10` — **done 7 Sep 2026, pushed; rides the site's next pull**

Examples and the server template's stamp only; the solver did not
move. Merged clean, `branding.py` intact, X's pages rebuilt.

## X10 — version 9's 0.5.33 (#323, an island behind a coupling) merged; label `0.5.33+x10` — **done 7 Sep 2026, live: `/healthz` reports `0.5.33+x10`, build `2026-09-06 23:37 UTC` running and on disk, and a floating-secondary transient solves on the live site, after Roberto's pull**

The same merge, no conflicts, `branding.py` intact. X's suite 425
passed and 1 skipped, pages rebuilt with the gold X. What X gains: a
coupled pair's secondary may float, with note 221 saying *behind a port
or a coupling*, and eight Nilsson & Riedel entries in Lesson 10. The
pull is the same pair of commands, no `pip`.

## X8, X9 — version 9's 0.5.32 (#320–#322, ports that float) merged, then its drawing fix; label `0.5.32+x8` — **done 7 Sep 2026, live: `/healthz` reports `0.5.32+x8`, build `2026-09-06 22:01 UTC` running and on disk, and the live site draws a groundless entry (X9's fix), after Roberto's pull**

Two merges the same morning, both `git merge -X theirs v9/main` in all
three repos with no conflicts and `branding.py` intact. X8 carried the
release: `port()` taking `[top,bottom]` pairs, an island behind a port
given its own reference (message 221), two overlapping blocks stacked in
lanes, the six Lesson 13 entries, the labels and reference sentence in
thirteen languages; label `0.5.32+x8`, X's suite 424 passed and 1
skipped, pages rebuilt with the gold X. X9 carried the fix that
followed: the drawing takes the port tool's references too, so a
groundless entry draws around the tool's own ground instead of showing
an error in the schematic card (`build_local.py`'s schematic rewrite
changed with it, and X's pages were rebuilt again). The solver did not
change between X8 and X9, so the label stays. The pull is the same pair
of commands as X6 and X7, no `pip`.

## X7 — version 9's 0.5.31 (#318, decimal rounding) merged; label `0.5.31+x7` — **done 6 Sep 2026, live: `/healthz` reports `0.5.31+x7`, build `2026-09-06 10:47 UTC` running and on disk, and the wye-delta solve on the live site prints -36.20, after Roberto's pull**

The same merge as X4–X6, `git merge -X theirs v9/main` in all three
repos, no conflicts, `branding.py` intact (checked). Label
`0.5.31+x7`, X's editable checkout refreshed, X's suite **412 passed,
1 skipped** (the IPython round trip), `build_local.py` re-run with X's
interpreter, the page differing from version 9's by `cmp`. What X
gains: the app's Rounding setting, its polar display and the `aa` tool
round in decimal, half away from zero, through the package's
`round_sig` -- twelve of the tutorial's rounded answers move to the
book's digit, and the wye-delta current reads `2.350∠-36.20°`. The
pull is the same pair of commands as X6, no `pip`.

## X6 — version 9's 0.5.30 (#315, the package in a notebook) merged; label `0.5.30+x6` — **done 6 Sep 2026, live: `/healthz` reports `0.5.30+x6`, build `2026-09-06 09:49 UTC` running and on disk, and a DC solve on the live site answers, after Roberto's pull**

The same merge as X4 and X5: `git fetch v9 && git merge -X theirs
v9/main` in all three repos, all three auto-merged with no conflict to
resolve by hand (`symbulator/__init__.py`, the server template's build
stamp and the generated `index.html` were the files that moved).
`branding.py` untouched by v9, so X's four values are intact -- checked
after the merge, not assumed. The version label set to **`0.5.30+x6`**,
X's editable checkout refreshed in `Application\vX\.venv`, X's suite
**410 passed, 1 skipped** (the skip is #315's IPython round trip, which
`importorskip` passes over where IPython is absent; the other 20
notebook tests ran). `build_local.py` re-run with X's interpreter so
X's pages carry the gold X and the fork's subtitle; the built page
differs from version 9's, verified by `cmp`. X's `sw.js` is at cache
v156 with the 0.5.30 wheel named, as version 9's is.

What X gains is what #315 is: typeset results in a notebook, the
tutorial's `ir1`/`v2` spellings on a `Result`, `polar()`, `rounded()`,
the cell magics, the quickstart notebook. None of it touches the app,
so X's site will look the same after the pull; `/healthz` will report
`0.5.30+x6`, which is the one visible change.

**The pull, on the X account** (bash, in a PythonAnywhere console;
lowercase home):

    cd /home/symbulatorx/solver && git pull

    cd /home/symbulatorx/symbulator_web && source ~/.virtualenvs/symbulator-venv/bin/activate && git pull

Then **Reload** on the Web tab. No `pip`: the solver is the editable
checkout, so the first `git pull` is the solver upgrade, and
`requirements.txt`'s `>=0.5.30` is satisfied by `0.5.30+x6`.

## X5 — version 9's 0.5.29 merged — **done 6 Sep 2026, live: `/healthz` reports `0.5.29+x5` after Roberto's pull**

The same merge as X4, an hour later, for the two fixes 0.5.29 carries
(the tapped autotransformer's internal unknown dropped from the answers,
a wide turns ratio printed above the row). X differs from 9 by the same
files as before.

## X4 — version 9's #314 merged; X2 and X3 superseded — **done 6 Sep 2026, pushed; the site awaits Roberto's pull of both clones and a reload**

Roberto took the four-terminal idea into version 9 itself (#314 in
`NEXT.md`, now upstream history here), with a different syntax from X2's:
brackets mean a pair, `t,[tl,bl],[tr,br],[N1,N2]` and
`z,[tl,bl],[tr,br][,[…]]`, and X2's flat `t,n1,n2,n1b,n2b,N1,N2` is
gone -- he noticed it on this site's reference table and asked whether it
should not be with brackets; it should, and now is. X3's currents at
every terminal are in 9 too, and the drawings X2 refused are drawn.

The merge: `git fetch v9 && git merge -X theirs v9/main` in all three
repositories, then version 9's own copies of `elements.py`,
`messages.py`, `schematic.py` and `symbulator_ui.py` checked out over the
X2/X3 hunks the merge had kept, so that X's solver differs from 9's by
its `CLAUDE.md`, the version label -- **`0.5.28+x4`** -- and the packaging
test's regex, and X's server by `CLAUDE.md`, `branding.py` and the two
diagnostics; then `build_local.py`, so X's pages carry the gold X again
(the merged pages were 9's). X's suite in `Application\vX\.venv`: 390
passed. The site: `cd /home/symbulatorx/solver && git pull`, then the web
clone's pull, then Reload; `/healthz` should read `0.5.28+x4`.

## X2 — a transformer or two-port block written with all four terminals — **superseded by version 9's #314 (X4)**; the record below is kept as history — **done 6 Sep 2026, live on `symbulatorx.pythonanywhere.com`: `/healthz` reports solver `0.5.26+x2`, and the four-node transformer case solves on the live site (`i_r0 = 5/202`, `i_r5 = 0`), verified by fetching after Roberto's pull ("Works.")**

Roberto, 6 Sep 2026: keep the calculator's two-node forms, and also
take *two-port name, top left, top right, bottom left, bottom right,
[parameters]* and *tname, top left, top right, bottom left, bottom
right, turns on the left, turns on the right*. His three rulings, from
the design round: **A1** the drawing can come later; **A2** the dots
stay top-left and top-right, as in the two-node form; **A3** rule 1
(the four-node form may put 0 anywhere, `z,1,2,0,0` being `z,1,2`
written out), rule 2 (a port with the same node at both terminals is
refused) and rule 3, with his correction: *floating* means **the whole
side of the circuit** has no ground node, not merely that side of the
element.

**The syntax needs no new letters; the field count says the form.** A
two-port with its bracket term stripped has two nodes or four; a
transformer has five terms or seven. Every existing description keeps
its meaning.

    z,1,2,[100,10,20,50]        two nodes, as before
    z,1,2,3,4,[100,10,20,50]    top-left, top-right, bottom-left, bottom-right
    t,1,2,1,3                   as before
    t,1,2,3,4,1,3               four nodes, then the turns

**One stamp for both forms.** `Element` gained `port_nodes` --
`((top_left, bottom_left), (top_right, bottom_right))`, with a literal
`"0"` for the bottoms of the two-node form -- and `four_node`, `turns`,
`param_idx` and `node_idx` beside it. `engine._stamp_t` and
`_stamp_two_port` read a port voltage as the difference across its
pair and put each port current into the top terminal and out of the
bottom; with the bottoms on 0 that is byte-for-byte what they did
before, which the tests prove by solving each form and comparing every
answer. The answer names are unchanged: `i_z12` is still the current
into the port at node 2, and the bottom terminal carries the negative.

**The rules, where they live.** `_validate_topology` skips the
no-ground-on-a-port rule for the four-node form and adds
`E_PORT_SAME_NODE` (218) for a shorted port; `_check_connected` joins
each port's own two terminals and **does not join the two ports**, so
an ideal transformer or parameter block conducts nothing across, and a
secondary side whose nodes never reach 0 -- however much hangs on it --
is `E_FLOATING_NODES`, the message a dangling resistor gets. That is
rule 3 as Roberto meant it, and it is what the grounded form had been
doing silently.

**Field counts and messages, without new dictionary keys.** The
element-count messages take their expectations as text, so m208 now
says *3 or 5 terms are expected for a two-port element, or 4 or 6 with
its parameters as the last term* and m209 says *Exactly 5 or 7* for a
transformer -- no new key, no translation work, which X does not do.
The two new codes (218, and 701 below) have English in
`messages.py` only; the page's `uiMsg` falls back to the engine's text
for a code it does not know, and the i18n check passes (`tools/i18n.py
check`: ok) because the check reads the page's own literals, not the
catalogue.

**Everything that reads a field by position was found and moved.** The
kind table `_IDENTIFIER_FIELD_IDX` stays for the two-node forms, and
`identifier_field_idx(el)` / `el.node_idx` answer by element: the
parser's case folding, the connectivity check, `laplace._is_controlled`,
`spice.py`'s node set, and in the app `expand_defines_in_desc` (which
also materialises the tacit `[z11,z12,z21,z22]` term on a four-node
block, so a Define lands -- verified live), the AC imaginary-unit
normaliser and the DC complex-value check. `_VALUE_FIELD_IDX`'s `t`
entry moves to the last two fields when there are four nodes, so a node
named `2k` on a four-node transformer is never asked about as a value.
`two_port_param_texts` reads the *last* field.

**SPICE export generalises directly.** A SPICE controlled source takes
four nodes anyway: the transformer's E/sense/F triple and the two-port's
VCCS quartet now name each port's pair, with `0` for the two-node form,
so the netlist for an old description is unchanged. **Ground truth:**
`test_spice_groundtruth.py` gained nine four-node cases -- a
transformer with its primary between two live nodes and a secondary
grounded on its own side, and every one of the six parameter kinds with
both ports spanning live pairs -- and ahkab agrees with the engine on
every node voltage to 1e-6. ahkab is installed in `Application\vX\.venv`
with `--no-deps` (its pins are from 2015; the test module's three shims
carry it on Python 3.14), which is what makes those tests run here
rather than skip.

**The drawer refuses, cleanly.** `to_svg` raises `E_DRAW_FOUR_NODE`
(701, a new 7xx range for `schematic.py`): *'t1' names four nodes. The
schematic drawer draws a transformer or two-port only in its two-node
form for now; the circuit still solves.* The layout is one node row
over one ground rail and both symbols hang between them, which *is* the
two-node form; drawing a live bottom pair as though it were the rail
would be a wrong picture rather than none. A four-node symbol is the
next item when Roberto wants it.

**The app's format reference** shows both forms on the `t` row and the
six two-port rows (English, `notranslate` cells, so the dictionaries are
untouched). **Not done:** the solver's `README.md` and the version 9
tutorial, both of which X shares with 9 and does not edit -- the
elements.py docstring carries the syntax; and the *Two-port parameters*
tool, which measures a circuit between two nodes and grounds them, is
unchanged.

**Verified.** Solver suite in the venv: **370 passed** (337 before,
33 new: 24 in `test_four_node_ports.py`, 9 ground-truth cases). On the
dev server: the four-node transformer case answers `i_r0 = 5/202`,
`i_t12 = 5/202`, `i_r1 = 5/101`, `i_r5 = 0` (reflected 400 Ω in series
with 4, the referencing resistor carrying nothing); a symbolic
four-node `z` with its four parameters in Define solves numerically;
`/api/schematic` on a four-node circuit returns code 701 with the
sentence above; the floating secondary returns 217 naming both of its
nodes; `/healthz` reports `0.5.26+x2`. The format reference serves both
forms (read from the DOM; the browser pane's screenshots came back
blank for the popup and were not chased).

## X1 — X runs its own solver checkout, not the PyPI package — **done 6 Sep 2026, live on `symbulatorx.pythonanywhere.com`: `/healthz` reports solver `0.5.26+x1`, build `2026-09-06 03:07 UTC` running and on disk, and a DC solve on the live site answers**

Roberto's first console pass came back reading `0.5.26` -- the checkout
was installed editable, but the version line had not been pushed, so the
clone read the same as PyPI. The label did its job: the two are
indistinguishable without it. Pushed, pulled again, reloaded: `+x1`.

Roberto, 6 Sep 2026: *"Is it possible to make modifications to
Symbulator X without touching 9? I would like to try some experimental
things."* Then, on whether to publish a `symbulatorx` package or run
from a local library: *"I agree with using a local library in X."*

The decision, and why. `symbulator` on PyPI is version 9's name and
Roberto's to release, and a second distribution was worse either way:
keeping the import name `symbulator` under a new distribution name puts
two packages in the same `site-packages/symbulator` folder, last one
installed wins silently; renaming the import package touches every
`from symbulator …` line in the server, the tools, the offline bridge
and the docs' exemplar renderer, and each of those lines then conflicts
on every merge from 9, with the reflex resolution taking 9's side --
the shape that made X a byte-identical clone once already. So X's
server keeps its `requirements.txt` pin and the fork's solver is
installed *over* the PyPI copy as an editable checkout. Three parts:

**The version label.** X's solver is `0.5.26+x1` -- a PEP 440 local
label on the version 9 release it forked from. It sorts above `0.5.26`,
so it satisfies the pin `symbulator>=0.5.26` and a later
`pip install -r requirements.txt` leaves it alone; PyPI refuses local
labels, so it cannot be uploaded by accident; and `/healthz` reports
it, so one request says whether a site is running X's solver or
version 9's. One line, `symbulator/__init__.py`, X's to keep on a
merge. The solver's packaging test asked for a bare `x.y.z`; it now
accepts an optional local label, which version 9's versions still
pass. Bump the label (`+x2`, …) whenever X's solver changes in a way a
site should be able to show.

**A virtualenv of X's own.** The machine's Python is the one version
9's dev server runs on, so an editable install there would have put
X's solver under version 9 -- exactly the touching this item exists to
prevent (measured before and after: the global interpreter still
resolves the 0.5.23 in `site-packages`). X's environment is
`Application\vX\.venv`, outside all three repos, made by:

    py -m venv Application\vX\.venv
    Application\vX\.venv\Scripts\python.exe -m pip install -r Application\vX\repos\server\requirements.txt
    Application\vX\.venv\Scripts\python.exe -m pip install -e Application\vX\repos\solver

The second command installs version 9's 0.5.26 from PyPI and the third
replaces it -- the same two steps, in the same order, that the
PythonAnywhere console will run. `pip list` there reads
`symbulator 0.5.26+x1 …\vX\repos\solver`. The dev server has its own
entry in `.claude/launch.json`, `symbulatorx-server`, on port **5001**
through that interpreter (`flask --app … run --port 5001 --debug`, so
`app.py`'s hard-wired 5000 is not edited and never collides with
version 9's server).

**Verified on the dev server, 6 Sep 2026:** `/healthz` reports
`"solver": "0.5.26+x1"` with build `2026-09-06 03:07 UTC` running and
on disk; the page carries the fork's gold X and subtitle; a DC solve
of `e1,1,0,10:r1,1,2,4:r2,2,0,6` posted to `/api/solve` answers
`i_r1 = 1`, `v_2 = 6`, `p_r2 = 6`. The solver's suite in the venv:
317 passed, 1 skipped.

**What is left is Roberto's console, on the `symbulatorx` account**
(lowercase home; the venv only needs activating because `pip` is
involved):

    cd /home/symbulatorx && git clone https://github.com/Symbulator-Team/solver.git
    cd /home/symbulatorx/symbulator_web && source ~/.virtualenvs/symbulator-venv/bin/activate && git pull && pip install -e /home/symbulatorx/solver

Then **Reload** on the Web tab, and
`https://symbulatorx.pythonanywhere.com/healthz` should say
`"solver": "0.5.26+x1"`. From then on a solver change reaches the site
by `git pull` in `/home/symbulatorx/solver` plus a reload -- no `pip`
unless the dependencies change. The clone is a sibling of
`symbulator_web`, not inside it, so the web repo's own pulls never see
it. Free-tier disk is tight (see `server/CLAUDE.md`); the checkout is
small, but `pip install -e` needs `setuptools` in the venv, which pip
fetches by itself.

**Not done, on purpose.** The offline build (`repos/local`) bundles a
wheel by filename in three pinned places (`build_local.py`, `sw.js`,
`vendor/`). Nothing there changes until an experiment reaches the
offline build; when one does, build a wheel from the checkout (`py -m
build --wheel` in `repos/solver`), which will be named
`symbulator-0.5.26+x1-py3-none-any.whl`, and move the three pins
together. `requirements.txt` is untouched, so it merges clean.
