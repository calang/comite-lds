#!/usr/bin/env python3
"""Genera index.md a partir de docs/Comité y docs/Comunidad."""

import logging
import os
import pathlib

from src.comite_lds import index_builder

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Escanea docs/ y escribe docs/index.md."""
    docs_root = pathlib.Path(os.environ["PROJECT_ROOT"]) / "docs"
    entries = index_builder.scan_documents(docs_root)
    output_path = docs_root / "index.md"
    output_path.write_text(index_builder.render_html(entries), encoding="utf-8")
    logger.info("Generado %s con %d documentos", output_path, len(entries))


if __name__ == "__main__":
    main()
