# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Two things layered together:

1. **The actual project**: organizing the "Comité de Vecinos de Lomas del Sol" (a residential neighborhood committee). The working content is Spanish-language Markdown — `agenda.md` (meeting agendas), `comisiones.md` (the committee's sub-commissions: Infraestructura, Comunicación, Tecnología, Actividades Sociales, Salud y Bienestar, Bienestar Animal, Seguridad), plus supporting files like `plan_de_organización.drawio` and PDFs of formal municipal documents.
2. **A Python project scaffold**: `src/`, `tests/`, `scripts/`, `experiments/`, `plans/`, `prompts/`, `data/`, `models/` currently contain only `.gitkeep` — no code has been written yet. This scaffolding exists in case AI-assisted automation (e.g. drafting agendas, tracking commission action items) becomes useful later. Don't assume any of these directories has structure beyond what you find in them.

When asked to do "project work," default to interpreting it as work on the committee documents unless the request is clearly about writing/running code.

## Environment setup

- Environment variables load from `.env` (git-ignored, created via `make init` from `.env_template`). `PROJECT_ROOT` and `PYTHONPATH` are set there.
- `make init` copies `.env_template` → `.env`, runs `uv sync` (+ dev group), and deletes `env.yml`/`requirements.txt` (the conda alternative). This repo has already committed to **uv**, not conda — `env.yml`/`requirements.txt` are vestigial template leftovers.
- Project-level `.bashrc` auto-loads `.env` and activates `.venv` when a new shell starts in this directory (assumes the user's `~/.bashrc` sources it).
- `pyproject.toml` currently has malformed `dependencies` (`dependencies = [dev]`, invalid TOML — should reference the `dependency-groups` table or be an empty list). No dependencies are installed via it yet since `src/` has no code depending on anything.

## Common commands

```bash
make init          # first-time setup: creates .env, uv sync, removes conda files
make update-env     # uv sync
make rm-env         # remove .venv
make lint            # pylint --load-plugins=pylint.extensions.docparams scripts src
make jupl            # start Jupyter Lab
make help            # list all Makefile targets
make show-vars       # print resolved Makefile variables (REPO_ROOT, BRANCH, ENV_NAME, ...)

uv run pytest                                   # run all tests
uv run pytest tests/path/test_foo.py::test_name  # run a single test
```

## Coding standards

- Linting: `pylintrc` implements the Google Python Style Guide (80-char lines, 4-space indent per Google's public guide, `R`-category and several specific checks disabled — see file for the full disable list).
- Style/testing/logging conventions for Python code are encoded in the `python-standards` Claude skill — invoke it before writing or reviewing Python.
- Coding-agent behavioral norms (simplicity first, surgical changes, state assumptions) are set at the user level, not repeated here.

## Working with the committee documents

- `agenda.md` and `comisiones.md` are the live, edited-by-hand source of truth — treat them like code: small, focused diffs, preserve the existing Markdown table/TOC conventions already in use.
- `agenda.docx` is a generated artifact from `agenda.md` (via `pandoc Agenda.md -o Agenda.docx`, per `.claude/settings.local.json`); don't hand-edit the `.docx`, regenerate it from the Markdown instead.
- Content is in Spanish; match that when editing these files.
- `docs/system_architecture.md` is a placeholder — there is no system architecture yet because there is no system yet.
- The site is published via GitHub Pages (Jekyll, `_config.yml` at `docs/_config.yml` — `docs/` is the Jekyll source, per `source: ./docs` in the deploy workflow, so build output paths mirror `docs/`'s contents directly with no `docs/` prefix, e.g. `docs/comite/agenda.md` publishes at `/comite/agenda.html`). GitHub's `github-pages` gem bundles `jekyll-optional-front-matter` and `jekyll-titles-from-headings`, so **any** `.md` anywhere under `docs/` gets converted to HTML and titled from its first `#` heading, front matter or not — front matter is only needed to set `layout: default` (minima's styling) and a specific `title:`. Two real controls, not front matter, decide what actually ships:
  - `exclude:` in `docs/_config.yml` — anything under `docs/` not meant to be a public page (currently just `dev/`) must be listed there, or Jekyll will build and publish it.
  - `header_pages: []` in `docs/_config.yml` — deliberately empty, so minima shows no top nav at all; without it, minima lists every titled page Jekyll finds, including anything not yet excluded.
  - Any new `.md` added under `docs/comite/` or `docs/comunidad/` should get front matter (`---\nlayout: default\ntitle: ...\n---`) for correct styling/title. `index_builder.py` unconditionally links every indexed `.md` entry to its `.html` counterpart, so it still gets indexed either way.
  - The deploy workflow (`.github/workflows/pages.yml`) only triggers on push to `main` touching `docs/**` (which now covers `docs/index.html` and `docs/_config.yml` too) — changes to files outside `docs/` won't redeploy even if they'd affect the site.
  - Run `make site` after adding or renaming documents to regenerate `docs/index.html`.
