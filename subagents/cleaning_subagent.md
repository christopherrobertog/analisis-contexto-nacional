# Subagente de Limpieza

**Agente padre:** `agents/data_agent.md`

## Objetivo
Normalizar el formato de los datos crudos antes de la validación formal.

## Tareas
- Convertir la respuesta JSON de la API del Banco Mundial en un DataFrame tabular (`país`, `código_iso3`, `indicador`, `año`, `valor`).
- Homologar nombres de país entre los tres archivos de indicadores (inflación, PIB, desempleo).
- Ordenar cronológicamente cada serie.
- Eliminar metadatos de paginación de la API que no forman parte de los datos.

## Salida
DataFrame intermedio consumido por `scripts/clean_data.py` y `scripts/validate_data.py`.
