# HBnB Project - Part 3 : Authentification, Autorisation & Persistance SQLAlchemy

## 1. Introduction

La Part 3 du projet HBnB étend l'application construite en Part 2 en ajoutant :
- **L'authentification JWT** pour sécuriser les endpoints
- **Le contrôle d'accès par rôle (RBAC)** pour les administrateurs
- **La persistance SQLAlchemy** pour remplacer le stockage en mémoire
- **Un schéma SQL** documentant la structure de la base de données



## 2. Stack Technique

| Outil | Rôle |

| Flask | Framework web |
| Flask-RESTx | API REST + Swagger |
| Flask-JWT-Extended | Authentification JWT |
| Flask-Bcrypt | Hachage des mots de passe |
| Flask-SQLAlchemy | ORM pour la persistance |
| SQLite | Base de données (développement) |



## 3. Architecture
```
hbnb/
├── run.py                          # Point d'entrée
├── config.py                       # Configuration Flask + SQLAlchemy
├── schema.sql                      # Schéma SQL brut
├── initial_data.sql                # Données initiales (admin + amenities)
├── ERD.md                          # Diagramme ER en Mermaid.js
├── requirements.txt
└── app/
    ├── __init__.py                 # Factory create_app + db.create_all
    ├── extensions.py               # bcrypt, jwt, db
    ├── models/
    │   ├── base_model.py           # BaseModel SQLAlchemy (id, timestamps)
    │   ├── user.py                 # User mappé SQLAlchemy
    │   ├── place.py                # Place mappé SQLAlchemy + relations
    │   ├── review.py               # Review mappé SQLAlchemy + relations
    │   └── amenity.py              # Amenity mappé SQLAlchemy
    ├── persistence/
    │   └── repository.py           # InMemoryRepository + SQLAlchemyRepository
    ├── services/
    │   ├── facade.py               # Pattern Facade
    │   └── repositories/
    │       └── user_repository.py  # UserRepository (get_user_by_email)
    └── api/v1/
        ├── auth.py                 # POST /api/v1/auth/login
        ├── users.py                # CRUD users + JWT
        ├── places.py               # CRUD places + JWT
        ├── reviews.py              # CRUD reviews + JWT
        └── amenities.py            # CRUD amenities + JWT admin
```



## 4. Installation
```bash
# Cloner le projet
git clone https://github.com/laetitiagrondin/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/part3/hbnb

# Créer et activer l'environnement virtuel
python3 -m venv env
source env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python3 run.py
```

La base de données est créée automatiquement au démarrage via `db.create_all()`.
L'administrateur par défaut est créé automatiquement :
- **Email** : admin@hbnb.com
- **Password** : admin1234



## 5. Tâches réalisées

### Tâche 0 — Mise en place du projet
Configuration de Flask, Flask-RESTx, structure des dossiers, fichier `run.py` et `config.py`.

### Tâche 1 — Implémentation des modèles
Création des entités `User`, `Place`, `Review`, `Amenity` héritant de `BaseModel` avec validation des attributs.

### Tâche 2 — Pattern Repository
Implémentation de `InMemoryRepository` et de l'interface `Repository` pour abstraire la persistance.

### Tâche 3 — Authentification JWT
- Endpoint `POST /api/v1/auth/login` retournant un token JWT
- Sécurisation des endpoints `POST/PUT places`, `POST/PUT/DELETE reviews`, `PUT users`
- Injection du `user_id` depuis le token JWT

### Tâche 4 — Contrôle d'accès Admin (RBAC)
- Claim `is_admin` dans le token JWT
- Admin peut modifier n'importe quel utilisateur, lieu ou avis
- Seul l'admin peut créer/modifier des amenities
- Création automatique de l'admin au démarrage

### Tâche 5 — SQLAlchemy Repository
- Ajout de `flask-sqlalchemy` dans les dépendances
- Création de `SQLAlchemyRepository` implémentant l'interface `Repository`
- Configuration `SQLALCHEMY_DATABASE_URI` dans `config.py`

### Tâche 6 — Mapping User vers SQLAlchemy
- `BaseModel` hérite de `db.Model` avec `__abstract__ = True`
- `User` mappé avec colonnes SQLAlchemy et validateurs `@db.validates`
- `UserRepository` avec méthode `get_user_by_email`
- Facade utilise `UserRepository`

### Tâche 7 — Mapping Place, Review, Amenity
- `Place`, `Review`, `Amenity` mappés vers SQLAlchemy
- Tables `places`, `reviews`, `amenities` créées automatiquement
- Repositories et Facade mis à jour

### Tâche 8 — Relations SQLAlchemy
Relations implémentées :

| Relation | Type | Description |

| User → Place | One-to-Many | Un user possède plusieurs places (`owner_id` FK) |
| User → Review | One-to-Many | Un user rédige plusieurs reviews (`user_id` FK) |
| Place → Review | One-to-Many | Une place reçoit plusieurs reviews (`place_id` FK) |
| Place ↔ Amenity | Many-to-Many | Via table `place_amenity` |

### Tâche 9 — Scripts SQL
- `schema.sql` : création complète du schéma (5 tables avec contraintes et FK)
- `initial_data.sql` : insertion de l'admin et 3 amenities (WiFi, Piscine, Climatisation)

### Tâche 10 — Diagramme ER
Diagramme Entity-Relationship en Mermaid.js dans `ERD.md` représentant toutes les entités et leurs relations.


## 6. Endpoints API

| Méthode | Endpoint | Auth | Description |

| POST | `/api/v1/auth/login` | Non | Connexion + token JWT |
| GET | `/api/v1/users/` | Non | Liste des utilisateurs |
| POST | `/api/v1/users/` | Non/Admin | Créer un utilisateur |
| GET | `/api/v1/users/<id>` | Non | Détail utilisateur |
| PUT | `/api/v1/users/<id>` | JWT | Modifier son profil |
| GET | `/api/v1/places/` | Non | Liste des lieux |
| POST | `/api/v1/places/` | JWT | Créer un lieu |
| GET | `/api/v1/places/<id>` | Non | Détail lieu |
| PUT | `/api/v1/places/<id>` | JWT | Modifier un lieu |
| GET | `/api/v1/reviews/` | Non | Liste des avis |
| POST | `/api/v1/reviews/` | JWT | Créer un avis |
| GET | `/api/v1/reviews/<id>` | Non | Détail avis |
| PUT | `/api/v1/reviews/<id>` | JWT | Modifier un avis |
| DELETE | `/api/v1/reviews/<id>` | JWT | Supprimer un avis |
| GET | `/api/v1/amenities/` | Non | Liste des équipements |
| POST | `/api/v1/amenities/` | Admin | Créer un équipement |
| PUT | `/api/v1/amenities/<id>` | Admin | Modifier un équipement |

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



## 8. Base de données

La base SQLite est créée automatiquement dans `instance/development.db`.

Pour initialiser avec les scripts SQL bruts :
```bash
sqlite3 test.db < schema.sql
sqlite3 test.db < initial_data.sql
```

