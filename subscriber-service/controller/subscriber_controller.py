from flask import Blueprint
from configuration.config import logger

subscriber_bp = Blueprint('subscriber', __name__)

@subscriber_bp.route("/health", methods=["GET"])
def health_check():
    return "OK", 200
