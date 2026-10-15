# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

A local workbench for coding-interview prep: a catalogue of 110 LeetCode problems, each with a Python reference solution and test suite, plus a React app to browse them, edit Python in the browser, run the tests there, and attempt problems from a blank skeleton. No backend; browser state lives in localStorage.

## Python: always use uv

**Every Python command goes through `uv`** (`uv sync`, `uv run python scripts/...`). Never bare `python`, `pip` or `venv`. Python 3.12 (`.python-version`). PyYAML is the only dependency and is used only by `scripts/`; everything under `problems/` is standard library only.

In the browser Python is Pyodide (CPython compiled to WASM, loaded from the jsDelivr CDN in a Web Worker). There is no server. Local Python exists only for the CLI tests and checks.

## Commands

`make help` lists them. The ones that matter:

| Command | What it does |
|---|---|
| `make test` | all reference solutions against `tests.yaml` (`uv run python scripts/run_tests.py`) |
| `make test-one P="two-sum lru-cache"` | one or more problems (also runs their `solution_*.py` variants) |
| `make catalogue` | `scripts/check_catalogue.py`: index vs directories, topics, required files, entry points |
| `make skeletons` | regenerate every `skeleton.py` from its `solution.py` (never hand-edit skeletons) |
| `make headers` | regenerate each `solution.py` module docstring from `index.yaml` (never hand-edit that docstring; edit `index.yaml`) |
| `make dev` / `make build` / `make preview` | Vite dev server / production build to `web/dist` / serve the build |
| `make lint` / `make typecheck` | oxlint / `tsc -b` in `web/` |
| `make links` | `scripts/verify_links.py`: every slug, number and premium flag against LeetCode's GraphQL API (needs network) |
| `make pre-push` | fixes what it can (skeletons, solution headers, `oxlint --fix`), then catalogue, tests, lint, typecheck, build, links. Run before pushing; it leaves rewrites in `git status` |

Package manager is npm (pnpm was not installed). `web/` is its own npm project.

## Layout

- `problems/index.yaml` is the catalogue (one entry per problem). `problems/<slug>/` holds `solution.py`, `skeleton.py`, `tests.yaml`, `description.md`, optional `validator.py`, and optional `solution_<variant>.py`. The slug is the LeetCode URL slug and is the directory name, the `index.yaml` key and the route `/p/:slug`.
- `problems/_scaffolds/` (`linked_list.py`, `tree.py`, `graph.py`): node classes and JSON conversions. They import nothing from the repo and have no top-level side effects, because the browser worker writes them into the Pyodide filesystem.
- `problems/_harness/runner.py`: the one harness used by both the CLI and the browser. Standard library only, reads no files. Callers pass the solution source, the parsed `tests.yaml`, a case and optionally the validator source.
- `scripts/`: `run_tests.py`, `check_catalogue.py`, `gen_skeletons.py`, `sync_headers.py`, `verify_links.py`, `_common.py` (topic list, paths, variant discovery).
- `web/`: Vite + React + TypeScript + Tailwind + shadcn/ui (radix-nova, neutral, Lucide), react-router (`HashRouter`), zustand, CodeMirror 6, ECharts via `echarts-for-react`.
- `.github/workflows/deploy.yml` builds and deploys `web/dist` to GitHub Pages on push to `main` (after catalogue check and tests). `.claude/skills/add-problem/SKILL.md` is the add-a-problem workflow.

## Big picture

**One harness, two hosts.** `runner.run_case(solution_source, spec, case, validator_source)` runs a single case and returns a plain dict (`name, status, ms, expected, actual, message, stdout, stderr`); it never raises. `run_case_json` is the string-in/string-out wrapper the worker calls. Scaffolds are imported as flat top-level modules, so both hosts put `_scaffolds/` and `_harness/` on `sys.path` (CLI: `scripts/_common.py`; browser: `web/src/py/worker.ts` writes the files to `/workbench`).

**Five-second rule.** The harness does not enforce the limit. CLI: `signal.alarm` per case raises `runner.CaseTimeout` (a `BaseException`, so user `except Exception` cannot hide it). Browser: `web/src/py/runner.ts` sends one case per worker message with a 5 s timer; on expiry it `terminate()`s the worker, marks that case `timeout` and the rest `skipped`, and starts a fresh worker in the background. Pyodide starts when the app loads (`main.tsx` imports the runner), not on first Run.

**Files on disk are the source of truth.** `web/src/lib/catalogue.ts` reads `problems/` with `import.meta.glob(..., '?raw')` (`server.fs.allow` includes the repo root), so editing a solution or `tests.yaml` hot-reloads. The Definitions block on the problem page is the leading `#` comment block of `skeleton.py`.

**Pages** (`HashRouter`, nav bar in `App.tsx`): `/` Problems (labelled filter bar, every column header sorts: click cycles ascending, descending, off), `/p/:slug` problem page, `/practice` session setup, `/practice/session` the running session, `/profile` completion tables by difficulty, set and topic plus practice history and a reset. The problem page and practice session share `components/Workspace.tsx` (editor toolbar, editor, and Test cases / Console / Add a case / Benchmark tabs). Layout is three columns on wide screens: a narrow left column (description and, in View mode, approach/tricks/edge cases), the code in the middle, and a narrow right column listing every test case with its result plus the add-a-case field. Below the editor are Console and Benchmark tabs.

**Problem page modes.** View solution shows the reference code (its docstring carries approach, tricks and edge cases, generated by `sync_headers.py`) plus an approach picker when `solution_*.py` variants exist. Implement starts from the skeleton, hides approach/tricks/edge cases, and offers Reveal solution.

**Practice** (`store.ts` `practice*` state, `pages/Practice*.tsx`): the user picks difficulty, topics, Blind 75, skip-done and a count; a random set is drawn and stepped through. No View, no Reveal, no hints, no notes; only the first two test cases are shown by name and input, later ones read "Hidden case n" until they fail. Passing all cases marks the problem done and records attempts and time; finished sessions go to `practiceHistory`. Practice drafts are keyed `practice:<slug>` and wiped when a session starts.

**Custom cases** are one line, parsed by `web/src/lib/caseFormat.ts`: `values → expected` for functions (values in `args` order, then converter extras such as `pos`), or `Class(args); method(args) → [results]` for operations problems. `->`, `=>` and `→` all work; JSON plus Python `True/False/None` and single quotes are accepted. `formatCase` and `parseCaseLine` are inverses (checked for every catalogue case), and the Tests tab shows each case in this same format.

**Persistence** is one zustand store under the localStorage key `leetcode-workbench` (`web/src/lib/store.ts`): done ticks, filters, sort, shuffle queue and position, editor drafts, custom cases, practice config/session/history, theme. Draft keys are `<slug>:view`, `<slug>:implement`, `<slug>:view:<variant>` and `practice:<slug>`. The editor marks app-initiated text replacement (mode switch, Reset) with an annotation so it is not saved as a user draft; keep that, or stale drafts block on-disk hot reload.

## Rules for solutions

- `solution.py` must be pasteable into LeetCode unchanged: `class Solution` with LeetCode's method name and current signature (lists, not legacy `Interval`), or LeetCode's class for design problems (`LRUCache`, `MinStack`, `Trie`, `MedianFinder`, `Codec`, `MyQueue`, ...). The harness pre-populates `List, Optional, Dict, Set, Tuple` and the scaffold classes (`ListNode`, `TreeNode`, `Node`), so do not import those; do import stdlib modules yourself. Standard library only.
- The module docstring of `solution.py` is generated from `index.yaml` (title, approach, tricks, edge cases, complexity) by `scripts/sync_headers.py`; change the catalogue entry, then `make headers`. Everything below the docstring is hand-written and should teach: block comments per phase explaining why, end-of-line comments only on non-obvious lines. Alternative `solution_<variant>.py` files keep their own hand-written docstring.
- `Node` is `linked_list.Node` (random pointer) or `graph.Node` depending on the problem's `scaffolds`; a problem must not list both.
- **Alternative approaches** are separate files next to the primary: `solution_<variant>.py` (underscores become spaces in the UI), same entry point, same `tests.yaml`, own docstring. `run_tests.py` and `check_catalogue.py` cover every variant; the web problem page shows an approach picker when there are several. Small alternatives may still live as an extra clearly named method in `solution.py`; the harness calls only the entry named in `tests.yaml`. Skeletons come from `solution.py` only.
- Tests: LeetCode examples, every edge case named in the catalogue entry, plus cases that break plausible wrong solutions. 5-10 cases, each well under 5 s. Derive expected values from the statement or by hand, not by running the solution. Avoid inputs with several valid answers unless the comparator handles it.
- YAML must parse identically in PyYAML (1.1) and the JS `yaml` package (1.2): no bare `yes/no/on/off`, no exponent floats like `1e5`, no leading-zero numbers, quote number-like strings (e.g. `"1"` grid cells).

## index.yaml

Entry fields: `slug, number, title, difficulty (easy|medium|hard), topic, tags, blind75, premium, leetcode, summary, tricks, edge_cases (list), complexity {time, space}`. Keep the file ordered by difficulty, then title. `topic` is exactly one of, and `tags` draw from the same list: Array, String, Hash, Two pointers, Sliding window, Stack, Monotonic stack, Binary search, Linked list, Tree, Trie, Heap, Graph, Intervals, Matrix, DP, Greedy, Backtracking, Bit manipulation, Design. The landing filter matches `topic` or `tags`. Titles drop the dagger/`(premium)` markers; three use LeetCode's official titles rather than the shortened ones (211, 167, 208). `blind75` follows the original appendix's daggers (74 of 110 are true).

## tests.yaml schema

```yaml
kind: function            # or: operations
entry: Solution.twoSum    # Class.method; for operations just the class name
scaffolds: []             # any of: linked_list, tree, graph
args: [nums, target]      # positional order of the LeetCode signature (function kind)
convert: {head: linked_list, result: linked_list}   # optional
compare: unordered        # default exact
call: false               # optional; skip calling entry (validator drives it)
cases:
  - {name: basic, input: {nums: [2, 7, 11, 15], target: 9}, expected: [0, 1]}
```

Operations kind: `cases: [{name, ops: [[ClassName, [ctor args]], [method, [args]], ...], expected: [null, ..]}]` with `null` for constructor and `None` results. `compare` may be `exact` or `float:<tol>` there.

Input converters (`convert.<arg>`): `linked_list`, `linked_list_array` (list of lists), `linked_list_cycle:<posarg>` (the tail points to index `input[posarg]`; that key is extra and not in `args`), `random_list` (`[[val, randomIndex], ...]`), `tree` (level order with `null`), `graph` (adjacency list; `[]` is a null graph), `tree_node:<arg of the root>` (input is a node value, found inside the built tree; used by both LCA problems). Result converters (`convert.result`): `linked_list`, `random_list`, `tree`, `graph`, and `node_val` (a returned node becomes its `val`). An in-place arg is read back through its own converter.

Comparators (`compare`): `exact` (default); `unordered` (sort the outer list only; use where inner order matters, e.g. permutations); `unordered_nested` (sort each inner list, then the outer); `in_place:<arg>` (compare the mutated argument; Rotate Image, Set Matrix Zeroes, Move Zeroes, Sort Colors, Reorder List); `float:<tol>` (absolute tolerance, recursive over lists); `validator`.

`validator.py` defines `validate(result, case, scaffolds) -> (ok, message)`: `result` is the raw return value, `case` is the case dict plus `args` (converted arguments after the call) and `entry` (the resolved callable or class), `scaffolds` a namespace of the scaffold modules. Used where several answers are correct or a property must hold: Alien Dictionary, Clone Graph and Copy List with Random Pointer (structure equal and no shared nodes), Serialize/Encode round trips (`call: false`, entry is the class), Longest Palindromic Substring, and First Bad Version (injects `isBadVersion` into the solution's globals and bounds the call count).

## Decisions the original brief left open

- The add-problem skill's step 7 says `uv run python ...` rather than the brief's bare `python ...`, to follow the always-uv rule. Step 6 also asks for `description.md` and a `sync_headers.py` run, which the original brief did not have.
- uv with a `pyproject.toml` (PyYAML for scripts only) instead of bare Python; PyYAML is not standard library, so the CLI scripts use it while the harness stays pure standard library and receives already-parsed specs.
- Extra harness features beyond the brief's list: `linked_list_array`, `linked_list_cycle:<arg>`, result converter `node_val`, `call: false`, a validator that receives raw results plus converted args, an optional `entry` for operations problems (needed for skeleton generation and the catalogue check), and the worker/CLI message carrying `validatorSource`.
- LeetCode links are verified through the GraphQL endpoint (`scripts/verify_links.py`), because plain HEAD requests get 403 from bot protection even for non-existent slugs. The same check also confirms number and premium flag.
- Routing is `HashRouter` and Vite `base: './'` so the static build works under any GitHub Pages path with no 404 fallback.
- Pyodide is pinned to a specific CDN version in `web/src/py/worker.ts` (`PYODIDE_URL`) so deploys are reproducible; bump it deliberately.
- Terminate-and-restart is the only cancellation path; the optional interrupt-buffer route (needs COOP/COEP headers, which GitHub Pages cannot send) was not built.
- Vite chunk warning limit is raised to 2500 kB because every problem's source text is embedded in the bundle. `web/src/components/ui/` (generated by shadcn) is excluded from oxlint.
- Charts are static (animation off) and tree-shaken (`echarts/core` with only bar, line, grid, title, tooltip, legend). `echarts-for-react/lib/core` is CommonJS and is unwrapped from `.default` in `Chart.tsx`; charts sit behind an error boundary so a bad option cannot blank a page.
- Landing "n of m done" under "Hide done" counts over the visible problems plus done ones, otherwise it would always read 0.

- LeetCode's statements are not copied (copyright). Each problem has a `description.md` written in our own words for an experienced reader: the task precisely (real parameter names in `code`, return value, input guarantees), then a `Constraints:` bullet list of only the limits that drive algorithm choice. It must not hint at the approach (practice mode shows it) and has no examples (the test cases are shown separately). Format is the small markdown subset rendered by `components/Description.tsx`: paragraphs, `- ` bullets, inline `code`. The problem page also links to the full statement on LeetCode.
- There is no histogram on the home page or the profile; progress is shown as the Profile page's completion tables. ECharts remains only for the benchmark charts.
- Multi-selects (difficulty, topic) are popovers of checkboxes where an empty selection means "all".

## Adding a problem

Use the `add-problem` skill (`/add-problem <name or URL> [source material]`). It does not touch other problems, the harness, the scaffolds or the web app.
