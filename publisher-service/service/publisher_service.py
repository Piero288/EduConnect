from confluent_kafka import Producer
from configuration.config import KAFKA_BOOTSTRAP_SERVERS
import json
from configuration.config import logger

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def publish_to_course_topic(course_title, message):
    topic = f"course-{course_title.replace(' ', '_').lower()}"
    logger.info(f"Publishing message to topic: {topic}")
    producer.produce(topic, json.dumps(message).encode('utf-8'), callback=delivery_report)
    producer.flush()
