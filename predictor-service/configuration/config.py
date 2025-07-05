from dotenv import load_dotenv
import os
import logging 

load_dotenv()
# Base URL del servizio Prometheus
PROMETHEUS_BASE_URL = os.getenv("PROMETHEUS_URL", "http://prometheus:9090")

# LOGGING config
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'predictor_service.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("predictor")