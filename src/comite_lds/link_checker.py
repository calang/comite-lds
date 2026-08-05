"""Detecta enlaces internos rotos entre documentos Markdown del repositorio."""

import dataclasses
import pathlib
import re
import subprocess

_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_EXTERNAL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
_NON_SLUG_RE = re.compile(r"[^\w\s-]", flags=re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")


@dataclasses.dataclass(frozen=True)
class BrokenLink:
    """Un enlace interno roto encontrado en un documento Markdown.

    Attributes:
        origin: Ruta del archivo que contiene el enlace, relativa al repo.
        line: Número de línea (1-indexado) donde aparece el enlace.
        text: Texto visible del enlace.
        target: Ruta/ancla de destino tal como aparece en el Markdown.
        reason: Motivo por el que el enlace se considera roto.
    """

    origin: str
    line: int
    text: str
    target: str
    reason: str


def find_markdown_files(repo_root: pathlib.Path) -> list[pathlib.Path]:
    """Lista los archivos `.md` versionados en el repositorio.

    Usa `git ls-files` para respetar `.gitignore` sin reimplementar sus
    reglas de exclusión.

    Args:
        repo_root: Raíz del repositorio Git.

    Returns:
        Lista de rutas absolutas a archivos `.md` versionados.
    """
    output = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=repo_root,
        check=True,
        capture_output=True,
    ).stdout
    return [
        repo_root / path
        for path in output.decode("utf-8").split("\0")
        if path
    ]


def extract_links(md_path: pathlib.Path) -> list[tuple[int, str, str]]:
    """Extrae los enlaces `[texto](destino)` de un archivo Markdown.

    Args:
        md_path: Ruta al archivo `.md` a analizar.

    Returns:
        Lista de tuplas `(línea, texto, destino)`, una por enlace
        encontrado, en el orden en que aparecen en el archivo.
    """
    links = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    for line_no, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = _INLINE_CODE_RE.sub("", line)
        for match in _LINK_RE.finditer(line):
            links.append((line_no, match.group(1), match.group(2)))
    return links


def slugify_heading(heading_text: str) -> str:
    """Genera el identificador de ancla que kramdown asigna a un encabezado.

    Replica el algoritmo de kramdown: minúsculas, se descarta toda
    puntuación salvo espacios y guiones, y los espacios se convierten en
    guiones.

    Args:
        heading_text: Texto del encabezado, sin los símbolos `#` iniciales.

    Returns:
        El slug correspondiente, como lo generaría kramdown.
    """
    lowered = heading_text.lower()
    stripped = _NON_SLUG_RE.sub("", lowered)
    return _WHITESPACE_RE.sub("-", stripped.strip())


def extract_heading_slugs(md_path: pathlib.Path) -> set[str]:
    """Recolecta los slugs de ancla de todos los encabezados de un archivo.

    Args:
        md_path: Ruta al archivo `.md` a analizar.

    Returns:
        Conjunto de slugs, uno por encabezado ATX (`#`..`######`) hallado.
    """
    slugs = set()
    for line in md_path.read_text(encoding="utf-8").splitlines():
        match = _HEADING_RE.match(line)
        if match:
            slugs.add(slugify_heading(match.group(2)))
    return slugs


def check_link(
    origin_path: pathlib.Path, target_ref: str
) -> str | None:
    """Verifica si un enlace interno resuelve a un destino válido.

    Args:
        origin_path: Archivo `.md` que contiene el enlace.
        target_ref: Destino del enlace tal como aparece en el Markdown
            (ruta relativa al archivo origen, con `#ancla` opcional).

    Returns:
        Un motivo de falla si el enlace está roto, o `None` si es válido o
        no corresponde validarlo (esquema externo, p. ej. `https://`).
    """
    if _EXTERNAL_SCHEME_RE.match(target_ref):
        return None

    path_part, _, anchor_part = target_ref.partition("#")

    target_path = (
        origin_path if not path_part else (origin_path.parent / path_part)
    )
    target_path = target_path.resolve()

    if not target_path.is_file():
        return "archivo no encontrado"

    if anchor_part and target_path.suffix == ".md":
        if anchor_part not in extract_heading_slugs(target_path):
            return "ancla no encontrada"

    return None


def check_all_links(repo_root: pathlib.Path) -> list[BrokenLink]:
    """Revisa todos los enlaces internos del repositorio y reporta los rotos.

    Args:
        repo_root: Raíz del repositorio Git.

    Returns:
        Lista de `BrokenLink`, en el orden en que se encontraron.
    """
    broken = []
    for md_path in find_markdown_files(repo_root):
        for line_no, text, target_ref in extract_links(md_path):
            reason = check_link(md_path, target_ref)
            if reason:
                broken.append(
                    BrokenLink(
                        origin=md_path.relative_to(repo_root).as_posix(),
                        line=line_no,
                        text=text,
                        target=target_ref,
                        reason=reason,
                    )
                )
    return broken
