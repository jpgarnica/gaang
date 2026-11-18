# src/factor.py
# Week 12 lab: Operation The Factor. Run: python -m src.factor
# Pre-registered hypothesis: DFW unemployment is associated with Dallas homicide
# clearance, in the negative direction (higher unemployment, lower clearance).
from pathlib import Path                 # Path lets us check whether the cache file exists
import pandas as pd                      # bring in pandas, nicknamed pd
import requests                          # downloads the FRED file
import statsmodels.formula.api as smf    # OLS regression written as a formula string

# FRED series LAUMT481910000000003A = unemployment rate, Dallas-Fort Worth-Arlington MSA,
# annual, not seasonally adjusted, 1990-. FRED's CSV download needs no API key.
fred_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=LAUMT481910000000003A"
factor_file = Path("data/dfw_unemployment.csv")   # our cleaned one-row-per-year factor


# --- Step 1: get the factor and wrangle it to one row per year (cached) ---
def get_unemployment() -> pd.DataFrame:
    if factor_file.exists():                       # already downloaded?
        print("using cache", factor_file)
        return pd.read_csv(factor_file)
    r = requests.get(fred_url, timeout=60)
    r.raise_for_status()                           # fail loudly if FRED is down
    raw = Path("data/fred_raw.csv")
    raw.write_bytes(r.content)                     # keep FRED's file untouched
    df = pd.read_csv(raw)                          # columns: observation_date, LAUMT4819...
    df["year"] = df.observation_date.str[:4].astype(int)   # "1990-01-01" -> 1990 (an int)
    # FRED writes a missing value as ".", so coerce turns it into NaN instead of crashing
    df["unemployment"] = pd.to_numeric(df["LAUMT481910000000003A"], errors="coerce")
    df = df[["year", "unemployment"]]              # keep just the two columns we merge on
    df.to_csv(factor_file, index=False)
    print(f"saved: {factor_file} ({len(df)} rows)")
    return df


series = pd.read_csv("reports/dallas_series.csv")   # year, reported, cleared, clearance
factor = get_unemployment()                         # year, unemployment

# --- Step 2: merge on year, then LOOK before modeling ---
# inner = keep only years both files have (1990-2025). year is an int in both frames.
merged = series.merge(factor, on="year", how="inner").sort_values("year")
print(merged.shape)
print(merged.head())

# --- Step 3: the pre-registered regression ---
m1 = smf.ols("clearance ~ unemployment", data=merged).fit()
print(m1.summary())

# --- Step 4: lag-1 variant: does LAST year's unemployment go with THIS year's clearance? ---
merged["unemployment_lag1"] = merged.unemployment.shift(1)   # move each value down one year
m2 = smf.ols("clearance ~ unemployment_lag1", data=merged.dropna()).fit()   # 1990 has no lag
print(m2.summary())
