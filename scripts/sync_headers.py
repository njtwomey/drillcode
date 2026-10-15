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

from _common import PROBLEMS, load_index


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


def main():
    check = "--check" in sys.argv
    stale = []
    for entry in load_index():
        path = PROBLEMS / entry["slug"] / "solution.py"
        if not path.exists():
            continue
        old = path.read_text()
        new = rewrite(old, header(entry))
        if new != old:
            stale.append(entry["slug"])
            if not check:
                path.write_text(new)
    if stale:
        print(("out of date: " if check else "rewrote header of: ") + ", ".join(stale))
    sys.exit(1 if (check and stale) else 0)


if __name__ == "__main__":
    main()
