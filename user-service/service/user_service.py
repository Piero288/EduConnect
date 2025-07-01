import repository.user_repository as repo
import bcrypt, os, requests
from configuration.config import logger
from model.user import User
from flask import jsonify

def authenticate_user(email, password):
    user = repo.get_user_by_email(email, False)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        auth_service_url = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:9050/auth')
        auth_api_url = f"{auth_service_url}/authenticate"
        payload = {'user_id': user.user_id}
        try:
            response = requests.post(auth_api_url, json=payload)
            if response.status_code == 200:
                token = response.json().get('token')
                logger.info("Authentication successful")
                return jsonify({"message": "Authentication successful", 
                                "user":user.to_dict(), 
                                "token": token}), 200
            else:
                logger.error(f"Token generation failed: {response.text}")
                return jsonify({"error": "Token generation failed", "details": response.text}), 500
        except Exception as e:
            logger.error(f"Error contacting auth service: {str(e)}")
            return jsonify({"error": "Error contacting auth service", "details": str(e)}), 500
    else:
        logger.error("Invalid email or password")
        return jsonify({"error": "Invalid email or password"}), 401


def list_users():
    return repo.get_all_users()

def get_user(user_id):
    return repo.get_user_by_id(user_id)

def get_user_by_email(email):
    return repo.get_user_by_email(email, True)

def create_user(data):
    user = repo.get_user_by_email(data["email"], False)
    if user:
        logger.error(f"There is already a user with this email address: {data['email']}")
        return False
    else:
        password_plain = data['password']
        hashed_password = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt())
        # Sovrascrivere la password con l'hash (in stringa)
        data['password'] = hashed_password.decode('utf-8')
        user = User(None, data["name"], data["email"], data["password"])
        return repo.create_user(user)

def update_user(data):
    password_plain = data['password']
    hashed_password = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt())
    data['password'] = hashed_password.decode('utf-8')
    user = User(data["user_id"], data["name"], data["email"], data["password"])
    return repo.update_user(user)

def delete_user(user_id):
    return repo.delete_user(user_id)
