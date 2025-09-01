from app import app
from database_setup import db

with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")
