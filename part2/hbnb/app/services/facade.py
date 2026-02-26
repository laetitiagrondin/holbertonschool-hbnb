"""
Module implémentant le pattern Facade pour coordonner les couches.
"""
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """ Facade pour gérer la communication entre les couches. """
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

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

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])
        
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Propriétaire non trouvé")

        place = Place(owner=owner, **place_data)
        
        # Ajout des amenities
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
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
