PROJET HBnB : Documentation Technique Complète

Architecture et Conception du Système Version : 1.0

Date : Mars 2026
1. Introduction
1.1 Objectif du Document

Ce document constitue le plan directeur complet du projet HBnB (Holberton B&B). Il fournit une référence détaillée de l'architecture du système, de la conception des composants et des interactions entre les couches. Ce guide accompagne les développeurs et architectes tout au long de l'implémentation pour garantir la cohérence du système.
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
