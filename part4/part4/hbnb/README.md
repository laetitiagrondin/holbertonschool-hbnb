---

## 🏗️ Architecture et Design Patterns

### Le Pattern Facade
Pour respecter les consignes du projet, une **Facade** a été implémentée dans `app/services/facade.py`. Elle sert de point d'entrée unique pour la logique métier, permettant :
* De découpler les contrôleurs API (Flask-RESTX) des modèles de données (SQLAlchemy).
* De centraliser la gestion des erreurs et la validation des données.
* De faciliter la maintenance et l'évolution du code.

### Modèle de Données (ERD)
L'application repose sur quatre entités principales liées entre elles :
* **User** : Gère les comptes et l'authentification (Bcrypt pour le hachage).
* **Place** : Représente les hébergements avec leurs coordonnées (latitude/longitude).
* **Amenity** : Liste les équipements disponibles (WiFi, Piscine, etc.).
* **Review** : Fait le lien entre un utilisateur et un lieu pour les évaluations.

## 🔒 Sécurité et Validation

### Gestion des Identités (JWT)
L'authentification est gérée par des jetons **JWT**. Contrairement à une session classique, le JWT est sans état (stateless), ce qui rend l'API plus performante. 
* Le jeton contient des informations sur l'utilisateur (ID, rôle admin).
* Il est vérifié à chaque requête sensible (`POST`, `PUT`, `DELETE`).

### Protection contre les attaques communes
* **SQL Injection** : Prévenue par l'utilisation de l'ORM SQLAlchemy qui paramètre automatiquement les requêtes.
* **XSS (Cross-Site Scripting)** : Prévenue côté Frontend par l'échappement systématique des données dynamiques.
* **CORS (Cross-Origin Resource Sharing)** : Configuré pour n'autoriser que les origines de confiance (localhost), empêchant les sites tiers de faire des requêtes malveillantes.

## 🛠️ Développement et Tests

### Seeding de la Base de Données
Le projet inclut un script de **seeding** automatique au démarrage de l'application (dans `app/__init__.py`). Cela permet d'avoir un environnement de test prêt à l'emploi avec :
* Un utilisateur administrateur (`admin@hbnb.com`).
* Un utilisateur de test (`test@hbnb.com`).
* Des équipements et des lieux pré-remplis.

### Endpoints Principaux
| Méthode | Endpoint | Description | Auth Requise |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | Connexion et récupération du JWT | Non |
| `GET` | `/api/v1/places/` | Liste tous les lieux | Non |
| `POST` | `/api/v1/reviews/` | Ajouter un avis sur un lieu | Oui (JWT) |
| `PUT` | `/api/v1/users/me` | Modifier son profil | Oui (JWT) |

## 👥 Auteur
* **Luidgi** - *Développement Backend & Intégration Frontend* -

---
*Projet réalisé dans le cadre du cursus Holberton School.*
