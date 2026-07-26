# Guía: Desplegar el Dashboard en Vercel

Estos pasos requieren tu propia cuenta de Vercel (gratuita) conectada a GitHub; no pueden automatizarse por mí.

## 1. Requisito previo

El repositorio debe estar publicado en GitHub (ver `docs/github_setup.md`) y `dashboard/` debe compilar localmente sin errores:

```bash
cd dashboard
npm install
npm run build
```

Si `npm run build` falla, corrige los errores antes de continuar — Vercel ejecutará el mismo build.

## 2. Conectar el repositorio a Vercel

1. Entra a https://vercel.com y accede con tu cuenta de GitHub.
2. "Add New..." → "Project".
3. Selecciona el repositorio `analisis-contexto-nacional`.
4. En **"Configure Project"**:
   - **Root Directory:** `dashboard` (¡importante! el proyecto Next.js vive en esa subcarpeta, no en la raíz del repositorio).
   - **Framework Preset:** Next.js (se detecta automáticamente al fijar el Root Directory).
   - **Build Command:** `npm run build` (por defecto).
   - **Output Directory:** `.next` (por defecto, no editar).

## 3. Variables de entorno

Si el dashboard llega a consumir una API externa en tiempo de ejecución (actualmente los datos se sirven como JSON estático en `dashboard/data/`, por lo que no son estrictamente necesarias), agrégalas en **Settings → Environment Variables** usando como referencia `.env.example`. Nunca subas valores reales al repositorio.

## 4. Desplegar

1. Click en "Deploy".
2. Espera a que termine el build (2-4 minutos típicamente).
3. Verifica la URL pública generada (`https://<proyecto>.vercel.app`).

## 5. Verificación post-despliegue (Agente Auditor)

- [ ] La URL pública carga sin errores 404/500.
- [ ] Los gráficos se renderizan con datos (no vacíos).
- [ ] Los filtros de país/año/indicador funcionan.
- [ ] La tabla de datos se puede desplazar y filtrar.
- [ ] El enlace de descarga del informe PDF funciona (ver paso 6).
- [ ] El enlace al repositorio de GitHub funciona.
- [ ] El dashboard se ve correctamente en un dispositivo móvil (usar las herramientas de desarrollador del navegador en modo responsive, o probar en un teléfono real).

## 6. Publicar el informe PDF junto al dashboard

Para que el botón "Descargar informe PDF" del dashboard funcione en producción, copia el PDF generado a la carpeta pública de Next.js antes de desplegar (o como parte de un script de build):

```bash
# Desde la raíz del proyecto, después de generar docs/informe_final.pdf
cp docs/informe_final.pdf dashboard/public/informe_final.pdf
git add dashboard/public/informe_final.pdf
git commit -m "report: publicar informe final en el dashboard"
git push
```

Vercel volverá a desplegar automáticamente con cada push a la rama `main`.

## 7. Actualizar el README con los enlaces finales

Una vez desplegado, reemplaza los marcadores `[pendiente...]` en `README.md` con:
- La URL pública del dashboard en Vercel.
- La URL del repositorio de GitHub.
