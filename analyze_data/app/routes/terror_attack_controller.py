from flask import Blueprint, jsonify, request
from analyze_data.app.db.repository.mongo_repository import *

terror_attack_blueprint = Blueprint('attack', __name__)


@terror_attack_blueprint.route('/most_deadly_terror_attacks', methods=['GET'])
def most_deadly_terror_attacks():
    try:
        result = most_deadly_attack_type_mongo()
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            result = result[:5]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@terror_attack_blueprint.route('/average_casualties_per_region', methods=['GET'])
def average_casualties_endpoint():
    try:
        result = average_casualties_per_region_mongo()
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            result = result[:5]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@terror_attack_blueprint.route('/top_5_groups_with_most_casualties', methods=['GET'])
def top_5_groups_endpoint():
    try:
        result = top_5_groups_with_most_casualties_mongo()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@terror_attack_blueprint.route('/percentage_change_in_attacks', methods=['GET'])
def percentage_change_in_attacks():
    try:
        result = calculate_percentage_change_mongo()
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            result = sorted(result, key=lambda x: x['percentage_change_in_attack_count'], reverse=True)[:5]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@terror_attack_blueprint.route('/active_groups', methods=['GET'])
def active_groups():
    try:
        region = request.args.get('region', default=None)
        limit = request.args.get('limit', default=None)
        result = process_active_groups_mongo(region=region)

        if limit:
            result = result[:limit]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@terror_attack_blueprint.route('/groups_same_attack_by_year', methods=['GET'])
def groups_same_attack_by_year():
    try:
        region = request.args.get('region', default=None)
        country = request.args.get('country', default=None)
        result = groups_with_common_targets_by_year(region=region, country=country)
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            result = result[:5]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@terror_attack_blueprint.route('/groups_participate_same_attack', methods=['GET'])
def groups_participate_same_attack():
    try:
        result = get_groups_involved_in_same_attack_mongo()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@terror_attack_blueprint.route('/groups_with_same_target', methods=['GET'])
def groups_with_same_target():
    try:
        region = request.args.get('region', default=None)
        country = request.args.get('country', default=None)
        result = groups_with_common_targets(region=region, country=country)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@terror_attack_blueprint.route('/groups_using_same_attack_strategies', methods=['GET'])
def groups_using_same_attack_strategies_endpoint():
    try:
        region = request.args.get('region', default=None)
        result = groups_using_same_attack_strategies(region=region)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@terror_attack_blueprint.route('/regions_with_high_intergroup_activity', methods=['GET'])
def regions_with_high_intergroup_activity_endpoint():
    try:
        region = request.args.get('region', default=None)
        country = request.args.get('country', default=None)
        result = unique_groups_by_country_or_region(region=region, country=country)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

