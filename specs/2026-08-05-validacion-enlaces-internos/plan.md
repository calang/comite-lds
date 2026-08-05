# Plan — Validación de enlaces internos rotos (Fase 4)

## 1. Módulo de detección (`src/comite_lds/link_checker.py`)

1.1. `find_markdown_files(repo_root)`: recorre el repositorio y devuelve la
lista de archivos `.md` a revisar (excluyendo lo que Git ignora, p. ej. vía
`git ls-files` o filtrando directorios como `.git/`, `data/`, `.venv/`).

1.2. `extract_links(md_path)`: parsea el contenido de un `.md` con una
expresión regular sobre el patrón `[texto](ruta)` y devuelve, por cada
enlace encontrado, `(línea, texto, ruta_destino)`. Ignora enlaces cuyo
destino empiece con un esquema (`http://`, `https://`, `mailto:`).

1.3. `slugify_heading(texto_encabezado)`: replica el algoritmo de slugs de
kramdown (minúsculas, quita/convierte símbolos, espacios a guiones).
Validar contra los slugs reales del TOC de `Comisiones.md`.

1.4. `extract_heading_slugs(md_path)`: lee un `.md` y devuelve el conjunto de
slugs generados a partir de sus encabezados (`#`, `##`, ...) usando
`slugify_heading`.

1.5. `check_link(origin_path, target_ref, repo_root) -> BrokenLink | None`:
resuelve `target_ref` (ruta + `#ancla` opcional) relativa a `origin_path`;
separa ruta y ancla; verifica que el archivo destino exista; si el destino
es `.md` y hay ancla, verifica que la ancla esté en
`extract_heading_slugs(destino)`. Devuelve un `BrokenLink` (dataclass con
origen, línea, texto, motivo) si algo falla, o `None` si el enlace es
válido.

1.6. `check_all_links(repo_root) -> list[BrokenLink]`: orquesta 1.1–1.5
sobre todo el repositorio y devuelve la lista completa de enlaces rotos.

## 2. Script ejecutable (`scripts/check_links.py`)

2.1. Punto de entrada estilo `scripts/generate_index.py`: usa
`PROJECT_ROOT` del entorno, llama a `link_checker.check_all_links`, imprime
cada `BrokenLink` (archivo:línea — texto — motivo) vía `logging`.

2.2. Sale con código 1 si `check_all_links` devuelve al menos un resultado;
código 0 si la lista está vacía.

## 3. Integración en Makefile

3.1. Nuevo target `check-links`: `uv run python scripts/check_links.py`.

3.2. Target `site` pasa a depender de `check-links` como prerrequisito
(`site: check-links`), de modo que si falla, `make site` se detiene sin
ejecutar `generate_index.py` (comportamiento nativo de Make).

3.3. Agregar `check-links` a la lista `.PHONY` y a `make help` si el
Makefile documenta targets ahí (seguir el patrón existente de comentarios
`# target: nombre - descripción`).

## 4. Tests (`tests/test_link_checker.py`)

4.1. Fixture con árbol temporal (`tmp_path`) de `.md` con: enlace válido a
otro `.md`, enlace válido con ancla válida, enlace a archivo inexistente,
enlace con ancla inexistente, enlace a archivo no-Markdown existente e
inexistente, enlace externo (`https://...`) que debe ignorarse.

4.2. Test de `slugify_heading` contra los slugs reales del TOC de
`Comisiones.md` (encabezados con acentos, paréntesis, mayúsculas).

4.3. Test de `check_all_links` end-to-end sobre el árbol fixture: verifica
que devuelva exactamente los enlaces rotos esperados (ni más ni menos) y
que ignore los externos.

## 5. Validación manual

5.1. Correr `make check-links` sobre el repo real: confirmar que los
enlaces reales existentes (Grupos_de_WhatsApp.md, Comisiones.md, agenda de
2026-07-14) no se reporten como rotos.

5.2. Introducir temporalmente un enlace roto en un archivo de prueba fuera
de `docs/` (o revertible), correr `make site` y confirmar que se detiene
con mensaje de error antes de tocar `docs/index.md`.
