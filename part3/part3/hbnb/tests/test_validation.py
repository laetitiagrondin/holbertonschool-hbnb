"""
Module de tests unitaires pour valider l'encapsulation (attributs privés)
et la logique de validation des setters dans les modèles.
"""
import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class TestModelValidation(unittest.TestCase):
    """
    Tests vérifiant que les setters lèvent des erreurs pour des données
    invalides et que les attributs privés sont correctement utilisés.
    """

    def test_user_email_validation(self):
        """ Vérifie que le setter d'email rejette les formats invalides. """
        # Test avec un email invalide
        with self.assertRaises(ValueError):
            User("Jean", "Dupont", "email-invalide")
        
        # Vérification de l'attribut privé
        user = User("Jean", "Dupont", "jean@test.com")
        self.assertEqual(user.email, "jean@test.com")

    def test_user_name_length(self):
        """ Vérifie que le prénom ne dépasse pas 50 caractères. """
        long_name = "a" * 51
        with self.assertRaises(ValueError):
            User(long_name, "Dupont", "jean@test.com")

    def test_amenity_name_validation(self):
        """ Vérifie que l'équipement a un nom valide. """
        with self.assertRaises(ValueError):
            Amenity("")  # Nom vide
        
        amenity = Amenity("Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_place_price_validation(self):
        """ Vérifie que le prix du lieu est strictement positif. """
        owner = User("Alice", "Smith", "alice@test.com")
        with self.assertRaises(ValueError):
            Place("Villa", "Desc", -10, 45.0, 5.0, owner)

    def test_place_coordinates(self):
        """ Vérifie les limites de latitude et longitude. """
        owner = User("Alice", "Smith", "alice@test.com")
        # Latitude hors limites (> 90)
        with self.assertRaises(ValueError):
            Place("Villa", "Desc", 100, 95.0, 5.0, owner)

    def test_review_rating_limits(self):
        """ Vérifie que la note est comprise entre 1 et 5. """
        owner = User("Alice", "Smith", "alice@test.com")
        place = Place("Villa", "Desc", 100, 45.0, 5.0, owner)
        
        with self.assertRaises(ValueError):
            Review("Super", 6, place, owner)  # Note > 5
        
        with self.assertRaises(ValueError):
            Review("Bof", 0, place, owner)    # Note < 1

    def test_review_instance_validation(self):
        """ Vérifie que place et user sont des instances valides. """
        owner = User("Alice", "Smith", "alice@test.com")
        with self.assertRaises(ValueError):
            # On passe une chaîne au lieu d'un objet Place
            Review("Texte", 5, "Pas un lieu", owner)

if __name__ == '__main__':
    unittest.main()
