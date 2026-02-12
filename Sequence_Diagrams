sequenceDiagram
    participant Client
    participant UserAPI
    participant HBnBFacade
    participant User
    participant UserRepository
    participant Database

    Client->>UserAPI: POST /users (registration data)
    UserAPI->>UserAPI: Validate input
    UserAPI->>HBnBFacade: create_user(data)
    HBnBFacade->>User: Instantiate User
    HBnBFacade->>User: Hash password
    HBnBFacade->>UserRepository: save(User)
    UserRepository->>Database: INSERT user
    Database-->>UserRepository: Success
    UserRepository-->>HBnBFacade: User saved
    HBnBFacade-->>UserAPI: Return user object
    UserAPI-->>Client: 201 Created

sequenceDiagram
    participant Client
    participant PlaceAPI
    participant HBnBFacade
    participant Place
    participant PlaceRepository
    participant Database

    Client->>PlaceAPI: POST /places
    PlaceAPI->>PlaceAPI: Validate token & input
    PlaceAPI->>HBnBFacade: create_place(user_id, data)
    HBnBFacade->>Place: Instantiate Place
    HBnBFacade->>PlaceRepository: save(Place)
    PlaceRepository->>Database: INSERT place
    Database-->>PlaceRepository: Success
    PlaceRepository-->>HBnBFacade: Place saved
    HBnBFacade-->>PlaceAPI: Return place object
    PlaceAPI-->>Client: 201 Created

sequenceDiagram
    participant Client
    participant ReviewAPI
    participant HBnBFacade
    participant Review
    participant ReviewRepository
    participant Database

    Client->>ReviewAPI: POST /places/{id}/reviews
    ReviewAPI->>ReviewAPI: Validate input
    ReviewAPI->>HBnBFacade: create_review(user_id, place_id, data)
    HBnBFacade->>HBnBFacade: Verify place exists
    HBnBFacade->>Review: Instantiate Review
    HBnBFacade->>ReviewRepository: save(Review)
    ReviewRepository->>Database: INSERT review
    Database-->>ReviewRepository: Success
    ReviewRepository-->>HBnBFacade: Review saved
    HBnBFacade-->>ReviewAPI: Return review object
    ReviewAPI-->>Client: 201 Created

sequenceDiagram
    participant Client
    participant PlaceAPI
    participant HBnBFacade
    participant PlaceRepository
    participant Database

    Client->>PlaceAPI: GET /places?filters
    PlaceAPI->>HBnBFacade: get_places(filters)
    HBnBFacade->>PlaceRepository: fetch_all(filters)
    PlaceRepository->>Database: SELECT * FROM places WHERE filters
    Database-->>PlaceRepository: Result set
    PlaceRepository-->>HBnBFacade: List<Place>
    HBnBFacade-->>PlaceAPI: Return places list
    PlaceAPI-->>Client: 200 OK (JSON list)
