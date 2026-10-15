# Python always goes through uv. The browser uses Pyodide (WASM), so there is no server.
.DEFAULT_GOAL := help
.PHONY: help install test test-one catalogue techniques skeletons headers links dev build preview lint typecheck check pre-push clean

help:  ## List targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-12s %s\n", $$1, $$2}'

install:  ## Install Python (uv) and web (npm) dependencies
	uv sync
	cd web && npm ci

test:  ## Run every reference solution against its tests (CLI)
	uv run python scripts/run_tests.py

test-one:  ## Run some problems: make test-one P="two-sum lru-cache"
	uv run python scripts/run_tests.py $(P)

catalogue:  ## Validate index.yaml against problems/
	uv run python scripts/check_catalogue.py

techniques:  ## Validate techniques/*.md (frontmatter, headings, code, coverage of every problem)
	uv run python scripts/check_techniques.py

skeletons:  ## Regenerate every skeleton.py from its solution
	uv run python scripts/gen_skeletons.py

headers:  ## Regenerate each solution.py docstring from index.yaml
	uv run python scripts/sync_headers.py

links:  ## Verify every LeetCode link (needs network)
	uv run python scripts/verify_links.py

dev:  ## Run the web app locally with hot reload
	cd web && npm run dev

build:  ## Production build into web/dist (what GitHub Pages serves)
	cd web && npm run build

preview: build  ## Serve the production build locally
	cd web && npm run preview

lint:  ## Lint the web app
	cd web && npm run lint

typecheck:  ## Type-check the web app
	cd web && npx tsc -b

check: catalogue techniques test lint typecheck  ## Fast checks, no network, no build

# Fixes what can be fixed (skeletons, lint autofixes), then runs every check. Anything
# it rewrote shows up in git status; commit it before pushing.
pre-push:  ## Everything before pushing: regenerate, check, test, lint, build, verify links
	uv sync --locked
	cd web && npm ci
	$(MAKE) skeletons
	$(MAKE) headers
	$(MAKE) catalogue
	$(MAKE) techniques
	$(MAKE) test
	cd web && npx oxlint --fix
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) build
	$(MAKE) links
	@git status --short
	@echo "pre-push OK"

clean:  ## Remove build output and caches
	rm -rf web/dist web/node_modules/.tmp
	find . -name __pycache__ -not -path './web/node_modules/*' -prune -exec rm -rf {} +
