#!/usr/bin/python3
"""
Module review
=============
Définit l'entité ``Review``, qui représente un avis laissé par un utilisateur
sur un lieu de la plateforme HBnB.

Un avis :
    - Appartient à exactement un ``Place`` (le lieu évalué).
    - Est rédigé par exactement un ``User`` (l'auteur).
    - Contient un texte libre et une note numérique de 1 à 5.

Règles de validation :
    - ``text``   : requis, ne peut pas être vide.
    - ``rating`` : entier compris entre 1 et 5 inclus.
    - ``place``  : doit être une instance valide de ``Place``.
    - ``user``   : doit être une instance valide de ``User``.

Dépendances :
    - ``base_model`` : classe parente fournissant id, created_at, updated_at.
    - ``user``       : référence à l'auteur de l'avis.
    - ``place``      : référence au lieu évalué.
"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """
    Représente un avis rédigé par un utilisateur à propos d'un lieu.

    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.

    Attributs d'instance
    --------------------
    text : str
        Contenu textuel de l'avis.  Requis, ne peut pas être vide.
    rating : int
        Note attribuée au lieu, comprise entre 1 (très mauvais) et 5 (excellent).
    place : Place
        Instance ``Place`` représentant le lieu évalué.
    user : User
        Instance ``User`` représentant l'auteur de l'avis.

    Relations
    ---------
    - Un avis est rattaché à **un seul lieu** (``place``).
    - Un avis est rédigé par **un seul utilisateur** (``user``).
    - Le lieu maintient une liste de ses avis (``Place.reviews``).
    """

    def __init__(self, text: str, rating: int, place: Place, user: User):
        """
        Initialise un nouvel avis et valide immédiatement ses attributs.

        Paramètres
        ----------
        text : str
            Contenu de l'avis (requis, non vide).
        rating : int
            Note de 1 à 5 inclus.
        place : Place
            Instance ``Place`` valide du lieu évalué.
        user : User
            Instance ``User`` valide de l'auteur de l'avis.

        Lève
        ----
        ValueError
            Si le texte est vide, la note hors plage, ou les références invalides.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__()

        self.text   = text
        # Conversion en int pour accepter les chaînes numériques éventuelles
        self.rating = int(rating)

        # Références vers les entités liées
        self.place = place  # Lieu évalué par cet avis
        self.user  = user   # Auteur de l'avis

        # Validation immédiate après affectation
        self._validate()

    # ------------------------------------------------------------------
    # Validation interne
    # ------------------------------------------------------------------

    def _validate(self):
        """
        Vérifie que les attributs de l'avis respectent les contraintes métier.

        Contrôles effectués :
            - ``text``   : chaîne non vide.
            - ``rating`` : entier entre 1 et 5 inclus.
            - ``place``  : instance de la classe ``Place``.
            - ``user``   : instance de la classe ``User``.

        Lève
        ----
        ValueError
            Si le texte est vide, la note invalide, ou les références incorrectes.
        """
        # Le texte de l'avis ne peut pas être vide
        if not self.text:
            raise ValueError("Le contenu de l'avis ('text') est obligatoire et ne peut pas être vide.")

        # La note doit être un entier entre 1 et 5 inclus
        if not (1 <= self.rating <= 5):
            raise ValueError(
                f"La note ('rating') doit être un entier entre 1 et 5 (reçu : {self.rating})."
            )

        # Le lieu doit être une instance valide de Place
        if not isinstance(self.place, Place):
            raise ValueError(
                "Le champ 'place' doit être une instance valide de la classe Place."
            )

        # L'auteur doit être une instance valide de User
        if not isinstance(self.user, User):
            raise ValueError(
                "Le champ 'user' doit être une instance valide de la classe User."
            )

    # ------------------------------------------------------------------
    # Mise à jour
    # ------------------------------------------------------------------

    def update(self, data: dict):
        """
        Met à jour les attributs modifiables de l'avis.

        Seuls les champs ``text`` et ``rating`` peuvent être modifiés.
        Les références ``place`` et ``user`` sont immuables après création.

        Paramètres
        ----------
        data : dict
            Dictionnaire des champs à modifier.

        Lève
        ----
        ValueError
            Si les nouvelles valeurs ne respectent pas les contraintes.
        """
        # Seuls le texte et la note sont modifiables après création
        # Si le texte est fourni, on le remplace
        if "text" in data:
            self.text = data["text"]
        if "rating" in data:
            # S'assure que la note est bien un entier
            self.rating = int(data["rating"])

        # Revalide après modification
        self._validate()

        # Rafraîchit l'horodatage de dernière modification
        self.save()

    # ------------------------------------------------------------------
    # Sérialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Sérialise l'avis sous forme de dictionnaire JSON-compatible.

        Retourne une représentation **étendue** : les références au lieu et
        à l'utilisateur incluent leurs informations de base (id, titre ou
        prénom/nom) plutôt que de simples UUIDs.

        Retour
        ------
        dict
            Dictionnaire complet de l'avis avec place et user développés.
        """
        # Récupère le dictionnaire de base (id, created_at, updated_at)
        base = super().to_dict()

        # Ajoute les attributs spécifiques à l'avis
        base.update({
            "text":   self.text,
            "rating": self.rating,

            # Sérialisation partielle du lieu (évite la récursion infinie
            # si Place.to_dict() incluait à son tour ses reviews)
            "place": {
                "id":    self.place.id,
                "title": self.place.title,
            },

            # Sérialisation partielle de l'auteur
            "user": {
                "id":         self.user.id,
                "first_name": self.user.first_name,
                "last_name":  self.user.last_name,
            },
        })
        return base
