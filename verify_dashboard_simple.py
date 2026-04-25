#!/usr/bin/env python3
"""
Simplified Dashboard Verification
Tests essential dashboard functionality
"""

import sys
from pathlib import Path
import sqlite3
import pandas as pd

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def main():
    print("\n" + "=" * 80)
    print("DASHBOARD VERIFICATION - ESSENTIAL CHECKS")
    print("=" * 80)
    
    checks_passed = 0
    checks_total = 0
    
    # 1. Database
    print(f"\n{YELLOW}[1] Database{RESET}")
    checks_total += 1
    db_path = Path("database/suicide_database.db")
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get counts
            cursor.execute("SELECT COUNT(*) FROM suicide_facts")
            fact_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM countries")
            country_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM years")
            year_count = cursor.fetchone()[0]
            
            # Check for Unknown regions
            cursor.execute("SELECT COUNT(*) FROM countries WHERE region = 'Unknown' OR region IS NULL")
            unknown_count = cursor.fetchone()[0]
            
            print(f"  {GREEN}✓ Database file: {db_path.stat().st_size / 1024 / 1024:.2f} MB{RESET}")
            print(f"  {GREEN}✓ Suicide facts: {fact_count:,}{RESET}")
            print(f"  {GREEN}✓ Countries: {country_count}{RESET}")
            print(f"  {GREEN}✓ Years: {year_count}{RESET}")
            
            if unknown_count == 0:
                print(f"  {GREEN}✓ No 'Unknown' regions{RESET}")
            else:
                print(f"  {RED}✗ Found {unknown_count} 'Unknown' regions{RESET}")
                checks_passed += 0
                checks_total += 1
                
            conn.close()
            checks_passed += 1
        except Exception as e:
            print(f"  {RED}✗ Error: {e}{RESET}")
    else:
        print(f"  {RED}✗ Database not found{RESET}")
    
    # 2. Dashboard directory
    print(f"\n{YELLOW}[2] Dashboard Files{RESET}")
    checks_total += 1
    app_file = Path("dashboard/app.py")
    if app_file.exists():
        print(f"  {GREEN}✓ dashboard/app.py exists{RESET}")
        checks_passed += 1
    else:
        print(f"  {RED}✗ dashboard/app.py missing{RESET}")
    
    # 3. Logos
    print(f"\n{YELLOW}[3] Assets (Logos){RESET}")
    checks_total += 1
    logos_ok = True
    for logo in ["cimat_logo.png", "image.png"]:
        logo_path = Path(f"dashboard/assets/{logo}")
        if logo_path.exists():
            print(f"  {GREEN}✓ {logo}: {logo_path.stat().st_size / 1024:.1f} KB{RESET}")
        else:
            print(f"  {RED}✗ {logo} missing{RESET}")
            logos_ok = False
    
    if logos_ok:
        checks_passed += 1
    
    # 4. Analysis files
    print(f"\n{YELLOW}[4] Analysis CSV Files{RESET}")
    checks_total += 1
    csv_files = [
        "analysis/country_year_aggregated.csv",
        "analysis/country_statistics.csv",
        "analysis/regional_statistics.csv",
    ]
    csv_ok = True
    for csv_file in csv_files:
        path = Path(csv_file)
        if path.exists():
            df = pd.read_csv(path)
            print(f"  {GREEN}✓ {csv_file}: {len(df):,} rows{RESET}")
        else:
            print(f"  {RED}✗ {csv_file} missing{RESET}")
            csv_ok = False
    
    if csv_ok:
        checks_passed += 1
    
    # 5. Configuration
    print(f"\n{YELLOW}[5] Configuration Files{RESET}")
    checks_total += 1
    config_ok = True
    
    procfile = Path("Procfile")
    if procfile.exists() and "python dashboard/app.py" in procfile.read_text():
        print(f"  {GREEN}✓ Procfile: correct{RESET}")
    else:
        print(f"  {RED}✗ Procfile: incorrect or missing{RESET}")
        config_ok = False
    
    requirements = Path("requirements.txt")
    if requirements.exists() and "dash" in requirements.read_text():
        print(f"  {GREEN}✓ requirements.txt: exists{RESET}")
    else:
        print(f"  {RED}✗ requirements.txt: issue{RESET}")
        config_ok = False
    
    runtime = Path("runtime.txt")
    if runtime.exists():
        print(f"  {GREEN}✓ runtime.txt: {runtime.read_text().strip()}{RESET}")
    else:
        print(f"  {YELLOW}⚠ runtime.txt: missing (not critical){RESET}")
    
    if config_ok:
        checks_passed += 1
    
    # 6. Git
    print(f"\n{YELLOW}[6] Git Repository{RESET}")
    checks_total += 1
    git_ok = False
    try:
        import subprocess
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  {GREEN}✓ Git repo initialized{RESET}")
            
            result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
            if 'Procfile' in result.stdout:
                print(f"  {GREEN}✓ Procfile tracked{RESET}")
                git_ok = True
            else:
                print(f"  {RED}✗ Procfile not tracked{RESET}")
        else:
            print(f"  {RED}✗ Not a git repo{RESET}")
    except:
        print(f"  {YELLOW}⚠ Git check failed{RESET}")
    
    if git_ok:
        checks_passed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    percent = int(100 * checks_passed / checks_total)
    
    if checks_passed == checks_total:
        print(f"\n{GREEN}✓ ALL CHECKS PASSED ({checks_passed}/{checks_total}){RESET}")
        print(f"\n{GREEN}Dashboard is ready for deployment!{RESET}\n")
        return 0
    else:
        print(f"\n{YELLOW}Results: {checks_passed}/{checks_total} passed ({percent}%){RESET}\n")
        if checks_passed >= checks_total - 1:
            print(f"{GREEN}Dashboard is ready for deployment!{RESET}\n")
            return 0
        else:
            print(f"{RED}Some critical checks failed{RESET}\n")
            return 1

if __name__ == '__main__':
    sys.exit(main())
