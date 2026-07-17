# Análisis del Contexto Nacional y Global: Inflación en Ecuador y su Entorno Internacional

Proyecto multiagéntico para el análisis del contexto económico nacional y global — Asignatura *Análisis del Contexto Nacional y Global*, Economía, Octavo Semestre.

## Integrantes

> Trabajo elaborado de forma individual (ajustar esta sección con los nombres reales del grupo antes de la entrega).

- [Nombre Apellido] — rol: coordinación, análisis y desarrollo integral del proyecto.

## Problema analizado

La inflación es uno de los indicadores más sensibles para evaluar la estabilidad macroeconómica de un país. Ecuador, al ser una economía **dolarizada desde el año 2000**, no controla su política monetaria y por lo tanto su inflación depende en gran medida de factores externos (precios internacionales, inflación importada desde Estados Unidos, choques de oferta regionales) y de la disciplina fiscal interna.

Este proyecto analiza la **evolución de la inflación en Ecuador (2014-2024)** en comparación con:

- **Estados Unidos** — economía ancla de la dolarización ecuatoriana.
- **Perú** — economía de la región con esquema de metas de inflación (moneda propia).
- **Panamá** — economía latinoamericana también dolarizada, comparable en régimen monetario.
- **América Latina y el Caribe (excl. altos ingresos)** — referencia regional agregada.

Se complementa con **crecimiento del PIB** y **tasa de desempleo** de las mismas economías para explorar relaciones entre inflación, actividad económica y mercado laboral.

## Objetivos

**Objetivo general:** Analizar el comportamiento de la inflación en Ecuador entre 2014 y 2024 en el contexto internacional, identificando riesgos y oportunidades derivados de su condición de economía dolarizada.

**Objetivos específicos:**
1. Recopilar y validar series de inflación, crecimiento del PIB y desempleo de fuentes oficiales (Banco Mundial) para Ecuador y economías de referencia.
2. Calcular indicadores descriptivos, tasas de variación y medidas de volatilidad de la inflación.
3. Analizar la correlación entre inflación, crecimiento económico y desempleo.
4. Visualizar los resultados en un dashboard interactivo público.
5. Elaborar un informe académico en PDF con interpretación económica de los resultados.

## Arquitectura multiagéntica

El proyecto se organiza mediante un **agente coordinador** y **8 agentes especializados** (más 6 subagentes), documentados en [`agents/`](agents/) y [`subagents/`](subagents/), con su configuración en [`config/agents.yaml`](config/agents.yaml) y el flujo de tareas en [`config/tasks.yaml`](config/tasks.yaml). El detalle completo está en [`docs/arquitectura_multiagente.md`](docs/arquitectura_multiagente.md).

| Agente | Responsabilidad |
|---|---|
| Coordinador | Distribuye tareas, integra resultados, gestiona consistencia |
| Fuentes | Localiza fuentes oficiales (Banco Mundial, BCE, INEC, FMI) |
| Recopilación de datos | Descarga y organiza datos crudos con metadatos |
| Validación | Revisa faltantes, duplicados, atípicos, consistencia |
| Análisis económico | Calcula indicadores y compara países |
| Econométrico/Estadístico | Estadística descriptiva, correlación, regresión, series de tiempo |
| Visualización | Diseña gráficos y tablas para el dashboard |
| Redactor | Elabora el informe final en PDF |
| Auditor | Revisa trazabilidad, coherencia y estructura del repositorio |

## Fuentes de datos

Todas las fuentes están registradas en [`config/sources.yaml`](config/sources.yaml) y [`docs/fuentes.md`](docs/fuentes.md). Fuente primaria: **World Bank Open Data API** (indicadores `FP.CPI.TOTL.ZG`, `NY.GDP.MKTP.KD.ZG`, `SL.UEM.TOTL.ZS`), consultada el 2026-07-16.

## Tecnologías utilizadas

- **Datos y análisis:** Python (pandas, requests, fpdf2)
- **Dashboard:** Next.js 14 (React), Recharts, desplegado en Vercel
- **Control de versiones:** Git + GitHub
- **Generación de informe:** Python (reproducible desde `scripts/generate_report.py`)

## Instrucciones de instalación

```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd analisis-contexto-nacional-global

# Backend / scripts de datos (Python)
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Dashboard (Next.js)
cd dashboard
npm install
```

## Instrucciones de ejecución

```bash
# 1. Descargar / actualizar datos crudos
python scripts/download_data.py

# 2. Limpiar y validar
python scripts/clean_data.py
python scripts/validate_data.py

# 3. Calcular indicadores y modelos
python scripts/calculate_indicators.py
python scripts/econometric_model.py

# 4. Generar el informe en PDF
python scripts/generate_report.py

# 5. Ejecutar el dashboard en local
cd dashboard
npm run dev
# abrir http://localhost:3000
```

## Enlaces

- **Dashboard (Vercel):** [pendiente de despliegue — ver `docs/despliegue_vercel.md`]
- **Informe PDF:** [`docs/informe_final.pdf`](docs/informe_final.pdf)
- **Repositorio GitHub:** [pendiente de publicación]

## Resultados principales

- Las dos economías dolarizadas de la muestra —**Panamá (0.90% promedio anual)** y **Ecuador (1.52%)**— registraron la inflación más baja y menor dispersión del grupo 2014-2024, frente a Estados Unidos (2.76%), Perú (3.65%) y el promedio de América Latina y el Caribe (3.93%).
- Perú y la región LAC mostraron mayor volatilidad y picos inflacionarios más altos en 2022 (post-pandemia / choque de oferta global, hasta 8.33% en Perú).
- El pico de inflación de Ecuador en el período (3.47% en 2022) coincide con el repunte generalizado observado en EE.UU. (8.0%) y a nivel regional, consistente con el mecanismo de inflación importada.
- Una regresión lineal simple entre la inflación de Ecuador y la de EE.UU. (2014-2024) arroja un R² de apenas 0.017 (no significativo con n=11), es decir, **la evidencia de este período no respalda una transmisión lineal fuerte y directa** entre ambas series pese a compartir la misma moneda — un hallazgo que matiza la hipótesis simple de "inflación importada" y amerita un modelo con más observaciones/rezagos.

*(Ver interpretación completa en el dashboard y en el informe PDF.)*

## Limitaciones del análisis

- Se utilizan series **anuales** del Banco Mundial; no se incorporan series mensuales oficiales de INEC/BCE por restricciones de acceso automatizado a esas fuentes dentro del alcance de esta entrega.
- El período 2014-2024 puede no capturar completamente ciclos económicos de mayor duración.
- La relación entre inflación, crecimiento y desempleo se explora mediante correlación y regresión simple; no se controla por variables omitidas (precio del petróleo, remesas, gasto público).
- Este es un trabajo de alcance individual adaptado del formato grupal original; el historial de commits refleja un único autor.

## Licencia

Código bajo licencia MIT — ver [`LICENSE`](LICENSE). Los datos provienen del Banco Mundial (Creative Commons Attribution 4.0 International — CC BY 4.0).
