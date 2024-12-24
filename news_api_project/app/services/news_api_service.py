import os
from dotenv import load_dotenv
from news_api_project.app.api.news_api import fetch_articles


load_dotenv(verbose=True)


def news_api_requests(articles_page=1):
    data = fetch_articles(os.environ['NEWS_API'], os.environ['NEWS_API_KEYWORD'], articles_page)
    return data['articles']["results"]

