# lockers.py — dedupe the case file, profile the victim ages, and rank the beats by open cases

normalized = []  # a LIST: holds every cleaned-up line in file order (slide 4's "empty locker")

with open("data/wk04_data_raw_cases_dupes.txt", encoding="utf-8") as f:  # open the week 4 data file
    for line in f:  # walk the file one line at a time
        clean = line.strip().upper()  # NORMALIZE FIRST: trim spaces, force one casing (slide 5's rule)
        if clean == "":  # the file ends with a blank line
            continue  # skip blanks so they never reach the count
        normalized.append(clean)  # add this cleaned line onto the end of the list

unique = set(normalized)  # a SET keeps one of each — the dedupe, done AFTER normalizing

ages = []  # a LIST to collect every victim age from the unique records
per_beat = {}  # a DICT: beat number -> how many OPEN cases it has

for rec in sorted(unique):  # sorted() gives a stable order, so the report reads the same every run
    fields = rec.split("|")  # split the record on the bare pipe
    age = int(fields[2].strip())  # convert the age text into a number
    beat = fields[5].strip().replace("BEAT", "").strip()  # "BEAT 352" becomes just "352"
    status = fields[6].strip()  # already uppercase from normalizing, so "OPEN" or "CLOSED"

    ages.append(age)  # collect the age now, analyze the whole list later (slide 4)

    if status == "OPEN":  # only open cases count toward the beat ranking
        if beat in per_beat:  # have we seen this beat before?
            per_beat[beat] += 1  # yes: add one to its locker
        else:  # first time seeing this beat
            per_beat[beat] = 1  # create its locker, starting at 1

print(f"Lines in file:      {len(normalized)}")  # how many real lines we read
print(f"Unique records:     {len(unique)}")  # how many survived the dedupe
print(f"Duplicates removed: {len(normalized) - len(unique)}")  # the difference is the duplicates
print()  # blank line between sections

average_age = sum(ages) / len(ages)  # total of all ages divided by how many ages there are
print(f"Youngest {min(ages)} / Oldest {max(ages)} / Average {average_age:.1f}")  # .1f = one decimal place
print()  # blank line before the ranking

print("Open cases per beat:")  # heading for the ranking
for beat in sorted(per_beat, key=per_beat.get, reverse=True):  # sort the KEYS by their VALUES, biggest first
    count = per_beat[beat]  # look up this beat's open-case count
    bar = "#" * count  # repeat "#" once per case — a histogram with zero libraries
    print(f"Beat {beat:<6}{count:>3}  {bar}")  # left-pad the beat, right-pad the count, then the bar
