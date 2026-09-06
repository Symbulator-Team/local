# Version X — its own items

Version X numbers its work **X1, X2, X3…** and writes it up here, in a
file version 9 never has, so a `git merge v9/main` can never conflict on
it. `NEXT.md` beside this file is version 9's running list and arrives
by merge; read it as upstream history, not as a record of X.

## X1 — X runs its own solver checkout, not the PyPI package — **done 6 Sep 2026 on the dev server; the PythonAnywhere half awaits Roberto's console pass**

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
