# src/charts.py
# Week 10 lab: Operation The Picture. Run: python -m src.charts
import pandas as pd               # bring in pandas, nicknamed pd
import matplotlib.pyplot as plt   # bring in matplotlib's plotting module, nicknamed plt

# --- Step 1: load the week 9 series ---
s = pd.read_csv("reports/dallas_series.csv")   # year, reported, cleared, clearance
s["pct"] = s.clearance * 100                   # 0.94 -> 94.0, so the axis reads in percent

# --- Step 2: break gaps instead of bridging them ---
# reindex to every year 1965-2025; a missing year becomes a NaN row,
# and matplotlib leaves a visible break in the line at NaN
full = s.set_index("year").reindex(range(1965, 2026))

# --- Step 3: draw the chart ---
fig, ax = plt.subplots(figsize=(10, 5))                          # one chart, 10 x 5 inches
ax.plot(full.index, full.pct, marker="o", markersize=3, linewidth=1.5)   # the clearance line

ax.set_ylim(0, 100)   # honesty check: rates get the full 0-100 axis, never a zoomed one
ax.set_xlabel("Year")
ax.set_ylabel("Homicide clearance (%)\nSource: FBI UCR via Murder Accountability Project")
ax.set_title("Dallas Police Department homicide clearance rate, 1965–2025")
ax.grid(alpha=0.3)    # faint grid lines so readers can trace values

# --- Step 4: annotate our #1 suspicious year (from week 9) ---
yr = 2017                                         # the year we flagged first
val = float(s.loc[s.year == yr, "pct"].iloc[0])   # its clearance %, as a plain number
ax.annotate(f"{yr}: {val:.0f}% — reporting change?",   # the label text
            xy=(yr, val),                              # where the arrow points
            xytext=(yr - 12, val + 8),                 # where the text sits
            arrowprops=dict(arrowstyle="->"))          # draw an arrow from text to point

# --- Step 5: mark the partial year so nobody reads it as final ---
last = float(s.loc[s.year == 2025, "pct"].iloc[0])   # 2025's clearance %
ax.annotate("2025: partial year",
            xy=(2025, last),
            xytext=(2010, last - 25),
            arrowprops=dict(arrowstyle="->"))

# --- Step 6: save the artifact ---
fig.tight_layout()                                        # stop labels being clipped
fig.savefig("reports/clearance_trend.png", dpi=150)       # 150 dpi = sharp enough to publish
