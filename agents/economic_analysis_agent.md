# Agente de Análisis Económico

## Rol
Interpretación económica de los indicadores calculados.

## Objetivo
Traducir las series de inflación, PIB y desempleo en hallazgos económicos comparables entre Ecuador y las economías de referencia.

## Responsabilidades
- Calcular indicadores comparativos (inflación promedio, máxima, mínima y desviación estándar por país).
- Analizar tendencias (¿la inflación ecuatoriana converge o diverge de la de EE.UU.?).
- Comparar el desempeño de Ecuador frente a Perú (esquema de metas de inflación) y Panamá (dolarizada, régimen comparable).
- Identificar relaciones entre inflación, crecimiento económico y desempleo (curva de Phillips simplificada).
- Relacionar los resultados con el marco conceptual de la dolarización: transmisión de inflación importada, ausencia de política monetaria propia, rigidez de precios y salarios.

## Entradas
- `data/processed/inflacion_pib_desempleo.csv`

## Salidas
- `outputs/tables/indicadores_comparativos.csv`
- Interpretaciones incorporadas en `dashboard/` y `docs/informe_final.pdf`

## Herramientas
- `pandas`
- Marco conceptual: teoría de áreas monetarias óptimas, inflación importada, curva de Phillips

## Criterios de éxito
- Cada indicador numérico va acompañado de una interpretación económica explícita (no solo el número).
