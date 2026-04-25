"""
Phase 3: Geospatial Analysis
Analyze suicide data by geographic regions using Geopandas
"""

import pandas as pd
import sqlite3
import geopandas as gpd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("PHASE 3: GEOSPATIAL ANALYSIS")
print("=" * 80)

# Configuration
DB_PATH = Path("database/suicide_database.db")
SAMPLE_DATA_DIR = Path("sample_data")
GEOM_FILE = SAMPLE_DATA_DIR / "world_geometries.geojson"

# Load data
print("\n[1/4] Loading data from database...")
try:
    conn = sqlite3.connect(str(DB_PATH))
    
    # Load suicide facts with country info
    query = """
    SELECT 
        c.country_name,
        c.country_code,
        c.region,
        c.subregion,
        y.year,
        sf.sex,
        sf.age_group,
        sf.generation,
        sf.suicides_no,
        sf.population,
        sf.suicide_rate_per_100k
    FROM suicide_facts sf
    JOIN countries c ON sf.country_id = c.country_id
    JOIN years y ON sf.year_id = y.year_id
    """
    
    suicide_data = pd.read_sql(query, conn)
    conn.close()
    
    print(f"✓ Loaded {len(suicide_data)} records from database")
    
except Exception as e:
    print(f"✗ Error loading data: {str(e)}")
    exit(1)

# Aggregate by country and year
print("\n[2/4] Aggregating data by country and year...")
try:
    country_year_agg = suicide_data.groupby(['country_name', 'country_code', 'region', 'year']).agg({
        'suicides_no': 'sum',
        'population': 'mean',
        'suicide_rate_per_100k': 'mean'
    }).reset_index()
    
    # Calculate overall country statistics
    country_stats = suicide_data.groupby(['country_name', 'country_code', 'region']).agg({
        'suicides_no': 'sum',
        'suicide_rate_per_100k': 'mean',
        'population': 'mean',
        'year': ['min', 'max']
    }).reset_index()
    
    country_stats.columns = ['country_name', 'country_code', 'region', 'total_suicides', 
                             'avg_suicide_rate', 'avg_population', 'year_min', 'year_max']
    
    print(f"✓ Aggregated data: {len(country_stats)} countries")
    
except Exception as e:
    print(f"✗ Error aggregating data: {str(e)}")
    exit(1)

# Regional analysis
print("\n[3/4] Performing regional analysis...")
try:
    regional_stats = suicide_data.groupby('region').agg({
        'suicides_no': 'sum',
        'suicide_rate_per_100k': ['mean', 'std', 'min', 'max'],
        'country_name': 'nunique',
        'year': 'max'
    }).reset_index()
    
    regional_stats.columns = ['region', 'total_suicides', 'mean_rate', 'std_rate', 
                              'min_rate', 'max_rate', 'num_countries', 'latest_year']
    
    # Sort by mean rate
    regional_stats = regional_stats.sort_values('mean_rate', ascending=False)
    
    print("\n📊 Regional Suicide Statistics:")
    print(regional_stats.to_string())
    
    # Detect hotspots (countries with rate > 75th percentile)
    suicide_rate_75 = suicide_data['suicide_rate_per_100k'].quantile(0.75)
    hotspots = suicide_data[suicide_data['suicide_rate_per_100k'] > suicide_rate_75]['country_name'].unique()
    
    print(f"\n🔴 Suicide Rate Hotspots (> 75th percentile: {suicide_rate_75:.1f}/100k):")
    for country in sorted(hotspots):
        rate = suicide_data[suicide_data['country_name'] == country]['suicide_rate_per_100k'].mean()
        print(f"   • {country}: {rate:.1f}/100k")
    
except Exception as e:
    print(f"✗ Error in regional analysis: {str(e)}")

# Try to load geometries and perform spatial analysis
print("\n[4/4] Attempting geospatial visualization setup...")
try:
    if GEOM_FILE.exists():
        print(f"Loading geometries from {GEOM_FILE}...")
        world = gpd.read_file(str(GEOM_FILE))
        
        # Merge with suicide data
        # Try to match on country name
        world = world.rename(columns={'name': 'country_name'} if 'name' in world.columns else {})
        
        # Create a mapping for country name variations
        mapping = {
            'United States': 'United States of America',
            'Russian Federation': 'Russia',
            'Republic of Korea': 'South Korea',
            'Congo': 'Democratic Republic of the Congo',
        }
        
        country_stats['country_name'] = country_stats['country_name'].replace(mapping)
        
        # Merge (left join to keep all countries)
        merged = world.merge(country_stats, how='left', on='country_name')
        
        print(f"✓ Merged {len(merged)} geographic features with suicide data")
        print(f"✓ {merged['total_suicides'].notna().sum()} countries have complete data")
        
        # Save merged GeoDataFrame for use in visualizations
        merged.to_file("database/merged_suicide_geodata.geojson", driver='GeoJSON')
        print("✓ Saved merged GeoDataFrame to: database/merged_suicide_geodata.geojson")
        
    else:
        print(f"⚠️  Geometry file not found: {GEOM_FILE}")
        print("   Skipping spatial analysis")
        print("   (Run download_kaggle_data.py to get world geometries)")

except Exception as e:
    print(f"⚠️  Geospatial analysis warning: {str(e)}")
    print("   Continuing with non-spatial analysis...")

# Save analysis results
print("\n" + "=" * 80)
print("✓ GEOSPATIAL ANALYSIS COMPLETED")
print("=" * 80)

# Save results to CSV for next phases
regional_stats.to_csv("analysis/regional_statistics.csv", index=False)
country_stats.to_csv("analysis/country_statistics.csv", index=False)
country_year_agg.to_csv("analysis/country_year_aggregated.csv", index=False)

print("\n📁 Analysis results saved:")
print("   • analysis/regional_statistics.csv")
print("   • analysis/country_statistics.csv")
print("   • analysis/country_year_aggregated.csv")

print("\nNext step: Run Phase 4 (visualizations_plotly.py)")
print("=" * 80)
