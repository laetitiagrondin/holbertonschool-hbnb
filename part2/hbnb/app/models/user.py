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
    _EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
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
        self.last_name  = last_name
        self.email      = email
        # bool() garantit que la valeur est bien un booléen même si on passe 1 ou 0
        self.is_admin   = bool(is_admin)

        # Validation immédiate : lève ValueError si une règle est violée
        self._validate()

    # ------------------------------------------------------------------
    # Validation interne
    # ------------------------------------------------------------------

    def _validate(self):
        """
        Vérifie que les attributs de l'utilisateur respectent les contraintes métier.

        Contrôles effectués :
            - ``first_name`` : non vide et longueur ≤ 50 caractères.
            - ``last_name``  : non vide et longueur ≤ 50 caractères.
            - ``email``      : correspond à l'expression régulière ``_EMAIL_RE``.

        Lève
        ----
        ValueError
            Message explicite indiquant quel champ est invalide et pourquoi.
        """
        # Vérification du prénom : doit être présent et ne pas dépasser 50 caractères
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError(
                "Le champ 'first_name' est obligatoire et doit contenir au maximum 50 caractères."
            )

        # Vérification du nom de famille : même règle que le prénom
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError(
                "Le champ 'last_name' est obligatoire et doit contenir au maximum 50 caractères."
            )

        # Vérification du format de l'e-mail via l'expression régulière
        if not self._EMAIL_RE.match(self.email):
            raise ValueError(
                f"L'adresse e-mail '{self.email}' est invalide. "
                "Format attendu : utilisateur@domaine.ext"
            )

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

        # Revalide l'objet après modification pour détecter toute incohérence
        self._validate()

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
