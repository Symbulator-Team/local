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

    variables = [v.strip() for v in
                 ui.re.split(r"[,\s]+", str(p.get("variables") or "")) if v.strip()]
    equations = lines("equations")
    # "vin = 12 and pr2 = 0" is one line naming two conditions -- expand
    # before validating/solving, matching app.py's /api/solve.
    conditions = ui._expand_and(lines("conditions"))
    unknowns = [u.strip() for u in
                ui.re.split(r"[,\s]+", str(p.get("unknowns") or "")) if u.strip()]

    err = ui._validate(desc, domain, omega, variables or None)
    if not err:
        err = ui._validate_extras(equations, unknowns, conditions)
    if not err and tool != "solve":
        if domain not in ("dc", "ac"):
            err = "Thevenin / impedance / two-port tools work in DC or AC only."
        elif not (n1 and n2):
            err = "Give the two port nodes (n1 and n2) for this tool."
    if err:
        return json.dumps({"ok": False, "error": err})

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
        return json.dumps({"ok": False, "error": ui._exc_text(exc)})

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

    # Always echo the circuit back one element per line, same as app.py's
    # /api/solve -- consistent every time you run, not just on the two
    # occasions (imaginary-unit normalizing, an ambiguous suffix being
    # resolved) that used to trigger it.
    desc = ":".join(e.name + "," + ",".join(e.fields) for e in elements)
    desc_used = desc.replace(":", "\n")

    res = ui.solve_ui(desc, domain, omega, variables or None, tool, n1, n2, kind,
                      equations, unknowns, conditions, _digits(p),
                      bool(p.get("si")), bool(p.get("units")),
                      bool(p.get("use_rms")), bool(p.get("approx")),
                      bool(p.get("polar")))
    # Attach the notes either way: when the solve fails, "normalised
    # '5*i' to '5j'" is often the explanation for the error underneath.
    res["notes"] = imaginary_notes + list(res.get("notes") or [])
    if res.get("ok"):
        # "approx"/"approx_forced" are left as solve_ui set them, not
        # overwritten with the request's original value -- solve_ui may
        # have switched exact to approximate itself, and the UI needs to
        # see that, not what was originally asked for.
        res.update({"domain": domain, "tool": tool, "desc_used": desc_used,
                    "digits": _digits(p), "si": bool(p.get("si")),
                    "units": bool(p.get("units")),
                    "use_rms": bool(p.get("use_rms")),
                    "polar": bool(p.get("polar"))})
    return json.dumps(res)


_VALID_PLOT_TOOLS = {"time", "bode"}
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
    for the "Plot vs. time" / "Bode plot" tools, with no server
    round-trip. Needs NumPy (see symbulator.plotting's module docstring
    for why it's not vendored by default) -- until a NumPy wheel is
    added to vendor/, this returns a friendly error rather than solving,
    same as it would for any other missing package."""
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

    extra_equations = lines("equations")
    extra_conditions = ui._expand_and(lines("conditions"))
    extra_unknowns = [u.strip() for u in
                      ui.re.split(r"[,\s]+", str(p.get("unknowns") or "")) if u.strip()]

    err = None
    if not desc:
        err = "Please enter a circuit description."
    elif tool not in _VALID_PLOT_TOOLS:
        err = "Unknown plot tool."
    elif not key or not ui._VARNAME.match(key):
        err = "Give a variable to plot, e.g. v_2 or i_r1."
    elif not (2 <= n <= MAX_PLOT_POINTS):
        err = f"Number of points must be between 2 and {MAX_PLOT_POINTS}."
    if not err:
        err = ui._validate_extras(extra_equations, extra_unknowns, extra_conditions)
    if err:
        return json.dumps({"ok": False, "error": err})

    if tool == "time":
        t_min, t_max, rng_err = _clean_range(p, 0.0, 1.0)
        if rng_err:
            return json.dumps({"ok": False, "error": rng_err})
        res = ui.plot_time_ui(desc, key, t_min, t_max, n,
                              extra_equations, extra_unknowns, extra_conditions)
    else:
        f_min, f_max, rng_err = _clean_range(p, 1.0, 1000.0)
        if rng_err:
            return json.dumps({"ok": False, "error": rng_err})
        if f_min <= 0 or f_max <= 0:
            return json.dumps({"ok": False, "error": "Bode frequencies must be positive (Hz)."})
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
    # The Conditions box (#96). The server splits and guards it in app.py;
    # here symbulator_ui does the reading, and the guards that matter are
    # its own -- there is no untrusted caller on this side of the wire.
    raw_conds = p.get("conditions") or ""
    if isinstance(raw_conds, list):
        conditions = [str(x).strip() for x in raw_conds if str(x).strip()]
    else:
        conditions = [ln.strip() for ln in str(raw_conds).splitlines()
                      if ln.strip()]
    return json.dumps(ui.evaluate_ui(expr, p.get("values") or {}, _digits(p),
                                     bool(p.get("si")), bool(p.get("approx")),
                                     str(p.get("domain", "")).strip().lower(),
                                     conditions))


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
    return json.dumps(ui.solveq_ui(equations, unknowns, p.get("values") or {},
                                   _digits(p), bool(p.get("si")),
                                   bool(p.get("approx")), bool(p.get("units")),
                                   bool(p.get("real_only")), conditions,
                                   str(p.get("domain", "")).strip().lower()))


def parse_book(text: str) -> str:
    """JS-callable counterpart of app.py's /api/examples and /api/upload:
    parse circuit-book text (see circuitbook.py) straight from the
    browser, whether it's the bundled examples.cir or a file the user
    picked, with no server involved."""
    circuits, warnings = circuitbook.parse_book(text)
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
                       "warnings": warnings})


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
                  "note", "plottool", "plotkey", "plotmin", "plotmax", "plotpoints",
                  "rounding", "evaluate", "solve_unknowns"):
            if raw.get(f):
                circuit[f] = str(raw[f])
        # Settings booleans -- always carried over (even when False), since
        # a saved circuit always has *some* Settings state, unlike the
        # "if present" fields above. "units" defaults to True (unlike the
        # other three): a circuit dict that never touched Settings at all
        # (e.g. parsed straight from examples.cir, which doesn't spell out
        # every default) means "show units", same as a fresh page load --
        # bool(None) would wrongly read that silence as "off".
        for f in ("si", "rms", "solve_real_only"):
            circuit[f] = bool(raw.get(f))
        circuit["units"] = bool(raw.get("units", True))
        for f in ("equations", "conditions", "evaluate_conditions",
                  "solve_equations", "solve_conditions"):
            items = raw.get(f)
            if isinstance(items, list):
                items = [str(x).strip() for x in items if str(x).strip()]
                if items:
                    circuit[f] = items
        if circuit["desc"].strip():
            circuits.append(circuit)

    if not circuits:
        return json.dumps({"ok": False, "error": "Nothing to save yet."})
    return json.dumps({"ok": True, "text": circuitbook.format_book(circuits)})
