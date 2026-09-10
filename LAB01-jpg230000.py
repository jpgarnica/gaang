record_3 = "  OKAFOR, SAMUEL J | M | 55 | 2018-07-09 | 1519 westhollow avenue | beat 341 | OPEN"

fields_3 = record_3.strip().split(" | ")

name_3   = fields_3[0].title()   # "Okafor, Samuel J"
sex_3    = fields_3[1].upper()   # "M"
age_3    = int(fields_3[2])      # 55 made integer
date_3   = fields_3[3]           # no change
year_3   = int(date_3[0:4])      # 2018 made integer
addr_3   = fields_3[4].title()   # "1519 Westhollow Avenue"
beat_3   = fields_3[5]           # no change
status_3 = fields_3[6].upper()   # "OPEN"

years_unsolved_3 = 2026 - year_3 

case_3 = f"{name_3} ({sex_3})"     
print(f"{case_3:<26}{age_3:>5}{years_unsolved_3:>18}")