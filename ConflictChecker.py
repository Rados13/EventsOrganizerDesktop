from dataclasses import dataclass
from enum import Enum
import pandas as pd


class ConflictType(Enum):
    LECTURER = 1
    PLACE = 2


@dataclass(frozen=True)
class Conflict:
    conflict_type: ConflictType
    first_table: int
    first_row: int
    second_table: int
    second_row: int

    # messages could be better
    def __str__(self):
        msg = "conflict between sheet " + str(self.first_table) + ", row " + str(self.first_row) + \
            " and sheet " + str(self.second_table) + ", row " + str(self.second_row) + "."
        if self.conflict_type == ConflictType.LECTURER:
            return "Lecturer " + msg
        else:
            return "Place " + msg


class ConflictChecker:

    def get_all_conflicts(self, df_list):
        conflicts = []
        for i, df in enumerate(df_list):
            for j in range(0, len(df)):
                event = (df.get("Data")[j], df.get("Godziny")[j], df.get("Sala")[j], df.get("Prowadzący")[j])
                new_conflicts = self.get_conflicts_with(event, i, j, df_list)
                conflicts += new_conflicts
        return conflicts

    def get_conflicts_with(self, event, table_index, event_index, df_list):
        (date, time, place, person) = event

        conflicts = []
        is_first_pass = True
        for i in range(table_index, len(df_list)):
            df = df_list[i]
            start_index = event_index + 1 if is_first_pass else 0

            for j in range(start_index, len(df)):
                other_date, other_time = df.get("Data")[j], df.get("Godziny")[j]
                other_place, other_person = df.get("Sala")[j], df.get("Prowadzący")[j]

                if date == other_date and self.in_conflict(time, other_time):
                    if place == other_place and place is not None and not pd.isna(place):
                        conflicts.append(Conflict(ConflictType.PLACE, table_index, event_index, i, j))

                    if person == other_person and person is not None and not pd.isna(person):
                        conflicts.append(Conflict(ConflictType.LECTURER, table_index, event_index, i, j))

            is_first_pass = False
        return conflicts

    # can be changed later
    def in_conflict(self, time: str, other_time: str):
        if time is None or other_time is None or pd.isna(time) or pd.isna(other_time):
            return False
        times_1 = time.split("-")
        times_2 = other_time.split("-")
        begin_1 = float(times_1[0])
        end_1 = float(times_1[1])
        begin_2 = float(times_2[0])
        end_2 = float(times_2[1])
        return not ((begin_1 > end_2) or (end_1 < begin_2))

