"""
Thin bridge between the Numerical Solver's page and `eqsheet`.

The same shape as bridge.py, and deliberately a separate file from it.
bridge.py imports symbulator_ui at module level, which pulls in the
whole solver package; the Numerical Solver needs none of that. Keeping
the two apart means the Solver page boots on Pyodide, SymPy, NumPy and
SciPy alone -- it never fetches the symbulator wheel, and the app page
never fetches SciPy.

eqsheet.py is the file the server runs, copied here verbatim by
build_local.py. Since #208 it knows nothing about Flask: dict in, dict
out. On the server eqsheet_web.py wraps these two functions in a
Blueprint; here they are wrapped in JSON, and that is the whole
difference between the hosted Solver and the downloaded one.
"""

import json

import eqsheet


def eq_parse(payload_json: str) -> str:
    """JS-callable counterpart of the server's /eqsheet/api/parse."""
    return json.dumps(eqsheet.api_parse(json.loads(payload_json)))


def eq_solve(payload_json: str) -> str:
    """JS-callable counterpart of the server's /eqsheet/api/solve."""
    return json.dumps(eqsheet.api_solve(json.loads(payload_json)))
