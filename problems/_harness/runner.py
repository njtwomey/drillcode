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
import linecache
import math
import sys
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

USER_FILE = "solution.py"


class CaseError(Exception):
    """An error whose message is already written for the reader (it is shown as-is).
    `line` is the line of solution.py the error points at, when there is one."""

    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line


def _user_frames(exc):
    return [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == USER_FILE]


def _user_line(exc):
    """The line of solution.py where the error happened: the innermost frame of the reader's code."""
    if isinstance(exc, SyntaxError) and exc.filename == USER_FILE:
        return exc.lineno
    frames = _user_frames(exc)
    return frames[-1].lineno if frames else None


def _user_traceback(exc):
    """A traceback with only the frames from the reader's own code."""
    frames = _user_frames(exc)
    if len(frames) > 8:  # deep recursion: keep the ends
        skipped = len(frames) - 7
        frames = frames[:3] + [None] + frames[-4:]
    lines = ["Traceback (most recent call last):"]
    for f in frames:
        if f is None:
            lines.append(f"  ... {skipped} more calls ...")
            continue
        lines.append(f'  File "{USER_FILE}", line {f.lineno}, in {f.name}')
        if f.line:
            lines.append("    " + f.line.strip())
    lines.append("".join(traceback.format_exception_only(type(exc), exc)).strip())
    return "\n".join(lines)


def _explain(exc, context):
    """Message for an exception that escaped while `context` was running: the reader's frames if
    their code was involved, otherwise a one-line description (no harness internals)."""
    if isinstance(exc, SyntaxError) and exc.filename == USER_FILE:
        return "Syntax error in your code:\n" + "".join(traceback.format_exception_only(type(exc), exc)).strip()
    if _user_frames(exc):
        return _user_traceback(exc)
    return f"{context}: {type(exc).__name__}: {exc}"


def needed_inputs(spec):
    """Input names a case must provide: the arguments, extras the checker reads, converter extras."""
    names = list(spec.get("args") or [])
    for name in (spec.get("extra_inputs") or {}):
        if name not in names:
            names.append(name)
    for conv in (spec.get("convert") or {}).values():
        if ":" in str(conv):
            extra = str(conv).split(":", 1)[1]
            if extra not in names and not str(conv).startswith("tree_node:"):
                names.append(extra)
    return names


def run_case(solution_source, spec, case, validator_source=None, reference_source=None):
    """Run one case and return a plain dict. Never raises (except SystemExit/KeyboardInterrupt).

    If the case has no `expected` key and `reference_source` is given, the expected value is what the
    reference solution returns for the same input."""
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
        "expected_source": None,
        "error_line": None,
    }
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            if "expected" not in case and reference_source is not None:
                case, result["expected"], result["expected_source"] = _derive_expected(spec, case, reference_source)
            namespace = build_namespace(spec)
            # Register the source so tracebacks can show the offending line of the reader's code.
            linecache.cache[USER_FILE] = (len(solution_source), None, solution_source.splitlines(True), USER_FILE)
            try:
                exec(compile(solution_source, USER_FILE, "exec"), namespace)
            except Exception as e:
                raise CaseError(_explain(e, "Your code failed while loading"), _user_line(e)) from None
            if spec.get("kind") == "operations":
                _run_operations(namespace, spec, case, result)
            else:
                _run_function(namespace, spec, case, result, validator_source)
    except CaseTimeout:
        result["status"] = "timeout"
        result["message"] = "Time limit exceeded"
        result["error_line"] = _user_line(sys.exc_info()[1])
    except CaseError as e:
        result["status"] = "error"
        result["message"] = str(e)
        result["error_line"] = e.line
    except Exception as e:
        # Not the reader's problem: a bug in the harness or a checker. Keep the full traceback to debug it.
        result["status"] = "error"
        result["error_line"] = _user_line(e)
        result["message"] = (
            _user_traceback(e) if _user_frames(e)
            else "Internal error in the test harness (not your code):\n" + traceback.format_exc()
        )
    result["stdout"] = out.getvalue()
    result["stderr"] = err.getvalue()
    return result


def _one_line(message):
    """The gist of an error message: the exception line of a traceback, or the sentence itself."""
    lines = [line.strip() for line in str(message).splitlines() if line.strip()]
    if not lines:
        return "unknown error"
    if lines[0].startswith("Traceback"):
        return lines[-1]
    return lines[0] if len(lines) == 1 else f"{lines[0]}: {lines[-1]}"


def _derive_expected(spec, case, reference_source):
    """Run the reference solution on the case's input and use its answer as the expected value."""
    ref_spec = dict(spec, call=True)
    if str(spec.get("compare", "")) == "validator":
        ref_spec["compare"] = "exact"  # we only want its output, not a verdict
    placeholder = [] if spec.get("kind") == "operations" else None
    ref = run_case(reference_source, ref_spec, dict(case, expected=placeholder))
    if ref["status"] in ("error", "timeout"):
        # One line, no traceback: the frames would be the reference solution's own code, not the reader's.
        raise CaseError(
            f"No expected value was given, and the reference solution could not answer this input ({_one_line(ref['message'])}). "
            "Check that each value has the right type and is within the problem's limits, or fill in the expected value yourself."
        )
    return dict(case, expected=ref["actual"]), ref["actual"], "reference"


def run_case_json(solution_source, spec_json, case_json, validator_source=None, reference_source=None):
    """String-in, string-out wrapper for the Pyodide worker."""
    result = run_case(solution_source, json.loads(spec_json), json.loads(case_json), validator_source, reference_source)
    return json.dumps(result)


def _resolve_entry(namespace, entry):
    cls_name, _, method = entry.partition(".")
    if cls_name not in namespace:
        hint = f" with a method {method}" if method else ""
        raise CaseError(f"Your code does not define {cls_name}. Define class {cls_name}{hint}.")
    target = namespace[cls_name]
    if not method:
        return target
    try:
        instance = target()
    except Exception as e:
        raise CaseError(_explain(e, f"Creating {cls_name}() failed"), _user_line(e)) from None
    if not hasattr(instance, method):
        raise CaseError(f"Your class {cls_name} has no method {method}.")
    return getattr(instance, method)


def _run_function(namespace, spec, case, result, validator_source):
    convert = spec.get("convert", {}) or {}
    mode = str(spec.get("compare", "exact"))
    case_input = case.get("input", {})

    entry = _resolve_entry(namespace, spec["entry"])

    needed = needed_inputs(spec)
    missing = [n for n in needed if n not in case_input]
    if missing:
        raise CaseError(
            f"This case is missing input value(s): {', '.join(missing)}. "
            f"Every case for this problem needs: {', '.join(needed)}."
        )

    # Arguments needing another argument (tree_node:) are built after the rest.
    args = {}
    building = None
    try:
        for name in spec["args"]:
            building = name
            conv = convert.get(name)
            if conv and conv.startswith("tree_node:"):
                continue
            args[name] = _convert_in(conv, case_input[name], case_input, args) if conv else copy.deepcopy(case_input[name])
        for name in spec["args"]:
            building = name
            if name not in args:
                args[name] = _convert_in(convert[name], case_input[name], case_input, args)
    except Exception as e:
        raise CaseError(f"Could not build the input {building!r} from {case_input.get(building)!r}: {type(e).__name__}: {e}") from None

    ordered = [args[name] for name in spec["args"]]
    raw = None
    if spec.get("call", True):
        start = time.perf_counter()
        try:
            raw = entry(*ordered)
        except Exception as e:
            raise CaseError(_explain(e, "Could not call your function"), _user_line(e)) from None
        finally:
            result["ms"] = (time.perf_counter() - start) * 1000

    if mode == "validator":
        try:
            namespace_v = {}
            exec(compile(validator_source or "", "validator.py", "exec"), namespace_v)
            scaffolds = types.SimpleNamespace(**{n: _module(n) for n in spec.get("scaffolds", [])})
            full_case = dict(case, args=args, entry=entry)
            ok, message = namespace_v["validate"](raw, full_case, scaffolds)
        except Exception as e:
            if _user_frames(e):  # the checker ran the reader's code and it failed
                raise CaseError(_explain(e, ""), _user_line(e)) from None
            hint = f" It needs an input value named {e.args[0]!r}; a case you added may be missing it." if isinstance(e, KeyError) and e.args else ""
            raise CaseError(
                f"The checker for this problem could not judge this case ({type(e).__name__}: {e}).{hint} "
                f"Inputs for this problem: {', '.join(needed)}."
            ) from None
        try:
            result["actual"] = to_json(_convert_out(convert.get("result"), raw)) if raw is not None else None
        except Exception:
            result["actual"] = None
        result["status"] = "pass" if ok else "fail"
        result["message"] = "" if ok else str(message)
        return

    try:
        if mode.startswith("in_place:"):
            name = mode.split(":", 1)[1]
            actual = to_json(_convert_out(convert.get(name), args[name]))
        else:
            actual = to_json(_convert_out(convert.get("result"), raw))
    except Exception as e:
        what = f"the modified {mode.split(':', 1)[1]}" if mode.startswith("in_place:") else "the returned value"
        raise CaseError(f"Could not read {what} to compare it: {type(e).__name__}: {e}") from None
    result["actual"] = actual
    try:
        expected = to_json(case.get("expected"))
    except Exception as e:
        raise CaseError(f"The expected value is not usable: {type(e).__name__}: {e}") from None
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
            call = f"{name}({', '.join(map(repr, op_args))})"
            try:
                if index == 0:
                    if name not in namespace:
                        raise CaseError(f"Your code does not define {name}. Define class {name}.")
                    instance = namespace[name](*copy.deepcopy(op_args))
                    value = None
                else:
                    if not hasattr(instance, name):
                        raise CaseError(f"Call {index + 1} of {len(ops)}: your class has no method {name}.")
                    value = getattr(instance, name)(*copy.deepcopy(op_args))
            except CaseError:
                raise
            except Exception as e:
                raise CaseError(f"Error in call {index + 1} of {len(ops)}: {call}\n" + _explain(e, "It raised"), _user_line(e)) from None
            finally:
                elapsed += (time.perf_counter() - start) * 1000
            try:
                actual.append(to_json(value))
            except Exception as e:
                raise CaseError(f"Call {index + 1} of {len(ops)}, {call}, returned something the tests cannot compare: {e}") from None
    finally:
        result["ms"] = elapsed
        result["actual"] = actual
    expected = to_json(case.get("expected"))
    ok = _compare(mode, actual, expected)
    result["status"] = "pass" if ok else "fail"
    if not ok and not isinstance(expected, list):
        result["message"] = "The expected value for a design problem must be a list with one result per call."
    elif not ok:
        for i, (a, e) in enumerate(zip(actual, expected)):
            if not _compare(mode, a, e):
                result["message"] = f"First difference at op {i} ({ops[i][0]}): expected {e!r}, got {a!r}"
                break
        else:
            result["message"] = "Output length differs from expected"
