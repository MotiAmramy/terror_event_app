from typing import List, Callable
import toolz as t
import pandas as pd

def insert_to_db_chunks(data: List, insert_func: Callable, chunks_size: int):
    [insert_func(chunk) for chunk in list(t.partition_all(chunks_size, data))]





def if_none(val):
    if isinstance(val, pd.Series):
        val = val.iloc[0] if not val.empty else None
    return None if pd.isna(val) else val