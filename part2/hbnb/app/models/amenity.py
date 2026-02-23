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

        # Validation immédiate après affectation
        self._validate()

    # ------------------------------------------------------------------
    # Validation interne
    # ------------------------------------------------------------------

    def _validate(self):
        """
        Vérifie que le nom de l'équipement respecte les contraintes métier.

        Contrôles effectués :
            - ``name`` : non vide et longueur ≤ 50 caractères.

        Lève
        ----
        ValueError
            Si le nom est vide ou trop long.
        """
        # Le nom doit être une chaîne non vide d'au plus 50 caractères
        if not self.name or len(self.name) > 50:
            raise ValueError(
                "Le champ 'name' de l'équipement est obligatoire "
                "et doit contenir au maximum 50 caractères."
            )

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

        # Revalide après modification
        self._validate()

        # Rafraîchit l'horodatage de dernière modification
        self.save()

    # ------------------------------------------------------------------
    # Sérialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Sérialise l'équipement sous forme de dictionnaire JSON-compatible.

        Étend le dictionnaire de base (``BaseModel.to_dict()``) avec le
        champ ``name``.

        Retour
        ------
        dict
            Dictionnaire contenant id, name, created_at et updated_at.
        """
        # Récupère le dictionnaire de base (id, created_at, updated_at)
        base = super().to_dict()

        # Ajoute le nom de l'équipement
        base["name"] = self.name
        return base
