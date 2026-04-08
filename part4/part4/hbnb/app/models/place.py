#!/usr/bin/python3
"""
Module place
Définit l'entité Place, qui représente une annonce de location sur
la plateforme HBnB.

Un lieu :
    - Appartient à exactement un User (propriétaire).
    - Peut recevoir plusieurs Review (avis, relation one-to-many).
    - Peut proposer plusieurs Amenity (équipements, relation many-to-many).
Dépendances :
    - base_model : classe parente fournissant id, created_at, updated_at.
    - user       : référence au propriétaire du lieu.
"""

from app.extensions import db
from app.models.base_model import BaseModel
from app.models.user import User


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    """
    Représente une annonce de location sur la plateforme HBnB.
    Hérite de ``BaseModel`` pour l'identifiant UUID et les horodatages.
    """

    __tablename__ = 'places'
    
    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True, default="")
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # Relation one-to-many : User -> Places
    owner = db.relationship('User', backref=db.backref('places', lazy=True))
    # Relation one-to-many : Place -> Reviews
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    # Relation many-to-many : Place <-> Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))
    
    def __init__(self, title, price, latitude, longitude,
                 owner=None, owner_id=None, description="", **kwargs):
        """
        Initialise un nouveau lieu et valide immédiatement ses attributs.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__(**kwargs)
        self.title       = title
        self.description = description
        # Conversion explicite en float pour accepter les entiers passés en paramètre
        self.price     = float(price)
        self.latitude  = float(latitude)
        self.longitude = float(longitude)
        # Référence vers l'instance User propriétaire du lieu
        if owner:
            self.owner    = owner
        elif owner_id:
            self.owner_id = owner_id
        # Liste des avis (Review) associés à ce lieu — initialement vide

    @db.validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Le titre est obligatoire (max 100 caractères).")
        return value

    @db.validates('price')
    def validate_price(self, key, value):
        if value is None or float(value) <= 0:
            raise ValueError("Le prix doit être positif.")
        return float(value)

    @db.validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90.0 <= float(value) <= 90.0):
            raise ValueError("La latitude doit être entre -90.0 et 90.0.")
        return float(value)


    @db.validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180.0 <= float(value) <= 180.0):
            raise ValueError("La longitude doit être entre -180.0 et 180.0.")
        return float(value)  

    # Gestion des relations
    
    def add_review(self, review) -> None:
        """
        Rattache un avis à ce lieu.

        L'avis est ajouté à la liste ``self.reviews``.  La méthode vérifie
        que l'argument passé est bien une instance de ``Review`` avant de
        l'ajouter, afin de maintenir l'intégrité des données.

        Paramètres
        
        review : Review
            Instance de ``Review`` à rattacher au lieu.

        Lève
        
        TypeError
            Si l'argument n'est pas une instance de ``Review``.

        Note
        
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
        
        amenity : Amenity
            Instance de ``Amenity`` à associer au lieu.

        Lève
        
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

    
    # Mise à jour
    

    def update(self, data: dict):
        """
        Met à jour les attributs modifiables du lieu.
        Seuls les champs title, description, price, latitude
        et longitude peuvent être modifiés.  Le propriétaire (owner)
        ne peut pas être changé via cette méthode.
        La validation est relancée après chaque mise à jour.
        Paramètres
        data : dict
            Dictionnaire des champs à modifier et de leurs nouvelles valeurs.
        Lève
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

    
    # Sérialisation
    

    def to_dict(self) -> dict:
        """
        Sérialise le lieu sous forme de dictionnaire JSON-compatible.
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

            # Sérialisation étendue du propriétaire
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

            "reviews": [
                {
                    "id": r.id,
                    "text": r.text,
                    "rating": r.rating,
                    "user_name": f"{r.user.first_name} {r.user.last_name}" if r.user else "Anonymous"
                } for r in self.reviews
            ]
        })
        return base

    def to_summary_dict(self) -> dict:
        """
        Retourne une représentation allégée du lieu pour les listes.

        Utilisé par l'endpoint ``GET /api/v1/places/`` pour retourner
        une liste compacte sans surcharger la réponse avec tous les détails.

        Retour
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
