# Prompt del Agente Redactor

Redacta la sección [X] del informe final siguiendo la estructura de `docs/metodologia.md`, con estas reglas:

1. Usa exclusivamente las cifras presentes en `outputs/tables/`. No redondees de forma que cambie la interpretación (ej. no reportar "0% de inflación" cuando el dato es "0.42%").
2. Cada afirmación cuantitativa debe poder verificarse en los datos procesados.
3. Cita las fuentes usando el formato de `subagents/references_subagent.md`.
4. Mantén un tono académico, en español formal, evitando adjetivos no sustentados ("catastrófico", "excelente") a menos que estén directamente respaldados por el análisis comparativo.
5. Al final de cada sección analítica, incluye un párrafo de interpretación económica que conecte el hallazgo con el marco conceptual de dolarización e inflación importada.
