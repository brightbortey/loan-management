# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin' or 'customer'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debtor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # New fields added
    account_number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(150), nullable=False)
    arrears = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(250), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)
    comments = db.Column(db.Text, nullable=True)