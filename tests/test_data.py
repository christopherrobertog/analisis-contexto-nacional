"""Pruebas del pipeline de datos (Agente de Validación / Agente Auditor)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"

RAW_FILES = [
    "worldbank_inflation_raw.json",
    "worldbank_gdp_growth_raw.json",
    "worldbank_unemployment_raw.json",
]


@pytest.mark.parametrize("filename", RAW_FILES)
def test_raw_file_exists_and_is_valid_json(filename: str) -> None:
    path = RAW_DIR / filename
    assert path.exists(), f"Falta el archivo crudo {filename}. Ejecutar scripts/download_data.py"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, list) and len(payload) == 2
    assert payload[1], "La respuesta de la API no contiene registros"


def test_processed_dataset_exists() -> None:
    assert PROCESSED_PATH.exists(), "Falta data/processed/inflacion_pib_desempleo.csv. Ejecutar el pipeline completo."


def test_processed_dataset_has_expected_columns() -> None:
    df = pd.read_csv(PROCESSED_PATH)
    expected_cols = {"pais", "codigo_iso3", "indicador", "anio", "valor"}
    assert expected_cols.issubset(set(df.columns))


def test_processed_dataset_has_no_duplicates() -> None:
    df = pd.read_csv(PROCESSED_PATH)
    dup = df.duplicated(subset=["pais", "indicador", "anio"])
    assert not dup.any(), f"Se encontraron {dup.sum()} filas duplicadas en el dataset procesado"


def test_processed_dataset_covers_expected_countries() -> None:
    df = pd.read_csv(PROCESSED_PATH)
    expected = {"Ecuador", "Estados Unidos", "Perú", "Panamá", "América Latina y el Caribe"}
    assert expected.issubset(set(df["pais"].unique()))


def test_processed_dataset_covers_expected_period() -> None:
    df = pd.read_csv(PROCESSED_PATH)
    assert df["anio"].min() <= 2015
    assert df["anio"].max() >= 2023
