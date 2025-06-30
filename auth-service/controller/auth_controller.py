from flask import Blueprint, jsonify, request
from service.auth_service import generate_token, verify_token

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"success": False, "error": "User ID missing"}), 400

    token = generate_token(user_id)
    return jsonify({"success": True, "token": token}), 200

@auth_blueprint.route('/verify_token', methods=['POST'])
def verify_token_route():
    token = request.json.get('token')
    if not token:
        return jsonify({"success": False, "error": "Token missing"}), 400

    valid, payload_or_error = verify_token(token)
    if valid:
        return jsonify({"valid": True, "user_id": payload_or_error})
    else:
        return jsonify({"valid": False, "error": payload_or_error}), 401

