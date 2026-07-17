"""Agente de Visualización (puente de datos).

Exporta el dataset procesado y las tablas generadas por los agentes de
análisis económico y econométrico a JSON, para que el dashboard de Next.js
consuma exactamente los mismos números que el informe en PDF (fuente única
de verdad: data/processed/ y outputs/tables/).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"
TABLES_DIR = ROOT / "outputs" / "tables"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"


def df_to_json(df: pd.DataFrame, path: Path) -> None:
    path.write_text(df.to_json(orient="records", indent=2, force_ascii=False), encoding="utf-8")
    print(f"[OK] {path.relative_to(ROOT)} ({len(df)} filas)")


def main() -> int:
    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

    dataset = pd.read_csv(PROCESSED_PATH)
    df_to_json(dataset, DASHBOARD_DATA_DIR / "dataset.json")

    df_to_json(pd.read_csv(TABLES_DIR / "indicadores_comparativos.csv"), DASHBOARD_DATA_DIR / "indicadores_comparativos.json")
    df_to_json(pd.read_csv(TABLES_DIR / "comparacion_pre_post_pandemia.csv"), DASHBOARD_DATA_DIR / "comparacion_pre_post_pandemia.json")
    df_to_json(pd.read_csv(TABLES_DIR / "volatilidad_inflacion.csv"), DASHBOARD_DATA_DIR / "volatilidad_inflacion.json")
    df_to_json(pd.read_csv(TABLES_DIR / "estadisticas_descriptivas.csv"), DASHBOARD_DATA_DIR / "estadisticas_descriptivas.json")
    df_to_json(pd.read_csv(TABLES_DIR / "correlaciones.csv"), DASHBOARD_DATA_DIR / "correlaciones.json")

    regresion_df = pd.read_csv(TABLES_DIR / "regresion_ecuador_eeuu.csv")
    (DASHBOARD_DATA_DIR / "regresion_ecuador_eeuu.json").write_text(
        regresion_df.iloc[0].to_json(force_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[OK] dashboard/data/regresion_ecuador_eeuu.json")

    # Scatter data: inflación vs PIB por país-año
    inflacion = dataset[dataset["indicador"] == "inflacion_precios_consumidor"][["pais", "anio", "valor"]].rename(columns={"valor": "inflacion"})
    pib = dataset[dataset["indicador"] == "crecimiento_pib"][["pais", "anio", "valor"]].rename(columns={"valor": "pib"})
    scatter = inflacion.merge(pib, on=["pais", "anio"])
    df_to_json(scatter, DASHBOARD_DATA_DIR / "scatter_inflacion_pib.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
