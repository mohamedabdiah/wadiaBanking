from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.account_controller import AccountController

account_bp = Blueprint('account', __name__)

@account_bp.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    return AccountController.create_account()

@account_bp.route('/account/<account_number>', methods=['GET'])
@jwt_required()
def get_account(account_number):
    return AccountController.get_account(account_number)

@account_bp.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    return AccountController.create_transaction() 