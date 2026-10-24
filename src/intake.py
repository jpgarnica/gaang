# src/intake.py - ITSS/OPRE 3312 Week 6 - Operation: Bulletproof

import csv                                 # bring in Python's csv module so it can split rows for us


def parse_row(row):                        # define a tool that turns one CSV row (a list) into a case dict
    """Validate one row and return it as a dict, or raise ValueError with a reason."""   # docstring: says what this tool does
    if len(row) != 8:                      # a good row has exactly 8 fields (case_id through status)
        raise ValueError("truncated row")  # stop here and report why this row is bad
    age = int(row[3])                      # turn the age text into a number; "unknown" raises ValueError on its own
    if row[4].strip() == "":               # the date field is empty after trimming spaces
        raise ValueError("missing date")   # stop here and report why this row is bad
    return {                               # row passed every check, so hand back a dict
        "case_id": row[0].strip(),         # field 1: the case number, spaces trimmed
        "name": row[1].strip().title(),    # field 2: victim name, trimmed and Title Cased ("carter, d" -> "Carter, D")
        "age": age,                        # the number we already converted above
        "date": row[4].strip(),            # field 5: the date, spaces trimmed
    }                                      # end of the dict


def load_cases(path):                      # define a tool that reads the whole CSV file
    """Read the CSV, keep good rows, quarantine bad ones, return (good, quarantine)."""   # docstring: says what this tool does
    good = []                              # list that will hold every row that parsed cleanly
    quarantine = []                        # list that will hold (line number, reason) for every bad row
    with open(path, newline="") as f:      #  newline=""  stops Python from changing hidden line endings like \r\n so csv.reader sees them as-is
        reader = csv.reader(f)             # csv.reader splits each line into a list, even "LAST, FIRST" in quotes
        header = next(reader)              # remove row 1 (the column names) so the loop only sees data
        for line_num, row in enumerate(reader, start=2):   # # enumerate numbers each tip as we loop: i is the number, tip is the line; start=2 means count from 2
            if len(row) == 0:              # a blank line comes back as an empty list
                continue                   # skip it, it is not a case record, and go to the next line
            try:                           # attempt the risky thing
                good.append(parse_row(row))   # parse the row and add the dict to the good list
            except ValueError as err:      # catch ONLY ValueError (never a bare except)
                quarantine.append((line_num, str(err)))   # log the line number and the reason as text
    return good, quarantine                # hand back both lists


def report(good, quarantine):              # define a tool that prints the results
    """Print loaded count, quarantined count, and the full quarantine log."""   # docstring: says what this tool does
    print(f"Rows loaded cleanly:   {len(good)}")   # how many rows made it into the good list
    print(f"Rows quarantined:      {len(quarantine)}")   # how many rows were rejected
    print()                                # print an empty line
    print("QUARANTINE LOG:")               # heading for the log
    for line_num, reason in quarantine:    # unpack each (line number, reason) pair
        print(f"  line {line_num}: {reason}")   # print where the bad row was and why it was rejected


good, quarantine = load_cases("data/wk06_data_raw_cases_100.csv")   # load the week 6 file into the two lists
report(good, quarantine)                   # print the report
