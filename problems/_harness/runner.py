"""Test harness shared by the CLI (scripts/run_tests.py) and the browser (Pyodide worker).

Standard library only. It never reads files: callers pass the solution source,
the parsed tests.yaml (`spec`), one `case`, and optionally the validator source.
The scaffold modules (linked_list, tree, graph) must be importable.
"""

import contextlib
import copy
import importlib
import io
import json
import math
import time
import traceback
import types
from typing import Dict, List, Optional, Set, Tuple

# Names each scaffold module contributes to the solution namespace.
SCAFFOLD_NAMES = {
    "linked_list": ["ListNode", "Node"],
    "tree": ["TreeNode"],
    "graph": ["Node"],
}


class CaseTimeout(BaseException):
    """Raised by the CLI's alarm handler. BaseException so `except Exception` in user code cannot hide it."""


def _module(name):
    return importlib.import_module(name)


def build_namespace(spec):
    namespace = {
        "__name__": "solution",
        "List": List,
        "Optional": Optional,
        "Dict": Dict,
        "Set": Set,
        "Tuple": Tuple,
    }
    for scaffold in spec.get("scaffolds", []):
        module = _module(scaffold)
        for name in SCAFFOLD_NAMES[scaffold]:
            namespace[name] = getattr(module, name)
    return namespace


# ---- conversion between JSON and scaffold objects ------------------------------------------

def _convert_in(conv, value, case_input, args):
    """JSON -> object. `args` holds the arguments built so far (for tree_node)."""
    if conv == "linked_list":
        return _module("linked_list").build_list(value)
    if conv == "linked_list_array":
        build = _module("linked_list").build_list
        return [build(v) for v in value]
    if conv.startswith("linked_list_cycle:"):
        pos = case_input[conv.split(":", 1)[1]]
        return _module("linked_list").build_list(value, pos)
    if conv == "random_list":
        return _module("linked_list").build_random_list(value)
    if conv == "tree":
        return _module("tree").build_tree(value)
    if conv == "graph":
        return _module("graph").build_graph(value)
    if conv.startswith("tree_node:"):
        root = args[conv.split(":", 1)[1]]
        return _module("tree").find_node(root, value)
    raise ValueError(f"unknown input converter {conv!r}")


def _convert_out(conv, value):
    """Object -> JSON-able value."""
    if conv in (None, ""):
        return value
    if conv == "linked_list":
        return _module("linked_list").list_to_array(value)
    if conv == "random_list":
        return _module("linked_list").random_list_to_array(value)
    if conv == "tree":
        return _module("tree").tree_to_array(value)
    if conv == "graph":
        return _module("graph").graph_to_adjacency(value)
    if conv == "node_val":
        return None if value is None else value.val
    raise ValueError(f"unknown output converter {conv!r}")


def to_json(value):
    """Normalise to plain JSON types (tuples -> lists, sets -> sorted lists)."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [to_json(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((to_json(v) for v in value), key=_sort_key)
    if isinstance(value, dict):
        return {str(k): to_json(v) for k, v in value.items()}
    raise TypeError(f"result of type {type(value).__name__} is not JSON-serialisable")


# ---- comparison -----------------------------------------------------------------------------

def _sort_key(value):
    return json.dumps(value, sort_keys=True)


def _close(a, b, tol):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return math.isclose(a, b, rel_tol=0, abs_tol=tol)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_close(x, y, tol) for x, y in zip(a, b))
    return a == b


def _compare(mode, actual, expected):
    if mode == "unordered":
        if isinstance(actual, list) and isinstance(expected, list):
            return sorted(actual, key=_sort_key) == sorted(expected, key=_sort_key)
        return actual == expected
    if mode == "unordered_nested":
        def norm(x):
            return sorted((sorted(inner, key=_sort_key) for inner in x), key=_sort_key)
        return norm(actual) == norm(expected)
    if mode.startswith("float:"):
        return _close(actual, expected, float(mode.split(":", 1)[1]))
    return actual == expected


# ---- running --------------------------------------------------------------------------------

def run_case(solution_source, spec, case, validator_source=None):
    """Run one case and return a plain dict. Never raises (except SystemExit/KeyboardInterrupt)."""
    out, err = io.StringIO(), io.StringIO()
    result = {
        "name": case.get("name", ""),
        "status": "error",
        "ms": 0.0,
        "expected": case.get("expected"),
        "actual": None,
        "message": "",
        "stdout": "",
        "stderr": "",
    }
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            namespace = build_namespace(spec)
            exec(compile(solution_source, "solution.py", "exec"), namespace)
            if spec.get("kind") == "operations":
                _run_operations(namespace, spec, case, result)
            else:
                _run_function(namespace, spec, case, result, validator_source)
    except CaseTimeout:
        result["status"] = "timeout"
        result["message"] = "Time limit exceeded"
    except Exception:
        result["status"] = "error"
        result["message"] = traceback.format_exc()
    result["stdout"] = out.getvalue()
    result["stderr"] = err.getvalue()
    return result


def run_case_json(solution_source, spec_json, case_json, validator_source=None):
    """String-in, string-out wrapper for the Pyodide worker."""
    result = run_case(solution_source, json.loads(spec_json), json.loads(case_json), validator_source)
    return json.dumps(result)


def _resolve_entry(namespace, entry):
    target = namespace[entry.split(".")[0]]
    if "." not in entry:
        return target
    cls_name, method = entry.split(".", 1)
    return getattr(target(), method)


def _run_function(namespace, spec, case, result, validator_source):
    convert = spec.get("convert", {}) or {}
    mode = str(spec.get("compare", "exact"))
    case_input = case.get("input", {})

    entry = _resolve_entry(namespace, spec["entry"])

    # Arguments needing another argument (tree_node:) are built after the rest.
    args = {}
    for name in spec["args"]:
        conv = convert.get(name)
        if conv and conv.startswith("tree_node:"):
            continue
        args[name] = _convert_in(conv, case_input[name], case_input, args) if conv else copy.deepcopy(case_input[name])
    for name in spec["args"]:
        if name not in args:
            args[name] = _convert_in(convert[name], case_input[name], case_input, args)

    ordered = [args[name] for name in spec["args"]]
    raw = None
    if spec.get("call", True):
        start = time.perf_counter()
        try:
            raw = entry(*ordered)
        finally:
            result["ms"] = (time.perf_counter() - start) * 1000

    if mode == "validator":
        namespace_v = {}
        exec(compile(validator_source or "", "validator.py", "exec"), namespace_v)
        scaffolds = types.SimpleNamespace(**{n: _module(n) for n in spec.get("scaffolds", [])})
        full_case = dict(case, args=args, entry=entry)
        ok, message = namespace_v["validate"](raw, full_case, scaffolds)
        result["actual"] = to_json(_convert_out(convert.get("result"), raw)) if raw is not None else None
        result["status"] = "pass" if ok else "fail"
        result["message"] = "" if ok else str(message)
        return

    if mode.startswith("in_place:"):
        name = mode.split(":", 1)[1]
        actual = to_json(_convert_out(convert.get(name), args[name]))
    else:
        actual = to_json(_convert_out(convert.get("result"), raw))
    result["actual"] = actual
    expected = to_json(case.get("expected"))
    ok = _compare(mode, actual, expected)
    result["status"] = "pass" if ok else "fail"
    if not ok:
        result["message"] = "Output does not match expected"


def _run_operations(namespace, spec, case, result):
    ops = case["ops"]
    mode = str(spec.get("compare", "exact"))
    instance = None
    actual = []
    elapsed = 0.0
    try:
        for index, (name, op_args) in enumerate(ops):
            start = time.perf_counter()
            try:
                if index == 0:
                    instance = namespace[name](*copy.deepcopy(op_args))
                    value = None
                else:
                    value = getattr(instance, name)(*copy.deepcopy(op_args))
            finally:
                elapsed += (time.perf_counter() - start) * 1000
            actual.append(to_json(value))
    finally:
        result["ms"] = elapsed
        result["actual"] = actual
    expected = to_json(case.get("expected"))
    ok = _compare(mode, actual, expected)
    result["status"] = "pass" if ok else "fail"
    if not ok:
        for i, (a, e) in enumerate(zip(actual, expected)):
            if not _compare(mode, a, e):
                result["message"] = f"First difference at op {i} ({ops[i][0]}): expected {e!r}, got {a!r}"
                break
        else:
            result["message"] = "Output length differs from expected"
