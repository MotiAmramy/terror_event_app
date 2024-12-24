import os
from dotenv import load_dotenv
from flask import Flask
from data_normalize.app.kafka_consumer.consumer import consume_topic
from data_normalize.app.services.csv_process_service import process_and_merge
from data_normalize.app.services.elastic_service import process_df_and_insert_to_elastic
from data_normalize.app.services.kafka_service import process_message_and_insert_to_es
from data_normalize.app.services.mongo_service import process_df_and_insert_to_mongo



load_dotenv(verbose=True)
app = Flask(__name__)


if __name__ == '__main__':
     merged_df = process_and_merge()
     process_df_and_insert_to_mongo(merged_df)
     process_df_and_insert_to_elastic(merged_df)
     consume_topic(os.environ['NEWS_TOPIC'], process_message_and_insert_to_es)
     app.run(port=5002, debug=True)
