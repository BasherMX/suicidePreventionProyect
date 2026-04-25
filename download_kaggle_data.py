"""
Phase 1: Automatic Data Download Script
Downloads Kaggle datasets and World Bank indicators
"""

import os
import subprocess
import pandas as pd
import json
import urllib.request
import zipfile
from pathlib import Path

print("=" * 80)
print("PHASE 1: AUTOMATED DATA DOWNLOAD")
print("=" * 80)

# Configuration
SAMPLE_DATA_DIR = Path("sample_data")
SAMPLE_DATA_DIR.mkdir(exist_ok=True)

# Kaggle datasets
KAGGLE_DATASETS = [
    ("russellyates88/suicide-rates-overview-1985-to-2016", "master.csv"),
    ("nikhileswarkomati/suicide-watch", "Suicide_Detection.csv"),
]

print("\n[1/4] Checking Kaggle credentials...")
kaggle_config = Path.home() / ".kaggle" / "kaggle.json"
if not kaggle_config.exists():
    print("⚠️  Kaggle configuration not found!")
    print("Please create ~/.kaggle/kaggle.json with your credentials")
    print("Continuing with alternative data sources...")
else:
    print(f"✓ Kaggle config found at {kaggle_config}")

print("\n[2/4] Downloading Kaggle datasets...")
for dataset_id, filename in KAGGLE_DATASETS:
    output_file = SAMPLE_DATA_DIR / filename
    
    if output_file.exists():
        print(f"✓ {filename} already exists (skipping)")
        continue
    
    print(f"Downloading {dataset_id}...")
    try:
        result = subprocess.run(
            ["kaggle", "datasets", "download", "-d", dataset_id, "-p", str(SAMPLE_DATA_DIR), "--unzip"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"✓ Downloaded {filename}")
        else:
            print(f"✗ Failed to download {dataset_id}")
            if "403" in result.stderr:
                print("  (403 Forbidden - may need to accept dataset terms on Kaggle.com)")
    except Exception as e:
        print(f"✗ Error downloading {dataset_id}: {str(e)}")

print("\n[3/4] Downloading World Bank indicators...")
world_bank_file = SAMPLE_DATA_DIR / "world_bank_indicators.csv"

if not world_bank_file.exists():
    try:
        # World Bank API for key development indicators
        # Indicators: NY.GDP.PCAP.CD (GDP per capita), 
        #            SP.URB.TOTL.IN.ZS (Urban population %), 
        #            SP.DYN.LE00.IN (Life expectancy)
        indicators = "NY.GDP.PCAP.CD;SP.URB.TOTL.IN.ZS;SP.DYN.LE00.IN;NY.ADJ.NNEX.CD"
        
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicators}?format=json&per_page=20000&date=1985:2016"
        
        print("Fetching from World Bank API...")
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        # Process World Bank data
        records = []
        if len(data) > 1:
            for country_record in data[1]:
                country_code = country_record.get("countryiso3code", "")
                country_name = country_record.get("name", "")
                
                for indicator_code, indicator_name in [
                    ("NY.GDP.PCAP.CD", "GDP_per_capita"),
                    ("SP.URB.TOTL.IN.ZS", "urban_population_pct"),
                    ("SP.DYN.LE00.IN", "life_expectancy"),
                ]:
                    if country_record.get("indicator", {}).get("id") == indicator_code:
                        for year_str, value_str in country_record.get("indicator", {}).items():
                            if year_str.isdigit() and value_str:
                                records.append({
                                    "country_code": country_code,
                                    "country_name": country_name,
                                    "indicator": indicator_name,
                                    "year": int(year_str),
                                    "value": float(value_str)
                                })
        
        if records:
            wb_df = pd.DataFrame(records)
            wb_df.to_csv(world_bank_file, index=False)
            print(f"✓ Downloaded World Bank indicators ({len(wb_df)} records)")
        else:
            print("⚠️  No World Bank data retrieved (API may be slow or unavailable)")
    except Exception as e:
        print(f"⚠️  Could not download World Bank data: {str(e)}")
        print("   (This is optional; continuing without it...)")
else:
    print(f"✓ World Bank indicators already exist")

print("\n[4/4] Downloading World geometries...")
geojson_file = SAMPLE_DATA_DIR / "world_geometries.geojson"

if not geojson_file.exists():
    try:
        # Natural Earth data via geodatasets or GitHub
        print("Fetching world geometries from Natural Earth data...")
        
        # Alternative: use geopandas directly
        import geopandas as gpd
        try:
            # Try using geodatasets
            import geodatasets
            world_geom = gpd.read_file(geodatasets.get_path('naturalearth.land'))
            world_geom.to_file(geojson_file, driver='GeoJSON')
            print(f"✓ Downloaded world geometries using geodatasets")
        except:
            # Fallback: Natural Earth URL
            url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
            zip_path = SAMPLE_DATA_DIR / "ne_countries.zip"
            
            with urllib.request.urlopen(url) as response:
                with open(zip_path, 'wb') as f:
                    f.write(response.read())
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(SAMPLE_DATA_DIR)
            
            shp_file = list(SAMPLE_DATA_DIR.glob("ne_*.shp"))[0]
            world_geom = gpd.read_file(str(shp_file))
            world_geom.to_file(geojson_file, driver='GeoJSON')
            
            zip_path.unlink()
            for f in SAMPLE_DATA_DIR.glob("ne_*"):
                if f.suffix in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                    f.unlink()
            
            print(f"✓ Downloaded world geometries from Natural Earth")
    except Exception as e:
        print(f"⚠️  Could not download world geometries: {str(e)}")
        print("   (This is optional; continuing without it...)")
else:
    print(f"✓ World geometries already exist")

# Summary
print("\n" + "=" * 80)
print("PHASE 1 SUMMARY")
print("=" * 80)

files_present = {
    "master.csv": (SAMPLE_DATA_DIR / "master.csv").exists(),
    "Suicide_Detection.csv": (SAMPLE_DATA_DIR / "Suicide_Detection.csv").exists(),
    "world_bank_indicators.csv": world_bank_file.exists(),
    "world_geometries.geojson": geojson_file.exists(),
}

for filename, exists in files_present.items():
    status = "✓" if exists else "✗"
    print(f"{status} {filename}")

print("\n" + "=" * 80)
print("Next step: Run etl_pipeline.py to create SQLite database")
print("=" * 80)
