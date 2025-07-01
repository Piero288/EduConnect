from flask import Blueprint, request, jsonify
import service.course_service as course_service

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/getAll', methods=['GET'])
def get_all_courses():
    courses = course_service.list_courses()
    return jsonify(courses), 200

@course_bp.route('/getById/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = course_service.get_course(course_id)
    if course:
        return jsonify(course), 200
    return jsonify({"error": "Course not found"}), 404

@course_bp.route('/new', methods=['POST'])
def create_course():
    data = request.get_json()
    required_fields = ("title", "description", "duration")
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    course_service.add_course(data)
    return jsonify({"message": "Course created successfully"}), 201

@course_bp.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    if 'course_id' not in data or 'user_email' not in data:
        return jsonify({"error": "Missing course_id or user_email"}), 400
    success = course_service.enroll_user_in_course(data['course_id'], data['user_email'])
    if success:
        return jsonify({"message": "Enrollment successful"}), 200
    else:
        return jsonify({"message": "User already enrolled"}), 409

@course_bp.route('/enrollments', methods=['GET'])
def get_enrollments():
    user_email = request.args.get('user_email')
    if not user_email:
        return jsonify({"error": "Missing user_email"}), 400
    enrollments = course_service.get_user_enrollments(user_email)
    return jsonify(enrollments), 200
