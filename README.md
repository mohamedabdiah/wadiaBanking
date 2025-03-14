# Wadia Banking API

A RESTful banking API built with Flask, SQLAlchemy, and JWT authentication.

## Features

- User authentication (register/login)
- Account management
- Transaction processing
- Loan management
- Beneficiary management

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wadiaBanking
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/banking_db
```

5. Create the database:
```bash
createdb banking_db
```

## Running the Application

1. Start the Flask development server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- POST `/register` - Register a new user
- POST `/login` - Login user and get JWT token

### Accounts
- POST `/account` - Create a new account
- GET `/account/<account_number>` - Get account details
- POST `/transaction` - Create a new transaction

### Loans
- POST `/loan` - Apply for a loan
- POST `/loan/<loan_id>/payment` - Make a loan payment

### Beneficiaries
- POST `/beneficiary` - Add a new beneficiary
- GET `/beneficiaries` - Get all beneficiaries

## Request/Response Examples

### Register User
```json
POST /register
{
    "first_name": "wadia",
    "last_name": "slamic",
    "email": "wadia@banking.com",
    "phone": "000000000",
    "password": "wadia123",
    "address": "12 aad jigjiga"
}
```

### Login
```json
POST /login
{
    "email": "wadia@banking.com",
    "password": "wadia@123"
}
```

### Create Account
```json
POST /account
{
    "account_type": "savings"
}
```

### Create Transaction
```json
POST /transaction
{
    "account_number": "00000000000",
    "transaction_type": "deposit",
    "amount": 1000.00
}
```

## Security

- All endpoints except `/register` and `/login` require JWT authentication
- Passwords are hashed using Werkzeug's security functions
- Database credentials are stored in environment variables
- JWT tokens expire after 1 hour

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
