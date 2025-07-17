create table CD ( 
    CD_ID INT PRIMARY KEY,
    CD_Name VARCHAR(100) NOT NULL,
    Artist VARCHAR(100) NOT NULL,
    Genera_ID INT NOT NULL,
    Release_Date DATE NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    vendor_ID INT NOT NULL,
    discount_percent DECIMAL(5, 2) NULL,
    FOREIGN KEY (vendor_ID) REFERENCES Vendor(vendor_ID),
    FOREIGN KEY (Genera_ID) REFERENCES Genera(Genera_ID)
);

Create table Genera (
    Genera_ID INT PRIMARY KEY,
    Genera_Name VARCHAR(100) NOT NULL
);

Create table order (
    order_ID INT PRIMARY KEY,
    customer_ID INT NOT NULL,
    purchase_date DATE NOT NULL,
    is_rental BOOLEAN NOT NULL,
    tax_amount DECIMAL(10, 2) NOT NULL,
    ship_date DATE NOT NULL,
    order_status VARCHAR(50) NOT NULL,
    shipped_amount DECIMAL(10, 2) NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    card_expiration DATE NOT NULL,
    card_cvv VARCHAR(4) NOT NULL,
    Date_due DATE NOT NULL,
    billing_address VARCHAR(255) NOT NULL,
    FOREIGN KEY (billing_address) REFERENCES address(address_ID),
    FOREIGN KEY (customer_ID) REFERENCES Customer(customer_ID)

);

create table order_items (
    item_ID INT PRIMARY KEY,
    order_ID INT NOT NULL,
    CD_ID INT NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_ID) REFERENCES order(order_ID),
    FOREIGN KEY (CD_ID) REFERENCES CD(CD_ID)

);

create table Customer (
    customer_ID INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    shipping_address INT NOT NULL,
    billing_address INT NOT NULL,
    customer_username VARCHAR(50) NOT NULL UNIQUE,
    customer_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (shipping_address) REFERENCES address(address_ID),
    FOREIGN KEY (billing_address) REFERENCES address(address_ID)
);

create table address (
    customer_ID INT NOT NULL,
    address_ID INT PRIMARY KEY,
    street VARCHAR(100) NOT NULL,
    street2 VARCHAR(100) NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_ID) REFERENCES Customer(customer_ID)
);

create table vendor (
    vendor_ID INT PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    vendor_username VARCHAR(50) NOT NULL UNIQUE,
    vendor_password VARCHAR(255) NOT NULL,
    email_address VARCHAR(100) NOT NULL UNIQUE
    shipping_address INT NOT NULL,
    billing_address INT NOT NULL,
    FOREIGN KEY (shipping_address) REFERENCES address(address_ID),
    FOREIGN KEY (billing_address) REFERENCES address(address_ID)
);


Create table administrator (
    admin_ID INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    admin_username VARCHAR(50) NOT NULL UNIQUE,
    admin_password VARCHAR(255) NOT NULL
);