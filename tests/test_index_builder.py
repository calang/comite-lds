"""Tests para src.comite_lds.index_builder."""

import html

import pytest

from src.comite_lds import index_builder


@pytest.fixture
def fake_repo(tmp_path):
    """Crea un árbol docs/ de prueba con comite/ y comunidad/.

    Args:
        tmp_path: Directorio temporal provisto por pytest.

    Returns:
        La ruta a docs/ del árbol de prueba (raíz del sitio Jekyll).
    """
    docs_root = tmp_path / "docs"
    comite = docs_root / "comite" / "agenda-minutas"
    comite.mkdir(parents=True)
    (docs_root / "comite" / "Comisiones.md").write_text("contenido")
    (comite / "minuta.pdf").write_text("contenido")
    (comite / ".gitkeep").write_text("")

    comunidad = docs_root / "comunidad"
    comunidad.mkdir(parents=True)
    (comunidad / "emprendimientos & vecinos.md").write_text("contenido")

    return docs_root


def test_scan_documents_finds_all_non_hidden_files(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    links = {entry.link for entry in entries}
    assert links == {
        "comite/comisiones.html",
        "comite/agenda-minutas/minuta.pdf",
        "comunidad/emprendimientos & vecinos.html",
    }


def test_scan_documents_links_markdown_to_rendered_html(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    md_entries = [entry for entry in entries if entry.name == "comisiones"]
    assert len(md_entries) == 1
    assert md_entries[0].link == "comite/comisiones.html"
    assert md_entries[0].extension == "html"


def test_scan_documents_leaves_non_markdown_extension_untouched(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    pdf_entries = [entry for entry in entries if entry.name == "minuta"]
    assert len(pdf_entries) == 1
    assert pdf_entries[0].link == "comite/agenda-minutas/minuta.pdf"
    assert pdf_entries[0].extension == "pdf"


def test_scan_documents_skips_hidden_files(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    assert all(not entry.name.startswith(".") for entry in entries)


def test_scan_documents_sorts_by_folder_then_name(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    keys = [(entry.folder, entry.name.lower()) for entry in entries]
    assert keys == sorted(keys)


def test_scan_documents_warns_on_missing_dir(tmp_path, caplog):
    with caplog.at_level("WARNING"):
        entries = index_builder.scan_documents(tmp_path)

    assert not entries
    assert "no encontrado" in caplog.text


def test_render_html_includes_a_link_per_entry(fake_repo):
    entries = index_builder.scan_documents(fake_repo)
    output = index_builder.render_html(entries)

    for entry in entries:
        assert f'href="{html.escape(entry.link)}"' in output


def test_render_html_escapes_special_characters(fake_repo):
    entries = index_builder.scan_documents(fake_repo)
    output = index_builder.render_html(entries)

    assert "emprendimientos &amp; vecinos" in output
    assert "emprendimientos & vecinos.md" not in output


def test_render_html_includes_filter_script(fake_repo):
    entries = index_builder.scan_documents(fake_repo)
    output = index_builder.render_html(entries)

    assert '<input id="filtro"' in output
    assert "<script>" in output
    assert "data-name" in output
