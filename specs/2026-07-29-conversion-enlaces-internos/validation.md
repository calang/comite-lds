# Validation — Conversión enlaces internos para Markdown hacia HTML (Fase 3)

## Automatizada

- No aplica código Python nuevo — no hay `pytest`/`pylint` que correr para
  este cambio (es contenido Markdown + documentación).
- `make site` no se ve afectado (el índice ya enlaza `.md` → `.html` desde
  Fase 2; esto no cambia `index_builder.py`).

## Manual

- [x] Los dos enlaces agregados en `docs/comite/agenda.md` usan ruta
      relativa (no absoluta, no `/docs/...`).
- [x] Tras el despliegue en `main`, abrir
      `https://calang.github.io/comite-lds/comite/agenda.html` y confirmar:
  - [x] El enlace hacia "tareas pendientes" abre
        `tareas_pendientes.html` (no `.md`).
  - [x] El enlace hacia "Comisión de Tecnología" abre `comisiones.html` y
        salta directamente a la sección "3. Comisión de Tecnología".
- [x] Confirmar que ningún enlace quedó apuntando a un `.md` crudo (revisar
      con el navegador, no solo el HTML fuente).

## Documentación

- [x] `.claude/CLAUDE.md` documenta la convención de enlaces internos
      (ruta relativa + ancla, alcance limitado a `docs/`).

## Definición de terminado

- [x] Al menos un enlace interno real funciona en el sitio publicado,
      incluyendo un caso con ancla.
- [x] Convención documentada en `.claude/CLAUDE.md`.
- [x] Item de Fase 3 en `specs/roadmap.md` marcado como `[x]`.
- [x] Cambios revisados y mergeados a `main`.