from dataclasses import dataclass
from enum import Enum
import pandas as pd
from Event import Event, ConflictType


@dataclass(frozen=True)
class Conflict:
    event_1: Event
    event_2: Event
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


def get_all_conflicts(event_table_list):
    conflicts = []
    for i, event_table in enumerate(event_table_list):
        for j, event in enumerate(event_table):
            new_conflicts = get_conflicts_with(event, i, j, event_table_list)
            conflicts += new_conflicts
    return conflicts


def get_conflicts_with(event, table_index, event_index, event_table_list):
    conflicts = []
    is_first_pass = True
    for i in range(table_index, len(event_table_list)):
        event_table = event_table_list[i]
        start_index = event_index + 1 if is_first_pass else 0

        for j in range(start_index, len(event_table)):
            other_event = event_table[j]
            conflict_type = event.get_conflict_type(other_event)
            if conflict_type is not None:
                conflicts.append(Conflict(event, other_event, conflict_type, table_index, event_index, i, j))

        is_first_pass = False

    return conflicts

