from elasticsearch import Elasticsearch

from analyze_data.app.db.es_database import connect_elasticsearch

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)




def build_search_query(keyword):
    return {
        "query": {
            "query_string": {
                "query": keyword,
                "default_field": "*"
            }
        }
    }


def execute_search(query, size=100):
    try:
        with connect_elasticsearch() as es_client:
            response = es_client.search(index="news", body=query, size=size)
            return [doc["_source"] for doc in response["hits"]["hits"]]
    except Exception as e:
        raise RuntimeError(f"Failed to execute search: {e}")




