from app.db.mongo_database import event_collection


def insert_many_event(data):
    try:
        event_collection.insert_many(data)
        return data
    except Exception as e:
        print(f"An error occurred while inserting the data: {e}")
        return None
