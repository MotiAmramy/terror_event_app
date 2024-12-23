import os


def save_map(map):
    map_path = os.path.join("static", "map.html")
    map.save(map_path)
