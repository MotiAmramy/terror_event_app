from datetime import datetime

from flask import Blueprint, request, jsonify

from analyze_data.app.db.repository.es_repository import build_search_query, execute_search, \
    search_by_category_and_keyword, search_by_keyword_and_date_range

search_blueprint = Blueprint('search', __name__)



@search_blueprint.route('/search/keywords', methods=['GET'])
def search_keyword():
    try:
        keyword = request.args.get("keyword")
        if keyword:
            query = build_search_query(keyword)
            results = execute_search(query=query)
            return jsonify({"count": len(results), "results": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500



@search_blueprint.route('/search/news', methods=['GET'])
def search_keyword_in_news():
    try:
        keyword = request.args.get("keyword")
        if keyword:
            query = search_by_category_and_keyword(category="nowadays terror attack", keyword=keyword)
            results = execute_search(query=query)
            return jsonify({"count": len(results), "results": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500



@search_blueprint.route('/search/historic', methods=['GET'])
def search_keyword_in_historic_news():
    try:
        keyword = request.args.get("keyword")
        if keyword:
            query = search_by_category_and_keyword(category="historical terror attack", keyword=keyword)
            results = execute_search(query=query)
            return jsonify({"count": len(results), "results": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500





@search_blueprint.route('/search/combined', methods=['GET'])
def search_keyword_combined():
    try:
        keyword = request.args.get("keyword")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        if not keyword:
            raise ValueError("Keyword is required.")
        if not start_date or not end_date:
            raise ValueError("Both start_date and end_date are required.")
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")
        query = search_by_keyword_and_date_range(start_date, end_date, keyword)
        results = execute_search(query=query)
        return jsonify({"count": len(results), "results": results}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
