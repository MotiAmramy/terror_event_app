from news_api_project.app.db.repository.es_repository import insert_review_elastic_search
from news_api_project.app.services.groq_api_service import get_news_with_location
from news_api_project.app.services.news_api_service import news_api_requests




if __name__ == "__main__":
    news_from_api = news_api_requests()
    news_for_insert_to_elastic_search = get_news_with_location(news_from_api)
    insert_review_elastic_search(news_for_insert_to_elastic_search)






