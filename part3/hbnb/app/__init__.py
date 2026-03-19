from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    return app
