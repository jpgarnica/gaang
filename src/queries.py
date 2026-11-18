# src/queries.py
# Week 11 lab: three questions for case.db. Run: python -m src.queries
# (run python -m src.fetch_city first, so data/case.db exists)
import sqlite3        # Python's built-in SQLite database
import pandas as pd   # read_sql runs a query and hands back a DataFrame

con = sqlite3.connect("data/case.db")   # open the database fetch_city.py built

# Q1: murders per service year. BETWEEN keeps out any garbage years (1011, 1429, ...)
q1 = """SELECT servyr AS year, COUNT(*) AS murders
        FROM incidents WHERE servyr BETWEEN 2014 AND 2026
        GROUP BY servyr ORDER BY servyr"""

# Q2: the 5 beats with the most murders since the feed began (June 2014)
q2 = """SELECT beat, COUNT(*) AS n FROM incidents
        WHERE beat IS NOT NULL GROUP BY beat ORDER BY n DESC LIMIT 5"""

# Q3, our squad's slice: what share of murders happen at a residence?
# Why this slice: killings at home are more often by someone the victim knows,
# and those cases clear more easily than street shootings. If the residence
# share moves over time, the case mix moved, and clearance can move with it.
# premise LIKE '%RESIDENCE%' is 1 (true) or 0 (false) per row, so SUM counts the matches
q3 = """SELECT ROUND(100.0 * SUM(premise LIKE '%RESIDENCE%') / COUNT(*), 1) AS pct_residence
        FROM incidents"""

for q in (q1, q2, q3):              # run each query and print its answer table
    print(pd.read_sql(q, con), "\n")

con.close()                         # done with the database
