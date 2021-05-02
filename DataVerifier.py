from datetime import datetime


def verify_and_filter(row, idx: int, table_name: str):
    fields = ("Forma", "Prowadzący", "Godziny", "Data")
    missing = [f for f in fields if f not in row or row[f] is None]

    if "Data" not in missing:
        if row["Data"].date() < datetime.today().date():
            date = row["Data"].date()
            print(f"Warning! Date {date} in row {idx} of {table_name} is before today.")

    if row["Forma"] not in ("zdalnie", "stacjonarnie"):
        print(f"\"Forma\" not recognized in row {idx} of {table_name}. Should be either \"zdalnie\" or \"stacjonarnie\".")

    if missing:
        print(f"Warning! Incomplete column set in row {idx} " +
              f"of {table_name}. {missing} missing. Row will be ignored in further operations.")
        return False
    else:
        return True


def verify_dataframe(dataframe, table_name: str):
    conflict_fields = ("Sala", "Prowadzący", "Godziny", "Data")
    submitted_fields = ("Zjazd", "Przedmiot", "Grupa", "L/W", "H", "Forma")
    important_missing = [f for f in conflict_fields if f not in dataframe.columns]
    submitted_missing = [f for f in submitted_fields if f not in dataframe.columns]

    if submitted_missing:
        print(f"Warning! Incomplete column set in {table_name}. " +
              f"{submitted_missing} missing. If submitted, these values will not be set on the service.")

    if important_missing:
        print(f"Warning! Incomplete column set in {table_name}. " +
              f"{important_missing} missing. Will be ignored in further operations.")
        return False
    else:
        return True