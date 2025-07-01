from configuration.config import get_db_connection, logger
from model.user import User

def get_all_users():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [User(*row).to_dict() for row in cursor.fetchall()]
        return users
    except Exception as e:
        logger.error(f"Failed to retrieve all users: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_by_id(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        return User(*row).to_dict() if row else None
    except Exception as e:
        logger.error(f"Failed to retrieve user by id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_by_email(email, public):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if public:
            return User(*row).to_dict() if row else None
        else:
            return User(*row) if row else None
    except Exception as e:
        logger.error(f"Failed to retrieve user by email: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_user(user: User):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (user.name, user.email, user.password)
        )
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_user(user: User):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name=%s, email=%s, password=%s WHERE user_id=%s",
            (user.name, user.email, user.password, user.user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return False  # Nessun utente aggiornato
        return True
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_user(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return False  # Nessun utente aggiornato
        return True
    except Exception as e:
        logger.error(f"Failed to delete user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
