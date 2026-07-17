# Prompt de Análisis Económico y Econométrico

Dado el dataset `data/processed/inflacion_pib_desempleo.csv` (columnas: `pais`, `codigo_iso3`, `indicador`, `anio`, `valor`), realiza lo siguiente:

1. Calcula estadística descriptiva (media, mediana, desviación estándar, mínimo, máximo) de la inflación por país para el período 2014-2024.
2. Calcula la correlación de Pearson entre inflación y crecimiento del PIB, e inflación y desempleo, por país.
3. Estima una regresión lineal simple: inflación de Ecuador (variable dependiente) explicada por la inflación de Estados Unidos (variable independiente). Reporta el coeficiente, el R² y su significancia.
4. Para cada resultado numérico, escribe una interpretación económica de 2-4 líneas que explique qué significa en el contexto de la dolarización ecuatoriana.
5. Señala explícitamente las limitaciones estadísticas (tamaño de muestra pequeño, n=11 observaciones anuales, no se controla por variables omitidas).

No reportes ningún número sin su interpretación correspondiente.
