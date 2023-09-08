from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, password, name):
        self.id = id(self)  # Unique
        self.email = email  # Unique
        self.password = password
        self.name = name


registered_users = []
