from flask import Blueprint, request, jsonify
from configuration.config import logger
import service.user_service as user_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

# POST /auth -> autenticazione utenter
@user_bp.route('/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    logger.info(f"A new auth request has arrived for user: {data.get('email', 'UNKNOWN')}")
    
    if 'email' not in data or 'password' not in data:
        logger.error("Email and password are required")
        return jsonify({"error": "Email and password are required"}), 400

    return user_service.authenticate_user(data['email'], data['password'])

# GET /getAll → tutti gli utenti
@user_bp.route('/getAll', methods=['GET'])
def get_all_users():
    logger.info("new request has arrived to recover all users")
    users = user_service.list_users()
    return jsonify(users), 200

# GET /getById/<user_id> → singolo utente tramite id
@user_bp.route('/getById/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    logger.info(f"A new request has arrived to retrieve the user with id {user_id}")
    user = user_service.get_user(user_id)
    if user:
        logger.info(f"User with id {user_id} found.")
        return jsonify(user), 200
    else:
        logger.error(f"User with id {user_id} not found.")
        return jsonify({"error": "User not found"}), 404

# GET /getByEmail?<email> → singolo utente tramite email
@user_bp.route('/getByEmail', methods=['GET'])
def get_user_by_email():
    
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Missing email parameter"}), 400

    logger.info(f"A new request has arrived to retrieve the user with email {email}")
    user = user_service.get_user_by_email(email)
    if user:
        logger.info(f"User with email {email} found.")
        return jsonify(user), 200
    else:
        logger.error(f"User with email {email} not found.")
        return jsonify({"error": "User not found"}), 404

# POST /new → crea utente
@user_bp.route('/new', methods=['POST'])
def create_user():
    logger.info("A new request has arrived to create a new user.")
    data = request.get_json()
    if not all(k in data for k in ("name", "email", "password")):
        logger.error("Missing fields")
        return jsonify({"error": "Missing fields"}), 400
    
    success = user_service.create_user(data)
    
    if success:
        logger.info("User created successfully")
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"error": "User already exists or creation failed"}), 409

# PUT /update → aggiorna utente
@user_bp.route('/update', methods=['PUT'])
def update_user():
    data = request.get_json()
    if not all(k in data for k in ("user_id", "name", "email", "password")):
        logger.error("Missing fields")
        return jsonify({"error": "Missing fields"}), 400
    
    logger.info(f"A new request has arrived to update user with id {data['user_id']}.")
    success = user_service.update_user(data)
    if success:
        logger.info("User updated successfully")
        return jsonify({"message": "User updated successfully"}), 200
    else:
        logger.error("User not found or update failed")
        return jsonify({"error": "User not found or update failed"}), 404

# DELETE /delete/<user_id> → elimina utente
@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    logger.info(f"A new request has arrived to delete user with id {user_id}.")
    success = user_service.delete_user(user_id)
    if success:
        logger.info("User deleted successfully")
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        logger.error("User not found or delete failed")
        return jsonify({"error": "User not found or delete failed"}), 404
    
