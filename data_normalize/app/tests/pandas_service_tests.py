import pytest
import pandas as pd
from io import StringIO
from data_normalize.app.services.csv_process_service import *



# Sample data for testing
CSV_1_CONTENT = """
iyear,imonth,iday,country_txt,region_txt,nkill,nwound,summary,gname,gname2,attacktype1_txt,attacktype2_txt,targtype1_txt,targtype2_txt,nperps
2020,1,10,CountryA,RegionA,5,10,DescriptionA,PerpetratorA,PerpetratorB,AttackTypeA,AttackTypeB,TargetTypeA,TargetTypeB,3
2019,0,0,CountryB,RegionB,2,5,DescriptionB,Unknown,None,AttackTypeC,None,TargetTypeC,None,-99.0
"""

CSV_2_CONTENT = """
date,country,city,latitude,longitude,region,target_type,attack_type,perpetrator,description,fatalities,injuries
10-Jan-20,CountryC,CityA,12.34,56.78,RegionC,TargetTypeD,WeaponTypeA,PerpetratorC,DescriptionC,7,15
15-Feb-19,CountryD,CityB,,,,TargetTypeE,WeaponTypeB,Unknown,DescriptionD,4,8
"""

@pytest.fixture
def sample_df1():
    return pd.read_csv(StringIO(CSV_1_CONTENT), encoding="iso-8859-1", low_memory=False)

@pytest.fixture
def sample_df2():
    return pd.read_csv(StringIO(CSV_2_CONTENT), encoding="iso-8859-1", low_memory=False)

def test_preprocess_df1(sample_df1):
    processed_df1 = preprocess_df1(sample_df1)
    assert "country_txt" not in processed_df1.columns
    assert "region_txt" not in processed_df1.columns
    assert "casualties" in processed_df1.columns
    assert processed_df1["casualties"].iloc[0] == 15


def test_preprocess_df2(sample_df2):
    processed_df2 = preprocess_df2(sample_df2)
    assert "latitude" in processed_df2.columns
    assert "longitude" in processed_df2.columns
    assert processed_df2["perpetrator"].iloc[1] is None

def test_merge_datasets(sample_df1, sample_df2):
    processed_df1 = preprocess_df1(sample_df1)
    processed_df2 = preprocess_df2(sample_df2)
    merged_df = merge_datasets(processed_df1, processed_df2)
    assert len(merged_df) == 4  # 2 rows from each dataframe
    assert "date" in merged_df.columns

def test_select_columns(sample_df1, sample_df2):
    processed_df1 = preprocess_df1(sample_df1)
    processed_df2 = preprocess_df2(sample_df2)
    merged_df = merge_datasets(processed_df1, processed_df2)
    selected_df = select_columns(merged_df)
    expected_columns = [
        'date', "country", "city", "latitude", "longitude", "region",
        "target_type", 'target_type2', "attack_type", 'attack_type2', "perpetrator2", "perpetrator",
        "num_of_attackers", "injuries", "fatalities", "casualties", 'description', 'region'
    ]
    assert all(col in selected_df.columns for col in expected_columns)

