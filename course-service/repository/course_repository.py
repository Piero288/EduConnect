from configuration.config import get_db_connection
from model.course import Course
import logging

logger = logging.getLogger(__name__)

def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Course(*row).to_dict() for row in rows]

def get_course_by_id(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Course(*row).to_dict() if row else None

def create_course(course):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO courses (title, description, duration) VALUES (%s, %s, %s)",
        (course.title, course.description, course.duration)
    )
    conn.commit()
    cursor.close()
    conn.close()
