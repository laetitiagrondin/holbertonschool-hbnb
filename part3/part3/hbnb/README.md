Introduction à la partie 2: Mise en œuvre de la logique d'entreprise et des points de terminaison API

Dans cette phase du projet HBnB, vous allez mettre en œuvre la fonctionnalité de base de l'application en utilisant Python et Flask. Cela impliquera de construire les couches logiques de présentation et d'affaires, et de définir les classes, les méthodes et les points de terminaison d'API essentiels, en fonction de la conception développée dans la partie précédente.

L'objectif est de donner vie à l'architecture documentée en créant la structure du projet, en développant la logique commerciale et en mettant en œuvre des fonctionnalités clés telles que la gestion des utilisateurs, des lieux, des critiques et des commodités.
Vision et portée du projet

Cette partie est axée sur la création d'une base fonctionnelle et évolutive pour l'application. Vous travaillerez sur:

    Business Logic Layer: Construire les modèles de base et la logique qui génèrent les fonctionnalités de l'application. Cela inclut la définition des relations, la gestion de la validation des données et la gestion des interactions entre les différents composants.

    Couche de présentation: Définition des services et des points de terminaison API à l'aide de Flask et flask-restx. Vous structurerez les points de terminaison logiquement, en assurant des chemins et des paramètres clairs pour chaque opération.

Objectifs d'apprentissage

Cette partie du projet est conçue pour vous aider à atteindre les résultats d'apprentissage suivants:

    Mettre en place la structure du projet:
        Organisez le projet en une architecture modulaire, en suivant les meilleures pratiques pour les applications Python et Flask.
        Créez les paquets nécessaires pour les couches Présentation et Logique d'entreprise.

    Mettre en œuvre la couche logique d'entreprise:

    Comprendre comment traduire des conceptions documentées en code de travail par:
        Développer les classes de base pour la logique d'entreprise, y compris les entités d'utilisateur, de lieu, de révision et d'équipement.
        Mettre en œuvre des relations entre les entités et définir la façon dont elles interagissent au sein de l’application.
        Mettre en œuvre le motif de façade pour simplifier la communication entre les couches Présentation et Business Logic.

    Créez des terminaux d'API RESTful:
        Mettre en œuvre les points de terminaison API nécessaires pour gérer les opérations CRUD pour les utilisateurs, les lieux, les avis et les équipements.
        Utilisation flask-restxpour définir et documenter l'API, en assurant une structure claire et cohérente.
        Implémentez la sérialisation de données pour renvoyer des attributs étendus pour les objets associés. Par exemple, lors de la récupération d'un lieu, l'API doit inclure des détails tels que celui du propriétaire first_name, last_name, et commodités pertinentes.

    Tester et valider l'API:
        Rédigez des tests pour valider le comportement des classes de logique d'entreprise.
        Assurez-vous que les réponses de l'API sont cohérentes avec le comportement attendu.
        Assurez-vous que chaque point de terminaison fonctionne correctement et gère les cas de bord de manière appropriée.



Créer la structure du répertoire de projet :

Votre projet doit être organisé dans la structure suivante:

hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md

Explication:

    Le app/répertoire contient le code d'application de base.
    Le api/sous-répertoire abrite les terminaux API, organisés par version (v1/).
    Le models/sous-répertoire contient les classes logiques d'entreprise (p. ex., user.py, place.py).
    Le services/Le sous-répertoire est l'endroit où le motif Facade est implémenté, en gérant l'interaction entre les couches.
    Le persistence/Le sous-répertoire est l'endroit où le dépôt en mémoire est implémenté. Cela sera ensuite remplacé par une solution de base de données utilisant SQL Alchemy.
    run.pyest le point d'entrée pour l'exécution de l'application Flask.
    config.pysera utilisé pour configurer les variables d'environnement et les paramètres d'application.
    requirements.txtIl listera tous les paquets Python nécessaires au projet.
    README.mdContiendra un bref aperçu du projet.

