# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

DrillCode: a local workbench for coding-interview prep (repository `njtwomey/drillcode`, app in `drillcode/`): a catalogue of 222 LeetCode problems, each with a Python reference solution and test suite, plus a React app to browse them, edit Python in the browser, run the tests there, and attempt problems from a blank skeleton. No backend; browser state lives in localStorage.

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
| `make techniques` | `scripts/check_techniques.py`: validates `techniques/*.md` and that every problem is listed by a technique |
| `make skeletons` | regenerate every `skeleton.py` from its `solution.py` (never hand-edit skeletons) |
| `make headers` | regenerate each `solution.py` module docstring from `index.yaml` (never hand-edit that docstring; edit `index.yaml`) |
| `make dev` / `make build` / `make preview` | Vite dev server / production build to `drillcode/dist` / serve the build |
| `make lint` / `make typecheck` | oxlint / `tsc -b` in `drillcode/` |
| `make links` | `scripts/verify_links.py`: every slug, number and premium flag against LeetCode's GraphQL API (needs network) |
| `make pre-push` | fixes what it can (skeletons, solution headers, `oxlint --fix`), then catalogue, techniques, tests, lint, typecheck, build, links. Run before pushing; it leaves rewrites in `git status` |

Package manager is npm (pnpm was not installed). `drillcode/` is its own npm project.

## Layout

- `problems/index.yaml` is the catalogue (one entry per problem). `problems/<slug>/` holds `solution.py`, `skeleton.py`, `tests.yaml`, `description.md`, `walkthrough.md`, optional `validator.py`, and optional `solution_<variant>.py`. The slug is the LeetCode URL slug and is the directory name, the `index.yaml` key and the route `/p/:slug`.
- `problems/_scaffolds/` (`linked_list.py`, `tree.py`, `graph.py`): node classes and JSON conversions. They import nothing from the repo and have no top-level side effects, because the browser worker writes them into the Pyodide filesystem.
- `problems/_harness/runner.py`: the one harness used by both the CLI and the browser. Standard library only, reads no files. Callers pass the solution source, the parsed `tests.yaml`, a case and optionally the validator source.
- `scripts/`: `run_tests.py`, `check_catalogue.py`, `gen_skeletons.py`, `sync_headers.py`, `verify_links.py`, `_common.py` (topic list, paths, variant discovery).
- `drillcode/`: Vite + React + TypeScript + Tailwind + shadcn/ui (radix-nova, neutral, Lucide), react-router (`HashRouter`), zustand, CodeMirror 6, ECharts via `echarts-for-react`.
- `.github/workflows/deploy.yml` builds and deploys `drillcode/dist` to GitHub Pages on push to `main` (after catalogue check and tests). `.claude/skills/add-problem/SKILL.md` is the add-a-problem workflow.

## Big picture

**One harness, two hosts.** `runner.run_case(solution_source, spec, case, validator_source)` runs a single case and returns a plain dict (`name, status, ms, expected, actual, message, stdout, stderr`); it never raises. `run_case_json` is the string-in/string-out wrapper the worker calls. Scaffolds are imported as flat top-level modules, so both hosts put `_scaffolds/` and `_harness/` on `sys.path` (CLI: `scripts/_common.py`; browser: `drillcode/src/py/worker.ts` writes the files to `/workbench`).

**Five-second rule.** The harness does not enforce the limit. CLI: `signal.alarm` per case raises `runner.CaseTimeout` (a `BaseException`, so user `except Exception` cannot hide it). Browser: `drillcode/src/py/runner.ts` sends one case per worker message with a 5 s timer; on expiry it `terminate()`s the worker, marks that case `timeout` and the rest `skipped`, and starts a fresh worker in the background. Pyodide starts when the app loads (`main.tsx` imports the runner), not on first Run.

**Files on disk are the source of truth.** `drillcode/src/lib/catalogue.ts` reads `problems/` with `import.meta.glob(..., '?raw')` (`server.fs.allow` includes the repo root), so editing a solution or `tests.yaml` hot-reloads. The Definitions block on the problem page is the leading `#` comment block of `skeleton.py`.

**Pages and URLs** (`BrowserRouter`, real paths; nav bar in `App.tsx`): `/` Home (a hero, problem / technique / walkthrough of the day chosen by date, progress with a 16-week solve heatmap, problems worth reviewing, jump-in-by-topic chips), `/problems` the catalogue table (labelled filter bar with search, difficulty, topic, an All / Not done yet / Done toggle and Only the Blind 75; every column header sorts; topic and tag chips filter when clicked; a Random problem button), `/p/:slug/view`, `/p/:slug/impl` and `/p/:slug/read` (the three pages of a problem; bare `/p/:slug` redirects to view), `/practice` session setup, `/practice/session` the running session, `/tips` and `/tips/:slug` the techniques reference, `/profile` (a user icon at the right of the header, beside the theme toggle) completion tables plus practice history and a reset. Because the paths are real, the build needs a base path and a `404.html`: the deploy workflow sets `BASE_PATH=/<repo name>/` (`vite.config.ts` reads it; locally it is `/`), the router's `basename` comes from `import.meta.env.BASE_URL`, and `npm run build` copies `index.html` to `404.html` so GitHub Pages serves the app for deep links. The problem pages and the practice session share `components/Workspace.tsx`: three columns (notes | code | tests) that sit side by side from the `lg` breakpoint (`lib/useIsWide.ts`) and stack below it. On wide screens the columns are shadcn `resizable` panels (`react-resizable-panels` v4): drag the handles, or collapse the notes and tests columns with the toolbar buttons. Every test case has a checkbox, a collapse chevron, a Run-only-this-test button and its own collapsed console output (stdout, stderr and tracebacks live with the test; there is no separate console); the list has Select all / Select none / Select mine (only the cases you added) and Expand all / Collapse all; cases you add appear at the top, newest first, followed by the catalogue cases; Run (⌘/Ctrl ↵) runs the ticked tests. Failing tests open themselves once per run. Test results are keyed by case name, so names must be unique within a problem. Only a run that covered every test calls `onResults` (that is what logs a solve), so running one test never counts as solving. Benchmark is a collapsible section under the editor and runs the ticked tests.

**The three problem pages.** View shows the reference code (its docstring carries approach, tricks and edge cases, generated by `sync_headers.py`), an approach picker when `solution_*.py` variants exist, and a Walkthrough button that opens `walkthrough.md` in a modal. Implement starts from the skeleton, hides approach, tricks, edge cases, techniques and the walkthrough, and offers Reveal solution; a solve is logged once per visit when every test passes. Read is a full-width page: the description, then the walkthrough, then links to Implement and View. Practice never links to View or Read.

**Practice** (`store.ts` `practice*` state, `pages/Practice*.tsx`): the user picks difficulty, topics, Blind 75, a status (All / Not done yet / Done, the last for spaced repetition) and a count; a random set is drawn (shuffled with a seed taken from the current time, `lib/random.ts`; the seed is kept on the session) and stepped through. No View, no Reveal, no hints, no notes; only the first two test cases are shown by name and input, later ones read "Hidden case n", show only a status and a lock, and cannot be opened: their input and expected output are never shown. Passing all cases marks the problem done and records attempts and time; finished sessions go to `practiceHistory`. Practice drafts are keyed `practice:<slug>` and wiped when a session starts.

**Custom cases** (`components/CustomCases.tsx`, in the right-hand column under the test list): function problems get one labelled field per input (argument names, with their types read from `skeleton.py`, plus converter extras such as `pos`), then an `expected` field, then the Add button below. The `expected` field is labelled with the return type and "optional" and is collapsed by default (a "set" badge shows if it has a value); where it is required (Practice, or problems with `call: false`) it is shown open and is not collapsible. The labels carry only names and types (read from the skeleton's entry method, ignoring the commented node definitions); the one explanatory note is on inputs that are not function arguments (`extra_inputs`). Each field takes JSON or Python literals (`True`, `None`, single quotes) and is validated as you type; for in-place problems the `expected` type is that of the modified argument. Design problems (`kind: operations`) have no fixed arguments, so they take one `calls` field (`Class(args); method(args)`) and one results field. **Leaving `expected` blank** stores the case without an `expected` key; the harness then runs the reference solution (always the primary `solution.py`, passed to the worker as `referenceSource`) on the same input and uses its answer (`run_case(..., reference_source)` / `_derive_expected` in `runner.py`; results carry `expected_source: 'reference'` and the UI says so). It is off in Practice (it would hand out the solution's behaviour) and for problems with `call: false` (their answer is not the function's return value), where `expected` stays required. If the reference cannot answer the input, the case errors with the reference's own message. The Tests list and the stored cases show each case as one line, `values → expected`, produced by `formatCase`; `parseCaseLine` (the inverse, used for `calls`) is checked against every catalogue case. `drillcode/src/lib/caseFormat.ts` holds both.

**Persistence and data model.** There is no backend: everything lives in the browser's localStorage, in one JSON document under the key `leetcode-workbench` (kept after the DrillCode rename so existing progress survives), written by zustand's `persist` middleware (`drillcode/src/lib/store.ts`, `version: 2` with a `migrate` for older shapes). Fields: `done` (slug to true), `filters`, `sort`, `drafts` (editor text by `<slug>:view`, `<slug>:implement`, `<slug>:view:<variant>`, `practice:<slug>`), `customCases` (by slug), `theme`, `practiceConfig`, `practice` (the running session, with per-problem attempts and seconds), `practiceHistory` (finished sessions: when, solved, total, seconds), and `solves`, an append-only log of `{slug, at, source: 'practice' | 'implement', seconds?}` capped at 5000 events. A solve is logged when every test passes in Practice (first pass of that problem in the session, with its time) or in Implement mode (once per visit). Ticking Done by hand does not log a solve. `lib/stats.ts` derives per-problem counts, last-solved dates and best times from the log; they appear in the Problems table (Solved column), on the problem page header, and in the Profile statistics (totals, last 7 days, day streak, most solved, longest since solved). Reset on the Profile page clears done ticks, solves and practice history but keeps drafts and custom cases. Data is per browser; clearing site data erases it.

## Judge notes and errors

**Judge notes.** Where the judge provides or expects something beyond the signature, the skeleton and the solution carry a `# Judge notes:` comment block above the class, in the style of the node definitions (the web "Definitions and judge notes" panel shows the skeleton's leading comments). `scripts/_common.py` `judge_notes()` builds it from `tests.yaml` and both `gen_skeletons.py` and `sync_headers.py` use it, so never hand-write it. Sources: the `provided:` text (injected APIs such as `isBadVersion`, the remove-duplicates custom judge, how `Codec`, `RandomizedSet` and the weighted picker are called); a modify-in-place reminder for `compare: in_place:<arg>`; and, for `kind: operations`, "your X object will be instantiated and called as such" with `obj = X(args)` and `param_n = obj.method(args)` lines read from the class's methods and return annotations. When a new problem has an injected API or a custom judge, add `provided:` to its `tests.yaml`.

**Inputs a checker reads.** A validator may read input values that are not function arguments (First Bad Version reads `bad`). Declare them under `extra_inputs:` (name: what it means); the add-a-case form then asks for them, labelled "not passed to your function", and a case missing one is rejected with a clear message.

**Error messages** (`runner.py`) are written for the person running their own code: only frames from `solution.py` are shown, with the source line (the source is registered with `linecache`), and deep recursion collapses to the first and last calls. Problems that are not the solution's fault get a plain sentence with no traceback: a case missing input values (names the missing ones and lists what the problem needs), a class or method that is not defined, a call that does not match the signature, a returned value that cannot be compared, an error in call N of a design problem (names the call), or a checker that could not judge the case. Only a genuine harness bug keeps the full traceback, prefixed "Internal error in the test harness". New failure modes should raise `CaseError` with a finished message.

## Walkthroughs

Every problem has `problems/<slug>/walkthrough.md`: a descriptive explanation of why the solution is shaped this way, shown on the Read page and in the View page's modal (never in Implement or Practice). Sections (all `##`): The idea, Set-up, Step by step (a small example traced round by round), Why it works, Where it goes wrong, Cost; Other approaches when a variant exists. Each has at least one ```text ASCII diagram; every number in a diagram must be real, so verify traces by running an instrumented scratch copy of the solution, never by hand. `problems/reverse-linked-list/walkthrough.md` is the style model. The app loads walkthroughs on demand (`loadWalkthrough` / `useWalkthrough` in `drillcode/src/lib`, one small chunk each) so they do not weigh down the main bundle; `hasWalkthrough` is the synchronous existence check. `check_catalogue.py` requires the file, at least one text diagram, parseable python excerpts, `##` headings only and at least 120 words. The Markdown renderer shows ```python fences with CodeMirror and every other fence as a plain monospace box.

## Rules for solutions

- `solution.py` must be pasteable into LeetCode unchanged: `class Solution` with LeetCode's method name and current signature (lists, not legacy `Interval`), or LeetCode's class for design problems (`LRUCache`, `MinStack`, `Trie`, `MedianFinder`, `Codec`, `MyQueue`, ...). The harness pre-populates `List, Optional, Dict, Set, Tuple` and the scaffold classes (`ListNode`, `TreeNode`, `Node`), so do not import those; do import stdlib modules yourself. Standard library only.
- The module docstring of `solution.py` is generated from `index.yaml` (title, approach, tricks, edge cases, complexity) by `scripts/sync_headers.py`; change the catalogue entry, then `make headers`. Everything below the docstring is hand-written and should teach: block comments per phase explaining why, end-of-line comments only on non-obvious lines. Alternative `solution_<variant>.py` files keep their own hand-written docstring.
- `Node` is `linked_list.Node` (random pointer) or `graph.Node` depending on the problem's `scaffolds`; a problem must not list both.
- **Alternative approaches** are separate files next to the primary: `solution_<variant>.py` (underscores become spaces in the UI), same entry point, same `tests.yaml`, own docstring. `run_tests.py` and `check_catalogue.py` cover every variant; the web problem page shows an approach picker when there are several. Small alternatives may still live as an extra clearly named method in `solution.py`; the harness calls only the entry named in `tests.yaml`. Skeletons come from `solution.py` only.
- Tests: LeetCode examples, every edge case named in the catalogue entry, plus cases that break plausible wrong solutions. 5-10 cases, each well under 5 s. Derive expected values from the statement or by hand, not by running the solution. Avoid inputs with several valid answers unless the comparator handles it.
- YAML must parse identically in PyYAML (1.1) and the JS `yaml` package (1.2): no bare `yes/no/on/off`, no exponent floats like `1e5`, no leading-zero numbers, quote number-like strings (e.g. `"1"` grid cells).

## index.yaml

Entry fields: `slug, number, title, difficulty (easy|medium|hard), topic, tags, blind75, premium, leetcode, summary, tricks, edge_cases (list), complexity {time, space}`. Keep the file ordered by difficulty, then title. `topic` is exactly one of, and `tags` draw from the same list: Array, String, Hash, Two pointers, Sliding window, Stack, Monotonic stack, Binary search, Linked list, Tree, Trie, Heap, Graph, Intervals, Matrix, Dynamic programming, Greedy, Backtracking, Bit manipulation, Design, Maths. The landing filter matches `topic` or `tags`. Titles drop the dagger/`(premium)` markers; three use LeetCode's official titles rather than the shortened ones (211, 167, 208). `blind75` follows the original appendix's daggers (only the original 110 can be true; new additions are false).

## tests.yaml schema

```yaml
kind: function            # or: operations
entry: Solution.twoSum    # Class.method; for operations just the class name
scaffolds: []             # any of: linked_list, tree, graph
args: [nums, target]      # positional order of the LeetCode signature (function kind)
convert: {head: linked_list, result: linked_list}   # optional
compare: unordered        # default exact
call: false               # optional; skip calling entry (validator drives it)
provided: |               # optional; judge notes shown as comments above the class (see Judge notes)
  The isBadVersion API is already defined for you.
extra_inputs: {bad: why}  # optional; inputs a validator reads that are not function arguments
cases:
  - {name: basic, input: {nums: [2, 7, 11, 15], target: 9}, expected: [0, 1]}
```

Operations kind: `cases: [{name, ops: [[ClassName, [ctor args]], [method, [args]], ...], expected: [null, ..]}]` with `null` for constructor and `None` results. `compare` may be `exact` or `float:<tol>` there.

Input converters (`convert.<arg>`): `linked_list`, `linked_list_array` (list of lists), `linked_list_cycle:<posarg>` (the tail points to index `input[posarg]`; that key is extra and not in `args`), `random_list` (`[[val, randomIndex], ...]`), `tree` (level order with `null`), `graph` (adjacency list; `[]` is a null graph), `tree_node:<arg of the root>` (input is a node value, found inside the built tree; used by both LCA problems). Result converters (`convert.result`): `linked_list`, `random_list`, `tree`, `graph`, and `node_val` (a returned node becomes its `val`). An in-place arg is read back through its own converter.

Comparators (`compare`): `exact` (default); `unordered` (sort the outer list only; use where inner order matters, e.g. permutations); `unordered_nested` (sort each inner list, then the outer); `in_place:<arg>` (compare the mutated argument; Rotate Image, Set Matrix Zeroes, Move Zeroes, Sort Colors, Reorder List); `float:<tol>` (absolute tolerance, recursive over lists); `validator`.

`validator.py` defines `validate(result, case, scaffolds) -> (ok, message)`: `result` is the raw return value, `case` is the case dict plus `args` (converted arguments after the call) and `entry` (the resolved callable or class), `scaffolds` a namespace of the scaffold modules. Used where several answers are correct or a property must hold: Alien Dictionary, Clone Graph and Copy List with Random Pointer (structure equal and no shared nodes), Serialize/Encode round trips (`call: false`, entry is the class), Longest Palindromic Substring, and First Bad Version (injects `isBadVersion` into the solution's globals and bounds the call count).

## Decisions the original brief left open

- The add-problem skill has grown past the original brief's wording and is kept in step with this file: commands use `uv run python`; step 6 also writes `description.md`, generates `skeleton.py` and the `solution.py` docstring (`gen_skeletons.py`, `sync_headers.py`) and asks for teaching comments and the shared variable names; step 7 adds the problem to `techniques/`; step 8 also runs `check_techniques.py`, `sync_headers.py --check` and `verify_links.py` (plain HEAD requests to LeetCode get 403, so the GraphQL check replaces "verify the URL resolves"). When a convention changes, update the skill too.
- uv with a `pyproject.toml` (PyYAML for scripts only) instead of bare Python; PyYAML is not standard library, so the CLI scripts use it while the harness stays pure standard library and receives already-parsed specs.
- Extra harness features beyond the brief's list: `linked_list_array`, `linked_list_cycle:<arg>`, result converter `node_val`, `call: false`, a validator that receives raw results plus converted args, an optional `entry` for operations problems (needed for skeleton generation and the catalogue check), and the worker/CLI message carrying `validatorSource`.
- LeetCode links are verified through the GraphQL endpoint (`scripts/verify_links.py`), because plain HEAD requests get 403 from bot protection even for non-existent slugs. The same check also confirms number and premium flag.
- Routing is `HashRouter` and Vite `base: './'` so the static build works under any GitHub Pages path with no 404 fallback.
- Pyodide is pinned to a specific CDN version in `drillcode/src/py/worker.ts` (`PYODIDE_URL`) so deploys are reproducible; bump it deliberately.
- Terminate-and-restart is the only cancellation path; the optional interrupt-buffer route (needs COOP/COEP headers, which GitHub Pages cannot send) was not built.
- Vite chunk warning limit is raised to 4000 kB because every problem's source text is embedded in the bundle. `drillcode/src/components/ui/` (generated by shadcn) is excluded from oxlint.
- Charts are static (animation off) and tree-shaken (`echarts/core` with only bar, line, grid, title, tooltip, legend). `echarts-for-react/lib/core` is CommonJS and is unwrapped from `.default` in `Chart.tsx`; charts sit behind an error boundary so a bad option cannot blank a page.
- Landing "n of m done" under "Hide done" counts over the visible problems plus done ones, otherwise it would always read 0.

- LeetCode's statements are not copied (copyright). Each problem has a `description.md` written in our own words for an experienced reader: the task precisely (real parameter names in `code`, return value, input guarantees), then a `Constraints:` bullet list of only the limits that drive algorithm choice. It must not hint at the approach (practice mode shows it) and has no examples (the test cases are shown separately). Format is the small markdown subset rendered by `components/Description.tsx`: paragraphs, `- ` bullets, inline `code`. The problem page also links to the full statement on LeetCode.
- There is no histogram on the home page or the profile; progress is shown as the Profile page's completion tables. ECharts remains only for the benchmark charts.
- Multi-selects (difficulty, topic, area) are popovers of checkboxes where an empty selection means "all". Topic and area lists are alphabetical (`TOPICS` in `scripts/_common.py` and `drillcode/src/lib/catalogue.ts` are kept sorted); difficulty stays easy, medium, hard.
- The topic `DP` was renamed `Dynamic programming` so every topic is spelled out. Persisted state is versioned (`version: 2` in `store.ts`): v1 `hideDone` / `skipDone` switches migrate to the three-way status filter and the old shuffle queue is dropped.
- The home page's Shuffle/queue was replaced by a Random problem button; Previous and Next on the problem page always follow catalogue order.

## Tips (techniques reference)

One page per technique in `techniques/<slug>.md` (the directory and `scripts/check_techniques.py` keep the brief's name; the UI, nav and routes say "Tips": `/tips`, `/tips/:slug`). Pages are derived from the code in `problems/`, not from memory; where a page and a solution disagree, one of them changes.

Frontmatter: `title`, `area` (one of Linked lists, Pointers and windows, Hashing and counting, Stacks, Binary search, Trees, Graphs, Backtracking, Divide and conquer, Heaps, Intervals, Dynamic programming, Greedy, Matrices, Maths, Bits, Tries, Design), `topics` (from the fixed topic list), `problems` (catalogue slugs in reading order), `related` (technique slugs). The app renders the problem list and related techniques from the frontmatter, so the body does not repeat them.

The body has exactly seven `##` headings in this order and nothing else: Reach for it when, Setup, Template, What it removes, Pitfalls, Variants, Worked example. Template is one runnable `python` block containing a function. Worked example starts with a line ``Problem: `slug` `` (a slug in the page's `problems`) and its `python` block is that solution's code verbatim (comments and docstring may be dropped); `check_techniques.py` compares it line by line after `ast.unparse`.

Shared variable names, used in templates, prose and solutions: `dummy`, `prev`, `curr`, `nxt`, `slow`, `fast`, `left`, `right`, `lo`, `hi`, `mid`, `path`, `result`, `visited`, `queue`, `seen`, `count`, `window`, `stack`, `best`. Rename locals in a solution (never signatures) when a role matches, then rerun its tests.

**Every catalogue problem must be listed by at least one technique** (`check_techniques.py` fails otherwise). If a problem fits no page, add a Variants entry to the nearest one or add a page.

`techniques/_index.md` holds the signals table; `drillcode/src/lib/techniques.ts` parses it into cards (a signal, then link chips to techniques) and builds a search index over each page's text, area, topics, signal rows and listed problems. The Tips page puts search first, with Area and Topic dropdowns, and shows cards, not tables. Technique badges appear on the problem page in View mode only, never in Implement or Practice, because they hint at the approach. Inline `code` in a page that equals a technique slug renders as a link.

## Adding a problem

Use the `add-problem` skill (`/add-problem <name or URL> [source material]`). It does not touch other problems, the harness, the scaffolds or the web app.
