"""
Initialisation de l'application Flask HBnB.
Configure Flask et Flask-RESTX.
"""
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.extensions import bcrypt, jwt, db
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

# Instance SQLAlchemy importée par les modèles et le repository



def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'instance de l'application Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Autorise les requêtes cross-origin depuis le client web
    CORS(app, origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080"
    ])
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    # Initialisation des extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Création de l'admin par défaut au démarrage
    with app.app_context():
        db.create_all()
        _create_admin()

    return app

def _create_admin():
    """
    Crée un utilisateur administrateur par défaut si aucun n'existe.
    Email    : admin@hbnb.com
    Password : admin1234
    """
    from app.services import facade
    from app.extensions import bcrypt

    # On ne crée l'admin que s'il n'existe pas déjà
    if facade.get_user_by_email('admin@hbnb.com'):
        return

    hashed = bcrypt.generate_password_hash('admin1234').decode('utf-8')
    facade.create_user({
        'first_name': 'Admin',
        'last_name':  'HBnB',
        'email':      'admin@hbnb.com',
        'password':   hashed,
        'is_admin':   True
    })
    print('>>> Administrateur créé : admin@hbnb.com / admin1234')
