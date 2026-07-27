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

- GitHub Pages habilitado en el repo con origen "GitHub Actions" (confirmado
  con el usuario antes de activarlo).
- Tras un `push` a `main` que toque `docs/**` o `index.html`, el workflow
  `.github/workflows/pages.yml` corre y termina en verde (build + deploy).
- Un `push` a `main` que **no** toque esos paths no dispara el workflow.
- Abrir `https://calang.github.io/comite-lds/` y verificar:
  - La portada es el `index.html` existente (mismo look, mismo filtro JS
    funcionando).
  - Los tres `.md` existentes (`agenda`, `tareas_pendientes`, `comisiones`)
    abren como páginas HTML renderizadas (títulos, listas, tablas con
    formato — no texto plano de Markdown crudo).
  - Los enlaces a PDF/DOCX/ODT siguen abriendo el archivo original sin
    cambios.
  - `docs/dev/` y el scaffold de Python (`src/`, `scripts/`, `tests/`, etc.)
    no son accesibles como páginas del sitio.
- Prueba de la convención para `.md` futuros: crear temporalmente un `.md` de
  prueba bajo `docs/comunidad/` **sin** front matter, regenerar el índice y
  confirmar que la entrada enlaza a un `.html` que Jekyll nunca genera (link
  roto/404 en el sitio publicado, aunque el índice se genera sin errores) —
  este es el comportamiento esperado a documentar, no un bug a corregir en
  esta fase; eliminar el archivo de prueba antes de terminar.
- Confirmar que agregar front matter a los tres `.md` no alteró el contenido
  visible al verlos en GitHub (el repo, no el sitio) — el front matter debe
  quedar discreto al inicio del archivo.

## Definición de terminado

- [ ] Sitio publicado y accesible en `https://calang.github.io/comite-lds/`.
- [ ] Workflow de CI/CD despliega automáticamente en cada push a `main` que
      toque `docs/**` o `index.html`.
- [ ] Todo `.md` indexado (agenda, tareas_pendientes, comisiones) se sirve
      renderizado a HTML, no como texto plano; la regla de enlace en
      `index_builder.py` es genérica por extensión, no por archivo.
- [ ] Convención de front matter para `.md` futuros documentada en
      `.claude/CLAUDE.md`.
- [ ] Tests nuevos pasan y `make lint` está limpio.
- [ ] Item correspondiente en `specs/roadmap.md` (Fase 2) marcado como `[x]`.
- [ ] Cambios revisados y mergeados a `main`.