from dataclasses import dataclass
from typing import List

from Event import Event, ConflictType


@dataclass(frozen=True)
class Conflict:
    event_1: Event
    event_2: Event
    conflict_type: ConflictType

    def __str__(self):
        msg = "conflict between " + str(self.event_1.table) + ", row " + str(self.event_1.row) + \
              " and " + str(self.event_2.table) + ", row " + str(self.event_2.row) + "."
        if self.conflict_type == ConflictType.LECTURER:
            return "Lecturer (" + self.event_1.first_name + " " + self.event_1.last_name + ") " + msg
        else:
            return "Place ( " + self.event_1.room + ") " + msg


def get_all_conflicts(events: List[Event]):
    conflicts = []
    for first_idx, first_event in enumerate(events):
        for second_event in events[first_idx:]:
            if first_event != second_event and first_event.is_conflict(second_event):
                conflicts.append(Conflict(
                    first_event, second_event, first_event.get_conflict_type(second_event)
                ))
    return conflicts
