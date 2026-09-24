# first_filter.py — Week 3: The First Filter
# Sweep all 50 records, flag stale open cases, and report the counts.

CURRENT_YEAR = 2026    # year we measure case age from
STALE_YEARS = 5        # cases this old or older are "stale"

# --- Step 1: set up accumulators BEFORE the loop ---
total_count = 0            # counts every valid record
open_count = 0             # counts OPEN cases
stale_count = 0            # counts OPEN cases 5+ years old
juvenile_open_count = 0    # counts OPEN cases with age under 18
oldest_year = CURRENT_YEAR # start high so any real year is older
oldest_name = ""           # name of the oldest open case (empty for now)

file = open("data/wk03_data_raw_cases_50.txt")   # open the data file for reading

# --- Step 2: walk every record and update INSIDE the loop ---
for line in file:                      # repeat once for each line in the file
    line = line.strip()                # remove spaces/newline from both ends
    if line == "":                     # is the line blank?
        continue                       # yes: skip to the next line

    fields = line.split("|")           # cut the line at each "|" into a list of 7 pieces
    if len(fields) != 7:               # does it NOT have exactly 7 pieces?
        continue                       # yes: junk line, skip it

    name = fields[0].strip().title()       # piece 0, trim spaces, "FUENTES, LAMAR" -> "Fuentes, Lamar"
    age = int(fields[2].strip())           # piece 2, trim spaces, turn text "31" into number 31
    year = int(fields[3].strip()[0:4])     # piece 3, take first 4 chars "1980" of the date, make it a number
    status = fields[6].strip().upper()     # piece 6, trim spaces, make ALL CAPS so "open" becomes "OPEN"

    years_unsolved = CURRENT_YEAR - year   # how many years old the case is
    total_count = total_count + 1          # add 1 to total (every record, open or closed)

    if status == "OPEN":                   # only do the rest for open cases
        open_count = open_count + 1        # add 1 to open count

        if years_unsolved >= STALE_YEARS:  # is this open case 5+ years old?
            stale_count = stale_count + 1  # yes: add 1 to stale count
            flag = "*** STALE ***"         # label to print next to the name
        else:                              # otherwise (less than 5 years old)
            flag = ""                      # no label

        if age < 18:                                       # is the victim under 18?
            juvenile_open_count = juvenile_open_count + 1  # yes: add 1 to juvenile count

        if year < oldest_year:             # is this case older than the oldest seen so far?
            oldest_year = year             # yes: save its year as the new oldest
            oldest_name = name             # and save its name

        print(f"{name:<22}{years_unsolved:>4} years  {flag}")   # print name (left, 22 wide), years (right, 4 wide), flag

file.close()   # close the file after the loop is done

# --- Step 3: report AFTER the loop ---
print()                                                      # blank line before the report
print(f"Total records:        {total_count}")                # total valid records
print(f"Open cases:           {open_count}")                 # number of open cases
print(f"Stale (>= {STALE_YEARS} yrs):     {stale_count}")    # number of stale open cases
print(f"Juvenile open cases:  {juvenile_open_count}")        # number of open juvenile cases
print(f"Oldest open case:     {oldest_name} ({oldest_year})")  # oldest open case name and year
