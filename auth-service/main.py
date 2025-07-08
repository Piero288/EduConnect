from flask import Flask
from controller.auth_controller import auth_blueprint
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/auth')

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Auth Service Metrics', version='1.0.0')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050)
