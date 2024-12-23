from flask import Blueprint, request, jsonify

from analyze_data.app.db.repository.es_repository import build_search_query, execute_search

search_blueprint = Blueprint('search', __name__)



@search_blueprint.route('/search_keyword', methods=['GET'])
def search_keyword():
    try:
        keyword = request.args.get("keyword")
        query = build_search_query(keyword)
        results = execute_search(query=query)
        return jsonify({"count": len(results), "results": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


