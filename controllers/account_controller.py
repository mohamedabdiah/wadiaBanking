from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.account import Account
from app.models.transaction import Transaction
from app.config.database import db
import random
import string

class AccountController:
    @staticmethod
    def generate_account_number():
        return ''.join(random.choices(string.digits, k=10))

    @staticmethod
    def create_account():
        user_id = get_jwt_identity()
        data = request.get_json()
        
        account = Account(
            user_id=user_id,
            account_number=AccountController.generate_account_number(),
            account_type=data['account_type']
        )
        
        db.session.add(account)
        db.session.commit()
        
        return jsonify({
            'message': 'Account created successfully',
            'account_number': account.account_number
        }), 201

    @staticmethod
    def get_account(account_number):
        user_id = get_jwt_identity()
        account = Account.query.filter_by(account_number=account_number, user_id=user_id).first()
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
            
        return jsonify({
            'account_number': account.account_number,
            'account_type': account.account_type,
            'balance': float(account.balance)
        }), 200

    @staticmethod
    def create_transaction():
        user_id = get_jwt_identity()
        data = request.get_json()
        
        account = Account.query.filter_by(account_number=data['account_number'], user_id=user_id).first()
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        if data['transaction_type'] == 'withdrawal' and float(data['amount']) > float(account.balance):
            return jsonify({'error': 'Insufficient funds'}), 400
        
        transaction = Transaction(
            account_id=account.id,
            transaction_type=data['transaction_type'],
            amount=data['amount']
        )
        
        if data['transaction_type'] == 'deposit':
            account.balance += float(data['amount'])
        elif data['transaction_type'] == 'withdrawal':
            account.balance -= float(data['amount'])
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({'message': 'Transaction completed successfully'}), 201 