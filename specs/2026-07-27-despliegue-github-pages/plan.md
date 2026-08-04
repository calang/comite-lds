# Plan — Despliegue en hospedaje gratuito (Fase 2)

## 1. Front matter en Markdown existente

1.1. Agregar a `docs/comite/agenda.md`, `docs/comite/tareas_pendientes.md` y
     `../../docs/comunidad/Comisiones.md` un front matter mínimo al inicio:
     ```
     ---
     layout: default
     title: <Título legible, p. ej. "Agenda">
     ---
     ```
1.2. Confirmar que el contenido existente de cada archivo queda sin cambios
     debajo del front matter (diff mínimo, solo agrega 4 líneas al inicio).

## 2. Configuración de Jekyll

2.1. Crear `_config.yml` en la raíz del repo con:
     - `title` y `description` (derivados de `specs/mission.md`).
     - `theme: minima`.
     - `exclude:` listando `src/`, `scripts/`, `tests/`, `experiments/`,
       `prompts/`, `data/`, `models/`, `docs/dev/`, `Makefile`,
       `pyproject.toml`, `uv.lock`, `pylintrc`.
2.2. Confirmar que `README.md` de la raíz no lleva front matter (para que
     Jekyll no lo procese ni lo sirva como página del sitio) — o agregarlo
     explícitamente a `exclude:` si Jekyll lo tratara como página por tener
     `.md`.

## 3. Regla genérica de enlace en `index_builder.py`

3.1. En `src/comite_lds/index_builder.py`, al construir cada `DocumentEntry`,
     si `extension == "md"`, generar `link` apuntando a la misma ruta con
     `.html` en vez de `.md`, y usar `extension="html"` para esa entrada
     (refleja lo que realmente se abre).
3.2. No introducir excepciones por nombre de archivo — la regla debe aplicar
     a cualquier entrada `.md` encontrada, presente o futura.
3.3. Regenerar `index.html` (`make site`) y revisar el diff: los tres
     enlaces `.md` existentes deben pasar a `.html`; el resto de entradas
     (pdf, docx, odt) no cambia.

## 4. Workflow de GitHub Actions

4.1. Crear `.github/workflows/pages.yml` basado en el workflow oficial
     `actions/jekyll-build-pages` + `actions/deploy-pages`:
     - Trigger: `on: push` a `main` con `paths: ["docs/**", "index.html"]`,
       más `workflow_dispatch`.
     - `permissions: contents: read, pages: write, id-token: write`.
     - `concurrency: group: "pages", cancel-in-progress: false`.
     - Job `build`: checkout, `actions/jekyll-build-pages@v1` (source `.`,
       destination `_site`), `actions/upload-pages-artifact@v3`.
     - Job `deploy`: `environment: github-pages`,
       `actions/deploy-pages@v4`, `needs: build`.

## 5. Habilitar GitHub Pages (una vez, manual)

5.1. Confirmar con el usuario antes de ejecutar.
5.2. `Settings → Pages → Build and deployment → Source: GitHub Actions` en
     `calang/comite-lds` (vía web UI o `gh api -X PUT repos/calang/comite-lds/pages
     -f build_type=workflow`, con confirmación previa por ser un cambio de
     configuración pública del repo).

## 6. Tests

6.1. En `tests/test_index_builder.py`, agregar caso: una entrada con
     extensión `md` produce `link` terminado en `.html` y `extension == "html"`
     en el `DocumentEntry`/HTML resultante.
6.2. `uv run pytest` y `make lint` limpios sobre los cambios en
     `index_builder.py`.

## 7. Documentación

7.1. Documentar en `.claude/CLAUDE.md` (sección "Working with the committee
     documents" o nueva sección) la convención: todo `.md` nuevo bajo
     `docs/comite/` o `docs/comunidad/` necesita front matter mínimo para
     renderizarse en el sitio publicado.
7.2. Agregar a `Makefile`/`README.md` la URL del sitio publicado
     (`https://calang.github.io/comite-lds/`) una vez confirmado el primer
     despliegue exitoso.
