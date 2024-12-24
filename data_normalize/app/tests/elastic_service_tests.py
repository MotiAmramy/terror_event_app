import pytest
from unittest.mock import patch, MagicMock
from data_normalize.app.services.elastic_service import (
    process_df_and_insert_to_elastic,
    process_message_and_insert_to_elastic,
    insert_to_db_chunks
)
import pandas as pd
from io import StringIO

# Sample data for testing
SAMPLE_DF_CONTENT = """
id,name,value
1,John,100
2,Jane,200
3,Doe,300
"""

SAMPLE_MESSAGE = [
    {"id": 1, "name": "John", "value": 100},
    {"id": 2, "name": "Jane", "value": 200},
    {"id": 3, "name": "Doe", "value": 300},
]


@pytest.fixture
def sample_df():
    return pd.read_csv(StringIO(SAMPLE_DF_CONTENT))


@pytest.fixture
def mock_insert_func():
    return MagicMock()


@patch("data_normalize.app.services.elastic_service.insert_to_db_chunks")
@patch("data_normalize.app.services.elastic_service.to_elasticsearch_doc_from_df")
def test_process_df_and_insert_to_elastic(mock_to_elasticsearch_doc_from_df, mock_insert_to_db_chunks, sample_df):
    mock_to_elasticsearch_doc_from_df.return_value = {"id": 1, "name": "John", "value": 100}
    process_df_and_insert_to_elastic(sample_df, chunks_size=2)
    assert mock_to_elasticsearch_doc_from_df.call_count == 3
    mock_insert_to_db_chunks.assert_called_once()


@patch("data_normalize.app.services.elastic_service.insert_to_db_chunks")
@patch("data_normalize.app.services.elastic_service.to_elasticsearch_doc_from_message")
def test_process_message_and_insert_to_elastic(mock_to_elasticsearch_doc_from_message, mock_insert_to_db_chunks):
    mock_to_elasticsearch_doc_from_message.return_value = {"id": 1, "name": "John", "value": 100}
    process_message_and_insert_to_elastic(SAMPLE_MESSAGE, chunks_size=2)
    assert mock_to_elasticsearch_doc_from_message.call_count == 3
    mock_insert_to_db_chunks.assert_called_once()
