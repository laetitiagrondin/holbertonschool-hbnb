## 1. User Registration :

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API (Présentation)
    participant S as UserService (Métier)
    participant M as UserModel
    participant P as Persistance

    C->>A: POST /users [first_name, last_name, email, password]
    A->>A: Valider format JSON
    alt Format JSON invalide
        A-->>C: 400 Bad Request (Invalid JSON)
    end
    
    A->>S: register_user(data)
    S->>M: validate_user_data(data)
    
    alt Données manquantes ou Email invalide
        M-->>S: Validation Error
        S-->>A: Business Logic Error
        A-->>C: 400 Bad Request (Invalid input data)
    else Données Valides
        S->>M: hash_password(password)
        S->>P: insert_user(user_obj)
        P-->>S: user_id
        S-->>A: 201 Created (id, email)
        A-->>C: 201 Created (JSON Response)
    end
```

## 2. Place Creation :

```mermaid
sequenceDiagram
    participant C as Client
    participant A as PlaceAPI
    participant S as PlaceService
    participant M as PlaceModel
    participant P as Persistance

    C->>A: POST /places [data]
    A->>A: Valider Token & Input format
    
    alt Token manquant ou Format invalide
        A-->>C: 400 Bad Request (Unauthorized or Invalid format)
    end

    A->>S: create_place(user_id, data)
    S->>M: validate_place_data(data)
    
    alt Prix < 0 ou Coordonnées invalides
        M-->>S: Validation Error
        S-->>A: Business Logic Error
        A-->>C: 400 Bad Request (Latitude/Longitude out of range)
    else Données Valides
        S->>P: insert_place(place_obj)
        P-->>S: place_id
        S-->>A: 201 Created (id, title)
        A-->>C: 201 Created (JSON Response)
    end
```

## 3. Review Submission :

```mermaid
sequenceDiagram
    participant C as Client
    participant A as ReviewAPI
    participant S as ReviewService
    participant M as ReviewModel
    participant P as Persistance

    C->>A: POST /places/{id}/reviews [comment, rating]
    
    A->>S: create_review(user_id, place_id, data)
    S->>M: validate_rating(rating)
    
    alt Note hors plage (pas 1-5)
        M-->>S: Invalid Rating
        S-->>A: Business Logic Error
        A-->>C: 400 Bad Request (Rating must be between 1 and 5)
    else Note Valide
        S->>P: insert_review(review_obj)
        P-->>S: review_id
        S-->>A: 201 Created (id, comment)
        A-->>C: 201 Created (JSON Response)
    end
```

## 4. Fetching a List of Places :

```mermaid
sequenceDiagram
    participant C as Client
    participant A as PlaceAPI
    participant F as HBnBFacade
    participant R as PlaceRepository
    participant DB as Database

    C->>A: GET /places?filters
    A->>F: get_places(filters)
    
    alt Filtres de pagination invalides (ex: page=0)
        F-->>A: Invalid Pagination
        A-->>C: 400 Bad Request (Invalid pagination parameters)
    else Paramètres Valides
        F->>R: fetch_all(filters)
        R->>DB: SELECT * FROM places WHERE filters
        DB-->>R: Result set
        R-->>F: List<Place>
        F-->>A: return places list
        A-->>C: 200 OK (JSON List)
    end
```
