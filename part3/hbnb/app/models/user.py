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
from app import bcrypt


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

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_admin: bool = False,
    ):
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
    @property
    def first_name(self):
        """ Getter pour le prénom. """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """ Setter pour le prénom (max 50 caractères). """
        if not value or len(value) > 50:
            raise ValueError(
                "Le prénom est obligatoire (max 50 caractères)."
            )
        self.__first_name = value

    @property
    def last_name(self):
        """ Getter pour le nom. """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """ Setter pour le nom (max 50 caractères). """
        if not value or len(value) > 50:
            raise ValueError(
                "Le nom est obligatoire (max 50 caractères)."
            )
        self.__last_name = value

    @property
    def email(self):
        """ Getter pour l'e-mail. """
        return self.__email

    @email.setter
    def email(self, value):
        """ Setter pour l'e-mail avec validation Regex. """
        if not value or not self.__EMAIL_RE.match(value):
            raise ValueError(
                f"L'adresse e-mail '{value}' est invalide."
            )
        self.__email = value

    @property
    def is_admin(self):
        """ Getter pour le statut administrateur. """
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """ Setter pour le statut administrateur. """
        if not isinstance(value, bool):
            raise ValueError("Le statut is_admin doit être un booléen.")
        self.__is_admin = value

    def hash_password(self, password):
        """Hashes the password before storing it."""
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
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
