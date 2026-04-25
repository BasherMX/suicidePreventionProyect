"""
Phase 5: Dash Interactive Dashboard
Análisis estadístico y visualización interactiva de tasas de suicidio global
Run with: python dashboard/app.py
Access at: http://localhost:8050
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Configuración
DB_PATH = Path("database/suicide_database.db")
ANALYSIS_DIR = Path("analysis")
ASSETS_DIR = Path("dashboard/assets")

# Crear directorio de assets si no existe
ASSETS_DIR.mkdir(exist_ok=True)

# Cargar datos
print("Cargando datos del dashboard...")
try:
    regional_stats = pd.read_csv(ANALYSIS_DIR / "regional_statistics.csv")
    country_stats = pd.read_csv(ANALYSIS_DIR / "country_statistics.csv")
    country_year = pd.read_csv(ANALYSIS_DIR / "country_year_aggregated.csv")
    
    # Convertir columnas numéricas
    numeric_cols_country = ['total_suicides', 'avg_suicide_rate', 'avg_population']
    for col in numeric_cols_country:
        if col in country_stats.columns:
            country_stats[col] = pd.to_numeric(country_stats[col], errors='coerce')
    
    numeric_cols_year = ['suicides_no', 'population', 'suicide_rate_per_100k']
    for col in numeric_cols_year:
        if col in country_year.columns:
            country_year[col] = pd.to_numeric(country_year[col], errors='coerce')
    
    numeric_cols_region = ['total_suicides', 'mean_rate', 'std_rate', 'min_rate', 'max_rate']
    for col in numeric_cols_region:
        if col in regional_stats.columns:
            regional_stats[col] = pd.to_numeric(regional_stats[col], errors='coerce')
    
    print("[OK] Datos cargados correctamente")
except Exception as e:
    print(f"[ERROR] Error al cargar datos: {str(e)}")
    print("Ejecuta las Fases 3 y 4 primero")
    exit(1)

# Inicializar aplicación Dash
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ]
)
app.title = "Dashboard de Análisis Estadístico - Tasas de Suicidio Global"

# Paleta de colores INEGI (azul marino, gris, acentos)
colors = {
    'background': '#f5f5f5',
    'surface': '#ffffff',
    'text': '#333333',
    'text_light': '#666666',
    'primary': '#003d82',      # Azul INEGI
    'primary_light': '#004fa3',
    'accent': '#e74c3c',       # Rojo para énfasis
    'success': '#27ae60',
    'border': '#e0e0e0'
}

# Componentes de equipo
team_members = [
    "ALVAREZ JOCELYN STEPHANIA",
    "LOPEZ SEGURA ANDREA GRACIELA",
    "MEDINA XIMENA",
    "NARVÁEZ PARADA MONTSERRAT",
    "VÁZQUEZ HEREDIA BRAYAN ULISES"
]

# Layout de la aplicación
app.layout = html.Div([
    # Encabezado principal
    html.Div([
        html.Div([
            html.Div([
                html.H1([html.I(className="fas fa-globe"), " Dashboard de Análisis - Tasas de Suicidio Global"], 
                        style={'marginBottom': '15px', 'fontSize': '2.5em', 'fontWeight': '700', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '20px', 'flexWrap': 'wrap'}),
                
                html.Div([
                    html.Img(src='/assets/cimat_logo.png', style={'height': '60px', 'display': 'inline-block', 'marginRight': '30px'}),
                    html.Img(src='/assets/image.png', style={'height': '60px', 'display': 'inline-block'})
                ], style={'marginBottom': '15px', 'textAlign': 'center', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '20px'}),
                
                html.P("Análisis estadístico y visualización de tasas de suicidio a nivel mundial", 
                       style={'color': 'rgba(255,255,255,0.85)', 'marginBottom': '0px', 'fontSize': '1.1em'})
            ], style={'marginBottom': '15px'}),
            
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.2)', 'marginTop': '15px', 'marginBottom': '15px'}),
            
            html.Div([
                html.Div([
                    html.P("MAESTRÍA EN ANÁLISIS ESTADÍSTICO Y COMPUTACIÓN", style={'fontSize': '0.9em', 'marginBottom': '5px', 'opacity': '0.9'}),
                    html.P("Segundo Semestre - Materia Programación", style={'fontSize': '0.85em', 'marginBottom': '5px', 'opacity': '0.85'}),
                    html.P("CENTRO DE INVESTIGACIÓN EN MATEMÁTICAS A.C. (CIMAT)", style={'fontSize': '0.85em', 'opacity': '0.85'})
                ], style={'width': '100%', 'textAlign': 'center'})
            ], style={'fontSize': '0.9em'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 20px'})
    ], style={
        'backgroundColor': colors['primary'],
        'color': 'white',
        'padding': '35px 20px 25px',
        'marginBottom': '20px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
    }),
    
    # Contenido principal
    html.Div([
        # Tabs navegables
        dcc.Tabs(id='tabs', value='tab-1', parent_className='custom-tabs', children=[
            
            # PESTAÑA 1: Análisis Geográfico
            dcc.Tab(label=html.Span([html.I(className="fas fa-map"), " Análisis Geográfico"]), 
                    value='tab-1', 
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-globe"), " Distribución Geográfica de Tasas de Suicidio"]),
                    
                    html.Div([
                        html.Div([
                            html.Label("Selecciona un Año:", style={'fontWeight': '600', 'display': 'block', 'marginBottom': '10px'}),
                            dcc.Dropdown(
                                id='choropleth-year',
                                options=[{'label': str(int(year)), 'value': year} 
                                        for year in sorted(country_year['year'].unique())],
                                value=2011,
                                style={'width': '100%'}
                            )
                        ], style={'width': '100%', 'maxWidth': '250px', 'marginBottom': '20px'}),
                    ], style={'display': 'flex', 'alignItems': 'flex-end'}),
                    
                    dcc.Graph(id='choropleth-graph', style={'marginTop': '20px'})
                ], style={'padding': '25px'})
            ]),
            
            # PESTAÑA 2: Tendencias Temporales
            dcc.Tab(label=html.Span([html.I(className="fas fa-chart-line"), " Tendencias Temporales"]), 
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-history"), " Tendencias de Tasas de Suicidio en el Tiempo"]),
                    
                    html.Div([
                        html.Div([
                            html.Label("Selecciona Países:", style={'fontWeight': '600', 'display': 'block', 'marginBottom': '10px'}),
                            dcc.Dropdown(
                                id='trend-countries',
                                options=[{'label': c, 'value': c} for c in sorted(country_stats['country_name'].dropna().unique())],
                                value=['Brazil', 'Germany', 'Japan', 'Mexico', 'Russian Federation', 'United States'],
                                multi=True,
                                style={'width': '100%'}
                            )
                        ], style={'width': '100%', 'marginBottom': '20px'}),
                    ]),
                    
                    dcc.Graph(id='trend-graph')
                ], style={'padding': '25px'})
            ]),
            
            # PESTAÑA 3: Comparación Regional
            dcc.Tab(label=html.Span([html.I(className="fas fa-chart-bar"), " Comparación Regional"]), 
                    value='tab-3',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-map-pin"), " Estadísticas de Suicidio por Región"]),
                    
                    html.Div([
                        html.Div([
                            dcc.Graph(id='regional-boxplot')
                        ], style={'width': '100%', 'marginBottom': '30px'}),
                        
                        html.Div([
                            dcc.Graph(id='regional-bar')
                        ], style={'width': '100%'}),
                    ]),
                    
                    html.H3("Resumen Estadístico Regional", style={'marginTop': '40px', 'marginBottom': '20px'}),
                    html.Div(id='regional-table', style={'overflowX': 'auto'})
                ], style={'padding': '25px'})
            ]),
            
            # PESTAÑA 4: Países Principales
            dcc.Tab(label=html.Span([html.I(className="fas fa-ranking-star"), " Países Principales"]), 
                    value='tab-4',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-crown"), " Países con Mayores Tasas de Suicidio"]),
                    
                    html.Div([
                        html.Div([
                            html.Label("Número de países a mostrar:", style={'fontWeight': '600', 'display': 'block', 'marginBottom': '15px'}),
                            dcc.Slider(
                                id='top-n-slider',
                                min=5,
                                max=30,
                                step=5,
                                value=15,
                                marks={i: str(i) for i in range(5, 31, 5)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], style={'marginBottom': '30px'}),
                    ]),
                    
                    dcc.Graph(id='top-countries-graph')
                ], style={'padding': '25px'})
            ]),
            
            # PESTAÑA 5: Insights y Análisis
            dcc.Tab(label=html.Span([html.I(className="fas fa-lightbulb"), " Insights y Análisis"]), 
                    value='tab-5',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-chart-pie"), " Hallazgos Principales"]),
                    
                    html.Div([
                        # Grid responsive para tarjetas
                        html.Div([
                            # Tarjeta 1: Países Analizados
                            html.Div([
                                html.H3([html.I(className="fas fa-globe"), " Países Analizados"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{len(country_stats)}", style={'fontSize': '2.5em', 'fontWeight': '700', 'color': colors['primary'], 'marginBottom': '5px'}),
                                html.P("de los 195 países", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#f0f7ff', 'borderRadius': '8px', 'border': f'2px solid {colors["primary"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                            
                            # Tarjeta 2: Período de Análisis
                            html.Div([
                                html.H3([html.I(className="fas fa-calendar"), " Período Analizado"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{int(country_year['year'].min())} - {int(country_year['year'].max())}", style={'fontSize': '2.5em', 'fontWeight': '700', 'color': colors['primary'], 'marginBottom': '5px'}),
                                html.P(f"{int(country_year['year'].max()) - int(country_year['year'].min())} años", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#f0f7ff', 'borderRadius': '8px', 'border': f'2px solid {colors["primary"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                            
                            # Tarjeta 3: Total de Suicidios
                            html.Div([
                                html.H3([html.I(className="fas fa-chart-bar"), " Total de Casos"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{country_year['suicides_no'].sum():,.0f}", style={'fontSize': '2em', 'fontWeight': '700', 'color': colors['accent'], 'marginBottom': '5px'}),
                                html.P("casos registrados", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#ffe8e8', 'borderRadius': '8px', 'border': f'2px solid {colors["accent"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                            
                            # Tarjeta 4: Promedio Global
                            html.Div([
                                html.H3([html.I(className="fas fa-chart-line"), " Promedio Global"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{country_year['suicide_rate_per_100k'].mean():.1f}", style={'fontSize': '2.5em', 'fontWeight': '700', 'color': colors['primary'], 'marginBottom': '5px'}),
                                html.P("por cada 100k habitantes", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#f0f7ff', 'borderRadius': '8px', 'border': f'2px solid {colors["primary"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                            
                            # Tarjeta 5: Tasa Mínima
                            html.Div([
                                html.H3([html.I(className="fas fa-arrow-down"), " Tasa Mínima"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{country_year['suicide_rate_per_100k'].min():.2f}", style={'fontSize': '2.5em', 'fontWeight': '700', 'color': colors['success'], 'marginBottom': '5px'}),
                                html.P("casos registrados", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#e8f5e9', 'borderRadius': '8px', 'border': f'2px solid {colors["success"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                            
                            # Tarjeta 6: Tasa Máxima
                            html.Div([
                                html.H3([html.I(className="fas fa-arrow-up"), " Tasa Máxima"], style={'fontSize': '1em', 'marginTop': '0px'}),
                                html.P(f"{country_year['suicide_rate_per_100k'].max():.2f}", style={'fontSize': '2.5em', 'fontWeight': '700', 'color': colors['accent'], 'marginBottom': '5px'}),
                                html.P("casos registrados", style={'color': colors['text_light'], 'fontSize': '0.9em'})
                            ], style={'backgroundColor': '#ffe8e8', 'borderRadius': '8px', 'border': f'2px solid {colors["accent"]}', 'padding': '20px', 'textAlign': 'center', 'minHeight': '140px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
                        ], style={
                            'display': 'grid',
                            'gridTemplateColumns': 'repeat(auto-fit, minmax(220px, 1fr))',
                            'gap': '20px',
                            'marginBottom': '30px'
                        }),
                        
                        # Consideraciones Éticas
                        html.Div([
                            html.H3([html.I(className="fas fa-exclamation-triangle"), " Consideraciones Importantes"], style={'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Este análisis presenta datos epidemiológicos únicamente - NO es una herramienta de diagnóstico clínico"),
                                html.Li("La calidad de datos varía según el país y año de reporte"),
                                html.Li("La correlación NO implica causalidad"),
                                html.Li("El apoyo profesional de salud mental es esencial para prevención"),
                                html.Li("Si tú o alguien que conoces necesita ayuda, contacta servicios locales de salud mental")
                            ], style={'paddingLeft': '20px', 'lineHeight': '1.8'})
                        ], style={'backgroundColor': '#f8d7da', 'borderRadius': '8px', 'border': f'1px solid {colors["border"]}', 'padding': '20px', 'marginTop': '20px'})
                    ], style={'marginTop': '20px'})
                ], style={'padding': '25px'})
            ]),
            
            # PESTAÑA 6: Integrantes del Equipo
            dcc.Tab(label=html.Span([html.I(className="fas fa-users"), " Integrantes del Equipo"]), 
                    value='tab-6',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                html.Div([
                    html.H2([html.I(className="fas fa-graduation-cap"), " Integrantes del Equipo"]),
                    
                    html.Div([
                        # Información institucional
                        html.Div([
                            html.H3("Información del Programa", style={'marginBottom': '20px', 'color': colors['primary']}),
                            
                            html.Div([
                                html.Div([
                                    html.P("Programa Académico", style={'fontWeight': '600', 'marginBottom': '8px'}),
                                    html.P("Maestría en Análisis Estadístico y Computación", style={'color': colors['text_light']})
                                ], style={'marginBottom': '20px'}),
                                
                                html.Div([
                                    html.P("Institución", style={'fontWeight': '600', 'marginBottom': '8px'}),
                                    html.P("Centro de Investigación en Matemáticas A.C. (CIMAT)", style={'color': colors['text_light']})
                                ], style={'marginBottom': '20px'}),
                                
                                html.Div([
                                    html.P("Semestre", style={'fontWeight': '600', 'marginBottom': '8px'}),
                                    html.P("Segundo Semestre", style={'color': colors['text_light']})
                                ], style={'marginBottom': '20px'}),
                                
                                html.Div([
                                    html.P("Materia", style={'fontWeight': '600', 'marginBottom': '8px'}),
                                    html.P("Programación", style={'color': colors['text_light']})
                                ])
                            ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px', 'border': f'1px solid {colors["border"]}'})
                        ], style={'marginBottom': '40px'}),
                        
                        # Miembros del equipo
                        html.Div([
                            html.H3("Integrantes del Equipo (Orden Alfabético)", style={'marginBottom': '25px', 'color': colors['primary']}),
                            
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.I(className="fas fa-user-circle", style={'fontSize': '3em', 'color': colors['primary'], 'marginBottom': '15px'}),
                                        html.P(member, style={
                                            'fontWeight': '600',
                                            'fontSize': '1.05em',
                                            'marginBottom': '0px',
                                            'color': colors['text'],
                                            'textAlign': 'center'
                                        })
                                    ], style={
                                        'padding': '25px 20px',
                                        'backgroundColor': colors['surface'],
                                        'borderRadius': '8px',
                                        'border': f'2px solid {colors["primary"]}',
                                        'textAlign': 'center',
                                        'transition': 'all 0.3s ease',
                                        'minHeight': '180px',
                                        'display': 'flex',
                                        'flexDirection': 'column',
                                        'justifyContent': 'center',
                                        'alignItems': 'center',
                                        'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                                        'hover': {'boxShadow': '0 4px 12px rgba(0,61,130,0.2)'}
                                    })
                                ], style={'padding': '10px'})
                                for member in team_members
                            ], style={
                                'display': 'grid',
                                'gridTemplateColumns': 'repeat(auto-fit, minmax(220px, 1fr))',
                                'gap': '20px',
                                'marginBottom': '30px'
                            }),
                        ]),
                    ], style={'marginTop': '20px'})
                ], style={'padding': '25px'})
            ])
        ], style={
            'borderBottom': f'3px solid {colors["primary"]}',
            'marginBottom': '20px'
        })
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 15px'}),
    
    # Footer
    html.Footer([
        html.Div([
            html.P([
                "MAEC - 2026  |  ",
                html.A("Integrantes del Equipo", 
                       href="",
                       id='footer-link',
                       style={'color': colors['primary'], 'textDecoration': 'underline', 'cursor': 'pointer', 'fontWeight': '600'})
            ], style={'textAlign': 'center', 'marginBottom': '0px', 'fontSize': '0.9em'})
        ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px 15px'})
    ], style={
        'backgroundColor': colors['surface'],
        'borderTop': f'2px solid {colors["border"]}',
        'marginTop': '40px',
        'color': colors['text_light']
    })
    
], style={
    'backgroundColor': colors['background'],
    'minHeight': '100vh',
    'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'color': colors['text'],
    'paddingBottom': '40px',
    'display': 'flex',
    'flexDirection': 'column'
})

# Callback para footer link
@callback(
    Output('tabs', 'value'),
    Input('footer-link', 'n_clicks'),
    prevent_initial_call=True
)
def navigate_to_team(n_clicks):
    return 'tab-6'

# Estilos CSS personalizados
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #f5f5f5; }
            
            .custom-tab { 
                padding: 12px 24px;
                cursor: pointer;
                border-bottom: 3px solid transparent;
                font-weight: 500;
                color: #666;
                transition: all 0.3s ease;
                display: flex;
                alignItems: center;
                gap: 10px;
                whiteSpace: nowrap;
            }
            
            .custom-tab:hover { 
                color: #003d82;
                backgroundColor: #f5f5f5;
            }
            
            .custom-tab--selected { 
                border-bottom-color: #003d82;
                color: #003d82;
                fontWeight: 700;
            }
            
            .custom-tabs-container { 
                display: flex;
                overflowX: auto;
                overflowY: hidden;
            }
            
            h2 { 
                marginBottom: 20px;
                fontSize: 1.8em;
                fontWeight: 700;
                color: #003d82;
                display: flex;
                alignItems: center;
                gap: 12px;
            }
            
            h3 { 
                fontSize: 1.3em;
                fontWeight: 600;
                color: #333;
                marginTop: 20px;
            }
            
            h1 {
                fontSize: 2.5em;
            }
            
            /* Plotly colorbar adjustments for mobile */
            .colorbar-mobile .cb {
                width: 100% !important;
            }
            
            @media (max-width: 1024px) {
                h1 { fontSize: 2em; }
                h2 { fontSize: 1.5em; }
            }
            
            @media (max-width: 768px) {
                h1 { 
                    fontSize: 1.4em;
                    margin: 0 auto;
                    text-align: center;
                }
                h2 { fontSize: 1.4em; }
                h3 { fontSize: 1.1em; }
                .custom-tab { 
                    padding: 8px 12px; 
                    fontSize: 0.8em; 
                }
                .custom-tabs-container { 
                    overflowX: scroll;
                    display: flex;
                    width: 100%;
                    flexWrap: nowrap;
                }
                
                /* Hide menu on mobile, show hamburger */
                .navbar {
                    display: none;
                }
                
                /* Adjust graph dimensions */
                .js-plotly-plot {
                    overflow-x: auto !important;
                }
                
                /* Colorbar for choropleth - make horizontal on mobile */
                .plotly .colorbar {
                    width: 30px !important;
                    height: auto;
                }
                
                /* Reduce padding */
                div[style*="padding: 25px"] {
                    padding: 15px !important;
                }
            }
            
            @media (max-width: 480px) {
                h1 { 
                    fontSize: 1.1em;
                    line-height: 1.2;
                }
                h2 { 
                    fontSize: 1.2em;
                    gap: 8px;
                }
                h3 { fontSize: 1em; }
                .custom-tab { 
                    padding: 6px 8px; 
                    fontSize: 0.7em; 
                    gap: 5px;
                }
                
                div[style*="display: grid"] {
                    grid-template-columns: 1fr !important;
                }
                
                div[style*="maxWidth: 220px"] {
                    max-width: 100% !important;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer></footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

# Callbacks para interactividad
@callback(
    Output('choropleth-graph', 'figure'),
    Input('choropleth-year', 'value')
)
def update_choropleth(selected_year):
    """Actualiza el mapa de calor con datos del año seleccionado"""
    data = country_year[country_year['year'] == selected_year]
    
    fig = go.Figure(data=go.Choropleth(
        locations=data['iso3_code'],
        z=data['suicide_rate_per_100k'],
        colorscale='Reds',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar=dict(
            title="Tasa/100k",
            thickness=15,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>%{customdata}</b><br>Tasa: %{z:.1f}<extra></extra>',
        customdata=data['country_name']
    ))
    
    fig.update_layout(
        title=f'Tasas de Suicidio Mundiales - {int(selected_year)}',
        height=700,
        geo=dict(showland=True, landcolor='rgb(243, 243, 243)'),
        font=dict(family="'Inter', sans-serif"),
        margin=dict(l=0, r=60, t=40, b=0)
    )
    
    return fig

@callback(
    Output('trend-graph', 'figure'),
    Input('trend-countries', 'value')
)
def update_trends(selected_countries):
    """Actualiza gráfico de tendencias temporales"""
    if not selected_countries:
        selected_countries = country_stats.dropna(subset=['avg_suicide_rate']).nlargest(3, 'avg_suicide_rate')['country_name'].values
    
    data = country_year[country_year['country_name'].isin(selected_countries)]
    
    fig = px.line(data, x='year', y='suicide_rate_per_100k', color='country_name',
                  markers=True, 
                  title='Tendencias de Tasas de Suicidio',
                  labels={'suicide_rate_per_100k': 'Tasa por 100k', 'year': 'Año', 'country_name': 'País'},
                  color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_layout(height=600, hovermode='x unified', font=dict(family="'Inter', sans-serif"))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    return fig

@callback(
    [Output('regional-boxplot', 'figure'),
     Output('regional-bar', 'figure'),
     Output('regional-table', 'children')],
    Input('tabs', 'value')
)
def update_regional(_):
    """Actualiza gráficos y tabla de comparación regional"""
    # Box plot
    fig1 = px.box(country_year, x='region', y='suicide_rate_per_100k',
                  color='region', 
                  title='Distribución de Tasas por Región',
                  labels={'suicide_rate_per_100k': 'Tasa por 100k', 'region': 'Región'},
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig1.update_layout(height=500, showlegend=False, font=dict(family="'Inter', sans-serif"))
    
    # Bar chart
    fig2 = go.Figure(data=[go.Bar(
        y=regional_stats['region'],
        x=regional_stats['mean_rate'],
        orientation='h',
        marker=dict(color=regional_stats['mean_rate'], colorscale='Reds'),
        hovertemplate='%{y}<br>Tasa Promedio: %{x:.1f}<extra></extra>'
    )])
    fig2.update_layout(
        title='Tasa Promedio por Región',
        xaxis_title='Tasa Promedio',
        yaxis_title='Región',
        height=500,
        font=dict(family="'Inter', sans-serif"),
        margin=dict(l=150, r=20, t=40, b=40)
    )
    
    # Tabla regional
    table = html.Table([
        html.Thead(
            html.Tr([
                html.Th("Región", style={'padding': '12px', 'textAlign': 'left', 'borderBottom': '2px solid #003d82', 'fontWeight': '600'}),
                html.Th("Tasa Promedio", style={'padding': '12px', 'textAlign': 'center', 'borderBottom': '2px solid #003d82', 'fontWeight': '600'}),
                html.Th("Tasa Mínima", style={'padding': '12px', 'textAlign': 'center', 'borderBottom': '2px solid #003d82', 'fontWeight': '600'}),
                html.Th("Tasa Máxima", style={'padding': '12px', 'textAlign': 'center', 'borderBottom': '2px solid #003d82', 'fontWeight': '600'}),
                html.Th("Países", style={'padding': '12px', 'textAlign': 'center', 'borderBottom': '2px solid #003d82', 'fontWeight': '600'})
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td(row['region'], style={'padding': '10px', 'borderBottom': '1px solid #e0e0e0'}),
                html.Td(f"{row['mean_rate']:.2f}", style={'padding': '10px', 'textAlign': 'center', 'borderBottom': '1px solid #e0e0e0'}),
                html.Td(f"{row['min_rate']:.2f}", style={'padding': '10px', 'textAlign': 'center', 'borderBottom': '1px solid #e0e0e0'}),
                html.Td(f"{row['max_rate']:.2f}", style={'padding': '10px', 'textAlign': 'center', 'borderBottom': '1px solid #e0e0e0'}),
                html.Td(f"{int(row['num_countries'])}", style={'padding': '10px', 'textAlign': 'center', 'borderBottom': '1px solid #e0e0e0'})
            ]) for _, row in regional_stats.iterrows()
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '10px', 'fontSize': '0.95em'})
    
    return fig1, fig2, table

@callback(
    Output('top-countries-graph', 'figure'),
    Input('top-n-slider', 'value')
)
def update_top_countries(n):
    """Actualiza gráfico de países principales"""
    top_data = country_stats.dropna(subset=['avg_suicide_rate']).nlargest(n, 'avg_suicide_rate').sort_values('avg_suicide_rate')
    
    fig = px.bar(top_data, y='country_name', x='avg_suicide_rate',
                 orientation='h', 
                 title=f'Top {n} Países por Tasa Promedio de Suicidio',
                 labels={'avg_suicide_rate': 'Tasa Promedio por 100k', 'country_name': 'País'},
                 color='avg_suicide_rate', 
                 color_continuous_scale='Reds')
    
    fig.update_layout(
        height=max(500, 250 + (n * 15)),
        yaxis={'categoryorder': 'total ascending'},
        font=dict(family="'Inter', sans-serif"),
        margin=dict(l=180, r=40, t=40, b=40),
        coloraxis_colorbar=dict(
            thickness=15,
            len=0.7
        )
    )
    
    return fig

if __name__ == '__main__':
    import os
    
    port = int(os.environ.get('PORT', 8050))
    
    print("=" * 80)
    print("Iniciando Dashboard de Análisis...")
    print("=" * 80)
    print(f"\nDashboard disponible en: http://0.0.0.0:{port}")
    print("Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=False, port=port, host='0.0.0.0')
