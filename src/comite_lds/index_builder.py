"""Escanea comite/ y comunidad/ (bajo docs/) para generar la página índice."""

import dataclasses
import html
import logging
import pathlib
import string

logger = logging.getLogger(__name__)

INDEXED_DIRS = ("comite", "comunidad")

DESCRIPTION_PARA_LIST = [
    "Punto de referencia para los vecinos de Lomas del Sol, Curridabat."
]

SITE_DESCRIPTION = "".join(
    "".join(["<p>", html.escape(desc), "</p>\n"])
    for desc in DESCRIPTION_PARA_LIST
)


_PAGE_TEMPLATE = string.Template("""\
---
layout: default
title: Comité de Vecinos de Lomas del Sol
---

# Comité de Vecinos de Lomas del Sol

$description
<p>
Enviá sugerencias y consultas a
<a href="mailto:lomasdelsolcomite@gmail.com">lomasdelsolcomite@gmail.com</a>.
</p>

<div class="doc-index">
<input id="filtro" type="text" placeholder="Filtrar documentos por nombre...">
$sections
</div>

<script>
document.getElementById("filtro").addEventListener("input", function (event) {
  var query = event.target.value.toLowerCase();
  document.querySelectorAll("li[data-name]").forEach(function (item) {
    var visible = item.dataset.name.indexOf(query) !== -1;
    item.style.display = visible ? "" : "none";
  });
});
</script>
""")

_SECTION_TEMPLATE = string.Template("""\
<h2>$folder</h2>
<ul>
$items
</ul>\
""")

_ENTRY_TEMPLATE = string.Template(
    '  <li data-name="$data_name"><a href="$link">$name</a>'
    '<span class="tipo">$extension</span></li>'
)


@dataclasses.dataclass(frozen=True)
class DocumentEntry:
    """Una entrada indexada del árbol de documentos.

    Attributes:
        name: Nombre del archivo sin extensión.
        folder: Ruta relativa de la carpeta contenedora.
        extension: Extensión del archivo, sin el punto, en minúsculas.
        link: Ruta relativa desde docs/ (raíz del sitio Jekyll) al archivo.
    """

    name: str
    folder: str
    extension: str
    link: str


def scan_documents(
    docs_root: pathlib.Path, indexed_dirs: tuple[str, ...] = INDEXED_DIRS
) -> list[DocumentEntry]:
    """Escanea recursivamente los directorios indexados en busca de documentos.

    Args:
        docs_root: Ruta a docs/, la raíz del sitio Jekyll.
        indexed_dirs: Rutas relativas a `docs_root` a escanear.

    Returns:
        Lista de DocumentEntry, ordenada por carpeta y luego por nombre.
    """
    docs_root = pathlib.Path(docs_root)
    entries = []
    for indexed_dir in indexed_dirs:
        base = docs_root / indexed_dir
        if not base.is_dir():
            logger.warning("Directorio indexado no encontrado: %s", base)
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.name.startswith("."):
                continue
            extension = path.suffix.lstrip(".").lower()
            link = path.relative_to(docs_root).as_posix()
            if extension == "md":
                # Con front matter, Jekyll convierte el .md a .html al
                # desplegar el sitio; el índice debe enlazar a ese artefacto.
                extension = "html"
                link = link[: -len("md")] + "html"
            entries.append(
                DocumentEntry(
                    name=path.stem,
                    folder=path.parent.relative_to(docs_root).as_posix(),
                    extension=extension,
                    link=link,
                )
            )
    entries.sort(key=lambda entry: (entry.folder, entry.name.lower()))
    return entries


def render_html(
    entries: list[DocumentEntry],
    description: str = SITE_DESCRIPTION
) -> str:
    """Genera la página índice (Markdown + front matter de Jekyll).

    Usa `layout: default` para que la portada tome el estilo minima del
    resto del sitio; la lista de documentos se emite como HTML embebido
    (kramdown la pasa sin tocar) para conservar el filtro por nombre.

    Args:
        entries: Lista de DocumentEntry a listar en el índice.
        description: Texto descriptivo del sitio.

    Returns:
        El contenido completo de index.md, como string.
    """
    grouped = {}
    for entry in entries:
        grouped.setdefault(entry.folder, []).append(entry)

    sections = [
        _SECTION_TEMPLATE.substitute(
            folder=html.escape(folder),
            items="\n".join(_render_entry(entry) for entry in grouped[folder]),
        )
        for folder in sorted(grouped)
    ]

    return _PAGE_TEMPLATE.substitute(
        description=description,
        sections="\n".join(sections),
    )


def _render_entry(entry):
    """Genera el `<li>` HTML correspondiente a una entrada indexada.

    Args:
        entry: DocumentEntry a renderizar.

    Returns:
        El fragmento HTML del `<li>`, como string.
    """
    return _ENTRY_TEMPLATE.substitute(
        data_name=html.escape(entry.name.lower()),
        link=html.escape(entry.link),
        name=html.escape(entry.name),
        extension=html.escape(entry.extension),
    )
