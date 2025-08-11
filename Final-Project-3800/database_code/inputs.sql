SE cd_database;

-- Genre
INSERT INTO genre (genre_id, genre_name) VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Jazz');

INSERT INTO vendors (vendor_id, vendor_name, email_address, shipping_address, billing_address) VALUES
(1, 'MusicWorld', 'contact@musicworld.com', 1, 2),
(2, 'CDPlanet', 'info@cdplanet.com', 3, 4);

-- Address
INSERT INTO addresses  (address_id, line1, line2, city, state, zip, country, customer_id, vendor_id) VALUES
(1, '123 Main St', '', 'New York', 'NY', '10001', 'USA', NULL, 1),
(2, '456 Broadway', 'Apt 2', 'New York', 'NY', '10002', 'USA', NULL, 1),
(3, '789 Market St', '', 'San Francisco', 'CA', '94103', 'USA', NULL, 2),
(4, '101 First Ave', '', 'San Francisco', 'CA', '94105', 'USA', NULL, 2),
(5, '555 Elm St', '', 'Chicago', 'IL', '60601', 'USA', 1, NULL),
(6, '777 Oak St', '', 'Chicago', 'IL', '60602', 'USA', 2, NULL);

-- Customer
INSERT INTO customers (customer_id, first_name, last_name, email, shipping_address, billing_address) VALUES
(1, 'Alice', 'Smith', 'alice.smith@email.com', 5, 5),
(2, 'Bob', 'Johnson', 'bob.johnson@email.com', 6, 6);

-- Administrator
INSERT INTO administrator (admin_id, first_name, last_name, email) VALUES
(1, 'Carol', 'Williams', 'carol.williams@email.com'),
(2, 'David', 'Brown', 'david.brown@email.com');

-- Cd
INSERT INTO cd (cd_id, cd_name, artist, genre_id, release_date, price, quantity, vendor_id) VALUES
(1, 'Greatest Hits', 'Queen', 1, '1981-10-26', 15.99, 10, 1),
(2, 'Thriller', 'Michael Jackson', 2, '1982-11-30', 13.99, 20, 2),
(3, 'Kind of Blue', 'Miles Davis', 3, '1959-08-17', 12.99, 15, 1);

-- Order
INSERT INTO orders  (order_id, customer_id, purchase_date, is_rental, tax_amount, ship_date, order_status, shipped_amount, card_type, card_number, card_expiration, card_cvv, date_due, billing_address) VALUES
(1, 1, '2024-06-01', FALSE, 1.50, '2024-06-02', 'Shipped', 17.49, 'Visa', '4111111111111111', '2026-12-31', '123', '456', 5),
(2, 2, '2024-06-03', TRUE, 1.20, '2024-06-04', 'Processing', 14.19, 'MasterCard', '5500000000000004', '2025-11-30', '456', '2024-07-03', 6);

-- Order_items
INSERT INTO order_items (item_id, order_id, cd_id, quantity) VALUES
(1, 1, 1, 1),
(2, 1, 3, 2),
(3, 2, 2, 1);