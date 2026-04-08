"""
Module implémentant le pattern Facade pour coordonner les couches.
"""
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    """ Facade pour gérer la communication entre les couches. """
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            user.update(user_data)
        return user
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity


    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])
        
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Propriétaire non trouvé")

        place = Place(owner=owner, **place_data)

        # Vérifier que chaque amenity existe
        for amenity_id in amenity_ids:
        # Si c'est un dict avec 'id' (venant du modèle nested)
            if isinstance(amenity_id, dict):
                amenity_id = amenity_id.get('id')
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} non trouvée")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if place:
            place.update(place_data)
        return place
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """ Relie un équipement existant à un lieu. """
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)
        
        if not place:
            raise ValueError("Lieu non trouvé")
        if not amenity:
            raise ValueError("Équipement non trouvé")
            
        place.add_amenity(amenity)
        
        return place

    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user:
            raise ValueError("Utilisateur non trouvé")
        if not place:
            raise ValueError("Lieu non trouvé")
        
        # Validation de la note (rating)
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
         # l'auteur ne peut pas évaluer son propre lieu
        if place.owner.id == review_data['user_id']:
            raise PermissionError("Vous ne pouvez pas évaluer votre propre lieu")

        # un seul avis par utilisateur par lieu
        existing = [
            r for r in self.review_repo.get_all()
            if r.place.id == review_data['place_id']
            and r.user.id == review_data['user_id']
        ]
        if existing:
            raise ValueError("Vous avez déjà laissé un avis pour ce lieu")

        from app.models.review import Review
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,   # On passe l'objet User
            place=place  # On passe l'objet Place
        )

        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        #review.update(review_data)
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}, 200
