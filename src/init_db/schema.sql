-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    address JSONB NOT NULL,
    date_of_birth DATE,
    created_at TIMESTAMP
);

-- INVENTORY TABLE
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_name TEXT UNIQUE NOT NULL,
    available_quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

-- ORDERS TABLE
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_date TIMESTAMP NOT NULL,
    status TEXT CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled', 'out of stock')),
    total NUMERIC(10, 2) NOT NULL
);

-- ORDER_ITEMS TABLE
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_name TEXT NOT NULL REFERENCES inventory(product_name) ON DELETE CASCADE,
    requested_quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);
