class Course:
    def __init__(self, course_id, title, description, duration):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.duration = duration
    
    def get_course_id(self):
        return self.course_id
    
    def get_title(self):
        return self.title
    
    def set_course_id(self, title):
        self.title = title
        
    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description
        
    def get_duration(self):
        return self.duration
    
    def set_duration(self, duration):
        self.duration = duration
    

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "duration": self.duration
        }