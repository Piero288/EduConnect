import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL"),
    "users": os.getenv("USER_SERVICE_URL"),
    "courses": os.getenv("COURSE_SERVICE_URL"),
}
