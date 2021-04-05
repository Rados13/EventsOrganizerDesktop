from dataclasses import dataclass
from enum import Enum
import pandas as pd
from typing import List

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


def get_all_conflicts(events: List[Event]):
    conflicts = []
    for first_idx, first_event in enumerate(events):
        for second_event in events[first_idx:]:
            if first_event != second_event and first_event.is_conflict(second_event):
                conflicts.append(Conflict(
                    first_event, second_event, first_event.get_conflict_type(second_event),
                    first_event.table, first_event.row, second_event.table, second_event.row))
    return conflicts
