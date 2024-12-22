import os
import folium
import requests


# Utility function to save the map
def save_map(map):
    map_path = os.path.join("static", "map.html")
    map.save(map_path)


def get_groups_with_same_target_generate_map(region=None, country=None):
    url = "http://127.0.0.1:5000/api/groups_with_same_target"
    params = {"region": region, "country": country}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        query_data = response.json()
    else:
        query_data = []

    # Create a base map centered at (20, 0) with zoom level 2
    map = folium.Map(location=[20, 0], zoom_start=2)

    # Iterate over the data and add markers for each group with coordinates
    for group in query_data:
        latitude = group.get('latitude')  # Use latitude
        longitude = group.get('longitude')  # Use longitude
        if latitude and longitude:
            folium.Marker(
                location=[latitude, longitude],
                popup=f"Groups: {', '.join(group['groups'])}<br>Target: {group['target']}<br>country: {group['country']}<br>region: {group['region']}",
            ).add_to(map),


    # Save the map to an HTML file
    save_map(map)


def get_groups_using_same_attack_strategies_generate_map(region=None):
    url = "http://127.0.0.1:5000/api/groups_using_same_attack_strategies"
    params = {"region": region}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        query_data = response.json()
    else:
        query_data = []
    map = folium.Map(location=[20, 0], zoom_start=2)
    for group in query_data:
        if group.get('lat') and group.get('lon'):
            folium.Marker(
                location=[group['lat'], group['lon']],
                popup=(
                    f"Attack Type: {group['attack_type']}<br>"
                    f"Groups: {', '.join(group['groups'])}<br>"
                    f"Region: {group['region']}"
                ),
            ).add_to(map)
    save_map(map)


def get_regions_with_high_intergroup_activity_generate_map(region=None, country=None):
    url = "http://127.0.0.1:5000/api/regions_with_high_intergroup_activity"
    params = {"region": region, "country": country}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        query_data = response.json()
    else:
        query_data = []

    map = folium.Map(location=[20, 0], zoom_start=2)
    for region_data in query_data:
        if region_data.get('latitude') and region_data.get('longitude'):
            folium.Marker(
                location=[region_data['latitude'], region_data['longitude']],
                popup=f"place: {region_data['country_or_region']}<br>Group num: {region_data['unique_group_count']}",
            ).add_to(map)
    save_map(map)

# Function to fetch data and generate the map
def get_average_casualties_data_generate_map(limit=None):
    url = "http://127.0.0.1:5000/api/average_casualties_per_region"
    response = requests.get(url)
    if response.status_code == 200:
        query_data = response.json()
        if limit:
            query_data = query_data[:int(limit)]
    else:
        query_data = []

    map = folium.Map(location=[20, 0], zoom_start=2)
    for place in query_data:
        if place.get('lat') and place.get('lon'):
            folium.Marker(
                location=[place['lat'], place['lon']],
                popup=f"Region: {place['_id']}<br>Average Casualties: {place['avg_casualties']}",
            ).add_to(map)
    save_map(map)

def get_percentage_change_in_attacks_generate_map(limit=None):
    url = "http://127.0.0.1:5000/api/percentage_change_in_attacks"
    response = requests.get(url)
    if response.status_code == 200:
        query_data = response.json()
        if limit:
            query_data = query_data[:int(limit)]
    else:
        query_data = []

    map = folium.Map(location=[20, 0], zoom_start=2)
    for place in query_data:
        if place.get('end_lat') and place.get('end_lon'):
            folium.Marker(
                location=[place['end_lat'], place['end_lon']],
                popup=(
                    f"Place: {place['_id']}<br>Start Year: {place['start_year']}<br>End Year: {place['end_year']}"
                    f"<br>Start Attack Count: {place['start_attack_count']}<br>End Attack Count: {place['end_attack_count']}"
                    f"<br>Percentage Change: {place['percentage_change_in_attack_count']}%"
                ),
            ).add_to(map)
    save_map(map)

def get_active_groups_generate_map(region=None, limit=None):
    url = "http://127.0.0.1:5000/api/active_groups"
    params = {}
    if region:
        params["region"] = region
    response = requests.get(url, params=params)
    if response.status_code == 200:
        query_data = response.json()
        if limit:
            query_data = query_data[:int(limit)]
    else:
        query_data = []

    map = folium.Map(location=[20, 0], zoom_start=2)
    for place in query_data:
        if place.get('lat') and place.get('lon'):
            folium.Marker(
                location=[place['lat'], place['lon']],
                popup=(
                    f"Region: {place['_id']}<br>Most Active Group: {place['most_active_group']}"
                    f"<br>Event Count: {place['event_count']}"
                ),
            ).add_to(map)
    save_map(map)
