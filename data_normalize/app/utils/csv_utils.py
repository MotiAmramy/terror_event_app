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
