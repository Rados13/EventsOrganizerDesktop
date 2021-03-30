import pandas as pd
from datetime import datetime
from __future__ import annotations


class Event:

    @staticmethod
    def create_from_data_frame(row) -> Event:
        start_time, end_time = row["Godziny"].split("-")
        event_date = row["Data"]
        start_time = datetime.strptime(event_date + " " + start_time, "%Y-%m-%d %H.%M")
        end_time = datetime.strptime(event_date + " " + end_time, "%Y-%m-%d %H.%M")
        return Event(row["Przedmiot"], row["L/W"], start_time, end_time, row["Forma"], row["Sala"], row["Prowadzący"])

    def __init__(self, name, event_type, start_time, end_time, form, room, lecture):
        self.name = name
        self.even_type = event_type
        self.start_time = start_time
        self.end_time = end_time
        self.form = form
        self.room = room
        self.lecture = lecture

    def at_same_date_other_event(self, other: Event) -> bool:
        return self.start_time < other.start_time < self.end_time

    def is_conflict(self, other: Event):
        same_time = self.at_same_date_other_event(other) or other.at_same_date_other_event(self)
        same_lecture_same_time = self.lecture == other.lecture and same_time
        same_room_same_time = self.room == other.lecture and self.room != "" and same_time

        return same_lecture_same_time or same_room_same_time
