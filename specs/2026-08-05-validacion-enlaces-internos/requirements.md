# Requirements — Validación de enlaces internos rotos (Fase 4)

## Alcance

Detectar enlaces internos rotos en los documentos Markdown del repositorio y
notificar al usuario, deteniendo `make site` si se encuentra alguno.

**Incluido:**

- Enlaces `[texto](ruta)` cuyo destino sea otro archivo dentro del
  repositorio, en cualquier `.md`, no solo bajo `docs/` (mismo alcance de
  rutas que la Fase 3).
- Validar que el archivo destino exista en disco, resolviendo la ruta
  relativa al archivo origen (misma convención que Fase 3:
  `../comunidad/comisiones.md` desde `docs/Comité/agenda.md`, etc.).
- Validar anclas (`#seccion`) cuando el destino es un `.md`: la ancla debe
  corresponder al slug kramdown de algún encabezado (`#`, `##`, ...) del
  documento destino (minúsculas, espacios y acentos a guiones — mismo
  algoritmo ya usado a mano en el TOC de `Comisiones.md`).
- Validar enlaces a archivos que no son `.md` (PDFs, `.docx`, imágenes,
  `.drawio`, etc.) referenciados desde un `.md` — solo existencia del
  archivo, sin verificación de contenido.
- Reportar cada enlace roto con: archivo origen, línea, texto del enlace y
  motivo (archivo no encontrado / ancla no encontrada).
- Código de salida distinto de cero cuando hay al menos un enlace roto, para
  que `make site` se detenga antes de correr `generate_index.py`.

**Explícitamente fuera de alcance:**

- URLs externas (`http://`, `https://`, `mailto:`) — igual que la Fase 3, no
  se valida disponibilidad de recursos externos; requeriría red y no fue
  pedido.
- Reparación automática de enlaces rotos — el mecanismo solo detecta y
  notifica, no corrige.
- Enlaces dentro de archivos no-Markdown (`.drawio`, `.docx`, HTML embebido
  fuera de bloques Markdown reconocibles).
- Un índice de "quién enlaza a quién" (ya descartado en la Fase 3).

## Decisiones

- **Implementación: script Python propio**, como nuevo módulo en
  `src/comite_lds/` (junto a `index_builder.py`), sin agregar dependencias
  nuevas (usa solo la librería estándar: `pathlib`, `re`). Coherente con el
  resto del proyecto (`uv`, `pytest`, `pylint`).
- **Alcance de escaneo**: todo el repositorio (`git ls-files -- '*.md'` o
  recorrido de directorio equivalente), no solo `docs/`, ya que la Fase 3
  permitió enlaces entre `.md` de cualquier ubicación (`README.md`,
  `specs/**`, etc.).
- **Integración en Makefile**: nuevo target (p. ej. `check-links`) que el
  target `site` ejecuta como prerrequisito. Si `check-links` falla (código
  de salida ≠ 0), `make site` se detiene antes de invocar
  `scripts/generate_index.py` — comportamiento estándar de Make al fallar un
  prerrequisito, no requiere lógica adicional en el Makefile.
- **Formato de salida**: mensajes en español por stdout/stderr, uno por
  enlace roto encontrado, listando todos los problemas antes de salir (no
  detenerse en el primero) para que el usuario pueda corregir todo de una
  vez.
- **Cálculo de slugs de anclas**: replicar el algoritmo de kramdown
  (minúsculas; acentos y símbolos removidos o convertidos; espacios a
  guiones) lo suficiente para cubrir los encabezados reales ya usados en el
  proyecto (ver TOC de `Comisiones.md` como caso de prueba).

## Contexto

- Sigue la Fase 4 de `specs/roadmap.md`: "Implementar un mecanismo que
  detecte enlaces internos rotos en los documentos Markdown y notifique al
  usuario sobre ellos" + "Incluir el uso de este mecanismo como una
  comprobación inicial entre los comandos utilizados en Makefile para el
  target `site`. De fallar, informa al usuario de los fallos y detiene la
  generación del sitio web."
- Depende de la convención de enlaces establecida en
  `specs/2026-07-29-conversion-enlaces-internos/requirements.md` (Fase 3):
  rutas relativas al archivo origen, sin prefijo `/docs/` ni rutas
  absolutas.
- Casos de prueba reales ya existentes en el repo (útiles como fixtures):
  - `docs/Comunidad/Grupos_de_WhatsApp.md` → enlaces a
    `Procedimientos/Normas_de_los_grupos_de_vecinos.md` e
    `Procedimientos/Inclusion_en_grupo_principal_WA.md`.
  - `docs/Comité/Comisiones.md` → enlaces a
    `Plan_de_Trabajo_de_la_Comisión_de_Integración_Recreación_y_Acción_Social.md`
    y `Estrategia_Comisión_Salud.md`.
  - `docs/draft/comite/agenda-minutas/2026-07-14/agenda.md` → enlace con
    ancla-menos a `../../../tareas_pendientes.md`.
  - TOC de `docs/Comité/Comisiones.md` (líneas 12-18) como referencia del
    slug kramdown esperado para encabezados con acentos y paréntesis.
- Contenido y mensajes en español, siguiendo la convención del resto del
  proyecto.
