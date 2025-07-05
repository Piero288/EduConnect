from flask import Flask
from controller.predictor_controller import predictor_bp

app = Flask(__name__)
app.register_blueprint(predictor_bp, url_prefix="/predictor")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9055, debug=True)
