from itertools import combinations

import pandas as pd


def most_deadly_attack_type(data):
    df = pd.DataFrame(data)
    df_exploded = df.explode('attack_types')
    df_exploded['attack_score'] = df_exploded.apply(
        lambda row: calculate_attack_score(row), axis=1
    )
    grouped = df_exploded.groupby('attack_types').agg(
        total_attack_score=('attack_score', 'sum')
    )
    grouped_sorted = grouped.sort_values(by='total_attack_score', ascending=False)
    result = grouped_sorted.reset_index().to_dict(orient='records')
    return result




def calculate_attack_score(row):
    return (row['fatalities'] * 2 if pd.notna(row['fatalities']) else 0) + \
           (row['injuries'] if pd.notna(row['injuries']) else 0)



def average_casualties_per_region(data):
    df = pd.json_normalize(data, sep='_')
    df['attack_score'] = df.apply(calculate_attack_score, axis=1)
    region_avg = df.groupby(['location_region'])['attack_score'].mean().reset_index()
    region_avg.rename(columns={'attack_score': 'avg_casualties'}, inplace=True)
    return region_avg.to_dict(orient='records')


def top_5_groups_with_most_casualties(data):
    df = pd.DataFrame(data)
    df_exploded = df.explode('group_types')
    group_casualties = df_exploded.groupby('group_types')['casualties'].sum().reset_index()
    top_5_groups = group_casualties.sort_values(by='casualties', ascending=False).head(5)

    # Return the result as a list of dictionaries for easy JSON conversion
    return top_5_groups.to_dict(orient='records')


def calculate_percentage_change(data):
    df = pd.json_normalize(data, sep='_')
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_data = df.groupby(['location_region', 'year']).size().reset_index(name='attack_count')
    result = yearly_data.groupby('location_region').apply(
        lambda group: {
            'region_name': group['location_region'].iloc[0],
            'start_year': int(group['year'].iloc[0]),
            'end_year': int(group['year'].iloc[-1]),
            'start_year_attack_count': int(group['attack_count'].iloc[0]),
            'end_year_attack_count': int(group['attack_count'].iloc[-1]),
            'percentage_change_in_attack_count': float(  # More informative key
                (group['attack_count'].iloc[-1] - group['attack_count'].iloc[0]) / group['attack_count'].iloc[0] * 100)

        }
    ).reset_index(drop=True)
    return result.tolist()


def process_active_groups(data, region=None):
    df = pd.DataFrame(data)
    if region:
        df = df[df['location_region'] == region]
    df_exploded = df.explode('group_types')
    group_counts = df_exploded.groupby('group_types').size().reset_index(name='event_count')
    top_groups = group_counts.sort_values(by='event_count', ascending=False).head(5)
    return top_groups


def get_groups_involved_in_same_attack(data):
    df = pd.DataFrame(data)
    df_exploded = df.explode('group_types')
    df_exploded['event_identifier'] = df_exploded['description'] + df_exploded['date'].astype(str)
    event_group_counts = df_exploded.groupby('event_identifier')['group_types'].nunique()
    multi_group_events = event_group_counts[event_group_counts > 1].index
    df_filtered = df_exploded[df_exploded['event_identifier'].isin(multi_group_events)]
    pairs = []
    for event_id, group_list in df_filtered.groupby('event_identifier')['group_types']:
        group_combinations = list(combinations(sorted(group_list.unique()), 2))
        pairs.extend(group_combinations)
    return pairs