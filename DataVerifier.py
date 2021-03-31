import pandas as pd


# Verifies and filters input data. So far only basic functionality concerning required column fields.
# Will be added: time verification.
def verify_and_filter(row):
    fields = ("Forma", "Prowadzący", "Godziny", "Data")
    missing = [f for f in fields if f not in row or row[f] is None]

    if missing:
        print("Warning! Incomplete column set in nr " +
              " xlsx file. " + str(missing) + " missing. Will be ignored in further operations.")
        return False
    else:
        return True
