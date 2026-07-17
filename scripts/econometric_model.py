"""Agente Econométrico / Estadístico.

Aplica estadística descriptiva, correlación y regresión lineal simple sobre
el dataset validado, con foco en la hipótesis de inflación importada por
dolarización (inflación Ecuador ~ inflación EE.UU.).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"
OUTPUT_DIR = ROOT / "outputs" / "tables"


def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (pais, indicador), group in df.groupby(["pais", "indicador"]):
        valores = group["valor"]
        rows.append(
            {
                "pais": pais,
                "indicador": indicador,
                "n": len(valores),
                "media": round(valores.mean(), 2),
                "mediana": round(valores.median(), 2),
                "desviacion_estandar": round(valores.std(), 2),
                "minimo": round(valores.min(), 2),
                "maximo": round(valores.max(), 2),
            }
        )
    return pd.DataFrame(rows).sort_values(["indicador", "pais"])


def correlations(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(index=["pais", "anio"], columns="indicador", values="valor").reset_index()
    rows = []
    for pais, group in pivot.groupby("pais"):
        group = group.dropna()
        if len(group) < 3:
            continue
        r_pib, p_pib = stats.pearsonr(group["inflacion_precios_consumidor"], group["crecimiento_pib"])
        r_des, p_des = stats.pearsonr(group["inflacion_precios_consumidor"], group["tasa_desempleo"])
        rows.append(
            {
                "pais": pais,
                "n_obs": len(group),
                "corr_inflacion_pib": round(r_pib, 3),
                "p_valor_inflacion_pib": round(p_pib, 3),
                "corr_inflacion_desempleo": round(r_des, 3),
                "p_valor_inflacion_desempleo": round(p_des, 3),
            }
        )
    return pd.DataFrame(rows)


def regression_ecuador_vs_usa(df: pd.DataFrame) -> pd.DataFrame:
    inflacion = df[df["indicador"] == "inflacion_precios_consumidor"]
    ecuador = inflacion[inflacion["pais"] == "Ecuador"].set_index("anio")["valor"]
    eeuu = inflacion[inflacion["pais"] == "Estados Unidos"].set_index("anio")["valor"]
    merged = pd.concat([ecuador.rename("ecuador"), eeuu.rename("eeuu")], axis=1).dropna()

    slope, intercept, r_value, p_value, std_err = stats.linregress(merged["eeuu"], merged["ecuador"])

    return pd.DataFrame(
        [
            {
                "modelo": "inflacion_ecuador ~ inflacion_eeuu",
                "n_obs": len(merged),
                "pendiente_beta": round(slope, 3),
                "intercepto": round(intercept, 3),
                "r_cuadrado": round(r_value**2, 3),
                "p_valor": round(p_value, 4),
                "error_estandar": round(std_err, 3),
            }
        ]
    )


def volatility(df: pd.DataFrame) -> pd.DataFrame:
    inflacion = df[df["indicador"] == "inflacion_precios_consumidor"]
    rows = []
    for pais, group in inflacion.groupby("pais"):
        std = group["valor"].std()
        mean = group["valor"].mean()
        cv = (std / abs(mean)) * 100 if mean != 0 else np.nan
        rows.append({"pais": pais, "volatilidad_desv_estandar": round(std, 2), "coef_variacion_pct": round(cv, 1)})
    return pd.DataFrame(rows).sort_values("volatilidad_desv_estandar")


def main() -> int:
    df = pd.read_csv(INPUT_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    desc = descriptive_stats(df)
    desc.to_csv(OUTPUT_DIR / "estadisticas_descriptivas.csv", index=False, encoding="utf-8")
    print("[OK] estadisticas_descriptivas.csv")

    corr = correlations(df)
    corr.to_csv(OUTPUT_DIR / "correlaciones.csv", index=False, encoding="utf-8")
    print("[OK] correlaciones.csv")
    print(corr.to_string(index=False))

    reg = regression_ecuador_vs_usa(df)
    reg.to_csv(OUTPUT_DIR / "regresion_ecuador_eeuu.csv", index=False, encoding="utf-8")
    print("[OK] regresion_ecuador_eeuu.csv")
    print(reg.to_string(index=False))

    vol = volatility(df)
    vol.to_csv(OUTPUT_DIR / "volatilidad_inflacion.csv", index=False, encoding="utf-8")
    print("[OK] volatilidad_inflacion.csv")
    print(vol.to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
