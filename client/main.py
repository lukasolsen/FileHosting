from src.routes.download import download
from src.routes.user import user
from flask import Flask
from flask_jwt_extended import JWTManager
import os
from src.database import db
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

app.secret_key = 'secret'


app.register_blueprint(download, url_prefix='/download')
app.register_blueprint(user, url_prefix='/user')


@app.route('/')
def home():
    return {"message": "Hello World!"}


if __name__ == '__main__':
    if os.getenv("location_type").lower() == "local":
        required_folders = ["files", "indexes", "images"]
        for folder in required_folders:
            path = os.path.join(os.getenv("local_path"), folder)
            if not os.path.exists(path):
                os.mkdir(path)

    app.run(debug=True, host=os.getenv("ip_address"), port=os.getenv("port"))
