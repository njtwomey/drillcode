# Interview workbench

A local workbench for coding-interview prep: 110 LeetCode problems, each with a Python reference solution and tests. A React app lets you browse and filter the catalogue, read solutions with notes, edit Python in the browser, run the tests there, add your own edge cases, benchmark, and attempt problems from a blank skeleton.

In the browser, Python runs as Pyodide (CPython compiled to WebAssembly) inside a Web Worker. There is no server. Progress, drafts and custom cases live in localStorage.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Node.js with npm.

```sh
make install     # uv sync + npm ci
```

## Everyday commands

```sh
make test                          # run every reference solution against its tests
make test-one P="two-sum lru-cache"
make dev                           # web app with hot reload (edits under problems/ reload too)
make pre-push                      # fix, check, test, lint, build, verify links
make help                          # everything else
```

All Python goes through `uv` (`uv run python scripts/run_tests.py [slug ...]`).

## Deploying to GitHub Pages

1. Push the repo to GitHub.
2. In the repository settings, set Pages -> Source to **GitHub Actions**.
3. Push to `main`. `.github/workflows/deploy.yml` checks the catalogue, runs the tests, builds `web/dist` and deploys it.

The build uses a relative base path and hash routes (`/#/p/two-sum`), so it works at `https://<user>.github.io/<repo>/` without further configuration. Run `make build && make preview` to try the production build locally.

## Adding a problem

Use the `add-problem` skill in Claude Code: `/add-problem <name or LeetCode URL>`. Conventions (layout, `tests.yaml` schema, alternative solutions as `solution_<variant>.py`) are in [CLAUDE.md](CLAUDE.md).
