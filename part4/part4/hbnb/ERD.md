# HBnB - Entity Relationship Diagram
```mermaid
erDiagram
    USER {
        string id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACE {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    REVIEW {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    AMENITY {
        string id PK
        string name
    }

    PLACE_AMENITY {
        string place_id FK
        string amenity_id FK
    }

    USER ||--o{ PLACE : possede
    USER ||--o{ REVIEW : redige
    PLACE ||--o{ REVIEW : recoit
    PLACE ||--o{ PLACE_AMENITY : contient
    AMENITY ||--o{ PLACE_AMENITY : associe
```

Explications des relations

USER → PLACE (possède)

Type 1 → N

Un utilisateur peut posséder plusieurs logements, chaque logement a exactement un propriétaire.

USER → REVIEW (rédige)

Type 1 → N

Un utilisateur peut écrire plusieurs avis, chaque avis appartient à un seul utilisateur.

PLACE → REVIEW (reçoit)

Type 1 → N

Un logement peut recevoir plusieurs avis, chaque avis est lié à un seul logement.

PLACE ↔ AMENITY via PLACE_AMENITY

Relation many-to-many

Un logement peut avoir plusieurs équipements, un équipement peut être lié à plusieurs logements.

PLACE_AMENITY fait le lien proprement pour éviter la duplication.
