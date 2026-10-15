"""uv run python scripts/check_catalogue.py  -- validate index.yaml against problems/ directories."""

import ast
import sys

from _common import PROBLEMS, REQUIRED_FILES, TOPICS, load_index, load_spec, problem_dirs, solution_files

DIFFICULTIES = {"easy", "medium", "hard"}
FIELDS = ["slug", "number", "title", "difficulty", "topic", "tags", "blind75", "premium",
          "leetcode", "summary", "tricks", "edge_cases", "complexity"]


def defined_names(source):
    tree = ast.parse(source)
    classes = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes[node.name] = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
    return classes


def main():
    errors = []
    index = load_index()
    slugs = [e["slug"] for e in index]
    if len(set(slugs)) != len(slugs):
        errors.append("duplicate slugs in index.yaml")
    dirs = set(problem_dirs())

    for slug in sorted(set(slugs) - dirs):
        errors.append(f"{slug}: in index.yaml but has no directory")
    for slug in sorted(dirs - set(slugs)):
        errors.append(f"{slug}: directory has no index.yaml entry")

    for entry in index:
        slug = entry["slug"]
        for field in FIELDS:
            if field not in entry:
                errors.append(f"{slug}: missing field {field}")
        if entry.get("difficulty") not in DIFFICULTIES:
            errors.append(f"{slug}: bad difficulty {entry.get('difficulty')!r}")
        for topic in [entry.get("topic")] + list(entry.get("tags") or []):
            if topic not in TOPICS:
                errors.append(f"{slug}: topic/tag {topic!r} is not on the fixed list")
        if not str(entry.get("leetcode", "")).endswith(f"/problems/{slug}/"):
            errors.append(f"{slug}: leetcode link does not match slug")
        if slug not in dirs:
            continue
        directory = PROBLEMS / slug
        missing = [f for f in REQUIRED_FILES if not (directory / f).exists()]
        for f in missing:
            errors.append(f"{slug}: missing {f}")
        if missing:
            continue
        spec = load_spec(slug)
        if spec.get("compare") == "validator" and not (directory / "validator.py").exists():
            errors.append(f"{slug}: compare is validator but validator.py is missing")
        if "entry" not in spec:
            errors.append(f"{slug}: tests.yaml has no entry")
            continue
        cls, _, method = spec["entry"].partition(".")
        for path in solution_files(slug):
            try:
                classes = defined_names(path.read_text())
            except SyntaxError as e:
                errors.append(f"{slug}: {path.name} does not parse: {e}")
                continue
            if cls not in classes:
                errors.append(f"{slug}: {path.name} does not define class {cls}")
            elif method and method not in classes[cls]:
                errors.append(f"{slug}: {path.name}: {cls} has no method {method}")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) found")
        sys.exit(1)
    print(f"catalogue OK: {len(index)} problems")


if __name__ == "__main__":
    main()
