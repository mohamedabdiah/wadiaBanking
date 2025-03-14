from datetime import datetime
from app.config.database import db

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)
    beneficiary_account = db.Column(db.String(20), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False) 