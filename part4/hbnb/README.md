# HBnB - Front-End Web Application

## Description

HBnB est une application web permettant aux utilisateurs de :
* consulter des lieux
* filtrer selon le prix
* voir les détails d'un lieu
* ajouter des avis.

Ce projet implémente un **front-end en Javascript pur (Vanilla JS)** qui communique avec une API backend via des requêtes AJAX ('fetch').

---

## Objectifs

* Implémenter l'authentification utilisateur avec JWT
* Afficher dynamiquement les lieux depuis une API
* Filtrer les lieux côté client
* Afficher les détails d'un lieu
* Permettre aux utilisateurs connectés d'ajouter des avis

---

## Fonctionnalités

### Authentification (login.html)

* Connexion via formulaire
* Envoi des identifiants à l'API
* Stockage du JWT dans un cookie
* Redirection vers la page principale après connexion

---

### Liste des lieux (index.html)

* Récupération des lieux via l'API
* Affichage dynamique avec JavaScript
* Filtrage par prix :
    * 10
    * 50
    * 100
    * All

---

### Détails d'un lieu (place.html)

* Récupération de l'ID depuis l'URL
* Affichage :
    * Nom
    * Prix
    * Description
    * Équipements
    * Avis
* Affichage du formulaire d'avis seulement si connecté

---

Ajout d'un avis (add_review.html)

* Vérification de l'authentification
* Redirection si non connecté
* Envoi de l'avis via POST
* Affichage d'un message de succès ou d'erreur
