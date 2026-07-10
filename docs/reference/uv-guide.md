# Cómo usar correctamente el gestor de paquetes uv
[Fecha de creación: 2026-04-20]

## Pregunta

How to properly use the uv package manager?

## Respuesta

## `uv` essentials

**Project setup**
```bash
uv init          # create new project (generates pyproject.toml)
uv sync          # create/update .venv from pyproject.toml + uv.lock
```

**Adding/removing dependencies**
```bash
uv add requests          # add to [project.dependencies]
uv add --dev pytest      # add to [dependency-groups] dev
uv remove requests       # remove
```

**Running code**
```bash
uv run python script.py  # run in managed venv
uv run pytest            # same for any tool
```

**Python version management**
```bash
uv python install 3.12   # install a Python version
uv python pin 3.12       # write .python-version (optional)
```
Or just set in `pyproject.toml`:
```toml
[project]
requires-python = ">=3.12"
```

**Key files**

| File | Purpose |
| ---- | ---- |
| `pyproject.toml` | deps + metadata (you edit this) |
| `uv.lock` | exact locked versions (commit this) |
| `.venv/` | local venv (gitignore) |

**Workflow summary**
1. `uv add <pkg>` — adds dep and updates lock
2. `uv sync` — installs from lock (teammates run this)
3. `uv run <cmd>` — no need to activate the venv manually

No need for `pip`, `virtualenv`, or `pyenv` separately — `uv` replaces all of them.
