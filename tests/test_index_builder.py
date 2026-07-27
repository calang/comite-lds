"""Tests para src.comite_lds.index_builder."""

import html

import pytest

from src.comite_lds import index_builder


@pytest.fixture
def fake_repo(tmp_path):
    """Crea un árbol de repositorio de prueba con docs/comite y docs/comunidad.

    Args:
        tmp_path: Directorio temporal provisto por pytest.

    Returns:
        La ruta a la raíz del repositorio de prueba.
    """
    comite = tmp_path / "docs" / "comite" / "agenda-minutas"
    comite.mkdir(parents=True)
    (tmp_path / "docs" / "comite" / "comisiones.md").write_text("contenido")
    (comite / "minuta.pdf").write_text("contenido")
    (comite / ".gitkeep").write_text("")

    comunidad = tmp_path / "docs" / "comunidad"
    comunidad.mkdir(parents=True)
    (comunidad / "emprendimientos & vecinos.md").write_text("contenido")

    return tmp_path


def test_scan_documents_finds_all_non_hidden_files(fake_repo):
    entries = index_builder.scan_documents(fake_repo)

    links = {entry.link for entry in entries}
    assert links == {
        "docs/comite/comisiones.md",
        "docs/comite/agenda-minutas/minuta.pdf",
        "docs/comunidad/emprendimientos & vecinos.md",
    }


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
