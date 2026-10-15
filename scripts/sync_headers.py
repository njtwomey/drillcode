"""uv run python scripts/sync_headers.py [--check]

Rewrites the module docstring of every problems/<slug>/solution.py from its index.yaml entry
(approach, tricks, edge cases, complexity), so the View mode of the web app shows them as a
comment at the top of the code. index.yaml is the source of truth: edit it, not the docstring.
Alternative approaches (solution_<variant>.py) keep their own hand-written docstring.
With --check, nothing is written and the exit status is 1 if any file is out of date.
"""

import ast
import sys
import textwrap

from _common import JUDGE_HEADER, PROBLEMS, judge_block, judge_notes, load_index, load_spec


def wrap(text, first, rest="    "):
    return textwrap.fill(text, width=88, initial_indent=first, subsequent_indent=rest)


def header(entry):
    lines = [f'{entry["title"]} (#{entry["number"]}, {entry["difficulty"]})', "",
             wrap(entry["summary"].rstrip("."), "Approach: ") + "."]
    if entry["tricks"].strip() != "None":
        lines.append(wrap(entry["tricks"].rstrip(".") , "Tricks: ") + ".")
    lines.append("Edge cases:")
    lines += [wrap(item, "  - ", "    ") for item in entry["edge_cases"]]
    lines.append("")
    lines.append(f'Time {entry["complexity"]["time"]}, space {entry["complexity"]["space"]}.')
    body = "\n".join(lines)
    assert '"""' not in body and "\\" not in body, entry["slug"]
    return f'"""{body}\n"""\n'


def rewrite(source, new_header):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    first = tree.body[0] if tree.body else None
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        start, end = first.lineno - 1, first.end_lineno
        return "".join(lines[:start]) + new_header + "".join(lines[end:])
    # No docstring: insert after any leading comment lines.
    at = 0
    while at < len(lines) and lines[at].startswith("#"):
        at += 1
    return "".join(lines[:at]) + new_header + "\n" + "".join(lines[at:])


def apply_notes(source, block):
    """Replace (or remove, or insert) the generated Judge notes block just after the module docstring."""
    lines = source.split("\n")
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    has_doc = isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str)
    start = first.end_lineno if has_doc else 0
    j = start
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and lines[j] == JUDGE_HEADER:
        k = j
        while k < len(lines) and lines[k].startswith("#"):
            k += 1
        j = k
        while j < len(lines) and lines[j].strip() == "":
            j += 1
    had_block = j > start and (start < len(lines)) and any(l == JUDGE_HEADER for l in lines[start:j])
    if not block and not had_block:
        return source  # nothing generated, nothing to remove: leave the file exactly as it is
    rest = lines[j:]
    head = lines[:start]
    if block:
        return "\n".join(head + [""] + block + ["", ""] + rest)
    return "\n".join(head + ["", ""] + rest) if head else "\n".join(rest)


def main():
    check = "--check" in sys.argv
    stale = []
    for entry in load_index():
        path = PROBLEMS / entry["slug"] / "solution.py"
        if not path.exists():
            continue
        old = path.read_text()
        new = rewrite(old, header(entry))
        spec = load_spec(entry["slug"])
        new = apply_notes(new, judge_block(judge_notes(spec, new)))
        if new != old:
            stale.append(entry["slug"])
            if not check:
                path.write_text(new)
    if stale:
        print(("out of date: " if check else "rewrote header of: ") + ", ".join(stale))
    sys.exit(1 if (check and stale) else 0)


if __name__ == "__main__":
    main()
