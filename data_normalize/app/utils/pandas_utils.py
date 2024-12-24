import pandas as pd



def if_none(val):
    if isinstance(val, pd.Series):
        val = val.iloc[0] if not val.empty else None
    return None if pd.isna(val) else val