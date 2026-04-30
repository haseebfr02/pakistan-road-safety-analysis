"""
Pakistan Road Safety Analysis
Step 1: ETL Pipeline
Author: Haseeb Waqas
Description: Extract raw government data, clean, engineer features, load to SQLite
"""

import pandas as pd
import numpy as np
import sqlite3
import os

RAW = '../data/traffic_accidents_raw.csv'
DB  = '../data/road_safety.db'

print("=" * 60)
print("STEP 1: ETL PIPELINE")
print("Pakistan Road Safety Analysis (2008-2019)")
print("=" * 60)

# ── EXTRACT ───────────────────────────────────────────────────
print("\n── EXTRACT ──")

df = pd.DataFrame({
    'Province': (
        ['Pakistan'] * 11 +
        ['Punjab'] * 11 +
        ['Sindh'] * 11 +
        ['Khyber Pakhtunkhwa'] * 11 +
        ['Balochistan'] * 11 +
        ['Islamabad'] * 7
    ),
    'Year': (
        ['2008-09','2009-10','2010-11','2011-12','2012-13',
         '2013-14','2014-15','2015-16','2016-17','2017-18','2018-19'] * 5 +
        ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19']
    ),
    'Total_Accidents': [
        9496,9747,9723,9140,8988,8359,7865,9100,9582,11121,10779,
        5240,5344,5420,4990,4587,3696,3054,3288,3819,5093,4823,
        1433,1465,1270,1054,935,945,881,924,880,848,972,
        2392,2559,2722,2772,2968,3120,3399,4287,4256,4425,4337,
        431,379,311,324,297,342,315,357,401,496,409,
        201,256,216,244,226,259,238
    ],
    'Fatal_Accidents': [
        4145,4378,4280,3966,3884,3500,3214,3591,4036,4829,4878,
        2471,2590,2591,2361,2213,1717,1435,1576,1989,2708,2808,
        824,883,758,681,582,613,583,634,608,586,620,
        644,712,773,785,846,877,942,1083,1103,1119,1097,
        206,193,158,139,136,173,147,178,209,259,226,
        107,120,107,120,127,157,127
    ],
    'Non_Fatal_Accidents': [
        5351,5369,5443,5174,5104,4859,4651,5509,5546,6292,5901,
        2769,2754,2829,2629,2374,1979,1619,1712,1830,2385,2015,
        609,582,512,373,353,332,298,290,272,262,352,
        1748,1847,1949,1987,2122,2243,2457,3204,3153,3306,3240,
        225,186,153,185,161,169,168,179,192,237,183,
        94,136,109,124,99,102,111
    ],
    'Killed': [
        4907,5280,5271,4758,4719,4348,3954,4448,5047,5948,5932,
        2912,3083,3167,2888,2692,2145,1750,2053,2494,3371,3423,
        961,1031,927,756,696,791,771,749,786,802,725,
        786,921,986,953,1059,1033,1137,1299,1317,1295,1318,
        248,245,191,161,163,247,178,207,321,313,330,
        109,132,118,140,129,167,136
    ],
    'Injured': [
        11037,11173,11383,10145,9710,9777,9661,11544,12696,14489,13219,
        5790,5856,5809,5071,4515,3941,3652,4550,5231,6772,5916,
        1160,1261,1071,681,637,893,863,754,970,838,829,
        3340,3560,4153,3913,4016,4257,4524,5527,5804,6093,5798,
        747,496,350,480,362,480,440,504,567,624,542,
        180,206,182,209,124,162,134
    ],
    'Vehicles_Involved': [
        10322,10496,10822,9986,9876,9423,8949,10636,11317,13134,12908,
        5240,5344,5420,4990,4587,3696,3054,3288,3819,5093,4823,
        1562,1580,1541,1121,960,1103,1029,1144,1009,1015,1142,
        2975,3128,3479,3501,3736,3934,4260,5490,5736,6052,6062,
        545,444,382,374,381,434,389,470,537,715,642,
        212,256,217,244,216,259,239
    ]
})

print(f"   Rows extracted  : {len(df)}")
print(f"   Provinces       : {list(df['Province'].unique())}")

# ── TRANSFORM ─────────────────────────────────────────────────
print("\n── TRANSFORM ──")

df['Year_Start']   = df['Year'].str[:4].astype(int)
df['Fatality_Rate']         = (df['Killed'] / df['Total_Accidents'] * 100).round(2)
df['Fatal_Pct']             = (df['Fatal_Accidents'] / df['Total_Accidents'] * 100).round(2)
df['Injury_Rate']           = (df['Injured'] / df['Total_Accidents'] * 100).round(2)
df['Killed_per_Accident']   = (df['Killed'] / df['Fatal_Accidents']).round(3)
df['Vehicles_per_Accident'] = (df['Vehicles_Involved'] / df['Total_Accidents']).round(3)

df['Severity'] = pd.cut(
    df['Fatality_Rate'],
    bins=[0, 40, 55, 70, 100],
    labels=['Low', 'Medium', 'High', 'Critical']
)

print(f"   Features added  : Fatality_Rate, Fatal_Pct, Injury_Rate, Severity")
print(f"   Year range      : {df['Year_Start'].min()} to {df['Year_Start'].max()}")

# ── LOAD ──────────────────────────────────────────────────────
print("\n── LOAD ──")

conn = sqlite3.connect(DB)

df.to_sql('fact_accidents', conn, if_exists='replace', index=False)
print(f"   fact_accidents  : {len(df)} rows ✅")

prov_dim = df[df['Province'] != 'Pakistan'].groupby('Province').agg(
    Total_Accidents=('Total_Accidents','sum'),
    Total_Killed=('Killed','sum'),
    Total_Injured=('Injured','sum'),
    Avg_Fatality_Rate=('Fatality_Rate','mean'),
    Years_Recorded=('Year','count')
).reset_index().round(2)
prov_dim.to_sql('dim_province', conn, if_exists='replace', index=False)
print(f"   dim_province    : {len(prov_dim)} provinces ✅")

national = df[df['Province'] == 'Pakistan'].copy()
national.to_sql('dim_national', conn, if_exists='replace', index=False)
print(f"   dim_national    : {len(national)} years ✅")

conn.close()

df.to_csv('../data/road_safety_cleaned.csv', index=False)
print(f"\n✅ STEP 1 COMPLETE")
print(f"   Exported: road_safety_cleaned.csv ({len(df)} rows)")
print(f"   Database: road_safety.db (3 tables)")
print(f"   Run step2_sql_analysis.py next")
