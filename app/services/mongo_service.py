from typing import List, Callable
import toolz as t
from app.db.models.mongo_event import TerrorEvent, Location
from app.db.repository.mongo_repository import insert_many_event
from app.services.csv_process_service import process_and_merge
import pandas as pd


def insert_to_mongo_chunks(data: List, insert_func: Callable, chunks_size: int):
    [insert_func(chunk) for chunk in list(t.partition_all(chunks_size, data))]


def process_df_and_insert_to_mongo(chunks_size=1000):
    merged_df = process_and_merge()
    data = [row_to_terror_event(row) for _, row in merged_df.iterrows()]
    insert_to_mongo_chunks(data, insert_many_event, chunks_size)

def if_none(val):
    if isinstance(val, pd.Series):
        # If the value is a Series, take the first element (this is usually safe)
        val = val.iloc[0] if not val.empty else None
    return None if pd.isna(val) else val

def row_to_terror_event(row) -> TerrorEvent:
    location = Location(
        country=if_none(row.get('country')),
        region=if_none(row.get('region')),  # Using get to avoid KeyError
        city=if_none(row.get('city')),
        latitude=if_none(row.get('latitude')),
        longitude=if_none(row.get('longitude'))
    )

    event_date = if_none(row.get('date'))
    attack_types = [if_none(row.get('attack_type')), if_none(row.get('attack_type2'))]
    attack_types = [item for item in attack_types if item is not None]

    target_types = [if_none(row.get('target_type')), if_none(row.get('target_type2'))]
    target_types = [item for item in target_types if item is not None]

    group_types = [if_none(row.get('perpetrator')), if_none(row.get('perpetrator2'))]
    group_types = [item for item in group_types if item is not None]

    terror_event = TerrorEvent(
        date=event_date,
        description=if_none(row.get('description')),
        fatalities=if_none(row.get('fatalities')),
        injuries=if_none(row.get('injuries')),
        casualties=if_none(row.get('casualties')),
        num_of_attackers=if_none(row.get('num_of_attackers')),
        location=location,
        attack_types=attack_types,
        target_types=target_types,
        group_types=group_types
    )
    return terror_event