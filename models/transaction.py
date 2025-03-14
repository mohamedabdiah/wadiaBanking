from datetime import datetime
from app.config.database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow) 