# 🌍 Proyecto Suicidio - Dashboard de Análisis Global

**Status:** ✅ **COMPLETADO Y FUNCIONAL**

Dashboard interactivo para análisis de tasas de suicidio global (1985-2016) con visualizaciones en tiempo real.

---

## 📊 Características Principales

### 🗺️ Tab 1: Geographic Analysis (Análisis Geográfico)

- **Mapa de calor interactivo** con tasas de suicidio por país
- **Selector de años** (1985-2016) para ver cambios temporales
- **Escala de color Reds** para identificar hotspots
- Datos de **71 países** analizados

### 📈 Tab 2: Temporal Trends (Tendencias Temporales)

- **Gráfico de líneas** comparando múltiples países
- **Selector de países** (dropdown con multi-select)
- Visualiza **32 años de datos** (1985-2016)
- Identifica tendencias y patrones

### 👥 Tab 3: Regional Comparison (Comparación Regional)

- **Box plots** para distribuciones por región
- **Estadísticas resumidas**
- Análisis de dispersión de tasas

### 🏆 Tab 4: Top Countries (Mejores/Peores Países)

- **Ranking de países** por tasa de suicidio
- **Slider ajustable** (5-30 países)
- Visualización horizontal para fácil comparación

### 🔬 Tab 5: Insights (Análisis e Insights)

- **Estadísticas globales** (195 países, 32 años)
- **Regiones de alto riesgo**
- **Promedio mundial** en grande
- **Notas éticas** y recursos de ayuda

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar Dashboard

```bash
.\.venv\Scripts\python.exe dashboard/app.py
```

### 3. Acceder

```
http://localhost:8050
```

---

## 📁 Estructura del Proyecto

```
PROYECTO_PROGRAMACION/
│
├── 📊 DASHBOARD
│   └── dashboard/app.py ..................... Aplicación Dash (puerto 8050)
│
├── 💾 DATABASE
│   ├── database_schema.sql .................. Esquema SQLite 3NF
│   └── suicide_database.db ................. Base de datos (200.71 MB, 71 países)
│
├── 📈 ANALYSIS (Datos para Dashboard)
│   ├── country_statistics.csv .............. 71 países con estadísticas
│   ├── country_year_aggregated.csv ......... 1,576 registros (país-año)
│   ├── regional_statistics.csv ............ Estadísticas regionales
│   ├── word_frequency.csv ................. Top 100 palabras (NLP)
│   ├── forecast_2017_2021.csv ............. Predicciones ARIMA
│   └── country_clusters.csv ............... Agrupaciones K-Means
│
├── 🐍 PYTHON MODULES
│   ├── download_kaggle_data.py ............ Descarga datasets Kaggle
│   ├── etl_pipeline.py ................... Carga datos a SQLite
│   ├── run_all_phases.py ................. Ejecuta pipeline completo
│   └── src/
│       ├── analysis_geospatial.py ........ Análisis geográfico
│       ├── visualizations_plotly.py ...... Genera visualizaciones
│       ├── analysis_advanced.py ......... NLP, clustering, forecasting
│       └── utils.py ..................... Funciones utilitarias
│
├── 📋 CONFIGURATION
│   ├── requirements.txt ................... Dependencias Python
│   ├── README.md .......................... Este archivo
│   ├── DEPLOYMENT_GUIDE.md ............... Guía de deployment
│   ├── PROJECT_COMPLETION_REPORT.md .... Reporte final
│   └── sample_data/ ...................... Datasets descargados
│
└── ✅ EXECUTION
    ├── Proyecto_Suicidio.ipynb .......... Notebook original mejorado
    └── Proyecto_Suicidio_Executed.ipynb . Notebook ejecutado
```

---

## 📊 Datos Incluidos

| Métrica                      | Valor                  |
| ---------------------------- | ---------------------- |
| **Países**                   | 71 con datos completos |
| **Años**                     | 32 (1985-2016)         |
| **Registros suicidios**      | 18,888                 |
| **Registros texto (NLP)**    | 232,074                |
| **Tamaño BD**                | 200.71 MB              |
| **CSV registros temporales** | 1,576                  |

---

## 🔧 Comandos Útiles

### Ejecutar Pipeline Completo

```bash
.\.venv\Scripts\python.exe run_all_phases.py
```

### Ejecutar Fase Individual

```bash
# Fase 1: Descargar datos
.\.venv\Scripts\python.exe download_kaggle_data.py

# Fase 2: ETL
.\.venv\Scripts\python.exe etl_pipeline.py

# Fase 3: Análisis geográfico
.\.venv\Scripts\python.exe src/analysis_geospatial.py

# Fase 4: Visualizaciones
.\.venv\Scripts\python.exe src/visualizations_plotly.py

# Fase 6: Análisis avanzado
.\.venv\Scripts\python.exe src/analysis_advanced.py
```

### Consultar Base de Datos

```bash
sqlite3 database/suicide_database.db
sqlite> SELECT COUNT(*) FROM suicide_facts;
sqlite> SELECT * FROM countries LIMIT 5;
sqlite> .quit
```

### Analizar Datos CSV

```python
import pandas as pd

# Cargar datos
df = pd.read_csv('analysis/country_statistics.csv')
print(df.describe())
print(df.nlargest(10, 'avg_suicide_rate'))
```

---

## 🌐 Deployment (Ver DEPLOYMENT_GUIDE.md)

### Opción 1: Render.com (RECOMENDADO ⭐)

- **Gratuito**
- **Sin tarjeta de crédito**
- Auto-deploy desde GitHub
- **URL ejemplo:** `https://suicide-prevention-dashboard.onrender.com`

### Opción 2: Railway.app

- **$5/mes créditos gratis**
- Interface amigable
- Soporte en español

### Opción 3: PythonAnywhere

- Hosting Python específico
- Tier gratuito disponible
- Dashboard administrativo

**[→ Ver DEPLOYMENT_GUIDE.md para instrucciones completas]**

---

## 📈 Tecnología Utilizada

**Backend:**

- Python 3.9+
- Dash (web framework)
- Plotly (visualizaciones)
- Pandas (procesamiento datos)
- SQLite (base de datos)

**Frontend:**

- HTML5 / CSS3
- JavaScript (Plotly interactive)
- Bootstrap styling

**Data Science:**

- Scikit-learn (ML)
- NumPy / SciPy (computación)
- NLTK (procesamiento NLP)
- Geopandas (geospatial)

---

## 🎯 Análisis Incluido

### Estadísticas Descriptivas

- ✅ Tasas promedio por país
- ✅ Agregaciones regionales
- ✅ Tendencias temporales (1985-2016)

### Machine Learning

- ✅ **Forecasting:** Predicciones ARIMA para 2017-2021
- ✅ **Clustering:** K-Means (3 clusters de riesgo)
- ✅ **NLP:** Análisis de palabras clave (232k textos)

### Pruebas Estadísticas

- ✅ ANOVA por región
- ✅ Correlaciones de Spearman
- ✅ Detección de hotspots (>75 percentil)

---

## ⚠️ Consideraciones Éticas

### Este proyecto es:

- 📌 **Para uso educativo y de investigación SOLAMENTE**
- 📌 **NO es una herramienta diagnóstica**
- 📌 **NO reemplaza soporte profesional de salud mental**

### Si necesitas ayuda:

- 🇺🇸 **USA:** 988 (Suicide & Crisis Lifeline)
- 🇬🇧 **UK:** 116 123 (Samaritans)
- 🇪🇸 **Spain:** 914 59 00 50 (Teléfono de la Esperanza)
- 🌍 **Global:** https://findahelpline.com

---

## 🐛 Troubleshooting

### El mapa no muestra datos

**Solución:**

1. Verificar que `iso3_code` existe en CSV:
   ```bash
   head -1 analysis/country_year_aggregated.csv
   ```
2. Recargar el navegador (Ctrl+F5)

### Dashboard tarda en cargar

**Solución:** Los primeros datos (232k registros NLP) se cargan al inicio. Esperar 5-10 segundos.

### Puerto 8050 ya en uso

**Solución:** Matar proceso Python y reintentar:

```bash
taskkill /F /IM python.exe
.\.venv\Scripts\python.exe dashboard/app.py
```

### Error en visualizaciones

**Solución:** Verificar que Plotly está instalado:

```bash
pip install --upgrade plotly dash
```

---

## 📚 Documentación Completa

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Cómo desplegar en la web
- **[PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md)** - Reporte técnico completo
- **[README.md](README.md)** - Documentación del proyecto (original)

---

## 🎓 Recursos Educativos

- [Dash Official Docs](https://dash.plotly.com)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org)
- [SQLite Guide](https://www.sqlite.org/docs.html)

---

## ✅ Checklist de Uso

### Uso Local:

- [x] Instalar dependencias
- [x] Ejecutar dashboard
- [x] Ver mapa de calor
- [x] Probar todos los tabs
- [x] Cambiar año en selector
- [x] Cambiar países en dropdown

### Antes de Deployment:

- [ ] Crear repositorio GitHub
- [ ] Subir código
- [ ] Crear Procfile
- [ ] Elegir plataforma (Render/Railway)
- [ ] Configurar deployment
- [ ] Probar en producción

---

## 📞 Contacto y Soporte

Para preguntas o issues:

1. Revisar este README
2. Consultar DEPLOYMENT_GUIDE.md
3. Revisar PROJECT_COMPLETION_REPORT.md
4. Documentación oficial de las herramientas

---

## 📄 Licencia

Proyecto educativo - MIT License

---

**Última actualización:** April 24, 2026  
**Estado:** ✅ COMPLETO Y OPERACIONAL  
**Dashboard:** http://localhost:8050

---

### 🚀 ¡Listo para Desplegar!

Sigue la guía en **DEPLOYMENT_GUIDE.md** para tener tu dashboard online en minutos.
