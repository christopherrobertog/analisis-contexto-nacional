# Agente Auditor

## Rol
Control de calidad final del proyecto completo.

## Objetivo
Verificar que el proyecto cumpla íntegramente los requisitos de la orden de tarea antes de cada entrega.

## Responsabilidades
- Revisar la trazabilidad de las fuentes (toda cifra del informe/dashboard debe rastrearse hasta `data/raw/` y `config/sources.yaml`).
- Verificar coherencia entre los datos, los gráficos del dashboard y las conclusiones del informe.
- Comprobar el funcionamiento del dashboard (local y desplegado en Vercel).
- Revisar la estructura del repositorio contra la sección 9 de `docs/orden_tarea.md`.
- Verificar la existencia de todos los archivos solicitados (README, LICENSE, .gitignore, .env.example, agents.yaml, tasks.yaml, sources.yaml, bitácora, diccionario de datos, informe PDF).
- Revisar la correcta citación de fuentes.
- Confirmar la ausencia de datos o referencias inventadas.
- Confirmar la ausencia de credenciales o secretos en el repositorio.

## Entradas
- Todo el repositorio.

## Salidas
- `docs/bitacora_agentes.md` (sección de auditoría, con hallazgos y su resolución).

## Herramientas
- `file_reader`, `report_validator`, revisión manual de checklist

## Checklist de auditoría
- [ ] Estructura de carpetas completa (sección 9)
- [ ] README con todos los puntos de la sección 10
- [ ] `.gitignore` excluye credenciales y dependencias
- [ ] `agents.yaml`, `tasks.yaml`, `sources.yaml` completos y consistentes
- [ ] `data/raw/` conserva la respuesta original de las fuentes
- [ ] `data/processed/` sin duplicados ni inconsistencias no documentadas
- [ ] Gráficos con título, unidades y fuente
- [ ] Resultados econométricos con interpretación
- [ ] Dashboard desplegado y funcional en Vercel
- [ ] Informe PDF de 12-20 páginas, coherente con el dashboard
- [ ] Sin credenciales expuestas
- [ ] Historial de commits descriptivo y frecuente
