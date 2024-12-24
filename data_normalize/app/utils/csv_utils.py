import os




def get_terror_event_csv_1_path() -> str:
    return os.path.join(os.path.dirname(__file__), '../../../csv_files', 'terror1_full.csv')

def get_terror_event_csv_2_path() -> str:
    return os.path.join(os.path.dirname(__file__), '../../../csv_files', 'terror2_full.csv')




def save_to_csv(df):
    try:
        output_path = "../../csv_files/merged_output.csv"
        df.to_csv(output_path, index=False, encoding='iso-8859-1')
        print(f"DataFrame successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")







columns_to_keep = [
        'date', "country", "city", "latitude", "longitude", "region",
        "target_type", 'target_type2', "attack_type", 'attack_type2', "perpetrator2", "perpetrator",
        "num_of_attackers", "injuries", "fatalities", "casualties", 'description', 'region'
    ]



columns_to_rename_df1 = {
        'region_txt': 'region',
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
    }