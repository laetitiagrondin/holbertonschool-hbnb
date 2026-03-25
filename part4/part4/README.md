# HBnB Project - Part 3 : Authentification, Autorisation & Persistance SQLAlchemy

## 1. Introduction

La Part 3 du projet HBnB étend l'application construite en Part 2 en ajoutant :
- **L'authentification JWT** pour sécuriser les endpoints
- **Le contrôle d'accès par rôle (RBAC)** pour les administrateurs
- **La persistance SQLAlchemy** pour remplacer le stockage en mémoire
- **Un schéma SQL** documentant la structure de la base de données

---

## 2. Stack Technique

| Outil | Rôle |
|---|---|
| Flask | Framework web |
| Flask-RESTx | API REST + Swagger |
| Flask-JWT-Extended | Authentification JWT |
| Flask-Bcrypt | Hachage des mots de passe |
| Flask-SQLAlchemy | ORM pour la persistance |
| SQLite | Base de données (développement) |

---

## 3. Architecture
```
hbnb/
├── run.py
├── config.py
├── schema.sql
├── initial_data.sql
├── ERD.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── extensions.py
    ├── models/
    │   ├── base_model.py
    │   ├── user.py
    │   ├── place.py
    │   ├── review.py
    │   └── amenity.py
    ├── persistence/
    │   └── repository.py
    ├── services/
    │   ├── facade.py
    │   └── repositories/
    │       └── user_repository.py
    └── api/v1/
        ├── auth.py
        ├── users.py
        ├── places.py
        ├── reviews.py
        └── amenities.py
```

---

## 4. Installation
```bash
git clone https://github.com/laetitiagrondin/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/part3/hbnb
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 run.py
```

La base de données est créée automatiquement au démarrage.
Administrateur par défaut :
- **Email** : admin@hbnb.com
- **Password** : admin1234

---

## 5. Tâches réalisées

### Tâche 0 — Mise en place du projet
Configuration de Flask, Flask-RESTx, structure des dossiers.

### Tâche 1 — Implémentation des modèles
Création des entités User, Place, Review, Amenity héritant de BaseModel avec validation.

### Tâche 2 — Pattern Repository
Implémentation de InMemoryRepository et de l'interface Repository.

### Tâche 3 — Authentification JWT
- Endpoint POST /api/v1/auth/login retournant un token JWT
- Sécurisation des endpoints places, reviews, users
- Injection du user_id depuis le token JWT

### Tâche 4 — Contrôle d'accès Admin (RBAC)
- Claim is_admin dans le token JWT
- Admin peut modifier n'importe quel utilisateur, lieu ou avis
- Seul l'admin peut créer/modifier des amenities

### Tâche 5 — SQLAlchemy Repository
- Ajout de flask-sqlalchemy
- Création de SQLAlchemyRepository
- Configuration SQLALCHEMY_DATABASE_URI

### Tâche 6 — Mapping User vers SQLAlchemy
- BaseModel hérite de db.Model
- User mappé avec colonnes et validateurs
- UserRepository avec get_user_by_email

### Tâche 7 — Mapping Place, Review, Amenity
- Place, Review, Amenity mappés vers SQLAlchemy
- Tables créées automatiquement

### Tâche 8 — Relations SQLAlchemy

| Relation | Type |
|---|---|
| User -> Place | One-to-Many |
| User -> Review | One-to-Many |
| Place -> Review | One-to-Many |
| Place <-> Amenity | Many-to-Many |

### Tâche 9 — Scripts SQL
- schema.sql : création du schéma complet
- initial_data.sql : admin + 3 amenities (WiFi, Piscine, Climatisation)

### Tâche 10 — Diagramme ER
Diagramme Mermaid.js dans ERD.md représentant toutes les entités et relations.

---

## 6. Endpoints API

| Méthode | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /api/v1/auth/login | Non | Connexion + token JWT |
| GET | /api/v1/users/ | Non | Liste des utilisateurs |
| POST | /api/v1/users/ | Non/Admin | Créer un utilisateur |
| GET | /api/v1/users/<id> | Non | Détail utilisateur |
| PUT | /api/v1/users/<id> | JWT | Modifier son profil |
| GET | /api/v1/places/ | Non | Liste des lieux |
| POST | /api/v1/places/ | JWT | Créer un lieu |
| GET | /api/v1/places/<id> | Non | Détail lieu |
| PUT | /api/v1/places/<id> | JWT | Modifier un lieu |
| GET | /api/v1/reviews/ | Non | Liste des avis |
| POST | /api/v1/reviews/ | JWT | Créer un avis |
| GET | /api/v1/reviews/<id> | Non | Détail avis |
| PUT | /api/v1/reviews/<id> | JWT | Modifier un avis |
| DELETE | /api/v1/reviews/<id> | JWT | Supprimer un avis |
| GET | /api/v1/amenities/ | Non | Liste des équipements |
| POST | /api/v1/amenities/ | Admin | Créer un équipement |
| PUT | /api/v1/amenities/<id> | Admin | Modifier un équipement |

---

## 7. Tests rapides
```bash
# Login admin
curl -s -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.com", "password": "admin1234"}'

# Créer un utilisateur
curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@test.com", "password": "pass1234"}'

# Lister les lieux
curl -s "http://127.0.0.1:5000/api/v1/places/"
```

---

## 8. Base de données

La base SQLite est créée automatiquement dans instance/development.db.

Pour initialiser avec les scripts SQL bruts :
```bash
sqlite3 test.db < schema.sql
sqlite3 test.db < initial_data.sql
```

---

## 9. Auteurs

Projet réalisé dans le cadre du cursus Holberton School.
