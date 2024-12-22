from flask import Flask
from analyze_data.app.routes.attack_controller import terror_attack_blueprint


app = Flask(__name__)

app.register_blueprint(terror_attack_blueprint, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
