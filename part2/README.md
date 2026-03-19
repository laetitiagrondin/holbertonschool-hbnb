#  HBnB Project - Phase 2 : Logique Métier & API REST

##  1. Introduction
Bienvenue dans la Phase 2 du projet HBnB. Cette étape consiste à transformer notre conception architecturale en une application fonctionnelle en utilisant **Python** et **Flask**. L'objectif est de construire les couches de présentation et de logique d'entreprise, tout en définissant les points de terminaison API essentiels.

##  2. Architecture et Vision
Le projet repose sur une architecture modulaire garantissant une séparation claire des responsabilités :

* **Couche Logique Métier (Business Logic) :** Définit les entités (`User`, `Place`, `Review`, `Amenity`), gère les relations et applique les règles de validation.
* **Couche de Présentation :** Expose les services via une API RESTful utilisant `Flask-RESTx`.
* **Pattern Façade :** Centralise la communication entre l'API et la logique métier pour un code plus propre et maintenable.



---

##  3. Règles de Validation (Business Rules)
Chaque modèle d'entité intègre une logique de validation rigoureuse avant tout stockage :

| Entité | Attribut | Règle de Validation |
| :--- | :--- | :--- |
| **User** | `first_name`, `last_name`, `email` | Ne doivent pas être vides. |
| **User** | `email` | Doit respecter un format d'e-mail valide (Regex). |
| **Place** | `title` | Ne doit pas être vide. |
| **Place** | `price` | Doit être un nombre strictement positif (> 0). |
| **Place** | `latitude` | Doit être comprise entre **-90.0** et **90.0**. |
| **Place** | `longitude` | Doit être comprise entre **-180.0** et **180.0**. |
| **Review** | `text` | Ne doit pas être vide. |
| **Review** | `rating` | Doit être un entier compris entre **1** et **5**. |

---

##  4. Registre des Tests API (Endpoints & cURL)

Ce tableau documente le succès des tests de boîte noire effectués. 
*Note : Les UUID utilisés sont des exemples basés sur un flux réel.*

| Ordre | Module | Objectif | Commande cURL | Réponse Attendue (HTTP & JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **User** | **Création (Succès)** | `curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'` | **201 Created** <br> `{"id": "550e8400...", "email": "john.doe@example.com"}` |
| **2** | **User** | **Données Invalides** | `curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "", "email": "invalid-email"}'` | **400 Bad Request** <br> `{"error": "Invalid input data"}` |
| **3** | **Place** | **Latitude hors portée**| `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Villa", "latitude": 150.0}'` | **400 Bad Request** <br> `{"error": "Latitude must be between -90 and 90"}` |
| **4** | **Place** | **Liaison Amenity** | `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/PLACE_UUID/amenities" -H "Content-Type: application/json" -d '{"amenity_id": "AMENITY_UUID"}'` | **200 OK** <br> `{"message": "Amenity added successfully"}` |
| **5** | **Review**| **Note > 5** | `curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"rating": 6}'` | **400 Bad Request** <br> `{"error": "Rating must be between 1 and 5"}` |
| **6** | **Global**| **ID inexistant** | `curl -i -X GET "http://127.0.0.1:5000/api/v1/users/non-existant-id"` | **404 Not Found** <br> `{"message": "User not found"}` |

# Tests API (Endpoints, Inputs & Outputs)

| Ordre | Module | Action / Objectif | Commande cURL | Réponse Attendue |
|------|------|------|------|------|
| 1 | User | Création (Succès) | `curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name":"Luidgi","last_name":"Wtsn","email":"owner@hbnb.com"}'` | **201 Created**<br>`{"id":"1e8d5f30-6b2c-4e8a-9f1a-3d5b7c8e9f0a","email":"owner@hbnb.com"}` |
| 2 | User | Erreur : Email en doublon | `curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"email":"owner@hbnb.com"}'` | **400 Bad Request**<br>`{"error":"Email already registered"}` |
| 3 | User | Erreur : Format Email | `curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"email":"invalid-format"}'` | **400 Bad Request**<br>`{"error":"L'adresse e-mail est invalide."}` |
| 4 | User | Récupération utilisateur inexistant | `curl -i -X GET "http://127.0.0.1:5000/api/v1/users/ffffffff-ffff-ffff-ffff-ffffffffffff"` | **404 Not Found**<br>`{"message":"User not found"}` |
| 5 | Amenity | Création (Succès) | `curl -i -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name":"WiFi"}'` | **201 Created**<br>`{"id":"7f2a1b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c","name":"WiFi"}` |
| 6 | Amenity | Erreur : Nom vide | `curl -i -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name":""}'` | **400 Bad Request**<br>`{"error":"Le nom est obligatoire."}` |
| 7 | Amenity | Mise à jour (Succès) | `curl -i -X PUT "http://127.0.0.1:5000/api/v1/amenities/7f2a1b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c" -H "Content-Type: application/json" -d '{"name":"Piscine"}'` | **200 OK**<br>`{"id":"7f2a1b3c...","name":"Piscine"}` |
| 8 | Place | Création (Succès) | `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title":"Villa","price":100.0,"owner_id":"1e8d5f30-6b2c-4e8a-9f1a-3d5b7c8e9f0a"}'` | **201 Created**<br>`{"id":"9a8b7c6d-5e4f-3a2b-1c0d-e9f8a7b6c5d4","title":"Villa"}` |
| 9 | Place | Erreur : Prix négatif | `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"price":-10.0,"owner_id":"1e8d5f30"}'` | **400 Bad Request**<br>`{"error":"Price must be positive"}` |
| 10 | Place | Erreur : Latitude hors limites | `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"latitude":120.0}'` | **400 Bad Request**<br>`{"error":"Latitude must be between -90 and 90"}` |
| 11 | Place | Ajouter une Amenity à une Place | `curl -i -X POST "http://127.0.0.1:5000/api/v1/places/9a8b7c6d-5e4f-3a2b-1c0d-e9f8a7b6c5d4/amenities" -H "Content-Type: application/json" -d '{"amenity_id":"7f2a1b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c"}'` | **200 OK**<br>`{"message":"Amenity added to place"}` |
| 12 | Review | Création (Succès) | `curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"text":"Top","rating":5,"user_id":"1e8d5f30","place_id":"9a8b7c6d"}'` | **201 Created**<br>`{"id":"3c2b1a0d-e9f8-a7b6-c5d4-3210fedcba98","text":"Top"}` |
| 13 | Review | Erreur : Note > 5 | `curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"rating":6}'` | **400 Bad Request**<br>`{"error":"Rating must be between 1 and 5"}` |
| 14 | Review | Mise à jour (Succès) | `curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/3c2b1a0d-e9f8-a7b6-c5d4-3210fedcba98" -H "Content-Type: application/json" -d '{"text":"Excellent"}'` | **200 OK**<br>`{"id":"3c2b1a0d...","text":"Excellent","rating":5}` |
| 15 | Review | Suppression (Succès) | `curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/3c2b1a0d-e9f8-a7b6-c5d4-3210fedcba98"` | **200 OK**<br>`{"message":"Review deleted successfully"}` |

---

# Logique des Codes de Réponse HTTP

| Code HTTP | Statut | Utilisation |
|-----------|--------|-------------|
| **200 OK** | Succès | Retour d'une requête GET, PUT ou DELETE réussie |
| **201 Created** | Création | Nouvelle ressource créée (User, Place, Amenity, Review) |
| **400 Bad Request** | Erreur client | Données invalides : email incorrect, prix négatif, note invalide |
| **404 Not Found** | Ressource introuvable | UUID inexistant ou ressource supprimée |

---

# Flux de Validation des Données

Lorsqu'une requête `POST` ou `PUT` est reçue, l'API suit les étapes suivantes :

1. Vérification du **format JSON** de la requête.
2. Validation des **champs obligatoires**.
3. Vérification des **contraintes métier** :
   - email valide et unique
   - prix positif
   - rating entre 1 et 5
   - latitude entre -90 et 90
4. Vérification de l'existence des **relations (User, Place, Amenity)**.
5. Si toutes les validations passent → **création ou mise à jour de la ressource**.
6. En cas d'erreur → retour d'un **code HTTP approprié** avec un message JSON explicatif.

---

##  5. Installation et Tests Automatisés

### Lancement de l'application
1. Installez les dépendances : `pip install -r requirements.txt`
2. Lancez le serveur : `python run.py`
3. Accédez à la documentation Swagger : `http://127.0.0.1:5000/api/v1/`

### Exécution des tests unitaires (`unittest`)
Nous utilisons des tests automatisés pour garantir la non-régression :
```bash
python3 -m unittest discover tests
