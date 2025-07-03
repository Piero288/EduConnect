from flask import Flask
from service.kafka_consumer_service import start_kafka_consumers
from configuration.config import logger
from controller.subscriber_controller import subscriber_bp

app = Flask(__name__)
app.register_blueprint(subscriber_bp, url_prefix='/subscriber')

if __name__ == '__main__':
    logger.info("Starting Subscriber Service...")
    start_kafka_consumers()
    app.run(host='0.0.0.0', port=5005, debug=False)