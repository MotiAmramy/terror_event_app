from typing import List
from data_normalize.app.db.models.mongo_event import TerrorEvent
from data_normalize.app.db.mongo_database import events_collection



def insert_many_event(data: List[TerrorEvent]):
    try:
        insert_data = [event.to_dict() for event in data]
        events_collection.insert_many(insert_data)
        print(f"Inserted {len(data)} events into MongoDB.")
    except Exception as e:
        print(f"An error occurred while inserting the data: {e}")