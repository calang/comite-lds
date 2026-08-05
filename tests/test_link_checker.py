"""Tests para src.comite_lds.link_checker."""

import subprocess

from src.comite_lds import link_checker


def test_slugify_heading_matches_kramdown_toc_slugs():
    cases = {
        "1. Comisión de Infraestructura": "1-comisión-de-infraestructura",
        "3. Comisión de Tecnología": "3-comisión-de-tecnología",
        (
            "4. Comisión de Actividades Sociales (Integración, "
            "recreación y Bienestar Social)"
        ): (
            "4-comisión-de-actividades-sociales-integración-"
            "recreación-y-bienestar-social"
        ),
    }
    for heading, expected_slug in cases.items():
        assert link_checker.slugify_heading(heading) == expected_slug


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_check_all_links_reports_only_broken_links(tmp_path):
    _write(tmp_path / "b.md", "# Sección Uno\n\ncontenido\n")
    _write(tmp_path / "image.png", "fake-png")
    _write(
        tmp_path / "a.md",
        "\n".join([
            "[enlace válido](b.md)",
            "[ancla válida](b.md#sección-uno)",
            "[archivo inexistente](no_existe.md)",
            "[ancla inexistente](b.md#no-existe)",
            "![imagen válida](image.png)",
            "![imagen rota](no_existe.png)",
            "[externo](https://example.com/pagina.md)",
            "",
        ]),
    )
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)

    broken = link_checker.check_all_links(tmp_path)

    broken_by_line = {b.line: b.reason for b in broken}
    assert broken_by_line == {
        3: "archivo no encontrado",
        4: "ancla no encontrada",
        6: "archivo no encontrado",
    }


def test_extract_links_ignores_plain_text(tmp_path):
    md_path = _write(
        tmp_path / "a.md", "sin enlaces aquí, solo [texto sin destino"
    )

    assert link_checker.extract_links(md_path) == []


def test_extract_links_ignores_inline_code_and_fenced_blocks(tmp_path):
    md_path = _write(
        tmp_path / "a.md",
        "\n".join([
            "Ejemplo: `[texto](ruta.md)` es solo sintaxis de muestra.",
            "```",
            "[también ignorado](otra_ruta.md)",
            "```",
            "[enlace real](b.md)",
            "",
        ]),
    )
    _write(tmp_path / "b.md", "contenido")

    assert link_checker.extract_links(md_path) == [
        (5, "enlace real", "b.md")
    ]
