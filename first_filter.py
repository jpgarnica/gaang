# first_filter.py - ITSS/OPRE 3312 Week 3 - Operation: First Filter

STALE_YEARS = 5                            # an open case this old or older is STALE

total_records = 0                          # counter: how many records we read
open_count = 0                             # counter: records with status OPEN
stale_count = 0                            # counter: open AND 5+ years old
juvenile_count = 0                         # counter: open cases with age under 18
oldest_year = 2026                         # start HIGH so the first real year beats it
oldest_name = ""                           # the name that goes with oldest_year

case_file = open("wk03_data_raw_cases_50.txt")   # connect to the evidence file
records = case_file.readlines()            # read it into a list, one string per line
case_file.close()                          # done reading, let the file go

for line in records:                       # run the block below once per record
    line = line.strip()                    # .strip() = shave whitespace off both ends

    if line == "":                         # blank line? (strip first, or it is "\n")
        continue                           # skip it, keep looping

    fields = line.split("|")               # .split("|") = chop at each pipe -> 7 pieces

    name = fields[0].strip().title()       # .title() = "OKAFOR, DARIUS" -> "Okafor, Darius"
    age = int(fields[2].strip())           # int() = text "16" -> number 16
    year = int(fields[3].strip()[0:4])     # [0:4] = "2017-07-20" -> "2017" -> 2017
    status = fields[6].strip().upper()     # .upper(): 'open' == 'OPEN' is False, so standardize

    years_unsolved = 2026 - year           # 2026 - 2017 = 9 years unsolved
    total_records = total_records + 1      # old count + 1, stored back

    if years_unsolved >= STALE_YEARS:      # Python takes the FIRST true branch
        flag = "*** STALE ***"             # 5+ years
    elif years_unsolved >= 2:              # only asked if the test above was False
        flag = "aging"                     # 2 to 4 years
    else:                                  # everything left over
        flag = "recent"                    # 0 or 1 years

    if status == "OPEN":                   # == asks a question, = would assign
        open_count = open_count + 1        # count this open case

        if years_unsolved >= STALE_YEARS:  # separate if, not elif - it can be both
            stale_count = stale_count + 1  # open AND stale

        if age < 18:                       # under 18, so 18 does not count
            juvenile_count = juvenile_count + 1

        if year < oldest_year:             # earlier than our current oldest?
            oldest_year = year             # new oldest year
            oldest_name = name             # and the name that goes with it

        print(f"{name}: {years_unsolved} years {flag}")   # f"" swaps in the {values}

print()                                    # blank line before the report
print(f"Total records:        {total_records}")      # expect 50
print(f"Open cases:           {open_count}")         # expect 29
print(f"Stale (>= 5 yrs):     {stale_count}")        # expect 27
print(f"Juveniles (age < 18): {juvenile_count}")     # expect 1
print(f"Oldest open case:     {oldest_name} ({oldest_year})")   # expect Fuentes, Lamar (1980)
