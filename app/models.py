import re
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Method to hash the password before storing it
    def set_password(self, password):
        if self.is_valid_password(password):
            self.password_hash = generate_password_hash(password)
        else:
            raise ValueError("Invalid password format")

    # Method to verify the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Validates email format
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValueError("Invalid email format")
        return email

    # Validates username format
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 4:
            raise ValueError("Username must be at least 4 characters long")
        if not re.match(r'^[a-zA-Z0-9-_?!]+$', username):
            raise ValueError("Username can only contain letters, numbers, and the following special characters: - _ ? !")
        return username

    # Validates password format
    def is_valid_password(self, password):
        if len(password) < 8:
            return False
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=\-{}\[\]:;"\'<>,.?\/\\|`~]+$', password):
            return False
        return True

    # String representation for debugging
    def __repr__(self):
        return f'<User {self.username}>'
