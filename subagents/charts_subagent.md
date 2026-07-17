# Subagente de Gráficos

**Agente padre:** `agents/visualization_agent.md`

## Objetivo
Definir la especificación técnica de cada gráfico del dashboard.

## Especificaciones

| Gráfico | Tipo | Variables | Componente |
|---|---|---|---|
| Evolución de la inflación | Línea multi-serie | Inflación % por país, 2014-2024 | `dashboard/components/InflationLineChart` |
| Comparación promedio | Barras | Inflación promedio 2014-2024 por país | `dashboard/components/AverageBarChart` |
| Inflación vs. crecimiento del PIB | Dispersión | Inflación % y PIB % por país-año | `dashboard/components/ScatterChart` |
| Tabla de datos | Tabla filtrable | Todas las variables, filtro por país/año/indicador | `dashboard/components/DataTable` |

## Reglas de diseño
- Ejes siempre comienzan en un valor que no distorsione la magnitud (evitar recortes engañosos en gráficos de barras).
- Colores consistentes por país en todos los gráficos del dashboard.
- Cada gráfico incluye: título, subtítulo con unidad, fuente y fecha de actualización.
