---
name: add-problem
description: Add a new LeetCode problem to the workbench catalogue (index.yaml entry, reference solution, skeleton, tests). Use when the user names a problem to add, pastes a LeetCode URL, or supplies a transcript or write-up describing a solution approach to implement.
argument-hint: <problem name or LeetCode URL> [optional: pasted transcript or description of the approach]
---

Add one problem to the workbench. CLAUDE.md holds every convention; this file only lists the steps.

Input: $ARGUMENTS

The first line names the problem or gives its LeetCode URL. Anything after it is source material: a transcript of a video, an article, or the user's own notes describing the approach they want implemented.

Steps:

1. Identify the problem: LeetCode number, exact title, difficulty, URL slug, and whether it is premium. Use the web if available; otherwise ask for the number and title and nothing else. Verify the URL resolves.
2. Check `problems/index.yaml`. If the slug already exists, stop and say so. Do not overwrite.
3. Choose the primary topic and tags from the fixed list in CLAUDE.md.
4. If source material was supplied, read it before writing anything and implement that approach, even when you know a different one. Write the summary and tricks from it. Put a first-line comment in `solution.py`: `# Approach from: <what the user said the source was>`. If the material describes a weaker approach than the standard one, implement what was described, add the standard one as a second clearly named method with a comment, and leave the entry point on the described approach.
5. If no source material was supplied, write the standard solution and the catalogue fields in the style of the existing entries: a one-sentence summary, a one-sentence trick, about three edge cases.
6. Add the entry to `index.yaml`, keeping the file ordered by difficulty then title. Create `problems/<slug>/` with `solution.py`, `skeleton.py`, `tests.yaml`, `description.md` (50-120 words in your own words, written for an experienced engineer: the task precisely, then a `Constraints:` bullet list; no approach hints and no examples; format in CLAUDE.md), and `validator.py` only if the comparators cannot express correctness. After writing the entry run `uv run python scripts/sync_headers.py` so the `solution.py` docstring matches it. Tests: the LeetCode examples, every edge case in the entry, and a few more. Set `complexity` from the solution.
7. Techniques: after writing the solution, read `techniques/` and add the new slug to the `problems` list of every technique the solution uses. If none fits, add a Variants entry to the nearest page; where the technique is genuinely new, add a new page following the structure in CLAUDE.md (seven headings, Problem line and verbatim solution in the worked example). Use the shared variable names in the solution (`dummy`, `prev`, `curr`, `nxt`, `slow`, `fast`, `left`, `right`, `lo`, `hi`, `mid`, `path`, `result`, `visited`, `queue`, `seen`, `count`, `window`, `stack`, `best`). `check_techniques.py` fails otherwise.
8. Run `uv run python scripts/run_tests.py <slug>`, `uv run python scripts/check_catalogue.py` and `uv run python scripts/check_techniques.py`. All must pass. Fix the solution, the tests or the technique pages until they do, and never weaken a test to make it pass without saying so.
9. Report: the entry as added, the approach implemented, and anything in the source material you could not follow or disagreed with.

Do not touch any other problem; the only other files to edit are `techniques/*.md` (step 7). Do not change the harness, the scaffolds or the web app; if the new problem needs something they cannot do, say what is missing and stop.
