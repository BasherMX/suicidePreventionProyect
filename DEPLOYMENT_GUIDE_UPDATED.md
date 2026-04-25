# 🚀 Guía de Deployment y Ejecución Local

## ✅ Cambios Realizados

### 1. Keep-Alive Daemon

- **Problema**: Render.com duerme instancias inactivas (50+ segundos)
- **Solución**: Script `keep_alive.py` que hace ping cada 30 segundos
- **Automático en Producción**: Se activa automáticamente cuando `RENDER=true`

### 2. Requirements Simplificado

- **Removido**: Jupyter, nbconvert, ipython (no necesarios en producción)
- **Resultado**: Build más rápido y instancia más liviana
- **Compatibilidad**: Incluye todas las dependencias críticas

### 3. Procfile Corregido

```
web: python dashboard/app.py
```

- Ejecuta directamente el app (sin gunicorn)
- Puerto dinámico desde variable `PORT`
- Host `0.0.0.0` para acceso remoto

### 4. Dashboard App Actualizado

- Detecta automáticamente si está en Render (`RENDER` env var)
- Inicia keep-alive daemon automáticamente en producción
- Puerto y host dinámicos

---

## 🏃 Ejecución Local

### Opción 1: Ejecutar Normalmente (Recomendado para desarrollo)

```bash
cd C:\Users\Ulises\Documents\MAEC\2DO_SEMESTRE\PROGRAMACION\PROYECTO_PROGRAMACION

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar dashboard
python dashboard/app.py
```

**URL**: http://localhost:8050

### Opción 2: Ejecutar con Script Keep-Alive

```bash
# (Mismo entorno virtual activado)

# Terminal 1: Keep-alive daemon
python keep_alive.py

# Terminal 2: Dashboard
python dashboard/app.py
```

### Opción 3: Simular Entorno Render Localmente

```bash
# En PowerShell
$env:RENDER = "true"
$env:PORT = "8050"
$env:APP_URL = "http://localhost:8050"

python dashboard/app.py
```

---

## 🌐 Deployment en Render (Corrected)

### Paso 1: Verificar que GitHub tenga los últimos cambios

```bash
git status  # Debe estar limpio
```

### Paso 2: En Render Dashboard

1. Ve a https://dashboard.render.com
2. Selecciona tu proyecto
3. Click en "Trigger New Deploy" o "Manual Deploy"
4. Espera a que complete (ahora sin errores)

### Paso 3: Verificar Build

En los logs debería ver:

```
==> Using Python version 3.9.X (specified in runtime.txt)
==> Running build command 'pip install -r requirements.txt'...
Successfully installed dash plotly pandas numpy scipy...
==> Build successful 🎉
==> Running 'python dashboard/app.py'
[KEEP-ALIVE] Daemon started (Render environment detected)
```

### Paso 4: Acceder

- **URL**: https://suicidePreventionProyect.onrender.com (o la que Render asigne)
- Dashboard debe estar disponible sin delays

---

## 🔧 Troubleshooting

### Problema: "Build failed" con gunicorn

**Causa**: Procfile tiene caché viejo

**Solución**:

1. En Render Settings → "Rebuild Latest Commit"
2. O ir a "Deployments" → Click en el último → "Redeploy"

### Problema: "ModuleNotFoundError: No module named 'jupyter'"

**Causa**: requirements.txt viejo con Jupyter

**Solución**:

```bash
git pull origin main
# Verificar requirements.txt no tiene jupyter
cat requirements.txt | grep -i jupyter  # No debe devolver nada
```

### Problema: Dashboard lento o no responde

**Causa**: Keep-alive no está corriendo

**Verificar**:

- En logs de Render debe haber: `[KEEP-ALIVE] Daemon started`
- Si falta, verificar que `RENDER=true` esté siendo detectado

---

## 📊 Estructura de Deployments

| Ambiente              | Host      | Puerto              | Keep-Alive | URL                                           |
| --------------------- | --------- | ------------------- | ---------- | --------------------------------------------- |
| **Local**             | localhost | 8050                | Manual     | http://localhost:8050                         |
| **Local (Prod-like)** | 0.0.0.0   | 8050                | Daemon     | http://0.0.0.0:8050                           |
| **Render**            | 0.0.0.0   | Dinámico (PORT var) | Automático | https://suicidePreventionProyect.onrender.com |

---

## 🔄 Workflow Recomendado

### Para hacer cambios locales:

```bash
# 1. Editar archivos localmente

# 2. Probar localmente
python dashboard/app.py

# 3. Cuando esté listo, hacer commit
git add .
git commit -m "Descripción de cambios"
git push origin main

# 4. Render automáticamente detecta el push y hace deploy
# (O manualmente: Dashboard → Redeploy)

# 5. Esperar a que complete el build (~2 min)
```

---

## 📝 Variables de Entorno

### En Render (Dashboard → Environment)

Agregar si es necesario:

```
RENDER=true
PORT=5000
PYTHON_VERSION=3.9
```

### Localmente (.env file - opcional)

```env
RENDER=false
PORT=8050
APP_URL=http://localhost:8050
```

---

## ✨ Keep-Alive Detalles

El keep-alive daemon:

- ✅ Se ejecuta en thread separado (no bloquea dashboard)
- ✅ Hace ping cada 30 segundos
- ✅ Silenciosamente falla si hay error (no crashea app)
- ✅ Solo activo en Render (detecta `RENDER` env var)
- ✅ Aumenta un poco el uso de CPU (negligible)

---

**Dashboard listo para producción en Render.com** 🚀
