# first_filter.py — Week 3: Operation First Filter
# Sweeps all 50 case records, flags the open ones, reports the counts.

DATA_FILE = "wk03_data_raw_cases_50.txt"  # name of the evidence file, in one place so it is easy to change
CURRENT_YEAR = 2026  # the year we are auditing from; every "years unsolved" is measured against this
STALE_YEARS = 5  # a case open this many years or longer gets the STALE flag
JUVENILE_AGE = 18  # victims under this age are counted separately

data = open(DATA_FILE)  # open the file and hand back a file object we can read from
lines = data.readlines()  # read every line into a list of strings, one string per line
data.close()  # close the file; we already have everything we need in memory

total_records = 0  # accumulator: how many real records we parsed
open_count = 0  # accumulator: how many of those are still OPEN
stale_count = 0  # accumulator: how many OPEN cases are STALE_YEARS or older
juvenile_open_count = 0  # accumulator: how many OPEN cases had a victim under 18
oldest_year = 9999  # min-tracker: start impossibly high so the first real year always beats it
oldest_name = ""  # name that goes with oldest_year; empty until the first record sets it

print("FLAGGED OPEN CASES")  # header for the per-case section
print("-" * 78)  # "-" repeated 78 times: a divider line without typing 78 dashes

for line in lines:  # run everything indented below once per line in the file
    line = line.strip()  # drop leading/trailing spaces and the invisible newline at the end
    if line == "":  # a blank or whitespace-only line has nothing to parse
        continue  # skip to the next line instead of crashing on it
    fields = line.split("|")  # split on the bare pipe; spaces around it get stripped per field below
    if len(fields) != 7:  # a real record has exactly 7 fields; anything else is junk
        continue  # skip malformed lines so one bad row cannot take down the run

    name = fields[0].strip().title()  # strip the padding, then Title Case: "CARTER, DEMARCUS" -> "Carter, Demarcus"
    sex = fields[1].strip().upper()  # standardize "m"/"M" to a single uppercase form
    age = int(fields[2].strip())  # convert the age text "39" into the number 39 so we can compare it
    year = int(fields[3].strip()[0:4])  # take characters 0-3 of "2014-06-11" -> "2014", then convert to 2014
    beat = fields[5].strip().title()  # "beat 352" and "Beat 352" both become "Beat 352"
    status = fields[6].strip().upper()  # "open"/"Open"/"OPEN" all become "OPEN" so == comparisons work

    total_records = total_records + 1  # this line survived the guards, so it counts as a record
    years_unsolved = CURRENT_YEAR - year  # how long this case has been sitting

    if status != "OPEN":  # closed cases are counted in the total but not investigated further
        continue  # next record

    open_count = open_count + 1  # everything past this point is an open case

    if years_unsolved >= STALE_YEARS:  # first question: has it been open 5+ years?
        flag = "*** STALE ***"  # yes — this is the flag the audit cares about
        stale_count = stale_count + 1  # and it goes on the stale tally
    elif years_unsolved >= 2:  # only asked when the line above was False
        flag = "aging"  # 2-4 years: worth watching, not yet stale
    else:  # everything left over: 0-1 years
        flag = "recent"

    if age < JUVENILE_AGE:  # a separate question, asked of every open case
        juvenile_open_count = juvenile_open_count + 1  # tally it
        flag = flag + " [JUVENILE]"  # and glue the marker onto whatever flag we already set

    if year < oldest_year:  # is this case older than the oldest one we have seen so far?
        oldest_year = year  # if so, it becomes the new record holder
        oldest_name = name  # keep the name with it, or we would only know the year

    print(f"{flag:<26} {name:<22} {sex} {age:<3} {year}  {years_unsolved:>2} yrs  {beat}")  # :<26 pads right, :>2 pads left, so columns line up

print()  # blank line between the two sections
print("CASE REPORT")  # header for the summary
print("-" * 78)
print(f"Total records:        {total_records}")  # reported AFTER the loop, once the walk is finished
print(f"Open cases:           {open_count}")
print(f"Stale (>= {STALE_YEARS} yrs):     {stale_count}")
#print(f"Juveniles (open):     {juvenile_open_count}") #not in the slides' final output. kept for curiosity.
print(f"Oldest open case:     {oldest_name} ({oldest_year})")
