from app import app, db

with app.app_context():
    db.create_all()  # This will create all tables defined in your models