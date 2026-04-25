# PASO A PASO: CÓMO DESPLEGAR EL DASHBOARD EN RENDER

## 🎯 SITUACIÓN ACTUAL

✅ **Dashboard está 100% listo**
- Código: Funciona sin errores
- Datos: 20,280 registros cargados
- Logos: Presentes y visibles
- Configuración: Correcta (Procfile, requirements.txt)
- Git: Todo sincronizado

❌ **Problema en Render**
- Render tiene cachéado el viejo comando: `gunicorn dashboard.app:server`
- Nuestro Procfile dice: `web: python dashboard/app.py`
- Render no está leyendo el Procfile actualizado

---

## 🚀 SOLUCIÓN: 5 PASOS SIMPLES

### PASO 1: Acceder a Render Dashboard
1. Abre: https://dashboard.render.com/
2. Inicia sesión con tu cuenta de Render
3. Busca tu servicio: "suicide prevention" o similar

### PASO 2: Ir a Configuración
1. Haz click en el servicio
2. Busca la pestaña o sección: **"Settings"** o **"Settings"**
3. Abre: **Build & Deploy**

### PASO 3: Encontrar el Start Command
1. En la sección "Build & Deploy" busca: **"Start Command"**
2. Deberías ver algo como:
   ```
   gunicorn dashboard.app:server --bind 0.0.0.0:${PORT:-5000}
   ```

### PASO 4: Cambiar el Comando
1. Borra todo lo que dice en "Start Command"
2. Escribe: `python dashboard/app.py`
3. Haz click: **"Save"** o **"Update"**

### PASO 5: Hacer Deploy Manual
1. Busca el botón: **"Manual Deploy"** o **"Deploy"** (color rojo)
2. Haz click en él
3. Espera a que aparezca en los logs:
   ```
   ==> Running 'python dashboard/app.py'
   ```
4. Si ves esto, ¡Listo! El deploy fue exitoso

---

## ✅ CÓMO VERIFICAR QUE FUNCIONÓ

### En los Logs de Render, deberías ver:
```
==> Build successful 🎉
==> Deploying...
==> Running 'python dashboard/app.py'
Cargando datos del dashboard...
[OK] Datos cargados correctamente
Dash is running on http://0.0.0.0:8050/
```

### Luego accede a tu dashboard:
1. Copia tu URL de Render (ej: https://tu-app.onrender.com/)
2. Abre en el navegador
3. Deberías ver el dashboard cargando
4. Verifica que:
   - Logos CIMAT e INEGI estén visibles ✓
   - Los 6 tabs aparezcan (Mapa, Tendencias, Regional, Top, Insights, Equipo) ✓
   - La región NO diga "Unknown" ✓
   - El año por defecto sea 2011 ✓

---

## 🆘 SI ALGO SALE MAL

### Error: "gunicorn: command not found"
- Significa que Render TODAVÍA tiene el viejo comando
- Solución: Intenta nuevamente desde PASO 2
- O: Borra el servicio y crea uno nuevo (fresco)

### Error: "ModuleNotFoundError"
- Significa que faltan dependencias
- Solución: Verifica que `requirements.txt` esté correcto en git
- Ejecuta localmente: `python dashboard/app.py` para verificar

### Dashboard carga pero dice "Unknown" regions
- Significa que la base de datos no se actualizó correctamente
- Solución: Re-ejecuta `augment_data.py` y `fix_regions.py` localmente

### Dashboard muy lento o no responde
- El keep-alive daemon debería activarse automáticamente
- Si no: Aumenta la RAM del servicio en Render (tier superior)

---

## 📞 ALTERNATIVA: Si Render sigue con problemas

**Opción A: Usar Heroku (gratis pero con restricciones)**
1. Cambia Procfile a: `web: python dashboard/app.py`
2. Sube a Heroku
3. Debería funcionar directamente

**Opción B: Usar Railway.app**
1. Similar a Render pero a veces sin issues de cache
2. Conecta tu GitHub
3. Será automático

**Opción C: Servidor local con ngrok**
1. Ejecuta: `python dashboard/app.py`
2. En otra terminal: `ngrok http 8050`
3. Comparte el link de ngrok (temporal, pero funciona)

---

## ✨ PRÓXIMAS ACCIONES (Después de Deploy)

Una vez que el dashboard esté en Render:

1. **Documental para presentación**
   - El dashboard está en vivo
   - URLs de acceso listo

2. **Preparar presentación**
   - Mostrar dashboard en vivo
   - Explicar cada tab
   - Datos de suicidio por país/región

3. **Backup**
   - La base de datos ya está en git
   - Los archivos están syncronizados

---

## 📋 RESUMEN FINAL

| Paso | Acción | Tiempo |
|------|--------|--------|
| 1 | Ir a Render Dashboard | 1 min |
| 2 | Entrar a Settings | 1 min |
| 3 | Encontrar Start Command | 2 min |
| 4 | Cambiar comando a `python dashboard/app.py` | 2 min |
| 5 | Hacer Manual Deploy | 3-5 min |
| **Total** | **Configuración de Render** | **~10 minutos** |

Luego:
- Deploy automático: 2-5 minutos
- Dashboard accesible: Inmediatamente después

**Tiempo total desde ahora hasta dashboard en vivo: ~15 minutos**

---

## 🎉 LISTO

Una vez que completes estos 5 pasos, tu dashboard de análisis de tasas de suicidio global estará en vivo en Render y accesible desde cualquier lugar.

¿Necesitas ayuda en alguno de estos pasos? Déjame saber cuál.
