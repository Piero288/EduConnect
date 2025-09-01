import os
import logging
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

# Ambiente (local o k8s)
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "k8s":
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_K8S", "kafka0:29092")
else:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_LOCAL", "kafka0:9092")

COURSE_SERVICE_URL = os.getenv("COURSE_SERVICE_URL", "http://course-service:9052/courses")

TOPICS = os.getenv("TOPICS", "")
TOPIC_LIST = [topic.strip() for topic in TOPICS.split(",") if topic.strip()]

# Logging
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'subscriber.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("subscriber")
