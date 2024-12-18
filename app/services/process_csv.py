import pandas as pd
import os
from datetime import datetime



def get_terror_event_csv_1_path() -> str:
    return os.path.join(os.path.dirname(__file__), '../../', 'csv_files', 'terror1.csv.csv')


def get_terror_event_csv_2_path() -> str:
    return os.path.join(os.path.dirname(__file__), '../../', 'csv_files', 'terror2.csv.csv')


def load_csv_files(csv_1_path, csv_2_path):
    """Loads two CSV files into pandas DataFrames."""
    df1 = pd.read_csv(csv_1_path, encoding='iso-8859-1', low_memory=False)
    df2 = pd.read_csv(csv_2_path, encoding='iso-8859-1', low_memory=False)
    return df1, df2

def convert_to_datetime(row):
    """Converts year, month, and day columns to a datetime object."""
    try:
        return pd.to_datetime(f"{row['iyear']}-{row['imonth']}-{row['iday']}")
    except ValueError:
        return None

def preprocess_csv1(df1):
    """Preprocesses CSV 1: Converts columns, adds new ones, and renames columns."""

    df1.drop(['country'], axis=1, inplace=True)
    df1.rename(columns={
        'nkill': 'fatalities',
        'nwound': 'injuries',
        'summary': 'description',
        'country_txt': 'country',
        'gname': 'perpetrator',
        'gname2': 'perpetrator2',
        'attacktype1_txt': 'attack_type',
        'attacktype2_txt': 'attack_type2',
        'targtype1_txt': 'target_type',
        'targtype2_txt': 'target_type2',
        'nperps': 'num_of_attackers'
    }, inplace=True)
    df1['casualties'] = df1['fatalities'] + df1['injuries']

    return df1

def merge_datasets(df1, df2):
    df1['date'] = df1.apply(lambda row: convert_to_datetime(row), axis=1)
    df2['Date'] = pd.to_datetime(df2['Date'], format='%d-%b-%y', errors='coerce')
    """Merges the two DataFrames on specified columns."""
    print(df1['date'])
    print(df2['Date'])
    merged_df = pd.merge(
        df1,
        df2,
        how='outer',
        left_on=['date', 'country', 'city', 'description', 'fatalities', 'injuries', 'perpetrator', 'attack_type'],
        right_on=['Date','Country', 'City', 'Description', 'Fatalities', 'Injuries', 'Perpetrator', 'Weapon']
    )
    return merged_df

def select_columns(merged_df):
    """Selects and retains specific columns from the merged DataFrame."""
    columns_to_keep = [
        'date', "country", "city", "latitude", "longitude", "region_txt",
        "target_type", 'target_type2', "attack_type", 'attack_type2', "perpetrator2", "perpetrator",
        "num_of_attackers", "injuries", "fatalities", "casualties"
    ]
    return merged_df[columns_to_keep]

def save_to_csv(df, output_path):
    """Saves the DataFrame to a CSV file."""
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Merged file saved to {output_path}")

def process_and_merge(csv_1_path, csv_2_path, output_path):
    """Main function to process and merge two CSV files."""
    df1, df2 = load_csv_files(csv_1_path, csv_2_path)
    df1 = preprocess_csv1(df1)
    print(df1.columns)
    print(df2.columns)
    merged_df = merge_datasets(df1, df2)
    final_df = select_columns(merged_df)
    save_to_csv(final_df, output_path)

# Example usage
if __name__ == "__main__":
    csv_1_path = get_terror_event_csv_1_path()
    csv_2_path = get_terror_event_csv_2_path()
    output_path = "merged_output.csv"
    process_and_merge(csv_1_path, csv_2_path, output_path)

