import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

connection_string = 'mongodb://admin:1234@localhost:27017/'

client = MongoClient(connection_string)
db = client['events_db']
events_collection = db["events"]
