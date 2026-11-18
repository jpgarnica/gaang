# src/casemap.py
# Week 10 lab: Operation The Picture. Run: python -m src.casemap
import pandas as pd   # bring in pandas, nicknamed pd
import folium         # folium draws Leaflet web maps and saves them as .html

# --- Step 1: load the WaPo Dallas cases (names were already dropped by get_data) ---
w = pd.read_csv("data/wapo_dallas.csv")

# a NaN lat or lon makes the whole map render blank, so drop those rows and say how many
before = len(w)
w = w.dropna(subset=["lat", "lon"])
print(f"dropped {before - len(w)} rows with no coordinates")   # 0 for the current file

# --- Step 2: a base map centered on downtown Dallas ---
# default OpenStreetMap tiles; the handout's "cartodbpositron" tiles now need an API key
m = folium.Map(location=[32.78, -96.80], zoom_start=11)

# --- Step 3: one dot per case, colored by arrest outcome ---
for _, row in w.iterrows():                    # _ = row number (unused), row = one case
    if row.disposition == "Open/No arrest":    # no arrest -> orange
        color = "orange"
    else:                                      # closed by arrest or without arrest -> green
        color = "green"
    folium.CircleMarker(
        location=[row.lat, row.lon],           # where the dot goes
        radius=3, color=color, fill=True, fill_opacity=0.6, weight=1,
    ).add_to(m)                                # put the dot on the map

# --- Step 4: legend, with the counts read from the data instead of typed in ---
n_open = (w.disposition == "Open/No arrest").sum()   # 676
n_closed = len(w) - n_open                           # 891 = 813 by arrest + 78 without
legend = f"""
<div style="position:fixed;bottom:30px;left:30px;background:white;padding:8px 12px;
border:1px solid #999;font-family:sans-serif;font-size:13px;z-index:9999">
<b>Dallas homicides 2007–2017</b><br>
<span style="color:orange">●</span> Open / no arrest ({n_open})<br>
<span style="color:green">●</span> Closed ({n_closed})<br>
Source: Washington Post Unsolved Homicide Database
</div>"""
m.get_root().html.add_child(folium.Element(legend))   # pin the legend onto the page

# --- Step 5: save the artifact ---
m.save("reports/dallas_map.html")
print(f"reports/dallas_map.html: {len(w)} markers")   # expect 1567
