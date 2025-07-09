from flask import Flask, request
from controller.user_controller import user_bp
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/users')

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'User Service Metrics', version='1.0.0')

werkzeug_logger = logging.getLogger('werkzeug')

@app.before_request
def mute_werkzeug_on_health_and_metrics():
    if request.path in ["/users/health", "/metrics"]:
        if werkzeug_logger.level != logging.ERROR:
            werkzeug_logger.setLevel(logging.ERROR)
    else:
        if werkzeug_logger.level != logging.INFO:
            werkzeug_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9051)
