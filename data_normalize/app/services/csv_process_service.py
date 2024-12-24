import pandas as pd
from data_normalize.app.utils.csv_utils import get_terror_event_csv_1_path, get_terror_event_csv_2_path, save_to_csv, \
    columns_to_keep, columns_to_rename_df1
from data_normalize.app.utils.pandas_utils import load_csv_files


def convert_to_datetime(row):
    try:
        day = row['iday'] if pd.notna(row['iday']) and row['iday'] != 0 else 1
        month = row['imonth'] if row['imonth'] != 0 else 1
        return pd.to_datetime(f"{row['iyear']}-{month}-{day}")
    except ValueError:
        return None


def preprocess_df1(df1):
    df1.columns = df1.columns.str.strip().str.lower()
    df1.drop(['country'], axis=1, inplace=True)
    df1.drop(['region'], axis=1, inplace=True)

    df1.rename(columns=columns_to_rename_df1, inplace=True)
    df1['casualties'] = df1['fatalities'] + df1['injuries']
    df1['date'] = df1.apply(lambda row: convert_to_datetime(row), axis=1)
    df1['perpetrator'] = df1['perpetrator'].replace(['Other', 'Unknown'], None)
    df1['attack_type'] = df1['attack_type'].replace(['Other', 'Unknown'], None)
    df1['num_of_attackers'] = df1['num_of_attackers'].replace([-99.0], None)
    return df1




def preprocess_df2(df2):
    df2.columns = df2.columns.str.strip().str.lower()
    df2['date'] = pd.to_datetime(df2['date'], format='%d-%b-%y', errors='coerce')
    df2['perpetrator'] = df2['perpetrator'].replace(['Other','Unknown'], None)

    df2.rename(columns={
        'weapon': 'attack_type',
        'description': 'description',
        'injuries': 'injuries',
        'fatalities': 'fatalities',
    }, inplace=True)
    for col in ['latitude', 'longitude', 'region', 'target_type', 'target_type2',
                'perpetrator2','attack_type2', 'num_of_attackers', 'casualties']:
        if col not in df2.columns:
            df2[col] = None
    return df2



def merge_datasets(df1, df2):
    merged_df = pd.concat([df1, df2], ignore_index=True)
    return merged_df


def select_columns(merged_df):
    columns = columns_to_keep
    return merged_df[columns]



def process_and_merge():
    csv_1_path = get_terror_event_csv_1_path()
    csv_2_path = get_terror_event_csv_2_path()
    df1, df2 = load_csv_files(csv_1_path, csv_2_path)
    df1 = preprocess_df1(df1)
    df2 = preprocess_df2(df2)
    merged_df = merge_datasets(df1, df2)
    final_df = select_columns(merged_df)
    save_to_csv(final_df)
    return final_df
