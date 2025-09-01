from flask import Flask, request
from controller.course_controller import course_bp
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)
app.register_blueprint(course_bp, url_prefix='/courses')

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Course Service Metrics', version='1.0.0')

werkzeug_logger = logging.getLogger('werkzeug')

@app.before_request
def mute_werkzeug_on_health_and_metrics():
    if request.path in ["/courses/health", "/metrics"]:
        if werkzeug_logger.level != logging.ERROR:
            werkzeug_logger.setLevel(logging.ERROR)
    else:
        if werkzeug_logger.level != logging.INFO:
            werkzeug_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9052)