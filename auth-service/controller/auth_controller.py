from flask import Blueprint, jsonify, request
from service.auth_service import generate_token, verify_token
from configuration.config import logger

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/authenticate', methods=['POST'])
def authenticate():
    logger.info(f"A new authenticate request has arrived.")
    
    data = request.json
    user_id = data.get('user_id')
    user_email = data.get('user_email')
    
    if not user_id or not user_email:
        logger.error("Missing userId or email")
        return jsonify({"success": False, "error": "Missing userId or email"}), 400

    token = generate_token(user_id, user_email)
    logger.info(f"Token generated successfully: {token}")
    return jsonify({"success": True, "token": token}), 200


@auth_blueprint.route('/verify_token', methods=['POST'])
def verify_token_route():
    logger.info("A new token verification request has arrived.")
    
    token = request.json.get('token')
    if not token:
        logger.error("Token missing")
        return jsonify({"success": False, "error": "Token missing"}), 400

    valid, payload_or_error = verify_token(token)
    if valid:
        logger.info("Token verified successfully")
        return jsonify({"valid": True,
                        "user_id": payload_or_error["user_id"],
                        "user_email": payload_or_error["user_email"]
                        }), 200
    else:
        logger.error(f"{payload_or_error}")
        return jsonify({"valid": False, "error": payload_or_error}), 401

