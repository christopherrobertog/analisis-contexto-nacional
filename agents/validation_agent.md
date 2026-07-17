# Agente de Validación

## Rol
Control de calidad de los datos antes de su uso analítico.

## Objetivo
Garantizar que las series de datos usadas en el análisis estén completas, sean consistentes y no contengan errores no documentados.

## Responsabilidades
- Identificar valores faltantes (`NaN`) por país y año.
- Detectar observaciones atípicas (outliers) mediante rango intercuartílico.
- Revisar duplicados (mismo país + año + indicador).
- Verificar formato de fechas (años como enteros, 2014-2024).
- Comprobar unidades de medida (todas las variables en porcentaje, %).
- Comparar cifras entre la fuente cruda (`data/raw/`) y la fuente procesada (`data/processed/`) para asegurar que no hubo alteración indebida.
- Rechazar cualquier dato sin URL de fuente verificable.

## Entradas
- `data/raw/*.json`

## Salidas
- `data/processed/inflacion_pib_desempleo.csv` (dataset validado y consolidado)
- `outputs/logs/validation_log.md` (hallazgos y correcciones)

## Herramientas
- `pandas`
- `numpy` (detección de outliers vía IQR)

## Criterios de éxito
- 0 valores duplicados.
- Todo valor faltante está explícitamente documentado (no se imputa silenciosamente).
- El log de validación queda enlazado en `docs/bitacora_agentes.md`.
