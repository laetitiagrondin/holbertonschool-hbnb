#!/usr/bin/python3
"""
Module base_model
=================
Définit la classe abstraite ``base_model`` dont héritent toutes les entités
du projet (User, Place, Review, Amenity).

Responsabilités de ce module :
    - Générer un identifiant universel unique (UUID v4) pour chaque instance.
    - Horodater automatiquement la création et les mises à jour.
    - Fournir des méthodes réutilisables de sauvegarde et de mise à jour en masse.

Dépendances :
    - ``uuid``     : génération d'identifiants UUID v4.
    - ``datetime`` : horodatage ISO 8601.
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Classe de base partagée par toutes les entités du projet HBnB.

    Attributs d'instance
    --------------------
    id : str
        Identifiant unique au format UUID v4 (ex. "550e8400-e29b-41d4-a716-446655440000").
        Stocké sous forme de chaîne pour faciliter la sérialisation JSON et le
        stockage dans les dépôts en mémoire.
    created_at : datetime
        Horodatage de la création de l'objet.  Défini une seule fois à
        l'instanciation et jamais modifié ensuite.
    updated_at : datetime
        Horodatage de la dernière modification.  Rafraîchi automatiquement par
        ``save()`` à chaque mutation.

    Pourquoi des UUIDs ?
    --------------------
    - **Unicité globale** : pas de collision entre plusieurs serveurs ou bases de données.
    - **Sécurité** : non-séquentiels, difficiles à deviner (contrairement aux entiers auto-incrémentés).
    - **Scalabilité** : les identifiants peuvent être générés côté client sans coordination serveur.
    """

    def __init__(self):
        """
        Initialise les trois attributs communs à toutes les entités.
        - ``id``         : UUID v4 converti en chaîne.
        - ``created_at`` : instant présent (datetime.now()).
        - ``updated_at`` : identique à ``created_at`` à la création.
        """
        # Génère un UUID v4 et le convertit en chaîne de caractères
        self.id = str(uuid.uuid4())

        # Enregistre l'instant de création — ne sera jamais modifié
        self.created_at = datetime.now()

        # Initialisé à la même valeur que created_at ; sera mis à jour
        # à chaque appel à save()
        self.updated_at = datetime.now()

    # ------------------------------------------------------------------
    # Méthodes de mutation
    # ------------------------------------------------------------------

    def save(self):
        """
        Rafraîchit le champ ``updated_at`` à l'instant courant.
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
