-- Phase 2: SQLite Database Schema (3NF - Third Normal Form)
-- Suicide Prevention Project Database
-- Created for normalized data storage with referential integrity

CREATE TABLE IF NOT EXISTS countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT UNIQUE NOT NULL,
    country_name TEXT NOT NULL,
    region TEXT,
    subregion TEXT,
    iso3 TEXT UNIQUE,
    latitude REAL,
    longitude REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS years (
    year_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER UNIQUE NOT NULL,
    decade INTEGER,
    is_leap_year BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS demographics (
    demographic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    year_id INTEGER NOT NULL,
    gdp_per_capita REAL,
    urban_population_pct REAL,
    life_expectancy REAL,
    total_population INTEGER,
    density REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries (country_id),
    FOREIGN KEY (year_id) REFERENCES years (year_id),
    UNIQUE (country_id, year_id)
);

CREATE TABLE IF NOT EXISTS suicide_facts (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    year_id INTEGER NOT NULL,
    sex TEXT CHECK(sex IN ('male', 'female')),
    age_group TEXT,
    generation TEXT,
    suicides_no INTEGER,
    population INTEGER,
    suicide_rate_per_100k REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries (country_id),
    FOREIGN KEY (year_id) REFERENCES years (year_id)
);

CREATE TABLE IF NOT EXISTS suicide_texts (
    text_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    tweet_text TEXT NOT NULL,
    label TEXT CHECK(label IN ('suicide', 'non-suicide')),
    is_training_data BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    model_name TEXT,
    predicted_label TEXT CHECK(predicted_label IN ('suicide', 'non-suicide')),
    confidence_score REAL CHECK(confidence_score >= 0 AND confidence_score <= 1),
    is_correct BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES suicide_texts (text_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_country_code ON countries(country_code);
CREATE INDEX IF NOT EXISTS idx_suicide_facts_country_year ON suicide_facts(country_id, year_id);
CREATE INDEX IF NOT EXISTS idx_suicide_texts_label ON suicide_texts(label);
CREATE INDEX IF NOT EXISTS idx_demographics_country_year ON demographics(country_id, year_id);

-- Create views for common queries
CREATE VIEW IF NOT EXISTS v_suicide_by_country_year AS
SELECT 
    c.country_name,
    c.region,
    y.year,
    sf.sex,
    sf.age_group,
    sf.generation,
    SUM(sf.suicides_no) as total_suicides,
    AVG(sf.suicide_rate_per_100k) as avg_suicide_rate,
    AVG(d.gdp_per_capita) as avg_gdp_per_capita,
    AVG(d.life_expectancy) as avg_life_expectancy
FROM suicide_facts sf
JOIN countries c ON sf.country_id = c.country_id
JOIN years y ON sf.year_id = y.year_id
LEFT JOIN demographics d ON sf.country_id = d.country_id AND sf.year_id = d.year_id
GROUP BY c.country_name, c.region, y.year, sf.sex, sf.age_group, sf.generation;

CREATE VIEW IF NOT EXISTS v_regional_statistics AS
SELECT 
    c.region,
    y.year,
    COUNT(DISTINCT c.country_id) as num_countries,
    SUM(sf.suicides_no) as total_suicides,
    SUM(sf.population) as total_population,
    ROUND(CAST(SUM(sf.suicides_no) AS FLOAT) / CAST(SUM(sf.population) AS FLOAT) * 100000, 2) as region_suicide_rate
FROM suicide_facts sf
JOIN countries c ON sf.country_id = c.country_id
JOIN years y ON sf.year_id = y.year_id
GROUP BY c.region, y.year;

CREATE VIEW IF NOT EXISTS v_model_performance AS
SELECT 
    model_name,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_predictions,
    ROUND(CAST(SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as accuracy_pct,
    AVG(confidence_score) as avg_confidence
FROM model_predictions
GROUP BY model_name;
