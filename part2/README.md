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
