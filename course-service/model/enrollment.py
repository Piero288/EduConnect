class Enrollment:
    def __init__(self, enrollment_id, course_id, user_email):
        self.enrollment_id = enrollment_id
        self.course_id = course_id
        self.user_email = user_email
    
    def get_enrollment_id(self):
        return self.enrollment_id
        
    def get_course_id(self):
        return self.title
    
    def set_course_id(self, course_id):
        self.course_id = course_id
    
    def get_user_email(self):
        return self.user_email
    
    def set_user_email(self, user_email):
        self.user_email = user_email

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "course_id": self.course_id,
            "user_email": self.user_email
        }
