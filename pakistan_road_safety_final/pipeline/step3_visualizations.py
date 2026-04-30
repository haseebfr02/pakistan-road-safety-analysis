"""
Pakistan Road Safety Analysis
Step 3: Visualizations
Author: Haseeb Waqas
Description: 10 professional charts for Pakistan Road Safety
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

# ── Colors ────────────────────────────────────────────────────
NAVY   = '#1E3A5F'
RED    = '#E74C3C'
GREEN  = '#2ECC71'
ORANGE = '#F39C12'
BLUE   = '#3498DB'
PURPLE = '#9B59B6'
BG     = '#F8F9FA'

PROVINCE_COLORS = {
    'Punjab':              '#3498DB',
    'Khyber Pakhtunkhwa':  '#2ECC71',
    'Sindh':               '#E74C3C',
    'Balochistan':         '#F39C12',
    'Islamabad':           '#9B59B6',
}

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor':   BG,
    'axes.grid':        True,
    'grid.color':       '#E0E0E0',
    'grid.linewidth':   0.8,
    'axes.spines.top':  False,
    'axes.spines.right':False,
})

VISUALS = '../visuals/'
os.makedirs(VISUALS, exist_ok=True)

# ── Load Data ─────────────────────────────────────────────────
df        = pd.read_csv('../data/road_safety_cleaned.csv')
national  = df[df['Province'] == 'Pakistan'].sort_values('Year_Start').reset_index(drop=True)
provinces = df[df['Province'] != 'Pakistan'].copy()
islamabad = df[df['Province'] == 'Islamabad'].sort_values('Year_Start').reset_index(drop=True)
nat_total = national.sum(numeric_only=True)

print("Generating visualizations...")

# ── Chart 1: National Trend ───────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
ax1.fill_between(range(len(national)), national['Total_Accidents'], alpha=0.2, color=BLUE)
ax1.plot(range(len(national)), national['Total_Accidents'],
         color=BLUE, linewidth=2.5, marker='o', markersize=7, label='Total Accidents')
ax2.plot(range(len(national)), national['Killed'],
         color=RED, linewidth=2.5, marker='s', markersize=7, linestyle='--', label='Killed')
ax1.set_xticks(range(len(national)))
ax1.set_xticklabels(national['Year'], rotation=30, ha='right', fontsize=9)
ax1.set_title('Pakistan Road Accidents & Fatalities (2008–2019)',
              fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax1.set_ylabel('Total Accidents', color=BLUE, fontsize=11)
ax2.set_ylabel('People Killed', color=RED, fontsize=11)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, fontsize=10, loc='upper left')
plt.tight_layout()
plt.savefig(f'{VISUALS}01 national trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 01 national trend.png")

# ── Chart 2: Province Comparison ─────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
prov_total = provinces.groupby('Province')['Total_Accidents'].sum().sort_values(ascending=True)
colors = [PROVINCE_COLORS[p] for p in prov_total.index]
bars = ax.barh(prov_total.index, prov_total.values, color=colors, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, prov_total.values):
    ax.text(val+100, bar.get_y()+bar.get_height()/2,
            f'{val:,}', va='center', fontsize=11, fontweight='bold')
ax.set_title('Total Road Accidents by Province (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Total Accidents', fontsize=11)
plt.tight_layout()
plt.savefig(f'{VISUALS}02 province comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 02 province comparison.png")

# ── Chart 3: Fatality Rate by Province ───────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
prov_fat = provinces.groupby('Province')['Fatality_Rate'].mean().sort_values(ascending=True)
colors = [RED if v>60 else ORANGE if v>50 else GREEN for v in prov_fat.values]
bars = ax.barh(prov_fat.index, prov_fat.values, color=colors, edgecolor='white', linewidth=1.5)
ax.axvline(prov_fat.mean(), color=NAVY, linestyle='--', linewidth=2,
           label=f'Average: {prov_fat.mean():.1f}%')
for bar, val in zip(bars, prov_fat.values):
    ax.text(val+0.3, bar.get_y()+bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=11, fontweight='bold')
ax.set_title('Average Fatality Rate by Province (%)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Fatality Rate (%)', fontsize=11)
high = mpatches.Patch(color=RED, label='>60% High')
mid  = mpatches.Patch(color=ORANGE, label='50-60% Medium')
low  = mpatches.Patch(color=GREEN, label='<50% Lower')
ax.legend(handles=[high, mid, low], fontsize=9, loc='lower right')
plt.tight_layout()
plt.savefig(f'{VISUALS}03 fatality rate by province.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 03 fatality rate by province.png")

# ── Chart 4: Islamabad Deep Dive ─────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(range(len(islamabad)), islamabad['Total_Accidents'],
             color=PURPLE, linewidth=2.5, marker='o', markersize=8)
axes[0].fill_between(range(len(islamabad)), islamabad['Total_Accidents'], alpha=0.2, color=PURPLE)
for i, y in enumerate(islamabad['Total_Accidents']):
    axes[0].annotate(str(y), (i, y), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=9, fontweight='bold')
axes[0].set_xticks(range(len(islamabad)))
axes[0].set_xticklabels(islamabad['Year'], rotation=30, ha='right', fontsize=8)
axes[0].set_title('Islamabad — Total Accidents per Year',
                  fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_ylabel('Accidents')

nat_avg = national['Fatality_Rate'].mean()
axes[1].plot(range(len(islamabad)), islamabad['Fatality_Rate'],
             color=RED, linewidth=2.5, marker='s', markersize=8)
axes[1].fill_between(range(len(islamabad)), islamabad['Fatality_Rate'], alpha=0.15, color=RED)
axes[1].axhline(nat_avg, color=NAVY, linestyle='--', linewidth=1.5,
                label=f'National Avg: {nat_avg:.1f}%')
for i, y in enumerate(islamabad['Fatality_Rate']):
    axes[1].annotate(f'{y:.1f}%', (i, y), textcoords='offset points',
                     xytext=(0, 8), ha='center', fontsize=9, fontweight='bold')
axes[1].set_xticks(range(len(islamabad)))
axes[1].set_xticklabels(islamabad['Year'], rotation=30, ha='right', fontsize=8)
axes[1].set_title('Islamabad — Fatality Rate vs National Average',
                  fontsize=12, fontweight='bold', color=NAVY)
axes[1].set_ylabel('Fatality Rate (%)')
axes[1].legend(fontsize=9)
fig.suptitle('Islamabad Road Safety Deep Dive (2012–2019)',
             fontsize=14, fontweight='bold', color=NAVY)
plt.tight_layout()
plt.savefig(f'{VISUALS}04 islamabad deep dive.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 04 islamabad deep dive.png")

# ── Chart 5: Province Trends ──────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
for prov, color in PROVINCE_COLORS.items():
    pdata = provinces[provinces['Province'] == prov].sort_values('Year_Start')
    ax.plot(pdata['Year_Start'], pdata['Total_Accidents'],
            color=color, linewidth=2, marker='o', markersize=5, label=prov)
ax.set_title('Road Accidents Trend by Province (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Year'); ax.set_ylabel('Total Accidents')
ax.legend(fontsize=10, loc='upper left')
plt.tight_layout()
plt.savefig(f'{VISUALS}05 province trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 05 province trends.png")

# ── Chart 6: Killed vs Injured ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
x = range(len(national))
ax.bar(x, national['Killed'], label='Killed', color=RED, alpha=0.85)
ax.bar(x, national['Injured'], bottom=national['Killed'], label='Injured', color=ORANGE, alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(national['Year'], rotation=30, ha='right', fontsize=9)
ax.set_title('Casualties: Killed vs Injured — National (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_ylabel('Number of People')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f'{VISUALS}06 killed vs injured.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 06 killed vs injured.png")

# ── Chart 7: Fatality Rate Trend ─────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(range(len(national)), national['Fatality_Rate'],
        color=RED, linewidth=2.5, marker='o', markersize=8)
ax.fill_between(range(len(national)), national['Fatality_Rate'],
                national['Fatality_Rate'].min()-1, alpha=0.15, color=RED)
ax.axhline(national['Fatality_Rate'].mean(), color=NAVY, linestyle='--',
           linewidth=1.5, label=f"Average: {national['Fatality_Rate'].mean():.1f}%")
for i, y in enumerate(national['Fatality_Rate']):
    ax.annotate(f'{y:.1f}%', (i, y), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')
ax.set_xticks(range(len(national)))
ax.set_xticklabels(national['Year'], rotation=30, ha='right', fontsize=9)
ax.set_title('National Fatality Rate Trend (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_ylabel('Fatality Rate (%)')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(f'{VISUALS}07 fatality rate trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 07 fatality rate trend.png")

# ── Chart 8: Severity Funnel ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
stages = [
    ('Total Accidents', int(nat_total['Total_Accidents']), BLUE),
    ('Fatal Accidents', int(nat_total['Fatal_Accidents']), ORANGE),
    ('People Killed',   int(nat_total['Killed']),          RED),
    ('People Injured',  int(nat_total['Injured']),         '#E67E22'),
]
max_val = stages[0][1]
for i, (label, value, color) in enumerate(stages):
    width = value / max_val
    left  = (1 - width) / 2
    ax.barh(i, width, left=left, height=0.6, color=color,
            alpha=0.85, edgecolor='white', linewidth=2)
    ax.text(0.5, i, f'{label}:  {value:,}',
            ha='center', va='center', fontsize=12,
            fontweight='bold', color='white',
            transform=ax.get_yaxis_transform())
    ax.text(left+width+0.01, i, f'{value/max_val*100:.1f}%',
            va='center', fontsize=11, color=color, fontweight='bold')
ax.set_xlim(0, 1.15)
ax.set_ylim(-0.5, len(stages)-0.5)
ax.set_yticks([]); ax.set_xticks([])
ax.set_title('Pakistan Road Safety — Severity Funnel (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
for spine in ax.spines.values(): spine.set_visible(False)
ax.grid(False)
plt.tight_layout()
plt.savefig(f'{VISUALS}08 severity funnel.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 08 severity funnel.png")

# ── Chart 9: Vehicles per Accident ───────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(range(len(national)), national['Vehicles_per_Accident'],
        color=BLUE, linewidth=2.5, marker='D', markersize=8)
ax.fill_between(range(len(national)), national['Vehicles_per_Accident'],
                national['Vehicles_per_Accident'].min()-0.01,
                alpha=0.15, color=BLUE)
for i, y in enumerate(national['Vehicles_per_Accident']):
    ax.annotate(f'{y:.3f}', (i, y), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9)
ax.set_xticks(range(len(national)))
ax.set_xticklabels(national['Year'], rotation=30, ha='right', fontsize=9)
ax.set_title('Average Vehicles Involved per Accident (2008–2019)',
             fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.set_ylabel('Vehicles per Accident')
plt.tight_layout()
plt.savefig(f'{VISUALS}09 vehicles per accident.png', dpi=150, bbox_inches='tight')
plt.close()
print("   ✅ 09 vehicles per accident.png")

# ── Chart 10: Executive Dashboard ────────────────────────────
fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor('#1A1A2E')
fig.suptitle('Pakistan Road Safety Analysis 2008–2019 | Haseeb Waqas',
             fontsize=20, fontweight='bold', color='white', y=0.98)

kpis = [
    ('Total Accidents',   f"{int(nat_total['Total_Accidents']):,}", '#3498DB'),
    ('Total Killed',      f"{int(nat_total['Killed']):,}",          '#E74C3C'),
    ('Total Injured',     f"{int(nat_total['Injured']):,}",         '#F39C12'),
    ('Avg Fatality Rate', f"{national['Fatality_Rate'].mean():.1f}%", '#9B59B6'),
]
for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_axes([0.03+i*0.245, 0.82, 0.22, 0.12])
    ax.set_facecolor(color)
    ax.text(0.5, 0.60, value, ha='center', va='center', fontsize=22,
            fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.20, label, ha='center', va='center', fontsize=10,
            color='white', alpha=0.85, transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)

ax1 = fig.add_axes([0.04, 0.44, 0.44, 0.34])
ax1.set_facecolor('#16213E')
ax1.plot(range(len(national)), national['Total_Accidents'],
         color='#3498DB', linewidth=2, marker='o', markersize=5, label='Accidents')
ax1.plot(range(len(national)), national['Killed'],
         color='#E74C3C', linewidth=2, marker='s', markersize=5,
         linestyle='--', label='Killed')
ax1.set_title('National Trend: Accidents & Fatalities',
              color='white', fontsize=12, fontweight='bold')
ax1.set_xticks(range(len(national)))
ax1.set_xticklabels(national['Year'].str[:4], rotation=45, color='white', fontsize=8)
ax1.tick_params(colors='white')
ax1.legend(fontsize=9)
ax1.grid(color='#333366', linewidth=0.5)
for spine in ax1.spines.values(): spine.set_color('#333366')

ax2 = fig.add_axes([0.54, 0.44, 0.44, 0.34])
ax2.set_facecolor('#16213E')
pdata = provinces.groupby('Province')['Total_Accidents'].sum().sort_values()
colors2 = [PROVINCE_COLORS[p] for p in pdata.index]
ax2.barh(range(len(pdata)), pdata.values, color=colors2, edgecolor='none')
ax2.set_yticks(range(len(pdata)))
ax2.set_yticklabels(pdata.index, color='white', fontsize=10)
ax2.tick_params(colors='white')
ax2.set_title('Total Accidents by Province',
              color='white', fontsize=12, fontweight='bold')
ax2.grid(color='#333366', linewidth=0.5)
for spine in ax2.spines.values(): spine.set_color('#333366')

ax3 = fig.add_axes([0.04, 0.02, 0.92, 0.34])
ax3.set_facecolor('#16213E')
ax3.set_xticks([]); ax3.set_yticks([])
for spine in ax3.spines.values(): spine.set_color('#333366')
insights = [
    "📌 REC 1: Sindh has highest fatality rate (78.85%) — urgent road safety interventions needed in Karachi urban routes.",
    "📌 REC 2: Accidents peaked in 2017-18 (11,121) — correlates with vehicle registration surge. Enforce stricter licensing.",
    "📌 REC 3: Islamabad fatality rate (56.64%) exceeds national avg in 5 of 7 years — traffic law enforcement must improve.",
    "📌 REC 4: KPK injury rate is highest (137.64 per 100 accidents) — emergency response infrastructure needs urgent investment.",
]
ax3.text(0.5, 0.93, '💡 Key Findings & Policy Recommendations',
         ha='center', va='top', fontsize=13, fontweight='bold',
         color='#F39C12', transform=ax3.transAxes)
for i, ins in enumerate(insights):
    ax3.text(0.02, 0.77-i*0.20, ins, ha='left', va='top',
             fontsize=10, color='white', transform=ax3.transAxes)

plt.savefig(f'{VISUALS}00 executive dashboard.png', dpi=150,
            bbox_inches='tight', facecolor='#1A1A2E')
plt.close()
print("   ✅ 00 executive dashboard.png")
print(f"\n✅ STEP 3 COMPLETE — All 10 visuals generated in visuals/")
