import requests
from Event import Event
from typing import List


BACKEND_URL = "https://eventsorganizer.herokuapp.com"

def get_lecture_events_from_db(first_name, last_name) -> List[Event]:
    result = requests.get(f"{BACKEND_URL}/classes/where?firstName={first_name}&lastName={last_name}")
    try:
        classes = result.json()
        return [Event.create_from_db_data(elem) for elem in classes]
    except Exception as e:
        print(e)
        print("Error with submit occurred.")
        print(result.content)