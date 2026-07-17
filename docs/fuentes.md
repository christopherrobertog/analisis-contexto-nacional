# Fuentes de Datos

## Fuente primaria (datos cuantitativos utilizados)

### World Bank Open Data API
- **Institución:** Banco Mundial (World Bank Group)
- **URL base:** https://api.worldbank.org/v2
- **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Fecha de consulta:** 2026-07-16
- **Fecha de última actualización reportada por la API:** 2026-07-13 (campo `lastupdated` de la respuesta JSON)

| Indicador | Código | Variable en el proyecto | Unidad | Archivo crudo |
|---|---|---|---|---|
| Inflation, consumer prices (annual %) | `FP.CPI.TOTL.ZG` | `inflacion_precios_consumidor` | % anual | `data/raw/worldbank_inflation_raw.json` |
| GDP growth (annual %) | `NY.GDP.MKTP.KD.ZG` | `crecimiento_pib` | % anual | `data/raw/worldbank_gdp_growth_raw.json` |
| Unemployment, total (% of total labor force) | `SL.UEM.TOTL.ZS` | `tasa_desempleo` | % de la fuerza laboral | `data/raw/worldbank_unemployment_raw.json` |

**Países/regiones incluidos:** Ecuador (ECU), Estados Unidos (USA), Perú (PER), Panamá (PAN), América Latina y el Caribe excl. altos ingresos (LAC).

**Cobertura temporal:** 2014-2024 (11 años).

**Por qué esta fuente:** el Banco Mundial armoniza metodológicamente las series nacionales de cada país (que a su vez provienen de los institutos de estadística y bancos centrales nacionales, incluyendo INEC y BCE para Ecuador), lo que permite comparabilidad internacional directa — un requisito central de este análisis. Es además accesible de forma programática y reproducible (API REST pública sin necesidad de clave de acceso), lo que garantiza que cualquier persona pueda repetir la descarga y obtener los mismos resultados.

## Fuentes de referencia metodológica y contextual (citadas en el marco conceptual, sección `subagents/literature_subagent.md`)

- **Banco Central del Ecuador (BCE)** — https://www.bce.fin.ec — Cifras económicas, contexto nacional, boletines de inflación mensual.
- **Instituto Nacional de Estadística y Censos (INEC)** — https://www.ecuadorencifras.gob.ec — Índice de Precios al Consumidor.
- **Fondo Monetario Internacional (FMI)** — https://www.imf.org — Perspectivas económicas regionales, contexto de dolarización.
- **CEPAL** — https://www.cepal.org — Panorama económico y social de América Latina y el Caribe.
- **Mundell, R. A. (1961).** A theory of optimum currency areas. *The American Economic Review, 51*(4), 657-665. — Marco teórico de áreas monetarias óptimas.

Estas fuentes no fueron extraídas de forma automatizada para la serie de datos cuantitativa de este proyecto (ver `README.md`, sección Limitaciones); se citan como respaldo metodológico y conceptual, y deben ser revisadas/ampliadas manualmente si el grupo decide profundizar con series mensuales oficiales de Ecuador.

## Registro de verificación de fuentes (Agente de Validación)

| Fuente | Verificada | Fecha | Observación |
|---|---|---|---|
| World Bank API — FP.CPI.TOTL.ZG | ✅ | 2026-07-16 | 55 registros descargados, sin errores HTTP |
| World Bank API — NY.GDP.MKTP.KD.ZG | ✅ | 2026-07-16 | 55 registros descargados, sin errores HTTP |
| World Bank API — SL.UEM.TOTL.ZS | ✅ | 2026-07-16 | 55 registros descargados, sin errores HTTP |
