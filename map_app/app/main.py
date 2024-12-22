from flask import Flask

from map_app.app.route import route_bp

app = Flask(__name__)
app.register_blueprint(route_bp)
if __name__ == "__main__":
    app.run(debug=True, port=5001)