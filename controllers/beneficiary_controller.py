from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.beneficiary import Beneficiary
from app.config.database import db

class BeneficiaryController:
    @staticmethod
    def add_beneficiary():
        user_id = get_jwt_identity()
        data = request.get_json()
        
        beneficiary = Beneficiary(
            user_id=user_id,
            beneficiary_name=data['beneficiary_name'],
            beneficiary_account=data['beneficiary_account'],
            bank_name=data['bank_name']
        )
        
        db.session.add(beneficiary)
        db.session.commit()
        
        return jsonify({'message': 'Beneficiary added successfully'}), 201

    @staticmethod
    def get_beneficiaries():
        user_id = get_jwt_identity()
        beneficiaries = Beneficiary.query.filter_by(user_id=user_id).all()
        
        return jsonify([{
            'id': b.id,
            'beneficiary_name': b.beneficiary_name,
            'beneficiary_account': b.beneficiary_account,
            'bank_name': b.bank_name
        } for b in beneficiaries]), 200 