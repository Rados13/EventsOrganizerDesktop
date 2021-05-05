import sys
from dataclasses import dataclass
from typing import List

from tqdm import tqdm

from Event import Event, ConflictType
from access_db import get_lecture_events_from_db


@dataclass(frozen=True)
class Conflict:
    event_1: Event
    event_2: Event
    conflict_type: ConflictType

    def __str__(self):
        msg = "conflict between " + str(self.event_1.table_path) + ", row " + str(self.event_1.row) + \
              " and " + str(self.event_2.table_path) + ", row " + str(self.event_2.row) + "."
        if self.conflict_type == ConflictType.LECTURER:
            return "Lecturer (" + self.event_1.first_name + " " + self.event_1.last_name + ") " + msg
        else:
            return "Place ( " + self.event_1.room + ") " + msg


def get_all_conflicts(events: List[Event], db_mode: bool):
    conflicts = []
    conflicts_with_db = []
    for first_idx, first_event in enumerate(tqdm(events, file=sys.stdout, desc="Checking conflicts",
                                                 bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')):
        for second_event in events[first_idx:]:
            if first_event != second_event and first_event.is_conflict(second_event):
                conflicts.append(Conflict(
                    first_event, second_event, first_event.get_conflict_type(second_event)
                ))

        if db_mode:
            for second_event in get_lecture_events_from_db(first_event.first_name, first_event.last_name):
                if first_event.is_conflict(second_event):
                    conflicts_with_db.append(Conflict(
                        first_event, second_event, first_event.get_conflict_type(second_event)
                    ))
    return conflicts + conflicts_with_db
