import os
from news_api_project.app.kafka_producer.producer import produce
from news_api_project.app.services.groq_api_service import get_news_with_location
from news_api_project.app.services.news_api_service import news_api_requests
from dotenv import load_dotenv


load_dotenv(verbose=True)





if __name__ == "__main__":
    news_from_api = news_api_requests()
    news_for_insert_to_elastic_search = get_news_with_location(news_from_api)
    produce(data=news_for_insert_to_elastic_search, key='news', topic=os.environ['NEWS_TOPIC'])






