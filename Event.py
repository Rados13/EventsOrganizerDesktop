from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum


class Event:

    @staticmethod
    def create_from_data_frame(table_idx: int, row_idx: int, row) -> Event:
        names = row["Prowadzący"].split(" ")
        first_name = names[0]
        last_name = names[1]
        start_time, end_time = row["Godziny"].split("-")
        event_date = row["Data"]
        start_time = datetime.strptime(start_time, "%H.%M")
        end_time = datetime.strptime(end_time, "%H.%M")
        start_time = event_date + timedelta(hours=start_time.hour, minutes=start_time.minute)
        end_time = event_date + timedelta(hours=end_time.hour, minutes=end_time.minute)
        return Event(table_idx,
                     row_idx,
                     row["Zjazd"] if "Zjazd" in row else None,
                     row["Przedmiot"] if "Przedmiot" in row else None,
                     row["L/W"] if "L/W" in row else None,
                     start_time,
                     end_time,
                     row["H"] if "H" in row else None,
                     row["Forma"],
                     row["Sala"],
                     row["Grupa"] if "Grupa" in row else None,
                     first_name,
                     last_name
                     )

    def __init__(self, table, row, appointment_number, name, event_type,
                 start_time, end_time, hours, form, room, group, first_name, last_name):
        self.appointment_number = int(appointment_number)
        self.name = name
        self.event_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.form = form
        self.room = room
        self.group = group
        self.first_name = first_name
        self.last_name = last_name
        self.hours = int(hours)
        self.table = table
        self.row = row

    def at_same_date_other_event(self, other: Event) -> bool:
        return self.start_time <= other.start_time <= self.end_time

    def is_conflict(self, other: Event):
        same_time = self.at_same_date_other_event(other) or other.at_same_date_other_event(self)
        same_lecturer_same_time = self.first_name == other.first_name and self.last_name == other.last_name and same_time
        same_room_same_time = self.room == other.room and self.room != "" and same_time and self.form != "zdalnie"

        return same_lecturer_same_time or same_room_same_time

    def get_conflict_type(self, other: Event):  # To add: None / NaN case
        same_time = self.at_same_date_other_event(other) or other.at_same_date_other_event(self)
        same_lecturer_same_time = self.first_name == other.first_name and self.last_name == other.last_name and same_time
        same_room_same_time = self.room == other.room and self.room != "" and same_time and self.form != "zdalnie"

        if same_lecturer_same_time:
            return ConflictType.LECTURER
        if same_room_same_time:
            return ConflictType.ROOM

    def __str__(self):
        return str(self.appointment_number) + " | " + str(self.name) + " | " + str(self.event_type) + " | " + \
               str(self.start_time) + " | " + str(self.end_time) + " | " + str(self.form) + " | " + \
               str(self.room) + " | " + str(self.first_name) + " | " + str(self.last_name) + " | " + \
               str(self.group)


class ConflictType(Enum):
    LECTURER = 1
    ROOM = 2
