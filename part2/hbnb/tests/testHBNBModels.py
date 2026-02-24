#!/usr/bin/python3
import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime

class TestHBNBModels(unittest.TestCase):

    # ------------------------------------------------------------------
    # AXE 1 : "SE PASSE BIEN" (Succès de création et sérialisation)
    # ------------------------------------------------------------------

    def test_user_creation_success(self):
        """Test la création réussie d'un utilisateur."""
        u = User(first_name="John", last_name="Doe", email="john@example.com")
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.email, "john@example.com")
        self.assertIsInstance(u.id, str)
        self.assertIsInstance(u.created_at, datetime)

    def test_amenity_to_dict(self):
        """Test que la sérialisation contient les bonnes clés."""
        a = Amenity(name="WiFi")
        d = a.to_dict()
        self.assertEqual(d['name'], "WiFi")
        self.assertIn('id', d)
        self.assertIn('created_at', d)

    def test_place_with_owner_success(self):
        """Test la création d'un lieu avec un propriétaire valide."""
        u = User(first_name="Owner", last_name="User", email="owner@test.com")
        p = Place(title="Villa", description="Belle", price=100.0, 
                  latitude=45.0, longitude=1.0, owner=u)
        self.assertEqual(p.owner.first_name, "Owner")

    # ------------------------------------------------------------------
    # AXE 2 : "SE PASSE MAL" (Erreurs de validation attendues)
    # ------------------------------------------------------------------

    def test_user_invalid_email(self):
        """Vérifie qu'un email mal formé lève une ValueError."""
        with self.assertRaises(ValueError):
            User(first_name="A", last_name="B", email="invalid-email")

    def test_place_negative_price(self):
        """Vérifie qu'un prix négatif est refusé."""
        u = User(first_name="A", last_name="B", email="a@b.com")
        with self.assertRaises(ValueError):
            Place(title="T", description="D", price=-10.0, 
                  latitude=0, longitude=0, owner=u)

    def test_amenity_name_too_long(self):
        """Vérifie la limite de 50 caractères pour Amenity."""
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)

    def test_review_invalid_rating(self):
        """Vérifie que la note doit être entre 1 et 5."""
        u = User(first_name="A", last_name="B", email="a@b.com")
        p = Place("T", "D", 10, 0, 0, u)
        with self.assertRaises(ValueError):
            Review(text="Bof", rating=6, place=p, user=u)

    # ------------------------------------------------------------------
    # AXE 3 : "AUTRE CHOSE ATTENDU" (Logique métier et protection)
    # ------------------------------------------------------------------

    def test_base_model_id_protection(self):
        """Vérifie que l'ID ne peut pas être modifié via update()."""
        a = Amenity(name="Clim")
        original_id = a.id
        a.update({"id": "new-id", "name": "Chauffage"})
        self.assertEqual(a.id, original_id)
        self.assertEqual(a.name, "Chauffage")

    def test_updated_at_on_save(self):
        """Vérifie que updated_at change après une modification."""
        u = User("John", "Doe", "j@d.com")
        old_updated_at = u.updated_at
        u.first_name = "Johnny"
        u.save()
        self.assertGreater(u.updated_at, old_updated_at)

    def test_place_add_amenity_no_duplicate(self):
        """Vérifie que add_amenity évite les doublons (identités)."""
        u = User("A", "B", "a@b.com")
        p = Place("T", "D", 10, 0, 0, u)
        wifi = Amenity("WiFi")
        p.add_amenity(wifi)
        p.add_amenity(wifi) # Tentative de doublon
        self.assertEqual(len(p.amenities), 1)

    def test_serialization_extended(self):
        """Vérifie que Place.to_dict() inclut les détails de l'owner."""
        u = User("Marc", "L", "m@l.com")
        p = Place("Studio", "Petit", 50, 48.8, 2.3, u)
        data = p.to_dict()
        self.assertEqual(data['owner']['first_name'], "Marc")
        self.assertIsInstance(data['owner'], dict)

if __name__ == '__main__':
    unittest.main()
# ------------------------------------------------------------------
    # COMPLÉMENTS DE COUVERTURE
    # ------------------------------------------------------------------

    def test_place_invalid_owner_type(self):
        """Vérifie que l'owner doit être une instance de User et rien d'autre."""
        with self.assertRaises(ValueError):
            Place("T", "D", 10, 0, 0, owner="Pas un User")

    def test_place_add_review_logic(self):
        """Vérifie le rattachement d'une review et l'import tardif."""
        u = User("A", "B", "a@b.com")
        p = Place("T", "D", 10, 0, 0, u)
        r = Review(text="Super", rating=5, place=p, user=u)
        p.add_review(r)
        self.assertIn(r, p.reviews)
        self.assertEqual(len(p.reviews), 1)

    def test_place_summary_dict(self):
        """Vérifie que le résumé est bien plus court que le dict complet."""
        u = User("A", "B", "a@b.com")
        p = Place("Villa", "Desc", 100, 0, 0, u)
        summary = p.to_summary_dict()
        self.assertIn('title', summary)
        self.assertNotIn('owner', summary) # Le summary ne doit pas avoir l'owner
        self.assertNotIn('amenities', summary)

    def test_user_is_admin_strict_bool(self):
        """Vérifie que is_admin n'accepte que des booléens (validation stricte)."""
        u = User("A", "B", "a@b.com")
        with self.assertRaises(ValueError):
            u.is_admin = "True" # C'est un string, pas un bool, doit lever ValueError
