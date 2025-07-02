import os
import logging
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENVIRONMENT", "local")
print(f"ENVIRONMENT: {env}")
if env == "k8s":
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_K8S", "kafka0:29092")
else:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_LOCAL", "kafka0:9092")

print(f"KAFKA_BOOTSTRAP_SERVERS: {KAFKA_BOOTSTRAP_SERVERS}")

# LOGGING config
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'publisher.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("publisher")