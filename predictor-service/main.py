from flask import Flask, request
from controller.predictor_controller import predictor_bp
import logging 

app = Flask(__name__)
app.register_blueprint(predictor_bp, url_prefix="/predictor")

werkzeug_logger = logging.getLogger('werkzeug')

@app.before_request
def mute_werkzeug_on_health_and_metrics():
    if request.path in ["/predictor/health", "/metrics"]:
        if werkzeug_logger.level != logging.ERROR:
            werkzeug_logger.setLevel(logging.ERROR)
    else:
        if werkzeug_logger.level != logging.INFO:
            werkzeug_logger.setLevel(logging.INFO)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9055, debug=True)
