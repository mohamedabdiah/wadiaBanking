from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.loan import Loan, Payment
from app.config.database import db

class LoanController:
    @staticmethod
    def apply_for_loan():
        user_id = get_jwt_identity()
        data = request.get_json()
        
        loan = Loan(
            user_id=user_id,
            loan_type=data['loan_type'],
            amount=data['amount'],
            interest_rate=data['interest_rate'],
            duration_months=data['duration_months']
        )
        
        db.session.add(loan)
        db.session.commit()
        
        return jsonify({'message': 'Loan application submitted successfully'}), 201

    @staticmethod
    def make_loan_payment(loan_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return jsonify({'error': 'Loan not found'}), 404
        
        payment = Payment(
            loan_id=loan_id,
            amount=data['amount']
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({'message': 'Payment recorded successfully'}), 201 