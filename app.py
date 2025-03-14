from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Account, Transaction, Loan, Payment, Beneficiary
from config import Config
import random
import string

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'error': 'Phone number already registered'}), 400
    
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        address=data.get('address')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    account = Account(
        user_id=user_id,
        account_number=generate_account_number(),
        account_type=data['account_type']
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({
        'message': 'Account created successfully',
        'account_number': account.account_number
    }), 201

@app.route('/account/<account_number>', methods=['GET'])
@jwt_required()
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

@app.route('/transaction', methods=['POST'])
@jwt_required()
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

@app.route('/loan', methods=['POST'])
@jwt_required()
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

@app.route('/loan/<int:loan_id>/payment', methods=['POST'])
@jwt_required()
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

@app.route('/beneficiary', methods=['POST'])
@jwt_required()
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

@app.route('/beneficiaries', methods=['GET'])
@jwt_required()
def get_beneficiaries():
    user_id = get_jwt_identity()
    beneficiaries = Beneficiary.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': b.id,
        'beneficiary_name': b.beneficiary_name,
        'beneficiary_account': b.beneficiary_account,
        'bank_name': b.bank_name
    } for b in beneficiaries]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 