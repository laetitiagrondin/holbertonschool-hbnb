#!/usr/bin/python3
"""
Module place
============
Définit l'entité ``Place``, qui représente une annonce de location sur
la plateforme HBnB.

Un lieu :
    - Appartient à exactement un ``User`` (propriétaire).
    - Peut recevoir plusieurs ``Review`` (avis, relation one-to-many).
    - Peut proposer plusieurs ``Amenity`` (équipements, relation many-to-many).

Règles de validation :
    - ``title``     : requis, longueur maximale de 100 caractères.
    - ``price``     : doit être un nombre strictement positif.
    - ``latitude``  : doit être compris entre -90.0 et 90.0 inclus.
    - ``longitude`` : doit être compris entre -180.0 et 180.0 inclus.
    - ``owner``     : doit être une instance valide de ``User``.

Dépendances :
    - ``base_model`` : classe parente fournissant id, created_at, updated_at.
    - ``user``       : référence au propriétaire du lieu.
"""

from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """
    Représente une annonce de location sur la plateforme HBnB.

    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.

    Attributs d'instance
    --------------------
    title : str
        Titre de l'annonce.  Requis, 1 à 100 caractères.
    description : str
        Description détaillée du lieu.  Optionnelle, peut être vide.
    price : float
        Prix par nuit en euros.  Doit être strictement positif (> 0).
    latitude : float
        Coordonnée géographique de latitude.  Plage : [-90.0, 90.0].
    longitude : float
        Coordonnée géographique de longitude.  Plage : [-180.0, 180.0].
    owner : User
        Instance ``User`` représentant le propriétaire du lieu.
    reviews : list[Review]
        Liste des avis associés à ce lieu.  Gérée via ``add_review()``.
    amenities : list[Amenity]
        Liste des équipements disponibles.  Gérée via ``add_amenity()``
        (sans doublons).
    """

    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
    ):
        """
        Initialise un nouveau lieu et valide immédiatement ses attributs.

        Paramètres
        ----------
        title : str
            Titre de l'annonce (requis, ≤ 100 caractères).
        description : str
            Description du lieu (peut être une chaîne vide).
        price : float
            Prix par nuit, doit être > 0.
        latitude : float
            Latitude en degrés décimaux, plage [-90.0, 90.0].
        longitude : float
            Longitude en degrés décimaux, plage [-180.0, 180.0].
        owner : User
            Instance ``User`` valide représentant le propriétaire.

        Lève
        ----
        ValueError
            Si l'un des attributs ne respecte pas les contraintes définies.
        TypeError
            Si ``owner`` n'est pas une instance de ``User``.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__()

        self.title       = title
        self.description = description

        # Conversion explicite en float pour accepter les entiers passés en paramètre
        self.price     = float(price)
        self.latitude  = float(latitude)
        self.longitude = float(longitude)

        # Référence vers l'instance User propriétaire du lieu
        self.owner = owner

        # Liste des avis (Review) associés à ce lieu — initialement vide
        self.reviews: list = []

        # Liste des équipements (Amenity) disponibles — initialement vide
        self.amenities: list = []

    @property
    def title(self):
        """ Getter pour le titre. """
        return self.__title

    @title.setter
    def title(self, value):
        """ Setter pour le titre (max 100 caractères). """
        if not value or len(value) > 100:
            raise ValueError(
                "Le titre est obligatoire et doit faire maximum 100 caractères."
            )
        self.__title = value

    @property
    def price(self):
        """ Getter pour le prix. """
        return self.__price

    @price.setter
    def price(self, value):
        """ Setter pour le prix (doit être positif). """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f"Le prix doit être une valeur positive (reçu : {value})."
            )
        self.__price = float(value)

    @property
    def latitude(self):
        """ Getter pour la latitude. """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """ Setter pour la latitude (-90.0 à 90.0). """
        if not (-90.0 <= value <= 90.0):
            raise ValueError(
                f"La latitude doit être entre -90.0 et 90.0 (reçu : {value})."
            )
        self.__latitude = float(value)

    @property
    def longitude(self):
        """ Getter pour la longitude. """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """ Setter pour la longitude (-180.0 à 180.0). """
        if not (-180.0 <= value <= 180.0):
            raise ValueError(
                f"La longitude doit être entre -180.0 et 180.0 (reçu : {value})."
            )
        self.__longitude = float(value)

    @property
    def owner(self):
        """ Getter pour le propriétaire. """
        return self.__owner

    @owner.setter
    def owner(self, value):
        """ Setter pour le propriétaire (doit être une instance de User). """
        if not isinstance(value, User):
            raise ValueError(
                "Le champ 'owner' doit être une instance valide de User."
            )
        self.__owner = value

    def add_review(self, review):
        """ Ajoute une critique à la liste. """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """ Ajoute un équipement à la liste. """
        self.amenities.append(amenity)  

    # ------------------------------------------------------------------
    # Gestion des relations
    # ------------------------------------------------------------------

    def add_review(self, review) -> None:
        """
        Rattache un avis à ce lieu.

        L'avis est ajouté à la liste ``self.reviews``.  La méthode vérifie
        que l'argument passé est bien une instance de ``Review`` avant de
        l'ajouter, afin de maintenir l'intégrité des données.

        Paramètres
        ----------
        review : Review
            Instance de ``Review`` à rattacher au lieu.

        Lève
        ----
        TypeError
            Si l'argument n'est pas une instance de ``Review``.

        Note
        ----
        L'import de ``Review`` est effectué en fin de fonction (import tardif)
        pour éviter les imports circulaires entre ``place.py`` et ``review.py``.
        """
        # Import tardif pour éviter la dépendance circulaire Place ↔ Review
        from app.models.review import Review

        # Vérifie que l'argument est bien un avis
        if not isinstance(review, Review):
            raise TypeError("L'argument doit être une instance de la classe Review.")

        # Ajoute l'avis à la liste des avis du lieu
        self.reviews.append(review)

    def add_amenity(self, amenity) -> None:
        """
        Associe un équipement à ce lieu (sans créer de doublon).

        L'équipement est ajouté à la liste ``self.amenities`` uniquement s'il
        n'y figure pas déjà.  La vérification d'identité repose sur la
        comparaison des objets Python (même référence).

        Paramètres
        ----------
        amenity : Amenity
            Instance de ``Amenity`` à associer au lieu.

        Lève
        ----
        TypeError
            Si l'argument n'est pas une instance de ``Amenity``.

        Note
        ----
        Import tardif pour éviter les imports circulaires.
        """
        # Import tardif pour éviter la dépendance circulaire Place ↔ Amenity
        from app.models.amenity import Amenity

        # Vérifie que l'argument est bien un équipement
        if not isinstance(amenity, Amenity):
            raise TypeError("L'argument doit être une instance de la classe Amenity.")

        # N'ajoute l'équipement que s'il n'est pas déjà présent (évite les doublons)
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # ------------------------------------------------------------------
    # Mise à jour
    # ------------------------------------------------------------------

    def update(self, data: dict):
        """
        Met à jour les attributs modifiables du lieu.

        Seuls les champs ``title``, ``description``, ``price``, ``latitude``
        et ``longitude`` peuvent être modifiés.  Le propriétaire (``owner``)
        ne peut pas être changé via cette méthode.

        La validation est relancée après chaque mise à jour.

        Paramètres
        ----------
        data : dict
            Dictionnaire des champs à modifier et de leurs nouvelles valeurs.

        Lève
        ----
        ValueError
            Si les nouvelles valeurs ne respectent pas les contraintes.
        """
        # Liste blanche des champs autorisés à être modifiés
        champs_autorises = {"title", "description", "price", "latitude", "longitude"}

        for cle, valeur in data.items():
            if cle in champs_autorises:
                setattr(self, cle, valeur)

        # Conversion en float pour garantir le bon type après mise à jour
        self.price     = float(self.price)
        self.latitude  = float(self.latitude)
        self.longitude = float(self.longitude)

        # Rafraîchit l'horodatage de dernière modification
        self.save()

    # ------------------------------------------------------------------
    # Sérialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """
        Sérialise le lieu sous forme de dictionnaire JSON-compatible.

        Retourne une représentation **étendue** : au lieu d'un simple UUID
        pour le propriétaire et les équipements, le dictionnaire inclut
        les informations détaillées de chaque entité liée (first_name,
        last_name, email pour l'owner ; id et name pour chaque amenity).

        Retour
        ------
        dict
            Dictionnaire complet du lieu avec owner et amenities développés.
        """
        # Récupère le dictionnaire de base (id, created_at, updated_at)
        base = super().to_dict()

        # Ajoute les attributs spécifiques au lieu
        base.update({
            "title":       self.title,
            "description": self.description,
            "price":       self.price,
            "latitude":    self.latitude,
            "longitude":   self.longitude,

            # Sérialisation étendue du propriétaire :
            # inclut les informations de contact plutôt que le simple UUID
            "owner": {
                "id":         self.owner.id,
                "first_name": self.owner.first_name,
                "last_name":  self.owner.last_name,
                "email":      self.owner.email,
            },

            # Sérialisation étendue de chaque équipement associé
            "amenities": [
                {"id": a.id, "name": a.name} for a in self.amenities
            ],
        })
        return base

    def to_summary_dict(self) -> dict:
        """
        Retourne une représentation allégée du lieu pour les listes.

        Utilisé par l'endpoint ``GET /api/v1/places/`` pour retourner
        une liste compacte sans surcharger la réponse avec tous les détails.

        Retour
        ------
        dict
            Dictionnaire contenant uniquement id, title, price, latitude
            et longitude.
        """
        return {
            "id":        self.id,
            "title":     self.title,
            "price":     self.price,
            "latitude":  self.latitude,
            "longitude": self.longitude,
        }
