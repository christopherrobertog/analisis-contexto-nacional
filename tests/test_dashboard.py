"""Pruebas de integridad de los datos que consume el dashboard (Agente Auditor).

No ejecuta Next.js (para eso ver dashboard/README y `npm run build`); valida que
los archivos JSON que el dashboard consume existan, tengan el esquema esperado
y sean consistentes con `data/processed/`.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"
PROCESSED_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"

REQUIRED_JSON_FILES = [
    "dataset.json",
    "indicadores_comparativos.json",
    "comparacion_pre_post_pandemia.json",
    "volatilidad_inflacion.json",
    "estadisticas_descriptivas.json",
    "correlaciones.json",
    "regresion_ecuador_eeuu.json",
    "scatter_inflacion_pib.json",
]


@pytest.mark.parametrize("filename", REQUIRED_JSON_FILES)
def test_dashboard_data_file_exists_and_is_valid_json(filename: str) -> None:
    path = DASHBOARD_DATA_DIR / filename
    assert path.exists(), f"Falta {filename} en dashboard/data/. Ver docs/despliegue_vercel.md"
    json.loads(path.read_text(encoding="utf-8"))


def test_dashboard_dataset_row_count_matches_processed() -> None:
    dashboard_data = json.loads((DASHBOARD_DATA_DIR / "dataset.json").read_text(encoding="utf-8"))
    processed = pd.read_csv(PROCESSED_PATH)
    assert len(dashboard_data) == len(processed)


def test_dashboard_essential_files_present() -> None:
    dashboard_dir = ROOT / "dashboard"
    for required in ["package.json", "app/page.tsx", "app/layout.tsx", "lib/data.ts"]:
        assert (dashboard_dir / required).exists(), f"Falta {required} en dashboard/"
