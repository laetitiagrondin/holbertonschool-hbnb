#!/usr/bin/python3
"""
Module review

Définit l'entité ``Review``, qui représente un avis laissé par un utilisateur
sur un lieu de la plateforme HBnB.

Dépendances :
    - ``base_model`` : classe parente fournissant id, created_at, updated_at.
    - ``user``       : référence à l'auteur de l'avis.
    - ``place``      : référence au lieu évalué.
"""

from app.extensions import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """
    Représente un avis rédigé par un utilisateur à propos d'un lieu.

    Relations
    
    - Un avis est rattaché à **un seul lieu** (place).
    - Un avis est rédigé par **un seul utilisateur** (user).
    - Le lieu maintient une liste de ses avis (Place.reviews).
    """

    __tablename__ = 'reviews'
    text   = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Clés étrangères
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relation one-to-many : User -> Reviews
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    
    def __init__(self, text, rating, place=None, user=None, place_id=None, user_id=None, **kwargs):
        """
        Initialise un nouvel avis et valide immédiatement ses attributs.
        Lève
        
        ValueError
            Si le texte est vide, la note hors plage, ou les références invalides.
        """
        # Initialise id, created_at et updated_at via le constructeur parent
        super().__init__(**kwargs)
        self.text = text
        # Conversion en int pour accepter les chaînes numériques éventuelles
        self.rating = int(rating)
        if place: 
            self.place = place
        elif place_id: 
            self.place_id = place_id
            
        if user: 
            self.user = user
        elif user_id: 
            self.user_id = user_id

    @db.validates('text')
    def validate_text(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Le contenu de l'avis est obligatoire.")
        return value

    @db.validates('rating')
    def validate_rating(self, key, value):
        val = int(value)
        if not (1 <= val <= 5):
            raise ValueError("La note doit être entre 1 et 5.")
        return val

    
    # Mise à jour
    

    def update(self, data: dict):
        """
        Met à jour les attributs modifiables de l'avis.

        Seuls les champs text et rating peuvent être modifiés.
        Les références place et user` sont immuables après création.

        Paramètres
        
        data : dict
            Dictionnaire des champs à modifier.

        Lève
        
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
        # Rafraîchit l'horodatage de dernière modification
        self.save()

    
    # Sérialisation
    

    def to_dict(self) -> dict:
        """
        Sérialise l'avis sous forme de dictionnaire JSON-compatible.
        Retourne une représentation **étendue** : les références au lieu et
        à l'utilisateur incluent leurs informations de base (id, titre ou
        prénom/nom) plutôt que de simples UUIDs.
        Retour
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
