from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum


class Event:

    @staticmethod
    def create_from_data_frame(table_idx: int, row_idx: int, row) -> Event:
        start_time, end_time = row["Godziny"].split("-")
        event_date = row["Data"]
        start_time = datetime.strptime(start_time, "%H.%M")
        end_time = datetime.strptime(end_time, "%H.%M")
        start_time = event_date + timedelta(hours=start_time.hour, minutes=start_time.minute)
        end_time = event_date + timedelta(hours=end_time.hour, minutes=end_time.minute)
        return Event(table_idx, row_idx, row["Zjazd"], row["Przedmiot"], row["L/W"], start_time, end_time, row["Forma"],
                     row["Sala"], row["Prowadzący"])

    def __init__(self, table, row, appointment_number, name, event_type, start_time, end_time, form, room, lecturer):
        self.appointment_number = appointment_number
        self.name = name
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.form = form
        self.room = room
        self.lecturer = lecturer
        self.table = table
        self.row = row

    def at_same_date_other_event(self, other: Event) -> bool:
        return self.start_time <= other.start_time <= self.end_time

    def is_conflict(self, other: Event):
        same_time = self.at_same_date_other_event(other) or other.at_same_date_other_event(self)
        same_lecturer_same_time = self.lecturer == other.lecturer and same_time
        same_room_same_time = self.room == other.room and self.room != "" and same_time and self.form != "zdalnie"

        return same_lecturer_same_time or same_room_same_time

    def get_conflict_type(self, other: Event):  # To add: None / NaN case
        same_time = self.at_same_date_other_event(other) or other.at_same_date_other_event(self)
        same_lecturer_same_time = self.lecturer == other.lecturer and same_time
        same_room_same_time = self.room == other.room and self.room != "" and same_time and self.form != "zdalnie"

        if same_lecturer_same_time:
            return ConflictType.LECTURER
        if same_room_same_time:
            return ConflictType.ROOM

    def __str__(self):
        return str(self.appointment_number) + " | " + str(self.name) + " | " + str(self.event_type) + " | " + \
               str(self.start_time) + " | " + str(self.end_time) + " | " + str(self.form) + " | " + \
               str(self.room) + " | " + str(self.lecturer)


class ConflictType(Enum):
    LECTURER = 1
    ROOM = 2
