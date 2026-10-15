"""Shared helpers for the scripts. Run everything through `uv run`."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"

TOPICS = [
    "Array", "String", "Hash", "Two pointers", "Sliding window", "Stack", "Monotonic stack",
    "Binary search", "Linked list", "Tree", "Trie", "Heap", "Graph", "Intervals", "Matrix",
    "DP", "Greedy", "Backtracking", "Bit manipulation", "Design",
]
REQUIRED_FILES = ["solution.py", "skeleton.py", "tests.yaml", "description.md"]

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
