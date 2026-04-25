#!/usr/bin/env python3
"""
Master Execution Script for Suicide Prevention Project
Runs all 6 phases in sequence
Usage: python run_all_phases.py
"""

import subprocess
import sys
from pathlib import Path
from time import sleep

print("=" * 80)
print("🚀 SUICIDE PREVENTION PROJECT - COMPLETE PIPELINE EXECUTION")
print("=" * 80)

phases = [
    {
        'number': 1,
        'name': 'Data Download',
        'script': 'download_kaggle_data.py',
        'description': 'Download datasets from Kaggle and World Bank API'
    },
    {
        'number': 2,
        'script': 'etl_pipeline.py',
        'name': 'ETL & Database',
        'description': 'Create SQLite database and load data'
    },
    {
        'number': 3,
        'name': 'Geospatial Analysis',
        'script': 'src/analysis_geospatial.py',
        'description': 'Geographic analysis and regional statistics'
    },
    {
        'number': 4,
        'name': 'Plotly Visualizations',
        'script': 'src/visualizations_plotly.py',
        'description': 'Create interactive Plotly visualizations'
    },
    {
        'number': 6,
        'name': 'Advanced Analysis',
        'script': 'src/analysis_advanced.py',
        'description': 'ARIMA forecasting, clustering, NLP analysis'
    }
]

completed = []
failed = []

for phase in phases:
    print(f"\n{'=' * 80}")
    print(f"PHASE {phase['number']}: {phase['name'].upper()}")
    print(f"{'=' * 80}")
    print(f"Description: {phase['description']}")
    print(f"Script: {phase['script']}")
    
    script_path = Path(phase['script'])
    if not script_path.exists():
        print(f"❌ ERROR: Script not found at {script_path}")
        failed.append(phase['name'])
        continue
    
    print(f"\n▶️  Executing {phase['script']}...")
    print("-" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, phase['script']],
            timeout=3600,  # 60 minute timeout per phase
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("-" * 80)
            print(f"✓ Phase {phase['number']} completed successfully")
            completed.append(phase['name'])
        else:
            print("-" * 80)
            print(f"❌ Phase {phase['number']} failed with exit code {result.returncode}")
            failed.append(phase['name'])
            
    except subprocess.TimeoutExpired:
        print("-" * 80)
        print(f"❌ Phase {phase['number']} timeout (exceeded 60 minutes)")
        failed.append(phase['name'])
    except Exception as e:
        print("-" * 80)
        print(f"❌ Phase {phase['number']} error: {str(e)}")
        failed.append(phase['name'])
    
    if len(completed) + len(failed) < len(phases):
        print("\n⏳ Waiting 5 seconds before next phase...")
        sleep(5)

# Print final summary
print("\n" + "=" * 80)
print("📊 PIPELINE EXECUTION SUMMARY")
print("=" * 80)

print(f"\n✓ Completed ({len(completed)}):")
for name in completed:
    print(f"   ✓ {name}")

if failed:
    print(f"\n❌ Failed ({len(failed)}):")
    for name in failed:
        print(f"   ✗ {name}")

print("\n" + "=" * 80)

if len(failed) == 0:
    print("🎉 ALL PHASES COMPLETED SUCCESSFULLY!")
    print("\n📱 NEXT STEPS:")
    print("   1. Review generated files in 'analysis/' directory")
    print("   2. View visualizations: open 'visualizations/' folder in browser")
    print("   3. Launch dashboard: python dashboard/app.py")
    print("   4. Access at: http://localhost:8050")
else:
    print(f"⚠️  {len(failed)} phase(s) failed. Check error messages above.")
    print("   Fix issues and run again.")

print("=" * 80)

sys.exit(0 if len(failed) == 0 else 1)
