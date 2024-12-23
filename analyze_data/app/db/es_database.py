import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv


load_dotenv(verbose=True)



def connect_elasticsearch():
    client = Elasticsearch(os.environ["ELASTIC_SEARCH_HOST"])
    if client.ping():
       print("Connected to Elasticsearch!")
    else:
       print("Connection failed.")
    return client


