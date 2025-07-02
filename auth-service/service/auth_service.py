import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET', 'your_secret_key')

def generate_token(user_id, user_email, expiration_minutes=60):
    payload = {
        'user_id': user_id,
        'user_email': user_email,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        user_email= decoded_token.get("user_email")
        return True, {
            "user_id": user_id,
            "user_email": user_email
        }
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"
