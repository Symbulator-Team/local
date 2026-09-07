# Version X — its own items

Version X numbers its work **X1, X2, X3…** and writes it up here, in a
file version 9 never has, so a `git merge v9/main` can never conflict on
it. `NEXT.md` beside this file is version 9's running list and arrives
by merge; read it as upstream history, not as a record of X.

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
