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

def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'instance de l'application Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Autorise les requêtes cross-origin depuis le client web
    CORS(app, origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ])
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    
    # Initialisation des extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Ajout des espaces de noms (Namespaces)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Initialisation de la base de données et des données de test
    with app.app_context():
        # IMPORTANT : Import des modèles ici pour éviter l'erreur "failed to locate name 'Review'"
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity
        
        db.create_all()
        
        try:
            from app.services import facade
            seed_data(facade)
        except ImportError:
            print(" Erreur : Impossible d'importer la facade depuis app.services")

    return app

def seed_data(facade_instance):
    """Initialisation : Admin, Test User, Amenities, Place et Review"""
    print(" Génération des données de démonstration...")
    
    try:
        # 1. Création des UTILISATEURS
        existing_users = facade_instance.get_all_users()
        
        # Création Admin
        admin = next((u for u in existing_users if u.email == "admin@hbnb.com"), None)
        if not admin:
            admin = facade_instance.create_user({
                "first_name": "Admin", 
                "last_name": "HBnB", 
                "email": "admin@hbnb.com", 
                "password": "admin123"
            })
            print(" Admin créé.")
        
        # Création Utilisateur Test
        test_user = next((u for u in existing_users if u.email == "test@hbnb.com"), None)
        if not test_user:
            test_user = facade_instance.create_user({
                "first_name": "Jean", 
                "last_name": "Test", 
                "email": "test@hbnb.com", 
                "password": "password123"
            })
            print(" Utilisateur Test créé.")

        # 2. Création des ÉQUIPEMENTS
        # On crée les objets pour les lier ensuite
        wifi = facade_instance.create_amenity({"name": "WiFi"})
        clim = facade_instance.create_amenity({"name": "Climatisation"})

        # 3. Création de la PLACE (Appartement de l'Admin)
        existing_places = facade_instance.get_all_places()
        place = None
        if not existing_places:
            place = facade_instance.create_place({
                "title": "Appartement de luxe",
                "description": "Superbe vue sur la tour Eiffel. Très calme et lumineux.",
                "price": 200.0,
                "latitude": 48.8584,
                "longitude": 2.2945,
                "owner_id": admin.id
            })
            
            # Tentative sécurisée d'ajout d'équipements
            try:
                if hasattr(facade_instance, 'add_amenity_to_place'):
                    facade_instance.add_amenity_to_place(place.id, wifi.id)
                    facade_instance.add_amenity_to_place(place.id, clim.id)
            except Exception:
                print(" Note : Liaison équipements ignorée")
            
            print(" Place créée.")
        else:
            place = existing_places[0]

        # 4. CRÉATION DE LA REVIEW (Avis de Jean Test sur la place de l'Admin)
        # On vérifie si la place a déjà des reviews pour ne pas doubler
        existing_reviews = facade_instance.get_reviews_by_place(place.id)
        if not existing_reviews:
            facade_instance.create_review({
                "text": "Séjour incroyable ! La vue est encore plus belle en vrai. Je recommande vivement.",
                "rating": 5,
                "user_id": test_user.id,
                "place_id": place.id
            })
            print(" Review de test ajoutée.")

    except Exception as e:
        print(f" Erreur lors du seeding : {e}")
