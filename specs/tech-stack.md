# Tech Stack

El proyecto es, hoy, un conjunto de documentos Markdown versionados en Git (actas, agendas, comisiones) publicado como sitio estático, más un paquete Python propio (`src/comite_lds`) que genera el índice del sitio y convierte archivos de oficina heredados a texto.

## Core

| Layer              | Choice                        | Rationale                                                                                                   |
|--------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------|
| Language           | Python 3.14 (gestionado con `uv`) | `pyproject.toml` define dependencias reales (`jupyterlab`, `ipympl`, `ipywidgets`, `python-dotenv`, `pyyaml`) y un grupo `dev` (`pylint`, `pytest`) |
| Front-end          | Markdown + Jekyll (theme `minima`) | `docs/` es la raíz del sitio Jekyll (`source: ./docs`); los `.md` de `../docs/Comité/` y `../docs/Comunidad/` llevan front matter y Jekyll los renderiza a HTML al desplegar; `header_pages: [__none__]` desactiva la nav automática de minima |
| Document Storage   | Markdown + PDFs en Git        | `agenda.md`, `Comisiones.md` y PDFs de documentos municipales formales son la fuente de verdad              |
| Document Retrieval | Índice generado + filtro JS del lado cliente | `docs/index.md` se genera con `make site` (`scripts/generate_index.py` → `src/comite_lds/index_builder.py`), que escanea `../docs/Comité/` y `../docs/Comunidad/` y arma una lista filtrable por nombre de archivo (JS embebido); no busca contenido |
| Legacy doc conversion | pandoc + LibreOffice (`soffice`) + poppler (`pdftotext`/`pdftoppm`) + Tesseract OCR (`spa`) | `scripts/convert_old_archive.py` convierte `docx`/`pptx`/`pdf`/`xls` de `docs/old/` a texto/Markdown en `data/old_archive/converted/` (excluido de git), con respaldo de OCR para PDFs escaneados; ver `docs/dev/analisis-docs-old.md` |
| Data Base          | Ninguna                       | Bajo volumen (actas, contactos, documentos); no hay necesidad actual de una base de datos                  |
| Server framework   | Ninguno                       | No existe un servicio en ejecución; no hay backend que exponer                                              |
| CI/CD Tools        | GitHub Actions                | `.github/workflows/pages.yml`: build con `actions/jekyll-build-pages`, deploy con `actions/deploy-pages`, disparado en push a `main` sobre `docs/**`  |
| Deployment tools   | GitHub Pages (Jekyll)         | Sitio estático publicado en `https://calang.github.io/comite-lds/`; `docs/_config.yml` define theme (`minima`) y excluye `dev/`, `draft/` y `old/` de la build                                  |


## Data

No hay un modelo de datos estructurado: el contenido vive en archivos Markdown editados a mano (`agenda.md`, `Comisiones.md`) y en PDFs de documentos formales. `agenda.docx` es un artefacto generado a partir de `agenda.md` vía `pandoc` (no se edita a mano). También existe un diagrama `plan_de_organización.drawio`. `data/old_archive/` contiene el resultado de convertir el archivo histórico (`docs/old/`) a texto: `converted/` (excluido de git), `manifest.csv` (estado de cada conversión) y `registro_temas.md`. `models/` del scaffold Python sigue vacío (solo `.gitkeep`), reservado por si se agrega automatización asistida por IA.


## Testing

- **pytest** (`uv run pytest`) para el código Python — `tests/test_index_builder.py` cubre `src/comite_lds/index_builder.py`
- **pylint** (`make lint`, con `pylintrc` que implementa la Google Python Style Guide y el plugin `pylint.extensions.docparams`) para calidad de código Python


## Tooling

- **uv** para gestión de dependencias y entorno virtual (`make init`, `make update-env`, `make rm-env`)
- **Makefile** como interfaz de comandos comunes (`init`, `lint`, `jupl`, `site`, `docxs`, `show-vars`, etc.)
- **Jupyter Lab** (`make jupl`) para exploración/experimentación
- **pandoc** para generar `agenda.docx` a partir de `agenda.md` (`make docxs`) y para convertir `docx` a texto en `convert_old_archive.py`
- **LibreOffice (`soffice`), poppler-utils (`pdftotext`/`pdftoppm`) y Tesseract OCR** como dependencias del sistema (no gestionadas por `uv`) usadas solo por `scripts/convert_old_archive.py`
- Variables de entorno en `.env` (`PROJECT_ROOT`, `PYTHONPATH`), cargadas automáticamente por el `.bashrc` del proyecto


## What We Are Not Using

- **conda** — el proyecto migró explícitamente a `uv`; `env.yml`/`requirements.txt` son remanentes vestigiales de la plantilla que `make init` elimina
- **Base de datos** — no hace falta; la fuente de verdad son archivos Markdown versionados en Git
- **Framework web / backend** — no existe; lo que se despliega es un sitio estático (GitHub Pages + Jekyll), sin servidor propio ni lógica de aplicación. El scaffold restante (`experiments/`, `models/`) existe por si se necesita automatización asistida por IA más adelante, pero no hay nada construido ahí
- **ORM** — no aplica sin base de datos

