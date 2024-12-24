from analyze_data.app.db.es_database import connect_elasticsearch




def build_search_query(keyword):
    return {
        "query": {
            "query_string": {
                "query": keyword,
                "default_field": "*"
            }
        }
    }


def search_by_category_and_keyword(category, keyword):
    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "category.keyword": category  # Search within the specified category
                        }
                    },
                    {
                        "match": {
                            "content": keyword  # Search for the keyword in the 'content' field (or any other field)
                        }
                    }
                ]
            }
        }
    }






def search_by_keyword_and_date_range(start_date, end_date, keyword):
    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "content": keyword
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "date": {
                                "gte": start_date,
                                "lte": end_date
                            }
                        }
                    }
                ]
            }
        }
    }



def execute_search(query):
    try:
        with connect_elasticsearch() as es_client:
            response = es_client.search(index="news", body=query)
            return [doc["_source"] for doc in response["hits"]["hits"]]
    except Exception as e:
        raise RuntimeError(f"Failed to execute search: {e}")

