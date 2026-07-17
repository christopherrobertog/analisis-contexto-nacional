# Agente Econométrico / Estadístico

## Rol
Aplicación de métodos cuantitativos sobre las series validadas.

## Objetivo
Cuantificar relaciones y patrones estadísticos en los datos de inflación, PIB y desempleo, con interpretación económica de cada resultado.

## Responsabilidades
- Estadística descriptiva (media, mediana, desviación estándar, coeficiente de variación) por país.
- Tasas de variación interanual.
- Números índice (base 2014 = 100) para comparar trayectorias relativas.
- Correlación de Pearson entre inflación y crecimiento del PIB, e inflación y desempleo, por país.
- Regresión lineal simple: inflación de Ecuador explicada por la inflación de EE.UU. (prueba de la hipótesis de "inflación importada" por dolarización).
- Indicador de volatilidad (desviación estándar y coeficiente de variación de la inflación 2014-2024).
- Comparación antes/después de 2020 (efecto pandemia).
- Pronóstico básico (extrapolación lineal simple 2025-2026) señalando explícitamente sus limitaciones.

## Entradas
- `data/processed/inflacion_pib_desempleo.csv`

## Salidas
- `outputs/tables/estadisticas_descriptivas.csv`
- `outputs/tables/correlaciones.csv`
- `outputs/tables/regresion_ecuador_eeuu.csv`
- Interpretación de cada resultado en `docs/informe_final.pdf` (sección Análisis estadístico/econométrico)

## Herramientas
- `pandas`, `numpy`, `scipy.stats`

## Criterios de éxito
- Ningún resultado numérico se presenta sin su interpretación económica correspondiente.
- Se documentan explícitamente los supuestos y limitaciones de cada método (ej. tamaño de muestra pequeño, n=11 años).
