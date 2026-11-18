"""Fetch every murder incident from Dallas OpenData into data/case.db.
Run: python -m src.fetch_city"""
# Week 11 lab: Operation The Tap.
import json                     # read/write the raw JSON cache file
import os                       # read environment variables (the app token)
import sqlite3                  # Python's built-in SQLite database
from pathlib import Path        # Path lets us build file paths like data/case.db
import pandas as pd             # DataFrame -> SQL table
import requests                 # asks the city's API over the web
from dotenv import load_dotenv  # copies KEY=value lines from .env into os.environ

load_dotenv()                                  # must run BEFORE we read the token
token = os.environ.get("DALLAS_APP_TOKEN")     # your token, or None if .env has no token yet
url = "https://www.dallasopendata.com/resource/qv6i-rri7.json"   # Police Incidents API
where = "offincident like '%MURDER%' OR offincident = 'HOMICIDE'"   # the murder filter
raw = Path("data/raw_incidents.json")          # cache: the API's answer, saved untouched
db = Path("data/case.db")                      # the SQLite database file
page_size = 5000                               # rows per request ($limit)


def fetch_all() -> list[dict]:
    if raw.exists():                           # already fetched once?
        print("using cache", raw)              # then never hit the API again
        return json.loads(raw.read_text())     # load the saved list of dicts
    rows, offset = [], 0                       # all rows so far, and where the next page starts
    while True:
        r = requests.get(url, params={         # requests URL-encodes the quotes and % for us
            "$where": where,
            "$order": "incidentnum",           # stable order, so pages never repeat rows
            "$limit": page_size,               # one page = 5000 rows max
            "$offset": offset,                 # skip the rows we already have
            "$$app_token": token,              # a None value is left out of the URL entirely
        }, timeout=60)
        r.raise_for_status()                   # fail loudly on 400/429/500
        page = r.json()                        # JSON -> list of dicts
        rows.extend(page)                      # add this page to the pile
        print(f"offset {offset}: {len(page)} rows")
        if len(page) < page_size:              # a short page means we reached the end
            break
        offset += page_size                    # otherwise ask for the next page
    raw.write_text(json.dumps(rows))           # save the cache for every future run
    return rows


def flatten(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)                    # list of dicts -> table, one column per field
    geo = df.pop("geocoded_column")            # nested dict column; SQLite can't store dicts
    df["lat"] = geo.apply(lambda g: float(g["latitude"]) if isinstance(g, dict) else None)
    df["lon"] = geo.apply(lambda g: float(g["longitude"]) if isinstance(g, dict) else None)
    df = df[[c for c in df.columns if not c.startswith(":@")]]   # drop computed-region columns
    df["servyr"] = pd.to_numeric(df["servyr"], errors="coerce")  # "2022" (string) -> 2022
    return df


def main() -> None:
    if token is None:                          # remind, but still run (the API allows it, throttled)
        print("no DALLAS_APP_TOKEN in .env, fetching without one")
    df = flatten(fetch_all())
    con = sqlite3.connect(db)                  # open (or create) data/case.db
    df.to_sql("incidents", con, if_exists="replace", index=False)   # DataFrame -> SQL table
    n = pd.read_sql("SELECT COUNT(*) AS n FROM incidents", con).n[0]
    print(f"case.db: {n} rows in incidents")
    con.close()


if __name__ == "__main__":   # only run main() when this file is run directly
    main()
