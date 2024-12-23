from flask import Flask

from analyze_data.app.routes.search_controller import search_blueprint
from analyze_data.app.routes.terror_attack_controller import terror_attack_blueprint


app = Flask(__name__)

app.register_blueprint(terror_attack_blueprint, url_prefix="/api")
app.register_blueprint(search_blueprint, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
