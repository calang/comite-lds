# Plan — Conversión enlaces internos para Markdown hacia HTML (Fase 3)

## 1. Enlaces de prueba reales en documentos existentes

1.1. En `../../docs/Comité/agenda.md`, en la fila "Asuntos pendientes en cada
     comisión" o en la sección "Contenido previsto", agregar un enlace hacia
     `../../docs/Comité/tareas_pendientes.md` usando ruta relativa
     (`tareas_pendientes.md`, mismo directorio).
1.2. En `../../docs/Comité/agenda.md`, en la fila/sección "Propuesta de Comisión de
     Tecnología", agregar un enlace con ancla hacia la sección
     correspondiente de `../../docs/Comunidad/Comisiones.md`
     (`../comunidad/comisiones.md#3-comisión-de-tecnología`), confirmando
     antes el slug exacto que genera `kramdown` para ese encabezado (mismo
     patrón ya usado en el TOC manual de `Comisiones.md`).

## 2. Documentar la convención

2.1. Agregar a `.claude/CLAUDE.md`, en la sección "Working with the committee
     documents", una entrada sobre enlaces internos: usar ruta relativa al
     archivo `.md` destino (con `#ancla` si aplica), nunca `/docs/...` ni
     ruta absoluta — Jekyll (`jekyll-relative-links`, activado por defecto en
     el gem `github-pages`, no configurable) reescribe `.md` → `.html`
     automáticamente al publicar.
2.2. Aclarar en el mismo punto que esto solo aplica a `.md` bajo `docs/` (lo
     que Jekyll construye); enlaces desde fuera de `docs/` (`README.md`,
     `specs/`) hacia adentro no se reescriben.

## 3. Validación en el sitio publicado

3.1. Mergear a `main` y esperar el despliegue automático
     (`.github/workflows/pages.yml`).
3.2. Abrir `https://calang.github.io/comite-lds/comite/agenda.html` y
     confirmar que ambos enlaces nuevos:
     - apuntan a `.html` (no a `.md` crudo),
     - el enlace con ancla salta a la sección correcta de
       `comisiones.html`.