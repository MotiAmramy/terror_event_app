
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