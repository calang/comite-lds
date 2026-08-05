# Validation — Validación de enlaces internos rotos (Fase 4)

## Automatizado

- `uv run pytest tests/test_link_checker.py` pasa, cubriendo:
  - enlace válido a `.md` (con y sin ancla) → no reportado.
  - enlace a archivo inexistente → reportado con motivo "archivo no
    encontrado".
  - enlace con ancla inexistente en un `.md` existente → reportado con
    motivo "ancla no encontrada".
  - enlace a archivo no-Markdown existente/inexistente → validado solo por
    existencia.
  - enlace externo (`http://`, `https://`, `mailto:`) → ignorado, nunca
    reportado.
  - `slugify_heading` reproduce los slugs reales del TOC de
    `docs/Comité/Comisiones.md` (encabezados con acentos y paréntesis).
- `uv run pytest` (suite completa) sigue pasando — no se rompe
  `tests/test_index_builder.py`.
- `make lint` no reporta errores nuevos sobre `src/comite_lds/link_checker.py`
  ni `scripts/check_links.py`.
- `specs/tech-stack.md` actualizado: agregar el nuevo módulo/target a las
  tablas de Core/Tooling si corresponde (ver si amerita una fila nueva bajo
  "Document Retrieval" o una nueva fila de "Calidad de contenido").

## Manual

- `make check-links` sobre el estado actual del repo: termina en código 0,
  sin reportar los enlaces reales existentes (`Grupos_de_WhatsApp.md`,
  `Comisiones.md`, agenda `2026-07-14`) como rotos (falsos positivos).
- Introducir un enlace roto de prueba (archivo inexistente o ancla
  inexistente), correr `make check-links`: termina en código ≠ 0 y el
  mensaje impreso identifica archivo, línea y motivo correctos.
- Con el enlace roto de prueba aún presente, correr `make site`: se detiene
  antes de regenerar `docs/index.md` (verificar con `git status` que
  `docs/index.md` no cambió) y muestra el mismo mensaje de error.
- Revertir el enlace de prueba; correr `make site` de nuevo: genera
  `docs/index.md` normalmente.

## Revisión de tono

- Mensajes de error en español, consistentes en formato con los logs ya
  emitidos por `scripts/generate_index.py` (`logging`, no `print`).

## Definición de terminado

- Los dos ítems de Fase 4 en `specs/roadmap.md` marcados `[x]`.
- `make check-links` y su integración en `make site` funcionando según lo
  descrito arriba.
- Tests nuevos y existentes en verde; `make lint` limpio.
- PR listo para revisión con los archivos: `src/comite_lds/link_checker.py`,
  `scripts/check_links.py`, `tests/test_link_checker.py`, `Makefile`
  actualizado.
