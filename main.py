from src.routes.download import download
from src.routes.user import user
from flask import Flask, request, send_from_directory, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
import uuid
from src import utils
from src.database import db, User
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'secret'


app.register_blueprint(download, url_prefix='/download')
app.register_blueprint(user, url_prefix='/user')


@app.route('/')
def home():
    return {"message": "Hello World!"}


if __name__ == '__main__':
    # Store download links temporarily in memory (consider using a more robust solution)
    app.run(debug=True, host='192.168.98.221', port=5000)
