# Requirements — Índice web de documentos (Fase 1)

## Alcance

Generar una página web estática (`index.html`) que sirva como punto de entrada al
contenido del comité: una breve descripción del sitio, y un índice navegable con
enlaces a todos los documentos existentes bajo `../../docs/Comité/` y `../../docs/Comunidad/`.

**Incluido:**

- Escaneo recursivo de `../../docs/Comité/` y `../../docs/Comunidad/`, indexando todos los
  archivos existentes (`.md`, `.pdf`, `.odt`, `.docx`), agrupados por carpeta de
  origen.
- Una página HTML autocontenida (CSS y JS embebidos, sin dependencias externas)
  con:
  - Descripción breve del sitio (tomada/adaptada de `specs/mission.md`).
  - Índice de documentos agrupado por carpeta, con enlaces relativos a cada
    archivo.
  - Un campo de filtro en JavaScript vanilla que oculta/muestra entradas del
    índice según coincidencia de texto (case-insensitive, substring) contra el
    nombre del documento — sin backend, sin dependencias nuevas.
- Un script Python que genera `index.html` a partir del árbol de `docs/`.

**Explícitamente fuera de alcance (fases futuras):**

- Búsqueda de texto completo dentro del contenido de los documentos (PDF/ODT/DOCX).
- Cualquier backend, base de datos o servicio desplegado.
- Autenticación o control de acceso.
- Edición de documentos desde la web.
- Estilizado avanzado / framework de diseño.

### Datos indexados por documento

| Campo          | Origen                                                          |
|----------------|------------------------------------------------------------------|
| Nombre         | Nombre de archivo sin extensión, tal cual aparece en disco       |
| Carpeta origen | Ruta relativa de la carpeta contenedora (p. ej. `comite/agenda-minutas`) |
| Tipo           | Extensión del archivo (md, pdf, odt, docx), mostrada como etiqueta |
| Enlace         | Ruta relativa desde `index.html` hasta el archivo                |

## Decisiones

- **Generación**: script Python (`uv run python scripts/generate_index.py`) que
  escanea `docs/` y escribe `index.html` en la raíz del repositorio. Se elige la
  raíz para que el archivo pueda abrirse localmente con doble clic o servirse
  directamente (p. ej. GitHub Pages) sin configuración adicional.
- **Sin dependencias nuevas**: el HTML se genera con `string.Template`/f-strings
  de la librería estándar — no se introduce Jinja2, Flask ni ningún paquete no
  presente ya en `pyproject.toml`, según lo indicado en `specs/tech-stack.md`.
- **Separación de código**: lógica de escaneo/generación en
  `src/comite_lds/index_builder.py` (importable y testeable), con un entrypoint
  delgado en `scripts/generate_index.py`. Sigue el patrón `src/` (librería) +
  `scripts/` (CLI) ya presente en el scaffold del proyecto.
- **Búsqueda**: filtro JS del lado cliente sobre el nombre del documento
  únicamente (no contenido) — cumple con "mecanismo de búsqueda" de forma mínima
  para esta fase; búsqueda de contenido queda para una fase posterior.
- **Estilo**: CSS mínimo embebido en el propio `index.html` (sin archivos
  separados, sin frameworks), consistente con "costo mínimo, sin dependencias
  externas" de `specs/mission.md`.
- **Comando Make**: se agrega un target `make site` (o similar) al Makefile para
  regenerar `index.html`, siguiendo la convención de comandos ya usada en el
  proyecto (`make init`, `make lint`, etc.).

## Contexto

- El contenido y las etiquetas de la página van en español, consistente con el
  resto del repositorio (`agenda.md`, `Comisiones.md`).
- El texto descriptivo del sitio se deriva de `specs/mission.md` (propósito y a
  quién sirve), resumido brevemente — no se copia el documento completo.
- No existe hoy ningún front-end en el proyecto (`specs/tech-stack.md` dice
  "Front-end: Ninguno"); esta fase introduce el primer HTML del proyecto, por lo
  que debe mantenerse deliberadamente simple.
- Los enlaces deben ser rutas relativas para que el índice funcione tanto
  abierto localmente (`file://`) como si se sirve estáticamente en el futuro.
- `agenda.docx` es un artefacto generado desde `agenda.md` vía `pandoc` — el
  índice debe listar el `.docx` como archivo indexado igual que cualquier otro,
  sin tratarlo de forma especial.