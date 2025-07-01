import repository.course_repository as course_repo
import repository.enrollment_repository as enroll_repo
from model.course import Course

def list_courses():
    return course_repo.get_all_courses()

def get_course(course_id):
    return course_repo.get_course_by_id(course_id)

def add_course(data):
    course = Course(None, data['title'], data['description'], data['duration'])
    course_repo.create_course(course)

def enroll_user_in_course(course_id, user_email):
    return enroll_repo.enroll_user(course_id, user_email)

def get_user_enrollments(user_email):
    return enroll_repo.get_enrollments_by_user(user_email)
