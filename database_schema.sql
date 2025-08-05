-- Demo Shop Database Schema
-- SQLite Database: demo_shop.db

-- Create customers table
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    city TEXT,
    signup_date DATE
);

-- Create products table
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price DECIMAL(10,2),
    stock INTEGER
);

-- Create orders table
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert sample data into customers
INSERT INTO customers VALUES
('CUST01', 'Alice', 28, 'New York', '2023-01-02'),
('CUST02', 'Bob', 34, 'Los Angeles', '2023-01-04'),
('CUST03', 'Charlie', 26, 'Chicago', '2023-01-06'),
('CUST04', 'David', 41, 'Houston', '2023-01-08'),
('CUST05', 'Eva', 29, 'Phoenix', '2023-01-10'),
('CUST06', 'Frank', 38, 'San Diego', '2023-01-12'),
('CUST07', 'Grace', 31, 'Dallas', '2023-01-14'),
('CUST08', 'Helen', 27, 'Austin', '2023-01-16'),
('CUST09', 'Ivy', 33, 'San Jose', '2023-01-18'),
('CUST10', 'Jack', 30, 'Seattle', '2023-01-20'),
('CUST11', 'Rishitha', 22, 'Denton', '2023-08-02');

-- Insert sample data into products
INSERT INTO products VALUES
('PROD01', 'Laptop', 'Computers', 1299.00, 25),
('PROD02', 'Phone', 'Electronics', 899.00, 60),
('PROD03', 'Tablet', 'Electronics', 499.00, 45),
('PROD04', 'Headphones', 'Accessories', 149.00, 120),
('PROD05', 'Monitor', 'Computers', 249.00, 70),
('PROD06', 'Keyboard', 'Accessories', 79.00, 200),
('PROD07', 'Mouse', 'Accessories', 39.00, 220),
('PROD08', 'Webcam', 'Accessories', 89.00, 150),
('PROD09', 'Dock', 'Accessories', 129.00, 90),
('PROD10', 'SSD 1TB', 'Computers', 139.00, 80);

-- Insert sample data into orders
INSERT INTO orders VALUES
('ORD01', 'CUST01', 'PROD01', 1, '2024-01-02'),
('ORD02', 'CUST02', 'PROD05', 2, '2024-01-04'),
('ORD03', 'CUST03', 'PROD04', 1, '2024-01-06'),
('ORD04', 'CUST04', 'PROD02', 1, '2024-01-08'),
('ORD05', 'CUST05', 'PROD03', 3, '2024-01-10'),
('ORD06', 'CUST06', 'PROD10', 1, '2024-01-12'),
('ORD07', 'CUST07', 'PROD06', 2, '2024-01-14'),
('ORD08', 'CUST08', 'PROD07', 1, '2024-01-16'),
('ORD09', 'CUST09', 'PROD08', 2, '2024-01-18'),
('ORD10', 'CUST10', 'PROD09', 1, '2024-01-20');