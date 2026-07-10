# Formación del Comité Lomas del Sol

Proyecto para reorganizar este esfuerzo.

Este directorio está planteado como un proyecto Python, apoyado por Claude, en caso de que sea de interés usar automatización basada en IA.

<!-- TOC -->
* [Formación del Comité Lomas del Sol](#formación-del-comité-lomas-del-sol)
  * [Requirements](#requirements)
  * [Environment Setup](#environment-setup)
  * [Common commands](#common-commands)
    * [uv](#uv)
  * [Coding Standards](#coding-standards)
  * [Use of AI Coding Agents](#use-of-ai-coding-agents)
  * [Project Layout](#project-layout)
  * [References](#references)
<!-- TOC -->

## Requirements

Linux, MacOS or WSL system with Python 3.14+

- Python 3.14+
- [`uv`](https://docs.astral.sh/uv/) — for the uv-based environment

## Environment Setup

- Key env vars are loaded from `.env` (generated from `.env_template`).
- `PYTHONPATH` is set to `PROJECT_ROOT`.
- Project-level `.bashrc` is sourced automatically when present in the project root (assumes `~/.bashrc` sources it).
- GPU support (TensorFlow/PyTorch with CUDA) requires uncommenting env vars in `Makefile` and `.bashrc`, and adding the relevant packages in `env.yml` or `pyproject.toml`.


## Common commands

### uv

```bash
source .venv/bin/activate   # or prefix commands with: uv run
make update-env             # runs uv sync (auto-detected)
make rm-env                 # removes .venv (auto-detected)
```

```bash
pytest                                     # run all tests (conda: direct; uv: uv run pytest)
pytest tests/path/test_foo.py::test_name   # run a single test
pylint src/                                # lint (conda: direct; uv: uv run pylint src/)
make jupl                                  # start Jupyter Lab (auto-detects backend)
make help                                  # list all Makefile targets
```

## Coding Standards

Encoded in the `python-standards` Claude skill.

Linting is configured in `pylintrc` using (Google Python Style Guide).

## Use of AI Coding Agents

This project uses AI coding agents to assist in code generation, debugging, and documentation.

## Project Layout

```
- .claude/ - configuration files for Claude API (if applicable)
- data/         # datasets, preprocessed data, results
- docs/         # documentation (system_architecture.md for architecture details)
- experiments/  # experiment scripts and results
- models/       # trained models and checkpoints
- plans/        # work plans
- scripts/      # scripts de uso auxiliar
- src/          # source code (on PYTHONPATH as PROJECT_ROOT)
- tests/        # unit tests
- .bashrc       # project-level bash config (sourced by ~/.bashrc)
- .env          # environment variables (created from .env_template)
- .env_template # template for .env file
- env.yml       # conda environment description (removed if using uv)
- Makefile - makefile with commands for common tasks
- pyproject.toml # uv environment description (removed if using conda)
- requirements.txt  # complement for env.yml conda environment (removed if using uv)
```

## References

- [Spec-Driven Development with Coding Agents](https://www.deeplearning.ai/short-courses/spec-driven-development-with-coding-agents)