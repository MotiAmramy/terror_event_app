from data_normalize.app.utils.insert_to_db_utils import if_none


def to_elasticsearch_doc_from_message(article):
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



def to_elasticsearch_doc_from_df(article):
    return {
        "_index": "news",
        "_source": {
            "content": if_none(article.get('description')),
            "date": if_none(article.get('date')),
            "category": "historical terror attack",
            "country": if_none(article.get('country')),
            "region": if_none(article.get('region')),
            "latitude": if_none(article.get('latitude')),
            "longitude": if_none(article.get('longitude')),
        },
    }


