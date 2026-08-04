# Validation — Despliegue en hospedaje gratuito (Fase 2)

## Automatizada

- `uv run pytest` pasa, incluyendo el nuevo caso en
  `tests/test_index_builder.py` que verifica que cualquier entrada con
  extensión `md` enlaza a la ruta `.html` equivalente (regla genérica, no
  atada a nombres de archivo puntuales).
- `make lint` no reporta errores nuevos sobre `src/comite_lds/index_builder.py`.
- `make site` regenera `index.html` sin errores y el diff resultante solo
  cambia los enlaces de las entradas `.md` existentes (`agenda`,
  `tareas_pendientes`, `comisiones`, de `.md` a `.html`) — el resto del
  índice (pdf, docx, odt) queda igual.

## Manual

- [x] GitHub Pages habilitado en el repo con origen "GitHub Actions"
      (confirmado con el usuario antes de activarlo).
- [x] Tras un `push` a `main` que toque `docs/**`, `index.html` o
      `_config.yml`, el workflow `.github/workflows/pages.yml` corre y
      termina en verde (build + deploy). Verificado con varios pushes
      reales, incluyendo el fix de nav/exclude descrito abajo.
- [x] Un `push` a `main` que no toca esos paths no dispara el workflow —
      confirmado indirectamente: los commits que solo tocaban `_config.yml`
      antes de agregarlo al trigger no dispararon ningún run (esa fue,
      justamente, la causa del bug de nav/exclude descrito abajo).
- [x] Abrir `https://calang.github.io/comite-lds/` y verificar:
  - [x] La portada es el `index.html` existente (mismo look, mismo filtro JS
        funcionando).
  - [x] Los tres `.md` existentes (`agenda`, `tareas_pendientes`,
        `comisiones`) abren como páginas HTML renderizadas (títulos, listas,
        tablas con formato — no texto plano de Markdown crudo).
  - [x] Los enlaces a PDF/DOCX/ODT siguen abriendo el archivo original sin
        cambios.
  - [x] `docs/dev/`, `specs/`, `README.md` y el scaffold de Python (`src/`,
        `scripts/`, `tests/`, etc.) no son accesibles como páginas del sitio
        (`404` confirmado con `curl` sobre `specs/mission.html` y
        `README.html`).
  - [x] Las páginas renderizadas (`agenda.html`, etc.) no muestran ninguna
        barra de navegación con enlaces a otras páginas (`header_pages` fija
        una lista de un solo path inexistente — una lista vacía `[]` no
        sirve, porque el filtro `default` de Liquid la trata como "sin
        definir" y minima vuelve a listar todas las páginas).
- **Bug encontrado y corregido durante esta validación**: el gem
  `github-pages` activa por defecto `jekyll-optional-front-matter` y
  `jekyll-titles-from-headings`, que convierten y titulan **cualquier** `.md`
  del repo, tenga o no front matter — no solo los que llevan front matter
  explícito, como se asumió originalmente (ver corrección en
  `requirements.md`). Por eso `specs/*.md` aparecía en la nav de `minima`
  pese a estar en `exclude:`: ese cambio a `_config.yml` nunca se había
  desplegado porque el workflow solo disparaba con cambios en `docs/**` o
  `index.html`. Corregido agregando `_config.yml` a los paths del trigger,
  fijando `header_pages` a un path inexistente, y agregando `README.md` a
  `exclude:`.
- Consecuencia de lo anterior sobre la convención de `.md` futuros: un `.md`
  nuevo bajo `../../docs/Comité/` o `../../docs/Comunidad/` **sin** front matter igual se
  convierte a `.html` y queda accesible (con título tomado del primer `#`
  encabezado), solo que sin el layout/estilo de `minima` — no es un link
  roto como se documentó inicialmente. El front matter sigue siendo necesario
  para consistencia visual, no para que el archivo se publique.

## Definición de terminado

- [x] Sitio publicado y accesible en `https://calang.github.io/comite-lds/`.
- [x] Workflow de CI/CD despliega automáticamente en cada push a `main` que
      toque `docs/**`, `index.html` o `_config.yml`.
- [x] Todo `.md` indexado (agenda, tareas_pendientes, comisiones) se sirve
      renderizado a HTML, no como texto plano; la regla de enlace en
      `index_builder.py` es genérica por extensión, no por archivo.
- [x] Convención de front matter para `.md` futuros documentada en
      `.claude/CLAUDE.md` (corregida tras el bug de nav/exclude).
- [x] Tests nuevos pasan y `make lint` está limpio.
- [x] Item correspondiente en `specs/roadmap.md` (Fase 2) marcado como `[x]`.
- [x] Cambios revisados y mergeados a `main`.