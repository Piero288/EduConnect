class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def get_user_id(self):
        return self.user_id
    
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password
    
    def set_name(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password    

    def set_email(self, email):
        self.email = email

    def to_dict(self):
        return {'user_id': self.user_id, 'name': self.name, 'email': self.email}
