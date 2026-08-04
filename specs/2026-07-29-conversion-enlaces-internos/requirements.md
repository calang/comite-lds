# Requirements — Conversión enlaces internos para Markdown hacia HTML (Fase 3)

## Alcance

Permitir que los `.md` del proyecto se enlacen entre sí usando rutas relativas
a otros archivos `.md` (con o sin ancla `#seccion`), y que esos enlaces
resuelvan correctamente en el sitio publicado (`.md` → `.html`).

**Incluido:**

- Enlaces `[texto](ruta.md)` y `[texto](ruta.md#ancla)` entre cualquier `.md`
  del repositorio, no solo `../../docs/Comité/` y `../../docs/Comunidad/` — incluyendo
  `docs/dev/` y archivos fuera de `docs/` (`README.md`, `specs/**`,
  `prompts/**`) si en el futuro se enlazan entre sí.
- Al menos un enlace real entre documentos existentes, como caso de prueba
  vivo (hoy no existe ninguno — se verificó por grep que ningún `.md` bajo
  `docs/` referencia a otro).
- Documentar la convención de escritura de enlaces internos para quien edite
  `agenda.md`, `Comisiones.md`, etc. a mano.

**Explícitamente fuera de alcance:**

- Enlaces salientes a URLs externas (ya funcionan sin cambios).
- Un índice de "quién enlaza a quién" o validación automática de enlaces
  rotos (linkchecker) — no se pidió y no hay CI para Markdown hoy.
- Cambios a `index_builder.py` — ya convierte `.md` → `.html` para las
  entradas del índice (Fase 2); este trabajo es sobre enlaces *dentro* del
  contenido de los documentos, no sobre el índice.

## Decisiones

- **Mecanismo: ninguno propio — se confía en Jekyll.** El gem `github-pages`
  activa por defecto el plugin `jekyll-relative-links` (junto con
  `jekyll-optional-front-matter` y `jekyll-titles-from-headings`, ya
  documentados en `.claude/CLAUDE.md`) y **no puede desactivarse** en GitHub
  Pages. Este plugin reescribe automáticamente cualquier enlace relativo a un
  `.md` para que apunte al `.html` renderizado equivalente, preservando
  anclas (`#seccion`). No se escribe script propio ni se agrega configuración
  a `docs/_config.yml` — no hace falta habilitar nada.
- **Sin nuevas dependencias**: no se agrega ningún gem, plugin ni paquete
  Python. `jekyll-relative-links` ya viene incluido en el gem `github-pages`
  que GitHub Pages usa para construir el sitio.
- **Alcance real de la conversión limitado por `source: ./docs`**: aunque el
  enlace pueda escribirse entre cualquier `.md` del repo, Jekyll solo
  construye páginas a partir de lo que está bajo `docs/` (y excluye
  `docs/dev/` vía `exclude:`). Un enlace desde `README.md` (fuera de `docs/`)
  hacia un `.md` de `docs/` no pasa por el build de Jekyll y **no** se
  reescribe — sigue siendo un enlace a un archivo `.md` crudo en GitHub. Esto
  no es un caso a resolver en este trabajo: no hay hoy ningún enlace de ese
  tipo, y el mecanismo de Jekyll ya cubre el caso real (enlaces entre `.md`
  publicados bajo `docs/`).
- **Convención de escritura**: rutas relativas al archivo origen (p. ej.
  desde `../../docs/Comité/agenda.md` hacia `../../docs/Comité/Comisiones.md`:
  `../comunidad/comisiones.md`), no rutas absolutas ni con prefijo `/docs/`.
  Los anclas siguen el slug que genera `kramdown` a partir del encabezado
  (minúsculas, espacios y acentos a guiones — ya visible en el TOC manual de
  `Comisiones.md`).

## Contexto

- Sigue la Fase 3 de `specs/roadmap.md`: "Implementar un mecanismo que
  detecte enlaces internos en los documentos Markdown y los convierta a
  enlaces HTML equivalentes en el sitio web."
- Verificado con `grep -rn '\.md' docs/**/*.md` que hoy no existe ningún
  enlace interno entre documentos — este trabajo agrega el primero (caso de
  prueba real) además de confirmar/documentar el mecanismo.
- Se confirmó por búsqueda web que `jekyll-relative-links` está en la lista
  de plugins que GitHub Pages activa por defecto y no permite desactivar,
  igual que `jekyll-optional-front-matter`/`jekyll-titles-from-headings`
  (ver corrección ya registrada en
  `specs/2026-07-27-despliegue-github-pages/requirements.md`).
- Contenido en español; el enlace de prueba y su documentación deben seguir
  ese idioma.