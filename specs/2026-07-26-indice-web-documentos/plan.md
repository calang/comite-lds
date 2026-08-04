# Plan — Índice web de documentos (Fase 1)

## 1. Escaneo de documentos

1.1. Crear `src/comite_lds/__init__.py` (nuevo paquete).
1.2. En `src/comite_lds/index_builder.py`, escribir una función que recorra
     recursivamente `../../docs/Comité/` y `../../docs/Comunidad/` y devuelva una lista de
     entradas (nombre, carpeta origen relativa, extensión, ruta relativa desde
     la raíz del repo).
1.3. Ordenar las entradas: primero por carpeta origen, luego alfabéticamente
     por nombre dentro de cada carpeta.
1.4. Excluir archivos ocultos/temporales (p. ej. `.$*.bkp`, `.gitkeep`).

## 2. Generación del HTML

2.1. Escribir una función de render en `index_builder.py` que reciba la lista
     de entradas y produzca el string HTML completo, usando `string.Template`
     o f-strings de la librería estándar (sin Jinja2).
2.2. Escapar correctamente nombres de archivo/rutas al insertarlos en el HTML
     (usar `html.escape`).
2.3. Incluir en el HTML:
     - Encabezado con título del sitio y descripción breve (derivada de
       `specs/mission.md`).
     - Índice agrupado por carpeta origen, con enlaces `<a href="...">`.
     - Un `<input>` de texto para filtrar el índice.
2.4. CSS mínimo embebido en un `<style>` dentro del mismo archivo.

## 3. Filtro de búsqueda (cliente)

3.1. Escribir JS vanilla embebido en un `<script>` dentro del `index.html`
     generado: al escribir en el `<input>`, oculta (`display:none`) las
     entradas del índice cuyo nombre no contenga el texto ingresado
     (case-insensitive).
3.2. Sin dependencias externas, sin build step.

## 4. Entrypoint y Makefile

4.1. Crear `scripts/generate_index.py`: script delgado que importa
     `index_builder`, ejecuta el escaneo + render, y escribe `index.html` en la
     raíz del repo.
4.2. Agregar target `site` al `Makefile` que ejecute
     `uv run python scripts/generate_index.py`.
4.3. Documentar el comando en la sección "Common commands" de
     `.claude/CLAUDE.md` (o dejar nota para hacerlo en la validación manual).

## 5. Tests

5.1. `tests/test_index_builder.py`: probar el escaneo (usando un directorio
     temporal con archivos de prueba) y el render (verificar que las entradas
     aparecen como enlaces, que el HTML escapa caracteres especiales, y que el
     filtro JS está presente en el output).
5.2. Verificar que `uv run pytest` pasa y `make lint` no reporta errores nuevos
     sobre el código agregado.