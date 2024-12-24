import toolz as t
from news_api_project.app.api.groq_api import get_json_from_groq_api
from news_api_project.app.utils.groq_utils import validate_groq_json



def get_valid_news_using_groq(article):
    try:
        location_dict = t.pipe(
            article,
            get_json_from_groq_api,
            validate_groq_json
            )
        if location_dict:
            return {
                "content": article["title"] + " " + article["body"],
                "date": article["date"],
                "category": location_dict["category"],
                "country": location_dict["country"],
                "region": location_dict["continent"],
                "latitude": location_dict["country_latitude"],
                "longitude": location_dict["country_longitude"]
            }
    except Exception as e:
        return None



def get_news_with_location(data):
    filtered_list = t.pipe(
        data,
        t.partial(map, lambda a: get_valid_news_using_groq(a)),
        t.partial(filter, lambda x: x is not None),
        list
    )
    return filtered_list



