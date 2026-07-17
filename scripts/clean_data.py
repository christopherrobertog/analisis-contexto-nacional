"""Subagente de Limpieza + Agente de Recopilación de Datos.

Convierte las respuestas JSON crudas de la API del Banco Mundial en un único
DataFrame tabular homogéneo, sin todavía validar calidad (eso corresponde a
validate_data.py).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
INTERIM_PATH = ROOT / "data" / "processed" / "_interim_tabular.csv"

INDICATOR_FILES = {
    "worldbank_inflation_raw.json": "inflacion_precios_consumidor",
    "worldbank_gdp_growth_raw.json": "crecimiento_pib",
    "worldbank_unemployment_raw.json": "tasa_desempleo",
}

COUNTRY_NAME_OVERRIDES = {
    "Latin America & Caribbean (excluding high income)": "América Latina y el Caribe",
    "United States": "Estados Unidos",
    "Peru": "Perú",
    "Panama": "Panamá",
}


def load_indicator_file(filename: str, variable_name: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload[1]

    rows = []
    for rec in records:
        if rec.get("value") is None:
            continue
        country_name = rec["country"]["value"]
        country_name = COUNTRY_NAME_OVERRIDES.get(country_name, country_name)
        rows.append(
            {
                "pais": country_name,
                "codigo_iso3": rec["countryiso3code"],
                "indicador": variable_name,
                "anio": int(rec["date"]),
                "valor": float(rec["value"]),
            }
        )
    return pd.DataFrame(rows)


def main() -> int:
    frames = [load_indicator_file(fname, var) for fname, var in INDICATOR_FILES.items()]
    df = pd.concat(frames, ignore_index=True)
    df = df.sort_values(["indicador", "pais", "anio"]).reset_index(drop=True)

    INTERIM_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(INTERIM_PATH, index=False, encoding="utf-8")
    print(f"[OK] {len(df)} filas escritas en {INTERIM_PATH}")
    print(df["pais"].value_counts())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
