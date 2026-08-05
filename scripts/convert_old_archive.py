#!/usr/bin/env python3
"""Convierte los documentos de oficina de docs/old a Markdown/texto.

Implementa el paso de conversión del Método A descrito en
docs/dev/analisis-docs-old.md: docx/pptx/pdf/xls -> texto plano, con
respaldo de OCR en español para PDFs que resultan ser escaneos de
imagen. Fotos, video, PSD y páginas web guardadas quedan fuera de
alcance (evidencia secundaria, no fuente primaria de decisiones).

La salida se escribe en data/old_archive/converted/, que está
excluido de git (mismo tratamiento de privacidad que docs/old).
"""

import csv
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(os.environ['PROJECT_ROOT'])
SRC_ROOT = REPO_ROOT / 'docs' / 'old'
OUT_ROOT = REPO_ROOT / 'data' / 'old_archive' / 'converted'
MANIFEST_PATH = REPO_ROOT / 'data' / 'old_archive' / 'manifest.csv'

CONVERTIBLE_EXTENSIONS = {'.docx', '.pptx', '.pdf', '.xls'}
OCR_MIN_CHARS = 200
OCR_LANG = 'spa'


def run(cmd):
    """Ejecuta un comando externo y devuelve (ok, stdout)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, check=False
        )
        if result.returncode != 0:
            logger.warning('%s -> rc=%s: %s', cmd[0], result.returncode,
                            result.stderr.strip()[:300])
            return False, ''
        return True, result.stdout
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.warning('%s -> error: %s', cmd[0], exc)
        return False, ''


def ocr_pdf(pdf_path, tmp_dir):
    """Extrae texto de un PDF escaneado renderizando cada página y
    aplicando tesseract en español."""
    prefix = tmp_dir / 'page'
    ok, _ = run(['pdftoppm', '-r', '200', '-png', str(pdf_path), str(prefix)])
    if not ok:
        return ''
    pages = sorted(tmp_dir.glob('page-*.png'))
    text_parts = []
    for page in pages:
        ok, _ = run(['tesseract', str(page), str(page.with_suffix('')),
                      '-l', OCR_LANG])
        txt_file = page.with_suffix('.txt')
        if ok and txt_file.exists():
            text_parts.append(txt_file.read_text(encoding='utf-8',
                                                   errors='ignore'))
    return '\n\n'.join(text_parts)


def pdf_to_text(pdf_path):
    """Extrae texto de un PDF; recurre a OCR si el texto nativo es
    demasiado escaso (indicio de escaneo de imagen)."""
    ok, text = run(['pdftotext', '-layout', str(pdf_path), '-'])
    text = text if ok else ''
    if len(text.strip()) >= OCR_MIN_CHARS:
        return text, 'pdftotext'
    logger.info('OCR fallback para %s (texto nativo insuficiente)', pdf_path)
    with tempfile.TemporaryDirectory() as tmp:
        ocr_text = ocr_pdf(pdf_path, Path(tmp))
    if len(ocr_text.strip()) > len(text.strip()):
        return ocr_text, 'ocr'
    return text, 'pdftotext'


def convert_docx(src, dst):
    ok, _ = run(['pandoc', str(src), '-o', str(dst), '--wrap=none'])
    return ok, 'pandoc'


def convert_via_pdf(src, dst):
    """Convierte docx/pptx/xls a PDF con LibreOffice y luego extrae
    texto (con respaldo de OCR) desde ese PDF intermedio."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        ok, _ = run(['soffice', '--headless', '--convert-to', 'pdf',
                     '--outdir', str(tmp_dir), str(src)])
        pdf_path = tmp_dir / (src.stem + '.pdf')
        if not ok or not pdf_path.exists():
            return False, 'soffice-failed'
        text, method = pdf_to_text(pdf_path)
    dst.write_text(text, encoding='utf-8')
    return True, method


def convert_xls(src, dst):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        ok, _ = run(['soffice', '--headless', '--convert-to', 'csv',
                     '--outdir', str(tmp_dir), str(src)])
        csv_path = tmp_dir / (src.stem + '.csv')
        if not ok or not csv_path.exists():
            return False, 'soffice-failed'
        shutil.copy(csv_path, dst.with_suffix('.csv'))
    return True, 'soffice-csv'


def convert_one(src):
    """Convierte un archivo fuente; devuelve (status, method, chars)."""
    rel = src.relative_to(SRC_ROOT)
    # Conserva la extensión original en el nombre: dos fuentes con el
    # mismo stem pero distinta extensión (p. ej. "X.docx" y "X.pdf")
    # no deben pisarse al convertir ambas a Markdown.
    dst = OUT_ROOT / rel.parent / (rel.name + '.md')
    dst.parent.mkdir(parents=True, exist_ok=True)

    ext = src.suffix.lower()
    if ext == '.docx':
        ok, method = convert_docx(src, dst)
    elif ext == '.xls':
        ok, method = convert_xls(src, dst)
    elif ext in ('.pptx',):
        ok, method = convert_via_pdf(src, dst)
    elif ext == '.pdf':
        text, method = pdf_to_text(src)
        dst.write_text(text, encoding='utf-8')
        ok = True
    else:
        return 'skipped', 'n/a', 0

    if not ok:
        return 'failed', method, 0
    chars = dst.stat().st_size if dst.exists() else 0
    if method == 'ocr':
        return 'ok-ocr', method, chars
    return 'ok', method, chars


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    sources = [p for p in SRC_ROOT.rglob('*')
               if p.is_file() and p.suffix.lower() in CONVERTIBLE_EXTENSIONS]
    logger.info('%d documentos a convertir', len(sources))

    rows = []
    for i, src in enumerate(sources, 1):
        status, method, chars = convert_one(src)
        logger.info('[%d/%d] %s -> %s (%s, %d chars)',
                     i, len(sources), src.relative_to(SRC_ROOT), status,
                     method, chars)
        rows.append({
            'path': str(src.relative_to(SRC_ROOT)),
            'status': status,
            'method': method,
            'chars': chars,
        })

    with open(MANIFEST_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'status', 'method',
                                                'chars'])
        writer.writeheader()
        writer.writerows(rows)
    logger.info('Manifest escrito en %s', MANIFEST_PATH)


if __name__ == '__main__':
    main()
