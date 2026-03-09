PROJET HBnB

Architecture et Conception du Système Version : 1.0

Date : Mars 2026
1. Introduction
1.1 Objectif du Document

Ce document constitue le plan directeur complet du projet HBnB. Il fournit une référence détaillée de l'architecture du système, de la conception des composants et des interactions entre les couches. Ce guide accompagne les développeurs et architectes tout au long de l'implémentation pour garantir la cohérence du système.
1.2 Portée du Document

Cette documentation couvre :

    L'architecture de haut niveau et le modèle en couches.

    La couche de logique métier (entités et relations).

    Les flux d'interaction API et les séquences de traitement.

    Les décisions de conception et leurs justifications.

1.3 Présentation du Projet

HBnB est une plateforme de réservation de logements permettant aux utilisateurs de publier des propriétés, de rechercher des hébergements et de gérer des réservations. Le système orchestre des entités clés : Utilisateurs, Logements, Équipements et Avis.
2. Architecture de Haut Niveau
2.1 Structure en Couches

L'application adopte une layered architecture (architecture en couches) pour séparer les préoccupations :

    Couche de Présentation : Gère les interactions via une API RESTful, la validation des entrées et les réponses HTTP.

    Couche de Logique Métier : Contient le cœur fonctionnel, les entités (Utilisateur, Logement, etc.) et les règles métier.

    Couche de Persistance : Abstrait le stockage des données via des Repositories et gère les transactions.

2.2 Le Patron Facade

Le patron Facade (FaçadeHBnB) sert de point d'entrée unique entre la présentation et la logique métier. Elle orchestre les appels aux services, gère les transactions complexes et découple les changements internes de l'interface externe.
3. Couche de Logique Métier
3.1 Diagramme de Classes Détaillé

Le diagramme suivant structure les entités, leurs attributs et leurs méthodes de validation :
3.2 Entités Principales
Entité	Attributs Clés	Méthodes Principales
Utilisateur	id (UUID), email, mot_de_passe, est_admin	inscrire(), se_connecter(), hacher_mot_de_passe()
Logement	id (UUID), titre, prix, latitude, longitude	creer_logement(), calculer_note_moyenne(), est_disponible()
Avis	id, commentaire, note (1-5), id_utilisateur	creer_avis(), valider_note()
Équipement	id, nom, description	creer_equipement(), modifier_equipement()
3.3 Relations et Cardinalités

    Utilisateur ↔ Logement (1:N) : Un utilisateur possède zéro ou plusieurs logements.

    Logement ↔ Avis (1:N) : Un logement reçoit plusieurs avis, chaque avis est lié à un seul logement.

    Logement ↔ Équipement (N:M) : Relation gérée via l'entité de liaison LogementEquipement.

4. Flux d'Interaction API
4.1 Séquence de Traitement (Exemple : Recherche de Logements)

Les diagrammes de séquence illustrent le flux de données entre les composants lors d'un appel API :

Processus type :

    Le Client envoie une requête GET à la Couche Présentation.

    L'API extrait les paramètres et appelle le ServiceLieu (Logique Métier).

    Le ServiceFiltre valide les critères (prix > 0, limites de pagination).

    La Couche Persistance exécute la requête SQL et retourne les données brutes.

    Le résultat est formaté et renvoyé au client avec un code 200 OK.

5. Décisions de Conception

    Utilisation d'UUID : Garantit l'unicité globale sans coordination centrale et renforce la sécurité des identifiants.

    Horodatage Automatique : Champs date_creation et date_mise_a_jour sur chaque entité pour l'audit et la traçabilité.

    Validation Centralisée : Logique de validation intégrée aux entités métier pour assurer la cohérence et faciliter les tests unitaires.

# HBnB Technical Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Architecture](#high-level-architecture)
3. [Business Logic Layer](#business-logic-layer)
4. [API Interaction Flow](#api-interaction-flow)
5. [Conclusion](#conclusion)



## 1. Introduction

**Objectif du document:**  
Ce document fournit une référence technique complète pour le projet HBnB, compilant les diagrammes et explications pour guider le développement et clarifier l’architecture.

**Aperçu du projet HBnB:**  
HBnB est une application de location de logements permettant aux utilisateurs de créer des comptes, gérer leurs annonces, réserver des logements et laisser des avis.  
Ce document décrit l’architecture globale, la logique métier et les flux d’interactions API.



## 2. High-Level Architecture

**Diagramme de packages:**  
![High-Level Package Diagram](diagrams/package_diagram.png)

**Notes explicatives:**  
- **But:** visualiser la structure globale et les modules principaux.  
- **Composants clés:** `app`, `models`, `services`, `api`.  
- **Décisions de conception:** architecture en couches et pattern façade pour isoler responsabilités et faciliter la maintenance.  
- **Lien avec l’architecture globale:** montre comment les modules interagissent et isolent la logique métier de l’interface utilisateur/API.



## 3. Business Logic Layer

**Diagramme de classes détaillé:**  
![Class Diagram](diagrams/class_diagram.png)

**Notes explicatives:**  
- **But:** définir les entités principales et leurs relations.  
- **Composants clés:**  
  - `Utilisateur`: gestion du compte et de l’authentification  
  - `Logement`: gestion des annonces et disponibilité  
  - `Avis`: création et gestion des commentaires  
  - `Equipement` et `LogementEquipement`: gestion des équipements  
- **Relations importantes:**  
  - Association `Utilisateur → Logement`  
  - Composition `Logement → Avis`  
  - Many-to-Many via `LogementEquipement`  
- **Décisions de conception:** UUID pour identifiants uniques, validation côté modèle, séparation logique métier/API.



## 4. API Interaction Flow

### 4.1 Création d’utilisateur (POST /api/v1/users/)
![Sequence Create User](diagrams/sequence_create_user.png)  

**Flux:**  
1. L’utilisateur envoie un JSON avec `first_name`, `last_name`, `email` et `password`.  
2. L’API appelle la couche service pour valider et enregistrer l’utilisateur.  
3. Retour : `201 Created` avec l’ID et informations de l’utilisateur.  
4. Si l’email existe déjà, `400 Bad Request` avec message explicite.


### 4.2 Mise à jour d’utilisateur (PUT /api/v1/users/<id>)
![Sequence Update User](diagrams/sequence_update_user.png)  

**Flux:**  
1. L’utilisateur envoie les champs à modifier (`first_name`, `last_name`, `email`, etc.).  
2. L’API valide les données.  
3. Si les données sont invalides (ex: email mal formé) → `400 Bad Request`.  
4. Si valide → mise à jour dans le modèle → `200 OK`.


### 4.3 Suppression d’utilisateur (DELETE /api/v1/users/<id>)
![Sequence Delete User](diagrams/sequence_delete_user.png)  

**Flux:**  
1. L’utilisateur ou l’administrateur envoie la requête de suppression.  
2. L’API supprime l’utilisateur du modèle.  
3. Retour : `204 No Content`.


### 4.4 Vérification email unique
![Sequence Check Email](diagrams/sequence_check_email.png)  

**Flux:**  
1. Lors de la création d’un nouvel utilisateur, le service vérifie si l’email est déjà enregistré.  
2. Si doublon → `400 Bad Request` avec message “Email already registered”.  
3. Si unique → création réussie.


**Notes générales sur les API:**  
- Endpoints RESTful avec codes HTTP explicites (`201`, `200`, `204`, `400`).  
- Validation critique côté serveur pour garantir la cohérence des données.  
- Séparation **API → Service → Modèle** pour testabilité et extensibilité.
