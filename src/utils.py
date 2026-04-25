"""
Utilities for the Suicide Prevention Project
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Tuple, Dict, List
import warnings

warnings.filterwarnings('ignore')

class SuicideDataManager:
    """Manage database operations for suicide data"""
    
    def __init__(self, db_path: str = "database/suicide_database.db"):
        self.db_path = Path(db_path)
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(str(self.db_path))
        return self.conn
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def get_suicide_data(self) -> pd.DataFrame:
        """Get all suicide facts with country and year info"""
        query = """
        SELECT 
            c.country_name, c.country_code, c.region,
            y.year,
            sf.sex, sf.age_group, sf.generation,
            sf.suicides_no, sf.population, sf.suicide_rate_per_100k
        FROM suicide_facts sf
        JOIN countries c ON sf.country_id = c.country_id
        JOIN years y ON sf.year_id = y.year_id
        """
        return pd.read_sql(query, self.connect())
    
    def get_text_data(self, limit: int = 10000) -> pd.DataFrame:
        """Get text data for NLP analysis"""
        query = f"SELECT * FROM suicide_texts LIMIT {limit}"
        return pd.read_sql(query, self.connect())
    
    def get_regional_stats(self) -> Dict[str, pd.Series]:
        """Get statistics grouped by region"""
        data = self.get_suicide_data()
        return {
            'by_region': data.groupby('region').agg({
                'suicides_no': 'sum',
                'suicide_rate_per_100k': 'mean',
                'population': 'sum'
            })
        }

class DataValidator:
    """Validate data quality"""
    
    @staticmethod
    def check_missing_values(df: pd.DataFrame) -> Dict[str, float]:
        """Check percentage of missing values per column"""
        return (df.isnull().sum() / len(df) * 100).to_dict()
    
    @staticmethod
    def check_outliers(df: pd.DataFrame, column: str, threshold: float = 3.0) -> List[int]:
        """Identify outliers using IQR method"""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        return df[(df[column] < lower_bound) | (df[column] > upper_bound)].index.tolist()
    
    @staticmethod
    def validate_country_data(df: pd.DataFrame) -> bool:
        """Validate country-level data integrity"""
        required_cols = ['country_name', 'year', 'suicides_no', 'population']
        return all(col in df.columns for col in required_cols)

class ReportGenerator:
    """Generate analysis reports"""
    
    @staticmethod
    def generate_summary(data: pd.DataFrame) -> str:
        """Generate text summary of data"""
        summary = f"""
        =================================
        SUICIDE DATA ANALYSIS SUMMARY
        =================================
        
        Total Records: {len(data)}
        Countries: {data['country_name'].nunique()}
        Regions: {data['region'].nunique()}
        Years: {data['year'].min():.0f} - {data['year'].max():.0f}
        
        Global Average Suicide Rate: {data['suicide_rate_per_100k'].mean():.1f} per 100k
        Highest Rate: {data['suicide_rate_per_100k'].max():.1f} per 100k
        Lowest Rate: {data['suicide_rate_per_100k'].min():.1f} per 100k
        
        Total Suicides Recorded: {data['suicides_no'].sum():,.0f}
        Total Population Covered: {data['population'].sum():,.0f}
        """
        return summary

# Export utilities
__all__ = ['SuicideDataManager', 'DataValidator', 'ReportGenerator']
