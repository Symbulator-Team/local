# Next build — accepted but not yet done

Small things deliberately deferred, each because doing it on its own would
cost a PyPI publish and a three-site deploy for no user-visible gain. Fold
them into the next release that has a real reason to happen.

Numbers are the running identifiers from the session that raised them, kept
so they can be referred to unambiguously later.

---

## #71 — `/healthz` should report what is actually deployed

**Accepted 22 Aug 2026.** Where: `server/app.py`, the `/healthz` route.

It currently returns `{"ok": true}`, which confirms the process answers HTTP
and nothing else. It should also report the **build stamp** from the footer
and `symbulator.__version__`, so that "is the deployed process running what I
pushed?" is one URL instead of an investigation.

This is not hypothetical. On 22 Aug a deploy went out where `git pull` had
updated the files, `git status` was clean, and the served page carried the new
build stamp -- yet the API was still answering from the previous `app.py`,
because the PythonAnywhere web app had never been reloaded. A browser hard
refresh and a `git pull` both leave the running process untouched; only the
Reload button on the Web tab restarts it. Diagnosing that took a dozen
round trips of comparing the live site against the repo. A health endpoint
reporting the stamp would have answered it in one request.

Report the stamp the page itself shows, read the same way the page gets it,
so the two cannot disagree -- an endpoint that reports a *different* stamp
from the footer would be worse than none.

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
