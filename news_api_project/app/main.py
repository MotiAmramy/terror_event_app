from flask import Flask
from news_api_project.app.services.kafka_service import produce_from_api_for_es_insert

app = Flask(__name__)




if __name__ == "__main__":
    produce_from_api_for_es_insert()
    app.run(port=5003, debug=True)






