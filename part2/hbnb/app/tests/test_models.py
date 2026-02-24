"""
Module de tests unitaires pour les modèles de l'application HBnB.
"""
import unittest
from app.models.user import User
from app.models.place import Place


class TestBaseModels(unittest.TestCase):
    """
    Classe de tests pour vérifier la logique métier de base.
    """

    def test_user_creation(self):
        """ Test de la création d'un utilisateur. """
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertIsNotNone(user.id)

    def test_place_relationship(self):
        """ Test de la relation entre un lieu et son propriétaire. """
        owner = User(first_name="Alice", last_name="Smith", email="alice@test.com")
        place = Place(
            title="Apartment",
            description="Nice place",
            price=100.0,
            latitude=37.7,
            longitude=-122.4,
            owner=owner
        )
        self.assertEqual(place.owner.first_name, "Alice")
        self.assertEqual(len(place.reviews), 0)

if __name__ == '__main__':
    unittest.main()
