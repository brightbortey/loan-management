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
    name_of_debtor = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    amount_owing = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    guarantor1_name = db.Column(db.String(150), nullable=False)
    guarantor1_contact = db.Column(db.String(150), nullable=False)
    guarantor2_name = db.Column(db.String(150), nullable=False)
    guarantor2_contact = db.Column(db.String(150), nullable=False)
    remarks = db.Column(db.Text, nullable=True)