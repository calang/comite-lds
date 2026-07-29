"""Escanea comite/ y comunidad/ (bajo docs/) para generar un índice HTML."""

import dataclasses
import html
import logging
import pathlib
import string

logger = logging.getLogger(__name__)

INDEXED_DIRS = ("comite", "comunidad")

SITE_DESCRIPTION = (
    "Punto de referencia para los vecinos de Lomas del Sol: acceso "
    "centralizado a estatutos, actas, agendas y demás documentos del "
    "Comité de Vecinos."
)

_PAGE_TEMPLATE = string.Template("""\
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Comité de Vecinos de Lomas del Sol</title>
<style>
  body {
    font-family: sans-serif;
    max-width: 60rem;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.5;
  }
  h1 { margin-bottom: 0.25rem; }
  #filtro { width: 100%; padding: 0.5rem; margin: 1rem 0; font-size: 1rem; }
  h2 { margin-top: 2rem; border-bottom: 1px solid #ccc; }
  ul { list-style: none; padding: 0; }
  li { padding: 0.25rem 0; }
  .tipo { color: #666; font-size: 0.85em; margin-left: 0.5em; }
</style>
</head>
<body>
<h1>Comité de Vecinos de Lomas del Sol</h1>
<p>$description</p>
<input id="filtro" type="text" placeholder="Filtrar documentos por nombre...">
$sections
<script>
document.getElementById("filtro").addEventListener("input", function (event) {
  var query = event.target.value.toLowerCase();
  document.querySelectorAll("li[data-name]").forEach(function (item) {
    var visible = item.dataset.name.indexOf(query) !== -1;
    item.style.display = visible ? "" : "none";
  });
});
</script>
</body>
</html>
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
    entries: list[DocumentEntry], description: str = SITE_DESCRIPTION
) -> str:
    """Genera el HTML completo del índice a partir de las entradas escaneadas.

    Args:
        entries: Lista de DocumentEntry a listar en el índice.
        description: Texto descriptivo del sitio a mostrar en el encabezado.

    Returns:
        El documento HTML completo, como string.
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
        description=html.escape(description),
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
