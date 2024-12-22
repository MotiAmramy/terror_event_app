import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

connection_string = os.environ['MONGO_URL']

client = MongoClient(connection_string)
db = client['events_db']
events_collection = db["events"]
