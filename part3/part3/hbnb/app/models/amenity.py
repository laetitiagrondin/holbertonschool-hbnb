#!/usr/bin/python3
"""
Module amenity mappé a SQLalchemy
Définit l'entité ``Amenity``, qui représente un équipement ou service
proposé par un lieu sur la plateforme HBnB (ex. Wi-Fi, Parking, Piscine).

Un équipement peut être associé à plusieurs lieux (relation many-to-many,
gérée côté ``Place`` via une liste d'instances ``Amenity``).
"""

from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Représente un équipement ou service proposé par un lieu.

    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.
    Un équipement peut être associé à plusieurs ``Place`` (many-to-many).
    Cette relation est gérée par la liste ``Place.amenities``.
    """

    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name: str, **kwargs):
        """
        Initialise un nouvel équipement et valide son nom immédiatement.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__(**kwargs)
        self.name = name

    @db.validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Le nom est obligatoire (max 50 caractères).")
        return value


    # ------------------------------------------------------------------
    # Mise à jour
    # ------------------------------------------------------------------

    def update(self, data: dict):
        """
        Met à jour le nom de l'équipement.

        Seul le champ ``name`` est modifiable.  La validation est relancée
        après la mise à jour pour garantir la cohérence.

        Paramètres
        ----------
        data : dict
            Dictionnaire pouvant contenir la clé ``"name"`` avec sa nouvelle valeur.
            Les autres clés sont ignorées.

        Lève
        ----
        ValueError
            Si le nouveau nom ne respecte pas les contraintes.
        """
        # Met à jour le nom uniquement s'il est fourni dans le dictionnaire
        if "name" in data:
            self.name = data["name"]

        # Rafraîchit l'horodatage de dernière modification
        self.save()
    
    # Sérialisation
    
    def to_dict(self) -> dict:
        """
        Sérialise l'équipement.
        """
        #renvoie id, created_at, updated_at
        base = super().to_dict()
        base["name"] = self.name
        return base
