from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.loan_controller import LoanController

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/loan', methods=['POST'])
@jwt_required()
def apply_for_loan():
    return LoanController.apply_for_loan()

@loan_bp.route('/loan/<int:loan_id>/payment', methods=['POST'])
@jwt_required()
def make_loan_payment(loan_id):
    return LoanController.make_loan_payment(loan_id) 