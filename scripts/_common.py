"""Shared helpers for the scripts. Run everything through `uv run`."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"

TOPICS = [
    "Array",
    "Backtracking",
    "Binary search",
    "Bit manipulation",
    "Design",
    "Dynamic programming",
    "Graph",
    "Greedy",
    "Hash",
    "Heap",
    "Intervals",
    "Linked list",
    "Maths",
    "Matrix",
    "Monotonic stack",
    "Sliding window",
    "Stack",
    "String",
    "Tree",
    "Trie",
    "Two pointers",
]
REQUIRED_FILES = ["solution.py", "skeleton.py", "tests.yaml", "description.md", "walkthrough.md"]

# The harness imports the scaffolds as flat top-level modules.
sys.path.insert(0, str(PROBLEMS / "_scaffolds"))
sys.path.insert(0, str(PROBLEMS / "_harness"))


def load_index():
    return yaml.safe_load((PROBLEMS / "index.yaml").read_text())


def load_spec(slug):
    return yaml.safe_load((PROBLEMS / slug / "tests.yaml").read_text())


def read_optional(path):
    return path.read_text() if path.exists() else None


def problem_dirs():
    return sorted(p.name for p in PROBLEMS.iterdir() if p.is_dir() and not p.name.startswith("_"))


def solution_files(slug):
    """solution.py first, then alternative approaches as solution_<variant>.py."""
    directory = PROBLEMS / slug
    return [directory / "solution.py", *sorted(directory.glob("solution_*.py"))]


def variant_label(path):
    return "primary" if path.name == "solution.py" else path.stem.removeprefix("solution_")


JUDGE_HEADER = "# Judge notes:"


def judge_notes(spec, source):
    """Lines (no leading '# ') describing what the judge provides or expects beyond the signature.

    - `provided:` in tests.yaml, verbatim (injected APIs such as isBadVersion, custom judges, Codec usage);
    - a modify-in-place reminder for compare: in_place:<arg>;
    - for `kind: operations`, how the class is instantiated and called, from the entry class's methods.
    """
    import ast

    notes = [line.rstrip() for line in str(spec.get("provided", "")).strip().splitlines() if line.strip()]
    compare = str(spec.get("compare", ""))
    if compare.startswith("in_place:"):
        notes.append(f"Do not return anything: modify {compare.split(':', 1)[1]} in place instead.")
    if spec.get("kind") == "operations":
        cls = next(
            (n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == spec["entry"]), None
        )
        if cls is not None:
            def params(fn):
                return ", ".join(a.arg for a in fn.args.args if a.arg != "self")

            methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
            init = next((m for m in methods if m.name == "__init__"), None)
            notes += [
                f"Your {cls.name} object will be instantiated and called as such:",
                f"obj = {cls.name}({params(init) if init else ''})",
            ]
            count = 0
            for m in (m for m in methods if not m.name.startswith("_")):
                returns_value = m.returns is not None and not (isinstance(m.returns, ast.Constant) and m.returns.value is None)
                if returns_value:
                    count += 1
                    notes.append(f"param_{count} = obj.{m.name}({params(m)})")
                else:
                    notes.append(f"obj.{m.name}({params(m)})")
    return notes


def judge_block(notes):
    """The comment block for a file, or an empty list."""
    return [JUDGE_HEADER] + [f"# {line}" for line in notes] if notes else []
