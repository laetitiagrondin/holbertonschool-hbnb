-- Insertion de l'administrateur
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$trP/B6xIHvMY03Ksdl8gBuUH413r06QIoqpKRrDnZsUjczMGnHo2q',
    TRUE
);

-- Insertion des amenities
INSERT INTO amenities (id, name) VALUES ('e4de9f60-795c-4ff0-af9f-501e7e180a61', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('cec7265e-3ac1-4bdb-aafd-817e190da08d', 'Piscine');
INSERT INTO amenities (id, name) VALUES ('7d66712d-a51d-4e22-9f74-147d3d7abbfb', 'Climatisation');
