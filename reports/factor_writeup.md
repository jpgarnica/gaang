# Factor writeup — Squad gaang

## Hypothesis (as locked at standup)
We hypothesize that DFW unemployment is associated with Dallas homicide clearance, in the negative direction (higher unemployment, lower clearance).

## Data
Clearance: reports/dallas_series.csv (FBI UCR via MAP), years 1990–2025. "Cleared" is the FBI definition: arrest or exceptional means.
Factor: unemployment rate, Dallas–Fort Worth–Arlington MSA, annual average, not seasonally adjusted (FRED series `LAUMT481910000000003A`) from https://fred.stlouisfed.org/series/LAUMT481910000000003A, downloaded 2026-11-17 by `src/factor.py`. One row per year, 36 rows after merge.

## Result
clearance ~ unemployment: coef = +0.0197, p = 0.100, R² = 0.078 (n = 36)
Lag-1 variant: coef = +0.0239, p = 0.048, R² = 0.113 (n = 35)

Read in plain terms: each 1-point rise in the DFW unemployment rate goes with about 2.0 percentage points *higher* clearance the same year (2.4 points the following year). Both signs are the opposite of what we pre-registered. The primary model does not clear p < 0.05. The lag-1 variant barely does (0.048), but it is the second specification we ran and it points against our hypothesis, so we do not treat it as a finding. R² says unemployment accounts for about 8 to 11 percent of the year-to-year variation in clearance.

## Two named confounders
1. **The long downward drift in clearance.** Dallas clearance falls from about 70–78% in the early 1990s to about 40–60% after 2015. DFW unemployment was highest in the early 1990s (7.0% in 1992) and mostly lower afterward, apart from the 2009–2011 and 2020 spikes. Anything else that changed slowly over these 35 years (forensic backlogs, witness cooperation, case mix, how DPD reports clearances to the FBI) lines up with "early years" in the same way unemployment does. The positive coefficient may only be saying "the 1990s cleared more cases and also had higher unemployment," not that unemployment does anything. A year trend term would test this, but adding it after seeing the result is a new specification, so we name it here and do not run it.
2. **Homicide caseload.** Crime waves move the economy story and the detective workload at the same time. A year with more homicides per detective can lower clearance regardless of unemployment, and caseload is not in our model. Our own series shows how large this swings: 500 reported murders in 1991 versus 116 in 2014.

Also worth stating: 2025 is a partial year in the FBI series and is included in the regression. The 2017–2018 jump and drop that we flagged in week 9 are also in the window, and if those are reporting artifacts, they add noise that no economic factor can explain.

## Verdict
Over 1990–2025, DFW unemployment is not detectably associated with Dallas homicide clearance in the negative direction we hypothesized. The point estimate is positive and not significant (p = 0.100). We do not claim causation because the model has one variable, 36 yearly observations, and at least two named confounders (the long-run decline and homicide caseload) that move with both series.
