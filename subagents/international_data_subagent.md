# Subagente de Datos Internacionales

**Agente padre:** `agents/source_agent.md`

## Objetivo
Localizar y descargar series comparables de inflación, PIB y desempleo para las economías de referencia (Estados Unidos, Perú, Panamá, América Latina y el Caribe).

## Fuente utilizada
World Bank Open Data API — indicadores:
- `FP.CPI.TOTL.ZG` (Inflation, consumer prices, annual %)
- `NY.GDP.MKTP.KD.ZG` (GDP growth, annual %)
- `SL.UEM.TOTL.ZS` (Unemployment, % of total labor force)

Endpoint base: `https://api.worldbank.org/v2/country/{codigo_pais}/indicator/{codigo_indicador}?date=2014:2024&format=json`

## Resultado
Ver `data/raw/worldbank_*.json` y el registro completo en `config/sources.yaml`.
