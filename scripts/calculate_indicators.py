"""Agente de Análisis Económico.

Calcula indicadores comparativos (estadística descriptiva básica, números
índice, tasas de variación) a partir del dataset validado.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"
OUTPUT_DIR = ROOT / "outputs" / "tables"


def build_comparative_indicators(df: pd.DataFrame) -> pd.DataFrame:
    inflacion = df[df["indicador"] == "inflacion_precios_consumidor"]
    summary = (
        inflacion.groupby("pais")["valor"]
        .agg(inflacion_promedio="mean", inflacion_mediana="median", inflacion_min="min", inflacion_max="max", desviacion_estandar="std")
        .round(2)
        .reset_index()
    )
    summary["coeficiente_variacion_pct"] = (
        (summary["desviacion_estandar"] / summary["inflacion_promedio"].abs()) * 100
    ).round(1)
    return summary.sort_values("inflacion_promedio")


def build_index_numbers(df: pd.DataFrame, indicador: str, base_year: int = 2014) -> pd.DataFrame:
    """Números índice (base_year = 100) usando el valor observado como nivel acumulado aproximado.

    Nota metodológica: dado que la variable original ya es una tasa de variación (%),
    el número índice se construye acumulando (1 + tasa/100) año a año desde el año base,
    para representar el crecimiento acumulado del nivel de precios/PIB.
    """
    subset = df[df["indicador"] == indicador].copy()
    rows = []
    for pais, group in subset.groupby("pais"):
        group = group.sort_values("anio")
        index_value = 100.0
        for _, row in group.iterrows():
            if row["anio"] > base_year:
                index_value *= 1 + (row["valor"] / 100)
            rows.append({"pais": pais, "anio": row["anio"], "indicador": indicador, "numero_indice": round(index_value, 2)})
    return pd.DataFrame(rows)


def build_pre_post_pandemic_comparison(df: pd.DataFrame) -> pd.DataFrame:
    inflacion = df[df["indicador"] == "inflacion_precios_consumidor"].copy()
    inflacion["periodo"] = inflacion["anio"].apply(lambda y: "2014-2019 (pre-pandemia)" if y <= 2019 else "2020-2024 (post-pandemia)")
    comparison = inflacion.groupby(["pais", "periodo"])["valor"].mean().round(2).reset_index()
    return comparison.pivot(index="pais", columns="periodo", values="valor").reset_index()


def main() -> int:
    df = pd.read_csv(INPUT_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    comparativos = build_comparative_indicators(df)
    comparativos.to_csv(OUTPUT_DIR / "indicadores_comparativos.csv", index=False, encoding="utf-8")
    print("[OK] indicadores_comparativos.csv")
    print(comparativos.to_string(index=False))

    indice_inflacion = build_index_numbers(df, "inflacion_precios_consumidor")
    indice_inflacion.to_csv(OUTPUT_DIR / "numeros_indice_inflacion.csv", index=False, encoding="utf-8")
    print("[OK] numeros_indice_inflacion.csv")

    pre_post = build_pre_post_pandemic_comparison(df)
    pre_post.to_csv(OUTPUT_DIR / "comparacion_pre_post_pandemia.csv", index=False, encoding="utf-8")
    print("[OK] comparacion_pre_post_pandemia.csv")
    print(pre_post.to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
