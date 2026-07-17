"""Agente de Validación.

Revisa el dataset tabular intermedio (generado por clean_data.py) en busca de
valores faltantes, duplicados y atípicos, y produce el dataset final validado
en data/processed/inflacion_pib_desempleo.csv junto con un log de hallazgos.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTERIM_PATH = ROOT / "data" / "processed" / "_interim_tabular.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "inflacion_pib_desempleo.csv"
LOG_PATH = ROOT / "outputs" / "logs" / "validation_log.md"

EXPECTED_COUNTRIES = 5
EXPECTED_YEARS = list(range(2014, 2025))
EXPECTED_INDICATORS = 3

# Rango económicamente plausible para señalar (no eliminar) atípicos.
PLAUSIBLE_RANGES = {
    "inflacion_precios_consumidor": (-10, 30),
    "crecimiento_pib": (-20, 20),
    "tasa_desempleo": (0, 35),
}


def main() -> int:
    df = pd.read_csv(INTERIM_PATH)
    findings: list[str] = []

    # 1. Duplicados
    dup_mask = df.duplicated(subset=["pais", "indicador", "anio"], keep=False)
    n_dup = int(dup_mask.sum())
    if n_dup:
        findings.append(f"- **Duplicados encontrados:** {n_dup} filas (se conservó la primera ocurrencia).")
        df = df.drop_duplicates(subset=["pais", "indicador", "anio"], keep="first")
    else:
        findings.append("- **Duplicados:** ninguno encontrado.")

    # 2. Completitud esperada
    expected_rows = EXPECTED_COUNTRIES * len(EXPECTED_YEARS) * EXPECTED_INDICATORS
    actual_rows = len(df)
    missing = expected_rows - actual_rows
    if missing > 0:
        findings.append(
            f"- **Datos faltantes:** se esperaban {expected_rows} observaciones "
            f"({EXPECTED_COUNTRIES} entidades x {len(EXPECTED_YEARS)} años x {EXPECTED_INDICATORS} indicadores) "
            f"y se obtuvieron {actual_rows} ({missing} faltantes). Ver detalle de combinaciones ausentes abajo."
        )
        full_index = pd.MultiIndex.from_product(
            [df["pais"].unique(), EXPECTED_YEARS, list(PLAUSIBLE_RANGES.keys())],
            names=["pais", "anio", "indicador"],
        )
        present = pd.MultiIndex.from_frame(df[["pais", "anio", "indicador"]])
        missing_combos = full_index.difference(present)
        for combo in missing_combos[:20]:
            findings.append(f"  - Faltante: {combo}")
    else:
        findings.append(f"- **Datos faltantes:** ninguno. {actual_rows}/{expected_rows} observaciones completas.")

    # 3. Atípicos (fuera de rango plausible, se documentan pero no se eliminan)
    outlier_notes = []
    for indicador, (lo, hi) in PLAUSIBLE_RANGES.items():
        subset = df[df["indicador"] == indicador]
        outliers = subset[(subset["valor"] < lo) | (subset["valor"] > hi)]
        for _, row in outliers.iterrows():
            outlier_notes.append(
                f"  - {row['pais']} {row['anio']} ({indicador}): {row['valor']:.2f}% "
                f"(fuera del rango plausible [{lo}, {hi}])"
            )
    if outlier_notes:
        findings.append(f"- **Valores atípicos detectados (revisados, no eliminados):**")
        findings.extend(outlier_notes)
    else:
        findings.append("- **Valores atípicos:** ninguno fuera de los rangos económicamente plausibles definidos.")

    # 4. Consistencia de códigos ISO3
    iso_map = df.groupby("pais")["codigo_iso3"].nunique()
    inconsistent = iso_map[iso_map > 1]
    if len(inconsistent):
        findings.append(f"- **Inconsistencia de código ISO3:** {list(inconsistent.index)}")
    else:
        findings.append("- **Códigos ISO3:** consistentes para todos los países.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_content = "# Log de Validación de Datos\n\n"
    log_content += f"Dataset validado: `{OUTPUT_PATH.relative_to(ROOT)}`\n\n"
    log_content += "\n".join(findings) + "\n"
    LOG_PATH.write_text(log_content, encoding="utf-8")

    print(f"[OK] Dataset validado escrito en {OUTPUT_PATH} ({len(df)} filas)")
    print(f"[OK] Log de validación escrito en {LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
