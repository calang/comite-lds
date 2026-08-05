#!/usr/bin/env python3
"""Detecta enlaces internos rotos en los `.md` del repositorio."""

import logging
import os
import pathlib
import sys

from src.comite_lds import link_checker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Revisa los enlaces internos del repo y reporta los rotos.

    Returns:
        Código de salida: 0 si no hay enlaces rotos, 1 en caso contrario.
    """
    repo_root = pathlib.Path(os.environ["PROJECT_ROOT"])
    broken_links = link_checker.check_all_links(repo_root)

    if not broken_links:
        logger.info("No se encontraron enlaces internos rotos.")
        return 0

    for broken in broken_links:
        logger.error(
            "%s:%d - [%s](%s) - %s",
            broken.origin,
            broken.line,
            broken.text,
            broken.target,
            broken.reason,
        )
    logger.error("%d enlace(s) roto(s) encontrado(s).", len(broken_links))
    return 1


if __name__ == "__main__":
    sys.exit(main())
