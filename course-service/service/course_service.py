import repository.course_repository as course_repo
import repository.enrollment_repository as enroll_repo
from configuration.config import logger
import requests
import os
from dotenv import load_dotenv
from model.course import Course

load_dotenv()

def list_courses():
    return course_repo.get_all_courses()

def get_course(course_id):
    return course_repo.get_course_by_id(course_id)

def add_course(data):
    course = Course(None, data['title'], data['description'], data['duration'])
    course_repo.create_course(course)


def enroll_user_in_course(course_id, token):
    try:
        auth_service_url = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:9050/auth')
        auth_api_url = f"{auth_service_url}/verify_token"
        response = requests.post(
            auth_api_url,
            json={"token": token}
        )
        if response.status_code != 200:
            logger.error("Token validation failed")
            return False, "Token validation failed"

        user_data = response.json()
        if not user_data.get("valid", False):
            return False, "Invalid token"

        user_email = user_data.get("user_email")
        if not user_email:
            return False, "User email not found in token"

    except Exception as e:
        logger.exception("Auth service not reachable")
        return False, "Auth service not reachable"

    success = enroll_repo.enroll_user(course_id, user_email)
    if success:
        return True, "Enrollment successful"
    else:
        return False, "User already enrolled"

def get_user_enrollments(user_email):
    return enroll_repo.get_enrollments_by_user(user_email)
