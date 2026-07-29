# Tech Stack

El proyecto es, hoy, un conjunto de documentos Markdown versionados en Git (actas, agendas, comisiones), con un scaffold de proyecto Python preparado para automatización futura pero sin código propio todavía.

## Core

| Layer              | Choice                        | Rationale                                                                                                   |
|--------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------|
| Language           | Python (gestionado con `uv`)  | Ya elegido en `pyproject.toml`; sin dependencias propias todavía porque `src/` está vacío                   |
| Front-end          | HTML estático generado + Jekyll (theme `minima`) | `docs/index.html` generado por `scripts/generate_index.py` (`make site`, CSS/JS embebidos); los `.md` de `docs/comite/` y `docs/comunidad/` llevan front matter y Jekyll los renderiza a HTML al desplegar   |
| Document Storage   | Markdown + PDFs en Git        | `agenda.md`, `comisiones.md` y PDFs de documentos municipales formales son la fuente de verdad              |
| Document Retrieval | Índice HTML + filtro JS del lado cliente | `docs/index.html` lista los documentos de `docs/comite/` y `docs/comunidad/` y permite filtrar por nombre de archivo; no busca contenido    |
| Data Base          | SQLlite                       | Solo se necesita para bajo volumen de eventuales listas de contactos y vectores de pocos (<1000) documentos |
| Server framework   | Ninguno                       | No existe un servicio en ejecución; no hay backend que exponer                                              |
| CI/CD Tools        | GitHub Actions                | `.github/workflows/pages.yml`: build con `actions/jekyll-build-pages`, deploy con `actions/deploy-pages`, disparado en push a `main` sobre `docs/**`  |
| Deployment tools   | GitHub Pages (Jekyll)         | Sitio estático publicado en `https://calang.github.io/comite-lds/`; `docs/` es la raíz del sitio Jekyll (`source: ./docs`), `docs/_config.yml` define theme (`minima`) y exclusiones                                  |


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
- **Framework web / backend** — no existe; lo que se despliega es un sitio estático (GitHub Pages + Jekyll), sin servidor propio ni lógica de aplicación. El scaffold (`src/`, `scripts/`, `experiments/`) existe por si se necesita automatización asistida por IA más adelante, pero no hay nada construido
- **ORM** — no aplica sin base de datos

