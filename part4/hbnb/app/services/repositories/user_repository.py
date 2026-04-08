"""
Module user_repository
Dépôt spécifique à l'entité User.
Étend SQLAlchemyRepository avec des méthodes propres aux utilisateurs.
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Dépôt dédié aux opérations sur les utilisateurs.
    Hérite des opérations CRUD génériques de SQLAlchemyRepository
    et ajoute des requêtes spécifiques à l'entité User.
    """

    def __init__(self):
        # Initialise le dépôt générique avec le modèle User
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Recherche un utilisateur par son adresse e-mail.
        """
        return self.model.query.filter_by(email=email).first()
