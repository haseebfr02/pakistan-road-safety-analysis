"""
Pakistan Road Safety Analysis
Step 2: SQL Analysis
Author: Haseeb Waqas
Description: 10 business queries on road safety SQLite database
"""

import sqlite3
import pandas as pd

DB = '../data/road_safety.db'
conn = sqlite3.connect(DB)

print("=" * 60)
print("STEP 2: SQL ANALYSIS")
print("Pakistan Road Safety Analysis (2008-2019)")
print("=" * 60)

queries = {
    "National KPIs": """
        SELECT
            SUM(Total_Accidents)                  AS Total_Accidents,
            SUM(Killed)                           AS Total_Killed,
            SUM(Injured)                          AS Total_Injured,
            ROUND(AVG(Fatality_Rate), 2)          AS Avg_Fatality_Rate_Pct,
            SUM(Vehicles_Involved)                AS Total_Vehicles_Involved
        FROM fact_accidents
        WHERE Province = 'Pakistan'
    """,
    "Deadliest Years": """
        SELECT Year, Total_Accidents, Killed, Fatality_Rate
        FROM fact_accidents
        WHERE Province = 'Pakistan'
        ORDER BY Killed DESC
        LIMIT 5
    """,
    "Province Total Accidents": """
        SELECT Province, Total_Accidents, Total_Killed,
               ROUND(Avg_Fatality_Rate, 2) AS Avg_Fatality_Rate
        FROM dim_province
        ORDER BY Total_Accidents DESC
    """,
    "Most Dangerous Province": """
        SELECT Province,
               ROUND(AVG(Fatality_Rate), 2) AS Avg_Fatality_Rate,
               SUM(Killed) AS Total_Killed
        FROM fact_accidents
        WHERE Province != 'Pakistan'
        GROUP BY Province
        ORDER BY Avg_Fatality_Rate DESC
    """,
    "Islamabad Trend": """
        SELECT Year, Total_Accidents, Killed, Injured, Fatality_Rate
        FROM fact_accidents
        WHERE Province = 'Islamabad'
        ORDER BY Year_Start
    """,
    "National Year on Year": """
        SELECT Year, Total_Accidents, Killed,
               ROUND(Fatality_Rate, 2) AS Fatality_Rate_Pct,
               Injured, Vehicles_Involved
        FROM fact_accidents
        WHERE Province = 'Pakistan'
        ORDER BY Year_Start
    """,
    "Best vs Worst Year per Province": """
        SELECT Province,
               MIN(Total_Accidents) AS Best_Year_Accidents,
               MAX(Total_Accidents) AS Worst_Year_Accidents,
               ROUND(MAX(Total_Accidents)*1.0/MIN(Total_Accidents), 2) AS Ratio
        FROM fact_accidents
        WHERE Province != 'Pakistan'
        GROUP BY Province
        ORDER BY Ratio DESC
    """,
    "Injury Rate by Province": """
        SELECT Province,
               ROUND(AVG(Injury_Rate), 2) AS Avg_Injury_Rate,
               SUM(Injured) AS Total_Injured
        FROM fact_accidents
        WHERE Province != 'Pakistan'
        GROUP BY Province
        ORDER BY Avg_Injury_Rate DESC
    """,
    "Vehicles per Accident Trend": """
        SELECT Year, Vehicles_Involved,
               ROUND(Vehicles_per_Accident, 3) AS Vehicles_per_Accident
        FROM fact_accidents
        WHERE Province = 'Pakistan'
        ORDER BY Year_Start
    """,
    "Islamabad vs National Fatality Rate": """
        SELECT i.Year,
               ROUND(i.Fatality_Rate, 2)  AS Islamabad_Rate,
               ROUND(p.Fatality_Rate, 2)  AS National_Rate,
               ROUND(i.Fatality_Rate - p.Fatality_Rate, 2) AS Difference
        FROM fact_accidents i
        JOIN fact_accidents p ON i.Year = p.Year
        WHERE i.Province = 'Islamabad'
          AND p.Province = 'Pakistan'
        ORDER BY i.Year_Start
    """
}

results = {}
for name, query in queries.items():
    print(f"\n📊 {name}:")
    result = pd.read_sql(query, conn)
    print(result.to_string(index=False))
    results[name] = result

with pd.ExcelWriter('../data/sql_analysis_results.xlsx', engine='openpyxl') as writer:
    for name, result in results.items():
        sheet_name = name[:31]
        result.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n✅ STEP 2 COMPLETE")
print(f"   SQL results exported: sql_analysis_results.xlsx (10 sheets)")
print(f"   Run step3_visualizations.py next")
conn.close()
