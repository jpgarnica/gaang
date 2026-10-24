# src/patterns.py - ITSS/OPRE 3312 Week 5 - Operation: Tip Line

import re                                  # bring in Python's regular expression (regex) module


def extract_phones(text):                  # define a tool that takes one tip's text as input
    """Find every phone number, (214) 555-1234 or 214-555-1234 style."""   # docstring: says what this tool does
    return re.findall(r"\(?\d{3}\)?[ -]\d{3}-\d{4}", text)   # findall: finds every piece that matches a pattern and gives them back to you as a list; optional ( , 3 digits, optional ) , space or dash, 3 digits, dash, 4 digits


def extract_case_refs(text):               # define a tool that finds case references in a tip
    """Find every case reference like CC-14589."""   # docstring: says what this tool does
    return re.findall(r"CC-\d{5}", text)   # literal "CC-" followed by exactly five digits


def extract_beats(text):                   # define a tool that finds beat numbers in a tip
    """Find every beat number mentioned, like beat 341."""   # docstring: says what this tool does
    return re.findall(r"[Bb]eat (\d{3})", text)   # "Beat" or "beat", a space, then capture () only the 3 digits


def extract_iso_dates(text):               # define a tool that finds year-first dates in a tip
    """Find every ISO date like 2019-02-19."""   # docstring: says what this tool does
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)   # 4-digit year, dash, 2-digit month, dash, 2-digit day


def extract_us_dates(text):                # define a tool that finds month/day/year dates in a tip
    """Find every US date like 4/7/2019."""   # docstring: says what this tool does
    return re.findall(r"\d{1,2}/\d{1,2}/\d{4}", text)   # 1 or 2 digit month, slash, 1 or 2 digit day, slash, 4-digit year


def summarize_tip(i, tip):                 # define a tool that builds one summary line for one tip
    """Run every extractor on one tip and return one formatted line."""   # docstring: says what this tool does
    phones = extract_phones(tip)           # call the phone tool and keep the list it hands back
    refs = extract_case_refs(tip)          # call the case-ref tool and keep its list
    beats = extract_beats(tip)             # call the beat tool and keep its list
    dates = extract_iso_dates(tip) + extract_us_dates(tip)   # call both date tools and join their lists with +
    return f"TIP {i}: phone={phones} case={refs} beat={beats} date={dates}"   # hand back the finished line as a string


tip_file = open("data/wk05_data_tipline.txt")   # open the tip-line file for reading
tips = tip_file.readlines()                # read every line of the file into a list (one tip per line)
tip_file.close()                           # close the file since we are done reading

callback_count = 0                         # start the counter for tips that left a phone number

for i, tip in enumerate(tips, start=1):    # enumerate numbers each tip as we loop: i is the number, tip is the line; start=1 means count from 1
    print(summarize_tip(i, tip))           # build this tip's summary line and print it

    if len(extract_phones(tip)) >= 1:      # check if this tip has at least one phone number
        callback_count = callback_count + 1   # add 1 to the callback counter

no_callback_count = len(tips) - callback_count   # every tip without a phone is a tip with no callback

print()                                    # print an empty line
print(f"Tips processed:       {len(tips)}")   # print how many tips were in the list
print(f"Tips with a callback: {callback_count}")   # print the callback counter
print(f"Tips with NO callback: {no_callback_count}  <- these leads die without follow-up")   # print the no-callback count
