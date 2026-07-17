"""Pruebas de los indicadores calculados (Agente de Análisis Económico / Econométrico)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = ROOT / "outputs" / "tables"

REQUIRED_TABLES = [
    "indicadores_comparativos.csv",
    "estadisticas_descriptivas.csv",
    "correlaciones.csv",
    "regresion_ecuador_eeuu.csv",
    "volatilidad_inflacion.csv",
    "comparacion_pre_post_pandemia.csv",
]


@pytest.mark.parametrize("filename", REQUIRED_TABLES)
def test_table_exists(filename: str) -> None:
    path = TABLES_DIR / filename
    assert path.exists(), f"Falta {filename}. Ejecutar scripts/calculate_indicators.py y scripts/econometric_model.py"


def test_inflacion_comparativos_has_all_countries() -> None:
    df = pd.read_csv(TABLES_DIR / "indicadores_comparativos.csv")
    assert len(df) == 5
    assert "inflacion_promedio" in df.columns


def test_regresion_r2_between_0_and_1() -> None:
    df = pd.read_csv(TABLES_DIR / "regresion_ecuador_eeuu.csv")
    r2 = df.iloc[0]["r_cuadrado"]
    assert 0 <= r2 <= 1


def test_volatilidad_no_negative_values() -> None:
    df = pd.read_csv(TABLES_DIR / "volatilidad_inflacion.csv")
    assert (df["volatilidad_desv_estandar"] >= 0).all()
