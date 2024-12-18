from typing import List, Callable
import toolz as t

def insert_to_mongo_chunks(data: List, insert_func: Callable, chunks_size: int):
    [insert_func(item) for item in list(t.partition_all(chunks_size, data))]