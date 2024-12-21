from flask import Blueprint, jsonify, request
from analyze_data.app.db.repository.mongo_repository import fetch_all_events_from_mongo
from analyze_data.app.services.pandas_service import most_deadly_attack_type, average_casualties_per_region, \
    top_5_groups_with_most_casualties, calculate_percentage_change, process_active_groups, \
    get_groups_involved_in_same_attack

attack_blueprint = Blueprint('attack', __name__)




@attack_blueprint.route('/top_5_terror_attacks', methods=['GET'])
def top_5_terror_attacks():
    try:
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        result = most_deadly_attack_type(fetch_data_from_mongo)
        top_5 = request.args.get('top_5', type=bool, default=False)
        if top_5:
            result = result.head(5)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@attack_blueprint.route('/average_casualties_per_region', methods=['GET'])
def average_casualties_endpoint():
    try:
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        result = average_casualties_per_region(fetch_data_from_mongo)
        top_5 = request.args.get('top_5', type=bool, default=False)
        if top_5:
            result = result.head(5)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@attack_blueprint.route('/top_5_groups_with_most_casualties', methods=['GET'])
def top_5_groups_endpoint():
    try:
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        result = top_5_groups_with_most_casualties(fetch_data_from_mongo)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@attack_blueprint.route('/percentage_change_in_attacks', methods=['GET'])
def percentage_change_in_attacks():
    try:
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        result = calculate_percentage_change(fetch_data_from_mongo)
        top_5 = request.args.get('top_5', type=bool, default=False)
        if top_5:
            result = result.sort_values(by='percentage_change', ascending=False).head(5)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@attack_blueprint.route('/active_groups', methods=['GET'])
def active_groups():
    try:
        region = request.args.get('region', default=None)
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        top_groups = process_active_groups(fetch_data_from_mongo, region)
        return jsonify({
            'top_groups': top_groups.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@attack_blueprint.route('/groups_same_attack', methods=['GET'])
def groups_same_attack():
    try:
        fetch_data_from_mongo = fetch_all_events_from_mongo()
        groups = get_groups_involved_in_same_attack(fetch_data_from_mongo)
        return jsonify(groups)

    except Exception as e:
        return jsonify({"error": str(e)}), 500