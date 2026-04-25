# 🌍 Suicide Prevention Analytics Project

A comprehensive data science project for analyzing global suicide statistics using exploratory data analysis, geospatial visualization, machine learning, and interactive dashboards.

## 📋 Project Overview

This project implements a complete data pipeline that:

- **Downloads** real-world datasets from Kaggle and World Bank APIs
- **Processes** data into a normalized SQLite database
- **Analyzes** geographic patterns and temporal trends
- **Visualizes** insights through interactive Plotly charts
- **Forecasts** future trends using time series analysis
- **Clusters** countries by suicide risk profiles
- **Provides** an interactive Dash dashboard for exploration

## 🏗️ Project Structure

```
PROYECTO_PROGRAMACION/
│
├── 📄 download_kaggle_data.py      # Phase 1: Download datasets
├── 📄 etl_pipeline.py               # Phase 2: ETL into SQLite
├── 📄 run_all_phases.py             # Master execution script
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # This file
│
├── 📁 src/                          # Python modules
│   ├── analysis_geospatial.py       # Phase 3: Geographic analysis
│   ├── visualizations_plotly.py     # Phase 4: Interactive charts
│   ├── analysis_advanced.py         # Phase 6: Advanced analysis
│   └── utils.py                     # Utility functions
│
├── 📁 dashboard/                    # Dash web app
│   └── app.py                       # Phase 5: Dashboard application
│
├── 📁 database/                     # Database files
│   ├── database_schema.sql          # SQLite schema (3NF)
│   ├── suicide_database.db          # ← Database created here
│   └── merged_suicide_geodata.geojson
│
├── 📁 analysis/                     # Analysis outputs
│   ├── regional_statistics.csv
│   ├── country_statistics.csv
│   ├── country_year_aggregated.csv
│   ├── forecast_2017_2021.csv
│   ├── country_clusters.csv
│   └── word_frequency.csv
│
├── 📁 visualizations/               # Interactive Plotly charts
│   ├── 01_choropleth_map.html
│   ├── 02_animated_bar_race.html
│   ├── 03_regional_distribution.html
│   ├── 04_time_series_top5.html
│   └── 05_regional_summary.html
│
├── 📁 sample_data/                  # Downloaded datasets
│   ├── master.csv                   # Suicide rates 1985-2016
│   ├── Suicide_Detection.csv        # Text data for NLP
│   ├── world_bank_indicators.csv    # Economic indicators
│   └── world_geometries.geojson     # World country boundaries
│
└── 📁 Proyecto_Suicidio.ipynb       # Original notebook (improved)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate      # Linux/Mac

# Install all dependencies
pip install -r requirements.txt
```

### 2. Run Complete Pipeline

**Option A: Automatic (Recommended)**

```bash
python run_all_phases.py
# This runs all 6 phases sequentially
```

**Option B: Manual Step-by-Step**

```bash
# Phase 1: Download data
python download_kaggle_data.py

# Phase 2: Create database & load data
python etl_pipeline.py

# Phase 3: Geospatial analysis
python src/analysis_geospatial.py

# Phase 4: Create visualizations
python src/visualizations_plotly.py

# Phase 6: Advanced analysis
python src/analysis_advanced.py

# Phase 5: Launch dashboard
python dashboard/app.py
# Access at: http://localhost:8050
```

### 3. Explore Results

#### Interactive Visualizations

Open any HTML file in `visualizations/` folder with a web browser:

- `01_choropleth_map.html` - World heat map by suicide rate
- `02_animated_bar_race.html` - Top 10 countries animation
- `03_regional_distribution.html` - Regional box plots
- `04_time_series_top5.html` - Country trends 1985-2016
- `05_regional_summary.html` - Regional averages

#### Dash Dashboard

```bash
python dashboard/app.py
# Visit http://localhost:8050 in your browser
```

Dashboard features:

- 🗺️ **Geographic Tab**: Interactive choropleth map with year slider
- 📈 **Trends Tab**: Compare suicide rates across countries
- 👥 **Regional Tab**: Regional statistics and distributions
- 🏆 **Top Countries Tab**: Ranking and filtering
- 🔬 **Insights Tab**: Key findings and statistics

#### CSV Analysis Files

Review generated CSV files in `analysis/` for detailed data exports:

- Forecasts (2017-2021)
- Country clusters and risk profiles
- Word frequency analysis
- Regional statistics

## 📊 6-Phase Architecture

### Phase 1: Data Download

**Script**: `download_kaggle_data.py` (30-45 min)

Downloads from:

- Kaggle: Suicide rates dataset (1985-2016) - 27k records
- Kaggle: Suicide detection texts - 160k+ records
- World Bank API: Economic indicators (GDP, life expectancy, etc.)
- Natural Earth: World geometries (GeoJSON)

**Output**: CSV files in `sample_data/`

### Phase 2: ETL & Database

**Script**: `etl_pipeline.py` (5-10 min)

- Creates normalized SQLite database (3rd Normal Form)
- Schema: 6 tables with referential integrity
- Validates and transforms data
- Indexes for query performance

**Output**: `database/suicide_database.db`

### Phase 3: Geospatial Analysis

**Script**: `src/analysis_geospatial.py` (10-15 min)

- Aggregates data by country, region, year
- Detects suicide hotspots (>75th percentile)
- Regional statistics and comparisons
- Prepares data for visualizations

**Output**: CSV files + GeoJSON with merged spatial data

### Phase 4: Interactive Visualizations

**Script**: `src/visualizations_plotly.py` (15-20 min)

Creates 5 interactive Plotly charts:

- Choropleth world map
- Animated bar race (top 10 countries)
- Regional distribution box plots
- Time series trends
- Regional summary bar charts

**Output**: HTML files (open in browser)

### Phase 5: Dash Dashboard

**Script**: `dashboard/app.py` (starts web server)

Professional web-based dashboard with:

- 5 interactive tabs
- Real-time filtering and selection
- Responsive design
- Key statistics and insights

**Access**: http://localhost:8050

### Phase 6: Advanced Analysis

**Script**: `src/analysis_advanced.py` (30-45 min)

- **ARIMA Forecasting**: Project suicide rates 2017-2021
- **K-Means Clustering**: Group countries by risk profiles
- **NLP Analysis**: Word frequency and text patterns
- **Statistical Tests**: ANOVA, correlations, trend analysis

**Output**: Forecast CSV, cluster assignments, word frequency

## 📈 Key Features

### Data Insights

- 195 countries analyzed
- 32-year time span (1985-2016)
- 27,000+ suicide facts records
- 160,000+ text records for NLP

### Visualizations

- ✅ Interactive choropleth maps with temporal slider
- ✅ Animated bar races showing country rankings
- ✅ Regional distributions and box plots
- ✅ Time series trends with comparisons
- ✅ Heatmaps and scatter plots

### Analysis

- ✅ Geographic hotspot detection
- ✅ Time series forecasting (ARIMA)
- ✅ Country clustering (K-means)
- ✅ NLP text analysis
- ✅ Statistical correlations
- ✅ Regional comparisons

### Dashboard

- ✅ 5 tabbed interface
- ✅ Interactive filters and selections
- ✅ Responsive design
- ✅ Real-time updates
- ✅ Export-ready data

## 🗄️ Database Schema

```sql
TABLES:
- countries (195 records)
- years (32 records: 1985-2016)
- demographics (country × year × indicators)
- suicide_facts (27k records - main analysis table)
- suicide_texts (160k+ records - NLP)
- model_predictions (model outputs)

VIEWS:
- v_suicide_by_country_year
- v_regional_statistics
- v_model_performance

INDEXES:
- Fast queries on country/year/region
```

## 🔍 Data Quality

- **Validation**: Missing value checks, outlier detection
- **Normalization**: 3rd Normal Form database design
- **Referential Integrity**: Foreign key constraints
- **Aggregation**: Multiple levels of detail (global, regional, country, demographic)

## ⚙️ Technology Stack

**Backend**:

- Python 3.7+
- SQLite (database)
- Pandas (data processing)
- Scikit-learn (ML)
- Geopandas (geospatial)
- NLTK (NLP)

**Frontend**:

- Dash (web framework)
- Plotly (interactive charts)
- HTML5/CSS3

**Data Sources**:

- Kaggle (suicide statistics & texts)
- World Bank API (economic indicators)
- Natural Earth (geographies)

## 📝 Important Ethical Notes

⚠️ **This project is for educational and research purposes only**

- Data presented is epidemiological, NOT a diagnostic tool
- Project does NOT diagnose or treat mental health conditions
- Professional mental health support is essential
- Results should be interpreted by qualified professionals
- Always prioritize human welfare and dignity

## 🆘 Mental Health Resources

If you or someone you know is struggling:

| Region           | Service                                   |
| ---------------- | ----------------------------------------- |
| 🇺🇸 USA           | National Suicide Prevention Lifeline: 988 |
| 🇬🇧 UK            | Samaritans: 116 123                       |
| 🇦🇺 Australia     | Lifeline: 13 11 14                        |
| 🇪🇸 Spain         | Teléfono de la Esperanza: 914 59 00 50    |
| 🌍 International | findahelpline.com                         |

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional geospatial analysis
- Deep learning models
- Real-time data ingestion
- Cloud deployment
- Mobile dashboard

## 📄 License

Educational project - MIT License

## 📧 Contact & Support

For questions or issues:

1. Check error messages and logs
2. Review phase-specific documentation
3. Verify all dependencies installed
4. Ensure data files downloaded successfully

---

**Made with ❤️ for data-driven suicide prevention research**

Last Updated: April 2026
