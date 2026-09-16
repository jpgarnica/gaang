record = " CARTER, DEMARCUS | m | 36 | 2018-03-22 | 412 larkmoor lane | beat 352 | OPEN "
fields = record.strip().split(" | ")
name = fields[0].title() # "Carter, Demarcus"
sex = fields[1].upper() # "M"
age = int(fields[2]) # 36
date = fields[3]
year = int(date[0:4]) # 2018
addr = fields[4].title() # "412 Larkmoor Lane"
status = fields[6]

years_unsolved = 2026 - year
summary = f"CASE: {name} ({sex}, {age}) | {date} | {addr} | " \
f"{status} — {years_unsolved} years without an arrest"
print(summary)