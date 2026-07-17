# Metodología

## Enfoque
Estudio comparativo cuantitativo de la inflación de Ecuador (2014-2024) frente a Estados Unidos, Perú, Panamá y la región de América Latina y el Caribe (excl. altos ingresos), complementado con crecimiento del PIB y desempleo para explorar relaciones macroeconómicas.

## Periodo de análisis
2014-2024 (11 observaciones anuales por país e indicador), cumpliendo el requisito de un mínimo de diez años de la orden de tarea. Se usa periodicidad **anual** por ser la granularidad disponible de forma confiable y programática en la fuente primaria (Banco Mundial); ver limitación sobre series mensuales en `README.md`.

## Selección de países
- **Ecuador:** objeto de estudio.
- **Estados Unidos:** economía ancla de la dolarización ecuatoriana desde 2000; su inflación se transmite parcialmente a Ecuador vía bienes transables.
- **Perú:** economía regional comparable en tamaño relativo, pero con política monetaria propia (metas de inflación), lo que permite contrastar el efecto de la dolarización.
- **Panamá:** economía latinoamericana también dolarizada, control comparativo directo del "efecto dolarización" sin el "efecto tamaño de EE.UU.".
- **América Latina y el Caribe (excl. altos ingresos):** referencia regional agregada.

## Fuentes y trazabilidad
Ver `docs/fuentes.md` y `config/sources.yaml`. Cada dato es trazable hasta el archivo JSON crudo en `data/raw/` descargado directamente de la API del Banco Mundial el 2026-07-16.

## Proceso (fases)
1. **Planificación:** selección del tema, países e indicadores (este documento).
2. **Recopilación:** descarga automatizada vía API (`scripts/download_data.py`).
3. **Procesamiento:** limpieza, homologación y validación (`scripts/clean_data.py`, `scripts/validate_data.py`).
4. **Análisis:** cálculo de indicadores comparativos (`scripts/calculate_indicators.py`) y análisis econométrico (`scripts/econometric_model.py`).
5. **Visualización:** dashboard interactivo (`dashboard/`).
6. **Informe:** documento académico en PDF (`scripts/generate_report.py`).
7. **Auditoría y despliegue:** revisión final y publicación en Vercel/GitHub.

## Técnicas estadísticas aplicadas
- Estadística descriptiva (media, mediana, desviación estándar, coeficiente de variación).
- Números índice (base 2014 = 100).
- Tasas de variación interanual.
- Correlación de Pearson (inflación-PIB, inflación-desempleo).
- Regresión lineal simple (inflación Ecuador ~ inflación EE.UU.).
- Comparación de sub-períodos (2014-2019 pre-pandemia vs. 2020-2024 post-pandemia).

## Estructura del informe final
Portada; Resumen ejecutivo; Introducción; Planteamiento del problema; Objetivos; Marco conceptual; Contexto nacional; Contexto global; Fuentes y metodología; Arquitectura multiagéntica; Procesamiento de datos; Análisis estadístico/econométrico; Resultados; Discusión; Riesgos y oportunidades para Ecuador; Conclusiones; Recomendaciones; Limitaciones; Referencias; Anexos.
