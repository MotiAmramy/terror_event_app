from data_normalize.app.db.repository.es_repository import insert_chunks_elastic_search
from data_normalize.app.utils.es_utils import to_elasticsearch_doc_from_message, to_elasticsearch_doc_from_df
from data_normalize.app.utils.insert_to_db_utils import insert_to_db_chunks


def process_df_and_insert_to_elastic(merged_df, chunks_size=1000):
    data = [to_elasticsearch_doc_from_df(row) for _, row in merged_df.iterrows()]
    insert_to_db_chunks(data, insert_chunks_elastic_search, chunks_size)


def process_message_and_insert_to_elastic(message, chunks_size=1000):
    es_documents = [to_elasticsearch_doc_from_message(document) for document in message]
    insert_to_db_chunks(es_documents, insert_chunks_elastic_search, chunks_size)

