import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(verbose=True)

# connection_string = f'mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_db}'
connection_string = 'mongodb://admin:1234@localhost:27017/'

client = MongoClient(connection_string)
db = client['events_db']
events_collection = db["events"]
#
# try:
#     client = MongoClient(connection_string)
#
#     # Test the connection by pinging the server
#     client.admin.command('ping')  # This sends a ping command to the MongoDB server
#
#     print("MongoDB connection successful!")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
