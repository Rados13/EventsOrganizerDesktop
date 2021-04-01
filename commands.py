import pandas as pd
from typing import List
from os.path import splitext, exists, isfile, isdir, join
from os import listdir
from ConflictChecker import get_all_conflicts
from Event import Event
from datetime import datetime
from DataVerifier import verify_and_filter


def import_data_from_excel(file_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_name, engine='openpyxl')
    df = df.where(pd.notnull(df), None)
    return fill_empty_cells(df)


def fill_empty_cells(df: pd.DataFrame) -> pd.DataFrame:
    for column in df:
        prev = None
        if column != "Godziny":
            for idx, elem in enumerate(df[column]):
                if elem is None or pd.isna(elem):
                    df.loc[idx, column] = prev
                if elem is not None and not pd.isna(elem):
                    prev = elem
    return df


def is_xlsx_file(path: str) -> bool:
    return isfile(path) and splitext(path)[1] == ".xlsx"


def find_all_excels_in_path(path: str) -> List[str]:
    result = [join(path, file) for file in listdir(path) if is_xlsx_file(join(path, file))]
    print(f"Read {len(result)} xlsx files in this directory")
    return result


def add_command(path: str) -> List[str]:
    if exists(path):
        if is_xlsx_file(path):
            return [path]
        elif isdir(path):
            return find_all_excels_in_path(path)
        else:
            print("This path does not correspond to directory or xlsx file")
    else:
        print("This path is not correct")


def check_command(excel_list: List[str], checked_events: List[Event]) -> List[Event]:
    data_frames = [(idx + 1, import_data_from_excel(excel)) for idx, excel in enumerate(excel_list)]

    events = [Event.create_from_data_frame(table, idx + 1, row) for (table, df) in data_frames
              for idx, row in df.iterrows() if isinstance(row["Data"], datetime) and verify_and_filter(row)]

    all_events = events + checked_events

    conflicts = get_all_conflicts(all_events)

    if conflicts:
        print("Conflicts Detected")
        print("\n".join([elem.__str__() for elem in conflicts]))
    else:
        return events


# made request to REST API
def submit_command(events_list: List[Event]):
    pass
