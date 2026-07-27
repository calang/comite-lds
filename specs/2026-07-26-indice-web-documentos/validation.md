# Validation — Índice web de documentos (Fase 1)

## Automatizada

- `uv run pytest` pasa, incluyendo los nuevos tests de `tests/test_index_builder.py`:
  - El escaneo encuentra todos los archivos esperados en un árbol de prueba y
    los agrupa/ordena correctamente.
  - El render produce HTML válido (bien formado) con un `<a href>` por cada
    entrada esperada.
  - Nombres de archivo con caracteres especiales (tildes, espacios, `&`, etc.)
    quedan correctamente escapados en el HTML.
  - El `<script>` de filtrado está presente en el HTML generado.
- `make lint` no reporta errores nuevos sobre `src/comite_lds/index_builder.py`
  ni `scripts/generate_index.py`.

## Manual

- Ejecutar `make site` (o el comando equivalente) y confirmar que se genera
  `index.html` en la raíz del repo sin errores.
- Abrir `index.html` directamente en un navegador (`file://`) y verificar:
  - La descripción del sitio se lee correctamente y en español.
  - Todos los documentos actuales de `docs/comite/` y `docs/comunidad/`
    aparecen listados, agrupados por carpeta.
  - Cada enlace abre el documento correcto (md, pdf, odt, docx).
  - Escribir en el campo de filtro reduce la lista a las entradas cuyo nombre
    coincide (probar con un término que coincida y uno que no coincida con
    ningún documento).
  - La página se ve razonablemente ordenada sin CSS externo (ancho, espaciado,
    legibilidad básica).
- Revisar que el tono/idioma del texto de la página coincide con el resto del
  repositorio (español, conciso, sin jerga técnica).

## Definición de terminado

- [ ] `index.html` se genera correctamente desde `docs/comite/` y `docs/comunidad/`.
- [ ] El filtro de búsqueda funciona sobre nombres de documento, sin backend.
- [ ] Tests nuevos pasan y `make lint` está limpio.
- [ ] Item correspondiente en `specs/roadmap.md` (Fase 1) marcado como `[x]`.
- [ ] Cambios revisados y mergeados a `main`.