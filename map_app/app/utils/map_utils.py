import os
import folium




def save_map(map):
    map_path = os.path.join("static", "map.html")
    map.save(map_path)


def get_color(average):
    if average < 10:
        return 'green'
    elif average < 30:
        return 'orange'
    return 'red'


def return_folium_settings_for_avg_casualties(data, popup_template):
    map = folium.Map(location=[20, 0], zoom_start=2)
    for item in data:
        lat = item.get("lat") or item.get("latitude") or item.get("end_lat")
        lon = item.get("lon") or item.get("longitude") or item.get("end_lon")
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(
                color=get_color(item['avg_casualties']),
                icon='info-sign'
            ),
            popup=popup_template.format(**item),
        ).add_to(map)
    save_map(map)

