"""Agente de Recopilación de Datos.

Descarga las series de inflación, crecimiento del PIB y desempleo desde la
API pública del Banco Mundial para Ecuador y las economías de referencia, y
las guarda sin modificar en data/raw/ para garantizar trazabilidad.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"

BASE_URL = "https://api.worldbank.org/v2/country"
COUNTRIES = "ECU;USA;PER;PAN;LAC"
START_YEAR = 2014
END_YEAR = 2024

INDICATORS = {
    "FP.CPI.TOTL.ZG": "worldbank_inflation_raw.json",
    "NY.GDP.MKTP.KD.ZG": "worldbank_gdp_growth_raw.json",
    "SL.UEM.TOTL.ZS": "worldbank_unemployment_raw.json",
}


def download_indicator(indicator_code: str, filename: str) -> None:
    url = (
        f"{BASE_URL}/{COUNTRIES}/indicator/{indicator_code}"
        f"?date={START_YEAR}:{END_YEAR}&format=json&per_page=1000"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2 or not payload[1]:
        raise RuntimeError(f"Respuesta inesperada de la API para {indicator_code}: {payload}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / filename
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {indicator_code} -> {out_path} ({payload[0].get('total', '?')} registros)")


def main() -> int:
    print(f"Descargando datos del Banco Mundial ({date.today().isoformat()})...")
    for code, filename in INDICATORS.items():
        try:
            download_indicator(code, filename)
        except requests.RequestException as exc:
            print(f"[ERROR] No se pudo descargar {code}: {exc}", file=sys.stderr)
            return 1
    print("Descarga completa. Ver data/raw/ y actualizar docs/fuentes.md si cambia la fecha de consulta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
