"""Agente Redactor (apoyo).

Combina la presentacion breve y el informe final en un unico PDF, para
plataformas de entrega que solo aceptan un archivo (docs/entrega_final.pdf).
Reproducible: requiere pypdf (pip).
"""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PRESENTATION = DOCS / "presentacion_resultados.pdf"
REPORT = DOCS / "informe_final.pdf"
OUTPUT_PATH = DOCS / "entrega_final.pdf"


def merge() -> None:
    writer = PdfWriter()
    for path in (PRESENTATION, REPORT):
        writer.append(str(path))
    with open(OUTPUT_PATH, "wb") as f:
        writer.write(f)
    print(f"[OK] Entrega combinada generada en {OUTPUT_PATH} ({len(writer.pages)} paginas)")


if __name__ == "__main__":
    merge()
