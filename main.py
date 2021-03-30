import pandas as pd
from typing import List
from os.path import splitext, exists, isfile, isdir, join
from os import listdir
import DataVerifier as dv
from ConflictChecker import get_all_conflicts
from Event import Event


file = '.\sheet3.xlsx'
QUIT = "quit"


def import_data_from_excel(file_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_name, engine='openpyxl')
    df = df.where(pd.notnull(df), None)
    return fill_empty_cells(df)


def fill_empty_cells(df: pd.DataFrame) -> pd.DataFrame:
    for column in df:
        prev = None
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



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    excel_lists = []
    # text = ""
    text = file
    print("Input excels paths")
    while text != QUIT:
        # text = input()
        if text != QUIT and exists(text):
            if is_xlsx_file(text):
                excel_lists.append(text)
            elif isdir(text):
                excel_lists.append(find_all_excels_in_path(text))
            else:
                print("This path does not correspond to directory or xlsx file")
        elif text != QUIT and not exists(text):
            print("This path is not correct")
        # text=QUIT
    data_frames = [import_data_from_excel(excel) for excel in excel_lists]

    events = [Event.create_from_data_frame(row) for df in data_frames for idx,row in df.iterrows()]

    data_frames = dv.verify_and_filter(data_frames)

    event_table_list = map(lambda a: map(lambda b: Event.create_from_data_frame(b), a), data_frames)

    conflicts = get_all_conflicts(event_table_list)

    if conflicts:
        print("Conflicts Detected")
    for conflict in conflicts:
        print(conflict)

