-- Insertion de l'administrateur
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1',
        'admin@hbnb.io',
        'Admin',
        'HBnB',
        '$2a$11$t.nnb.kCjrxtCaWdMUlRKu3Pso8guJJF/97H6SXKCQwsUMfKJXtm',
        TRUE
);

-- Insertion des amenities
INSERT INTO amenities (id, name) VALUES ('83ab8592-3937-4452-8dcc-8a7d9e006eef', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('980ffe62-7c6f-41af-9b0f-ca4e4102b96b', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('b26ac5a7-e36d-4d41-9a9e-8ddc18405ec9', 'Air Conditioning');
