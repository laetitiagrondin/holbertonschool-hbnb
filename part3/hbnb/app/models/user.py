#!/usr/bin/python3
"""
Module user
===========
Définit l'entité ``User``, qui représente un utilisateur de la plateforme HBnB.

Un utilisateur peut :
    - Posséder plusieurs lieux (relation one-to-many avec ``Place``).
    - Rédiger plusieurs avis (relation one-to-many avec ``Review``).
    - Disposer de droits administrateur (attribut ``is_admin``).

Règles de validation appliquées à la création et à la mise à jour :
    - ``first_name`` et ``last_name`` : requis, longueur maximale de 50 caractères.
    - ``email`` : requis, doit respecter le format standard d'adresse e-mail.
    - L'unicité de l'e-mail est garantie au niveau de la façade, pas ici.

Dépendances :
    - ``re``            : validation du format de l'adresse e-mail.
    - ``base_model``    : classe parente fournissant id, created_at, updated_at.
"""

import re
from app.models.base_model import BaseModel
from app import db, bcrypt


class User(BaseModel):
    """
    Représente un utilisateur enregistré sur la plateforme HBnB.

    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.

    Attributs d'instance
    --------------------
    first_name : str
        Prénom de l'utilisateur.  Requis, 1 à 50 caractères.
    last_name : str
        Nom de famille de l'utilisateur.  Requis, 1 à 50 caractères.
    email : str
        Adresse e-mail unique de l'utilisateur.  Doit respecter le format
        standard (ex. "alice@exemple.fr").
    is_admin : bool
        Indique si l'utilisateur possède les droits d'administration.
        ``False`` par défaut.
    """

    # Expression régulière pour valider le format d'une adresse e-mail.
    # Accepte les caractères alphanumériques, points, tirets et signes +
    # avant le @, puis un domaine avec une extension d'au moins 2 lettres.
    __EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")

    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship("Place", backref="owner", lazy=True)
    reviews = relationship("Review", backref="author", lazy=True)

    def __init__(self, first_name: str,
                 last_name: str, email: str,
                 password: str = None, is_admin: bool = False):
        """
        Initialise un nouvel utilisateur et valide immédiatement ses attributs.

        Paramètres
        ----------
        first_name : str
            Prénom de l'utilisateur (requis, ≤ 50 caractères).
        last_name : str
            Nom de l'utilisateur (requis, ≤ 50 caractères).
        email : str
            Adresse e-mail valide et unique (vérifiée par regex).
        is_admin : bool, optionnel
            Droits administrateur.  ``False`` par défaut.

        Lève
        ----
        ValueError
            Si l'un des attributs ne respecte pas les contraintes définies.
        """
        # Appel du constructeur parent pour initialiser id, created_at, updated_at
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        # bool() garantit que la valeur est bien un booléen même si on passe 1 ou 0
        self.is_admin = bool(is_admin)

        # Validation immédiate : lève ValueError si une règle est violée
    @db.validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Le prénom est obligatoire (max 50 caractères).")
        return value

    @db.validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Le nom est obligatoire (max 50 caractères).")
        return value

    @db.validates('email')
    def email(self, key, value):
        if not value or not self.__EMAIL_RE.match(value):
            raise ValueError(f"L'adresse e-mail '{value}' est invalide.")
        return value

    @db.validates('is_admin')
    def is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Le statut is_admin doit être un booléen.")
        return bool(value)

    def hash_password(self, password):
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    # ------------------------------------------------------------------
    # Mise à jour
    # ------------------------------------------------------------------

    def update(self, data: dict):
        """
        Met à jour les attributs modifiables de l'utilisateur.

        Seuls les champs ``first_name``, ``last_name``, ``email`` et
        ``is_admin`` peuvent être modifiés.  La validation est relancée
        après chaque mise à jour pour garantir la cohérence des données.

        Paramètres
        ----------
        data : dict
            Dictionnaire des champs à modifier et de leurs nouvelles valeurs.
            Les clés inconnues sont silencieusement ignorées.

        Lève
        ----
        ValueError
            Si les nouvelles valeurs ne respectent pas les contraintes.
        """
        # Liste blanche des champs autorisés à être modifiés
        champs_autorises = {"first_name", "last_name", "email", "is_admin"}

        for cle, valeur in data.items():
            if cle in champs_autorises:
                setattr(self, cle, valeur)

        # Met à jour l'horodatage de modification
        self.save()

    # ------------------------------------------------------------------
    # Sérialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Sérialise l'utilisateur sous forme de dictionnaire JSON-compatible.

        Étend le dictionnaire de base (``BaseModel.to_dict()``) avec les
        attributs spécifiques à l'utilisateur.

        Retour
        ------
        dict
            Dictionnaire contenant tous les champs publics de l'utilisateur.
        """
        # Récupère le dictionnaire de base (id, created_at, updated_at)
        base = super().to_dict()

        # Ajoute les attributs propres à l'utilisateur
        base.update({
            "first_name": self.first_name,
            "last_name":  self.last_name,
            "email":      self.email,
            "is_admin":   self.is_admin,
        })
        return base
