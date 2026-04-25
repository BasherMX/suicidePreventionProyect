"""
Phase 2: ETL Pipeline
Extract -> Transform -> Load data into SQLite database
"""

import pandas as pd
import sqlite3
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("PHASE 2: ETL PIPELINE - DATA LOADING")
print("=" * 80)

# Configuration
SAMPLE_DATA_DIR = Path("sample_data")
DB_PATH = Path("database/suicide_database.db")
SCHEMA_PATH = Path("database/database_schema.sql")

DB_PATH.parent.mkdir(exist_ok=True)

# Step 1: Create database schema
print("\n[1/5] Creating database schema...")
try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    
    # Split by semicolon and execute each statement
    for statement in schema_sql.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    conn.commit()
    print("[OK] Database schema created")
except Exception as e:
    print(f"[ERROR] Error creating schema: {str(e)}")
    exit(1)

# Step 2: Load master.csv (suicide rates)
print("\n[2/5] Loading suicide rates data (master.csv)...")
try:
    master_path = SAMPLE_DATA_DIR / "master.csv"
    if not master_path.exists():
        print(f"[ERROR] File not found: {master_path}")
        raise FileNotFoundError(f"master.csv not found in {SAMPLE_DATA_DIR}")
    
    master_df = pd.read_csv(master_path)
    print(f"  Loaded {len(master_df)} records from master.csv")
    
    # Data cleaning and transformation
    master_df.columns = master_df.columns.str.lower().str.strip()
    
    # Rename columns to match schema
    master_df = master_df.rename(columns={
        'country': 'country_name',
        'year': 'year',
        'suicides_no': 'suicides_no',
        'population': 'population',
        'suicides/100k pop': 'suicide_rate_per_100k',
        'sex': 'sex',
        'age group': 'age_group',
        'generation': 'generation',
    })
    
    # Normalize sex values
    master_df['sex'] = master_df['sex'].str.lower().str.strip()
    
    # Extract region/country code (if available)
    if 'country' in master_df.columns:
        master_df['country_code'] = master_df['country'].str[:2].str.upper()
    else:
        master_df['country_code'] = master_df['country_name'].str[:2].str.upper()
    
    # Fill NaN values
    if 'age_group' not in master_df.columns:
        master_df['age_group'] = 'Unknown'
    else:
        master_df['age_group'] = master_df['age_group'].fillna('Unknown')
    
    if 'generation' not in master_df.columns:
        master_df['generation'] = 'Unknown'
    else:
        master_df['generation'] = master_df['generation'].fillna('Unknown')
    
    print(f"  [OK] Data cleaned: {len(master_df)} records")
    
except Exception as e:
    print(f"[ERROR] Error loading master.csv: {str(e)}")
    master_df = pd.DataFrame()

# Step 3: Load Suicide_Detection.csv (texts)
print("\n[3/5] Loading text data (Suicide_Detection.csv)...")
try:
    text_path = SAMPLE_DATA_DIR / "Suicide_Detection.csv"
    if not text_path.exists():
        print(f"[ERROR] File not found: {text_path}")
        raise FileNotFoundError(f"Suicide_Detection.csv not found in {SAMPLE_DATA_DIR}")
    
    texts_df = pd.read_csv(text_path)
    print(f"  Loaded {len(texts_df)} text records")
    
    # Clean column names
    texts_df.columns = texts_df.columns.str.lower().str.strip()
    
    # Normalize label values
    if 'class' in texts_df.columns:
        # Map class values: 0 = non-suicide, 1 = suicide (or similar)
        texts_df['label'] = texts_df['class'].apply(lambda x: 'suicide' if x == 1 else 'non-suicide')
        texts_df = texts_df.drop('class', axis=1)
    elif 'label' in texts_df.columns:
        texts_df['label'] = texts_df['label'].str.lower().str.strip()
    
    # Ensure text column exists
    if 'text' not in texts_df.columns:
        # Try common alternatives
        if 'tweet' in texts_df.columns:
            texts_df = texts_df.rename(columns={'tweet': 'text'})
        elif 'post' in texts_df.columns:
            texts_df = texts_df.rename(columns={'post': 'text'})
    
    texts_df['text'] = texts_df['text'].fillna('')
    
    print(f"  [OK] {len(texts_df)} text records loaded and cleaned")
    
except Exception as e:
    print(f"[ERROR] Error loading Suicide_Detection.csv: {str(e)}")
    texts_df = pd.DataFrame()

# Step 4: Insert data into database
print("\n[4/5] Inserting data into database...")

try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 4a: Insert years
    print("  Inserting years...")
    years_set = sorted(set(master_df['year'].dropna().unique()) if not master_df.empty else [])
    for year in years_set:
        decade = int(year // 10 * 10)
        cursor.execute(
            "INSERT OR IGNORE INTO years (year, decade) VALUES (?, ?)",
            (int(year), decade)
        )
    conn.commit()
    print(f"    [OK] Inserted {len(years_set)} years")
    
    # 4b: Insert countries
    print("  Inserting countries...")
    countries_set = master_df['country_name'].unique() if not master_df.empty else []
    for country in countries_set:
        country_code = master_df[master_df['country_name'] == country]['country_code'].iloc[0] if not master_df.empty else country[:2].upper()
        cursor.execute(
            "INSERT OR IGNORE INTO countries (country_code, country_name) VALUES (?, ?)",
            (country_code, str(country))
        )
    conn.commit()
    print(f"    [OK] Inserted {len(countries_set)} countries")
    
    # 4c: Insert suicide facts
    print("  Inserting suicide facts...")
    for idx, row in master_df.iterrows():
        try:
            # Get IDs
            cursor.execute("SELECT country_id FROM countries WHERE country_name = ?", (row['country_name'],))
            country_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT year_id FROM years WHERE year = ?", (int(row['year']),))
            year_id = cursor.fetchone()[0]
            
            # Insert fact
            cursor.execute(
                """INSERT INTO suicide_facts 
                (country_id, year_id, sex, age_group, generation, suicides_no, population, suicide_rate_per_100k)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (country_id, year_id, row['sex'], row.get('age_group', 'Unknown'),
                 row.get('generation', 'Unknown'), int(row['suicides_no']),
                 int(row['population']), float(row['suicide_rate_per_100k']))
            )
        except Exception as e:
            pass  # Skip problematic rows
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM suicide_facts")
    fact_count = cursor.fetchone()[0]
    print(f"    [OK] Inserted {fact_count} suicide facts")
    
    # 4d: Insert text data
    print("  Inserting text data...")
    for idx, row in texts_df.iterrows():
        try:
            cursor.execute(
                "INSERT INTO suicide_texts (tweet_text, label, is_training_data) VALUES (?, ?, ?)",
                (row.get('text', ''), row.get('label', 'non-suicide'), 1)
            )
        except Exception as e:
            pass  # Skip problematic rows
    
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM suicide_texts")
    text_count = cursor.fetchone()[0]
    print(f"    [OK] Inserted {text_count} text records")
    
    conn.close()
    
except Exception as e:
    print(f"[ERROR] Error inserting data: {str(e)}")
    exit(1)

# Step 5: Verify database
print("\n[5/5] Verifying database integrity...")
try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Count records in each table
    tables = ['countries', 'years', 'suicide_facts', 'suicide_texts', 'demographics']
    summary = {}
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        summary[table] = count
        print(f"  {table}: {count} records")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("[OK] ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print(f"Database: {DB_PATH}")
    print(f"Total records loaded: {sum(summary.values())}")
    print("\nNext step: Run Phase 3 (analysis_geospatial.py)")
    print("=" * 80)
    
except Exception as e:
    print(f"[ERROR] Error verifying database: {str(e)}")
    exit(1)
