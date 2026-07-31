# Análisis de `docs/old`: métodos para explorar el archivo histórico

## 1. Qué hay realmente en `docs/old`

`docs/old` es un volcado sin organizar de dos archivos de comités vecinales distintos, no una colección de notas ya estructuradas:

- **`COMITE VECINAL/`** — materiales del comité del barrio **La Lía**, 2017–2020 (boletines, agenda comunal, presentaciones, reglamento).
- **`Arcivo COMITE CARLOS/`** — materiales del comité de **Lomas del Sol**, la mayoría de 2023–2026 (actas, minutas, oficios, agenda de seguimiento de pendientes). Es el más relevante para el trabajo actual del Comité.

Datos concretos (704 archivos, 3.5 GB):

| Formato | Archivos | Tamaño | Naturaleza |
|---|---|---|---|
| `.jpg` | 374 | 1.20 GB | Fotos de eventos, capturas de pantalla, hojas de firmas escaneadas |
| `.mp4` | 13 | 842 MB | Videos de eventos |
| `.psd` (y variantes) | 8 | ~748 MB | Artes fuente de boletines/afiches |
| `.pptx` | 65 | 285 MB | Presentaciones, boletines |
| `.pdf` | 57 | 222 MB | Documentos formales, algunos escaneados como imagen |
| `.docx` | 144 | 24 MB | Actas, minutas, oficios, reglamento — el texto más denso del archivo |
| `.htm`/`.html`/`.mht` | 20 | 33 MB | Páginas guardadas (Gmail, búsquedas de Google) — bajo valor informativo |
| `.xls`, `.rar`, `.png`, `.tmp` | 18 | 135 MB | Menores / `.rar` sin explorar |

Distribución temporal: 2 archivos de 2017, 494 de 2018 (pico de actividad de La Lía), 67 de 2019, 30 dispersos entre 2020–2023, y un repunte de 111 en 2024–2026 (actividad reciente de Lomas del Sol).

**Implicación práctica:** el contenido con valor real para "propuestas, incidencias, proyectos" está concentrado en ~267 documentos de oficina (docx/pptx/pdf/xls); fotos y video son evidencia secundaria, no fuente primaria de decisiones. Varios PDF son escaneos de imagen (necesitan OCR, no solo extracción de texto). Ya hay herramientas locales instaladas que cubren esto sin nada nuevo: `pandoc`, `tesseract` (con paquete de idioma **español** ya instalado), `libreoffice`/`soffice`, `ffmpeg`, `uv`.

## 2. Métodos evaluados

### Método A — Conversión + síntesis única indexada (recomendado)

1. Convertir una sola vez todo `.docx`/`.pptx`/`.pdf` a Markdown (`pandoc`/`soffice --headless`; OCR con `tesseract -l spa` para PDFs e imágenes escaneadas que lo requieran).
2. Con eso ya en Markdown, un solo pase de síntesis (LLM) produce **un archivo índice**: una tabla con tema, tipo (propuesta/incidencia/proyecto), comité (La Lía o Lomas del Sol), fecha de origen, última actualización, documentos relacionados, estado, y si requiere atención del Comité actual.
3. Cada consulta futura primero lee ese índice (pequeño, rápido); solo si hace falta detalle se abre el `.md` original correspondiente.

Es una versión reforzada de la opción 1 propuesta: mismo backbone de conversión a Markdown, pero con un paso de construcción de índice para no tener que re-derivar las relaciones entre documentos en cada consulta. Encaja con la convención ya usada en este repo (Markdown como fuente de verdad).

### Método B — Conversión + escaneo completo del corpus en cada consulta

Mismo paso de conversión a Markdown que el Método A, pero **sin** paso de síntesis: cada pregunta hace que el agente relea/regrep-ee todo el corpus convertido y razone desde cero. Es la opción 1 tal como se planteó originalmente.

### Método C — Base de conocimiento tipo grafo (Graphify / familia GraphRAG)

Herramientas evaluadas: **Graphify** (github.com/Graphify-Labs/graphify — verificado: CLI en Python 3.10+/`uv`, procesa PDFs, imágenes y video/audio (transcripción local con `faster-whisper`, útil para los 13 `.mp4`), soporte de Office marcado como opcional; construye un grafo con aristas `EXTRACTED`/`INFERRED`, consultable con `graphify query`) y alternativas más maduras de la misma familia como **Cognee** o **Graphiti** (self-hosted, Apache 2.0, grafo local sin base de datos en la nube).

Construye relaciones explícitas entre entidades (documentos, personas, temas) y permite trazar caminos ("¿qué conecta la propuesta X con la incidencia Y?"), pero su modelo de extracción está pensado para código/documentación técnica, no para "propuesta/incidencia/estado" de un comité vecinal — requiere ajustar prompts para que la ontología tenga sentido en este dominio.

## 3. Tabla comparativa

| # | Método | Precisión esperada | Tiempo de síntesis (una vez) | Tiempo de respuesta por consulta | Complejidad de instalación |
|---|---|---|---|---|---|
| 1 | **A — Conversión + índice de síntesis** | Alta (el índice fija relaciones una vez; se corrige con más facilidad que re-derivarlas cada vez) | Media (~267 documentos, conversión rápida con herramientas ya instaladas + 1–2 pases de síntesis por LLM) | Rápido (lee un índice de pocos KB antes de tocar el corpus completo) | Ninguna nueva — `pandoc`, `tesseract -l spa`, `soffice` ya están instalados |
| 2 | **B — Conversión + escaneo completo por consulta** | Media (misma calidad de texto que A, pero cada consulta puede inferir relaciones de forma distinta al no existir un registro persistente) | Baja (solo el paso de conversión, sin síntesis extra) | Lento (cada pregunta relee/regrep-ea decenas de MB de Markdown; empeora si el archivo crece) | Ninguna nueva |
| 3 | **C — Grafo de conocimiento (Graphify / GraphRAG)** | Variable (el trazado de relaciones es potente, pero la ontología no está pensada para "propuesta/incidencia/estado" de un comité; soporte de Office es opcional y necesita verificarse; herramienta de un solo mantenedor, menos probada en este tipo de corpus) | Alta (pase semántico por LLM sobre cada documento/imagen + transcripción de 842 MB de video + instalación y configuración de infraestructura de grafo) | Rápido una vez construido, pero con curva de aprendizaje para formular bien las consultas al grafo | Media–alta — instalar `uv tool install`, clave de API para el pase semántico, aprender el modelo de consulta |

## 4. Justificación de la evaluación

- **Precisión**: se favorece a los métodos que dejan un registro explícito y corregible de "qué es cada tema y cómo se relaciona", en vez de que el agente lo re-infiera en cada pregunta (por eso A > B). C puede ser tan o más preciso en teoría, pero su modelo de extracción no está calibrado para este dominio (comité vecinal, no código), lo que introduce riesgo de relaciones mal etiquetadas o irrelevantes.
- **Tiempo de síntesis**: dominado por (a) cuántos documentos hay que convertir/OCR-ear (267 sustantivos, corpus de texto pequeño una vez extraído) y (b) si hay un pase semántico adicional por LLM sobre todo el contenido, incluyendo medios pesados (video). B es el más barato de construir porque no sintetiza nada; C es el más caro porque su pase semántico cubre también imágenes y transcribe video.
- **Tiempo de respuesta**: depende de si la consulta parte de un resumen pequeño (A, C) o tiene que releer el corpus completo cada vez (B). B escala mal a medida que se agreguen más documentos al archivo.
- **Ajuste al corpus real**: este archivo es pequeño (267 documentos sustantivos, ~30 MB de texto extraíble en `.docx`, el resto en PDF/PPTX con más peso gráfico que textual), de un solo comité vecinal pequeño, en español. La infraestructura de grafo (C) tiene un costo fijo de instalación y aprendizaje que solo se justifica en corpus mucho más grandes o con relaciones más complejas que "qué propuestas siguen abiertas". Por eso A queda primero, B segundo (funciona, pero no cumple bien el requisito de "cómo se relacionan entre sí" sin volver a razonar cada vez) y C tercero.

## 5. Recomendación

Empezar por el **Método A**. Es el único que, con las herramientas ya instaladas en esta máquina, deja un artefacto persistente y de bajo costo (el índice de síntesis) que responde directamente a las tres preguntas del pedido original: qué propuestas/incidencias/proyectos hay, cuándo se crearon/actualizaron, y cómo se relacionan — sin requerir infraestructura nueva. Si más adelante el archivo crece mucho o se necesita trazar relaciones más finas entre documentos, migrar a C (idealmente Cognee/Graphiti en vez de Graphify, por estar más probados) es la siguiente escalada razonable.
