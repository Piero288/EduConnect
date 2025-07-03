from flask import Blueprint, jsonify
from configuration.config import logger

subscriber_bp = Blueprint('subscriber', __name__)

@subscriber_bp.route('/')
def home():
    logger.info("Subscriber service is running")
    return jsonify({"message": "Subscriber service is running"}), 200