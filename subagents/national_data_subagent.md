# Subagente de Datos Nacionales

**Agente padre:** `agents/source_agent.md`

## Objetivo
Localizar fuentes oficiales ecuatorianas de inflación, PIB y desempleo.

## Fuentes objetivo
- Instituto Nacional de Estadística y Censos (INEC) — Índice de Precios al Consumidor (IPC).
- Banco Central del Ecuador (BCE) — Cifras Económicas, Boletín de Inflación.
- Ministerio de Economía y Finanzas — contexto fiscal.

## Resultado en este proyecto
Estas fuentes se documentan en `docs/fuentes.md` como referencia metodológica y de contraste cualitativo del contexto ecuatoriano. La serie cuantitativa utilizada para Ecuador en el análisis (2014-2024) proviene del Banco Mundial (que a su vez consolida series de INEC/BCE bajo metodología armonizada internacionalmente), lo que permite comparabilidad directa con los demás países del estudio. Ver limitación explícita en `README.md`.
