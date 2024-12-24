from flask import Blueprint, request, jsonify
from analyze_data.app.db.repository.es_repository import build_search_query, execute_search, \
    search_by_category_and_keyword, search_by_keyword_and_date_range

search_blueprint = Blueprint('search', __name__)



@search_blueprint.route('/search/keywords', methods=['GET'])
def search_keyword():
    try:
        keyword = request.args.get("keyword")
        query = build_search_query(keyword)
        results = execute_search(query=query)
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            results = results[:5]
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500



@search_blueprint.route('/search/news', methods=['GET'])
def search_keyword_in_news():
    try:
        keyword = request.args.get("keyword")
        query = search_by_category_and_keyword(category="nowadays terror attack", keyword=keyword)
        results = execute_search(query=query)
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            results = results[:5]
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500



@search_blueprint.route('/search/historic', methods=['GET'])
def search_keyword_in_historic_news():
    try:
        keyword = request.args.get("keyword")
        query = search_by_category_and_keyword(category="historical terror attack", keyword=keyword)
        results = execute_search(query=query)
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            results = results[:5]
        return jsonify({"count": len(results), "results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500





@search_blueprint.route('/search/combined', methods=['GET'])
def search_keyword_combined():
    try:
        keyword = request.args.get("keyword")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        query = search_by_keyword_and_date_range(start_date, end_date, keyword)
        results = execute_search(query=query)
        limit = request.args.get('top_5', type=bool, default=False)
        if limit:
            result = results[:5]
        return jsonify({"count": len(result), "results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
