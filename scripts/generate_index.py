#!/usr/bin/env python3
"""Genera index.html a partir de docs/comite y docs/comunidad."""

import logging
import pathlib

from src.comite_lds import index_builder

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Escanea docs/ y escribe index.html en la raíz del repositorio."""
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    entries = index_builder.scan_documents(repo_root)
    output_path = repo_root / "index.html"
    output_path.write_text(index_builder.render_html(entries), encoding="utf-8")
    logger.info("Generado %s con %d documentos", output_path, len(entries))


if __name__ == "__main__":
    main()
