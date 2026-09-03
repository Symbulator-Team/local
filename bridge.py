"""
Thin bridge between the browser page and `symbulator_ui`.

The browser build runs the *same* symbulator_ui module the Flask server
uses; this file only adapts the calling convention. JavaScript hands in
a plain object and gets JSON back, so nothing but strings and numbers
crosses the boundary.

There is deliberately no security validation beyond what symbulator_ui
already does for good error messages: with no server involved, the only
person a runaway expression can inconvenience is the user who typed it,
in their own browser tab.
"""

import json

import symbulator_ui as ui
import circuitbook

MAX_PLOT_POINTS = getattr(ui, "MAX_PLOT_POINTS", 2000)


def _digits(payload):
    """Read and sanity-clamp the "digits" field of a JS payload dict
    (see symbulator_ui._clean_digits) -- a tiny shared helper since
    several of the functions below need this same value more than once."""
    return ui._clean_digits(payload.get("digits"))


def solve(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/solve: same validation,
    same ambiguous-suffix negotiation, same call into symbulator_ui --
    just JSON string in, JSON string out instead of an HTTP request/
    response, since there's no server here to speak HTTP to."""
    p = json.loads(payload_json)

    desc = str(p.get("desc", "")).strip()
    # Elements may be separated by ":" or by new lines.
    desc = ui.re.sub(r"[\r\n]+", ":", desc)
    desc = ui.re.sub(r":{2,}", ":", desc).strip(":")

    domain = str(p.get("domain", "dc")).strip().lower()
    omega = str(p.get("omega", "")).strip()
    tool = str(p.get("tool", "solve")).strip().lower() or "solve"
    n1, n2 = str(p.get("n1", "")).strip(), str(p.get("n2", "")).strip()
    kind = str(p.get("kind", "z")).strip().lower()

    def lines(field):
        """Read `field` from the payload as a list of non-blank strings,
        accepting either a JSON array or one newline-separated block of
        text -- mirrors app.py's `_lines` helper for the same reason
        (a plain <textarea> sends the latter)."""
        raw = p.get(field) or ""
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
        return [ln.strip() for ln in ui.re.split(r"[\r\n]+", str(raw)) if ln.strip()]

    # A list or a comma/space-separated string, because app.py takes
    # both and these two files are not allowed to differ. str() on a
    # list gives "['v 2']", which then splits into garbage -- found by
    # verify_bridge.py on its first run, 31 Aug 2026. Not reachable from
    # the page, which sends the Variables field's text, but the drift is
    # the bug.
    _vars = p.get("variables") or ""
    if not isinstance(_vars, (list, tuple)):
        _vars = ui.re.split(r"[,\s]+", str(_vars))
    variables = [str(v).strip() for v in _vars if str(v).strip()]
    # Equations and conditions alike: one per line, or several on one
    # line joined with ` and ` -- "re = 12'k and ir3 = 6'm" is two
    # equations. Expanded before validating/solving, matching app.py's
    # /api/solve. Equations joined the conditions on 28 Aug 2026, when
    # the Expert Mode hint started saying so (#12 of the day's batch)
    # and Roberto asked whether it was actually true.
    equations = ui._expand_and(lines("equations"))
    conditions = ui._expand_and(lines("conditions"))
    unknowns = [u.strip() for u in
                ui.re.split(r"[,\s]+", str(p.get("unknowns") or "")) if u.strip()]

    # The Define field, expanded before anything reads the text -- and
    # before the ambiguous-suffix check below, so a definition that brings
    # in a bare "1k" is questioned exactly as an inline one would be.
    defines, define_err = ui.parse_defines(lines("defines"))
    if define_err:
        return json.dumps(ui._err(define_err))
    define_notices = []
    if defines:
        define_notices = ui.define_shadow_notices(defines, desc)
        desc = ui.expand_defines_in_desc(desc, defines)
        equations = [ui.expand_defines(e, defines) for e in equations]
        conditions = [ui.expand_defines(c, defines) for c in conditions]
        unknowns = [ui.expand_defines(u, defines) for u in unknowns]

    err = ui._validate(desc, domain, omega, variables or None)
    if not err:
        err = ui._validate_extras(equations, unknowns, conditions)
    if not err and tool != "solve":
        if domain not in ("dc", "ac", "fd"):
            err = ("Thevenin / impedance / two-port tools work in DC, AC "
                   "or FD -- not in the time domain.")
        elif not (n1 and n2):
            err = "Give the two port nodes (n1 and n2) for this tool."
    if err:
        return json.dumps(ui._err(err))

    # --- i / I / j all mean the imaginary unit in AC; settle on j, and
    # say so -- outside AC those letters are ordinary variables, so this
    # is a no-op there (see symbulator_ui.normalise_imaginary) ---
    desc, imaginary_notes = ui.normalise_imaginary(desc, domain)

    # --- ambiguous bare suffixes: ask, then rewrite explicitly ---
    choices = {str(k): str(v) for k, v in (p.get("suffix_choices") or {}).items()
               if v in ("si", "var")}
    try:
        from symbulator.elements import (parse_circuit, ambiguous_in_elements,
                                         _VALUE_FIELD_IDX)
        from symbulator.si_prefix import bare_suffix_match, _BARE_SUFFIX_EXP
        # expand_si=False: keep SI-prefix shorthand (4.7'M) as typed in
        # these elements' fields -- they're what desc_used gets rebuilt
        # from below, matching app.py's /api/solve. It's still expanded
        # to a real number the normal way when solve_ui parses `desc`
        # again for the actual solve.
        elements = parse_circuit(desc, expand_si=False)
        ambiguous = ambiguous_in_elements(elements)
    except Exception as exc:
        # _exc_msg, not _exc_text: this is the parse step, and it was
        # the last place a CircuitError's code (#199) was flattened.
        # app.py had the same gap; verify_bridge.py found this one.
        return json.dumps(ui._err(ui._exc_msg(exc)))

    if ambiguous:
        if any(a["token"] not in choices for a in ambiguous):
            groups = {}
            for a in ambiguous:
                g = groups.setdefault(a["token"], {
                    "token": a["token"], "number": a["number"],
                    "letter": a["letter"],
                    "exponent": _BARE_SUFFIX_EXP[a["letter"]], "elements": []})
                g["elements"].append(a["element"])
            return json.dumps({"ok": False, "ambiguous": list(groups.values())})
        for el in elements:
            for idx in _VALUE_FIELD_IDX.get(el.kind, ()):
                if idx >= len(el.fields):
                    continue
                m = bare_suffix_match(el.fields[idx])
                if m:
                    sep = "'" if choices[el.fields[idx].strip()] == "si" else "*"
                    el.fields[idx] = f"{m[0]}{sep}{m[1]}"
                    # Keep the typed copy in step: `desc` is rebuilt from
                    # raw_fields below, so the resolved spelling has to
                    # land there too or the choice would be lost.
                    _raw = getattr(el, "raw_fields", None)
                    if _raw and idx < len(_raw):
                        _raw[idx] = el.fields[idx]

    # Always echo the circuit back one element per line, same as app.py's
    # /api/solve -- consistent every time you run, not just on the two
    # occasions (imaginary-unit normalizing, an ambiguous suffix being
    # resolved) that used to trigger it.
    #
    # Each element re-emits from raw_fields -- the fields as typed --
    # not from fields, where the `[...]` shortcut has already been
    # rewritten to pr(...). Re-emitting the rewrite was #116: solve_ui's
    # own parse then recorded pr(...) as "what the reader typed", so an
    # error about the value quoted `rxpr(1'k)` for a reader who wrote
    # `rx[1'k]`. raw_fields is empty when nothing was rewritten (fields
    # is identical) and when the shortcut's inner commas made the typed
    # text split differently (unrecoverable -- see parse_circuit), so
    # falling back to fields loses nothing. An unbalanced bracket cannot
    # reach here: it raised in the parse above.
    desc = ":".join(
        e.name + "," + ",".join(getattr(e, "raw_fields", None) or e.fields)
        for e in elements)
    desc_used = desc.replace(":", "\n")

    res = ui.solve_ui(desc, domain, omega, variables or None, tool, n1, n2, kind,
                      equations, unknowns, conditions, _digits(p),
                      bool(p.get("si")), bool(p.get("units")),
                      bool(p.get("use_rms")), bool(p.get("approx")),
                      bool(p.get("polar")), bool(p.get("dual")))
    # Attach the notes either way: when the solve fails, "normalised
    # '5*i' to '5j'" is often the explanation for the error underneath.
    res["notes"] = (define_notices + imaginary_notes
                    + list(res.get("notes") or []))
    if res.get("ok"):
        # "approx"/"approx_forced" are left as solve_ui set them, not
        # overwritten with the request's original value -- solve_ui may
        # have switched exact to approximate itself, and the UI needs to
        # see that, not what was originally asked for.
        res.update({"domain": domain, "tool": tool, "desc_used": desc_used,
                    "digits": _digits(p), "si": bool(p.get("si")),
                    "units": bool(p.get("units")),
                    "use_rms": bool(p.get("use_rms")),
                    "polar": bool(p.get("polar")),
                    "dual": bool(p.get("dual"))})
    return json.dumps(res)


_VALID_PLOT_TOOLS = {"time", "bode", "bode_tf", "sweep"}
_MAX_RANGE = 1e15


def _clean_range(raw, lo_default, hi_default):
    """Same parsing as app.py's /api/plot helper of the same name."""
    try:
        lo = float(raw.get("min")) if raw.get("min") not in (None, "") else lo_default
        hi = float(raw.get("max")) if raw.get("max") not in (None, "") else hi_default
    except (TypeError, ValueError):
        return None, None, "Range values must be numbers."
    if not (-_MAX_RANGE < lo < _MAX_RANGE and -_MAX_RANGE < hi < _MAX_RANGE):
        return None, None, "Range values are out of bounds."
    return lo, hi, None


def plot(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/plot: samples a circuit
    (or a typed transfer function, or a DC answer against a symbolic
    value) for the Plot card's tools, with no server round-trip. Needs
    NumPy (see symbulator.plotting's module docstring for why it's not
    vendored by default) -- until a NumPy wheel is added to vendor/,
    this returns a friendly error rather than solving, same as it would
    for any other missing package."""
    p = json.loads(payload_json)
    desc = str(p.get("desc", "")).strip()
    desc = ui.re.sub(r"[\r\n]+", ":", desc)
    desc = ui.re.sub(r":{2,}", ":", desc).strip(":")
    tool = str(p.get("tool", "")).strip().lower()
    key = str(p.get("key", "")).strip()
    try:
        n = int(p.get("n", 200))
    except (TypeError, ValueError):
        n = -1

    def lines(field):
        raw = p.get(field) or ""
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]
        return [ln.strip() for ln in ui.re.split(r"[\r\n]+", str(raw)) if ln.strip()]

    extra_equations = ui._expand_and(lines("equations"))
    extra_conditions = ui._expand_and(lines("conditions"))
    extra_unknowns = [u.strip() for u in
                      ui.re.split(r"[,\s]+", str(p.get("unknowns") or "")) if u.strip()]

    # Same defines expansion the server route does -- until 27 Aug 2026
    # this function skipped it, so an offline plot of a circuit that
    # leaned on the Define box failed on symbols the solve had accepted.
    defines, define_err = ui.parse_defines(lines("defines"))
    if define_err:
        return json.dumps(ui._err(define_err))
    if defines:
        desc = ui.expand_defines_in_desc(desc, defines)
        extra_equations = [ui.expand_defines(e, defines) for e in extra_equations]
        extra_conditions = [ui.expand_defines(c, defines) for c in extra_conditions]
        extra_unknowns = [ui.expand_defines(u, defines) for u in extra_unknowns]

    xname = str(p.get("xname", "")).strip()
    err = None
    if tool not in _VALID_PLOT_TOOLS:
        err = "Unknown plot tool."
    elif tool == "bode_tf":
        # No circuit involved: `key` carries the transfer function itself.
        if not key:
            err = "Give a transfer function of s, e.g. 100/(s^2 + 10*s + 100)."
        elif len(key) > 500 or not ui._ALLOWED.match(key) or "__" in key:
            err = "Transfer function contains invalid characters."
    elif not desc:
        err = "Please enter a circuit description."
    elif not key or not ui._VARNAME.match(key):
        err = "Give a variable to plot, e.g. v_2 or i_r1."
    elif tool == "sweep" and (not xname or not ui._VARNAME.match(xname)):
        err = "Give a variable to sweep along the x-axis, e.g. rx."
    if not err and not (2 <= n <= MAX_PLOT_POINTS):
        err = f"Number of points must be between 2 and {MAX_PLOT_POINTS}."
    if not err and tool != "bode_tf":
        err = ui._validate_extras(extra_equations, extra_unknowns, extra_conditions)
    if err:
        return json.dumps(ui._err(err))

    if tool == "time":
        t_min, t_max, rng_err = _clean_range(p, 0.0, 1.0)
        if rng_err:
            return json.dumps({"ok": False, "error": rng_err})
        res = ui.plot_time_ui(desc, key, t_min, t_max, n,
                              extra_equations, extra_unknowns, extra_conditions)
    elif tool == "sweep":
        x_min, x_max, rng_err = _clean_range(p, 0.0, 1.0)
        if rng_err:
            return json.dumps({"ok": False, "error": rng_err})
        res = ui.sweep_ui(desc, key, xname, x_min, x_max, n,
                          extra_equations, extra_unknowns, extra_conditions)
    else:
        f_min, f_max, rng_err = _clean_range(p, 1.0, 1000.0)
        if rng_err:
            return json.dumps({"ok": False, "error": rng_err})
        if f_min <= 0 or f_max <= 0:
            return json.dumps({"ok": False, "error": "Bode frequencies must be positive (Hz)."})
        if tool == "bode_tf":
            res = ui.bode_tf_ui(key, f_min, f_max, n)
        else:
            res = ui.bode_ui(desc, key, f_min, f_max, n,
                             extra_equations, extra_unknowns, extra_conditions)
    if res.get("ok"):
        res["tool"] = tool
    return json.dumps(res)


def schematic(payload_json: str) -> str:
    """Draw the circuit as an SVG, without solving it. Called from JS the
    same way as the others; the whole dict is serialised, so a key added
    in symbulator_ui arrives here without this file changing."""
    p = json.loads(payload_json)
    return json.dumps(ui.schematic_ui(str(p.get("desc") or "")))


def evaluate(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/evaluate: substitute the
    posted values into `expr` and format the result, with no server
    round-trip."""
    p = json.loads(payload_json)
    expr = str(p.get("expr", "")).strip()
    if not expr:
        return json.dumps({"ok": False, "error": "Enter an expression to evaluate."})
    defines, define_err = ui.parse_defines(p.get("defines") or "")
    if define_err:
        return json.dumps(ui._err(define_err))
    # The Conditions box (#96). The server splits and guards it in app.py;
    # here symbulator_ui does the reading, and the guards that matter are
    # its own -- there is no untrusted caller on this side of the wire.
    raw_conds = p.get("conditions") or ""
    if isinstance(raw_conds, list):
        conditions = [str(x).strip() for x in raw_conds if str(x).strip()]
    else:
        conditions = [ln.strip() for ln in str(raw_conds).splitlines()
                      if ln.strip()]
    if defines:
        expr = ui.expand_defines(expr, defines)
        conditions = [ui.expand_defines(c, defines) for c in conditions]
    return json.dumps(ui.evaluate_ui(expr, p.get("values") or {}, _digits(p),
                                     bool(p.get("si")), bool(p.get("approx")),
                                     str(p.get("domain", "")).strip().lower(),
                                     conditions, bool(p.get("dual"))))


def mini_tool(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/minitool: run one of the
    small version 7 helpers against the solved answers. Kept deliberately
    thin, like the others here -- every check that matters lives in
    symbulator_ui, so the offline build and the server cannot disagree
    about what an argument may contain."""
    p = json.loads(payload_json)
    tool = str(p.get("tool", "")).strip()
    args = [str(a or "").strip() for a in (p.get("args") or [])]
    return json.dumps(ui.mini_tool_ui(tool, args, p.get("values") or {},
                                      _digits(p) or 4))


def spice(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/spice: translate between
    Symbulator notation and a SPICE netlist (the SPICE Translator card,
    #160). Thin like the others -- the work and the warnings both live
    in symbulator_ui.spice_ui."""
    p = json.loads(payload_json)
    return json.dumps(ui.spice_ui(str(p.get("direction", "")).strip(),
                                  p.get("text", "")))


def solve_equations(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/solveq: solve user-
    supplied equations against known values, with no server round-trip."""
    p = json.loads(payload_json)
    raw = p.get("equations") or ""
    equations = ([str(x).strip() for x in raw if str(x).strip()]
                 if isinstance(raw, list)
                 else [ln.strip() for ln in ui.re.split(r"[\r\n]+", str(raw)) if ln.strip()])
    if not equations:
        return json.dumps({"ok": False, "error": "Enter at least one equation to solve."})
    unknowns = [u.strip() for u in
                ui.re.split(r"[,\s]+", str(p.get("unknowns") or "")) if u.strip()]
    raw_conds = p.get("conditions") or ""
    conditions = ([str(x).strip() for x in raw_conds if str(x).strip()]
                  if isinstance(raw_conds, list)
                  else [ln.strip() for ln in ui.re.split(r"[\r\n]+", str(raw_conds)) if ln.strip()])
    conditions = ui._expand_and(conditions)
    defines, define_err = ui.parse_defines(p.get("defines") or "")
    if define_err:
        return json.dumps(ui._err(define_err))
    if defines:
        equations = [ui.expand_defines(e, defines) for e in equations]
        conditions = [ui.expand_defines(c, defines) for c in conditions]
        unknowns = [ui.expand_defines(u, defines) for u in unknowns]
    return json.dumps(ui.solveq_ui(equations, unknowns, p.get("values") or {},
                                   _digits(p), bool(p.get("si")),
                                   bool(p.get("approx")), bool(p.get("units")),
                                   bool(p.get("real_only")), conditions,
                                   str(p.get("domain", "")).strip().lower(),
                                   bool(p.get("dual"))))


def parse_book(text: str) -> str:
    """JS-callable counterpart of app.py's /api/examples and /api/upload:
    parse circuit-book text (see circuitbook.py) straight from the
    browser, whether it's one of the bundled example files or a file the
    reader picked, with no server involved.

    The title comes back with the entries, as it does from the server, so
    the interface can label the file by what it calls itself rather than
    by its filename."""
    circuits, warnings, title = circuitbook.parse_book(text)
    if not circuits:
        # The server sends an `error` when nothing parses, and the page shows
        # it. Without one here the offline build fell back to a generic
        # "could not read that file" and dropped the warnings that say what
        # was actually wrong -- the same failure, explained less well.
        return json.dumps({
            "ok": False, "circuits": [], "warnings": warnings,
            "error": "No entries found in that file. Each entry needs a "
                     "[Name] heading followed by its circuit lines."})
    return json.dumps({"ok": True, "circuits": circuits,
                       "warnings": warnings, "title": title})


def export_book(payload_json: str) -> str:
    """Mirrors app.py's /api/export: renders the browser's live file of
    circuits as circuit-book text. Nothing is stored anywhere -- the
    list of circuits comes in whole with every call."""
    p = json.loads(payload_json)
    raw_circuits = p.get("circuits")
    if not isinstance(raw_circuits, list) or not raw_circuits:
        return json.dumps({"ok": False, "error": "Nothing to save yet."})

    circuits = []
    for raw in raw_circuits[:circuitbook.MAX_CIRCUITS]:
        if not isinstance(raw, dict):
            continue
        circuit = {"name": str(raw.get("name") or "Circuit")[:circuitbook.MAX_NAME_LEN],
                   "desc": str(raw.get("desc") or "")}
        for f in ("domain", "omega", "vars", "tool", "n1", "n2", "kind", "unknowns",
                  "plottool", "plotkey", "plotmin", "plotmax", "plotpoints",
                  "rounding", "evaluate", "solve_unknowns"):
            if raw.get(f):
                circuit[f] = str(raw[f])
        # Settings booleans -- always carried over (even when False), since
        # a saved circuit always has *some* Settings state, unlike the
        # "if present" fields above. "units" defaults to True (unlike the
        # other three): a circuit dict that never touched Settings at all
        # (e.g. parsed straight from a supplied example, which doesn't spell out
        # every default) means "show units", same as a fresh page load --
        # bool(None) would wrongly read that silence as "off".
        for f in ("si", "rms", "solve_real_only"):
            circuit[f] = bool(raw.get(f))
        circuit["units"] = bool(raw.get("units", True))
        # #237: `note` moved up here when it became repeatable -- one
        # paragraph per entry. Left among the scalars above it would
        # have been str()-ed into the literal text "['a', 'b']" and
        # written to the file that way.
        for f in ("equations", "conditions", "evaluate_conditions",
                  "solve_equations", "solve_conditions", "note"):
            items = raw.get(f)
            if isinstance(items, list):
                items = [str(x).strip() for x in items if str(x).strip()]
                if items:
                    circuit[f] = items
        if circuit["desc"].strip():
            circuits.append(circuit)

    if not circuits:
        return json.dumps({"ok": False, "error": "Nothing to save yet."})
    title = str(p.get("title") or "")[:circuitbook.MAX_TITLE_LEN]
    return json.dumps({"ok": True,
                       "text": circuitbook.format_book(circuits, title)})
