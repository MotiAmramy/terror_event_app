from data_normalize.app.db.mongo_database import events_collection




def fetch_all_events_from_mongo():
    cursor = events_collection.find({})
    return list(cursor)


def most_deadly_attack_type_mongo():
    pipeline = [
        {"$unwind": "$attack_types"},
        {
            "$addFields": {
                "attack_score": {
                    "$add": [
                        {"$multiply": ["$fatalities", 2]},
                        {"$ifNull": ["$injuries", 0]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$attack_types",
                "total_attack_score": {"$sum": "$attack_score"}
            }
        },
        {"$sort": {"total_attack_score": -1}}
    ]
    return list(events_collection.aggregate(pipeline))


def average_casualties_per_region_mongo():
    pipeline = [
        {
            "$match": {
                "location.region": {"$ne": None}
            }
        },
        {
            "$addFields": {
                "attack_score": {
                    "$add": [
                        {"$multiply": ["$fatalities", 2]},
                        {"$ifNull": ["$injuries", 0]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$location.region",  # Group by region
                "avg_casualties": {"$avg": "$attack_score"},  # Average attack score
                "lat": {"$first": "$location.latitude"},  # Get latitude of first document
                "lon": {"$first": "$location.longitude"}  # Get longitude of first document
            }
        },
        {
            "$match": {
                "lat": {"$ne": None},
                "lon": {"$ne": None}  # Exclude records with null lat/lon
            }
        },
        {
            "$sort": {"avg_casualties": -1}  # Sort by average casualties in descending order
        }
    ]
    return list(events_collection.aggregate(pipeline))


def top_5_groups_with_most_casualties_mongo():
    pipeline = [
        {"$unwind": "$group_types"},
        {
            "$group": {
                "_id": "$group_types",
                "total_casualties": {"$sum": "$casualties"}
            }
        },
        {"$sort": {"total_casualties": -1}},
        {"$limit": 5}
    ]
    return list(events_collection.aggregate(pipeline))


def calculate_percentage_change_mongo():
    pipeline = [
        {"$addFields": {"year": {"$year": {"$toDate": "$date"}}}},

        # Group by region and year to calculate attack count
        {
            "$group": {
                "_id": {"region": "$location.region", "year": "$year"},
                "attack_count": {"$sum": 1},
                "lat": {"$first": "$location.latitude"},  # Get latitude of first document
                "lon": {"$first": "$location.longitude"}  # Get longitude of first document
            }
        },
        {"$sort": {"_id.region": 1, "_id.year": 1}},

        # Group by region to get first and last year attack counts
        {
            "$group": {
                "_id": "$_id.region",
                "first_year_data": {
                    "$first": {"year": "$_id.year", "attack_count": "$attack_count", "lat": "$lat", "lon": "$lon"}},
                "last_year_data": {
                    "$last": {"year": "$_id.year", "attack_count": "$attack_count", "lat": "$lat", "lon": "$lon"}}
            }
        },

        # Calculate percentage change and add fields
        {
            "$project": {
                "region": "$_id",
                "start_year": "$first_year_data.year",
                "end_year": "$last_year_data.year",
                "start_attack_count": "$first_year_data.attack_count",
                "end_attack_count": "$last_year_data.attack_count",
                "percentage_change_in_attack_count": {
                    "$multiply": [
                        {
                            "$divide": [
                                {
                                    "$subtract": [
                                        "$last_year_data.attack_count",
                                        "$first_year_data.attack_count"
                                    ]
                                },
                                "$first_year_data.attack_count"
                            ]
                        },
                        100
                    ]
                },
                "end_lat": "$last_year_data.lat",  # Get latitude for last year
                "end_lon": "$last_year_data.lon"  # Get longitude for last year
            }
        },

        # Filter out regions or lat/lon that are null
        {
            "$match": {
                "region": {"$ne": None},  # Exclude null regions
                "end_lat": {"$ne": None},  # Exclude null latitudes
                "end_lon": {"$ne": None}  # Exclude null longitudes
            }
        },

        # Match documents where end year exists
        {
            "$match": {
                "end_year": {"$exists": True}
            }
        }
    ]
    return list(events_collection.aggregate(pipeline))


def process_active_groups_mongo(region=None):
    pipeline = []

    # If region is provided, filter by region
    if region:
        pipeline.append({"$match": {"location.region": region}})

    # Unwind group types (to count events for each group)
    pipeline.extend([
        {"$unwind": "$group_types"},
        {
            "$group": {
                "_id": "$location.region",  # Group by region
                "most_active_group": {"$first": "$group_types"},  # Get the most active group type (first one)
                "event_count": {"$sum": 1},  # Count events for each group in the region
                "lat": {"$first": "$location.latitude"},  # Get the latitude of the region
                "lon": {"$first": "$location.longitude"}  # Get the longitude of the region
            }
        },
        {"$sort": {"event_count": -1}}  # Sort by event count in descending order
    ])

    # Match to exclude records with null lat, lon, or region values
    pipeline.append({
        "$match": {
            "lat": {"$ne": None},
            "lon": {"$ne": None},
            "_id": {"$ne": None}  # Exclude regions with null values
        }
    })

    pipeline.extend([
        {
            "$project": {
                "region": "$_id",  # Include the region name
                "most_active_group": 1,  # Include the most active group
                "event_count": 1,  # Include the count of events for the group
                "lat": 1,  # Include the latitude of the region
                "lon": 1  # Include the longitude of the region
            }
        }
    ])

    # Execute the aggregation and return the results
    return list(events_collection.aggregate(pipeline))

def get_groups_involved_in_same_attack_mongo():
    pipeline = [
        {"$unwind": "$group_types"},
        {
            "$group": {
                "_id": "$date",
                "unique_groups": {"$addToSet": "$group_types"}
            }
        },
        {
            "$match": {"$expr": {"$eq": [{"$size": "$unique_groups"}, 2]}}
        },
        {
            "$project": {
                "groups": "$unique_groups"
            }
        }
    ]
    result = list(events_collection.aggregate(pipeline))
    return result

def groups_with_common_targets(region=None, country=None):
    match_stage = {}
    if region:
        match_stage["location.region"] = region
    if country:
        match_stage["location.country"] = country

    pipeline = [
        {"$match": match_stage},
        {"$unwind": "$group_types"},
        {"$unwind": "$target_types"},
        {
            "$group": {
                "_id": {
                    "region": "$location.region",
                    "country": "$location.country",
                    "latitude": {"$ifNull": ["$location.latitude", None]},
                    "longitude": {"$ifNull": ["$location.longitude", None]},
                    "target": "$target_types"
                },
                "groups": {"$addToSet": "$group_types"}
            }
        },
        {
            "$match": {
                "$expr": {"$gt": [{"$size": "$groups"}, 1]}
            }
        },
        {
            "$project": {
                "_id": 0,
                "region": "$_id.region",
                "country": "$_id.country",
                "latitude": "$_id.latitude",
                "longitude": "$_id.longitude",
                "target": "$_id.target",
                "groups": 1
            }
        }
    ]

    return list(events_collection.aggregate(pipeline))



def groups_with_common_targets_by_year(region=None, country=None):
    match_stage = {}
    if region:
        match_stage["location.region"] = region
    if country:
        match_stage["location.country"] = country
    pipeline = [
        {"$match": match_stage},
        {"$unwind": "$group_types"},
        {"$unwind": "$target_types"},
        # הוספת שלב להוספת שנה מתוך התאריך
        {"$addFields": {"year": {"$year": {"$toDate": "$date"}}}},
        {
            "$group": {
                "_id": {"region": "$location.region", "country": "$location.country", "target": "$target_types", "year": "$year"},
                "groups": {"$addToSet": "$group_types"}
            }
        },
        {
            "$match": {
                "$expr": {"$gt": [{"$size": "$groups"}, 1]}
            }
        },
        {
            "$project": {
                "_id": 0,
                "region": "$_id.region",
                "country": "$_id.country",
                "target": "$_id.target",
                "year": "$_id.year",
                "groups": 1
            }
        }
    ]
    return list(events_collection.aggregate(pipeline))


def groups_using_same_attack_strategies(region=None):
    match_stage = {}
    if region:
        match_stage["location.region"] = region

    pipeline = [
        {"$unwind": "$attack_types"},
        {"$unwind": "$group_types"},
        {"$group": {
            "_id": {"region": "$location.region", "attack_type": "$attack_types"},
            "groups": {"$addToSet": "$group_types"},
            "lat": {"$first": "$location.latitude"},  # Get the first latitude for the region
            "lon": {"$first": "$location.longitude"}  # Get the first longitude for the region
        }},
        {"$match": {"$expr": {"$gt": [{"$size": "$groups"}, 1]}}},  # More than one group
        {"$match": {"_id.region": {"$ne": None}}},  # Exclude None regions
        {"$project": {
            "region": "$_id.region",
            "attack_type": "$_id.attack_type",
            "groups": 1,
            "lat": 1,  # Include latitude in the output
            "lon": 1  # Include longitude in the output
        }},
        {"$sort": {"region": 1}}  # Sort by region
    ]

    result = list(events_collection.aggregate(pipeline))
    return result


def unique_groups_by_country_or_region(country=None, region=None):
    match_stage = {}
    if country:
        match_stage["location.country"] = country
    elif region:
        match_stage["location.region"] = region

    pipeline = [
        {"$match": match_stage},
        {"$unwind": "$group_types"},
        {"$group": {
            "_id": "$location.country" if country else "$location.region",
            "unique_groups_count": {"$addToSet": "$group_types"},
            "average_lat": {"$avg": "$location.latitude"},
            "average_lon": {"$avg": "$location.longitude"}
        }},
        {"$project": {
            "_id": 0,
            "country_or_region": {"$ifNull": ["$_id", ""]},
            "unique_group_count": {"$size": "$unique_groups_count"},
            "latitude": "$average_lat",
            "longitude": "$average_lon"
        }}
    ]

    return list(events_collection.aggregate(pipeline))