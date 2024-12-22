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
                "_id": "$location.region",
                "avg_casualties": {"$avg": "$attack_score"}
            }
        },
        {"$sort": {"avg_casualties": -1}}
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
        {
            "$group": {
                "_id": {"region": "$location.region", "year": "$year"},
                "attack_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.region": 1, "_id.year": 1}},
        {
            "$group": {
                "_id": "$_id.region",
                "first_year_data": {"$first": {"year": "$_id.year", "attack_count": "$attack_count"}},
                "last_year_data": {"$last": {"year": "$_id.year", "attack_count": "$attack_count"}}
            }
        },
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
                }
            }
        },
        {
            "$match": {
                "end_year": {"$exists": True}
            }
        }
    ]
    return list(events_collection.aggregate(pipeline))


def process_active_groups_mongo(region=None):
    pipeline = []
    if region:
        pipeline.append({"$match": {"location.region": region}})
    pipeline.extend([
        {"$unwind": "$group_types"},
        {
            "$group": {
                "_id": "$group_types",
                "event_count": {"$sum": 1}
            }
        },
        {"$sort": {"event_count": -1}}
    ])
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
                "_id": {"region": "$location.region", "country": "$location.country", "target": "$target_types"},
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
            "groups": {"$addToSet": "$group_types"}
        }},
        {"$match": {"$expr": {"$gt": [{"$size": "$groups"}, 1]}}},
        {"$match": {"_id.region": {"$ne": None}}},
        {"$project": {
            "region": "$_id.region",
            "attack_type": "$_id.attack_type",
            "groups": 1
        }},
        {"$sort": {"region": 1}}  # מיון לפי אזור
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
            "unique_groups_count": {"$addToSet": "$group_types"}
        }},
        {"$project": {
            "_id": 0,
            "country_or_region": {"$ifNull": ["$_id", ""]},
            "unique_group_count": {"$size": "$unique_groups_count"}
        }}
    ]

    return list(events_collection.aggregate(pipeline))