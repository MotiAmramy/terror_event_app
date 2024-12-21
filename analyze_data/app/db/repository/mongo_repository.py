from app.db.mongo_database import events_collection


def fetch_events_from_mongo():
    cursor = events_collection.find({}, {'attack_types': 1, 'fatalities': 1, 'injuries': 1, 'description': 1,
                                         'location': 1})
    return list(cursor)



def fetch_all_events_from_mongo():
    cursor = events_collection.find({})
    return list(cursor)