import threading
import time
import requests
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer
from configuration.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_LIST, COURSE_SERVICE_URL, logger

def wait_for_topic(topic_name, timeout=10):
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    elapsed = 0
    while elapsed < timeout:
        metadata = admin_client.list_topics(timeout=5)
        if topic_name in metadata.topics:
            return True
        time.sleep(1)
        elapsed += 1
    return False

def create_topic_if_not_exists(topic_name):
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    metadata = admin_client.list_topics(timeout=5)

    if topic_name in metadata.topics:
        logger.info(f"Topic {topic_name} already exists.")
        return

    new_topic = NewTopic(topic=topic_name, num_partitions=2, replication_factor=1)
    admin_client.create_topics([new_topic])
    logger.info(f"Created topic {topic_name}.")

def consume_topic(topic_name):
    
    logger.info(f"Trying to consume topic: {topic_name}")

    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': f'subscriber-group-{topic_name}',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic_name])

    logger.info(f"Subscribed to topic: {topic_name}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Error in message: {msg.error()}")
                continue

            message_value = msg.value().decode('utf-8')
            logger.info(f"Received message on topic '{topic_name}': {message_value}")

            course_title = topic_name.replace("course-", "")
            notify_users_enrolled(course_title, message_value)

    except KeyboardInterrupt:
        logger.warning("Stopping consumer due to keyboard interrupt")
    finally:
        consumer.close()


def notify_users_enrolled(course_title, message):
    try:
        url = f"{COURSE_SERVICE_URL}/enrollments/emails?course_title={course_title}"
        logger.info(f"Calling course-service to retrieve users for course '{course_title}'")
        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to get users for course {course_title}: {response.text}")
            return

        users_enrolled = response.json()
        emails = users_enrolled.get("emails", [])
        logger.info(f"Notifying {len(emails)} users for course '{course_title}'")
        for email in emails:
            logger.info(f"Sending notice to {email}: {message}")
            #inviare un'email o salvare in un DB, per ora solo logging
    except Exception as e:
        logger.exception(f"Error while notifying users for course {course_title}: {str(e)}")


def start_kafka_consumers():
    
    logger.info("Starting Kafka topic consumers...")

    for topic in TOPIC_LIST:

        logger.info(f"Ensuring topic exists: {topic}")
        create_topic_if_not_exists(topic)

        if not wait_for_topic(topic, timeout=10):
            logger.error(f"Topic {topic} did not become available in time. Skipping consumer.")
            continue

        thread = threading.Thread(target=consume_topic, args=(topic,))
        thread.start()
        logger.info(f"Started consumer thread for topic: {topic}")
