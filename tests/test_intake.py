# tests/test_intake.py - ITSS/OPRE 3312 Week 6 - tests for parse_row

import pytest                              # bring in pytest so we can use pytest.raises
from src.intake import parse_row           # borrow parse_row from src/intake.py


def test_good_row_parses():                # test 1: a clean row should come back as a correct dict
    row = ["CC-1", " carter, d ", "m", "36",
           "2018-03-22", "412 larkmoor", "352", "open"]   # a made-up good row with messy spacing and lowercase
    case = parse_row(row)                  # run the parser on it
    assert case["age"] == 36               # assert = "must be True or the test fails"; age text "36" must become the number 36
    assert case["name"] == "Carter, D"     # if False, pytest stops with AssertionError; name must be trimmed and Title Cased


def test_bad_age_rejected():               # test 2: an "unknown" age must be rejected
    row = ["CC-1", " carter, d ", "m", "36",
           "2018-03-22", "412 larkmoor", "352", "open"]   # start from the same good row
    row[3] = "unknown"                     # break the age field
    with pytest.raises(ValueError):        # the test passes only if the next line raises ValueError
        parse_row(row)                     # run the parser on the broken row


def test_missing_date_rejected():          # test 3: an empty date must be rejected
    row = ["CC-1", " carter, d ", "m", "36",
           "2018-03-22", "412 larkmoor", "352", "open"]   # start from the same good row
    row[4] = ""                            # break the date field
    with pytest.raises(ValueError):        # the test passes only if the next line raises ValueError
        parse_row(row)                     # run the parser on the broken row
