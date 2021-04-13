from datetime import datetime


def verify_and_filter(row, idx: int):
    fields = ("Forma", "Prowadzący", "Godziny", "Data")
    missing = [f for f in fields if f not in row or row[f] is None]

    if "Data" not in missing:
        if row["Data"].date() < datetime.today().date():
            print("Warning! Date " + str(row["Data"].date()) + " in row " + str(idx) + " is before today.")

    if row["Forma"] not in ("zdalnie", "stacjonarnie"):
        print("\"Forma\" not recognized on row " + str(idx) + " . Should be either \"zdalnie\" or \"stacjonarnie\".")

    if missing:
        print("Warning! Incomplete column set in row " + str(idx) +
              " of xlsx file. " + str(missing) + " missing. Row will be ignored in further operations.")
        return False
    else:
        return True


def verify_dataframe(dataframe):
    conflict_fields = ("Sala", "Prowadzący", "Godziny", "Data")
    submitted_fields = ("Zjazd", "Przedmiot", "Grupa", "L/W", "H", "Forma")
    important_missing = [f for f in conflict_fields if f not in dataframe.columns]
    submitted_missing = [f for f in submitted_fields if f not in dataframe.columns]

    if submitted_missing:
        print("Warning! Incomplete column set in xlsx file. " +
              str(submitted_missing) + " missing. If submitted, these values will not be set on the service.")

    if important_missing:
        print("Warning! Incomplete column set in xlsx file. " +
              str(important_missing) + " missing. Will be ignored in further operations.")
        return False
    else:
        return True
