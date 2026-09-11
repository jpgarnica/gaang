record_5 = "BOOKER, TERRENCE | M | 41 | 2018-11-08 | 907 n. calloway drive | Beat 442 | OPEN"

#Step 1:

fields = record_5.strip().split(" | ")

#Step 2:

Name = fields[0].title()                 # Booker, Terrence 
sex = fields[1].upper()                  # M  
Name_sex = f"{Name} ({sex})"             # Booker, Terrence (M) This variable will help print the sex in parenthesis next to the name.
Age = int(fields[2])                     # 41
date = fields[3]                         # 2018-11-08
year = int(date[0:4])                    # 2018
address = fields[4].title()              # 907 N. Calloway Drive
status = fields[6]                       #  OPEN   

# SteP 3:

years_unsolved = 2026 - year             # 8

print(f"{'Name':<20}{'Age':<5}{'Years Unsolved':<5}")
print(f"{Name_sex:<20} {Age:<5}{years_unsolved:<5}")