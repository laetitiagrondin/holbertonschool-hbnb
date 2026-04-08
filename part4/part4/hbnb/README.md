# 🏨 HBnB - Application Web Complète

HBnB est une application web de type AirBnB avec **Backend Flask** et **Frontend HTML/CSS/JS Vanilla**, permettant la gestion des utilisateurs, lieux, équipements et avis, avec authentification sécurisée via **JWT**.

---

## 🎯 Objectifs du Projet

1. Compléter les fichiers HTML/CSS pour correspondre aux spécifications de design.
2. Créer les pages suivantes :
   - Formulaire de login
   - Liste des lieux
   - Détails d’un lieu
   - Formulaire d’ajout d’avis
3. Implémenter l’authentification avec JWT, stockée dans un cookie.
4. Afficher dynamiquement les données depuis l’API via JavaScript.
5. Filtrer les lieux côté client par prix.
6. Respecter les standards HTML/CSS W3C.

---

## 🏗️ Architecture et Design Patterns

### Backend

- **Flask + Flask-RESTX + SQLAlchemy + Bcrypt + JWT**
- **Pattern Facade** (`app/services/facade.py`) :
  - Centralise la logique métier
  - Découple API ↔ Base de données
  - Simplifie la maintenance et l’évolution
  - Gestion centralisée des erreurs et validation des données

### Modèle de Données (ERD)

L'application repose sur quatre entités principales liées entre elles :

- **User** : Gère les comptes et l'authentification (Bcrypt pour le hachage)
- **Place** : Titre, prix, localisation, chambres, salles de bain
- **Amenity** : Liste des équipements disponibles
- **Review** : Liens utilisateur ↔ lieu pour les évaluations

Relations :  

- User → Place (propriétaire)  
- Place → Amenity (many-to-many)  
- Place → Review (one-to-many)  

---

## 🔒 Sécurité et Validation

### Gestion des Identités (JWT)

- Jetons JWT pour l'authentification
- Contiennent les informations utilisateur (ID, rôle admin)
- Vérifiés à chaque requête sensible (`POST`, `PUT`, `DELETE`)

### Protection contre les attaques courantes

- **SQL Injection** : ORM SQLAlchemy paramètre les requêtes automatiquement
- **XSS (Cross-Site Scripting)** : Échappement côté frontend
- **CORS** : Autorise uniquement les origines de confiance (localhost)
- **Règles métier** : 
  - Un utilisateur ne peut pas noter son propre lieu
  - Un utilisateur ne peut publier qu’un seul avis par lieu

---

## 🌐 Frontend et Design

### Pages et Objectifs

1. **Login (`login.html`)**
   - Formulaire email/mot de passe
   - AJAX POST vers API `/login`
   - Stockage JWT dans cookie
   - Redirection vers `index.html` après login réussi
   - Affichage d’erreur si login échoue

2. **Liste des lieux (`index.html`)**
   - Affichage des lieux sous forme de **cartes**
   - Informations : nom, prix, bouton “View Details”
   - Filtrage côté client par prix
   - Login link visible uniquement si non connecté

3. **Détails d’un lieu (`place.html`)**
   - Informations détaillées : hôte, description, prix, équipements
   - Liste des avis existants sous forme de cartes
   - Formulaire ajout d’avis visible uniquement si connecté

4. **Ajouter un avis (`add_review.html`)**
   - Accessible uniquement aux utilisateurs authentifiés
   - Redirection vers `index.html` si non connecté
   - AJAX POST vers API `/reviews` avec JWT
   - Affichage message succès ou erreur

### Structure HTML/CSS

- **Header** : logo (`class="logo"`) + bouton login (`class="login-button"`)
- **Footer** : texte “All rights reserved”
- **Navigation** : liens vers `index.html` et `login.html`
- **Cartes de lieux** : `class="place-card"`  
  - Margin : 20px
  - Padding : 10px
  - Border : 1px solid #ddd
  - Border-radius : 10px
- **Cartes d’avis** : `class="review-card"` (mêmes styles)
- **Détails** : `class="place-details"` et `place-info`
- **Formulaire ajout d’avis** : `class="add-review"` et `form`

---

## 🛠️ JavaScript et Fonctionnalités

- **Vérification Auth JWT** : présence du cookie `token` pour afficher/masquer login link ou form
- **Login**
  - Form submit AJAX POST `/login`
  - Stockage JWT dans cookie
  - Redirection vers `index.html`
- **Affichage Liste des Lieux**
  - Fetch GET vers API `/places`
  - Création dynamique des éléments DOM
  - Filtrage par prix via dropdown
- **Détails d’un lieu**
  - Fetch GET vers API `/places/:id`
  - Affichage dynamique : nom, description, prix, équipements, avis
  - Formulaire ajout d’avis visible uniquement si authentifié
- **Ajout d’avis**
  - Form submit AJAX POST `/reviews` avec JWT
  - Gestion du succès et des erreurs

---

## 🧪 Tests

- Login valide et invalide
- Stockage JWT et redirection correcte
- Filtrage prix côté client
- Accès au formulaire d’avis uniquement si connecté
- Chargement correct des détails de lieu

---

## ⚙️ Installation

### Backend

```bash
pip install -r requirements.txt
python3 run.py
Frontend
Ouvrir index.html via Live Server ou tout autre serveur local
Ports recommandés : 5500 ou 8000
🔧 Seeding et Données Démonstration
Script automatique au démarrage (app/__init__.py)
Utilisateurs :
Admin : admin@hbnb.com / admin123
Test : test@hbnb.com / password123
Lieux et équipements pré-remplis pour tests
📌 Endpoints Principaux
Méthode	Endpoint	Description	Auth Requise
POST	/api/v1/auth/login	Connexion et récupération du JWT	Non
GET	/api/v1/places/	Liste tous les lieux	Non
POST	/api/v1/reviews/	Ajouter un avis sur un lieu	Oui (JWT)
PUT	/api/v1/users/me	Modifier son profil	Oui (JWT)

## W3C Validation

Toutes les pages HTML et le fichier de style CSS ont été validés avec succès (0 erreur, 0 avertissement). Vous pouvez consulter les rapports officiels ci-dessous :

| Fichier / Page | Statut | Rapport de Validation (PDF) |
|:--- |:---:|:--- |
| `index.html` | ✅ Valide | [Consulter le rapport](./part4/part4/hbnb/w3c_reports/index_w3c.pdf) |
| `login.html` | ✅ Valide | [Consulter le rapport](./part4/part4/hbnb/w3c_reports/login_w3c.pdf) |
| `place.html` | ✅ Valide | [Consulter le rapport](./part4/part4/hbnb/w3c_reports/place_w3c.pdf) |
| `add_review.html` | ✅ Valide | [Consulter le rapport](./part4/part4/hbnb/w3c_reports/addreview_w3c.pdf) |
| `styles.css` | ✅ Valide | [Consulter le rapport](./part4/part4/hbnb/w3c_reports/css_w3c.pdf) |

> **Note :** La conformité a été vérifiée via le [Nu Html Checker](https://validator.w3.org/nu/) et le validateur CSS du W3C.

👥 Auteur
Luidgi — Développement Backend & Intégration Frontend
