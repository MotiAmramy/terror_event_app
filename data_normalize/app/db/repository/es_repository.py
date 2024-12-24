from news_api_project.app.db.es_database import connect_elasticsearch
from elasticsearch import helpers

from news_api_project.app.utils.es_utils import to_elasticsearch_doc


def insert_chunks_elastic_search(es_documents):
    with connect_elasticsearch() as es_client:
        try:
            helpers.bulk(es_client, es_documents)
            print(f"Successfully inserted {len(es_documents)} news articles into Elasticsearch.")

        except Exception as e:
            print(f"Error inserting data into Elasticsearch: {e}")
    return "Finished inserting data into Elasticsearch"



