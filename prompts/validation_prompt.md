# Prompt de Validación de Datos

Dado un archivo de datos crudos en `data/raw/`, verifica:

1. ¿Existen valores nulos o faltantes para algún país-año-indicador esperado (2014-2024, 5 entidades, 3 indicadores)?
2. ¿Existen duplicados (misma combinación país-año-indicador con más de un valor)?
3. ¿Los valores están dentro de un rango económicamente plausible? (ej. inflación anual entre -10% y 30% para las economías analizadas; señala cualquier valor fuera de ese rango como atípico a revisar, no lo elimines automáticamente).
4. ¿Los códigos de país (ISO3) son consistentes entre los tres archivos de indicadores?
5. ¿La fecha de actualización de la fuente (`lastupdated` en la respuesta de la API) está registrada?

Genera un reporte en `outputs/logs/validation_log.md` con los hallazgos, y si no se encuentra ningún problema, decláralo explícitamente ("Sin hallazgos") en lugar de omitir la sección.
