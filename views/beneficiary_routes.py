from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.beneficiary_controller import BeneficiaryController

beneficiary_bp = Blueprint('beneficiary', __name__)

@beneficiary_bp.route('/beneficiary', methods=['POST'])
@jwt_required()
def add_beneficiary():
    return BeneficiaryController.add_beneficiary()

@beneficiary_bp.route('/beneficiaries', methods=['GET'])
@jwt_required()
def get_beneficiaries():
    return BeneficiaryController.get_beneficiaries() 