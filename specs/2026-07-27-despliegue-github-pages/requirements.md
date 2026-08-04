# Requirements — Despliegue en hospedaje gratuito (Fase 2)

## Alcance

Publicar el sitio (hoy solo generado y abierto localmente) en GitHub Pages, con
despliegue automático vía CI/CD cada vez que cambie la documentación en `main`.
Todo archivo `.md` indexado se sirve renderizado a HTML, no como texto plano.

**Incluido:**

- Publicación en `https://calang.github.io/comite-lds/` usando GitHub Pages con
  origen "GitHub Actions" (no la rama `gh-pages` legacy).
- Workflow de GitHub Actions (`.github/workflows/pages.yml`) que construye el
  sitio con Jekyll nativo y lo despliega, disparado por `push` a `main` que
  toque `docs/**` o `index.html` (más `workflow_dispatch` manual).
- Todo archivo `.md` bajo `docs/comite/` y `docs/comunidad/` (hoy: `agenda.md`,
  `tareas_pendientes.md`, `Comisiones.md`) se renderiza a HTML vía Jekyll —
  no solo agenda y comisiones.
- El índice existente (`index.html`, todos los tipos de archivo: md, pdf, odt,
  docx) se mantiene tal cual — se sigue publicando completo. Los enlaces a
  entradas `.md` se actualizan para apuntar al `.html` renderizado.
- `_config.yml` mínimo en la raíz, con `exclude:` para no publicar el scaffold
  de Python (`src/`, `scripts/`, `tests/`, `experiments/`, `prompts/`,
  `data/`, `models/`), `docs/dev/` (documentación interna de desarrollo, no
  para vecinos), y archivos sueltos de la raíz sin relación con el sitio
  (`Makefile`, `pyproject.toml`, `uv.lock`, `pylintrc`, el PDF suelto en la
  raíz del repo).

**Explícitamente fuera de alcance (fases futuras):**

- Dominio propio (se usa `github.io` por ahora).
- Oracle Cloud u otro hospedaje — evaluado como opción futura si el sitio
  necesita backend/IA, no en esta fase.
- Cualquier backend, base de datos, autenticación o edición desde la web.
- Rediseño visual del sitio (se acepta el look por defecto de Jekyll/minima
  para las páginas renderizadas).

## Decisiones

- **Mecanismo de render**: Jekyll nativo de GitHub Pages — cero build propio
  en el repo. **Corrección post-implementación**: se asumió inicialmente que
  un `.md` sin front matter quedaba sin convertir; en la práctica, el gem
  `github-pages` trae activados por defecto `jekyll-optional-front-matter` y
  `jekyll-titles-from-headings`, que convierten y titulan **cualquier** `.md`
  del repo tenga o no front matter. El front matter que se agrega a mano en
  cada `.md` existente controla el `layout` y el `title`, no si se convierte.
  Lo que sí controla qué se publica es `exclude:` en `_config.yml` (qué `.md`
  no debe ni compilarse) y `header_pages:` (qué páginas aparecen en la nav de
  `minima`) — ver detalle en `.claude/CLAUDE.md`.
- **Theme**: `minima` (el theme por defecto del gem `github-pages`, sin
  configuración ni dependencia propia) con `layout: default` — da HTML válido
  (charset, título de pestaña) sin escribir layouts Jekyll a mano.
- **`index.html` no se toca por Jekyll**: al no tener front matter, Jekyll lo
  copia tal cual (no se envuelve con el theme), preservando el índice
  personalizado ya existente como página de entrada.
- **Regla de enlace genérica**: en `index_builder.py`, toda entrada con
  extensión `md` enlaza a la ruta `.html` equivalente (lo que Jekyll produce),
  en vez de al `.md` crudo. No hay excepciones por archivo — la regla aplica
  a cualquier `.md` bajo los directorios indexados, presentes o futuros.
- **Trigger del workflow**: `push` a `main` filtrado por paths (`docs/**`,
  `index.html`), más disparo manual (`workflow_dispatch`) para reintentos.
- **Habilitar Pages en el repo**: cambio de configuración del repositorio
  (Settings → Pages → Source: GitHub Actions) — se hace una sola vez,
  manualmente, confirmando con el usuario antes de ejecutarlo (afecta
  visibilidad pública del repo).

## Contexto

- Sigue directamente la Fase 2 de `specs/roadmap.md`: "Configurar un flujo de
  trabajo de CI/CD para desplegar automáticamente la página web en un
  hospedaje gratuito... cada vez que se actualice la documentación."
- Decisión tomada junto con el usuario tras conversar sobre Oracle Cloud como
  alternativa: se arranca con GitHub Pages por ser más simple y ya estar
  integrado al repo; OCI queda como opción para una fase futura si el sitio
  necesita volverse dinámico (backend + asistente de IA).
- El repo ya es público en GitHub (`calang/comite-lds`), así que publicar su
  contenido vía Pages no expone nada nuevo — el `exclude:` en `_config.yml`
  es por prolijidad del sitio, no por confidencialidad.
- Convención a documentar (en `CLAUDE.md` o en el propio `docs/`): todo `.md`
  nuevo bajo `docs/comite/` o `docs/comunidad/` debe incluir front matter
  mínimo para que se renderice en el sitio; si se omite, el archivo se sigue
  indexando pero como texto plano sin convertir.