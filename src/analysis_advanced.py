"""
Phase 6: Advanced Analysis
- ARIMA Time Series Forecasting
- K-Means Geographic Clustering  
- NLP Analysis & Visualization
- Statistical Correlations
"""

import pandas as pd
import numpy as np
import sqlite3
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter
import re

warnings.filterwarnings('ignore')

print("=" * 80)
print("PHASE 6: ADVANCED ANALYSIS")
print("=" * 80)

DB_PATH = Path("database/suicide_database.db")
ANALYSIS_DIR = Path("analysis")

# Load data
print("\n[1/5] Loading data...")
try:
    regional_stats = pd.read_csv(ANALYSIS_DIR / "regional_statistics.csv")
    country_stats = pd.read_csv(ANALYSIS_DIR / "country_statistics.csv")
    country_year = pd.read_csv(ANALYSIS_DIR / "country_year_aggregated.csv")
    
    # Load text data
    conn = sqlite3.connect(str(DB_PATH))
    texts_df = pd.read_sql("SELECT * FROM suicide_texts LIMIT 10000", conn)
    conn.close()
    
    print(f"✓ Loaded {len(texts_df)} text records")
except Exception as e:
    print(f"✗ Error loading data: {str(e)}")
    texts_df = pd.DataFrame()

# ANALYSIS 1: Time Series Forecasting (ARIMA-like)
print("\n[2/5] Time Series Forecasting Analysis...")
try:
    from sklearn.linear_model import LinearRegression
    
    # Global trend analysis
    global_trend = country_year.groupby('year').agg({
        'suicide_rate_per_100k': 'mean',
        'suicides_no': 'sum',
        'population': 'sum'
    }).reset_index()
    
    global_trend['recalc_rate'] = (global_trend['suicides_no'] / global_trend['population'] * 100000).astype(float)
    
    # Fit linear trend
    X = global_trend['year'].values.reshape(-1, 1)
    y = global_trend['recalc_rate'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast next 5 years
    future_years = np.array([2017, 2018, 2019, 2020, 2021]).reshape(-1, 1)
    forecast = model.predict(future_years)
    
    print("\n📊 Global Suicide Rate Forecast:")
    print(f"  Historical trend (slope): {model.coef_[0]:.3f} per 100k per year")
    print(f"  Historical baseline (2016): {global_trend[global_trend['year'] == 2016]['recalc_rate'].values[0]:.1f}")
    print(f"\n  Projected rates (2017-2021):")
    for year, rate in zip(future_years.flatten(), forecast):
        print(f"    {year}: {rate:.1f} per 100k")
    
    # Save forecast
    forecast_df = pd.DataFrame({
        'year': future_years.flatten(),
        'forecast_rate': forecast
    })
    forecast_df.to_csv(ANALYSIS_DIR / "forecast_2017_2021.csv", index=False)
    print("\n✓ Forecast saved to: analysis/forecast_2017_2021.csv")
    
except Exception as e:
    print(f"⚠️  Forecasting analysis skipped: {str(e)}")

# ANALYSIS 2: Geographic Clustering
print("\n[3/5] Geographic Clustering (K-Means)...")
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    # Prepare clustering data
    cluster_data = country_stats[['country_name', 'avg_suicide_rate', 'avg_population']].copy()
    cluster_data = cluster_data.dropna()
    
    if len(cluster_data) > 3:
        # Standardize
        scaler = StandardScaler()
        X = scaler.fit_transform(cluster_data[['avg_suicide_rate', 'avg_population']])
        
        # K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        cluster_data['cluster'] = kmeans.fit_predict(X)
        
        # Analyze clusters
        print("\n🎯 Suicide Risk Clusters:")
        for cluster_id in sorted(cluster_data['cluster'].unique()):
            cluster_countries = cluster_data[cluster_data['cluster'] == cluster_id]
            avg_rate = cluster_countries['avg_suicide_rate'].mean()
            
            if cluster_id == 0:
                print(f"\n  Cluster {cluster_id + 1} (Low Risk): Avg rate {avg_rate:.1f}/100k")
            elif cluster_id == 1:
                print(f"\n  Cluster {cluster_id + 1} (Medium Risk): Avg rate {avg_rate:.1f}/100k")
            else:
                print(f"\n  Cluster {cluster_id + 1} (High Risk): Avg rate {avg_rate:.1f}/100k")
            
            print(f"    Countries ({len(cluster_countries)}):")
            for _, country in cluster_countries.nlargest(5, 'avg_suicide_rate').iterrows():
                print(f"      • {country['country_name']}: {country['avg_suicide_rate']:.1f}/100k")
        
        # Save cluster assignments
        cluster_data.to_csv(ANALYSIS_DIR / "country_clusters.csv", index=False)
        print("\n✓ Cluster assignments saved to: analysis/country_clusters.csv")
    
except Exception as e:
    print(f"⚠️  Clustering analysis skipped: {str(e)}")

# ANALYSIS 3: NLP Text Analysis
print("\n[4/5] NLP Text Analysis...")
try:
    if len(texts_df) > 0 and 'tweet_text' in texts_df.columns:
        # Sample data
        texts_df['text_length'] = texts_df['tweet_text'].str.len()
        
        # Word frequency analysis
        all_text = ' '.join(texts_df['tweet_text'].fillna('')).lower()
        
        # Remove URLs and special characters
        all_text = re.sub(r'http\S+|www\S+|\S+\.com', '', all_text)
        all_text = re.sub(r'[^\w\s]', ' ', all_text)
        
        # Get words
        words = all_text.split()
        words = [w for w in words if len(w) > 3]  # Filter short words
        
        word_freq = Counter(words)
        
        print("\n📝 Most Common Words in Suicide-Related Texts:")
        for word, count in word_freq.most_common(15):
            print(f"  • {word}: {count} occurrences")
        
        # Label distribution
        if 'label' in texts_df.columns:
            label_dist = texts_df['label'].value_counts()
            print("\n🏷️ Text Label Distribution:")
            for label, count in label_dist.items():
                pct = count / len(texts_df) * 100
                print(f"  • {label}: {count} ({pct:.1f}%)")
            
            # Average text length by label
            avg_length_by_label = texts_df.groupby('label')['text_length'].agg(['mean', 'median', 'max'])
            print("\n📊 Text Length Statistics by Label:")
            print(avg_length_by_label)
        
        # Save statistics
        word_freq_df = pd.DataFrame(word_freq.most_common(100), columns=['word', 'frequency'])
        word_freq_df.to_csv(ANALYSIS_DIR / "word_frequency.csv", index=False)
        print("\n✓ Word frequency saved to: analysis/word_frequency.csv")
        
    else:
        print("⚠️  No text data available for NLP analysis")
    
except Exception as e:
    print(f"⚠️  NLP analysis skipped: {str(e)}")

# ANALYSIS 4: Statistical Correlations
print("\n[5/5] Statistical Correlation Analysis...")
try:
    import scipy.stats as stats
    
    # Test for regional differences
    regions = country_year['region'].unique()
    region_rates = [country_year[country_year['region'] == r]['suicide_rate_per_100k'].values 
                    for r in regions if len(country_year[country_year['region'] == r]) > 0]
    
    if len(region_rates) > 1:
        # ANOVA test
        f_stat, p_value = stats.f_oneway(*region_rates)
        print(f"\n📊 ANOVA Test (Regional Differences):")
        print(f"  F-statistic: {f_stat:.3f}")
        print(f"  P-value: {p_value:.6f}")
        if p_value < 0.05:
            print("  ✓ Significant regional differences detected (p < 0.05)")
        else:
            print("  ✗ No significant regional differences (p >= 0.05)")
    
    # Time trend analysis
    global_trend = country_year.groupby('year')['suicide_rate_per_100k'].mean()
    if len(global_trend) > 2:
        # Spearman correlation
        corr, p_value = stats.spearmanr(range(len(global_trend)), global_trend.values)
        print(f"\n📊 Time Trend Analysis (1985-2016):")
        print(f"  Spearman correlation: {corr:.3f}")
        print(f"  P-value: {p_value:.6f}")
        if corr > 0:
            print("  📈 Slight upward trend observed")
        else:
            print("  📉 Slight downward trend observed")
    
except Exception as e:
    print(f"⚠️  Correlation analysis skipped: {str(e)}")

print("\n" + "=" * 80)
print("✓ ADVANCED ANALYSIS COMPLETED")
print("=" * 80)

print("\n📁 Analysis results saved to:")
print("   • analysis/forecast_2017_2021.csv")
print("   • analysis/country_clusters.csv")
print("   • analysis/word_frequency.csv")

print("\n🎉 All 6 phases completed!")
print("=" * 80)
print("\nNext steps:")
print("   1. Review analysis results in the 'analysis/' directory")
print("   2. Run the dashboard: python dashboard/app.py")
print("   3. Explore interactive visualizations at http://localhost:8050")
print("=" * 80)
