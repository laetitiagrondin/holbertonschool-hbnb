"""
Initialisation de l'application Flask HBnB.
Configure Flask et Flask-RESTX.
"""
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
<<<<<<< HEAD
=======
from app.api.v1.places import api as places_ns
>>>>>>> 22fff6f (Add app/__init__.py from app.api.v1.amenities import api as amenities_ns|from app.api.v1.places import api as places_ns|api.add_namespace(amenities_ns, path='/api/v1/amenities')|api.add_namespace(places_ns, path='/api/v1/places'))

def create_app():
    """
    Crée et configure l'instance de l'application Flask.
    """
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
<<<<<<< HEAD
=======
    api.add_namespace(places_ns, path='/api/v1/places')
>>>>>>> 22fff6f (Add app/__init__.py from app.api.v1.amenities import api as amenities_ns|from app.api.v1.places import api as places_ns|api.add_namespace(amenities_ns, path='/api/v1/amenities')|api.add_namespace(places_ns, path='/api/v1/places'))
    return app
