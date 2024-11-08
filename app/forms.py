from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from .models import User

class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, message="Username must be at least 4 characters long"),
        Regexp(r'^[a-zA-Z0-9-_?!]+$', message="Username can only contain letters, numbers, and the following special characters: - _ ? !")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Invalid email address"),
        Length(max=120)
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+=\-{}\[\]:;"\'<>,.?\/\\|`~]+$', message="Password can only contain letters, numbers, and special characters")
    ])
    
    submit = SubmitField('Add User')

    # Custom validator to check if the username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
    
    # Custom validator to check if the email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
