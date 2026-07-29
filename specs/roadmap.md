# Hoja de Ruta

Esto describe las fases en el desarrollo de esta solución.

Las fases son intencionalmente pequeñas — cada una es una porción de trabajo entregable, revisable y comprobable de forma independiente.

---

## Fase 1 — Versión mínima inicial

### Objetivo

Proveer acceso a la documentación bajo el docs/comite/ y docs/comunidad/
a través de una página web (en html) de forma organizada, con un mecanismo de búsqueda y recuperación de información.

### Funcionalidades

- [x] Presentar una página web inicial con una descripción del sitio, un índice de documentos y enlaces a los mismos.


## Fase 2 — Despliegue en hospedaje gratuito

### Objetivo

Automatizar el despliegue de la página web en un hospedaje gratuito, asegurando que los cambios en la documentación se reflejen automáticamente en el sitio web.

### Funcionalidades

- [x] Configurar un flujo de trabajo de CI/CD para desplegar automáticamente la página web en un hospedaje gratuito (por ejemplo, GitHub Pages u Oracle Open Cloud) cada vez que se actualice la documentación.

---

## Fase 3 — Conversión enlaces internos para Markdown hacia HTML

### Objetivo

Permitir que los documentos internos puedan tener enlaces hacia otros documentos Markdown, y que estos enlaces se conviertan automáticamente a HTML en el sitio web.

### Funcionalidades

- [ ] Implementar un mecanismo que detecte enlaces internos en los documentos Markdown y los convierta a enlaces HTML equivalentes en el sitio web.

---

Fases posteriores (aún no planificadas): [...].