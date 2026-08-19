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
    conditions = lines("conditions")
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

    # --- i / I / j all mean the imaginary unit; settle on j, and say so ---
    desc, imaginary_notes = ui.normalise_imaginary(desc)

    # --- ambiguous bare suffixes: ask, then rewrite explicitly ---
    choices = {str(k): str(v) for k, v in (p.get("suffix_choices") or {}).items()
               if v in ("si", "var")}
    desc_used = desc.replace(":", "\n") if imaginary_notes else None
    try:
        from symbulator.elements import (parse_circuit, ambiguous_in_elements,
                                         _VALUE_FIELD_IDX)
        from symbulator.si_prefix import bare_suffix_match, _BARE_SUFFIX_EXP
        elements = parse_circuit(desc)
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
        desc = ":".join(e.name + "," + ",".join(e.fields) for e in elements)
        desc_used = desc.replace(":", "\n")

    res = ui.solve_ui(desc, domain, omega, variables or None, tool, n1, n2, kind,
                      equations, unknowns, conditions, _digits(p),
                      bool(p.get("si")), bool(p.get("units")),
                      bool(p.get("use_rms")), bool(p.get("approx")))
    # Attach the notes either way: when the solve fails, "normalised
    # '5*i' to '5j'" is often the explanation for the error underneath.
    res["notes"] = imaginary_notes + list(res.get("notes") or [])
    if res.get("ok"):
        res.update({"domain": domain, "tool": tool, "desc_used": desc_used,
                    "digits": _digits(p), "si": bool(p.get("si")),
                    "units": bool(p.get("units")),
                    "use_rms": bool(p.get("use_rms")),
                    "approx": bool(p.get("approx"))})
    return json.dumps(res)


def evaluate(payload_json: str) -> str:
    """JS-callable counterpart of app.py's /api/evaluate: substitute the
    posted values into `expr` and format the result, with no server
    round-trip."""
    p = json.loads(payload_json)
    expr = str(p.get("expr", "")).strip()
    if not expr:
        return json.dumps({"ok": False, "error": "Enter an expression to evaluate."})
    return json.dumps(ui.evaluate_ui(expr, p.get("values") or {}, _digits(p),
                                     bool(p.get("si")), bool(p.get("approx"))))


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
    return json.dumps(ui.solveq_ui(equations, unknowns, p.get("values") or {},
                                   _digits(p), bool(p.get("si")),
                                   bool(p.get("approx")), bool(p.get("units")),
                                   bool(p.get("real_only"))))


def parse_book(text: str) -> str:
    """JS-callable counterpart of app.py's /api/examples and /api/upload:
    parse circuit-book text (see circuitbook.py) straight from the
    browser, whether it's the bundled examples.sym or a file the user
    picked, with no server involved."""
    circuits, warnings = circuitbook.parse_book(text)
    return json.dumps({"ok": bool(circuits), "circuits": circuits,
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
        for f in ("domain", "omega", "vars", "tool", "n1", "n2", "kind", "unknowns"):
            if raw.get(f):
                circuit[f] = str(raw[f])
        for f in ("equations", "conditions"):
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
