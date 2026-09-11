# intake.py — turn one raw record into a clean summary
import datetime

record = "Nguyen, Daniel | m | 17 | 2018-04-03 | 2846 QUAIL RIDGE ROAD | beat 537 | Open"
fields = record.strip().split(" | ")
name = fields[0].title() # "Carter, Demarcus"
sex = fields[1].upper() # "M"
age = int(fields[2]) # 36 (now a number)
date = fields[3]
year = int(date[0:4]) # 2018
addr = fields[4].title() # "412 Larkmoor Lane"
status = fields[6]
current_year = datetime.date.today().year
years_unsolved = current_year - year
summary = f"CASE: {name} ({sex}, {age}) | {date} | {addr} | " \
f"{status} — {years_unsolved} years without an arrest"
print(summary)
