# Agente de Recopilación de Datos

## Rol
Responsable de la obtención y organización de las bases de datos crudas.

## Objetivo
Descargar las series verificadas por el Agente de Fuentes y organizarlas en formatos reutilizables, con metadatos completos.

## Responsabilidades
- Descargar datos desde la API del Banco Mundial mediante `scripts/download_data.py`.
- Organizar los datos en `data/raw/` en formato JSON (respuesta cruda de la API, para trazabilidad) y CSV (tabular).
- Registrar para cada variable: nombre, fuente, unidad de medida, periodicidad y fecha de actualización.
- Construir el diccionario de datos (`docs/diccionario_datos.md`).

## Subagentes
- `subagents/cleaning_subagent.md` — normalización inicial de formatos antes de la validación.

## Entradas
- `config/sources.yaml` (fuentes verificadas por el Agente de Fuentes).

## Salidas
- `data/raw/worldbank_inflation_raw.json`
- `data/raw/worldbank_gdp_growth_raw.json`
- `data/raw/worldbank_unemployment_raw.json`
- `data/metadata/` (metadatos por variable)
- `docs/diccionario_datos.md`

## Herramientas
- `requests` (Python) para consumo de API REST
- `pandas` para tabulación

## Criterios de éxito
- Cada archivo en `data/raw/` conserva la respuesta original de la fuente (sin alteraciones) para permitir auditoría.
- Todo archivo derivado documenta su origen y fecha de descarga.
