---
name: add-problem
description: Add a new LeetCode problem to the workbench catalogue (index.yaml entry, reference solution, skeleton, tests). Use when the user names a problem to add, pastes a LeetCode URL, or supplies a transcript or write-up describing a solution approach to implement.
argument-hint: <problem name or LeetCode URL> [optional: pasted transcript or description of the approach]
---

Add one problem to the workbench. CLAUDE.md holds every convention; this file only lists the steps.

Input: $ARGUMENTS

The first line names the problem or gives its LeetCode URL. Anything after it is source material: a transcript of a video, an article, or the user's own notes describing the approach they want implemented.

Steps:

1. Identify the problem: LeetCode number, exact title, difficulty, URL slug, and whether it is premium. Use the web if available; otherwise ask for the number and title and nothing else. Plain HEAD requests to leetcode.com get 403, so verify the slug with `uv run python scripts/verify_links.py` once the entry exists (it checks every slug, number and premium flag through LeetCode's GraphQL endpoint). New additions are `blind75: false` unless the user says otherwise.
2. Check `problems/index.yaml`. If the slug already exists, stop and say so. Do not overwrite.
3. Choose the primary topic and tags from the fixed list in CLAUDE.md.
4. If source material was supplied, read it before writing anything and implement that approach, even when you know a different one. Write the summary and tricks from it. Put a first-line comment in `solution.py`: `# Approach from: <what the user said the source was>`. If the material describes a weaker approach than the standard one, implement what was described, add the standard one as a second clearly named method with a comment, and leave the entry point on the described approach.
5. If no source material was supplied, write the standard solution and the catalogue fields in the style of the existing entries: a one-sentence summary, a one-sentence trick, about three edge cases.
6. Write the problem, in this order:
   - Add the entry to `problems/index.yaml` (fields and conventions in CLAUDE.md), keeping the file ordered by difficulty then title. `topic` and `tags` come from the fixed list, spelled out (`Dynamic programming`, not `DP`). `leetcode` is `https://leetcode.com/problems/<slug>/`.
   - `problems/<slug>/solution.py`: LeetCode's current signature, standard library only, pasteable unchanged. Write no module docstring (`sync_headers.py` generates it; keep only a leading `# Approach from:` line if step 4 applies). Use the shared variable names (list in step 7). Add comments that teach: why each phase exists, the invariant a loop keeps, what the tricky line guards against; not a comment per line. A genuinely different second approach goes in `solution_<variant>.py` with its own docstring (same entry point; run by the same tests).
   - `problems/<slug>/tests.yaml`: the LeetCode examples, every edge case in the entry, and a few more, 5-10 cases, each well under 5 s. Work out expected values by hand, not by running the solution. YAML must parse in both PyYAML and the JS `yaml` package (no bare yes/no/on/off, no `1e5`, quote number-like strings). Add `validator.py` only if the comparators cannot express correctness.
   - `problems/<slug>/description.md`: 50-120 words in your own words, written for an experienced engineer: the task precisely (real parameter names, return value, input guarantees), then a `Constraints:` bullet list of only the limits that drive the algorithm choice. No approach hints (practice mode shows it) and no examples. Format in CLAUDE.md.
   - `problems/<slug>/walkthrough.md`: the "read" page. Explain why the solution is shaped this way: `## The idea`, `## Set-up`, `## Step by step` (a small example traced round by round), `## Why it works`, `## Where it goes wrong`, `## Cost`. At least one ```text ASCII diagram showing the data changing, with every number verified by running the solution on that example (instrument a scratch copy; never trust a hand trace). Own words, 250-450 words plus diagrams, `##` headings only, python excerpts must parse. See `problems/reverse-linked-list/walkthrough.md` for the style.
   - Generate, never hand-write: `uv run python scripts/gen_skeletons.py <slug>` for `skeleton.py`, and `uv run python scripts/sync_headers.py` for the `solution.py` docstring (approach, tricks, edge cases and complexity come from the entry, so set `complexity` from the solution first).
7. Techniques: after writing the solution, read `techniques/` and add the new slug to the `problems` list of every technique the solution uses. If none fits, add a Variants entry to the nearest page; where the technique is genuinely new, add a new page following the structure in CLAUDE.md (seven headings, Problem line and verbatim solution in the worked example). Use the shared variable names in the solution (`dummy`, `prev`, `curr`, `nxt`, `slow`, `fast`, `left`, `right`, `lo`, `hi`, `mid`, `path`, `result`, `visited`, `queue`, `seen`, `count`, `window`, `stack`, `best`). `check_techniques.py` fails otherwise.
8. Run `uv run python scripts/run_tests.py <slug>`, `uv run python scripts/check_catalogue.py`, `uv run python scripts/check_techniques.py`, `uv run python scripts/sync_headers.py --check` and `uv run python scripts/verify_links.py`. All must pass; `make pre-push` runs the full set plus the web build and lint. Fix the solution, the tests or the technique pages until they do, and never weaken a test to make it pass without saying so.
9. Report: the entry as added, the approach implemented, and anything in the source material you could not follow or disagreed with.

Do not touch any other problem; the only other files to edit are `problems/index.yaml` (step 6) and `techniques/*.md` (step 7). The web app picks the new problem up from disk, so it needs no change. Do not change the harness, the scaffolds or the web app; if the new problem needs something they cannot do, say what is missing and stop.
