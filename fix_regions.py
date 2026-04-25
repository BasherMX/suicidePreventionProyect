"""
Fix regional data in the database by mapping countries to UN geographic regions
"""

import sqlite3
from pathlib import Path

# Mapping of countries to UN geographic regions
COUNTRY_REGION_MAPPING = {
    # Americas - North America
    'Canada': 'Americas',
    'United States': 'Americas',
    'Mexico': 'Americas',
    
    # Americas - Central America
    'Belize': 'Americas',
    'Costa Rica': 'Americas',
    'El Salvador': 'Americas',
    'Guatemala': 'Americas',
    'Honduras': 'Americas',
    'Nicaragua': 'Americas',
    'Panama': 'Americas',
    
    # Americas - South America
    'Argentina': 'Americas',
    'Bolivia': 'Americas',
    'Brazil': 'Americas',
    'Chile': 'Americas',
    'Colombia': 'Americas',
    'Ecuador': 'Americas',
    'Guyana': 'Americas',
    'Paraguay': 'Americas',
    'Peru': 'Americas',
    'Suriname': 'Americas',
    'Uruguay': 'Americas',
    'Venezuela': 'Americas',
    
    # Americas - Caribbean
    'Antigua and Barbuda': 'Americas',
    'Bahamas': 'Americas',
    'Barbados': 'Americas',
    'Cuba': 'Americas',
    'Dominica': 'Americas',
    'Dominican Republic': 'Americas',
    'Grenada': 'Americas',
    'Haiti': 'Americas',
    'Jamaica': 'Americas',
    'Saint Kitts and Nevis': 'Americas',
    'Saint Lucia': 'Americas',
    'Saint Vincent and the Grenadines': 'Americas',
    'Trinidad and Tobago': 'Americas',
    'Puerto Rico': 'Americas',
    
    # Europe - Northern Europe
    'Denmark': 'Europe',
    'Estonia': 'Europe',
    'Finland': 'Europe',
    'Iceland': 'Europe',
    'Ireland': 'Europe',
    'Latvia': 'Europe',
    'Lithuania': 'Europe',
    'Norway': 'Europe',
    'Sweden': 'Europe',
    'United Kingdom': 'Europe',
    
    # Europe - Western Europe
    'Austria': 'Europe',
    'Belgium': 'Europe',
    'France': 'Europe',
    'Germany': 'Europe',
    'Luxembourg': 'Europe',
    'Netherlands': 'Europe',
    'Switzerland': 'Europe',
    
    # Europe - Southern Europe
    'Albania': 'Europe',
    'Andorra': 'Europe',
    'Bosnia and Herzegovina': 'Europe',
    'Croatia': 'Europe',
    'Cyprus': 'Europe',
    'Greece': 'Europe',
    'Italy': 'Europe',
    'Malta': 'Europe',
    'Montenegro': 'Europe',
    'Portugal': 'Europe',
    'Serbia': 'Europe',
    'Slovenia': 'Europe',
    'Spain': 'Europe',
    'Macedonia': 'Europe',
    'North Macedonia': 'Europe',
    
    # Europe - Eastern Europe
    'Belarus': 'Europe',
    'Bulgaria': 'Europe',
    'Czech Republic': 'Europe',
    'Czechia': 'Europe',
    'Hungary': 'Europe',
    'Moldova': 'Europe',
    'Poland': 'Europe',
    'Romania': 'Europe',
    'Russian Federation': 'Europe',
    'Slovakia': 'Europe',
    'Ukraine': 'Europe',
    
    # Asia - East Asia
    'China': 'Asia',
    'Hong Kong': 'Asia',
    'Macau': 'Asia',
    'Japan': 'Asia',
    'Mongolia': 'Asia',
    'North Korea': 'Asia',
    'South Korea': 'Asia',
    'Republic of Korea': 'Asia',
    'Taiwan': 'Asia',
    
    # Asia - Southeast Asia
    'Brunei': 'Asia',
    'Cambodia': 'Asia',
    'Indonesia': 'Asia',
    'Laos': 'Asia',
    'Malaysia': 'Asia',
    'Myanmar': 'Asia',
    'Philippines': 'Asia',
    'Singapore': 'Asia',
    'Thailand': 'Asia',
    'Timor-Leste': 'Asia',
    'Vietnam': 'Asia',
    
    # Asia - South Asia
    'Afghanistan': 'Asia',
    'Bangladesh': 'Asia',
    'Bhutan': 'Asia',
    'India': 'Asia',
    'Iran': 'Asia',
    'Maldives': 'Asia',
    'Nepal': 'Asia',
    'Pakistan': 'Asia',
    'Sri Lanka': 'Asia',
    
    # Asia - West Asia/Middle East
    'Armenia': 'Asia',
    'Azerbaijan': 'Asia',
    'Bahrain': 'Asia',
    'Georgia': 'Asia',
    'Kazakhstan': 'Asia',
    'Kyrgyzstan': 'Asia',
    'Uzbekistan': 'Asia',
    'Iraq': 'Asia',
    'Israel': 'Asia',
    'Jordan': 'Asia',
    'Kuwait': 'Asia',
    'Lebanon': 'Asia',
    'Oman': 'Asia',
    'Palestine': 'Asia',
    'Qatar': 'Asia',
    'Saudi Arabia': 'Asia',
    'Syria': 'Asia',
    'Turkey': 'Europe',  # Straddling Europe and Asia
    'United Arab Emirates': 'Asia',
    'Yemen': 'Asia',
    
    # Africa - North Africa
    'Algeria': 'Africa',
    'Egypt': 'Africa',
    'Libya': 'Africa',
    'Morocco': 'Africa',
    'Sudan': 'Africa',
    'Tunisia': 'Africa',
    'Western Sahara': 'Africa',
    
    # Africa - West Africa
    'Benin': 'Africa',
    'Burkina Faso': 'Africa',
    'Cabo Verde': 'Africa',
    'Côte d\'Ivoire': 'Africa',
    'Gambia': 'Africa',
    'Ghana': 'Africa',
    'Guinea': 'Africa',
    'Guinea-Bissau': 'Africa',
    'Liberia': 'Africa',
    'Mali': 'Africa',
    'Mauritania': 'Africa',
    'Niger': 'Africa',
    'Nigeria': 'Africa',
    'Senegal': 'Africa',
    'Sierra Leone': 'Africa',
    'Togo': 'Africa',
    
    # Africa - Central Africa
    'Angola': 'Africa',
    'Cameroon': 'Africa',
    'Central African Republic': 'Africa',
    'Chad': 'Africa',
    'Republic of the Congo': 'Africa',
    'Democratic Republic of the Congo': 'Africa',
    'Equatorial Guinea': 'Africa',
    'Gabon': 'Africa',
    'São Tomé and Príncipe': 'Africa',
    
    # Africa - East Africa
    'Burundi': 'Africa',
    'Comoros': 'Africa',
    'Djibouti': 'Africa',
    'Eritrea': 'Africa',
    'Ethiopia': 'Africa',
    'Kenya': 'Africa',
    'Madagascar': 'Africa',
    'Malawi': 'Africa',
    'Mauritius': 'Africa',
    'Mozambique': 'Africa',
    'Rwanda': 'Africa',
    'Seychelles': 'Africa',
    'Somalia': 'Africa',
    'South Sudan': 'Africa',
    'Tanzania': 'Africa',
    'Uganda': 'Africa',
    'Zambia': 'Africa',
    'Zimbabwe': 'Africa',
    
    # Africa - Southern Africa
    'Botswana': 'Africa',
    'Eswatini': 'Africa',
    'Lesotho': 'Africa',
    'Namibia': 'Africa',
    'South Africa': 'Africa',
    
    # Oceania
    'Australia': 'Oceania',
    'Fiji': 'Oceania',
    'Kiribati': 'Oceania',
    'Marshall Islands': 'Oceania',
    'Micronesia': 'Oceania',
    'Nauru': 'Oceania',
    'New Zealand': 'Oceania',
    'Palau': 'Oceania',
    'Papua New Guinea': 'Oceania',
    'Samoa': 'Oceania',
    'Solomon Islands': 'Oceania',
    'Tonga': 'Oceania',
    'Tuvalu': 'Oceania',
    'Vanuatu': 'Oceania',
}

DB_PATH = Path("database/suicide_database.db")

print("=" * 80)
print("FIXING REGIONAL DATA")
print("=" * 80)

try:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get all unique countries
    cursor.execute("SELECT country_id, country_name FROM countries")
    countries = cursor.fetchall()
    
    print(f"\nProcessing {len(countries)} countries...")
    
    updated = 0
    not_mapped = []
    
    for country_id, country_name in countries:
        region = COUNTRY_REGION_MAPPING.get(country_name)
        
        if region:
            cursor.execute(
                "UPDATE countries SET region = ? WHERE country_id = ?",
                (region, country_id)
            )
            updated += 1
            print(f"  ✓ {country_name} → {region}")
        else:
            not_mapped.append(country_name)
            print(f"  ⚠ {country_name} → NOT MAPPED")
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*80}")
    print(f"[OK] Updated {updated} countries with regions")
    
    if not_mapped:
        print(f"\n[WARNING] {len(not_mapped)} countries not mapped:")
        for country in not_mapped:
            print(f"  - {country}")
    
    print(f"{'='*80}")
    
except Exception as e:
    print(f"[ERROR] Error updating regions: {str(e)}")
    exit(1)
