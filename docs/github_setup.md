# Guía: Publicar el repositorio en GitHub

Estos pasos deben ejecutarse manualmente desde tu cuenta de GitHub (requieren tus propias credenciales; no pueden automatizarse por ti).

## 1. Crear el repositorio

1. Entra a https://github.com/new
2. Nombre sugerido: `analisis-inflacion-ecuador` (relacionado con el tema, según el requisito de la orden de tarea).
3. Visibilidad: **Público** (salvo indicación distinta del docente).
4. **No** marques "Initialize with README" (el proyecto ya tiene uno).
5. Crea el repositorio.

## 2. Conectar el repositorio local

Desde la carpeta `analisis-contexto-nacional-global/` en VS Code (terminal integrada):

```bash
git init
git add README.md LICENSE .gitignore .env.example package.json requirements.txt vercel.json docs agents subagents prompts config data scripts tests
git commit -m "docs: estructura inicial del proyecto y arquitectura multiagentica"

git branch -M main
git remote add origin https://github.com/<tu-usuario>/analisis-inflacion-ecuador.git
git push -u origin main
```

> Nota: se listan las carpetas explícitamente en el primer `git add` para evitar
> incluir accidentalmente `dashboard/node_modules` u otros artefactos pesados
> antes de que `.gitignore` esté verificado. En los commits siguientes puedes
> usar `git add <archivo>` o `git add -A` con confianza, ya que `.gitignore`
> ya excluye `node_modules/`, `.venv/`, `.next/`, etc.

## 3. Commits frecuentes y descriptivos

Sigue el patrón de la orden de tarea (ver también `README.md`):

```
feat: agregar agente de validacion de datos
data: incorporar indicadores del Banco Mundial
fix: corregir calculo de tasa de crecimiento
docs: actualizar metodologia del proyecto
dashboard: agregar filtro por pais
report: incorporar conclusiones del analisis
```

Evita un único commit masivo al final: el docente revisará el historial de
commits como evidencia del proceso de desarrollo, no solo el resultado final.

## 4. Crear una release

Cuando el proyecto esté funcional (dashboard desplegado, informe generado):

```bash
git tag -a v1.0.0 -m "Version estable: dashboard desplegado e informe final generado"
git push origin v1.0.0
```

Luego, en GitHub → Releases → "Draft a new release", selecciona el tag `v1.0.0` y publica.

## 5. Checklist antes de hacer push

- [ ] `.env` real (si existe) **no** está incluido — solo `.env.example`.
- [ ] `dashboard/node_modules/` no está incluido (verificar con `git status`).
- [ ] `.venv/` no está incluido.
- [ ] No hay claves ni tokens en ningún archivo (`git grep -i "api_key\|secret\|password"` antes de cada push).
- [ ] El README refleja el estado real del proyecto (enlaces al dashboard y al PDF).
