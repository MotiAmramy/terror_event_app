
from data_normalize.app.db.models.mongo_event import TerrorEvent, Location
from data_normalize.app.db.repository.mongo_repository import insert_many_event
from data_normalize.app.services.elastic_service import insert_to_db_chunks
from data_normalize.app.utils.pandas_utils import  if_none





def process_df_and_insert_to_mongo(merged_df, chunks_size=1000):
    data = [row_to_terror_event(row) for _, row in merged_df.iterrows()]
    insert_to_db_chunks(data, insert_many_event, chunks_size)



def row_to_terror_event(row) -> TerrorEvent:
    location = Location(
        country=if_none(row.get('country')),
        region=if_none(row.get('region')),
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