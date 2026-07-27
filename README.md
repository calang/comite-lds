# Comité Lomas del Sol

El propósito de este proyecto es proveer un punto de referencia para los vecinos de Lomas del Sol, con el fin de organizar y facilitar la comunicación, colaboración y participación en actividades comunitarias.

La motivación para cumplir con ese propósito es que la comunidad de Lomas del Sol se beneficie de un espacio centralizado donde los vecinos puedan acceder a información relevante, compartir ideas y coordinar esfuerzos para mejorar la calidad de vida en el vecindario.

<!-- TOC -->
* [Comité Lomas del Sol](#comité-lomas-del-sol)
  * [Requisitos](#requisitos)
  * [Configuración del entorno](#configuración-del-entorno)
  * [Comandos comunes](#comandos-comunes)
    * [uv](#uv)
  * [Estándares de codificación](#estándares-de-codificación)
  * [Uso de agentes de codificación con IA](#uso-de-agentes-de-codificación-con-ia)
  * [Estructura del proyecto](#estructura-del-proyecto)
  * [Referencias](#referencias)
<!-- TOC -->

## Funciones

La misión, hoja de ruta y plataforma tecnológica de este proyecto se describen en los documentos
- [mission.md](specs/mission.md)
- [roadmap.md](specs/roadmap.md)
- [tech-stack.md](specs/tech-stack.md)


## Requisitos Técnicos

Sistema Linux, MacOS o WSL con Python 3.14+

- Python 3.14+
- [`uv`](https://docs.astral.sh/uv/) — para el entorno basado en uv

## Configuración del entorno

- Las variables de entorno clave se cargan desde `.env` (generado a partir de `.env_template`).
- `PYTHONPATH` se establece como `PROJECT_ROOT`.
- El `.bashrc` a nivel de proyecto se ejecuta automáticamente cuando está presente en la raíz del proyecto (asume que `~/.bashrc` lo incluye).
- El soporte de GPU (TensorFlow/PyTorch con CUDA) requiere descomentar variables de entorno en `Makefile` y `.bashrc`, y agregar los paquetes correspondientes en `env.yml` o `pyproject.toml`.


## Comandos comunes

### uv

```bash
source .venv/bin/activate   # o anteponer a los comandos: uv run
make update-env             # ejecuta uv sync (auto-detectado)
make rm-env                 # elimina .venv (auto-detectado)
```

```bash
pytest                                     # ejecuta todas las pruebas (conda: directo; uv: uv run pytest)
pytest tests/path/test_foo.py::test_name   # ejecuta una sola prueba
pylint src/                                # linting (conda: directo; uv: uv run pylint src/)
make jupl                                  # inicia Jupyter Lab (auto-detecta el backend)
make help                                  # lista todos los objetivos del Makefile
```

## Estándares de codificación

Definidos en el skill `python-standards` de Claude.

El linting está configurado en `pylintrc` siguiendo la (Google Python Style Guide).

## Uso de agentes de codificación con IA

Este proyecto usa agentes de codificación con IA para asistir en la generación de código, depuración y documentación.

## Estructura del proyecto

```
- .claude/ - archivos de configuración para la API de Claude (si aplica)
- data/         # conjuntos de datos, datos preprocesados, resultados
- docs/         # documentación (system_architecture.md para detalles de arquitectura)
- experiments/  # scripts de experimentos y resultados
- models/       # modelos entrenados y checkpoints
- plans/        # planes de trabajo
- scripts/      # scripts de uso auxiliar
- specs/        # especificaciones de diseño y arquitectura
- src/          # código fuente (en PYTHONPATH como PROJECT_ROOT)
- tests/        # pruebas unitarias
- .bashrc       # configuración de bash a nivel de proyecto (incluida por ~/.bashrc)
- .env          # variables de entorno (creado a partir de .env_template)
- .env_template # plantilla para el archivo .env
- env.yml       # descripción del entorno conda (se elimina si se usa uv)
- Makefile - makefile con comandos para tareas comunes
- pyproject.toml # descripción del entorno uv (se elimina si se usa conda)
- requirements.txt  # complemento del entorno conda para env.yml (se elimina si se usa uv)
```

## Referencias

- [Spec-Driven Development with Coding Agents](https://www.deeplearning.ai/short-courses/spec-driven-development-with-coding-agents)