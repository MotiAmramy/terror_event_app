import folium
import requests
from map_app.app.utils.map_utils import save_map, return_folium_settings_for_avg_casualties


def fetch_data_from_api(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return []

def generate_map(data, popup_template):
    map = folium.Map(location=[20, 0], zoom_start=2)
    for item in data:
        lat = item.get("lat") or item.get("latitude") or item.get("end_lat")
        lon = item.get("lon") or item.get("longitude") or item.get("end_lon")
        if lat and lon:
            folium.Marker(
                location=[lat, lon],
                popup=popup_template.format(**item),
            ).add_to(map)
    save_map(map)



def get_groups_with_same_target_generate_map(region=None, country=None):
    url = "http://127.0.0.1:5000/api/groups_with_same_target"
    params = {"region": region, "country": country}
    data = fetch_data_from_api(url, params)
    popup_template = "Groups: {groups}<br>Target: {target}<br>Country: {country}<br>Region: {region}"
    generate_map(data, popup_template)

def get_groups_using_same_attack_strategies_generate_map(region=None):
    url = "http://127.0.0.1:5000/api/groups_using_same_attack_strategies"
    params = {"region": region}
    data = fetch_data_from_api(url, params)
    popup_template = "Attack Type: {attack_type}<br>Groups count: {groups_count}<br>Region: {region}"
    generate_map(data, popup_template)

def get_regions_with_high_intergroup_activity_generate_map(region=None, country=None):
    url = "http://127.0.0.1:5000/api/regions_with_high_intergroup_activity"
    params = {"region": region, "country": country}
    data = fetch_data_from_api(url, params)
    popup_template = "Place: {country_or_region}<br>Group Count: {unique_group_count}"
    generate_map(data, popup_template)

def get_average_casualties_data_generate_map(limit=None):
    url = "http://127.0.0.1:5000/api/average_casualties_per_region"
    data = fetch_data_from_api(url)
    if limit:
        data = data[:int(limit)]
    popup_template = "Region: {_id}<br>Average Casualties: {avg_casualties}"
    return_folium_settings_for_avg_casualties(data, popup_template)

def get_percentage_change_in_attacks_generate_map(limit=None):
    url = "http://127.0.0.1:5000/api/percentage_change_in_attacks"
    data = fetch_data_from_api(url)
    if limit:
        data = data[:int(limit)]
    popup_template = (
        "Place: {_id}<br>Start Year: {start_year}<br>End Year: {end_year}<br>"
        "Start Attack Count: {start_attack_count}<br>End Attack Count: {end_attack_count}<br>"
        "Percentage Change: {percentage_change_in_attack_count}"
    )
    generate_map(data, popup_template)

def get_active_groups_generate_map(region=None, limit=None):
    url = "http://127.0.0.1:5000/api/active_groups"
    params = {"region": region} if region else {}
    data = fetch_data_from_api(url, params)
    if limit:
        data = data[:int(limit)]
    popup_template = "Region: {_id}<br>Most Active Group: {most_active_group}<br>Event Count: {event_count}"
    generate_map(data, popup_template)

def generate_map_from_keywords(keyword=None, limit=None):
    url = "http://127.0.0.1:5000/api/search/keywords"
    params = {"keyword": keyword}
    data = fetch_data_from_api(url, params)
    data = data['results']
    if limit:
        data = data[:int(limit)]
    popup_template = "Category: {category}<br>Country: {country}<br>Date: {date}"
    generate_map(data, popup_template)

def generate_map_from_news(keyword=None, limit=None):
    url = "http://127.0.0.1:5000/api/search/news"
    params = {"keyword": keyword}
    data = fetch_data_from_api(url, params)
    data = data['results']
    if limit:
        data = data[:int(limit)]
    popup_template = "Category: {category}<br>Country: {country}<br>Date: {date}"
    generate_map(data, popup_template)

def generate_map_from_historic(keyword=None, limit=None):
    url = "http://127.0.0.1:5000/api/search/historic"
    params = {"keyword": keyword}
    data = fetch_data_from_api(url, params)
    data = data['results']
    if limit:
        data = data[:int(limit)]
    popup_template = "Category: {category}<br>Country: {country}<br>Date: {date}"
    generate_map(data, popup_template)

def generate_map_from_combined(limit=None , keyword=None, start_date=None, end_date=None):
    url = "http://127.0.0.1:5000/api/search/combined"
    params = {"keyword": keyword, "start_date": start_date, "end_date": end_date}
    data = fetch_data_from_api(url, params)
    data = data['results']
    if limit:
        data = data[:int(limit)]
    popup_template = "Category: {category}<br>Country: {country}<br>Date: {date}"
    generate_map(data, popup_template)