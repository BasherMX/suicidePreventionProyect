#!/usr/bin/env python3
"""
Comprehensive Dashboard Verification Script
Tests all dashboard functionality locally without starting the server
"""

import sys
import sqlite3
from pathlib import Path
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test_database():
    """Verify database integrity and data"""
    print(f"\n{YELLOW}[TEST 1] Database Verification{RESET}")
    
    db_path = Path("database/suicide_database.db")
    if not db_path.exists():
        print(f"{RED}✗ Database file not found at {db_path}{RESET}")
        return False
    
    print(f"{GREEN}✓ Database file exists (size: {db_path.stat().st_size / 1024 / 1024:.2f} MB){RESET}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        required_tables = ['countries', 'years', 'suicide_facts', 'suicide_texts']
        
        for table in required_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{GREEN}✓ Table '{table}': {count:,} records{RESET}")
            else:
                print(f"{RED}✗ Table '{table}' not found{RESET}")
                return False
        
        # Check for data completeness
        cursor.execute("SELECT COUNT(DISTINCT country_id) FROM suicide_facts")
        countries = cursor.fetchone()[0]
        print(f"{GREEN}✓ Countries in data: {countries}{RESET}")
        
        cursor.execute("SELECT COUNT(DISTINCT year_id) FROM suicide_facts")
        years = cursor.fetchone()[0]
        print(f"{GREEN}✓ Years in data: {years}{RESET}")
        
        # Check for "Unknown" regions
        cursor.execute("SELECT COUNT(*) FROM countries WHERE region = 'Unknown' OR region IS NULL")
        unknown_regions = cursor.fetchone()[0]
        if unknown_regions == 0:
            print(f"{GREEN}✓ No 'Unknown' regions found{RESET}")
        else:
            print(f"{RED}✗ Found {unknown_regions} 'Unknown' regions{RESET}")
            return False
        
        # Check region distribution
        cursor.execute("""
            SELECT region, COUNT(*) as count 
            FROM countries 
            GROUP BY region 
            ORDER BY count DESC
        """)
        print(f"{GREEN}Region distribution:{RESET}")
        for region, count in cursor.fetchall():
            print(f"  - {region}: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"{RED}✗ Database error: {e}{RESET}")
        return False

def test_dependencies():
    """Verify all required packages are installed"""
    print(f"\n{YELLOW}[TEST 2] Dependency Verification{RESET}")
    
    required_packages = {
        'dash': '4.1.0+',
        'pandas': '1.5.0+',
        'plotly': '5.10.0+',
        'flask': '1.0.4+',
        'geopandas': '0.12.0+',
        'sklearn': '1.1.0+',
        'nltk': '3.8+',
    }
    
    all_ok = True
    for package, min_version in required_packages.items():
        try:
            if package == 'sklearn':
                import sklearn
                mod = sklearn
            else:
                mod = __import__(package)
            
            version = getattr(mod, '__version__', 'unknown')
            print(f"{GREEN}✓ {package}: {version}{RESET}")
        except ImportError as e:
            print(f"{RED}✗ {package}: NOT INSTALLED{RESET}")
            all_ok = False
    
    return all_ok

def test_config_files():
    """Verify configuration files"""
    print(f"\n{YELLOW}[TEST 3] Configuration Files{RESET}")
    
    files_to_check = {
        'Procfile': 'web: python dashboard/app.py',
        'runtime.txt': 'python-3.9.18',
        'requirements.txt': 'pandas>=1.5.0'
    }
    
    all_ok = True
    for filename, expected_content in files_to_check.items():
        filepath = Path(filename)
        if filepath.exists():
            content = filepath.read_text().strip()
            if expected_content.lower() in content.lower():
                print(f"{GREEN}✓ {filename} configured correctly{RESET}")
            else:
                print(f"{YELLOW}⚠ {filename} may need review{RESET}")
                print(f"  Expected to contain: {expected_content}")
        else:
            print(f"{RED}✗ {filename} not found{RESET}")
            all_ok = False
    
    return all_ok

def test_data_files():
    """Verify data analysis files"""
    print(f"\n{YELLOW}[TEST 4] Data Analysis Files{RESET}")
    
    analysis_files = [
        'analysis/country_year_aggregated.csv',
        'analysis/country_statistics.csv',
        'analysis/regional_statistics.csv',
    ]
    
    all_ok = True
    for filepath in analysis_files:
        path = Path(filepath)
        if path.exists():
            try:
                df = pd.read_csv(path)
                print(f"{GREEN}✓ {filepath}: {len(df):,} rows{RESET}")
            except Exception as e:
                print(f"{RED}✗ {filepath}: Error reading file - {e}{RESET}")
                all_ok = False
        else:
            print(f"{RED}✗ {filepath} not found{RESET}")
            all_ok = False
    
    return all_ok

def test_app_structure():
    """Verify dashboard app structure"""
    print(f"\n{YELLOW}[TEST 5] Dashboard App Structure{RESET}")
    
    app_file = Path("dashboard/app.py")
    if not app_file.exists():
        print(f"{RED}✗ dashboard/app.py not found{RESET}")
        return False
    
    content = app_file.read_text(encoding='utf-8')
    
    # Check for key components
    checks = {
        'Dash import': 'from dash import',
        'Callbacks': '@app.callback',
        'Choropleth tab': 'dcc.Tab(label="Mapa de Calor"',
        'Trends tab': 'dcc.Tab(label="Tendencias"',
        'Regional tab': 'dcc.Tab(label="Análisis Regional"',
        'Top countries tab': 'dcc.Tab(label="Top',
        'Insights tab': 'dcc.Tab(label="Insights"',
        'Team tab': 'dcc.Tab(label="Integrantes del Equipo"',
        'host 0.0.0.0': "host='0.0.0.0'",
        'Dynamic PORT': "os.environ.get('PORT'",
        'Keep-alive': 'keep_alive',
    }
    
    all_ok = True
    for check_name, search_term in checks.items():
        if search_term in content:
            print(f"{GREEN}✓ {check_name}{RESET}")
        else:
            print(f"{RED}✗ {check_name} not found{RESET}")
            all_ok = False
    
    return all_ok

def test_assets():
    """Verify asset files"""
    print(f"\n{YELLOW}[TEST 6] Asset Files{RESET}")
    
    assets = [
        'dashboard/assets/cimat_logo.png',
        'dashboard/assets/image.png',
    ]
    
    all_ok = True
    for asset in assets:
        path = Path(asset)
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"{GREEN}✓ {asset}: {size_kb:.1f} KB{RESET}")
        else:
            print(f"{RED}✗ {asset} not found{RESET}")
            all_ok = False
    
    return all_ok

def test_git_status():
    """Verify git configuration"""
    print(f"\n{YELLOW}[TEST 7] Git Status{RESET}")
    
    import subprocess
    
    try:
        # Check if git repo
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{GREEN}✓ Git repository initialized{RESET}")
        else:
            print(f"{RED}✗ Not a git repository{RESET}")
            return False
        
        # Check Procfile in git
        result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
        if 'Procfile' in result.stdout:
            print(f"{GREEN}✓ Procfile tracked in git{RESET}")
        else:
            print(f"{RED}✗ Procfile not tracked{RESET}")
            return False
        
        # Check branch
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True)
        branch = result.stdout.strip()
        print(f"{GREEN}✓ On branch: {branch}{RESET}")
        
        return True
    except Exception as e:
        print(f"{YELLOW}⚠ Git check skipped: {e}{RESET}")
        return True

def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("DASHBOARD COMPREHENSIVE VERIFICATION")
    print("=" * 80)
    
    tests = [
        test_database,
        test_dependencies,
        test_config_files,
        test_data_files,
        test_app_structure,
        test_assets,
        test_git_status,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"{RED}✗ Test failed with exception: {e}{RESET}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}✓ ALL TESTS PASSED ({passed}/{total}){RESET}")
        print(f"\n{GREEN}Dashboard is ready for deployment!{RESET}")
        return 0
    else:
        print(f"{YELLOW}⚠ {passed}/{total} tests passed{RESET}")
        print(f"{RED}Some tests failed - review above{RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
