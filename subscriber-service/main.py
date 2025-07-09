from flask import Flask, request
from service.kafka_consumer_service import start_kafka_consumers
from configuration.config import logger
from controller.subscriber_controller import subscriber_bp
import logging 

app = Flask(__name__)
app.register_blueprint(subscriber_bp, url_prefix='/subscriber')

werkzeug_logger = logging.getLogger('werkzeug')

@app.before_request
def mute_werkzeug_on_health_and_metrics():
    if request.path in ["/subscriber/health", "/metrics"]:
        if werkzeug_logger.level != logging.ERROR:
            werkzeug_logger.setLevel(logging.ERROR)
    else:
        if werkzeug_logger.level != logging.INFO:
            werkzeug_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("Starting Subscriber Service...")
    start_kafka_consumers()
    app.run(host='0.0.0.0', port=5005, debug=False)