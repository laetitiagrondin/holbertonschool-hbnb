#!/usr/bin/python3
"""
Module base_model
Définit la classe abstraite ``base_model`` dont héritent toutes les entités
du projet (User, Place, Review, Amenity).

Responsabilités de ce module :
    - Générer un identifiant universel unique (UUID v4) pour chaque instance.
    - Horodater automatiquement la création et les mises à jour.
    - Fournir des méthodes réutilisables de sauvegarde et de mise à jour en masse.
"""

import uuid
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """
    Classe abstraite SQLAlchemy — aucune table n'est créée pour elle.
    Toutes les entités héritent de cette classe pour partager
    les colonnes id, created_at et updated_at.
    """
    __abstract__ = True  # SQLAlchemy ne crée pas de table pour cette classe

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Force les valeurs immédiatement sans attendre le commit SQLAlchemy
        if not self.id:
            self.id = str(uuid.uuid4())
        now = datetime.utcnow()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now


    def save(self):
        """
        Rafraîchit le champ updated_at à l'instant courant.
        Doit être appelée après chaque modification d'un attribut afin de
        garder une trace fiable de la dernière mise à jour.
        """
        # Met à jour l'horodatage de modification à l'instant présent
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """
        Met à jour les attributs de l'objet à partir d'un dictionnaire.

        Seules les clés correspondant à des attributs **déjà existants** sont
        acceptées.  Les champs ``id`` et ``created_at`` sont protégés et ne
        peuvent jamais être modifiés via cette méthode.

        Les sous-classes peuvent surcharger ``update()`` pour ajouter leurs
        propres validations métier.

        Paramètres
        ----------
        data : dict
            Dictionnaire ``{nom_attribut: nouvelle_valeur}``.
            Les clés inconnues ou protégées sont silencieusement ignorées.
        """
        for key, value in data.items():
            # Protège l'identifiant et la date de création contre toute
            # modification accidentelle ou malveillante
            if key in ("id", "created_at"):
                continue

            # N'accepte que les attributs déjà déclarés sur l'objet
            if hasattr(self, key):
                setattr(self, key, value)

        # Rafraîchit automatiquement l'horodatage de dernière modification
        self.save()

    # ------------------------------------------------------------------
    # Sérialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Sérialise les attributs communs sous forme de dictionnaire Python.

        Les dates sont converties en chaînes ISO 8601 pour être compatibles
        avec le format JSON attendu par l'API REST.

        Les sous-classes enrichissent ce dictionnaire avec leurs propres
        attributs en appelant ``super().to_dict()`` puis en y ajoutant
        leurs champs spécifiques.

        Retour
        ------
        dict
            Dictionnaire contenant ``id``, ``created_at`` et ``updated_at``.
        """
        return {
            "id": self.id,
            # isoformat() produit une chaîne compatible JSON
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
