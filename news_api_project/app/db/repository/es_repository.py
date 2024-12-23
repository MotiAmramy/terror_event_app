from news_api_project.app.db.es_database import connect_elasticsearch
from elasticsearch import helpers




def insert_review_elastic_search(news_list):
    with connect_elasticsearch() as es_client:
        try:

            es_documents = [to_elasticsearch_doc(document) for document in news_list]
            helpers.bulk(es_client, es_documents)
            print(f"Successfully inserted {len(es_documents)} news articles into Elasticsearch.")

        except Exception as e:
            print(f"Error inserting data into Elasticsearch: {e}")
    return "Finished inserting data into Elasticsearch"




def to_elasticsearch_doc(article):
    return {
        "_index": "news",
        "_source": {
            "content": article["content"],
            "date": article["date"],
            "category": article["category"],
            "country": article["country"],
            "region": article["region"],
            "latitude": article["latitude"],
            "longitude": article["longitude"],
        },
    }