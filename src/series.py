# src/series.py
# Week 9 lab: Operation First Cut. Run: python -m src.series
import pandas as pd   # bring in pandas, nicknamed pd

# --- Step 1: load the file and look at it first (shape -> columns -> head) ---
df = pd.read_csv("data/map_ucr.csv")   # load the whole FBI archive into a DataFrame
print(df.shape)                        # (rows, columns) -> (186519, 9)
print(df.columns.tolist())             # the real column names: YEAR, MRD, CLR...
print(df.head())                       # eyeball the first 5 rows

# --- Step 2: filter to Dallas PD by ORI, not by name ---
dallas = df[df["ORI"] == "TXDPD00"]    # keep only rows where ORI is Dallas PD
print("Dallas PD rows:", len(dallas))  # confirm the count: should be 61

# --- Step 3: groupby year -> reported, cleared, clearance rate ---
per_year = dallas.groupby("YEAR").agg(   # one bucket per year
    reported=("MRD", "sum"),             # new column: add up murders reported
    cleared=("CLR", "sum"),              # new column: add up murders cleared
)
per_year["clearance"] = per_year["cleared"] / per_year["reported"]   # the rate
per_year.index.name = "year"                  # lowercase name for the CSV header
per_year.to_csv("reports/dallas_series.csv")  # write the deliverable

# --- Step 4: the three mandatory sanity checks ---
# 1. rates over 100%
print(per_year[per_year.clearance > 1])

# 2. missing years
years = set(per_year.index)                     # the years we actually have
print(sorted(set(range(1965, 2026)) - years))   # every year we should have, minus those

# 3. biggest year-over-year jumps in clearance
print(per_year.clearance.diff().abs().sort_values(ascending=False).head(5))

# --- Step 5: the 5 most suspicious years, one line of reasoning each ---
print("5 most suspicious years:")
print("2017 - clearance jumps from 50% to 80% in one year, the 2nd biggest jump in the series")
print("2018 - clearance drops from 80% to 40% the next year, the biggest jump in the series")
print("2007 - clearance falls from 81% to 58%, the start of the 2007-2011 slide")
print("1974 - clearance falls from 90% to 69%, then bounces back to 89% in 1975")
print("2025 - partial year, still being reported, so the numbers will change")
