from flask import Blueprint, request, jsonify
from service.publisher_service import publish_to_course_topic
from configuration.config import logger

publisher_bp = Blueprint('publisher', __name__)

@publisher_bp.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

@publisher_bp.route('/publish_notice', methods=['POST'])
def publish_notice():
    logger.info("A new request to publish notice has arrived.")
    data = request.get_json()
    required_fields = ['course_title', 'title', 'content', 'date']

    if not all(field in data for field in required_fields):
        logger.error("Missing fields in request")
        return jsonify({"error": "Missing fields"}), 400

    message = {
        "title": data["title"],
        "content": data["content"],
        "date": data["date"]
    }

    publish_to_course_topic(data["course_title"], message)
    logger.info(f"Published message: {message}")
    return jsonify({"message": "Notice published successfully"}), 200