"""uv run python scripts/check_techniques.py  -- validate techniques/*.md against the catalogue.

Fails if: frontmatter or a required field is missing; a `problems` entry is not a catalogue slug;
a `related` entry is not a technique; a `topics` entry is off the fixed list; the seven headings
are missing, out of order or joined by extra headings; a Python block does not parse; the Template
is not a function; the Worked example does not name a problem or shows code that is not in that
problem's solution; or any catalogue problem is listed by no technique.
"""

import ast
import re
import sys

import yaml

from _common import PROBLEMS, ROOT, TOPICS, load_index

TECHNIQUES = ROOT / "techniques"
AREAS = [
    "Linked lists",
    "Pointers and windows",
    "Hashing and counting",
    "Stacks",
    "Binary search",
    "Trees",
    "Graphs",
    "Backtracking",
    "Divide and conquer",
    "Heaps",
    "Intervals",
    "Dynamic programming",
    "Greedy",
    "Matrices",
    "Math",
    "Bits",
    "Tries",
    "Design",
]
HEADINGS = [
    "Reach for it when", "Setup", "Template", "What it removes", "Pitfalls", "Variants", "Worked example",
]
REQUIRED = ["title", "area", "topics", "problems", "related"]
FENCE = re.compile(r"^```(\w*)\s*$")


def split_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), match.group(2)


def scan_body(body):
    """Return (headings, sections, code_blocks): headings outside fences, body text and python blocks per heading."""
    headings, blocks = [], []
    current = None
    in_fence, lang, buf = False, "", []
    sections = {}
    for line in body.split("\n"):
        fence = FENCE.match(line)
        if fence and not in_fence:
            in_fence, lang, buf = True, fence.group(1), []
            continue
        if in_fence and line.strip() == "```":
            in_fence = False
            blocks.append((current, lang, "\n".join(buf)))
            continue
        if in_fence:
            buf.append(line)
            continue
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if heading:
            headings.append((len(heading.group(1)), heading.group(2)))
            current = heading.group(2)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return headings, {k: "\n".join(v) for k, v in sections.items()}, blocks


def stripped_lines(source):
    return [line.strip() for line in ast.unparse(ast.parse(source)).splitlines() if line.strip()]


def contains_sequence(haystack, needle):
    n = len(needle)
    return n > 0 and any(haystack[i:i + n] == needle for i in range(len(haystack) - n + 1))


def main():
    errors = []
    index = {e["slug"]: e for e in load_index()}
    files = sorted(p for p in TECHNIQUES.glob("*.md") if not p.name.startswith("_"))
    slugs = {p.stem for p in files}
    listed = set()

    if not (TECHNIQUES / "_index.md").exists():
        errors.append("techniques/_index.md is missing")
    else:
        text = (TECHNIQUES / "_index.md").read_text()
        for name in set(re.findall(r"`([a-z0-9-]+)`", text)):
            if name not in slugs and "-" in name:
                errors.append(f"_index.md: `{name}` is not a technique")

    for path in files:
        slug = path.stem
        meta, body = split_frontmatter(path.read_text())
        if meta is None:
            errors.append(f"{slug}: no frontmatter")
            continue
        for field in REQUIRED:
            if field not in meta:
                errors.append(f"{slug}: missing frontmatter field {field}")
        if meta.get("area") not in AREAS:
            errors.append(f"{slug}: area {meta.get('area')!r} is not in the area list")
        for topic in meta.get("topics") or []:
            if topic not in TOPICS:
                errors.append(f"{slug}: topic {topic!r} is not on the fixed list")
        for problem in meta.get("problems") or []:
            if problem not in index:
                errors.append(f"{slug}: problem {problem!r} is not in index.yaml")
            listed.add(problem)
        for related in meta.get("related") or []:
            if related not in slugs:
                errors.append(f"{slug}: related {related!r} is not a technique")
        if not meta.get("problems"):
            errors.append(f"{slug}: lists no problems")

        headings, sections, blocks = scan_body(body)
        names = [h[1] for h in headings]
        if names != HEADINGS or any(level != 2 for level, _ in headings):
            errors.append(f"{slug}: headings must be exactly {HEADINGS} (## level), found {names}")
            continue
        for name in HEADINGS:
            if not sections[name].strip() and not any(b[0] == name for b in blocks):
                errors.append(f"{slug}: section '{name}' is empty (write one line saying there is nothing to add)")

        parsed = {}
        for section, lang, code in blocks:
            if lang != "python":
                continue
            try:
                parsed.setdefault(section, []).append(ast.parse(code))
            except SyntaxError as e:
                errors.append(f"{slug}: python block in '{section}' does not parse: {e}")
        template = parsed.get("Template", [])
        if not template:
            errors.append(f"{slug}: Template has no python block")
        elif not any(isinstance(n, ast.FunctionDef) for tree in template for n in ast.walk(tree)):
            errors.append(f"{slug}: Template must be a complete function")

        example = sections["Worked example"]
        named = re.search(r"^Problem:\s*`([a-z0-9-]+)`", example, re.M)
        if not named:
            errors.append(f"{slug}: Worked example must start with a line  Problem: `slug`")
        elif named.group(1) not in index:
            errors.append(f"{slug}: worked example problem {named.group(1)!r} is not in index.yaml")
        else:
            problem = named.group(1)
            if problem not in (meta.get("problems") or []):
                errors.append(f"{slug}: worked example {problem} is not in this page's problems list")
            solution = PROBLEMS / problem / "solution.py"
            haystack = stripped_lines(solution.read_text()) if solution.exists() else []
            shown = parsed.get("Worked example", [])
            if not shown:
                errors.append(f"{slug}: Worked example has no python block")
            for tree in shown:
                if not contains_sequence(haystack, stripped_lines(ast.unparse(tree))):
                    errors.append(f"{slug}: worked example code is not verbatim from problems/{problem}/solution.py")

    for problem in sorted(set(index) - listed):
        errors.append(f"{problem}: not listed by any technique")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) found")
        sys.exit(1)
    print(f"techniques OK: {len(files)} pages cover all {len(index)} problems")


if __name__ == "__main__":
    main()
