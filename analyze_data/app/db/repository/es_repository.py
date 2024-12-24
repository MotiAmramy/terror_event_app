from analyze_data.app.db.es_database import connect_elasticsearch


def build_search_query(keyword=None):
    query = {
        "query": {
            "match_all": {}
        }
    }
    if keyword:
        query = {
            "query": {
                "query_string": {
                    "query": keyword,
                    "default_field": "*"
                }
            }
        }
    return query



def search_by_category_and_keyword(category, keyword=None):
    # Base query for category
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "category.keyword": category
                        }
                    }
                ]
            }
        }
    }

    if keyword:
        query['query']['bool']['must'].append({
            "match": {
                "content": keyword
            }
        })

    return query


def search_by_keyword_and_date_range(start_date=None, end_date=None, keyword=None):
    query = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        }
    }
    if keyword:
        query["query"]["bool"]["must"].append({
            "match": {
                "content": keyword
            }
        })

    if start_date and end_date:
        query["query"]["bool"]["filter"].append({
            "range": {
                "date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })

    return query

def execute_search(query):
    try:
        with connect_elasticsearch() as es_client:
            response = es_client.search(index="news", body=query)
            return [doc["_source"] for doc in response["hits"]["hits"]]
    except Exception as e:
        raise RuntimeError(f"Failed to execute search: {e}")

