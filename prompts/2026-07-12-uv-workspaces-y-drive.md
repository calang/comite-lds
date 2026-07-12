# Workspaces de uv y acceso a Google Drive
Creado el 2026-07-12

## Pregunta

como parte de la formación del comité, tengo interés en producir herramientas de IT que faciliten el trabajo de la misma. he pensado que talvez podría crear un sub-espacio (workspace) en este repositorio para producir el código con el que se formen esas herramientas. ¿es esta una buena idea o es preferible crear un repositorio aparte para desarrollar esas herramientas? muestra pros y contras de cada una de esas opciones. agrega una breve explicación inicial de como funcionan los workspaces con uv y como se pueden utilizar dentro de este repositorio, mediante Pycharm y claude.

## Respuesta

### Cómo funcionan los workspaces de uv (breve)

Un **workspace** de uv es un `pyproject.toml` raíz que declara miembros (`[tool.uv.workspace] members = [...]`), donde cada miembro es su propio paquete con su propio `pyproject.toml`. Todos comparten:

- **Un solo `.venv`** en la raíz del workspace (no uno por paquete).
- **Un solo `uv.lock`** — resuelve las dependencias de todos los miembros juntos, evitando versiones incompatibles entre herramientas.
- Los miembros pueden depender entre sí vía `[tool.uv.sources] mi_paquete = { workspace = true }`, sin publicar a PyPI.

Comandos clave: `uv sync` (raíz) instala todo; `uv run --package <nombre> ...` ejecuta algo de un miembro específico; `uv add --package <nombre> <dep>` agrega una dependencia solo a ese miembro.

**En este repo**: hoy `src/` es un solo scaffold vacío, no varios paquetes — no hay todavía necesidad real de un workspace multi-paquete. Si se crean varias herramientas independientes (ej. un generador de agendas, un bot de notificaciones), ahí sí conviene: cada una como `herramientas/<nombre>/pyproject.toml`, listada en `members` del `pyproject.toml` raíz.

**PyCharm**: se abre la raíz del repo como proyecto y se apunta el intérprete a `REPO_ROOT/.venv/bin/python` (creado por `uv sync`). Como el venv es compartido, PyCharm resuelve imports de todos los miembros sin configuración especial; solo hay que marcar cada carpeta de miembro como "Sources Root" si el autocompletado no los detecta.

**Claude Code**: puede tener un `CLAUDE.md` por sub-carpeta de herramienta (scoped), además del `CLAUDE.md` raíz — así cada herramienta documenta sus propias convenciones sin mezclarlas con las del repo de documentos del comité.

### ¿Mismo repo o repo aparte?

| | Mismo repo (workspace) | Repo aparte |
|---|---|---|
| **Pros** | Ya está el scaffold pensado para esto (`src/`, `scripts/`, etc. en CLAUDE.md); un solo lugar para clonar/onboardear a otros miembros del comité; las herramientas pueden leer directamente `docs/agenda.md`, `docs/comisiones.md` sin cruzar repos | Separa dos ritmos distintos: documentos (ediciones manuales, poco frecuentes) vs. código (commits frecuentes, CI, releases); permite abrir el código a otros sin exponer contenido interno del comité; versionado de herramientas no se mezcla con snapshots de actas |
| **Contras** | El `git log` y los PRs mezclan cambios de actas con cambios de código, lo que ensucia la revisión; si más adelante se quiere publicar/abrir solo el código, toca separar historial | Dos repos que mantener y clonar; si la herramienta necesita leer las actas, hay que pasarle los archivos de algún modo (submódulo, copia, input manual) |

**Recomendación**: empezar dentro de este repo. El scaffold ya está pensado para eso, el proyecto es chico y de un solo mantenedor, y evita la fricción de sincronizar dos repos para algo que hoy es solo una idea. Si en el futuro una herramienta crece lo suficiente como para tener su propio ciclo de release, CI, o se quiere compartir fuera del comité, en ese momento se separa (uv/git lo permiten sin gran esfuerzo, aunque se pierde el historial fácil de portar).

---

## Pregunta

he pensado en mantener actas, agendas en un google Drive compartido, como hemos hecho hasta ahora. ¿es posible dar acceso a las herramientas del comité a estos documentos y a claude, de manera que se puedan utilizar por la mismas y se aprenda de ellos en forma regular?

## Respuesta

Sí es posible, pero conviene separar dos accesos distintos y aclarar qué significa "aprender" en este contexto.

**Acceso a los documentos:**
- *Para Claude directamente* (como en esta conversación): existe un conector nativo de Google Drive vía MCP, ya disponible en este entorno (solo requiere autorización OAuth una vez). Con eso, Claude puede leer/buscar las actas y agendas del Drive compartido sin que se mueva nada.
- *Para herramientas propias del comité* (scripts que corran solos, sin que alguien abra Claude): necesitan su propia integración con la API de Google Drive (credenciales OAuth o una cuenta de servicio), independiente del conector de Claude.

**Sobre "aprender de ellos en forma regular":** los modelos de Claude no se entrenan ni se actualizan con lo que leen — no hay aprendizaje continuo automático. Lo que sí existe es releer los documentos frescos cada vez que se necesiten (perfectamente suficiente para el volumen de actas de un comité de vecinos), o, si el archivo crece mucho, construir un índice de búsqueda (RAG) que se actualice periódicamente. Para el tamaño actual, no haría falta lo segundo.

**El tradeoff principal**: el conector de Drive es acceso inmediato sin código, pero depende de que alguien lo use interactivamente con su cuenta de Claude autorizada; una integración propia vía API permite automatización desatendida (ej. resumir semanalmente actas nuevas) pero agrega manejo de credenciales y código a mantener en el repo.

Recomendación: empezar con el conector de Drive para uso ad-hoc, y solo construir la integración propia si de verdad se necesita automatización sin intervención humana (ej. un cron que resuma actas nuevas cada semana).