from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.database import db
from app.config import Config
from app.views.auth_routes import auth_bp
from app.views.account_routes import account_bp
from app.views.loan_routes import loan_bp
from app.views.beneficiary_routes import beneficiary_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(beneficiary_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
