import pandas as pd

from data_normalize.app.utils.csv_utils import get_terror_event_csv_1_path, get_terror_event_csv_2_path


def if_none(val):
    if isinstance(val, pd.Series):
        val = val.iloc[0] if not val.empty else None
    return None if pd.isna(val) else val



def load_csv_files(csv_1_path, csv_2_path):
    df1 = pd.read_csv(csv_1_path, encoding='iso-8859-1', low_memory=False)
    df2 = pd.read_csv(csv_2_path, encoding='iso-8859-1', low_memory=False)
    return df1, df2
