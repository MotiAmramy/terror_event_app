from flask import Blueprint, render_template, request
from .map_service import *



route_bp = Blueprint('event', __name__)

@route_bp.route("/", methods=["GET", "POST"])
def home():
    selected_query = request.form.get("query_type", "average_casualties")
    region = request.form.get("region", "")
    country = request.form.get("country", "")
    limit = request.form.get("limit", None)

    if selected_query == "average_casualties":
        get_average_casualties_data_generate_map(limit=limit)
    elif selected_query == "percentage_change_in_attacks":
        get_percentage_change_in_attacks_generate_map(limit=limit)
    elif selected_query == "active_groups":
        get_active_groups_generate_map(region=region, limit=limit)
    elif selected_query == "groups_with_same_target":
        get_groups_with_same_target_generate_map(region=region, country=country)
    elif selected_query == "groups_using_same_attack_strategies":
        get_groups_using_same_attack_strategies_generate_map(region=region)
    elif selected_query == "regions_with_high_intergroup_activity":
        get_regions_with_high_intergroup_activity_generate_map(region=region, country=country)

    return render_template("index.html", selected_query=selected_query, region=region, country=country, limit=limit)