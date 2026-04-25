# Instrucciones para descargar los datos del proyecto

## Problema encontrado

El notebook está correctamente estructurado y las rutas están bien configuradas, pero **faltan los archivos de datos**:

1. `master.csv` - Datos históricos de tasas de suicidio por país
2. `Suicide_Detection.csv` - Dataset de textos para entrenar el modelo de clasificación

## Cómo descargar los datos

### Opción 1: Descargar desde Kaggle (Recomendado)

1. **Ir a Kaggle**
   - Visita: https://www.kaggle.com/datasets/ramanshsingh/suicide-rates-overview-1985-to-2016
   - Descarga `master.csv`

2. **Descargar el dataset de textos**
   - Visita: https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch
   - Descarga `Suicide_Detection.csv`

3. **Colocar los archivos**
   - Coloca ambos archivos en la carpeta: `sample_data/`
   - Estructura esperada:
     ```
     sample_data/
     ├── master.csv
     ├── Suicide_Detection.csv
     ├── california_housing_test.csv
     ├── california_housing_train.csv
     └── ...
     ```

### Opción 2: Usar la API de Kaggle (Avanzado)

Si tienes la CLI de Kaggle instalada:

```bash
kaggle datasets download -d ramanshsingh/suicide-rates-overview-1985-to-2016
kaggle datasets download -d nikhileswarkomati/suicide-watch

# Descomprime en sample_data/
unzip suicide-rates-overview-1985-to-2016.zip -d sample_data/
unzip suicide-watch.zip -d sample_data/
```

## Errores corregidos en el notebook

✅ **Rutas de datos**: Corregidas de `"master.csv"` a `"sample_data/master.csv"`  
✅ **Rutas de datos**: Corregidas de `"Suicide_Detection.csv"` a `"sample_data/Suicide_Detection.csv"`  
✅ **Dependencias instaladas**: numpy, pandas, matplotlib, seaborn, scipy, scikit-learn, nltk, geopandas

## Próximos pasos

1. Descarga los archivos CSV desde Kaggle
2. Coloca los archivos en la carpeta `sample_data/`
3. Ejecuta el notebook nuevamente - debería funcionar sin problemas

## Notas

- El notebook requiere conexión a Internet para descargar recursos de NLTK y datos geoespaciales
- El preprocesamiento de textos puede tomar varios minutos en la primera ejecución
- Los modelos de clasificación (Logistic Regression y SVM) pueden tomar 5-10 minutos según el hardware
