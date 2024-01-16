from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.database import User, db
from src.utils import AUTH_EXPIRATION_TIME

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    print("Login")
    data = request.get_json()
    print(data)
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.username ,expires_delta=AUTH_EXPIRATION_TIME)
        return jsonify(access_token=access_token, role=user.role), 200
    else:
        return {"message": "Invalid username or password"}, 401


@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return {"message": "Username already taken"}, 400

    # Create a new user
    new_user = User(username=data['username'], role='user')
    new_user.set_password(data['password'])

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201
