import os
import mysql.connector
import logging 
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:9050/auth')

# DB connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        database=os.getenv("MYSQL_DB"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )

# LOGGING config
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'course_service.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("course_service")

#kafka
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "k8s":
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_K8S", "kafka0:29092")
else:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS_LOCAL", "kafka0:9092")