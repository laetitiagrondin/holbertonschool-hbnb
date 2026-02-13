```
---
title: Business Logic Layer - Class Diagram
---
classDiagram
class User {
    +id: UUID
    +first_name: str
    +last_name: str
    +email: str
    +password: str
    +is_admin: bool
    +created: datetime
    +updated: datetime
    +deleted: datetime
    +register(first_name: str, last_name: str, email: str, password: str) User
}
class Place {
    +id: UUID
    +id_owner: UUID
    +title: str
    +description: str
    +price: float
    +latitude: float
    +longitude: float
    +created: datetime
    +updated: datetime
    +deleted: datetime
    +listed_by_place() list[Place]
}
class Review {
    +id: UUID
    +user_id: UUID
    +place_id: UUID
    +created: datetime
    +updated: datetime
    +deleted: datetime
    +listed: list
    +comment: str
    +rating: int
}
class Amenity {
    +id: UUID
    +name: str
    +description: str
    +created: datetime
    +updated: datetime
    +deleted: datetime
    +listed: list
}

User -- Place
User -- Review
Place -- Review
Place o-- Amenity
```
