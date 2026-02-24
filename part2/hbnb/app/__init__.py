"""
Initialisation de l'application Flask HBnB.
Configure Flask et Flask-RESTX.
"""
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    """
    Crée et configure l'instance de l'application Flask.
    """
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    return app
