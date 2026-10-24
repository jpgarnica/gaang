normalized = []  # empty list that will hold every cleaned-up line, in the order it appears in the file

with open("data/wk04_data_raw_cases_dupes.txt", encoding="utf-8") as f:  #  encoding="utf-8" tells Python how the text bytes are stored
    for line in f:  # loop through the file one line at a time
        clean = line.strip().upper()  # .strip() removes spaces/newlines at both ends, .upper() makes everything capitals so "open" and "OPEN" match
        if clean == "":  # true when the line was blank (e.g. the empty line at the end of the file)
            continue  # skip the rest of this loop pass and go to the next line
        normalized.append(clean)  # .append() adds the cleaned line to the end of the list

unique = set(normalized)  # set() keeps only one copy of each value, which removes the duplicate records

ages = []  # empty list that will collect every victim age
per_beat = {}  # empty dictionary: key = beat number, value = how many OPEN cases that beat has

for rec in sorted(unique):  # sorted() returns the set's records in a fixed alphabetical order so output is the same every run
    fields = rec.split("|")  # .split("|") cuts the record at each pipe into a list of fields
    age = int(fields[2].strip())  # take field 3 (index 2), trim spaces, and int() turns the text "34" into the number 34
    beat = fields[5].strip().replace("BEAT", "").strip()  # field 6 is like "BEAT 352"; .replace() deletes "BEAT", leaving "352"
    status = fields[6].strip()  # field 7 is the case status, already uppercase: "OPEN" or "CLOSED"

    ages.append(age)  # add this record's age to the ages list

    if status == "OPEN":  # only open cases are counted per beat
        if beat in per_beat:  # "in" checks whether this beat is already a key in the dictionary
            per_beat[beat] += 1  # it is, so add 1 to its count
        else:  # this beat hasn't been seen yet
            per_beat[beat] = 1  # create the key with a starting count of 1

print(f"Lines in file:      {len(normalized)}")  # f-string: anything inside {} is calculated and inserted; len() counts items in the list
print(f"Unique records:     {len(unique)}")  # number of records left in the set after duplicates were removed
print(f"Duplicates removed: {len(normalized) - len(unique)}")  # total lines minus unique records = how many were duplicates
print()  # print an empty line to separate sections

average_age = sum(ages) / len(ages)  # sum() adds all ages, divided by how many ages there are = the mean
print(f"Youngest {min(ages)} / Oldest {max(ages)} / Average {average_age:.1f}")  # min()/max() find smallest/largest; :.1f formats a number with exactly 1 decimal place (f = float)
print()  # another blank line before the ranking

print("Open cases per beat:")  # heading for the beat ranking
for beat in sorted(per_beat, key=per_beat.get, reverse=True):  # sort the beat keys by their counts (key=per_beat.get), biggest first (reverse=True)
    count = per_beat[beat]  # look up this beat's number of open cases
    bar = "#" * count  # multiplying a string repeats it, e.g. "#" * 3 = "###", making a text bar chart
    print(f"Beat {beat:<6}{count:>3}  {bar}")  # :<6 left-aligns the beat in 6 spaces, :>3 right-aligns the count in 3 spaces so columns line up
