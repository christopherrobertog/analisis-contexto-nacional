# Diccionario de Datos

## Dataset: `data/processed/inflacion_pib_desempleo.csv`

| Campo | Tipo | Descripción | Valores posibles |
|---|---|---|---|
| `pais` | texto | Nombre del país o región | Ecuador, Estados Unidos, Perú, Panamá, América Latina y el Caribe |
| `codigo_iso3` | texto | Código ISO 3166-1 alpha-3 | ECU, USA, PER, PAN, LAC |
| `indicador` | texto | Variable económica medida | `inflacion_precios_consumidor`, `crecimiento_pib`, `tasa_desempleo` |
| `anio` | entero | Año de la observación | 2014-2024 |
| `valor` | decimal | Valor del indicador en el año/país correspondiente | Ver unidad por indicador abajo |

## Variables

| Variable (`indicador`) | Nombre completo | Fuente | Unidad | Periodicidad | Fecha de actualización |
|---|---|---|---|---|---|
| `inflacion_precios_consumidor` | Inflation, consumer prices (annual %) | World Bank — `FP.CPI.TOTL.ZG` | % anual | Anual | 2026-07-13 (según API) |
| `crecimiento_pib` | GDP growth (annual %) | World Bank — `NY.GDP.MKTP.KD.ZG` | % anual | Anual | 2026-07-13 (según API) |
| `tasa_desempleo` | Unemployment, total (% of total labor force) | World Bank — `SL.UEM.TOTL.ZS` (estimación modelada OIT) | % de la fuerza laboral | Anual | 2026-07-13 (según API) |

## Tablas derivadas (`outputs/tables/`)

| Archivo | Generado por | Contenido |
|---|---|---|
| `indicadores_comparativos.csv` | `scripts/calculate_indicators.py` | Estadística descriptiva de inflación por país |
| `numeros_indice_inflacion.csv` | `scripts/calculate_indicators.py` | Número índice acumulado de inflación, base 2014=100 |
| `comparacion_pre_post_pandemia.csv` | `scripts/calculate_indicators.py` | Inflación promedio 2014-2019 vs. 2020-2024 |
| `estadisticas_descriptivas.csv` | `scripts/econometric_model.py` | Media, mediana, desviación estándar por país e indicador |
| `correlaciones.csv` | `scripts/econometric_model.py` | Correlación de Pearson inflación-PIB e inflación-desempleo |
| `regresion_ecuador_eeuu.csv` | `scripts/econometric_model.py` | Regresión lineal simple inflación Ecuador ~ inflación EE.UU. |
| `volatilidad_inflacion.csv` | `scripts/econometric_model.py` | Desviación estándar y coeficiente de variación de la inflación |

## Notas de calidad de datos

Ver `outputs/logs/validation_log.md` (generado por `scripts/validate_data.py`) para el detalle de valores faltantes, duplicados y atípicos detectados en cada ejecución del pipeline.
