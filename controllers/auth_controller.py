from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.config.database import db

class AuthController:
    @staticmethod
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

    @staticmethod
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401 