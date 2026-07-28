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
REPORT = DOCS / "informe_final.pdf"


def merge(quien: str = "christopher") -> None:
    presentation = DOCS / (
        "presentacion_resultados.pdf" if quien == "christopher" else f"presentacion_resultados_{quien}.pdf"
    )
    output_path = DOCS / (
        "entrega_final.pdf" if quien == "christopher" else f"entrega_final_{quien}.pdf"
    )
    writer = PdfWriter()
    for path in (presentation, REPORT):
        writer.append(str(path))
    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"[OK] Entrega combinada generada en {output_path} ({len(writer.pages)} paginas)")


if __name__ == "__main__":
    import sys

    merge(quien=sys.argv[1] if len(sys.argv) > 1 else "christopher")
