import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL"),
    "user": os.getenv("USER_SERVICE_URL"),
    "course": os.getenv("COURSE_SERVICE_URL"),
}
