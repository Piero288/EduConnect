from flask import Blueprint, request, jsonify
from configuration.config import logger
import service.course_service as course_service

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/getAll', methods=['GET'])
def get_all_courses():
    logger.info("A new request has arrived to recover all courses")
    
    courses = course_service.list_courses()
    return jsonify(courses), 200

@course_bp.route('/getById/<int:course_id>', methods=['GET'])
def get_course(course_id):
    logger.info(f"A new request has arrived to retrieve the course with id {course_id}")
    
    course = course_service.get_course(course_id)
    
    if course:
        logger.info(f"Course with id {course_id}  found.")
        return jsonify(course), 200
    else:
        logger.error(f"Course with id {course_id} not found.")
        return jsonify({"error": "Course not found"}), 404

@course_bp.route('/new', methods=['POST'])
def create_course():
    logger.info("A new request has arrived to create a new course.")
    
    data = request.get_json()
    required_fields = ("title", "description", "duration")
    
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    course_service.add_course(data)
    
    logger.info("Course created successfully")
    return jsonify({"message": "Course created successfully"}), 201


@course_bp.route('/new_enroll', methods=['POST'])
def enroll():
    logger.info(f"A new request has arrived to create a new enrollment.")
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({"error": "Missing course_id"}), 400

    success, message = course_service.enroll_user_in_course(course_id, token)
    if success:
        logger.info(f"{message}")
        return jsonify({"message": message}), 200
    else:
        logger.error(f"{message}")
        return jsonify({"error": message}), 409 if message == "User already enrolled" else 401


@course_bp.route('/user_enrollments', methods=['GET'])
def get_user_enrollments():
    logger.info(f"A new request has arrived to retrieve enrollment for user")
   
    user_email = request.args.get('user_email')
    if not user_email:
        logger.error("Missing user_email")
        return jsonify({"error": "Missing user_email"}), 400
    
    enrollments = course_service.get_user_enrollments(user_email)
    logger.info(f"All enrollments for user: {user_email} are: {enrollments}")
    
    return jsonify(enrollments), 200

@course_bp.route('/enrollments/emails', methods=['GET'])
def get_enrolled_emails():
    course_title = request.args.get('course_title')
    if not course_title:
        logger.error("Missing course title")
        return jsonify({"error": "Missing course_title"}), 400

    course_title = course_title.replace("_", " ") if "_" in course_title else course_title

    logger.info(f"Fetching enrolled emails for course: {course_title}")
    emails = course_service.get_enrolled_emails_by_title(course_title)
    logger.info(f"Found {len(emails)} emails")
    return jsonify({"emails": emails}), 200
