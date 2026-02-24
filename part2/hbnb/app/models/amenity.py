#!/usr/bin/python3
"""
Module amenity
==============
Définit l'entité ``Amenity``, qui représente un équipement ou service
proposé par un lieu sur la plateforme HBnB (ex. Wi-Fi, Parking, Piscine).

Un équipement peut être associé à plusieurs lieux (relation many-to-many,
gérée côté ``Place`` via une liste d'instances ``Amenity``).

Règles de validation :
    - ``name`` : requis, longueur maximale de 50 caractères.

Dépendances :
    - ``base_model`` : classe parente fournissant id, created_at, updated_at.
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Représente un équipement ou service proposé par un lieu.

    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.

    Attributs d'instance
    --------------------
    name : str
        Nom de l'équipement (ex. "Wi-Fi", "Parking", "Piscine").
        Requis, 1 à 50 caractères.

    Relations
    ---------
    Un équipement peut être associé à plusieurs ``Place`` (many-to-many).
    Cette relation est gérée par la liste ``Place.amenities``.
    """

    def __init__(self, name: str):
        """
        Initialise un nouvel équipement et valide son nom immédiatement.

        Paramètres
        ----------
        name : str
            Nom de l'équipement (requis, ≤ 50 caractères).

        Lève
        ----
        ValueError
            Si le nom est vide ou dépasse 50 caractères.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__()
        self.name = name

    @property
    def name(self):
        """ Getter pour l'attribut privé _name. """
        return self.__name

    @name.setter
    def name(self, value):
        """
        Setter pour le nom avec logique de validation intégrée.
        Lève une ValueError si les contraintes ne sont pas respectées.
        """
        if not value or not isinstance(value, str):
            raise ValueError(
                "Le nom de l'équipement est obligatoire et doit être une chaîne."
            )
        if len(value) > 50:
            raise ValueError(
                "Le nom de l'équipement ne doit pas dépasser 50 caractères."
            )
        self.__name = value

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
