from configuration.config import get_db_connection
from model.enrollment import Enrollment
import logging

logger = logging.getLogger(__name__)

def enroll_user(course_id, user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM enrollments WHERE course_id = %s AND user_email = %s",
        (course_id, user_email)
    )
    if cursor.fetchone()[0] > 0:
        cursor.close()
        conn.close()
        return False  # Già iscritto

    cursor.execute(
        "INSERT INTO enrollments (course_id, user_email) VALUES (%s, %s)",
        (course_id, user_email)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_enrollments_by_user(user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollments WHERE user_email = %s", (user_email,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Enrollment(*row).to_dict() for row in rows]

def get_emails_by_course_title(course_title):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT e.user_email
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE c.title = %s
    """
    cursor.execute(query, (course_title,))
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return emails
