from flask import Flask
from controller.user_controller import user_bp
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/users')

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'User Service Metrics', version='1.0.0')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9051)
