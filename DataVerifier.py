import pandas as pd

# Verifies and filters input data. So far only basic functionality concerning required column fields.
# Will be added: time verification.
def verify_and_filter(df_list):
    new_list = []
    fields = ("Sala", "Prowadzący", "Godziny", "Data")
    for idx, df in enumerate(df_list):
        missing = [f for f in fields if f not in df.columns]

        if missing:
            print("Warning! Incomplete column set in nr " + str(idx)
                  + " xlsx file. " + str(missing) + " missing. Will be ignored in further operations.")
        else:
            new_list.append(df)

    return new_list
