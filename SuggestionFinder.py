import sys
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime, time, timedelta, date
from tqdm import tqdm
from ConflictChecker import Conflict
from Event import Event, ConflictType
from access_db import get_lecture_events_from_db, get_room_events_from_db

# config
DAY_START = time(hour=8)
DAY_END = time(hour=20)


@dataclass(frozen=True)
class Suggestion:
    conflicting_event: Event
    timeframes: List[Tuple[time]]


def find_suggestions_to_event(conflicting_event: Event, events_same_lecturer: List[Event], events_same_classroom: List[Event]):
    minimum_time_delta = datetime.combine(date.min, conflicting_event.end_time.time()) \
                         - datetime.combine(date.min, conflicting_event.start_time.time())
    conflicting_events = events_same_lecturer + events_same_classroom
    conflicting_events.sort(key=(lambda event: event.start_time))

    timeframes = []
    start_time = DAY_START
    for event in conflicting_events:

        if event.start_time.time() < start_time:
            if event.end_time.time() > start_time:
                start_time = event.end_time.time()
            continue

        if event.start_time.time() > start_time:
            duration_to_next = datetime.combine(date.min, event.start_time.time()) - datetime.combine(date.min, start_time)
            duration_to_end = datetime.combine(date.min, DAY_END) - datetime.combine(date.min, start_time)
            time_delta = min(duration_to_next, duration_to_end)
            if time_delta >= minimum_time_delta:
                timeframes.append((start_time, min(event.start_time.time(), DAY_END)))
            start_time = min(event.end_time.time(), DAY_END)

    if start_time < DAY_END:
        duration = datetime.combine(date.min, DAY_END) - datetime.combine(date.min, start_time)
        if duration >= minimum_time_delta:
            timeframes.append((start_time, DAY_END))

    if len(timeframes) == 0:
        return None
    else:
        return Suggestion(conflicting_event, timeframes)


def find_all_suggestions(conflict_list: List[Conflict], correct_events: List[Event]):
    suggested_correct = [conflict.event_2 for conflict in conflict_list] # Simplification - we presume, that second events of conflicts are correct
    correct_events = correct_events + suggested_correct

    suggestions = []
    for conflict in tqdm(conflict_list, file=sys.stdout,  desc="Finding suggestions",
                         bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):

        c = conflict.event_1
        events_same_lecturer = [e for e in correct_events + get_lecture_events_from_db(c.first_name, c.first_name)
                                if e.first_name == c.first_name and e.last_name == c.last_name
                                and e.start_time.date() == c.start_time.date()]
        events_same_classroom = [e for e in correct_events + get_room_events_from_db(c.room)
                                 if e.room == c.room and e.form != "zdalnie" and c.form != "zdalnie"
                                 and e.start_time.date() == c.start_time.date()]

        suggestions.append(find_suggestions_to_event(c, events_same_lecturer, events_same_classroom))

    return filter(lambda x: x is not None, suggestions)


