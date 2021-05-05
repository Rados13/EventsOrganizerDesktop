import sys
import pandas as pd
from typing import List
from os.path import splitext, exists, isfile, isdir, join
from os import listdir
from tqdm import tqdm
from ConflictChecker import get_all_conflicts
from Event import Event, print_event_label
from datetime import datetime
from DataVerifier import verify_and_filter, verify_dataframe
import requests

from SuggestionFinder import find_all_suggestions
from access_db import BACKEND_URL


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def check_command(excel_list: List[str], checked_events: List[Event], db_mode: bool) -> List[Event]:
    print(bcolors.WARNING, end='')
    data_frames = [(excel, import_data_from_excel(excel)) for excel in excel_list]
    data_frames = [frame for frame in data_frames if verify_dataframe(frame[1], frame[0])]

    events = [Event.create_from_data_frame(table, idx + 1, row) for (table, df) in data_frames
              for idx, row in df.iterrows() if isinstance(row["Data"], datetime) and verify_and_filter(row, idx, table)]

    print(bcolors.ENDC, end='')
    print()

    all_events = events + checked_events

    conflicts = get_all_conflicts(all_events, db_mode)

    if conflicts:
        print(bcolors.FAIL, end='')
        print("Conflicts Detected:\n")
        for elem in conflicts:
            print(elem)
            print_event_label()
            print(elem.event_1)
            print(elem.event_2)
            print()
        print(bcolors.ENDC, end='')

        events_conflicting = [c.event_1 for c in conflicts] + [c.event_2 for c in conflicts]
        events_non_conflicting = [e for e in events if e not in events_conflicting]
        suggestions = find_all_suggestions(conflicts, events_non_conflicting)
        if suggestions:
            print(bcolors.OKBLUE, end='')
            print("Suggestions:\n")
            for suggestion in suggestions:
                print("Event:")
                print_event_label()
                print(suggestion.conflicting_event)
                print("Could have its timeframe changed to:")
                for timeframe in suggestion.timeframes:
                    print(str(timeframe[0].hour).zfill(2) + ":" + str(timeframe[0].minute).zfill(2) + " - " +
                          str(timeframe[1].hour).zfill(2) + ":" + str(timeframe[1].minute).zfill(2))
                print()
            print(bcolors.ENDC, end='')
    else:
        return events


def print_events_command(events_list: List[Event]):
    print_event_label()
    for event in events_list:
        print(event)


def print_files_command(files_list: List[str]):
    for file in files_list:
        print(file)


# makes request to REST API
def submit_command(events_list: List[Event]):
    for event in tqdm(events_list, file=sys.stdout, desc="Submitting", bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        classes_form = None
        if event.form == "zdalnie":
            classes_form = "REMOTE"
        if event.form == "stacjonarnie":
            classes_form = "STATIONARY"

        classes_type = None
        if event.event_type == "L":
            classes_type = "LABORATORY"
        if event.event_type == "W":
            classes_type = "LECTURE"
        json = {
            "appointmentNumber": event.appointment_number,
            "startTime": event.start_time.strftime("%Y-%m-%d %H.%M"),
            "endTime": event.end_time.strftime("%Y-%m-%d %H.%M"),
            "name": event.name,
            "studentsGroup": event.group,
            "firstName": event.first_name,
            "lastName": event.last_name,
            "classesType": classes_type,
            "numberOfHours": event.hours,
            "classesForm": classes_form,
            "classroom": event.room,
            "event": event.table_name
        }
        result = requests.post(f"{BACKEND_URL}/classes/submit", json=json)
        try:
            result.json()
        except:
            print("Error with submit occurred.")
            print(result.content)
