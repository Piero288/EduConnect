from flask import Flask, request
from controller.publisher_controller import publisher_bp
import logging 

app = Flask(__name__)
app.register_blueprint(publisher_bp, url_prefix='/publisher')

werkzeug_logger = logging.getLogger('werkzeug')

@app.before_request
def mute_werkzeug_on_health_and_metrics():
    if request.path in ["/publisher/health", "/metrics"]:
        if werkzeug_logger.level != logging.ERROR:
            werkzeug_logger.setLevel(logging.ERROR)
    else:
        if werkzeug_logger.level != logging.INFO:
            werkzeug_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)