# Tech Stack

El proyecto es, hoy, un conjunto de documentos Markdown versionados en Git (actas, agendas, comisiones), con un scaffold de proyecto Python preparado para automatización futura pero sin código propio todavía.

## Core

| Layer              | Choice                        | Rationale                                                                                        |
|--------------------|-------------------------------|--------------------------------------------------------------------------------------------------|
| Language           | Python (gestionado con `uv`)  | Ya elegido en `pyproject.toml`; sin dependencias propias todavía porque `src/` está vacío        |
| Front-end          | Ninguno                       | El contenido se consume como Markdown plano en el repositorio, no como sitio web                 |
| Document Storage   | Markdown + PDFs en Git        | `agenda.md`, `comisiones.md` y PDFs de documentos municipales formales son la fuente de verdad   |
| Document Retrieval | Git + búsqueda de texto plano | No hay base de datos ni motor de búsqueda; se navega por archivos y `grep`/lectura directa       |
| Server framework   | Ninguno                       | No existe un servicio en ejecución; no hay backend que exponer                                   |
| CI/CD Tools        | Ninguno todavía               | No configurado; posible necesidad futura si se agrega código en `src/`                           |
| Deployment tools   | Ninguno                       | No hay nada que desplegar; el proyecto no es un servicio                                         |


## Data

No hay un modelo de datos estructurado: el contenido vive en archivos Markdown editados a mano (`agenda.md`, `comisiones.md`) y en PDFs de documentos formales. `agenda.docx` es un artefacto generado a partir de `agenda.md` vía `pandoc` (no se edita a mano). También existe un diagrama `plan_de_organización.drawio`. Los directorios `data/` y `models/` del scaffold Python están vacíos (solo `.gitkeep`), reservados por si se agrega automatización asistida por IA.


## Testing

- **pytest** (`uv run pytest`) para el código Python, cuando exista — `tests/` está vacío por ahora
- **pylint** (`make lint`, con `pylintrc` que implementa la Google Python Style Guide y el plugin `pylint.extensions.docparams`) para calidad de código Python


## Tooling

- **uv** para gestión de dependencias y entorno virtual (`make init`, `make update-env`, `make rm-env`)
- **Makefile** como interfaz de comandos comunes (`init`, `lint`, `jupl`, `show-vars`, etc.)
- **Jupyter Lab** (`make jupl`) para exploración/experimentación
- **pandoc** para generar `agenda.docx` a partir de `agenda.md`
- Variables de entorno en `.env` (`PROJECT_ROOT`, `PYTHONPATH`), cargadas automáticamente por el `.bashrc` del proyecto


## What We Are Not Using

- **conda** — el proyecto migró explícitamente a `uv`; `env.yml`/`requirements.txt` son remanentes vestigiales de la plantilla que `make init` elimina
- **Base de datos** — no hace falta; la fuente de verdad son archivos Markdown versionados en Git
- **Framework web / servicio desplegado** — no existe todavía; el scaffold (`src/`, `scripts/`, `experiments/`) existe por si se necesita automatización asistida por IA más adelante, pero no hay nada construido
- **ORM** — no aplica sin base de datos

