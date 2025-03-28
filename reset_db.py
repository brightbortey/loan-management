# reset_db.py
from app import app, db, User, Transaction, Response 
from datetime import datetime


with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Create all tables again
    print("Database has been reset.")