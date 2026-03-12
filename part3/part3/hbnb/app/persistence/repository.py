"""
Module définissant l'interface du dépôt et son implémentation en mémoire.
"""


from abc import ABC, abstractmethod
from app.extensions import db

class Repository(ABC):
    """ Interface abstraite pour les dépôts de données. """
    
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """ Implémentation en mémoire de l'interface Repository. """
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
    


class SQLAlchemyRepository(Repository):
    """Implémentation SQLAlchemy de l'interface Repository."""

    def __init__(self, model):
        # Le modèle SQLAlchemy géré par ce dépôt (User, Place, etc.)
        self.model = model

    def add(self, obj):
        """Ajoute un objet en base et valide la transaction."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Récupère un objet par son identifiant UUID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retourne tous les objets du modèle."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Met à jour les attributs d'un objet et valide la transaction."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Supprime un objet de la base et valide la transaction."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Filtre les objets par un attribut donné."""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()
