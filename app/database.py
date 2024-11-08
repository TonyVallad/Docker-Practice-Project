from .models import db

# Initialize the database
def init_db():
    db.create_all()  # This will create all tables based on the models defined in models.py
