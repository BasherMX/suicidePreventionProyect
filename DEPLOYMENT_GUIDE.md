# 🚀 Deployment Guide - Suicide Prevention Analytics Dashboard

Este documento explica cómo desplegar el dashboard en plataformas gratuitas.

---

## 📊 Dashboard Local

**URL:** http://localhost:8050  
**Comando:** `.\.venv\Scripts\python.exe dashboard/app.py`

---

## 🌐 Opciones de Deployment Gratuito

### Opción 1: **Render.com** ⭐ (RECOMENDADO)

**Ventajas:**

- Gratuito con tier Starter
- Sin necesidad de tarjeta de crédito para empezar
- Muy fácil de configurar
- Auto-deploy desde GitHub

**Pasos:**

#### 1. Preparar el proyecto

```bash
# Crear archivo requirements.txt (ya existe)
# Crear archivo Procfile
echo "web: gunicorn dashboard.app:server" > Procfile

# Instalar gunicorn
pip install gunicorn
```

#### 2. Subir a GitHub

```bash
git init
git add .
git commit -m "Suicide Prevention Analytics Dashboard"
git branch -M main
git remote add origin https://github.com/tu-usuario/proyecto-suicidio.git
git push -u origin main
```

#### 3. Conectar con Render

1. Ir a https://render.com
2. Hacer signup con GitHub
3. Crear nuevo "Web Service"
4. Seleccionar el repositorio
5. Configurar:
   - **Name:** suicide-prevention-dashboard
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn dashboard.app:server --bind 0.0.0.0:${PORT:-5000}`

#### 4. Variables de Entorno (si necesitas)

En Render → Environment, agregar:

```
FLASK_ENV=production
```

**URL de ejemplo:** `https://suicide-prevention-dashboard.onrender.com`

---

### Opción 2: **Railway.app**

**Ventajas:**

- $5/mes créditos gratis
- Interfaz muy amigable
- Soporte en español

**Pasos:**

#### 1. Preparar

```bash
# Crear Procfile
echo "web: gunicorn dashboard.app:server" > Procfile
pip install gunicorn
```

#### 2. Deploy

1. Ir a https://railway.app
2. Signup con GitHub
3. Crear nuevo proyecto
4. Seleccionar "Deploy from GitHub"
5. Elegir el repositorio
6. Railway auto-detectará que es Python
7. Agregar variable: `PYTHON_VERSION=3.9`

**URL de ejemplo:** `https://proyecto-suicidio-prod.up.railway.app`

---

### Opción 3: **Heroku** (Cambiado - Ahora de Pago)

**⚠️ NOTA:** Heroku ya no tiene tier gratuito desde November 2022. Solo se recomienda si ya tienes cuenta.

---

### Opción 4: **PythonAnywhere.com**

**Ventajas:**

- Hosting específico para Python
- Tier gratuito con limitaciones
- Dashboard administrativo intuitivo

**Pasos:**

1. Ir a https://www.pythonanywhere.com
2. Crear cuenta gratuita
3. Upload de archivos:
   - Subir carpetas `src/`, `database/`, `analysis/`, `dashboard/`
   - Subir `requirements.txt`
4. Crear Web App:
   - Framework: Flask
   - Python: 3.9+
5. Configurar WSGI:

```python
# /var/www/usuario_pythonanywhere_com_wsgi.py
import sys
path = '/home/usuario/proyecto'
if path not in sys.path:
    sys.path.append(path)

from dashboard.app import app as application
```

**URL de ejemplo:** `https://usuario.pythonanywhere.com`

---

### Opción 5: **Vercel + Backend Alternativo**

**Nota:** Vercel es para frontend. Para Dash recomendamos Render o Railway.

---

## 📋 Requisitos para Deployment

### Archivo: `Procfile`

```
web: gunicorn dashboard.app:server --bind 0.0.0.0:${PORT:-5000}
```

### Archivo: `requirements.txt`

```
dash>=2.8.0
plotly>=5.10.0
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
scikit-learn>=1.1.0
nltk>=3.8
geopandas>=0.12.0
geodatasets>=2022.9.0
gunicorn>=20.1.0
```

### Archivo: `runtime.txt` (Opcional, para especificar versión)

```
python-3.9.16
```

---

## 🔧 Estructura Esperada en Servidor

```
proyecto-suicidio/
├── dashboard/
│   └── app.py
├── database/
│   └── suicide_database.db
├── analysis/
│   ├── country_statistics.csv
│   ├── country_year_aggregated.csv
│   ├── regional_statistics.csv
│   └── word_frequency.csv
├── src/
│   ├── visualizations_plotly.py
│   └── utils.py
├── Procfile
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## 🚀 Deploy Paso a Paso (Render)

### Paso 1: Preparar GitHub

```bash
cd proyecto-suicidio
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tuusuario/proyecto-suicidio.git
git push -u origin main
```

### Paso 2: Crear Procfile

```bash
echo "web: gunicorn dashboard.app:server --bind 0.0.0.0:\${PORT:-5000}" > Procfile
```

### Paso 3: Actualizar requirements.txt

```bash
pip freeze > requirements.txt
```

### Paso 4: Commit

```bash
git add Procfile requirements.txt
git commit -m "Add deployment files"
git push
```

### Paso 5: Render.com

1. https://dashboard.render.com/
2. Create → Web Service
3. Connect GitHub repo
4. Configurar exactamente como se muestra arriba
5. Deploy

**¡Listo! Tu dashboard estará disponible en:**

```
https://suicide-prevention-dashboard.onrender.com
```

---

## ✅ Verificación Post-Deployment

1. Visitar la URL pública
2. Verificar que:
   - ✓ El mapa de calor se carga con datos
   - ✓ Dropdown de años funciona
   - ✓ Tabs se cargan correctamente
   - ✓ Los gráficos son interactivos
   - ✓ Las transiciones son suaves

---

## 🛠️ Troubleshooting

### Problema: "No module named 'dashboard'"

**Solución:** Verificar que el Procfile especifica la ruta correcta:

```
web: gunicorn dashboard.app:server
```

### Problema: "Port already in use"

**Solución:** La plataforma asigna automáticamente el puerto. No fijar puerto en el código.

### Problema: Base de datos no se carga

**Solución:**

1. Verificar que `database/suicide_database.db` está en el repo
2. Si es muy grande (>200MB), puede haber límite de upload
3. Considerar comprimir o usar base de datos en la nube (MongoDB Atlas gratis)

### Problema: "CSV files not found"

**Solución:** Verificar paths relativos en el código:

```python
ANALYSIS_DIR = Path("analysis")  # Relativo al directorio raíz
```

---

## 📊 Optimizaciones para Producción

### 1. Deshabilitar debug mode

```python
# dashboard/app.py
app.run(debug=False, port=8050, host='0.0.0.0')
```

### 2. Usar compresión

```python
app = dash.Dash(__name__, compress_css=True, compress_js=True)
```

### 3. Cache de datos

```python
@cache.cached(timeout=300)
def load_data():
    # Cargar datos una sola vez cada 5 minutos
```

---

## 🔐 Variables de Entorno Seguras

Si necesitas almacenar credenciales o configuración sensible:

**En Render/Railway:**
Settings → Environment Variables

**Ejemplo:**

```
DATABASE_URL=postgresql://user:password@host/db
SECRET_KEY=tu_clave_secreta
```

**En código:**

```python
import os
db_url = os.environ.get('DATABASE_URL')
```

---

## 💾 Alternativa: Base de Datos en la Nube

### MongoDB Atlas (Gratuito)

1. https://www.mongodb.com/cloud/atlas
2. Crear cluster gratuito
3. Conectar desde Python con `pymongo`

### Firebase (Gratuito)

1. https://firebase.google.com
2. Integrar con Python usando `firebase-admin`

---

## 📞 Soporte y Recursos

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **PythonAnywhere:** https://help.pythonanywhere.com
- **Dash Deployment:** https://dash.plotly.com/deployment

---

## 🎯 Recomendación Final

**Para este proyecto:**

1. **MEJOR OPCIÓN:** Render.com (más fácil y gratis)
2. **Segunda opción:** Railway.app (interface bonita)
3. **Alternativa:** PythonAnywhere (específico para Python)

---

**¡Tu dashboard estará online en 10 minutos!** 🚀
