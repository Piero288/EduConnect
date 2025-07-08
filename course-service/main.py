from flask import Flask
from controller.course_controller import course_bp
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.register_blueprint(course_bp, url_prefix='/courses')

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Course Service Metrics', version='1.0.0')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9052)