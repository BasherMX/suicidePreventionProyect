"""
Phase 4: Interactive Visualizations with Plotly
Create interactive charts for the dashboard
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("PHASE 4: PLOTLY INTERACTIVE VISUALIZATIONS")
print("=" * 80)

# Load aggregated data from Phase 3
ANALYSIS_DIR = Path("analysis")

print("\n[1/6] Loading analysis data...")
try:
    regional_stats = pd.read_csv(ANALYSIS_DIR / "regional_statistics.csv")
    country_stats = pd.read_csv(ANALYSIS_DIR / "country_statistics.csv")
    country_year = pd.read_csv(ANALYSIS_DIR / "country_year_aggregated.csv")
    
    print(f"✓ Loaded regional, country, and temporal data")
except Exception as e:
    print(f"✗ Error loading analysis data: {str(e)}")
    print("  Run Phase 3 first (analysis_geospatial.py)")
    exit(1)

# Create visualizations directory
viz_dir = Path("visualizations")
viz_dir.mkdir(exist_ok=True)

# 1. Choropleth Map (World Heatmap by Suicide Rate)
print("\n[2/6] Creating choropleth map...")
try:
    # Use 2016 data (most recent)
    latest_year_data = country_year[country_year['year'] == country_year['year'].max()].copy()
    
    fig_choropleth = go.Figure(data=go.Choropleth(
        locations=latest_year_data['country_code'],
        z=latest_year_data['suicide_rate_per_100k'],
        colorscale='Reds',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="Suicide Rate<br>per 100k",
        hovertemplate='<b>%{locations}</b><br>Rate: %{z:.1f}/100k<extra></extra>',
    ))
    
    fig_choropleth.update_layout(
        title_text='World Suicide Rates (Latest Year Available)',
        geo=dict(showland=True, landcolor='rgb(243, 243, 243)'),
        height=600,
        font=dict(family="Arial, sans-serif")
    )
    
    fig_choropleth.write_html(str(viz_dir / "01_choropleth_map.html"))
    print("✓ Created: visualizations/01_choropleth_map.html")
    
except Exception as e:
    print(f"✗ Error creating choropleth: {str(e)}")

# 2. Animated Bar Race (Top 10 Countries Over Time)
print("\n[3/6] Creating animated bar race chart...")
try:
    top_countries = country_year.nlargest(10, 'suicide_rate_per_100k')['country_name'].unique()
    filtered_data = country_year[country_year['country_name'].isin(top_countries)].copy()
    filtered_data = filtered_data.sort_values(['year', 'suicide_rate_per_100k'], ascending=[True, False])
    
    fig_bar_race = px.bar(
        filtered_data,
        x='suicide_rate_per_100k',
        y='country_name',
        animation_frame='year',
        animation_group='country_name',
        orientation='h',
        title='Top 10 Countries by Suicide Rate (Animated Over Time)',
        labels={'suicide_rate_per_100k': 'Suicide Rate (per 100k)'},
        height=600,
        color='suicide_rate_per_100k',
        color_continuous_scale='Reds'
    )
    
    fig_bar_race.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        font=dict(family="Arial, sans-serif")
    )
    
    fig_bar_race.write_html(str(viz_dir / "02_animated_bar_race.html"))
    print("✓ Created: visualizations/02_animated_bar_race.html")
    
except Exception as e:
    print(f"✗ Error creating bar race: {str(e)}")

# 3. Regional Box Plots
print("\n[4/6] Creating regional distribution plots...")
try:
    # Prepare data by region
    region_data = country_year.copy()
    
    fig_boxplot = px.box(
        region_data,
        x='region',
        y='suicide_rate_per_100k',
        title='Suicide Rate Distribution by Region',
        labels={'suicide_rate_per_100k': 'Suicide Rate (per 100k)', 'region': 'Region'},
        color='region',
        height=600
    )
    
    fig_boxplot.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif")
    )
    
    fig_boxplot.write_html(str(viz_dir / "03_regional_distribution.html"))
    print("✓ Created: visualizations/03_regional_distribution.html")
    
except Exception as e:
    print(f"✗ Error creating box plots: {str(e)}")

# 4. Time Series by Top Countries
print("\n[5/6] Creating time series visualization...")
try:
    top_5_countries = country_stats.nlargest(5, 'avg_suicide_rate')['country_name'].values
    ts_data = country_year[country_year['country_name'].isin(top_5_countries)]
    
    fig_ts = px.line(
        ts_data,
        x='year',
        y='suicide_rate_per_100k',
        color='country_name',
        title='Suicide Rate Trends - Top 5 Countries',
        labels={'suicide_rate_per_100k': 'Suicide Rate (per 100k)', 'year': 'Year'},
        markers=True,
        height=600
    )
    
    fig_ts.update_layout(
        hovermode='x unified',
        font=dict(family="Arial, sans-serif")
    )
    
    fig_ts.write_html(str(viz_dir / "04_time_series_top5.html"))
    print("✓ Created: visualizations/04_time_series_top5.html")
    
except Exception as e:
    print(f"✗ Error creating time series: {str(e)}")

# 5. Regional Summary Bar Chart
print("\n[6/6] Creating regional summary chart...")
try:
    regional_sorted = regional_stats.sort_values('mean_rate', ascending=True)
    
    fig_regional = go.Figure(data=[
        go.Bar(
            y=regional_sorted['region'],
            x=regional_sorted['mean_rate'],
            orientation='h',
            marker=dict(color=regional_sorted['mean_rate'], colorscale='Reds', showscale=True),
            text=regional_sorted['mean_rate'].round(1),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Avg Rate: %{x:.1f}/100k<extra></extra>'
        )
    ])
    
    fig_regional.update_layout(
        title='Average Suicide Rate by Region',
        xaxis_title='Average Suicide Rate (per 100k)',
        yaxis_title='Region',
        height=500,
        font=dict(family="Arial, sans-serif")
    )
    
    fig_regional.write_html(str(viz_dir / "05_regional_summary.html"))
    print("✓ Created: visualizations/05_regional_summary.html")
    
except Exception as e:
    print(f"✗ Error creating regional summary: {str(e)}")

# Summary statistics
print("\n" + "=" * 80)
print("✓ PLOTLY VISUALIZATIONS COMPLETED")
print("=" * 80)

print("\n📊 Generated visualizations:")
for i, viz in enumerate([
    "01_choropleth_map.html",
    "02_animated_bar_race.html",
    "03_regional_distribution.html",
    "04_time_series_top5.html",
    "05_regional_summary.html"
], 1):
    print(f"   {i}. visualizations/{viz}")

print("\n💡 Open visualizations in a web browser for interactive exploration!")
print("   Example: python -m http.server 8000 (then visit http://localhost:8000/visualizations)")

print("\nNext step: Run Phase 5 (dashboard/app.py)")
print("=" * 80)
